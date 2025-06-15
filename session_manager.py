import time

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.timeout = 3600  

    def create_session(self, email):
        session_id = str(hash(email + str(time.time())))
        self.sessions[session_id] = {
            'email': email,
            'created_at': time.time(),
            'last_activity': time.time()
        }
        return session_id

    def validate_session(self, session_id):
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if time.time() - session['last_activity'] < self.timeout:
                session['last_activity'] = time.time()
                return True
            else:
                self.end_session(session_id)
        return False

    def end_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]