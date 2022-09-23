import os
import uuid

from server.utils_api.Authorization import Authorization


class OS1Common:

    def __init__(self):
        return

    @staticmethod
    def get_headers():
        auth_object = Authorization()
        token = auth_object.fetch_token()
        tenant_id = os.getenv('OS1_TENANT')
        headers = {
            'X-COREOS-ACCESS': token,
            'X-COREOS-TID': tenant_id,
            'X-COREOS-USERINFO': '{"id":1,"name":"abc"}',
            'X-COREOS-REQUEST-ID': str(uuid.uuid4()),
            'Content-Type': 'application/json'
        }
        return headers;