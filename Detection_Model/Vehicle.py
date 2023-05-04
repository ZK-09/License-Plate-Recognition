# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : Vehicle.py
# Description : 
# '''
# This file contains the Vehicle class 
# storing license plate number object
# ''' 
# First Written Date : 12th March 2023
# Last Modified Date : 16th April 2023


# Import Libraries
from Database import DatabaseSQL
from detection import Detection_Model
from sms_api import SMS_API

USERNAME = 'root'
PASSWORD = '#Swat9298'
HOST = '127.0.0.1'
TABLE = 'easy_go'

# Global Class CallBack
mysql = DatabaseSQL(USERNAME, PASSWORD, HOST, TABLE)
detect = Detection_Model()

class Plate ():
    
    def __init__(self, _plate_num):
        self.plate_num = _plate_num.upper()
        self.exit_time = None   # Exit Time
        self.entry_time = None  # Entry Time
        self.parking_fee = None # Parking Fee Total Amount
        self.balance = None     # Balance User Amount 
        self.user = None
        self.phone = None

    # Verify if the license plate has registered
    def plate_verify (self):        
        record = None
        access_ = None         
        query = """ SELECT * 
                    FROM vehicle 
                    WHERE Plate_Num = %s; 
                """
        mysql.connect()  # Connect Mysql
        record = mysql.execute(query, (self.plate_num,)) # Execute
        if record is None:
            print(f"{self.plate_num} is not registered")
            access_ = False
        else:
            print(f"{self.plate_num} has access the gate")
            date_, time_ = detect.detect_datetime()
            access_ = True
        mysql.disconnect()
        return access_, self.plate_num, date_, time_
    
    # Record Successfully Access Data 
    ''' 
        query --> to check if the vehicle is duplicated record in database
        query_plate_record --> Record the entering vehicle information
        query_check_status --> To verify the recording vehicle status
        query_datetime --> To INSERT the datetime of entrance
    '''
    def check_access_record(self, _entry_date, _entry_time):
        access_ = None
        query = """ SELECT * 
                    FROM user_vehicle 
                    WHERE Plate_Num = '{}' AND
                    (Progress IS NOT NULL AND
                     Progress != 'EXIT'); 
                """.format(self.plate_num)
        query_plate_record =  """ INSERT INTO
                                  user_vehicle (Plate_Num, Progress, Status_ID)
                                  VALUES (%s, %s, %s);
                              """
        query_update_statusID = """ UPDATE user_vehicle
                                    SET Status_ID = (SELECT Status_ID 
                                                    FROM vehicle_status 
                                                    WHERE Entrance_Time = '{}' AND
                                                    Exit_Time IS NULL)
                                    WHERE Plate_Num = '{}'  AND
                                    Progress = 'ENTERED';
                                """.format(_entry_time, self.plate_num)
        query_check_status = """ SELECT * 
                                 FROM user_vehicle uv 
                                 INNER JOIN vehicle_status vs 
                                 ON uv.Status_ID = vs.Status_ID
                                 WHERE Plate_Num = '{}' AND
                                 Progress != 'EXIT' AND
                                 Entrance_Time IS NOT NULL; 
                             """.format(self.plate_num)
        query_datetime = """ INSERT INTO 
                             vehicle_status (Entrance_Date, Entrance_Time, Exit_Date, Exit_Time, Paid_Fee) 
                             VALUES (%s, %s, %s, %s, %s);
                         """
        mysql.connect()
        record = mysql.execute(query, None) 
        print(f'Record From check_access_record --> {record}')
        # If approaching vehicle is new, record it to database
        if record is None:  # Record None : Vehicle is a new record
            print(f"{self.plate_num} has not recorded")
            plate_query_date = (self.plate_num, 'ENTERED', None)                   
            mysql.execute_insert(query_plate_record, plate_query_date)  # If new income vehicle, record 
            access_ = False
        else:   # Else Statement : Vehicle is recorded and required insert datetime 
            print(f"{self.plate_num} has recorded")
            status_check = mysql.execute(query_check_status, None)
            print(f'Status CHECK --> {status_check}')   # Check if the 
            if status_check is None:                
                data = (_entry_date, _entry_time, None, None, None)
                mysql.execute_insert(query_datetime, data)  # Record Entrance Time
                mysql.execute_insert(query_update_statusID, None)   # Update Status_ID with Entrance Time
                access_ = True
            else:
                pass
            
        mysql.disconnect()
        
        return access_    
    
    # # Get Both Entrance and Exit Time
    def entry_exit_time(self):
        query_get_time = """ SELECT vs.Entrance_Time, vs.Exit_Time
                             FROM user_vehicle uv
                             INNER JOIN vehicle_status vs
                             ON uv.Status_ID = vs.Status_ID
                             WHERE uv.Plate_Num = '{}' AND
                             uv.Progress = 'ENTERED';
                         """.format(self.plate_num)
        print(f'--Entry Exit Function--')
        mysql.connect()
        entry_exit_datetime = mysql.execute(query_get_time, None)   # Retrieve Entry & Exit Time
        entry_time_ = entry_exit_datetime[0]
        exit_time_ = entry_exit_datetime[1]
        
        self.entry_time = entry_time_
        print(f'ENTRY TIME -> {self.entry_time}')
        self.exit_time = exit_time_
        print(f'EXIT TIME -> {self.exit_time}')
        mysql.disconnect()
        
    # To get user's balance amount from mysql
    def balance_amount(self):
        query_balance_amount =  """ SELECT u.User_ID, u.Balance, u.Phone, uv.Plate_Num, uv.Progress
                                    FROM user_own_vehicle uov
                                    INNER JOIN user_vehicle uv
                                    ON uov.Plate_Num = uv.Plate_Num
                                    INNER JOIN user u
                                    ON u.User_ID = uov.User_ID
                                    WHERE uv.Plate_Num = '{}' AND
                                    Progress = 'ENTERED';
                                """.format(self.plate_num)
        print(f'--Check Balance Function--')
        mysql.connect()
        balance_results = mysql.execute(query_balance_amount, None)
        self.user = balance_results[0]
        self.balance = balance_results[1]
        self.phone = balance_results[2]
        print(f'Details : {self.user},{self.balance}, {self.phone}')
        mysql.disconnect()
        
    # To record the exit date & time
    '''
        query --> Record Exit Datetime to database
        query_update_progress --> UPDATE Status
        query_get_time --> Get ENTRY & EXIT Time
    '''
    def record_exit_datetime(self, _exit_date, _exit_time):      
        query = """ UPDATE vehicle_status vs
                    JOIN user_vehicle uv ON
                    vs.Status_ID = uv.Status_ID
                    SET Exit_Date = '{}', 
                        Exit_Time = '{}'
                    WHERE uv.Plate_Num = '{}' AND 
                    uv.Progress = 'ENTERED';
                """.format(_exit_date, _exit_time, self.plate_num)
        query_update_progress = """ UPDATE vehicle_status vs
                                    INNER JOIN user_vehicle uv ON
                                    vs.Status_ID = uv.Status_ID
                                    SET uv.Progress = '{}'
                                    WHERE uv.Plate_Num = '{}' AND 
                                    uv.Progress = 'ENTERED';
                                """.format('EXIT', self.plate_num)
        mysql.connect()
        mysql.execute_insert(query, None)  
        mysql.disconnect()
     
        self.entry_exit_time()  # Must have the system insert the exit time
        self.balance_amount()
        print(f'--Update Progress Function--')
        mysql.connect()
        mysql.execute_insert(query_update_progress, None)            
        mysql.disconnect()
    
    def update_balance(self, _total_balance):
        query_update_balance =  """ UPDATE user
                                    SET Balance = '{}'
                                    WHERE User_ID = '{}';
                                """.format(_total_balance, self.user)
        print(f'--Update Balance Function--')
        mysql.connect()        
        mysql.execute_insert(query_update_balance, None)
        mysql.disconnect()
        
    # Get the entry time from mysql
    def entry_access_time(self):
        record_ = False
        query = """ SELECT Entrance_Time
                    FROM user_vehicle uv
                    INNER JOIN vehicle_status vs
                    ON uv.Status_ID = vs.Status_ID
                    WHERE uv.Plate_Num = %s AND
                    Progress = 'ENTERED';
                """
                
        mysql.connect()
        record_ = mysql.execute(query, (self.plate_num,))
        record_ = record_[0]
        mysql.disconnect()
                  
        return record_
    
    # Record total parking fee from user
    def record_parking_fee(self, _date, _time):
        query = """ UPDATE vehicle_status vs
                    JOIN user_vehicle uv ON
                    vs.Status_ID = uv.Status_ID
                    SET Paid_Fee = '{}'
                    WHERE uv.Plate_Num = '{}' AND
                    vs.Exit_Date = '{}' AND 
                    vs.Exit_Time = '{}'
                """.format(self.parking_fee, self.plate_num, _date, _time)
        print(f'Parking Fee is {self.parking_fee}')        
        mysql.connect()
        mysql.execute_insert(query, None)            
        mysql.disconnect()
    
    # Check Balance in Vehicle Account
    # IF less than 10, send SMS APIs
    # Parameter : User_ID, Phone
    # Get the parameter to access into APIs
    def balance_reminder(self):
        self.balance_amount()   # Get User Balance Amount & Phone
        if self.balance is None :
            self.balance = 0
        else:
            pass
        SMS = SMS_API()
        if self.balance < 10: 
            print('SMS IF statement')        
            SMS.sms_generate(self.user , self.phone)
        else:
            print(f'{self.user} Balance Sufficient')
            pass
        mysql.disconnect()        


