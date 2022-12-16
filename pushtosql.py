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


######################
######################
######################

def resample_mean(df, time, cols, round_val):
  df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level='tank_id'),pd.Grouper(level='error_status')])[cols].mean(numeric_only=True) 
  df = df.round(round_val)
  return df

def resample_sum(df, time, cols, round_val):
  df= df[(df >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level='tank_id')])[cols].sum()
  df = df.round(round_val)
  return df

def resample_max(df, time, cols, round_val):
  df= df[(df >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level='tank_id')])[cols].max()
  df = df.round(round_val)
  return df

######################
######################
######################

# data = pd.read_csv (r'/home/pi/wase-cabinet/file_7.csv')   
data = pd.read_csv(r'/home/farscopestudent/Documents/WASE/wase-cabinet/file_7.csv') 
data2 = pd.read_csv(r'/home/farscopestudent/Documents/WASE/wase-cabinet/file_6.csv') 
df = pd.DataFrame(data)
df2 = pd.DataFrame(data)



######################
######################
######################



ls = ['datetime', 'error_status', 'column_c']

for i in np.arange(1,10):
    present = 'card_present_channel_' + str(i)
    enabled = 'card_enabled_channel_' + str(i)
    voltage = 'card_voltage_channel_' + str(i)
    current = 'card_current_channel_' + str(i) 
    ls.extend([present, enabled, voltage, current])





df.columns = ls
df2.columns = ls





df = df.dropna()
df2 = df2.dropna()




df.set_index(['datetime', 'error_status', 'column_c'], inplace =True)
df2.set_index(['datetime', 'error_status', 'column_c'], inplace =True)



cols = len(df.columns)
cols_ls = np.linspace(0, cols, 10)


cols_ls_len = len(cols_ls)
index = 0 
index2 = 9
concat_df = pd.DataFrame()

def rename_slice(d, col_name, dex_num):
    d = d.rename({col_name + '_' + str(dex_num) : col_name}, axis='columns')
    return d



df_dict = {}

for i in np.arange(0, cols_ls_len-1, 1): 
    index += 1
    df_slice = df.iloc[:, int(cols_ls[int(i)]):int(cols_ls[int(i)+1])]
    df_slice = rename_slice(df_slice, 'card_present_channel', index)
    df_slice = rename_slice(df_slice, 'card_enabled_channel', index)
    df_slice = rename_slice(df_slice, 'card_voltage_channel', index)
    df_slice = rename_slice(df_slice, 'card_current_channel', index)


    index2 += 1
    df_slice2 = df2.iloc[:, int(cols_ls[int(i)]):int(cols_ls[int(i)+1])]
    df_slice2 = rename_slice(df_slice2, 'card_present_channel', index)
    df_slice2 = rename_slice(df_slice2, 'card_enabled_channel', index)
    df_slice2 = rename_slice(df_slice2, 'card_voltage_channel', index)
    df_slice2 = rename_slice(df_slice2, 'card_current_channel', index)

    df_name =  str(index)
    df_dict[df_name] = df_slice 

    df_name =  str(index2)
    df_dict[df_name] = df_slice2

    



concat_df = pd.concat(df_dict)
concat_df.reset_index(inplace =True)

concat_df = concat_df.loc[concat_df['card_present_channel'] == True]




concat_df = concat_df.rename(columns={'level_0':'tank_id'})





concat_df['datetime'] = pd.to_datetime(concat_df['datetime'])







######### resample current data 5min #########


concat_df.set_index(['datetime','tank_id','error_status'], inplace=True)
concat_df.to_csv('out.csv')
concat_df = resample_mean(concat_df, '5T', concat_df.columns, 3)
concat_df.drop(concat_df.columns[[0]],axis=1,inplace=True)
print(concat_df)


concat_df = concat_df.reset_index()





# df.drop(columns=['card_present_channel', 'card_enabled_channel'], inplace = True)
concat_df['datetime'] = concat_df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')


cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='cabinet_datasets')
cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in concat_df.columns.tolist()])


for i,row in concat_df.iterrows():
    sql = "INSERT INTO `current_data` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()





# Create cursor
my_cursor = cnx.cursor()


# # Execute Query
# my_cursor.execute("SELECT * from current_data")

# # Fetch the records
# result = my_cursor.fetchall()

# for i in result:
#     print(i)

cnx.close()


# os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')
