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




if __name__ == '__main__':
    
   
   
    
   
    
    ser1.flush()

    i = 0

   
    while True:
         i +=1
         print('Current count =')
         print(i)
         line1 = ser1.readline().decode("utf-8")
         print(line1)
            
            
            # with open ("temperature.csv","a") as f:
                
            #     writer = csv.writer(f, delimiter=",")
            #     writer.writerow([time.asctime(),line1])
            #     time.sleep(1000)
                

          
            # print('writing temperature data')
            # print(line1)
        #  except UnicodeDecodeError:
        #      pass