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
        self.time_2 = self.time
        self.file_path = file_path
        self.file_name = file_name
        for i in self.data:
            self.data.update({i: float(self.data.get(i))})

    def print_times(self):
        print('---------------')
        for i in self.data:
            print(f'{i}: {format_time(self.data.get(i))}')
        print('---------------')

    def update(self, arg_1, arg_2):
        pass

    def idle(self):
        started = False
        while True:
            self.print_times()
            if not started:
                input_key = input(
                    'key\n(exit to save and quit)' +
                    '\n(merge <old> <new> if misspelled): ').split(' ')
            arguments = []
            command = ''

            if input_key[0] in ['exit', 'e', 'clear']:
                command = input_key[0]
                if len(input_key) == 2:
                    arguments = [input_key[1]]
            elif len(input_key) == 1:
                arguments = [input_key[0]]
            else:
                command = input_key[0]
                arguments = input_key[1:]

            try:
                current_time = self.data.get(arguments[0])
            except IndexError:
                pass
            if command in ['exit', 'e']:
                if len(arguments) > 0:
                    self.data.update(
                        {arguments[0]:
                         self.data.get(arguments[0]) +
                         time.time() -
                         self.time})
                save_file(file_path, file_name, data)
                return

            if command in ['clear']:
                clear_file(file_path, file_name)
                load_file(file_path, file_name)
                self.data.clear()
            elif command in ['merge', 'm']:
                self.data.update({arguments[1]: self.data.get(arguments[0]) +
                                  self.data.get(arguments[1])})
                self.data.pop(arguments[0])
            elif command in ['start', 's']:
                self.data.update(
                    {arguments[0]: current_time + time.time() - self.time})
                started = True
            elif command in ['delete', 'd']:
                for i in arguments:
                    self.data.pop(i)
            elif arguments[0] in self.data:
                self.data.update(
                    {arguments[0]: current_time + time.time() - self.time})
            else:
                self.data.update({arguments[0]: time.time() - self.time})

            if started:
                self.data.update(
                    {arguments[0]: current_time + time.time() - self.time})
                if time.time() - self.time_2 > 5:
                    self.time_2 += 5
                    self.print_times()
            save_file(file_path, file_name, data)
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
