#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import sqlite3
from google.cloud import storage
import pandas as pd 
import numpy as np
from datetime import datetime
import mysql.connector 
import sys 
import os

# data = pd.read_csv (r'/home/pi/wase-cabinet/file_7.csv')   
data = pd.read_csv(r'/home/harvey/Documents/WASE/wase-cabinet/file_7.csv') 
data2 = pd.read_csv(r'/home/harvey/Documents/WASE/wase-cabinet/file_6.csv') 
df = pd.DataFrame(data)
df2 = pd.DataFrame(data)

ls = ['datetime', 'error_status', 'column_c']

for i in np.arange(1,10):
    present = 'card_present_channel_' + str(i)
    enabled = 'card_enabled_channel_' + str(i)
    voltage = 'card_voltage_channel_' + str(i)
    current = 'card_current_channel_' + str(i) 
    ls.extend([present, enabled, voltage, current])





df.columns = ls
df2.columns = ls

df['datetime'] = pd.to_datetime(df['datetime'])
df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
df2['datetime'] = pd.to_datetime(df2['datetime'])
df2['datetime'] = df2['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')



df = df.dropna()
df2 = df2.dropna()

df.set_index(['datetime', 'error_status', 'column_c'], inplace =True)
df2.set_index(['datetime', 'error_status', 'column_c'], inplace =True)

print(df2)

cols = len(df.columns)
cols_ls = np.linspace(0, cols, 10)
print(cols_ls)

cols_ls_len = len(cols_ls)
index = 0 
index2 = 9
concat_df = pd.DataFrame()

def rename_slice(d, col_name, dex_num):
    d = d.rename({col_name + '_' + str(dex_num) : col_name}, axis='columns')
    return d



for i in np.arange(0, cols_ls_len-1, 1): 
    index += 1
    df_slice = df.iloc[:, int(cols_ls[int(i)]):int(cols_ls[int(i)+1])]
    df_slice = rename_slice(df_slice, 'card_present_channel', index)
    df_slice = rename_slice(df_slice, 'card_enabled_channel', index)
    df_slice = rename_slice(df_slice, 'card_voltage_channel', index)
    df_slice = rename_slice(df_slice, 'card_current_channel', index)
    df_slice['tank_id'] = index
    index2 += 1
    
    df_slice2 = df2.iloc[:, int(cols_ls[int(i)]):int(cols_ls[int(i)+1])]
    df_slice2 = rename_slice(df_slice2, 'card_present_channel', index)
    df_slice2 = rename_slice(df_slice2, 'card_enabled_channel', index)
    df_slice2 = rename_slice(df_slice2, 'card_voltage_channel', index)
    df_slice2 = rename_slice(df_slice2, 'card_current_channel', index)
    df_slice2['tank_id'] = index2

    concat_df = concat_df.append(df_slice)
    concat_df = concat_df.append(df_slice2)


concat_df.reset_index(inplace=True)
concat_df.set_index(['datetime','tank_id', 'error_status', 'column_c'], inplace=True)

concat_df.to_csv('out.csv')
df = concat_df.reset_index()



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


# # Execute Query
# my_cursor.execute("SELECT * from current_data")

# # Fetch the records
# result = my_cursor.fetchall()

# for i in result:
#     print(i)

cnx.close()


os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')
