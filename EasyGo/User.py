# Programmer Name : TAN ZE KAI - TP 061463
# Program Name : User.py
# '''
# This python file consists of the Abstract Class 
# and Method of User including Customer & Admin
# ''' 
# First Written Date : 10th April 2023
# Last Modified Date : 10th April 2023

from abc import ABC, abstractmethod

class User(ABC):
    
    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def password_control(self, _password):
        pass