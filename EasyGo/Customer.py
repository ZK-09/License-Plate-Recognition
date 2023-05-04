# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : Customer.py
# '''
# This python file consists of the Class and Method
# of Customer
# ''' 
# First Written Date : 8th April 2023
# Last Modified Date : 16th April 2023

# Import
from mysql import DatabaseMYSQL
from User import User
import re

class Customer(User):
    
    def __init__(self, username, password, app, mysql):
        self.username = username
        self.password = password
        self.phone_num = None
        self.balance = None
        self.app = app
        self.mysql = mysql
        self.database = DatabaseMYSQL('localhost', 
                                      'root', 
                                      '#Swat9298', 
                                      'easy_go', 
                                      self.app, 
                                      self.mysql)
    
    # User Login
    def login(self):
        query = """ SELECT User_ID
                    FROM user
                    WHERE User_ID = %s AND
                    Password = %s
                """
        self.database.connect()
        data = (self.username, self.password)
        results_ = self.database.execute(query, data)
        
        return results_
    
    # Get the balance amount
    def check_balance(self, _username):
        query = """ SELECT Balance
                    FROM user
                    WHERE User_ID = %s
                """ 
        self.database.connect()
        self.username = _username
        results = self.database.execute(query, (self.username,))
        if results is not None:
            self.balance = results[0]
            
        return self.balance
    
    # Confirm Phone Nummber
    def confirm_phone_num(self, _phone_num):
        query = """ SELECT Phone
                    FROM user
                    WHERE Phone = %s 
                """ 
        self.database.connect()
        results_ = self.database.execute(query, (_phone_num,))
        if results_ is not None:
            self.phone_num = results_[0]
        else:
            pass
        return results_
    
    # Reset Password
    '''
    Check the new password if full-fill the requirements.
    Then verify the new password and UPDATE
    '''
    def reset_password(self, _new_pass, _re_new_pass):
        flag_ = None
        query = """ UPDATE user
                    SET Password = %s
                    WHERE Phone = %s 
                """ 
        _valid, _msg = self.password_control(_new_pass) # Password Control
        if _valid is True:
            if _new_pass == _re_new_pass:   # Verify New Password
                self.database.connect()
                data = (_new_pass, self.phone_num)
                self.database.execute(query, data)
                flag_ = True
                message_ = 'Password Re-New Successfully. Please Login Again.'
            else:
                flag_ = False
                message_ = 'Your new password does not match'
        else:
            flag_ = False
            message_ = _msg
        
        return flag_ , message_
    
    # Password Formate Control
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
    
    # Top Up Balance Amount
    def top_up_balance(self, amount):
        query = """ UPDATE user
                    SET Balance = %s
                    WHERE User_ID = %s; 
                """  
        self.database.connect()
        amount = float(amount)
        if self.balance is not None:
            self.balance = float(self.balance)
            self.balance = self.balance + amount    # Add new amount
        else:
            self.balance = amount
        data = (self.balance, self.username)
        self.database.execute(query, data)
        
    # User view own record in their interface
    def view_record(self):
        query = """ SELECT uv.Plate_Num, uv.Progress, vs.Entrance_Date, vs.Entrance_Time, vs.Exit_Date, vs.Exit_Time, vs.Paid_Fee
                    FROM user_own_vehicle uov
                    INNER JOIN user_vehicle uv
                    ON uov.Plate_Num = uv.Plate_Num
                    INNER JOIN vehicle_status vs
                    ON vs.Status_ID = uv.Status_ID
                    WHERE uov.User_ID = '{}';
                """.format(self.username)  
        self.database.connect()
        results = self.database.execute_list(query, None)
        
        return results