
# TODO automate the token pass through

import json
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient
import pprint
import elasticsearch
import bs4

def main():

    client_id = "2288TW"
    code = "6b01dd23c0ff08ea7c67ad4c7b607a8f"
    # Full scope scope = ["activity", "heartrate", "location", "nutrition", "profile", "settings", "sleep", "social", "weight"]
    scope = ["heartrate"]

    # Initialize client
    client = MobileApplicationClient(client_id)

    fitbit = OAuth2Session(client_id, client=client, scope=scope)
    authorization_url = "https://www.fitbit.com/oauth2/authorize"

    # Grab the URL for Fitbit's authorization page.
    auth_url, state = fitbit.authorization_url(authorization_url)
    # print(auth_url, state)

    print("Visit this page in your browser: {}".format(auth_url))

    """After authenticating,  Fitbit will redirect you to the URL 
        you specified in your application settings. 
        It contains the access token."""

    callback_url = input("Paste URL you get back here: ")

    # Now we extract the token from the URL to make use of it.
    strip_access_token = fitbit.token_from_fragment(callback_url)
    # print(strip_access_token)

    access_token = strip_access_token['access_token']
    # print(access_token)

    # At this point, assuming nothing blew up, we can make calls to the API as normal, for example:
    user = json.loads(fitbit.get(
        'https://api.fitbit.com/1/user/-/profile.json?2288TW=6b01dd23c0ff08ea7c67ad4c7b607a8f').content.decode('utf-8'))
    # print(user_json['user']['age'])

    #start_date = '2015/01/27'
    start_date = '2017-04-18'

    hr_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/{0}/{1}/{2}.json'.format(start_date, 'today', '1min')
    print(hr_url)

    #test_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec/time/00:00/00:01.json'
    test_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/{0}/1d/1min.json'.format(start_date)
    print(test_url)

    # works!
    #test_url = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec.json'
    #dict_data_heart_rate = json.loads(fitbit.get(test_url).content.decode('utf-8'))
    json_data_heart_rate = fitbit.get(test_url).content.decode('utf-8')

    es = elasticsearch.Elasticsearch()
    es.index(index='heartrate', doc_type='fitbit_heartrate', id=start_date, body=json_data_heart_rate)

    # pprint.pprint(json_data_heart_rate, width=4)

if __name__ == '__main__':
    main()