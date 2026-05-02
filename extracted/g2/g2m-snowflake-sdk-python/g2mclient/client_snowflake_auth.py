"""
Copyright (c) 2025 Go2Market Insights Inc
All rights reserved.
https://g2m.ai

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import json
import requests
from datetime import datetime, timedelta
from .snowflake_keypair_auth import SnowflakeKeyPairAuth

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("ApiClient")

class SnowflakeAuthClient:
    """
    SnowflakeAuthClient manages authentication with Snowflake using key pair authentication.
    """

    def __init__(self, host=None, verbose=False):
        """
        Initialize the SnowflakeAuthClient.
        
        Args:
            host (str, optional): The host URL for API calls.
            verbose (bool, optional): Whether to log verbose information.
        """
        if verbose:
            log.info("Starting: Init Snowflake Client")
        self.host = host.rstrip("/") if host else None
        self._token = {"token": ""}
        self._token_time = None
        self.verbose = verbose
        self._keypair_auth = None

    ###########################################################################
    #                          Basic API calls                                #
    ###########################################################################

    def _get(self, uri, params=None):
        """
        Protected GET request with authentication.
        
        Args:
            uri (str): The URI to send the GET request to.
            params (dict, optional): Query parameters to include in the request.
            
        Returns:
            dict: A standardized response format with status and response data.
        """
        if self.verbose:
            log.info(f"[GET] {uri}")
        r = requests.get(uri, headers=self._headers(), params=params)
        return self._response(r)

    def _post(self, uri, json_obj=None, compressed=False):
        """
        Protected POST request with authentication.
        
        Args:
            uri (str): The URI to send the POST request to.
            json_obj (dict, optional): JSON data to include in the request body.
            
        Returns:
            dict: A standardized response format with status and response data.
        """
        if self.verbose:
            log.info(f"[POST] {uri}")
        data = json.dumps(json_obj)   
        r = requests.post(uri, json=data, headers=self._headers())
        return self._response(r)

    def _response(self, r):
        """
        Standardized response format.
        
        Args:
            r (Response): The response object from requests.
            
        Returns:
            dict: A standardized response format with status and response data.
        """
        res = {
            'status': r.status_code,
            'response': None
        }
        if 200 <= r.status_code < 300:
            # Attempt to parse JSON
            try:
                res['response'] = r.json()
            except json.JSONDecodeError:
                res['response'] = r.text
        else:
            log.error(f"WARNING! Request returned status code: {r.status_code}")
        return res

    def _headers(self):
        """
        Return headers with Snowflake Token in the Authorization header.
        
        Returns:
            dict: Headers for API requests.
        """
        if self._token and self._token.get("token"):
            return {
                "Authorization": f'Snowflake Token="{self._token["token"]}"'
            }
        return {}

    ###########################################################################
    #                       Authentication methods                            #
    ###########################################################################

    def _login(self, user, account, endpoint, endpoint_path, role, snowflake_account_url, lifetime=59, renewal_delay=54, private_key_file_path=None):
        """
        Authenticate using Snowflake key pair authentication.
        
        Args:
            user (str): Snowflake username.
            account (str): Snowflake account identifier.
            endpoint (str): The ingress endpoint of the service.
            endpoint_path (str): The URL path for the ingress endpoint.
            role (str, optional): Snowflake role to use.
            snowflake_account_url (str, optional): Full Snowflake account URL.
            lifetime (int, optional): Token lifetime in minutes.
            renewal_delay (int, optional): Token renewal delay in minutes.
            private_key_file_path (str): Path to the private key file.
            
        Returns:
            int: HTTP status code (200 for success, other for failure).
        """
        if self.verbose:
            log.info("Starting: _login with Snowflake key pair authentication")
        
        try:
            # Create keypair auth
            self._keypair_auth = SnowflakeKeyPairAuth(
                account=account,
                user=user,
                private_key_file_path=private_key_file_path,
                endpoint=endpoint,
                endpoint_path=endpoint_path,
                role=role,
                snowflake_account_url=snowflake_account_url,
                lifetime=timedelta(minutes=lifetime),
                renewal_delay=timedelta(minutes=renewal_delay),
                verbose=self.verbose
            )
            
            snowflake_jwt = self._keypair_auth.exchange_token()
            
            # Save the token
            self._token = {"token": snowflake_jwt}
            self._token_time = datetime.now()
            
            if self.verbose:
                partial_token = (self._token['token'] or '')[:10] + '...'
                log.info(f"[LOGIN] Acquired Snowflake token via keypair auth: {partial_token}")
            
            return 200
        except Exception as e:
            log.error(f"[LOGIN] Keypair authentication failed: {str(e)}")
            return 400

    def _logout(self):
        """
        Log out by clearing the token.
        
        Returns:
            dict: Status of the logout operation.
        """
        if self.verbose:
            log.info("Starting logout...")
        
        self.clean_token()
        
        return {"status": 200, "response": "Logged out successfully"}

    ###########################################################################
    #                          Token-related methods                          #
    ###########################################################################

    @property
    def is_token(self):
        """
        Check if a token exists.
        
        Returns:
            bool: True if a token exists, False otherwise.
        """
        return bool(self._token.get('token'))

    def clean_token(self):
        """
        Clear the token.
        """
        self._token = {"token": ""}
        self._token_time = None
        self._keypair_auth = None
        
    def _save_token(self, token_dict):
        """
        Save the new token, track the acquisition time.
        We'll assume the server's response is {"token": "<snowflake_token>"}.
        """
        self._token['token'] = token_dict.get('token', '')
        self._token_time = datetime.now()
