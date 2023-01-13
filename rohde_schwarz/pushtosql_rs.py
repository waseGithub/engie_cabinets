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
from pathlib import Path



barrels_postion = {'2C':1, '2B':1,'1B':3, '1A':1, '3B':2, '2A':2, '3C':3, '1C':4, '3A':4}


def format_rs_csv(csvdest):
    path2csv = Path(csvdest)
    csvlist = path2csv.glob("*.csv")

    for i in csvlist:
        print(i)
        csvlist = [] 
        csvlist.append(i)


    csv = csvlist[0]

    df_header = pd.read_csv(csv, nrows=14, names=['attribute', 'data'])
    colnames = ["Timestamp","U1[V]","I1[A]","P1[W]","U2[V]","I2[A]","P2[W]","U3[V]","I3[A]","P3[W]","U4[V]","I4[A]","P4[W]"]
    df = pd.read_csv(csv, skiprows=16, names=colnames)
    # print(df)


    start_time = df_header[df_header['attribute'] == '#Start Time'].data.values[0]
    start_date = df_header[df_header['attribute'] == '#Date'].data.values[0]
    start_datetime = str(str(start_date) + " " + str(start_time))
    increment = df_header[df_header['attribute'] == '#Logging Interval[s]'].data.values[0]
    increment = int(float(increment))/ 60
    count_row = df.shape[0] 
    duration = increment * (count_row)
    end_datetime= pd.to_datetime(start_datetime) + pd.to_timedelta(duration,'m')
        # print(duration)
        # print(count_row)    
        # print("start time", start_datetime)
        # print("end time", end_datetime)

    ls_datetime_range = pd.date_range(start=start_datetime, periods=count_row, freq='5Min')
    df_datetimes = pd.DataFrame(ls_datetime_range, columns=['datetime'])
    df = pd.concat([df, df_datetimes], axis=1)
    df.set_index('datetime', inplace =True)
    return df





    
def append_rs_csv_to_ls(df, tank_names_ls):

    single_tank_ls = []
    for tank in tank_names_ls:
        print(tank)
        index_value = barrels_postion.get(tank)
        print(index_value)

        single_tank_df = df[["U" + str(index_value) + "[V]", "I" + str(index_value) +"[A]", "P" + str(index_value) + "[W]"]]

        
        # single_tank_df['ID'] = tank
        single_tank_df.insert(1, "ID", tank, True)

      


        # single_tank_df.loc['ID'] = tank
        
        single_tank_df = single_tank_df.rename(columns={"U" + str(index_value) + "[V]" :'V', "I" + str(index_value) +"[A]" : 'A', "P" + str(index_value) + "[W]":'P'})
        single_tank_ls.append(single_tank_df)
    concat_df = pd.concat(single_tank_ls, axis=0)
    concat_df.reset_index(inplace=True)
    concat_df.set_index(['datetime', 'ID'], inplace=True)
    concat_df = concat_df.groupby([pd.Grouper(freq='5T', level='datetime'), pd.Grouper(level='ID')])['V', 'A', 'P'].mean()  
    return concat_df
    


    # tank_1 = df[["U1[V]", "I1[A]", "P1[W]"]]
    # tank_1['ID'] = 1
    # tank_1 = tank_1.rename(columns={'U1[V]': 'V', 'I1[A]': 'A', 'P1[W]': 'P'})
    # tank_2 = df[["U2[V]", "I2[A]", "P2[W]"]]
    # tank_2['ID'] = 2
    # tank_2 = tank_2.rename(columns={'U2[V]': 'V', 'I2[A]': 'A', 'P2[W]': 'P'})
    # tank_3 = df[["U3[V]", "I3[A]", "P3[W]"]]
    # tank_3['ID'] = 3
    # tank_3 = tank_3.rename(columns={'U3[V]': 'V', 'I3[A]': 'A', 'P3[W]': 'P'})
    # tank_4 = df[["U4[V]", "I4[A]", "P4[W]"]]
    # tank_4['ID'] = 4
    # tank_4 = tank_4.rename(columns={'U4[V]': 'V', 'I4[A]': 'A', 'P4[W]': 'P'})

    # df = pd.concat([tank_1, tank_2, tank_3, tank_4], axis=0) 
    # df.reset_index(inplace=True)
    # df.set_index(['datetime', 'ID'], inplace=True)
    # df = df.groupby([pd.Grouper(freq='5T', level='datetime'), pd.Grouper(level='ID')])['V', 'A', 'P'].mean()   
    # return df




power_ls = []    
# print(power_ls)



#########
#########


# psu_pathtop = '/home/farscopestudent/Documents/WASE/wase-cabinet/rohde_schwarz'
# psu_pathmid = '/home/farscopestudent/Documents/WASE/wase-cabinet/rohde_schwarz'
# psu_pathbot = '/home/farscopestudent/Documents/WASE/wase-cabinet/rohde_schwarz'

psu_pathtop = '/run/user/1000/gvfs/ftp:host=192.168.100.107,user=toppsu/int/logging'
psu_pathmid = '/run/user/1000/gvfs/ftp:host=192.168.100.104,user=midpsu/int/logging'
psu_pathbot = '/run/user/1000/gvfs/ftp:host=192.168.100.103,user=botpsu/int/logging'

