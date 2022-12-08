# uncompyle6 version 3.8.0
# Python bytecode 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (default, Jun 22 2022, 20:18:18) 
# [GCC 9.4.0]
# Embedded file name: startrun_R1.py
"""
Bittern build
"""
import datetime
import time
from sys import exit
import csv
import pandas as pd

import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print('   ', p, '\n')
else:
    var = input('>>> ')
    time.sleep(1)
    ser = serial.Serial()
    try:
        ser = serial.Serial(var, 57600, timeout=180)
        print('connect')
    except serial.serialutil.SerialException:
        done = False


    else:
        time.sleep(0.1)
        line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        print('\n', line, '\n')
        time.sleep(1)
        ser.write(b'1000')
        time.sleep(0.1)
        line = ser.readline()
        if line != b'*** Do you want to save existing log files to your computer before continuing? ***':
            line = ser.readline()
            line = line.rstrip()
            # print(line.decode())
        else:
            print()
            print('To save the existing log files from SD card on your computer before new run starts press Enter now...')
            print('')
            print('OR')
            print('')
            print('To delete existing log files on SD card and start new run, press d followed by the Enter key... ')
            print('')
            var = 'd'

if var == 'D' or var == 'd':
    ser.write(b'N')
else:
    ser.write(b'Y')

    
while line != b'starting eventlog.csv writeback':
    line = ser.readline()
    line = line.rstrip()
    # print(line.decode())

f1 = open('eventlog.csv', 'wb')
line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
ramdiskf1 = b'file uploaded: ' + line.encode() + b'\n'







while True:


    while line != b'starting snapshot.csv writeback':
        line = ser.readline()
        line = line.rstrip()
        print(line.decode())

    f2 = open('snapshot.csv', 'wb')
    line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    ramdiskf2 = b'file uploaded: ' + line.encode() + b'\n'
    while True:
        if line != b'writeback completed - snapshot.csv closed':
            line = ser.readline()
            line = line.rstrip()
            # print(line.decode())
            ramdiskf2 = ramdiskf2 + line + b'\n'

        while line != b'starting daily.csv writeback':
            line = ser.readline()
            line = line.rstrip()
            # print(line.decode())

        f3 = open('daily.csv', 'wb')
        line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        ramdiskf3 = b'file uploaded: ' + line.encode() + b'\n'
        while True:
            if line != b'writeback completed - daily.csv closed':
                line = ser.readline()
                line = line.rstrip()
                # print(line.decode())
                ramdiskf3 = ramdiskf3 + line + b'\n'

            # while line != b'starting hourly.csv writeback':
            #     line = ser.readline()
            #     line = line.rstrip()
                # print(line.decode())

            # f4 = open('hourly.csv', 'wb')
            # line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            # ramdiskf4 = b'file uploaded: ' + line.encode() + b'\n'
            # while line != b'writeback completed - hourly.csv closed':
            #     line = ser.readline()
            #     line = line.rstrip()
            #     # print(line.decode())
            #     ramdiskf4 = ramdiskf4 + line + b'\n'

            f1.write(ramdiskf1)
            f1.close()
            f2.write(ramdiskf2)
            f2.close()
            f3.write(ramdiskf3)
            f3.close()

            while line != b'Power on self test complete':
                line = ser.readline()
                line = line.rstrip()

            time.sleep(0.5)


            print('******************************************************')
            print('******************************************************')
            print('******************************************************')
            time.sleep(0.1)
            print()
            done = False

            f1 = open('setup.csv', 'r')
            line = f1.readline()

            for num in range(1, 17):
                line = f1.readline()
                print(line, end='')
                time.sleep(0.1)
                line = line + 'eol^'
                time.sleep(0.1)
                ser.write(line.encode())
                time.sleep(0.1)
            else:
                f1.close()
                while line != b'starting setup.csv writeback':
                    line = ser.readline()
                    line = line.rstrip()
                    # print(line.decode())

                f1 = open('setup.csv', 'ab')
                f1.write(b'file uploaded: ')
                line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                f1.write(line.encode())
                f1.write(b',\n')
                while line != b'writeback completed - setup.csv closed':
                    line = ser.readline()
                    f1.write(line)
                    line = line.rstrip()
                    print(line.decode())

                f1.close()

                time.sleep(0.1)
             
                print()
                time.sleep(0.1)
                ser.write(b'X')
                done = False
               
               
               
               
               
                flowmeter_info = ['Channel', 'Name', 'timestamp', 'temp_C', 'pressureh_Pa', 'total_tips_since_start', 'volume_this_tip_ml', 
                                  'total_vol_since_start_ml', 'tips_this_day', 'vol_this_dayml', 'tips_this_hour', 'vol_this_hourml', 
                                  'net_gas_attributable_to_test_sample_since_startmlg']
                while not done:
                    line = ser.readline()
                    line = line.rstrip()
                    log_dict = {}
                    
                    if line != b'ping':
                        # print(line.decode())
                        if line.decode() == '**********':
                            pass
                           
                            
                        elif len(line.decode()) > 0:
                            line_ls = line.decode().split(", ")
                            for word in line_ls:
                                # print(word)
                                word_ls = word.split(" ")
                                log_dict[str(word_ls[0])] = [word_ls[1]]
                        print(log_dict)
                            
                    if len(log_dict) > 0:
                        print(log_dict)
                        df = pd.DataFrame.from_dict(log_dict) 
                
                        # df.to_csv (r'test8.csv',mode = 'a', index = False, header=True)
                        with open(r'flowmeter.csv', 'a') as f:
                            df.to_csv(f, mode='a',index = False, header=f.tell()==0)


                ser.close()
                print('Bye')
                time.sleep(2)
                exit(0)
    # okay decompiling startrun_R1.pyc
