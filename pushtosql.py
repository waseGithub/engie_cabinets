#!/usr/bin/env python
# coding: utf-8

import sqlite3
from google.cloud import storage
import pandas as pd 
import numpy as np
from datetime import datetime
import mysql.connector 
import sys 
import os
import pandas as pd






data = pd.read_csv (r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')   
df_flow = pd.DataFrame(data)
data = pd.read_csv (r'/home/wase-cabinet/wase-cabinet/temp_push.csv')  
df_temp = pd.DataFrame(data)








cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='cabinet_datasets')
cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_flow.columns.tolist()])
for i,row in df_flow.iterrows():
    sql = "INSERT INTO `flowmeter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()


cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_temp.columns.tolist()])
for i,row in df_temp.iterrows():
    sql = "INSERT INTO `temperature` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()
 




# Create cursor
my_cursor = cnx.cursor()


# # Execute Query
# my_cursor.execute("SELECT * from flowmeter")

# # Fetch the records
# result = my_cursor.fetchall()

# for i in result:
#     print(i)

# Close the connection
cnx.close()
os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')
