import os.path
from os import environ

from fabric import api
from fabric.utils import puts, abort
from fabric.contrib.files import exists

api.env.hosts = ['bear']
api.env.use_ssh_config = True

api.env.supervisord_name = 'mylesb.ca-raven'

# Directories
api.env.root_dir = '/srv/www/mylesb.ca/raven'
api.env.proj_dir = os.path.join(api.env.root_dir, 'app')
api.env.logs_dir = os.path.join(api.env.root_dir, 'logs')
api.env.html_dir = os.path.join(api.env.root_dir, 'html')
api.env.venv_dir = os.path.join(api.env.root_dir, 'venv')

# Python Bullshit
api.env.venv_python = os.path.join(api.env.venv_dir, 'bin/python')
api.env.venv_pip = os.path.join(api.env.venv_dir, 'bin/pip')

# Git Bullshit
api.env.repo = 'https://github.com/myles/mylesb.ca-raven.git'
api.env.remote = 'origin'
api.env.branch = 'master'

api.env.dotenv = {}

with open(os.path.join(os.path.dirname(__file__), '.env'), 'r') as fobj:
    for line in fobj:
        line = line.strip()

        if not line or line.startswith('#') or '=' not in line:
            continue

        k, v = line.split('=', 1)
        k, v = k.strip(), v.strip()

        api.env.dotenv[k] = v.strip("'")


@api.task
def setup():
    """
    Setup the deploy server.
    """
    supervisor('stop', warn_only=True)
    supervisor('remove', warn_only=True)

    # Make a bunch of the directories.
    api.sudo('mkdir -p {0}'.format(' '.join([api.env.proj_dir,
                                             api.env.logs_dir,
                                             api.env.html_dir,
                                             api.env.venv_dir])))

    # Make sure the directories are writeable by me.
    api.sudo('chown myles:myles {0}'.format(' '.join([api.env.proj_dir,
                                                      api.env.html_dir,
                                                      api.env.venv_dir])))

    if not exists(os.path.join(api.env.proj_dir, '.git')):
        # Clone the GitHub Repo
        with api.cd(api.env.proj_dir):
            api.run('git clone {repo} .'.format(**api.env))

    # Createh virtual environment.
    if not exists(os.path.join(api.env.venv_dir, 'bin/python')):
        api.run('virtualenv '
                '--python=/usr/bin/python3.4 {venv_dir}'.format(**api.env))

    # Install the dependencies.
    pip_upgrade()

    # Put the enovirment vairables on the server.
    with api.cd(api.env.proj_dir):
        api.put('.env', '.env')

    # Setup supervisord service
    with api.cd(api.env.proj_dir):
        api.sudo('foreman export --user=myles --app={supervisord_name} '
                 '--root={proj_dir} --log={logs_dir} --port=5001 supervisord '
                 '/etc/supervisor/conf.d'.format(**api.env))

    # Load and start the supervisord config.
    supervisor('load')
    supervisor('start')


@api.task
def python_version():
    """
    Return the Python version on the server for testing.
    """
    with api.cd(api.env.proj_dir):
        api.run("{venv_python} -V".format(**api.env))


@api.task
def update_code():
    """
    Update to the latest version of the code.
    """
    with api.cd(api.env.proj_dir):
        api.run('git reset --hard HEAD')
        api.run('git checkout {branch}'.format(**api.env))
        api.run('git pull {remote} {branch}'.format(**api.env))


@api.task
def pip_upgrade():
    """
    Upgrade the third party Python libraries.
    """
    with api.cd(api.env.proj_dir):
        api.run('{venv_pip} install --upgrade -r '
                'requirements.txt'.format(**api.env))


@api.task
def supervisor(command, warn_only=False):
    """Interact with the supervisord process."""
    name = api.env.supervisord_name
    api.sudo('supervisorctl {command} {name}'.format(command=command,
                                                     name=name),
             warn_only=warn_only)


@api.task
@api.runs_once
def register_deployment(git_path):
    """Register the Deployment with Opbeat."""
    with(api.lcd(git_path)):
        opbeat_config = {
            'revision': api.local('git log -n 1 --pretty="format:%H"',
                                  capture=True),
            'branch': api.local('git rev-parse --abbrev-ref HEAD',
                                capture=True),
            'org_id': api.env.dotenv['RAVEN_OPBEAT_ORGANIZATION_ID'],
            'app_id': api.env.dotenv['RAVEN_OPBEAT_APP_ID'],
            'secret_token': api.env.dotenv['RAVEN_OPBEAT_SECRET_TOKEN']
        }

        api.local('curl https://intake.opbeat.com/api/v1/organizations/'
                  '{org_id}/apps/{app_id}/releases/ -H "Authorization: Bearer '
                  '{secret_token}" -d rev="{revision}" -d branch="{branch}" '
                  '-d status=completed'.format(**opbeat_config))


@api.task
def ship_it():
    """
    Deploy the application.
    """
    # Check to make sure that there isn't any unchecked files
    git_status = api.local('git status --porcelain', capture=True)

    if git_status:
        abort('There are unchecked files.')

    # Push the repo to the remote
    api.local('git push {remote} {branch}'.format(**api.env))

    # Put the config.json file on the remote server
    with api.cd(api.env.proj_dir):
        api.put('config.json', 'config.json')

    # The deploy tasks
    update_code()
    pip_upgrade()
    supervisor('restart')

    register_deployment('.')

    # Draw a ship
    puts("                           |    |    |                           ")
    puts("                          )_)  )_)  )_)                          ")
    puts("                         )___))___))___)\                        ")
    puts("                        )____)____)_____)\\                      ")
    puts("                      _____|____|____|____\\\__                  ")
    puts("             ---------\                   /---------             ")
    puts("               ^^^^^ ^^^^^^^^^^^^^^^^^^^^^                       ")
    puts("                 ^^^^      ^^^^     ^^^    ^^                    ")
    puts("                      ^^^^      ^^^                              ")
