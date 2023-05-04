# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : main.py
# Description : 
# '''
# This MAIN python file consists of the real-time detection of
# license plate recognition with YOLOv5 detection model function 
# & the GUI of the system function in main()
# ''' 
# First Written Date : 8th March 2023
# Last Modified Date : 16th April 2023

import cv2
import torch
import PySimpleGUI as sg
import numpy as np
import time
from Vehicle import Plate
from detection import Detection_Model

# Call Detection Class
detect = Detection_Model()

# Load the YOLOv5 from public repository
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

def detection_model(_frame):
    model(_frame) # Model
    PLATE_ = None
    TIME_ = None 
    STATUS_ = None
    try:         
        # Image Processing Method
        cropped_image = detect.image_processing(model, _frame)
        
        # Read License Plate
        text = detect.text_reader(cropped_image)
        num_plate = text[0][-2] # Number Plate Text
        accuracy = text[0][-1]  # Accuracy of recognize the text          
 
        # Call Vehicle Class
        vehicle_plate = Plate(num_plate)
        access, plate_ , date_ , time_ = vehicle_plate.plate_verify() # Verify if the license plate is registered            
        
        # Entry Logic
        if access is True:
            access_record = vehicle_plate.check_access_record(date_, time_) # Record Entered Plate Number into database
            if access_record is True:
                # Check User Account Balance 
                STATUS_ = 'ENTRY'
                print(f'Access Record True')
                vehicle_plate.balance_reminder()  # RMB to un-comment (This credit is very limit)
            PLATE_ = plate_
            TIME_ = time_ 
        else:
            pass
        
        # Exit Logic 
        _time_recorded_entry = vehicle_plate.entry_access_time() # Record Current Time
        check_exit = detect.detection_time_check(_time_recorded_entry) # Check if the vehicle is at exit        
        if check_exit is True: 
            if access is True:
                # Insert Exit Datetime
                vehicle_plate.record_exit_datetime(date_ , time_)   # Update Exit Datetime & Progress
                STATUS_ = 'EXIT'
                # Dedect Parking Fee From User Account
                balance_flag = None
                total_duration = detect.parking_total_duration(vehicle_plate.entry_time, vehicle_plate.exit_time) # total duration in parking
                total_fees = detect.balance_amount_deduct(total_duration)   
                vehicle_plate.parking_fee = total_fees  # Total Parking Fees ----------------------------------------------------------------------
                # Record Paid Amount
                vehicle_plate.record_parking_fee(date_, time_)
                print(f'Total Fees : {total_fees}')
                print(f'User Balance {vehicle_plate.balance}')
                balance_flag = detect.sufficient_verify(vehicle_plate.balance)
                
                total_balance = 0                
                if balance_flag is True:
                    total_balance = vehicle_plate.balance - total_fees
                    print(f'TOTAL Balance : {total_balance}')
                    if total_balance != vehicle_plate.balance:
                        vehicle_plate.update_balance(total_balance)  # Update New Balance
                    else:
                        print(f'TOTAL BALANCE FLAG')
                        pass
                else:
                    print(f'Amount Insufficient.')                
                time.sleep(5) # Avoid Duplicated Entry Record after EXIT RECORDING
            else:
                pass
            PLATE_ = plate_
            TIME_ = time_ 
        else:
            pass
    except:
        pass
    
    return PLATE_ , TIME_, STATUS_

def main():
    sg.theme('Black') # Set Theme Colour

    # Window Layout 
    layout = [[sg.Text('Video Capture', size=(30,1), justification='center',font=('Georgia', 20))],
              [sg.Button('Switch On', size=(10,1),font=('Georgia', 14)),
              sg.Button('Switch Off', size=(10,1),font=('Georgia', 14), disabled=True)],
              [sg.Text('Output', size=(30,1),  font=('Georgia', 20))],
              [sg.Image(key='image')],
              [sg.Text('Vehicle',font=('Georgia', 14))],
              [sg.Text('',font=('Georgia', 12), key='-VEHICLE-')],
              [sg.Text('Time',font=('Georgia', 14))],
              [sg.Text('',font=('Georgia', 12), key='-TIME-')],
              [sg.Text('Status',font=('Georgia', 14))],
              [sg.Text('',font=('Georgia', 12), key='-STATUS-')],]

    # Create window
    window = sg.Window('EasyGO-LPR',
                       layout,
                       size=(480, 850))
    
    # Event LOOP Read and display frames, operate the GUI  #
    video = cv2.VideoCapture(1)
    recording = False

    while True:
        event, values = window.read(timeout=20)

        img = np.full((480, 640), 255)
        # this is faster, shorter and needs less includes
        imgbytes = cv2.imencode('.png', img)[1].tobytes()
        if event != sg.WIN_CLOSED:
            window['image'].update(data=imgbytes)
    
        if event == 'Switch Off' or event == sg.WIN_CLOSED:
            confirm_exit = sg.popup_yes_no('Are you sure to exit ?')
            if confirm_exit == 'Yes':
                return
        elif event == 'Switch On':
            recording = True
            window['Switch Off'].update(disabled=False)
            window['Switch On'].update(disabled=True)

        if recording:
            ret, frame = video.read()           
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            plate_num , _time, _status = detection_model(frame)  # Model 
            window['image'].update(data=imgbytes)
            window['-VEHICLE-'].update(plate_num)
            window['-TIME-'].update(_time)
            window['-STATUS-'].update(_status)
        
if __name__ == "__main__":
    main()