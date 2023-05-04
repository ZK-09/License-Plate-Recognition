# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : mysql.py
# Description : 
# '''
# This is a class storing database methods
# ''' 
# First Written Date : 7th April 2023
# Last Modified Date : 7th April 2023 

class DatabaseMYSQL():
    
    def __init__(self, localhost, root, password, table, app, mysql):
        self.localhost = localhost
        self.root = root
        self.password = password
        self.table = table
        self.app = app
        self.mysql = mysql
        
    def connect(self):
        self.app.config['MYSQL_HOST'] = self.localhost
        self.app.config['MYSQL_USER'] = self.root
        self.app.config['MYSQL_PASSWORD'] = self.password
        self.app.config['MYSQL_DB'] = self.table
        
    # Execution
    def execute(self, _query, _data):        
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(_query, _data)
            results = cursor.fetchone()
            print(f'EXECUTE RESULTS : {results}')
            self.mysql.connection.commit()
            flag_ = results
        except Exception:
            print(f'ERROR : EXECUTION')

        return flag_
    
    # Execution Insert
    def execute_insert(self, _query, _data):
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(_query, _data)
            self.mysql.connection.commit()
            
        except Exception:
            print(f'ERROR : INSERT EXECUTION')
    
    def execute_list(self, _query, _data):
        results_ = None
        try:
            cursor = self.mysql.connection.cursor()
            cursor.execute(_query, _data)
            results = cursor.fetchall()
            self.mysql.connection.commit()            
            results_ = results
            
        except Exception:
            print(f'ERROR : LIST EXECUTION')
    
        return results_
    
    def disconnect(self):
        self.mysql.connection.close()