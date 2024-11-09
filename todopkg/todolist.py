from flask import (Blueprint, request, jsonify)
from todopkg.db import get_db, get_taskStatus, get_user
from todopkg.misc import decodeAuth
from todopkg.auth import verify

bp = Blueprint('todolist', __name__, url_prefix='/todolist')

statusList = ['completed', 'in-progress', 'suspended', 'dropped']

@bp.route("/create_task", methods = ("POST", ))
def create_task():
    # check if necessary headers have been sent, otherwise, return error
    # check if necessary json object properties have been provided 
    # validate if the Authentication header is correct, fetch userid
    if 'Authorization' not in request.headers:
        return "Log in first"
    if 'brief' not in request.json or 'detail' not in request.json or 'taskStatus' not in request.json:
        return "Provide the necessary json data to proceed"
    username, passwd = decodeAuth(request.headers['Authorization'])

    if not verify(username, passwd):
        return "Username or password incorrect"
    status = get_taskStatus(request.json['taskStatus'])
    if status is None:
        return "Incorrect taskStatus value"
    
    # make a query to add the task
    db = get_db()
    query = "INSERT INTO task(brief, detail, taskStatus, taskOwner) VALUES(?, ?, ?, ?)"
    try: 
        db.execute(query, (request.json['brief'], request.json['detail'], status, get_user(username)))
        db.commit()
    except db.IntegrityError:
        return "Insertion failed"
    else:
        return "Task created successfully"

@bp.route("/fetch", methods = ("GET", ))
def fetch():
    # I should make the sql filter, instead of getting all the records and filtering them in python, right?
    db = get_db()
    status = None
    query = "SELECT task.id, task.brief"
    if 'detailed' in request.args:
        query += ", task.detail "
    query += ",statusTable.statusName FROM task INNER JOIN statusTable ON statusTable.id=task.taskStatus"
    if 'status' in request.args:
        status = get_taskStatus(request.args['status']) 
        if status is None:
            return "Incorrect status"
    if status is not None:
        query += f" WHERE taskStatus = {status}"
    try:
        data = db.execute(query).fetchall()
        db.commit()
    except db.IntegrityError:
        return "DATABASE ERROR"
    else:
        return jsonify( [{k: row[k] for k in row.keys()} for row in data] )

@bp.route("/update", methods=('POST', ))
def update():
    # user sends the id, and in json any of the values for: id(compulsory), brief, detail, taskStatus
    # then we validate, whether the user is the owner of that task and send the sql UPDATE query to our database
    db = get_db()
    query = "UPDATE task SET "
    if 'brief' in request.json:
        query += f"brief='{request.json['brief']}' "
    if 'detail' in request.json:
        query += f",detail='{request.json['detail']}'"
    if 'taskStatus' in request.json:
        query += f",taskStatus={get_taskStatus(request.json['taskStatus'])}"

    if 'Authorization' not in request.headers:
        return "Log in first"
    username, passwd = decodeAuth(request.headers['Authorization'])
    if not verify(username, passwd):
        return "Username or password incorrect"
    if 'id' not in request.json:
        return "Id of the task to be updated must be provided"
    query += f"WHERE taskOwner = {get_user(username)} AND id={request.json['id']}"
    
    try:
        if db.execute(query).rowcount < 1:
            return "No changes to the database were made (not existing id, task belonging to a different user?)"
        db.commit()
    except db.IntegrityError:
        return "Failed"
    else:
        return f"Success"

@bp.route('/delete', methods=('POST', ))
def delete():
    # verify user (is login is correct, and if they're the owner of task)
    db = get_db()
    if 'id' not in request.json:
        return "Id of the task to be updated must be provided"
    if 'Authorization' not in request.headers:
        return "Log in first"
    username, passwd = decodeAuth(request.headers['Authorization'])
    if not verify(username, passwd):
        return "Username or password incorrect"
    query = f"DELETE FROM task WHERE id={request.json['id']} AND taskOwner={get_user(username)}"
    try:
        if db.execute(query).rowcount < 1:
            return "No changes to the database were made (invalid id, user not owner of the task?)"
        db.commit()
    except db.IntegrityError:
        return "Failed"
    else:
        return f"Success"