link_ls = [psu_pathbot, psu_pathmid, psu_pathtop]

df_bot= format_rs_csv(link_ls[0])
df_mid = format_rs_csv(link_ls[1])
df_top = format_rs_csv(link_ls[2])






df_bot = append_rs_csv_to_ls(df_bot, ['1A', '2A', '1B', '3A'])
df_mid = append_rs_csv_to_ls(df_mid, ['2B', '3B', '3C', '1C'])
df_top = append_rs_csv_to_ls(df_top, ['2C'])

df_ls = [df_bot , df_mid , df_top]
power_df = pd.concat(df_ls, axis=0) 


print(power_df)



 




######################
######################
######################


# colnames = ['datetime','Channel','Name','timestamp','tempC','pressurehPa','total_tips_since_start','volume_this_tipml','total_vol_since_startml','tips_this_day','vol_this_dayml','tips_this_hour','vol_this_hourml','net_gas_attributable_to_test_sample_since_startmlg']
# data = pd.read_csv ('/home/wase-cabinet/wase-cabinet/flowmeter_push.csv',  names=colnames, on_bad_lines='skip',skiprows=2 )
# #data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/flowmeter_push.csv')  
# df_flow = pd.DataFrame(data)





# data = pd.read_csv (r'/home/wase-cabinet/wase-cabinet/temp_push.csv')  
# #data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/temp_push.csv')  
# df_temp = pd.DataFrame(data)



# def resample_mean(df, time, cols, round_val, level_name):
#   df.dropna(inplace=True)
#   df =  df[(df.astype(float) >= 0.0).all(1)]
#   df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].mean() 
#   df = df.round(round_val)
#   return df

# def resample_sum(df, time, cols, round_val, level_name):
#   df.dropna(inplace=True)
#   df= df[(df.astype(float) >= 0.0).all(1)]
#   df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].sum()
#   df = df.round(round_val)
#   return df

# def resample_max(df, time, cols, round_val, level_name):
#   df.dropna(inplace=True)
#   print(df)
#   df= df[(df.astype(float) >= 0.0).all(1)]
#   df = df.groupby([pd.Grouper(freq=time, level='datetime'), pd.Grouper(level=level_name)])[cols].max()
#   df = df.round(round_val)
#   return df






# df_temp['datetime'] = pd.to_datetime(df_temp['datetime'], errors='coerce')
# df_temp.set_index(['probe_id', 'datetime'], inplace = True)
# ls = list(df_temp.columns)
# df_temp = df_temp.apply(pd.to_numeric, errors='coerce')
# df_temp = resample_mean(df_temp, '30T', ls, 3, 'probe_id')
# df_temp.reset_index(inplace=True)
# df_temp['datetime'] = df_temp['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')





# df_flow = df_flow.drop(['net_gas_attributable_to_test_sample_since_startmlg', 'timestamp', 'tips_this_day', 'tips_this_hour', 'tips_this_hour', 'vol_this_dayml'], axis = 1)

# df_flow['datetime'] = pd.to_datetime(df_flow['datetime'], errors='coerce')

# df_flow.set_index(['datetime', 'Channel', 'Name'], inplace=True)
# df_1 = resample_max(df_flow, '30T', ['total_tips_since_start', 'total_vol_since_startml'], 3, 'Name')

# 'volume_this_tipml'
# df_2 = resample_mean(df_flow, '30T', ['tempC', 'pressurehPa'], 3, 'Name')
# df_3 = resample_sum(df_flow, '30T', ['volume_this_tipml'], 3, 'Name')
# df_3 = df_3.rename(columns = {'volume_this_tipml' : 'volume_this_tip_intervalml'})





# df_flow = pd.concat([df_1, df_2, df_3], axis=1)
# df_flow.reset_index(inplace=True)
# df_flow['datetime'] = df_flow['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

# print(df_flow)





# cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='cabinet_datasets')


# cursor = cnx.cursor()
# cols = "`,`".join([str(i) for i in df_temp.columns.tolist()])
# for i,row in df_temp.iterrows():
#     sql = "INSERT INTO `temperature` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
#     cursor.execute(sql, tuple(row))
#     cnx.commit()

# os.remove(r'/home/wase-cabinet/wase-cabinet/temp_push.csv')
 

# cursor = cnx.cursor()
# cols = "`,`".join([str(i) for i in df_flow.columns.tolist()])
# for i,row in df_flow.iterrows():
#     sql = "INSERT INTO `flowmeter` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
#     cursor.execute(sql, tuple(row))
#     cnx.commit()

# os.remove(r'/home/wase-cabinet/wase-cabinet/flowmeter_push.csv')



# # Create cursor
# my_cursor = cnx.cursor()


# # # Execute Query
# # my_cursor.execute("SELECT * from flowmeter")

# # # Fetch the records
# # result = my_cursor.fetchall()

# # for i in result:
# #     print(i)

# # Close the connection
# cnx.close()