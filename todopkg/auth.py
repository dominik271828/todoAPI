from flask import (Blueprint, request)
from todopkg.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = ('POST',))
def register():
    db = get_db()
    if 'username' not in request.json or 'passwd' not in request.json:
        return "username and passwd need to be provided"
    try:
        query = "INSERT INTO user(username, passwd) VALUES (?, ?)"
        db.execute(query, (request.json['username'], generate_password_hash(request.json['passwd'])))
        db.commit()
    except db.IntegrityError:
        return f"{request.json['username']} already exists, register failed"
    else:
        return f"user {request.json['username']} created successfully"

def verify(username, passwd):
    db = get_db()
    try: 
        query = "SELECT * FROM user WHERE username = ?"
        user = db.execute(query, (username, )).fetchone()
        db.commit()
    except:
        print("VERIFY ERROR")
    else:
        if user is None:
            return False
        if check_password_hash(user['passwd'], passwd):
            return True
        else:
            return False

