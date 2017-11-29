import base64
import urllib2
import urllib
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import sys
import json
import fitbit_profile as fp

auth_id = sys.argv[1]
id = sys.argv[2]

base = 'public.localhost'

uri = 'http://%s/fitbit'%base

#if base == "kikxapp.com" or  base == "www.kikxapp.com":
#    client_id = "22CKHB"
#    secret_id = "07c2e9f3527fc37d4df40d8557cc03fb"
#else:

client_id = "22CK2Y"
secret_id = "f1f4ad8872a71d2f25df999299e78f94"
    
    
    
#These are the secrets etc from Fitbit developer
OAuthTwoClientID = client_id
ClientOrConsumerSecret = secret_id

#This is the Fitbit URL
TokenURL = "https://api.fitbit.com/oauth2/token"

#I got this from the first verifier part when authorising my application
AuthorisationCode = auth_id

#Form the data payload
BodyText = {'code' : AuthorisationCode,
            'redirect_uri' : uri,
            'client_id' : OAuthTwoClientID,
            'grant_type' : 'authorization_code'}

BodyURLEncoded = urllib.urlencode(BodyText)
print BodyURLEncoded

#Start the request
req = urllib2.Request(TokenURL,BodyURLEncoded)

#Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
req.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

#Fire off the request
try:
    response = urllib2.urlopen(req)
    FullResponse = response.read()
    dfFull = json.loads(FullResponse)
    token_id = str(dfFull['access_token'])
    user_id = str(dfFull['user_id'])
    refresh_token = str(dfFull['refresh_token'])
    members_id = id
    result_fp = fp.main(user_id,refresh_token,token_id,members_id)
    bday = result_fp['user']['dateOfBirth']
    w = result_fp['user']['weight']
    h = result_fp['user']['height']
    country = result_fp['user']['timezone']
    gender = result_fp['user']['gender'] 
    engine = create_engine('mysql+mysqldb://kikxroot:yM83jkikx!@127.0.0.1/kikxdb')
    query = "INSERT INTO `fitbit_users` (`members_id`, `access_token`, `refresh_token`, `user_id`,`date_birth`,`weight`,`height`,`country`,`gender`)"
    query +=" VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(members_id,token_id,refresh_token,user_id,bday,w,h,country,gender)
    df = pd.io.sql.read_sql(query,engine)
    print dfFull
   
except urllib2.URLError as e:
  print e.code
  print e.read()





