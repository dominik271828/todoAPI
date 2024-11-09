import sqlite3

import click
from flask import current_app, g

def get_user(username):
    db = get_db()
    query = "SELECT id FROM user WHERE username = ?"
    try:
        data = db.execute(query, (username, )).fetchone()
        db.commit() 
    except:
        return None
    else:
        if data is not None:
            return data['id']
        else:
            return None

def get_taskStatus(taskname):
    db = get_db()
    query = "SELECT id FROM statusTable WHERE statusName = ?"
    try:
        data = db.execute(query, (taskname, )).fetchone()
        db.commit() 
    except:
        return None
    else:
        if data is not None:
            return data['id']
        else:
            return None

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            # detect_types=sqlite3.PARSE_DECLTYPES
        )
        # This makes the database return database rows as 'Rows' instance, which behave like dictionaries
        # As opposed to the tuple default
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

#sqlite3.register_converter(
#    "timestamp", lambda v: datetime.fromisoformat(v.decode())
#)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
