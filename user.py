from db import create_user, login_user, create_tables

class User:
    def __init__(self, db, email, password):
        self.db = db
        self.email = email
        self.password = password
        self.id = None
    
    def create_tables(self):
        create_tables(self.db)

    def register(self):
        create_user(self.db, self.email, self.password)

    def login(self):
        self.id = login_user(self.db, self.email, self.password)
        return self.id
    
    def __str__(self):
        return f'User {self.email}'
