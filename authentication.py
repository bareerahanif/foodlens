import json
import hashlib
import time
import re
from typing import Dict, Optional, Tuple
from datetime import datetime

class SessionManager:
    
    def __init__(self, session_timeout: int = 3600):
        self.sessions: Dict[str, dict] = {}
        self.session_timeout = session_timeout

    def create_session(self, email: str) -> str:
        session_id = hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()
        self.sessions[session_id] = {
            'email': email,
            'created_at': time.time(),
            'last_activity': time.time()
        }
        return session_id

    def validate_session(self, session_id: str) -> Tuple[bool, Optional[str]]:
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if time.time() - session['last_activity'] < self.session_timeout:
                session['last_activity'] = time.time()
                return True, session['email']
            else:
                self.end_session(session_id)
        return False, None

    def end_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]

    def cleanup_expired_sessions(self) -> None:
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time - session['last_activity'] >= self.session_timeout
        ]
        for session_id in expired_sessions:
            self.end_session(session_id)


class AuthenticationManager:
    
    def __init__(self, db_path: str = 'users_db.json'):
        self.db_path = db_path
        self.users = self._load_users()
        self.session_manager = SessionManager()
        self.login_attempts: Dict[str, dict] = {} 
        self.password_reset_tokens: Dict[str, dict] = {}  

    def _load_users(self) -> Dict[str, dict]:
        try:
            with open(self.db_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_users(self) -> None:
        with open(self.db_path, 'w') as file:
            json.dump(self.users, file, indent=2)

    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password_complexity(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def _encrypt_password(self, password: str) -> str:
        salt = "foodlens_salt_"  
        return hashlib.sha256((salt + password).encode()).hexdigest()

    def _check_login_attempts(self, email: str) -> bool:
        if email in self.login_attempts:
            attempts = self.login_attempts[email]
            if attempts['count'] >= 5:
                if time.time() - attempts['last_attempt'] < 300:  
                    return False
                else:
                    del self.login_attempts[email]
        return True

    def _record_failed_attempt(self, email: str) -> None:
        if email not in self.login_attempts:
            self.login_attempts[email] = {
                'count': 1,
                'last_attempt': time.time()
            }
        else:
            self.login_attempts[email]['count'] += 1
            self.login_attempts[email]['last_attempt'] = time.time()

    def sign_up(self, username: str, email: str, password: str, dob: str) -> Tuple[bool, str]:
        if not username or not email or not password or not dob:
            return False, "All fields are required."
        
        if not self._validate_email(email):
            return False, "Invalid email format."
            
        if email in self.users:
            return False, "Email already registered."
            
        if not self._validate_password_complexity(password):
            return False, "Password must be at least 8 characters with uppercase, lowercase, number, and special character."
            
        try:
            datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD."
            
        self.users[email] = {
            "username": username,
            "email": email,
            "password": self._encrypt_password(password),
            "dob": dob,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_locked": False,
            "tier": "personal"  
        }
        
        self._save_users()
        return True, f"User {username} registered successfully."

    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[str]]:
        if not self._check_login_attempts(email):
            return False, "Too many failed attempts. Please try again later.", None
            
        if email not in self.users:
            self._record_failed_attempt(email)
            return False, "Invalid email or password.", None
            
        if self.users[email].get('is_locked', False):
            return False, "Account is locked. Please contact support.", None
            
        encrypted_password = self._encrypt_password(password)
        if self.users[email]['password'] != encrypted_password:
            self._record_failed_attempt(email)
            return False, "Invalid email or password.", None
            
        if email in self.login_attempts:
            del self.login_attempts[email]
            
        self.users[email]['last_login'] = datetime.now().isoformat()
        self._save_users()
        
        session_id = self.session_manager.create_session(email)
        return True, f"Welcome back, {self.users[email]['username']}!", session_id
    

    def logout(self, session_id: str) -> None:
        self.session_manager.end_session(session_id)

    def validate_session(self, session_id: str) -> Tuple[bool, Optional[str]]:
        return self.session_manager.validate_session(session_id)

    def change_password(self, email: str, current_password: str, new_password: str) -> Tuple[bool, str]:
        if email not in self.users:
            return False, "User not found."
            
        if not self._validate_password_complexity(new_password):
            return False, "New password must be at least 8 characters with uppercase, lowercase, number, and special character."
            
        current_encrypted = self._encrypt_password(current_password)
        if self.users[email]['password'] != current_encrypted:
            return False, "Current password is incorrect."
            
        self.users[email]['password'] = self._encrypt_password(new_password)
        self._save_users()
        return True, "Password changed successfully."

    def generate_password_reset_token(self, email: str) -> Tuple[bool, Optional[str]]:
        if email not in self.users:
            return False, None
            
        token = hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()
        self.password_reset_tokens[token] = {
            'email': email,
            'created_at': time.time(),
            'used': False
        }
        return True, token

    def reset_password_with_token(self, token: str, new_password: str) -> Tuple[bool, str]:
        if token not in self.password_reset_tokens:
            return False, "Invalid or expired token."
            
        token_data = self.password_reset_tokens[token]
        
        if token_data['used']:
            return False, "Token has already been used."
            
        if time.time() - token_data['created_at'] > 3600:  
            return False, "Token has expired."
            
        if not self._validate_password_complexity(new_password):
            return False, "New password must be at least 8 characters with uppercase, lowercase, number, and special character."
            
        email = token_data['email']
        self.users[email]['password'] = self._encrypt_password(new_password)
        token_data['used'] = True
        self._save_users()
        return True, "Password reset successfully."

    def get_user_info(self, email: str) -> Optional[dict]:
        """Get user information without sensitive data."""
        if email in self.users:
            user = self.users[email].copy()
            user.pop('password', None)
            return user
        return None

    def cleanup(self) -> None:
        """Clean up expired sessions and reset tokens."""
        self.session_manager.cleanup_expired_sessions()
        
        current_time = time.time()
        expired_tokens = [
            token for token, data in self.password_reset_tokens.items()
            if current_time - data['created_at'] > 3600 or data['used']
        ]
        for token in expired_tokens:
            del self.password_reset_tokens[token]