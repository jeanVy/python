import base64
import urllib2
import urllib
import sqlalchemy
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine
import sys
import json
import datetime
import fitbit_profile as fp


def sleep_logs():
    auth_id = token
    TokenURL = "https://api.fitbit.com/1/user/%s/sleep/date/%s.json"%(user_id,date)
    req = urllib2.Request(TokenURL)
        
    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', 'Bearer ' + auth_id)
    try:
        response = urllib2.urlopen(req)
        FullResponse = response.read()
        dfFull_sleep = json.loads(FullResponse)
        print dfFull_sleep
        
    except urllib2.URLError as e:
         print e.code
         print e.read()

#################################     MAIN     ################################

def main():
    auth_id = token
    list_data = ['steps','calories','distance']
    data_all = []
    calories_df = []
    mets_df = []
    distance_df = []
    
    for data in list_data:
        TokenURL = "https://api.fitbit.com/1/user/%s/activities/%s/date/today/1d/15min/time/00:00/23:59.json"%(user_id,data)
        req = urllib2.Request(TokenURL)
        
        #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
        req.add_header('Authorization', 'Bearer ' + auth_id)
        try:
            response = urllib2.urlopen(req)
            FullResponse = response.read()
            dfFull = json.loads(FullResponse)
            
            if data == 'steps':
                for i in range(len(dfFull['activities-' + data + '-intraday']['dataset'])):
                    ts = dfFull['activities-' + data + '-intraday']['dataset'][i]['time']
                    steps = dfFull['activities-' + data + '-intraday']['dataset'][i]['value']
                    data_all.append({'ts':date +" "+ts,'steps':steps})
            if data == 'calories' :
                for i in range(len(dfFull['activities-' + data + '-intraday']['dataset'])):
                    calories = dfFull['activities-' + data + '-intraday']['dataset'][i]['value']
                    mets = dfFull['activities-' + data + '-intraday']['dataset'][i]['mets']
                    mets_df.append({'mets':mets})
                    calories_df.append({data:calories})
                    
            if data == 'distance' :
                for i in range(len(dfFull['activities-' + data + '-intraday']['dataset'])):
                    distance = dfFull['activities-' + data + '-intraday']['dataset'][i]['value']
                    distance_df.append({data:distance})
        except urllib2.URLError as e:
          print data
          print e.code
          print e.read()
          result = fp.refresh_token(r_token,id)
          if len(result) != 0:
              main()
#    sleep_data = sleep_logs()
    data_all = pd.DataFrame(data_all)  
    data_all.set_index('ts')
    data_all['distance'] = pd.DataFrame(distance_df)  
    data_all['calories'] = pd.DataFrame(calories_df)  
    data_all['mets'] = pd.DataFrame(mets_df)
    data_all.columns =['steps','timestamp','distance','calories','calories_mets']
    with engine.connect() as conn, conn.begin():
        data_all.to_sql('%s_fitbit_data'%id, conn, if_exists='append', index=False)
        conn.execute('ALTER TABLE `%s_fitbit_data` ADD COLUMN `id` INT NOT NULL AUTO_INCREMENT FIRST,ADD PRIMARY KEY (`id`);'%id)
        
currentDT = datetime.datetime.now()
date = currentDT.strftime("%Y-%m-%d")
engine = create_engine('mysql+mysqldb://kikxroot:yM83jkikx!@127.0.0.1/kikxdb')
user_id = str(sys.argv[1])
r_token = str(sys.argv[2])
token = str(sys.argv[3])
id = str(sys.argv[4])
main()
