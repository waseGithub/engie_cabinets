import serial
from serial import SerialException
import time
import csv
import os
import pandas as pd
import numpy


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
        if '9503830353135190A221' in hwid:
          print('Requested device found temperature arduino')
          print(port)
          Megas.append(port)

print('Temp arduino as port:')          
print(Megas)
ser1 = serial.Serial(str(Megas[0]),  9600, timeout = 25)




def arduino_read(port):
    data = port.readline().decode("utf-8")
    print(type(data))
    if(len(data)) == 56 :
        with open ("temperature.csv","a") as file:
                    writer = csv.writer(file, delimiter="|")
                    writer.writerow([time.asctime(),data[0:5], data[13:18]])
    #     with open ("temperature.csv","a") as file:
    #                 writer = csv.writer(file, delimiter="|")
    #                 writer.writerow([time.asctime(),data])
    # print(data)
    return data


while(True):
    arduino_read(ser1)

    
   
   
    
   
    
    