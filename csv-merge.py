#!/usr/bin/env python3

import sys
import csv
import re
import datetime

schedule = []
patterns = {'first line (week-days)': r'first_line_weekdays', 
            'backup (week-days)': r'backup_weekdays', 
            'FIRST LINE (weekend)': r'first_line_weekends', 
            'BACKUP (weekend)': r'backup_weekends', }

def get_rotation_name(file_name):
    for k in patterns:
        match = re.search(patterns[k], file_name)
        if match:
            return k

def process_line(row, rotation_name):
    date_string = row['User On Call Periods Start Time of On Call Segment Time']
    end_date = row['User On Call Periods End Time of On Call Segment Time']
    date_time_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    date_time_obj_end = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S.%f')
    schedule.append([str(date_time_obj), row['User Name'], str(date_time_obj_end), rotation_name])

def sort_schedule():
    schedule.sort(key=lambda elem: elem[0])

def print_schedule():
    with open('schedule_file.csv', mode='w') as schedule_file:
        writer = csv.writer(schedule_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'First line', 'End date', 'Rotation'])

        for sch in schedule:
            writer.writerow(sch)

def read_files():
    for argv in sys.argv[1:]:
        with open(argv, mode='r') as file:
            rotation_name = get_rotation_name(argv)
            csv_reader = csv.DictReader(file)
            line_count = 0
            for row in csv_reader:
                process_line(row, rotation_name)
                line_count += 1
        
        print(f'Processed {line_count} lines from {rotation_name} rotation')

if len(sys.argv) < 2:
    print('Please provide argument files')
    exit(1)

read_files()
sort_schedule()
print_schedule()