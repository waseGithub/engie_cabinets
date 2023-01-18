import serial
from serial import SerialException
import time
import csv
import os
import pandas as pd
import numpy
from time import gmtime, strftime


import serial.tools.list_ports



import re
import subprocess
import pandas as pd 

device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")
devices = []

line1 = None
line2 = None
line3 = None 
line4 = None 
line5 = None




     
       


ports = serial.tools.list_ports.comports(include_links =False)
ls = []
for port in ports:
    print(port.device)
    ls.append(port.device)
   
print(ls)


import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

Megas = []
unos = []
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        if '85036313130351F01161' in hwid:
          print('Requested device found temperature arduino')
          print(port)
          Megas.append(port)
        elif '9503830353135190A221' in hwid:
          print('Requested device found temperature arduino')
          print(port)
          Megas.append(port)

print('Temp arduino as port:')          
print(Megas)
ser1 = serial.Serial(str(Megas[0]),  9600, timeout = 25)
ser2 = serial.Serial(str(Megas[1]),  9600, timeout = 25)

temp_dict = {'71':'TA', '8B':'TB', '7F':'TC', 'F3':'TD'}


def arduino_read(port):
    data = port.readline().decode("utf-8")
    if(len(data)) == 56 :
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(now)
        file_exists = os.path.isfile('temp_push.csv')

        with open ("temp_push.csv", 'a') as file:
            headers = ['datetime', 'temperature_degC', 'probe_id']
            writer = csv.writer(file, delimiter=",")
            

            if not file_exists:
                writer.writerow(headers)  # file doesn't exist yet, write a header
            try:
                writer.writerow([now,data[0:5], temp_dict[data[16:18]]])
            except KeyError:
                pass



      


        # with open ("temp_push.csv","a") as file:
        #             writer = csv.writer(file, delimiter=",")
        #             writer.writerow([now,data[0:5], temp_dict[data[16:18]]])
        # with open ("temp_archive.csv","a") as file:
        #             writer = csv.writer(file, delimiter=",")
        #             writer.writerow([now,data[0:5], temp_dict[data[16:18]]])
        
        # with open(r"temp_push.csv", 'a') as f:
        #     fieldnames = ['datetime', 'temperature_degC', 'probe_id']
        #     writer = csv.writer(file, delimiter=",")
        #     writer.writerow([now,data[0:5], temp_dict[data[16:18]]])
                    
        # with open(r"temp_archive.csv", 'a') as f:
        #     writer = csv.writer(file, delimiter=",", fieldnames=fieldnames)
        #     writer.writerow([now,data[0:5], temp_dict[data[16:18]]])

    print(data)
    return data


while(True):
    arduino_read(ser1)
    arduino_read(ser2)
    

    
   
   
    
   
    
    