from decouple import config
import json
import requests

auth_token_url = "https://api.codechef.com/oauth/token"
oauth_url = "https://api.codechef.com/oauth/authorize"

def makeRequest(type, url, body={}):

    CLIENT_ID = config('CLIENT_ID')
    CLIENT_SECRET = config('CLIENT_SECRET')
    STATE = config('STATE')

    data = {
        "grant_type": "client_credentials",
        "scope": "public",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    # Add logic to store ACCESS TOKEN in a secure manner. - Client Grant

    res = requests.post(auth_token_url, data)
    json_data = json.loads(res.text)
    ACCESS_TOKEN = json_data.get('result').get('data').get('access_token')

    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}

    if type == "GET":
        res = requests.get(url, headers=headers)
    if type == "POST":
        res = requests.post(url, data=body, headers=headers)

    return res
