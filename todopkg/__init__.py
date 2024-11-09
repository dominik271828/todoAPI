# we're using the app factory pattern, so todopkg is a python package (a collection of modules)
from flask import Flask

def create_app():
    # instance_relative_config searches for an 'instance' folder one directory up from the module
    # it is where we put our config
    # instance folder should not be under version control
    app = Flask(__name__, instance_relative_config=True)
    # because of 'with app.app_context()' i can use current_app.instance_path inside the config.py folder
    with app.app_context():
        app.config.from_pyfile('config.py')
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import todolist
    app.register_blueprint(todolist.bp)

    return app