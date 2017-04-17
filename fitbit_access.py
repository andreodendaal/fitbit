
# TODO You should set "http://localhost/callback" as your callback URL

import json
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

# Set up your client ID and scope: the scope must match that which you requested when you set up your application.
client_id = "2288TW"
scope = ["activity", "heartrate", "location", "nutrition", "profile", "settings", "sleep", "social", "weight"]

# Initialize client
client = MobileApplicationClient(client_id)
fitbit = OAuth2Session(client_id, client=client, scope=scope)
authorization_url = "https://www.fitbit.com/oauth2/authorize"

# Grab the URL for Fitbit's authorization page.
auth_url, state = fitbit.authorization_url(authorization_url)
print(auth_url, state)
print("Visit this page in your browser: {}".format(auth_url))

token = fitbit.access_token

# After authenticating, Fitbit will redirect you to the URL you specified in your application settings. It contains the access token.
callback_url = input("Paste URL you get back here: ")

# Now we extract the token from the URL to make use of it.
fitbit.token_from_fragment(callback_url)

# We can also store the token for use later.
#token = fitbit['token']

# At this point, assuming nothing blew up, we can make calls to the API as normal, for example:
r = fitbit.get('https://api.fitbit.com/1/user/-/sleep/goal.json')
user = json.loads(fitbit.get('https://api.fitbit.com/1/user/-/profile.json?2288TW=6b01dd23c0ff08ea7c67ad4c7b607a8f').content)
heartrate = json.loads(fitbit.get('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json?2288TW=6b01dd23c0ff08ea7c67ad4c7b607a8f').content)

print(heartrate)
print(user['user']['age'])

