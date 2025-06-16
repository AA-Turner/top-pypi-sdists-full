import requests
from requests.auth import HTTPBasicAuth

class ApiRequest:
    """request class for web api"""

    def __init__(self, config):
        self.config = config
        self.url = self.config.url

        if hasattr(self.config, 'auth_type') and self.config.auth_type == 'none':
            self.auth_headers = {}
        elif hasattr(self.config, 'auth_type') and self.config.auth_type == 'auth':
            self.auth = HTTPBasicAuth(self.config.user, self.config.token)
        else:
            self.auth_headers = {'Authorization': "Bearer {}".format(self.config.token), }

    def request(self, location, params=None, headers=None, method='GET', files=None):
        if headers is None and hasattr(self, 'auth_headers'):
            headers = self.auth_headers

        url = f'{self.url}{location}'
        r = requests.request(method=method, url=url, params=params, headers=headers, auth=self.auth, files=files)
        return r.text

    def get(self, location, params=None, headers=None):
        """ get request to bitbucket api
        :param location: url location path
        :param params: request query params
        :param headers: http headers
        :return: text of response
        """
        if headers is None:
            headers = self.auth_headers
        url = f'{self.url}{location}'
        r = requests.get(url=url, params=params, headers=headers)
        return r.text

    def post(self, location, headers=None, data=None, json=None, files=None):
        """
        :param location: location: url location path
        :param headers:  http headers
        :param data: request data
        :param json: json in request body
        :param files: dictionary with opened files
        :return: response
        """
        if headers is None:
            headers = self.auth_headers
        url = f'{self.url}{location}'
        r = requests.post(url, headers=headers, data=data, json=json, files=files)
        return r

    def put(self, location, headers=None, data=None, json=None):
        """
        :param location: url location path
        :param headers: http headers
        :param data: request data
        :param json: json in request body
        :return: response
        """
        url = f'{self.url}{location}'
        r = requests.post(url, headers=headers, data=data, json=json)
        return r

    def delete(self, location, headers=None):
        """
        :param location:  url location path
        :param headers: http headers
        :return: status code
        """
        url = f'{self.url}{location}'
        if headers is None:
            headers = self.auth_headers
        r = requests.delete(url, headers=headers)
        return r.status_code
