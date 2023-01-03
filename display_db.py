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



cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='cabinet_datasets')

# Create cursor
my_cursor = cnx.cursor()


# Execute Query
my_cursor.execute("SELECT * from current_data")

# Fetch the records
result = my_cursor.fetchall()

for i in result:
    print(i)

cnx.close()


