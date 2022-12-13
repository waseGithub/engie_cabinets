#!/usr/bin/env python
# coding: utf-8


import pandas as pd

data = pd.read_csv (r'/home/pi/wase-cabinet/file_7.csv')   
df = pd.DataFrame(data)
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