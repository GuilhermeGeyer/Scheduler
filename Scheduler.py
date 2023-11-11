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
    def __init__(self, data, file_path, file_name):
        self.data = data
        self.time = time.time()
        self.file_path = file_path
        self.file_name = file_name
        for i in self.data:
            self.data.update({i: float(self.data.get(i))})

    def idle(self):
        while True:
            print('---------------')
            for i in self.data:
                print(f'{i}: {format_time(self.data.get(i))}')
            print('---------------')
            input_key = input(
                'key\n(exit to save and quit)' +
                '\n(merge <old> <new> if misspelled): ').split(' ')
            if input_key[0] == 'exit':
                save_file(file_path, file_name, data)
                return
            elif input_key[0] == 'merge':
                self.data.update({input_key[2]: self.data.get(input_key[1]) +
                                  self.data.get(input_key[2])})
                self.data.pop(input_key[1])
            elif input_key[0] in self.data:
                current_time = self.data.get(input_key[0])
                self.data.update(
                    {input_key[0]: current_time + time.time() - self.time})
            else:
                self.data.update({input_key[0]: time.time() - self.time})
            self.time = time.time()


def format_time(seconds):
    minutes = 0
    hours = 0
    if seconds > 3600:
        hours = seconds // 3600
        seconds = seconds % 3600
    if seconds > 60:
        minutes = seconds // 60
        seconds %= 60
    return f'{hours}h {minutes}m {seconds:.2f}s'


def clear_file(file_path, file_name):
    with open(f'{file_path}/{file_name}', 'w') as file:
        file.write('{}')


def load_file(file_path, file_name):
    try:
        with open(f'{file_path}/{file_name}', 'r') as file:
            pass
    except FileNotFoundError:
        with open(f'{file_path}/{file_name}', 'w') as file:
            file.write('{}')
    finally:
        with open(f'{file_path}/{file_name}', 'r') as file:
            data = json.load(file)
    return data


def save_file(file_path, file_name, data):
    with open(f'{file_path}/{file_name}', 'w') as file:
        json.dump(data, file)
    return data


def beep(frequency, duration, sleep_time):
    timer = time.time()
    winsound.Beep(frequency, duration)
    while time.time() - timer < sleep_time:
        time.sleep(0.001)


def idle():
    while True:
        current_time = datetime.datetime.now()
        alarm(data, current_time)
        time.sleep(1)


def alarm(data, current_time):
    current_time_hm = f'{current_time.hour}h{current_time.minute}'
    if current_time_hm in data:
        print(current_time_hm, data.get(current_time_hm))
        while True:
            beep(1000, 200, 0.3)


if __name__ == '__main__':
    data = load_file(file_path, file_name)
    terminal = Terminal(data, file_path, file_name)
    terminal.idle()
