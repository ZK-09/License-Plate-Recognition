# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : Database.py
# Description : 
# '''
# This file contains the connection 
# with mysql database
# ''' 
# First Written Date : 14th March 2023
# Last Modified Date : 18th March 2023

# Libraries Import
import mysql.connector
from mysql.connector import errorcode

class DatabaseSQL():
    
    def __init__(self, user, password, host, database):
        self.user=user
        self.password=password
        self.host=host
        self.database=database
        self.connection = None           
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                                user = self.user,
                                password = self.password,
                                host = self.host,
                                database = self.database
                        )
            if self.connection.is_connected():
                print("Database has connected")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User OR Password is invalid")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err) 
    
    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")
    
    # Execution for respective row
    def execute(self, _query, _statistic_data):
        cursor = self.connection.cursor()
        cursor.execute(_query, _statistic_data)
        results_ = cursor.fetchone()
        
        return results_

    # Insert Execution
    def execute_insert(self, _query, _statistic_value):
        cursor = self.connection.cursor()
        cursor.execute(_query, _statistic_value)
        self.connection.commit()
        
    # Executiono for obtain user ID & phone number
    def execute_value(self, _query, _statistic_value):
        flag_ = None
        cursor = self.connection.cursor()
        row = cursor.execute(_query, _statistic_value)
        if row > 0 :
            flag_ = True
            results = cursor.fetchall()
            for data in results:
                user_id_ = data[0]
                phone_num_ = data[1]
                print(f'RETURN USER ID : {user_id_}')
                print(f'RETURN PHONE {phone_num_}')
        else :
            flag_ = False
        
        return user_id_ , phone_num_ , flag_