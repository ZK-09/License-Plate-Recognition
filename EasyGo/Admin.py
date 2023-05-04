# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : Admin.py
# '''
# This python file consists of the Class and Method
# of Admin
# ''' 
# First Written Date : 8th April 2023
# Last Modified Date : 8th April 2023

# Import Libraries
from mysql import DatabaseMYSQL
from User import User
import re

class Admin(User):
    
    def __init__(self, username, password, app, mysql):
        self.username = username
        self.password = password
        self.app = app
        self.mysql = mysql
        self.database = DatabaseMYSQL('localhost',
                                      'root',
                                      '#Swat9298',
                                      'easy_go',
                                      self.app,
                                      self.mysql)
    
    # Login
    def login(self):
        query = """ SELECT Admin_ID
                    FROM admin
                    WHERE Admin_ID = %s AND
                    Password = %s;
                """
        self.database.connect()
        data = (self.username, self.password)
        results_ = self.database.execute(query, data)
        
        return results_
    
    # Vehicle Register
    def register_vehicle(self, user_username, user_password, user_gender, user_phone, user_vehicle, user_model):
        query = """ INSERT into
                    user (User_ID, Password, Gender, Phone, Balance)
                    VALUES (%s, %s, %s, %s, %s);
                """
        query_model = """ INSERT into
                          vehicle (Plate_Num, Model)
                          VALUES (%s, %s);
                      """
        query_vehicle = """ INSERT into
                            user_own_vehicle (User_ID, Plate_Num)
                            VALUES (%s, %s);
                        """
        
        _verify, _msg = self.password_control(user_password)    # Password Control
        _username_flag = self.user_validate(user_username)  # Username Control
        _vehicle_flag = self.vehicle_number(user_vehicle)
        flag_ = None
        if _username_flag is True:
            if _verify is True:
                if _vehicle_flag is True:
                    self.database.connect()
                    data = (user_username, user_password, user_gender, user_phone, None)
                    data_model = (user_vehicle, user_model)
                    data_vehicle = (user_username, user_vehicle)
                    self.database.execute_insert(query, data)   # Insert into each table respectively
                    self.database.execute_insert(query_model, data_model)
                    self.database.execute_insert(query_vehicle, data_vehicle)
                    flag_ = True
                    message = _msg
                else:
                    flag_ = False
                    message = f'{user_vehicle} has registered to the account. Please Verify Again.'
            else:
                flag_ = False
                message = _msg
        else:
            message = f'{user_username} is registered. Please choose another username.' 
            
        return flag_, message    
    
    # Vehicle Plate Number Control
    def vehicle_number(self, _plate_num):
        # Query to check if vehicle has been registered
        query_registered =  """ SELECT Plate_Num
                                FROM vehicle
                                WHERE Plate_Num = '{}';
                            """.format(_plate_num)
        self.database.connect()
        results = self.database.execute(query_registered, None)
        if results is None: # If None, the vehicle has not registered
            return True
        else:
            return False    # If False, the vehicle has registered
        
    # Insert to database
    def add_vehicle(self, user_username, user_plate, user_model):
        query_model = """ INSERT into
                          vehicle (Plate_Num, Model)
                          VALUES (%s, %s);
                      """
        query_vehicle = """ INSERT into
                            user_own_vehicle (User_ID, Plate_Num)
                            VALUES (%s, %s);
                        """
        self.database.connect()
        model_data = (user_plate, user_model)
        vehicle_data = (user_username, user_plate)
        self.database.execute_insert(query_model, model_data)   # Insert into each table respectively
        self.database.execute_insert(query_vehicle, vehicle_data)
        
    # Controlling Password Format     
    def password_control(self, _password):
        flag_ = True
        msg_ = "Strong password"
        if len(_password) < 8 or len(_password) > 20:
            flag_ = False
            msg_ = "Password must be between 8 and 20 characters"
    
        if not re.search("[A-Z]", _password):
            flag_ = False
            msg_ = "Password must contain at least one uppercase letter"
        
        if not re.search("[a-z]", _password):
            flag_ = False
            msg_ = "Password must contain at least one lowercase letter"
        
        if not re.search("[0-9]", _password):
            flag_ = False
            msg_ = "Password must contain at least one digit"
        
        if not re.search("[!@#$%^&*()]", _password):
            flag_ = False
            msg_ = "Password must contain at least one special character"

        return flag_ , msg_
    
    # Only one username is allowed in the system
    def user_validate(self, user_name):
        flag_ = None
        query = """ SELECT User_ID
                    FROM user
                    WHERE User_ID = %s;
                """
        self.database.connect()
        results = self.database.execute(query, (user_name,))
        if results is not None:
            flag_ = False
        else:
            flag_ = True
        
        return flag_
    
    def view_history(self):
        query = """ SELECT uv.Plate_Num, uv.Progress, vs.Entrance_Date, vs.Entrance_Time, vs.Exit_Date, vs.Exit_Time, vs.Paid_Fee
                    FROM user_vehicle uv
                    INNER JOIN vehicle_status vs
                    ON uv.Status_ID = vs.Status_ID;
                """
        self.database.connect()
        results = self.database.execute_list(query, None)
        
        return results
    
    def search_history(self, input_search):
        query = """ SELECT uv.Plate_Num, uv.Progress, vs.Entrance_Date, vs.Entrance_Time, vs.Exit_Date, vs.Exit_Time
                    FROM user_vehicle uv
                    INNER JOIN vehicle_status vs
                    ON uv.Status_ID = vs.Status_ID
                    WHERE uv.Plate_Num = %s;
                """

        self.database.connect()
        results = self.database.execute_list(query, (input_search,))
        
        return results
        