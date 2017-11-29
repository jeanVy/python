import base64
import urllib2
import urllib
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import sys
import json



engine = create_engine('mysql+mysqldb://kikxroot:yM83jkikx!@127.0.0.1/kikxdb')

def add_fitbit_profile(bday,w,h,country,gender,id):
    query = "UPDATE `fitbit_users` SET `date_birth`='%s',`weight`='%s',`height`='%s',`country`='%s',`gender`='%s'"%(bday,w,h,country,gender)
    query+= "WHERE `members_id`='%s'"%(id)
    pd.io.sql.read_sql(query,engine)
    return 'done'


def change_refresh_token(newtoken,id):
    query = "UPDATE `fitbit_users` SET `refresh_token`='%s' WHERE `members_id`='%s'"%(newtoken,id)
    print query
    pd.io.sql.read_sql(query,engine)
    return 'done'

def refresh_token(token,id):

    #This is the Fitbit URL
    TokenURL = "https://api.fitbit.com/oauth2/token"
    
    #Form the data payload
    BodyText = {'refresh_token' : token,
                'grant_type' : 'refresh_token'}
    
    BodyURLEncoded = urllib.urlencode(BodyText)
    print BodyURLEncoded
    
    #Start the request
    req = urllib2.Request(TokenURL,BodyURLEncoded)
    
    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', 'Basic MjJDSzJZOmYxZjRhZDg4NzJhNzFkMmYyNWRmOTk5Mjk5ZTc4Zjk0')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    #Fire off the request
    try:
        response = urllib2.urlopen(req)
        FullResponse = response.read()
        dfFull = json.loads(FullResponse)
#        print dfFull
#        print dfFull['refresh_token']
        newtoken = dfFull['refresh_token']
        result = change_refresh_token(newtoken,id)
        if result == 'done':
            return newtoken
    except urllib2.URLError as e:
      print e.code
      print e.read()

#################################     MAIN     ################################

def main(user_id,r_token,token,id):
    auth_id = token
    TokenURL = "https://api.fitbit.com/1/user/-/profile.json"
    
    #Start the request
    req = urllib2.Request(TokenURL)
    
    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', 'Bearer ' + auth_id)
    try:
        response = urllib2.urlopen(req)
        FullResponse = response.read()
        dfFull = json.loads(FullResponse)
        return dfFull
    except urllib2.URLError as e:
      return e.code
      result = refresh_token(r_token)
      if result == 'done':
          main(user_id,r_token,token,id)