from os.path import join, dirname

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean

from dotenv import load_dotenv

from raven.app import create_app

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = create_app()

manager = Manager(app)

manager.add_command('runserver', Server())
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())

if __name__ == '__main__':
    manager.run()
