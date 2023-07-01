from flask import Flask
from flaskext.mysql import MySQL

class Database:
    def __init__(self, host, user, password, database):
        self.mysql_instance = MySQL()
        self.cursor = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connected = False
        self.connection = None
    
    def init(self, application_instance: Flask):
        application_instance.config['MYSQL_DATABASE_HOST'] = self.host
        application_instance.config['MYSQL_DATABASE_USER'] = self.user
        application_instance.config['MYSQL_DATABASE_PASSWORD'] = self.password
        application_instance.config['MYSQL_DATABASE_DB'] = self.database
        try:
            self.mysql_instance.init_app(application_instance)
        except Exception as e:
            print(f"Failed to initialize MySQL application, Exception: {e}")
    
    def connect(self):
        if self.connected is False:
            self.connected = True
            self.connection = self.mysql_instance.connect()
        
    def open_cursor(self):
        if self.cursor is None:
            self.cursor = self.connection.cursor()
    
    def close_cursor(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        

