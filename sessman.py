import secrets
import datetime

class SessMan:

    def __init__(self):
        self._sessions = {}
        
        
    def new_session(self, username):
        # You may want to verify that a session doesn't
        # already exist for the username here, before 
        # creating a new one, to prevent a Chris attack.
        token = str(secrets.randbits(256))
        
        self._sessions[token] = {'username':username, 'timeout':datetime.datetime.now()}
        
        return token
        
    def validate_session(self, token):
        # Include session timing out here
        return token in self._sessions
        
    # You may also want to create a 
    # "delete_session" routine for removing
    # sessions, either on logout or timeout.