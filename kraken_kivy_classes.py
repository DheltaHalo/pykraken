# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:30:33 2021

@author: Usuario
"""
from kivy.uix.label import Label
from kivy.uix.button import Button

class RedLabel(Label):
    pass

class ValueLabel(Label):
    def __init__(self, color, **kwargs):
        super(ValueLabel, self).__init__(**kwargs)
        self.color = color

class aButton(Button):
    pass

class calButton(Button):
    pass

class CryptoButton(Button):
    def __init__(self, time, **kwargs):
        super(CryptoButton, self).__init__(**kwargs)
        self.time = time
        
    def get_time(self):
        return self.time
    
