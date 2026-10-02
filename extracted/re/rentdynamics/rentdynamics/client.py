import datetime
import hashlib
import hmac
import json
import requests
import time

from collections import OrderedDict


class Client:
    api_key = None
    api_secret = None
    auth_token = None
    development = False
    user_id = None

    def __init__(self, api_key=None, api_secret=None, development=False, base_url=None,
                 base_development_url=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.base_development_url = base_development_url
        self.development = development

    def get(self, endpoint):
        headers = self.get_headers(endpoint)
        request_url = self.get_base_url() + endpoint
        return requests.get(request_url, headers=headers)

    def get_base_url(self):
        if self.development:
            if self.base_development_url:
                return self.base_development_url
            return 'https://api.rentdynamics.dev'
        else:
            if self.base_url:
                return self.base_url
            return 'https://api.rentdynamics.com'

    def get_headers(self, endpoint, body=None):
        timestamp = str(self.get_timestamp_milliseconds())
        nonce = self.get_nonce(timestamp=timestamp, url=endpoint, body=body)
        headers = {
            'x-rd-timestamp': timestamp,
            'x-rd-api-nonce': nonce,
            'x-rd-api-key': self.api_key
        }
        if self.auth_token:
            headers['AUTHORIZATION'] = 'Token {0}'.format(self.auth_token)
        return headers

    def login(self, username, password):
        m = hashlib.sha1()
        m.update(password.encode('utf-8'))
        hashed_password = m.hexdigest()
        endpoint = '/auth/login'
        data = {
            'username': username,
            'password': hashed_password
        }
        resp = self.post(endpoint, data)
        if resp.status_code == requests.codes.ok:
            self.auth_token = resp.json()['token']
            self.user_id = resp.json()['userId']
        return resp

    def get_nonce(self, timestamp, url, body=None):
        m = hmac.new(self.api_secret.encode(), digestmod=hashlib.sha1)
        m.update(str(timestamp).encode('utf-8'))
        m.update(url.encode('utf-8'))
        if body:
            sorted_body = self.sort_body(body)
            sorted_json = json.dumps(sorted_body, ensure_ascii=False).replace(' ', '')
            m.update(sorted_json.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def get_timestamp_milliseconds(dt=None):
        if not dt:
            dt = datetime.datetime.now()
        # grab time since epoch milliseconds
        return int(time.mktime(dt.timetuple()) * 1000 + dt.microsecond / 1000)

    def post(self, endpoint, body):
        headers = self.get_headers(endpoint, body=body)
        request_url = self.get_base_url() + endpoint
        return requests.post(request_url, json=body, headers=headers)

    def put(self, endpoint, body):
        headers = self.get_headers(endpoint, body=body)
        request_url = self.get_base_url() + endpoint
        return requests.put(request_url, json=body, headers=headers)

    def sort_body(self, data):
        """
        Where possible, sorts all dictionary and dictionary-like items by key. Reliably sorts
        root-level dictionaries, nested dictionaries, and stringified dictionaries. OrderedDict,
        list, and set types will not be sorted, but the objects they contain are subject to sorting.

        Some edge cases may produce unexpected sorting, including but not limited to:
            - Strings with JSON, list, or set formatted contents will be converted to dict format, with objects
                cast to their inferred types as per json.loads() best judgement
            - OrderedDicts keys won't be sorted, but OrderedDict[key] values will have a sort attempted
            - If contained in a dict, lists and sets will recursively sort each item. Items are not sorted
                within the list, but are sorted within themselves
                    Example: sort_body({"a": [{"c": 1, "b": 2}]}) == {"a": [{"b": 2. "c": 1}]}

        :param data: The payload to be sorted before nonce calculation
        :return: Sorted data
        """
        if isinstance(data, dict):
            sorted_result = OrderedDict()
            # Only sort by keys in dictionaries. Keys should be strings, and must all be the same object type.
            #   sorted() fails silently when comparing different types, such as a string and an integer.
            for key, value in sorted(data.items()):
                # everything will be in unicode unless we've converted it and went to the next level of depth
                if isinstance(value, str):
                    try:
                        # If we parse the JSON successfully, give the work to a further nested sort_body function
                        parsed_value = json.loads(value)
                        if isinstance(parsed_value, dict) or isinstance(parsed_value, list) or isinstance(parsed_value,
                                                                                                          set):
                            sorted_result[key] = self.sort_body(parsed_value)
                        else:  # we only want to use the parsed value if result is dict
                            sorted_result[key] = value
                    except ValueError:
                        sorted_result[key] = value
                elif isinstance(value, dict) or isinstance(value, OrderedDict):
                    sorted_result[key] = self.sort_body(value)
                elif isinstance(value, list) or isinstance(value, set):
                    sorted_result[key] = [self.sort_body(list_item) for list_item in value]
                else:
                    sorted_result[key] = value
            return sorted_result
        if isinstance(data, list) or isinstance(data, set):
            # Just in case the list contains dictionaries that need sorted
            return [self.sort_body(list_item) for list_item in data]
        # Anything that isn't a list or dict gets ignored
        return data
