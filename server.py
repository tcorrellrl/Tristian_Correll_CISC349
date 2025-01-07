from flask import Flask, jsonify, request

import pyodbc
import secrets
from appdb import AppDB
from sessman import SessMan


app = Flask(__name__)
cs = "DRIVER={PostgreSQL ODBC Driver(UNICODE)};SERVER=douglasrumbaugh.com;UID=test_user;PWD=cisc349_test$123;DATABASE=test_db"

app_db = AppDB(cs)
sess_man = SessMan()

@app.route('/login', methods=['PUT', 'POST'])
def login():
    
    body = request.get_json()
    username = str(body['username'])
    password = str(body['password']).encode('utf-8')
    
    authenticated = app_db.validate_login(username, password)
    
    if authenticated:
        session_token = sess_man.new_session(username)
        
    resp = jsonify({'valid':authenticated})
    
    if authenticated:
        resp.headers['Session-Token'] = session_token
    
    return resp
        
    
    
@app.route('/logout', methods=['GET'])
def logout():
    # Implement the code for this endpoint. It should
    # remove the user's session token from the manager.
    pass
    
@app.route('/question', methods=['PUT', 'POST'])
def add_question():

    session = request.headers.get('Session-Token')
    
    if session is None or not sess_man.validate_session(session):
        resp = jsonify({"status":"No valid session provided"})
        resp.status_code = 400
        
        return resp

    body = request.get_json()

    q_text = body.get('text')
    q_answer = body.get('answer')
    
    if q_text and q_answer is not None:
        app_db.insert_question(q_text, q_answer)
        msg = {"status":"Success"}
        stat = 200
    else:
        msg = {"status":"Invalid request body"}
        stat = 400
    
    resp = jsonify(msg)
    resp.status_code = stat
    return resp
    
@app.route('/question/<int:q_id>', methods=['GET'])
def get_question(q_id):
    
    session = request.headers.get('Session-Token')
    
    if session is None or not sess_man.validate_session(session):
        resp = jsonify({"status":"No valid session provided"})
        resp.status_code = 400
        
        return resp
        
    question = app_db.get_question(q_id)
    
    if question:
        resp = jsonify(question)
        resp.status_code = 200
    else:
        resp = jsonify({'status':'thingamajig not located'})
        resp.status_code = 404
    
    return resp
    
    
    


if __name__ == '__main__':
    app.run('0.0.0.0')