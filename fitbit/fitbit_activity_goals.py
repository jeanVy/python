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
    TokenURL = "https://api.fitbit.com/1/user/%s/sleep/goal.json"%(user_id)
    req = urllib2.Request(TokenURL)
        
    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', 'Bearer ' + auth_id)
    try:
        response = urllib2.urlopen(req)
        FullResponse = response.read()
        dfFull_sleep = json.loads(FullResponse)
        sleep = str(dfFull_sleep['goal']['minDuration'])
        return sleep
        
    except urllib2.URLError as e:
         print e.code
         print e.read()
         result = fp.refresh_token(r_token,id)
         if len(result) != 0:
              main()

#################################     MAIN     ################################

def main():
    auth_id = token
    TokenURL = "https://api.fitbit.com/1/user/%s/activities/date/%s.json"%(user_id,date)
    req = urllib2.Request(TokenURL)
        
    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', 'Bearer ' + auth_id)
    try:
        response = urllib2.urlopen(req)
        FullResponse = response.read()
        dfFull = json.loads(FullResponse)
        steps = str(dfFull['goals']['steps'])
        calories = str(dfFull['goals']['caloriesOut'])
        distance = str(dfFull['goals']['distance'])
        members_id = id
        sleep = sleep_logs()
        query = "INSERT INTO `users_fitbit_goals` (`members_id`, `steps`, `calories`, `distance`,`sleep`)"
        query +=" VALUES ('%s','%s','%s','%s','%s')"%(members_id,steps,calories,distance,sleep)
        pd.io.sql.read_sql(query,engine)
        
        
    except urllib2.URLError as e:
         print e.code
         print e.read()
         result = fp.refresh_token(r_token,id)
         if len(result) != 0:
              main()
              
currentDT = datetime.datetime.now()
date = currentDT.strftime("%Y-%m-%d")
engine = create_engine('mysql+mysqldb://kikxroot:yM83jkikx!@127.0.0.1/kikxdb')
user_id = str(sys.argv[1])
r_token = str(sys.argv[2])
token = str(sys.argv[3])
id = str(sys.argv[4])
main()
