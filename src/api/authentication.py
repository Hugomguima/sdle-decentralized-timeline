import json
import os
import hashlib
class Authentication:
    def __init__(self, node):
        self.node = node
        self.action_list = {
            'register': self.register,
            'login': self.login,
        }

    def action(self, action, information):
        return self.action_list[action](information)
    
    def register(self, information):
        username = information['username']
        password = information['password']
        
        try:
            user_info = self.node.get(username)
            
            salt = os.urandom(32) # A new salt for this user
            print(salt)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            if user_info is None:
                user_data = {
                    'salt': salt.hex(),
                    'hash_password': key.hex(),
                    "followers": [],
                    "following": [],
                    "ip": self.node.ip,
                    "port": self.node.port,
                }

                self.node.set(username, json.dumps(user_data))
                user_args = (self.node, username, user_data)
            else:
                raise Exception(f'Registration failed. User {username} already exists')
        except Exception as e:
            print(e)
            exit(1)
        print('Register successful!')
        return user_args

    def login(self, information):
        username = information['username']
        password = information['password']

        try: 
            user_info = self.node.get(username)

            if user_info is not None:
                user_info = json.loads(user_info)
                salt = bytes.fromhex(user_info['salt'])
                key = bytes.fromhex(user_info['hash_password'])
                new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

                if key != new_key:
                    raise Exception(f"Login failed. Password is wrong!")
                
                user_args = (self.node, username, user_info)
            else:
                raise Exception(f"Login failed. User {username} doesn't exist")
                
        except Exception as e:
            print(e)
            exit(1)
        print('Login successful!')
        return user_args