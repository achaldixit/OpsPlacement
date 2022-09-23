import json
import os

from flask import Flask, make_response, jsonify, request
import requests
import uuid
from server.utils_api.Authorization import Authorization
from server.utils_api.OS1Common import OS1Common


class Location:
    url = ''

    def __init__(self):
        self.url = os.getenv('OS1_BASE_URL')
        return

    def initialize(self):
        path = '/core/api/v1/locations/country/search?city=New Delhi'
        headers = OS1Common.get_headers()
        payload = {}

        rsp = requests.request("GET", self.url + path, headers=headers, data=payload)

        data = json.loads(rsp.text)

        print(data)

        return True

    # Get County Search Location API in Country Congfig
    def get_all_location_pincodes(self,city):

        path = '/core/api/v1/locations/country/search?city='
        headers = OS1Common.get_headers()
        payload = {}

        rsp = requests.request("GET", self.url + path + city, headers=headers, data=payload)
        if rsp.status_code == requests.codes.ok:
            response = make_response(rsp.text, 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return 'Bad Request', 400

    # def create_location_type(self, payload):
    #     path = '/core/api/v1/locations/'
    #     headers = OS1Common.get_headers()

    #     rsp = requests.request("POST", self.url + path, headers=headers, data=json.dumps(payload))
    #     if rsp.status_code == requests.codes.ok:
    #         response = make_response(rsp.text, 200)
    #         response.headers["Content-Type"] = "application/json"
    #         return response
    #     else:
    #         return 'Bad Request', 400

    def create_location(self, payload):
        return None

    def get_location_by_id(self,location_id):
        path = '/core/api/v1/locations/{}'.format(location_id)
        headers = OS1Common.get_headers()
        payload = {}

        rsp = requests.request("GET", self.url + path, headers=headers, data=payload)
        if rsp.status_code == requests.codes.ok:
            response = make_response(rsp.text, 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return 'Bad Request', 400