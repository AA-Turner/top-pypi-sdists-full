import requests
from rox.core.logging.logging import Logging

class RequestData:
    def __init__(self, url, query_params):
        self.url = url
        self.query_params = query_params if query_params is not None else {}

class Request:
    def send_get(self, request_data):
        Logging.get_logger().debug('GET request to %s' % (request_data.url))
        resp = requests.get(request_data.url, params=request_data.query_params, timeout=30)
        return resp

    def send_post(self, request_data):
        Logging.get_logger().debug('POST request to %s' % (request_data.url))
        resp = requests.post(request_data.url, json=request_data.query_params, timeout=30)
        return resp
