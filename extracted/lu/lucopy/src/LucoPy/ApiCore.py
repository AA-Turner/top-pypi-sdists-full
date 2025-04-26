import requests
from datetime import datetime, timedelta
import logging
from .exceptions import ApiException, AuthException

logger = logging.getLogger(__name__)

class ApiCore:

    def __init__(self, config, timeout, identity):

        # Load service principle credentials from config dict
        self.credentials = config

        if config['tenant_id'] and config['client_id'] and config['client_secret'] and config['resource_id']:
            self.identity = ServicePrinciple(config)
        else:
            self.identity = identity

        self.token_expiry = datetime.now() + timedelta(minutes=-5)
        self.timeout = timeout

    def check_auth(self, buffer=30):
        """
        Check that token exists and has not expired. Buffer enforces a minimum time
        before expiry.
        """            
        if datetime.now() > (self.token_expiry + timedelta(seconds=-buffer)):
            logger.debug('No valid token')
            
            # Call the generate_token method from whichever identity object
            # has been provided
            try:
                token, expiry = self.identity.generate_token()
            except:
                raise AuthException('Failed to generate bearer token. Please check authentication credentials.')

            logger.debug(f'New token generated')

            self.auth_header = {'Authorization': f'Bearer {token}'}

            # set expiry datetime
            self.token_expiry = expiry
        else:
            logger.debug('Valid token')

    def __check_error(self, response, allow_status):
        
        if allow_status:
            allow_status = [int(allow_status)] if isinstance(allow_status, (str, int)) else allow_status
        else:
            allow_status = []

        if not response.ok and response.status_code not in allow_status:
            try:
                api_msg = f'{response.status_code} :: {response.text}'
                logger.error(api_msg)
                raise ApiException(api_msg)
            except ApiException as e:
                raise e
            except:
                response.raise_for_status()
        
    def get_request(self, endpoint, params=None, allow_status=None):
        self.check_auth()
        headers = self.auth_header
        url = f'{self.credentials["base_url"]}{endpoint}'
        response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
        self.__check_error(response, allow_status)
        return response

    def post_request(self, endpoint, additionalHeaders={}, data=None, params=None, json=None, allow_status=None):
        self.check_auth()
        headers = dict(**self.auth_header, **additionalHeaders)
        url = f'{self.credentials["base_url"]}{endpoint}'
        response = requests.post(url, headers=headers, data=data, params=params, json=json, timeout=self.timeout)
        self.__check_error(response, allow_status)
        return response

    # def delete_request(self, endpoint, data=None, params=None):
    #     self.check_auth()
    #     headers = self.auth_header
    #     url = f'{self.credentials["base_url"]}{endpoint}'
    #     response = requests.delete(url, headers=headers, data=data, params=params, timeout=self.timeout)
    #     return response

    # def put_request(self, endpoint, additionalHeaders={}, data=None, params=None, allow_status=None):
    #     self.check_auth()
    #     headers = dict(**self.auth_header, **additionalHeaders)
    #     url = f'{self.credentials["base_url"]}{endpoint}'
    #     response = requests.put(url, headers=headers, data=data, params=params, timeout=self.timeout)
    #     self.__check_error(response, allow_status)
    #     return response

class ServicePrinciple:

    def __init__(self, config):
        self.credentials = config

    def generate_token(self):
        """
        Called when token doesn't exist or has expired. Sends a request to produce a new 
        access token based on the client credentials.
        """
        # Construct new token request parameters
        auth_url = f'https://login.microsoftonline.com/{self.credentials["tenant_id"]}/oauth2/v2.0/token'
        scope = f'{self.credentials["resource_id"]}/.default'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = f'grant_type=client_credentials&scope={scope}'

        # Send request for new token
        r = requests.post(auth_url, data=payload, headers=headers, 
                          auth=(self.credentials["client_id"], self.credentials["client_secret"]))
        r.raise_for_status()

        # Extract token from request, set expiry and generate header
        expiry = datetime.now() + timedelta(seconds=r.json()['expires_in'])

        return r.json()['access_token'], expiry
