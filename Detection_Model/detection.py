# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : detection.py
# Description : 
# '''
# This python file consists of the real-time detection CLASS of
# license plate recognition with YOLOv5 detection model
# ''' 
# First Written Date : 8th March 2023
# Last Modified Date : 31st March 2023

# Import Libraries
import cv2
import easyocr
import numpy as np
import imutils
from datetime import date
from datetime import datetime
from datetime import timedelta

class Detection_Model :
    
    def __init__(self):
        '''Get English Language Only (Malaysia Plate have numbers and English Alphabet only)'''
        self.reader = easyocr.Reader(lang_list=['en'])              

    # Capture License Plate Image Processing
    def image_processing (self, _model, _frame):
        # Get the co-ordinates of license plate based on the model detected
        results_df = _model(_frame).pandas().xyxy[0].loc[0]
        x_min = int(results_df['xmin'])
        x_max = int(results_df['xmax'])
        y_min = int(results_df['ymin'])
        y_max = int(results_df['ymax'])
        # Crop license plate from the recorded image
        license_plate = _frame[y_min:y_max+1, x_min:x_max+1]
        
        # Convert image to grayscale
        gray = cv2.cvtColor(license_plate, cv2.COLOR_RGB2GRAY)
        
        # Binarizing Image
        binarize = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(binarize, 30, 200) # Edge Detection
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        location = None # Location of the license plate
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
            
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(license_plate, license_plate, mask=mask)

        (x,y) = np.where(mask==255)
        (x1,y1) = (np.min(x), np.min(y))
        (x2,y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]  # Plate Number loaction actual
        
        return cropped_image
    
    # Plate Number Recognition
    def text_reader (self, _cropped_image):
        license_plate_text = self.reader.readtext(_cropped_image)   # Read Text
        return license_plate_text

    # Retrive Current Date & Time
    def detect_datetime(self):
        # Current Date 
        _date = date.today()
        _time = datetime.now()
        _time = _time.strftime("%H:%M:%S")
        
        return _date, _time
    
    # Verify exit status by the difference with entry time
    def detection_time_check(self, _time):
        _str_time = str(_time)
        _database_time = datetime.strptime(_str_time, "%H:%M:%S")
                
        _current_datetime = datetime.now()
        _current_time = _current_datetime.strftime('%H:%M:%S')        
        _current_time = datetime.strptime(_current_time, "%H:%M:%S")
        
        delta = _current_time - _database_time        
        delta = delta.total_seconds()
        
        if delta > 10 :
            return True
        else:
            return False
    
    # Find the difference of entry and exit time
    def parking_total_duration(self, _entry_time, _exit_time):
        
        # Convert Datetime to string
        _str_entry_time = str(_entry_time)
        _str_exit_time = str(_exit_time)
        
        # Convert to .strptime format for calculation
        entry_time_ = datetime.strptime(_str_entry_time, "%H:%M:%S")
        exit_time_ = datetime.strptime(_str_exit_time, "%H:%M:%S")
        
        time_duration_delta = exit_time_ - entry_time_
        time_duration_ = time_duration_delta.total_seconds()
        
        return time_duration_
    
    # Amount Dedeuction Logic
    def balance_amount_deduct(self, time_duration):
        fees_ = 0
        # If within 15 mins, FREE
        if time_duration <= 900:
            fees_ = 0
        # If within 1 to 3 hour, 1 ringgit 
        if time_duration > 900 and time_duration <= 10800:
            fees_ = 1
        # If 3 hour and above, 3 ringgit
        if time_duration > 10800:
            fees_ = 3
        
        return fees_
    
    # Verify a Sufficient Account 
    def sufficient_verify(self, account_balance):
        flag_ = None
        if account_balance > 10:
            flag_ = True
        else:
            flag_ = False
            
        return flag_
