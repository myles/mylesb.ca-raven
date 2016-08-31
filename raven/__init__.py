from raven.app import create_app

__version__ = '0.1.0'
__project_name__ = 'raven'
__project_url__ = 'https://github.com/myles/raven'

app = create_app()

port = int(os.environ.get("PORT", 5000))
host = str(os.environ.get("HOST", '0.0.0.0'))

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
