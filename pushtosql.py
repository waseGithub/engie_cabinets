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





colnames = ['datetime','Channel','Name','timestamp','tempC','pressurehPa','total_tips_since_start','volume_this_tipml','total_vol_since_startml','tips_this_day','vol_this_dayml','tips_this_hour','vol_this_hourml','net_gas_attributable_to_test_sample_since_startmlg']
data = pd.read_csv ('/home/wase-cabinet/wase-cabinet/flowmeter_push.csv',  names=colnames, on_bad_lines='skip')
#data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/flowmeter_push.csv')  
df_flow = pd.DataFrame(data)





data = pd.read_csv (r'/home/wase-cabinet/wase-cabinet/temp_push.csv')  
#data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/temp_push.csv')  
df_temp = pd.DataFrame(data)



def resample_mean(df, time, cols, round_val, level_name):
  df.dropna(inplace=True)
  df =  df[(df.astype(float) >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].mean() 
  df = df.round(round_val)
  return df

def resample_sum(df, time, cols, round_val, level_name):
  df.dropna(inplace=True)
  df= df[(df.astype(float) >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].sum()
  df = df.round(round_val)
  return df

def resample_max(df, time, cols, round_val, level_name):
  df.dropna(inplace=True)
  display(df)
  df= df[(df.astype(float) >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].max()
  df = df.round(round_val)
  return df






df_temp['datetime'] = pd.to_datetime(df_temp['datetime'], errors='coerce')
df_temp.set_index(['probe_id', 'datetime'], inplace = True)
ls = list(df_temp.columns)
df_temp = df_temp.apply(pd.to_numeric, errors='coerce')
df_temp = resample_mean(df_temp, '5T', ls, 3, 'probe_id')
df_temp.reset_index(inplace=True)
df_temp['datetime'] = df_temp['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')





df_flow = df_flow.drop(['net_gas_attributable_to_test_sample_since_startmlg', 'timestamp', 'tips_this_day', 'tips_this_hour', 'tips_this_hour', 'vol_this_dayml'], axis = 1)

df_flow['datetime'] = pd.to_datetime(df_flow['datetime'], errors='coerce')

df_flow.set_index(['datetime', 'Channel', 'Name'], inplace=True)
df_1 = resample_max(df_flow, '5T', ['total_tips_since_start', 'total_vol_since_startml'], 3, 'Name')

'volume_this_tipml'
df_2 = resample_mean(df_flow, '5T', ['tempC', 'pressurehPa'], 3, 'Name')
df_3 = resample_sum(df_flow, '5T', ['volume_this_tipml'], 3, 'Name')
df_3 = df_3.rename(columns = {'volume_this_tipml' : 'volume_this_tip_intervalml'})





df_flow = pd.concat([df_1, df_2, df_3], axis=1)
df_flow.reset_index(inplace=True)
df_flow['datetime'] = df_flow['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

print(df_flow)





cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='cabinet_datasets')


cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_temp.columns.tolist()])
for i,row in df_temp.iterrows():
    sql = "INSERT INTO `temperature` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

os.remove(r'/home/wase-cabinet/wase-cabinet/temp_push.csv')
 

cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in df_flow.columns.tolist()])
for i,row in df_flow.iterrows():
    sql = "INSERT INTO `flowmeter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()

os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')



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


