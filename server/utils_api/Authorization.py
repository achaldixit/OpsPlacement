import os
import requests
import json
import uuid

cache = dict()


class Authorization:

    def __init__(self):
        return

    @staticmethod
    def generate_token():
        url = os.getenv('OS1_BASE_URL')
        client_id = os.getenv('OS1_CLIENT_ID')
        client_secret = os.getenv('OS1_CLIENT_SECRET')
        audience = os.getenv('OS1_DEFAULT_AUDIENCE')
        path = '/core/api/v1/aaa/auth/client-credentials'

        payload = json.dumps({
            "clientId": client_id,
            "clientSecret": client_secret,
            "audience": audience
        })
        headers = {
            'X-COREOS-REQUEST-ID': str(uuid.uuid4()),
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url + path, headers=headers, data=payload)
        if response.status_code == requests.codes.ok:
            return response.json()['data']['accessToken']
        else:
            print('Auth Failed')
            return None

    def fetch_token(self):
        if 'token' not in cache:
            cache['token'] = self.generate_token()
        return cache['token']