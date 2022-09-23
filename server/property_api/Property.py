import json
import os

from flask import Flask, make_response, jsonify, request
import requests
import uuid
from server.utils_api.Authorization import Authorization
from server.utils_api.OS1Common import OS1Common


class Property:

    url = ''

    def __init__(self):
        self.url = os.getenv('OS1_BASE_URL')
        return

    def get_all_props(self):
        path = '/app/fpa/api/v1/properties'
        headers = OS1Common.get_headers()
        payload = {}

        rsp = requests.request("GET", self.url + path, headers=headers, data=payload)

        data = json.loads(rsp.text)

        #Obtain Lat-Longs Only

        return data

    # we are not creating any property as of now
    def create_property(self, payload):
        path = '/app/fpa/api/v1/properties'
        headers = OS1Common.get_headers()

        rsp = requests.request("POST", self.url + path, headers=headers, data=json.dumps(payload))
        if rsp.status_code == requests.codes.ok:
            response = make_response(rsp.text, 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return 'Bad Request', 400

    def get_property_by_id(self, property_id):
        path = '/app/fpa/api/v1/properties/:{}'.format(property_id)
        headers = OS1Common.get_headers()
        payload = {}

        rsp = requests.request("GET", self.url + path, headers=headers, data=payload)
        if rsp.status_code == requests.codes.ok:
            response = make_response(rsp.text, 200)
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            return 'Bad Request', 400