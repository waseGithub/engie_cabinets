import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots


app = dash.Dash()


def plot_plotly(df, y_axis, column, show_dash, index_ls):
  
  fig = go.Figure()
    # df[column] = df[column][(df[[column]] < 30000).all(1)]
    #  df[column] = df[column][(df[[column]] > 0).all(1)]
    
  try:
    df.reset_index(inplace = True)
  except ValueError:
    pass
  

  for i in index_ls:
    print(i)
    if show_dash == True:
      line_dict = {'1': '5px', 
                  '2': '10px',
                  '3': '1px',
                  '4': '0px'}
    else:
      line_dict = {'1': '0px', 
                  '2': '0px',
                  '3': '0px',
                  '4': '0px'} 
      
    line_width = {'1': 2, 
                 '2': 2,
                 '3': 2,
                 '4': 2}
    
    fig.add_trace(go.Scatter(
            x=df[df['Name'] == i]['datetime'],
            y=df[df['Name'] == i][column],
            name = 'Tank' + str(i),
            line_shape='spline',
            connectgaps= False, 
            line=dict(color= colours_dict.get(i), width=line_width.get(i[0]), dash=line_dict.get(i[0]))
        # Style name/legend entry with html tags
        ))

  fig.update_yaxes(showline=True, linewidth=2, gridcolor='lightgray', linecolor='black')
  fig.update_xaxes(showline=True, linewidth=2, gridcolor='lightgray', linecolor='black')
  fig.update_layout(legend=dict(orientation="v",yanchor="top",y=0.99,xanchor="right",x=1.01))
  fig.update_layout(template = "plotly_white", height=900, yaxis_title=y_axis,font=dict(size=15), margin=dict(l=50,r=50,b=50,t=50,pad=3))

 
  return fig 





def plot_plotly_subplot(df, y_axis, column, index_ls, grph_num):
  if grph_num > 3:
    fig = make_subplots(rows=2, cols=2, subplot_titles=("0.8V Tank", "1V Tank", "1.3V Tank", 'AD Tank'))
  else:
    fig = make_subplots(rows=2, cols=2, subplot_titles=("0.8V Tank", "1V Tank", "1.3V Tank"))
  X = range(1, 50+1)
  X = list(X)
  # colours = ['#595457','#9E1946', '#4D6CFA', '#DE0D92', '#C17817', '#4464AD', '#F8F991', '#2F0147']
  
  for i in index_ls[0:3]:
    fig.add_trace(go.Scatter(
              x=df[df['Name'] == i]['datetime'],
              y=df[df['Name'] == i][column],
              name = 'Tank' + str(i),
              line_shape='spline',
              connectgaps= False, 
              line=dict(color= colours_dict.get(i), width=2)),row=1, col=1)
    fig.update_yaxes(title_text="tank_1" + y_axis, row=1, col=1)
  
  for i in index_ls[3:6]:
    fig.add_trace(go.Scatter(
              x=df[df['Name'] == i]['datetime'],
              y=df[df['Name'] == i][column],
              name = 'Tank' + str(i),
              line_shape='spline',
              connectgaps= False, 
              line=dict(color= colours_dict.get(i), width=2)),row=1, col=2)

  
  for i in index_ls[6:9]:
    fig.add_trace(go.Scatter(
              x=df[df['Name'] == i]['datetime'],
              y=df[df['Name'] == i][column],
              name = 'Tank' + str(i),
              line_shape='spline',
              connectgaps= False, 
              line=dict(color= colours_dict.get(i), width=2)),row=2, col=1)
    fig.update_yaxes(title_text= y_axis, row=2, col=1)
    fig.update_xaxes(title_text= 'Datetime', row=2, col=1)
  
  if grph_num >  3:
    for i in index_ls[9:12]:
      fig.add_trace(go.Scatter(
                x=df[df['Name'] == i]['datetime'],
                y=df[df['Name'] == i][column],
                name = 'Tank' + str(i),
                line_shape='spline',
                connectgaps= False, 
                line=dict(color= colours_dict.get(i), width=2)),row=2, col=2)
      fig.update_xaxes(title_text= 'Datetime', row=2, col=2)
    
    
      
  
  
  

  
  


    



    
  fig.update_layout(template = "plotly_white", yaxis_title=y_axis,font=dict(size=15), height=900, margin=dict(l=50,r=50,b=50,t=50,pad=3))
  # fig.update_layout(legend=dict(orientation="v",yanchor="top",y=0.95,xanchor="right",x=1.01))
  fig.update_yaxes(showline=True, linewidth=2, gridcolor='lightgray', linecolor='black')
  fig.update_xaxes(showline=True, linewidth=2, gridcolor='lightgray', linecolor='black')






  return fig





###############
###############
###############






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
reactor_names.sort()
print(reactor_names)




#create colours dictionary for plot lines
colours_dict = {'1A': '#F9C7CF', '1B': '#F6828C', '1C': '#F2404F', 
                '2A': '#BFC7D9', '2B': '#8B9ABB', '2C': '#445374',
                '3A': '#C7F2A7', '3B': '#9AE75F', '3C': '#5CB11B',
                '4A': '#FF8533', '4B': '#FF6700', '4C': '#B84900'
}

print(flow_db)


#read current data from sql to pandas
current_db = pd.read_sql('SELECT*FROM current_data', con=naturedb)
current_db['card_current_channel'] = current_db['card_current_channel'].astype('float')
print(current_db)







fig_current = plot_plotly(current_db, 'Module Current (mA)', 'card_current_channel', False,reactor_names)
fig_flow = plot_plotly(flow_db, 'total vol since start (ml)', 'total_vol_since_startml',True,reactor_names)


fig_flow_subplot = plot_plotly_subplot(flow_db, 'total vol since start (ml)', 'total_vol_since_startml',reactor_names, 4)
fig_current_subplot = plot_plotly_subplot(current_db, 'Module Current (mA)', 'card_current_channel',reactor_names, 3)








# fig_current_G1 =  plot_plotly(current_db, 'Module Current', 'card_current_channel', False,reactor_names[0:3])
# fig_current_G2 =  plot_plotly(current_db, 'Module Current', 'card_current_channel', False,reactor_names[3:6])
# fig_current_G3 =  plot_plotly(current_db, 'Module Current', 'card_current_channel', False,reactor_names[6:9])







# fig_current_G1.show()
# fig_current_G2.show()
# fig_current_G3.show()


app = dash.Dash()



dcc.Interval 
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Cabinet Reactor data', style = {'textAlign':'center','marginTop':40,'marginBottom':1}),
       
        dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':'Current', 'value':fig_current},
            {'label':'Flow', 'value':fig_flow},
            {'label': 'Current Subplot', 'value':fig_current_subplot},
            {'label': 'Flow Subplot', 'value':fig_flow_subplot},
            ],
        value = fig_flow_subplot),
        dcc.Graph(id = 'bar_plot')
    ])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_value):
    print(dropdown_value)
    fig = dropdown_value
    return fig  



if __name__ == '__main__': 
    app.run_server(debug=False)

