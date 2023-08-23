# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 14:41:32 2023

@author: user
"""


import time
import json
import winsound
import datetime
import os


file_path = os.path.abspath(os.path.dirname(__file__))
file_name = 'Scheduler.txt'


class Terminal():
    def __init__(self,data,file_path,file_name):
        self.data = data
        self.time = time.time()
        self.file_path = file_path
        self.file_name = file_name
        for i in self.data:
            #item = self.data.get(i)
            #item = float(item)
            self.data.update({i:float(self.data.get(i))})
            print(f'{i}: {format_time(self.data.get(i))}')
    def idle(self):
        while True:
            input_key = input('key\n(exit to save and quit)\n(merge <old> <new> if misspelled): ')
            if input_key == 'exit':
                save_file(file_path,file_name,data)
                return
            #print(input_key[:6])
            elif input_key[:6] == 'merge ':
                inputs = input_key.split(' ')
                #print(inputs)
                self.data.update({inputs[2]:self.data.get(inputs[1]) + self.data.get(inputs[2])})
                self.data.pop(inputs[1])
            #input_value = input('value: ')
            elif input_key in self.data:
                current_time = self.data.get(input_key)
                self.data.update({input_key:current_time + time.time() - self.time})
            else:
                self.data.update({input_key:time.time() - self.time})
            self.time = time.time()
            for i in self.data:
                #print(f'{i}: {self.data.get(i):.2f}')
                print(f'{i}: {format_time(self.data.get(i))}')


def format_time(seconds):
    #seconds = float(seconds)
    minutes = 0
    hours = 0
    if seconds > 3600:
        hours = seconds // 3600
        seconds = seconds % 3600
    if seconds > 60:
        minutes = seconds // 60
        seconds %= 60
    return f'{hours}h {minutes}m {seconds:.2f}s'


def clear_file(file_path,file_name):
    with open(f'{file_path}/{file_name}','w') as file:
        file.write('{}')


def load_file(file_path,file_name):
    try:
        with open(f'{file_path}/{file_name}','r') as file:
            pass
    except FileNotFoundError:
        with open(f'{file_path}/{file_name}','w') as file:
            file.write('{}')
    finally:
        with open(f'{file_path}/{file_name}','r') as file:
            data = json.load(file)
    #print(f'data: {data} {type(data)}')
    return data


def save_file(file_path,file_name,data):
    with open(f'{file_path}/{file_name}','w') as file:
        json.dump(data,file)
        #print(data)
    return data


def beep(frequency,duration,sleep_time):
    timer = time.time()
    winsound.Beep(frequency, duration)
    while time.time() - timer < sleep_time:
        time.sleep(0.001)


def idle():
    while True:
        current_time = datetime.datetime.now()
        alarm(data,current_time)
        #print(f'{current_time.hour}h{current_time.minute}')
        time.sleep(1)
    

def alarm(data,current_time):
    current_time_hm = f'{current_time.hour}h{current_time.minute}'
    if current_time_hm in data:
        print(current_time_hm, data.get(current_time_hm))
        while True:
            beep(1000,200,0.3)


data = load_file(file_path, file_name)


terminal = Terminal(data,file_path,file_name)
terminal.idle()

