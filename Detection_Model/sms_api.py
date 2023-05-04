# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : sms_api.py
# Description : 
# '''
# This file contains the SMS API class 
# storing accessing APIs methods
# ''' 
# First Written Date : 25th March 2023
# Last Modified Date : 25th March 2023

from twilio.rest import Client

class SMS_API():
    
    def __init__(self):
        self.SSID = "AC9970c608244457b6eaa35e14df216935"
        self.AUTH_TOKEN = "730b9d0f8023c19af459fdc821a0b675"
        self.TWILO_PHONE_NUM = "+14754710854"
    
    # Generate SMS notification request
    def sms_generate(self, _user, _phone_num):
        client = Client(self.SSID, self.AUTH_TOKEN)

        message = client.messages.create(
            to=["+6{}".format(_phone_num)],
            from_=self.TWILO_PHONE_NUM,
            body="\nDear {},\nYour Account Balance is insufficient.\nPlease reload your account.\nThank You\nYour Sincerely,\nEasyGo.".format(_user)
            )

        print(message.status)
