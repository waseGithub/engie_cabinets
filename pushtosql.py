#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np

data = pd.read_csv (r'/home/pi/wase-cabinet/file_7.csv')   
df = pd.DataFrame(data)

ls = ['datetime', 'error_status', 'column_c']

for i in np.arange(1,10):
    present = 'card_present_channel_' + str(i)
    enabled = 'card_enabled_channel_' + str(i)
    voltage = 'card_voltage_channel_' + str(i)
    current = 'card_current_channel_' + str(i) 
    ls.extend([present, enabled, voltage, current])




print(ls)
df.columns = ls
df['datetime'] = pd.to_datetime(df['datetime'])
df = df.dropna()
print(df)

import sqlite3
from google.cloud import storage
import pandas as pd 
import numpy as np
from datetime import datetime
import mysql.connector 
import sys 
import os


cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='cabinet_datasets')
cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df.columns.tolist()])


for i,row in df.iterrows():
    sql = "INSERT INTO `current_data` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

print(df) 



# Create cursor
my_cursor = cnx.cursor()


cnx.close()
# os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')
