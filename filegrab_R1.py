# uncompyle6 version 3.8.0
# Python bytecode 3.8.0 (3413)
# Decompiled from: Python 3.8.10 (default, Jun 22 2022, 20:18:18) 
# [GCC 9.4.0]
# Embedded file name: filegrab_R1.py
"""
Bittern build

filegrab_bit_2 changes from filegrab_bit_1

finds current working pathname and creates /data/ subdirectory if it doesn't already exist
all data files then written to /data/ subdirectory 

"""

import serial, serial.tools.list_ports, time, datetime
from sys import exit
import os, sys
from pathlib import Path
ser = serial.Serial()
dirname = os.path.dirname(os.path.realpath(sys.argv[0]))
dirname = dirname + '/data/'
newname = list(dirname)
for i, c in enumerate(dirname):
    len = i
else:
    for i in range(0, len + 1):
        if newname[i] == '\\':
            newname[i] = '/'
        newpath = ''.join(newname)
        path = Path(newpath + 'testfile.txt')
        path.parent.mkdir(parents=True, exist_ok=True)
        subdir = newpath
        print()
        print('>>> **********************************************************************************')
        print('>>> anaero technology - www.anaero.co.uk - file upload utility')
        print('>>> this utility performs an upload of all log files from the Arduino SD card')
        print('>>> data logging will still remain active')
        print()
        print('>>> checking for /data/ sub-directory', subdir)
        print(">>> sub-directory will be created if it doesn't already exist")
        print('>>>')
        print('>>> filegrab version R1 - compatible with Bittern build gas flow meter software')
        print('>>> files uploaded will have comma (,) as field separator and point (.) as decimal point')
        print('>>>')
        print('>>> serial ports being used on this machine are:', '\n')
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print('    ', p, '\n')
        else:
            print('>>> enter the name of the COM port the Arduino Mega 2560 is connected to')
            print('>>> e.g. COM1 or COM2 or COM3 or COM4 or similar, and then press enter', '\n')
            var = input('>>> ')
            time.sleep(1)
            print('>>> configuring serial port')
            ser.port = var
            ser.baudrate = 57600
            ser.timeout = 180
            ser.setDTR(False)
            time.sleep(0.5)
            print('>>> port configured')
            print('>>> opening serial port')
            try:
                ser.open()
            except serial.serialutil.SerialException:
                print('>>> Arduino not connected - please check COM port and try again')
                print('>>> press any key to exit program')
                done = False
                while not done:
                    if msvcrt.kbhit():
                        line = msvcrt.getch()
                        print('>>> keyboard input detected - quitting monitor')
                        done = True
                        exit(0)

            else:
                time.sleep(1.0)
                print('>>> serial connection established')
                print()
                print('>>> requesting connection to Arduino - this may take a short while', '\n')
                line = ser.readline()
                line = line.rstrip()
                # while line != b'ping':
                #     line = ser.readline()
                #     line = line.rstrip()

                time.sleep(0.01)
                ser.write(b'9999x')
                print('>>> waiting - writeback request sent', '\n')
                # while line != b'Connection request acknowledged....':
                #     line = ser.readline()
                #     line = line.rstrip()

                print('>>> connection request acknowledged....', '\n')
                # while line != b'starting eventlog.csv writeback':
                #     line = ser.readline()
                #     line = line.rstrip()
                #     if line == b'starting eventlog.csv writeback':
                #         print('>>> ', line.decode(), '\n')

                fileName = 'eventlog_'
                fileExtn = '.csv'
                timeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d_%H_%M')
                fullName = subdir + fileName + timeStamp + fileExtn
                f1 = open(fullName, 'wb')
                line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                ramdiskf1 = b'file uploaded: ' + line.encode() + b'\n'
                while line != b'writeback completed - eventlog.csv closed':
                    line = ser.readline()
                    line = line.rstrip()
                    print('\t', line.decode())
                    ramdiskf1 = ramdiskf1 + line + b'\n'

                print()
                while line != b'starting snapshot.csv writeback':
                    line = ser.readline()
                    line = line.rstrip()
                    print('\t', line.decode())

                fileName = 'snapshot_'
                fileExtn = '.csv'
                timeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d_%H_%M')
                fullName = subdir + fileName + timeStamp + fileExtn
                f2 = open(fullName, 'wb')
                line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                ramdiskf2 = b'file uploaded: ' + line.encode() + b'\n'
                while line != b'writeback completed - snapshot.csv closed':
                    line = ser.readline()
                    line = line.rstrip()
                    print('\t', line.decode())
                    ramdiskf2 = ramdiskf2 + line + b'\n'

                print()
                if line != b'starting daily.csv writeback':
                    line = ser.readline()
                    line = line.rstrip()
                    print('\t', line.decode())
                else:
                    fileName = 'daily_'
                    fileExtn = '.csv'
                    timeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d_%H_%M')
                    fullName = subdir + fileName + timeStamp + fileExtn
                    f3 = open(fullName, 'wb')
                    line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    ramdiskf3 = b'file uploaded: ' + line.encode() + b'\n'
                    if line != b'writeback completed - daily.csv closed':
                        line = ser.readline()
                        line = line.rstrip()
                        print('\t', line.decode())
                        ramdiskf3 = ramdiskf3 + line + b'\n'
                    else:
                        print()

        if line != b'starting hourly.csv writeback':
            line = ser.readline()
            line = line.rstrip()
            print('\t', line.decode())
        else:
            fileName = 'hourly_'
            fileExtn = '.csv'
            timeStamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y_%m_%d_%H_%M')
            fullName = subdir + fileName + timeStamp + fileExtn
            f4 = open(fullName, 'wb')
            line = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            ramdiskf4 = b'file uploaded: ' + line.encode() + b'\n'
            if line != b'writeback completed - hourly.csv closed':
                line = ser.readline()
                line = line.rstrip()
                print('\t', line.decode())
                ramdiskf4 = ramdiskf4 + line + b'\n'
            else:
                f1.write(ramdiskf1)
                f1.close()
                f2.write(ramdiskf2)
                f2.close()
                f3.write(ramdiskf3)
                f3.close()
                f4.write(ramdiskf4)
                f4.close()
                ser.close()
                print()
                print('>>> upload of logfiles complete :-)')
                print('>>> filegrab utility will close in 10 seconds')
                time.sleep(10)
                print('>>> bye...')
                time.sleep(2)
                exit
# okay decompiling filegrab_R1.pyc
