import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


def plot_plotly():
  y_axis = 'Module Current'
  fig = go.Figure()
    # df[column] = df[column][(df[[column]] < 30000).all(1)]
    #  df[column] = df[column][(df[[column]] > 0).all(1)]
    
  try:
    df.reset_index(inplace = True)
  except ValueError:
    pass

  for i in reactor_names:
    print(i)
    fig.add_trace(go.Scatter(
            x=df[df['Name'] == i]['datetime'],
            y=df[df['Name'] == i]['card_current_channel'],
            name = 'Tank' + str(i),
            line_shape='spline',
            connectgaps= False,
            line=dict(color= colours_dict.get(i))
        # Style name/legend entry with html tags
        ))

  fig.update_yaxes(showline=True, linewidth=2, gridcolor='lightgray', linecolor='black')
  fig.update_xaxes(showline=True, linewidth=2, gridcolor='lightgray', linecolor='black')
  fig.update_layout(legend=dict(orientation="v",yanchor="top",y=0.99,xanchor="right",x=1.01))
  fig.update_layout(template = "plotly_white", width=1000, height=600, yaxis_title=y_axis,font=dict(size=15), margin=dict(l=50,r=50,b=50,t=50,pad=3))

  fig.show()









#connect to mysql database
naturedb = mysql.connector.connect(
    host='34.89.81.147',
    database='cabinet_datasets',
    user='root',
    password='wase2022'
)
#test if connection worked
print(naturedb)

#read flowmeter data from sql to pandas
flow_db = pd.read_sql('SELECT*FROM flowmeter', con=naturedb)
#print(flow_db)

#find unique reactors, then split their data into different dataframes
reactor_names = flow_db['Name'].unique().tolist()
print(reactor_names)


#create line thickness dictionary, then make AD bolder
thick_dict = {reactor: 2 for reactor in reactor_names}
thick_dict.update({'4A':5, '4B':5, '4C':5})
# print(thick_dict)

#create colours dictionary for plot lines
colours_dict = {'1A': '#012969', '1B': '#2358ad', '1C': '#5f95ed', 
                '2A': '#8a1d01', '2B': '#c94a2a', '2C': '#ed6a18',
                '3A': '#297002', '3B': '#71d63a', '3C': '#64ed7d',
                '4A': '#6e036e', '4B': '#ba25ba', '4C': '#e629b6'
}

print(flow_db)


#read current data from sql to pandas
current_db = pd.read_sql('SELECT*FROM current_data', con=naturedb)
current_db['card_current_channel'] = current_db['card_current_channel'].astype('float')
print(current_db)






df = current_db
plot_plotly()













#voltage dictionary to differentiate between different voltages
#flow_dict = {reactor: flow_db.loc[flow_db['Name'] == reactor] for reactor in reactor_names}

# # #create plots of each different reactor
# plt.figure()
# for reactor in flow_dict:
#   sns.lineplot(x='index', y='total_vol_since_startml', data=flow_dict[reactor].reset_index(), label=f'{reactor}', linewidth=thick_dict[reactor], color=colours_dict[reactor])



# #find unique reactors, then split their data into different dataframes
# current_dict = {reactor: current_db.loc[current_db['Name'] == reactor] for reactor in reactor_names}
# #print(current_dict)

# #subsample each databse in curernt_dict as its quite big
# for reactor in current_dict:
#     current_dict[reactor] = current_dict[reactor].reset_index()
#     current_dict[reactor] = current_dict[reactor][::10]
#     current_dict[reactor]['card_current_channel'] = current_dict[reactor]['card_current_channel'].astype('float')
    

# print('test reactor', current_dict['1A']['card_current_channel'])
# #create plots of each different reactor
# # plt.figure()
# # for reactor in current_dict:
# #   sns.lineplot(x='index', y='card_current_channel', data=current_dict[reactor].reset_index(), label=f'{reactor}', linewidth=thick_dict[reactor], color=colours_dict[reactor])


# # plt.ylim(-5, 30)
# # plt.show()
