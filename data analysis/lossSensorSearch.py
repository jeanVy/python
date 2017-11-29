
import pandas as pd
import numpy as np
from datetime import timedelta as td
from datetime import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine
import sys
import requests
import csv
import json
import os

list_days =['3days']
t_num =[3]
total_data = []
tdata = raw_input('from: ')
fdata = raw_input('to: ')
for i, day in enumerate(list_days):
    
    days = day
    tdate = dt.strptime(fdata, "%Y-%m-%d %H:%M:%S")
    fdate = dt.strptime(tdata, "%Y-%m-%d %H:%M:%S")
    print fdate,tdate
    engine = create_engine('mysql+pymysql://root:senslope@127.0.0.1/senslopedb')
    query = "SELECT name FROM senslopedb.site_column_props order by name asc"
    df = pd.io.sql.read_sql(query,engine)
    all_data= []
    for site in df.name:
       collected = []
       query_latest = "select timestamp,id from senslopedb.%s  where timestamp between '%s' and '%s' order by timestamp desc"%(site,fdate,tdate)
       df_latest = pd.io.sql.read_sql(query_latest,engine)
       dfa = pd.DataFrame(df_latest)
       dfa.to_csv('//var//www//html//temp//data//json_sensor//%s_json_3days.csv'%(site))
       
       