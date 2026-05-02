"""
Copyright (c) 2025 Go2Market Insights Inc
All rights reserved.
https://g2m.ai

This software is given from https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/tutorial-1#optional-access-the-public-endpoint-programmatically. The functionality of the class is given by them.
It has been modified to accomodate the needs of our organization.
"""

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.backends import default_backend
from datetime import timedelta, timezone, datetime
import base64
import hashlib
import logging
import requests
import json
import jwt

logger = logging.getLogger(__name__)

class SnowflakeKeyPairAuth:
    """
    A class that handles Snowflake authentication using key pair authentication.
    This combines the functionality of generateJWT.py and access-via-keypair.py
    into a single, programmatically usable class.
    """
    
    # JWT constants
    ISSUER = "iss"
    EXPIRE_TIME = "exp"
    ISSUE_TIME = "iat"
    SUBJECT = "sub"
    
    # JWT generation settings
    JWT_LIFETIME = timedelta(minutes=59)  # The tokens will have a 59-minute lifetime
    JWT_RENEWAL_DELTA = timedelta(minutes=54)  # Tokens will be renewed after 54 minutes
    JWT_ALGORITHM = "RS256"  # Tokens will be generated using RSA with SHA256
    
    def __init__(self, account, user, private_key_file_path, 
                 endpoint=None, endpoint_path='/', role=None, 
                 snowflake_account_url=None, passphrase=None,
                 lifetime=JWT_LIFETIME, renewal_delay=JWT_RENEWAL_DELTA,
                 verbose=False):
        """
        Initialize the SnowflakeKeyPairAuth with the necessary parameters.
        
        Args:
            account (str): Your Snowflake account identifier.
            user (str): The Snowflake username.
            private_key_file_path (str): Path to the private key file used for signing the JWTs.
            endpoint (str, optional): The ingress endpoint of the service.
            endpoint_path (str, optional): The url path for the ingress endpoint of the service. Defaults to '/'.
            role (str, optional): The role to use for the session. If None, uses the default role.
            snowflake_account_url (str, optional): The full account URL. If None, constructed from account.
            passphrase (str, optional): Passphrase for encrypted private key. If None and needed, will prompt.
            lifetime (timedelta, optional): The lifetime of the JWT. Defaults to 59 minutes.
            renewal_delay (timedelta, optional): When to renew the JWT. Defaults to 54 minutes.
            verbose (bool, optional): Whether to log verbose information. Defaults to False.
        """
        self.account = account
        self.user = user
        self.private_key_file_path = private_key_file_path
        self.endpoint = endpoint
        self.endpoint_path = endpoint_path if endpoint_path.startswith("/") else f"/{endpoint_path}"
        self.role = role
        self.snowflake_account_url = snowflake_account_url
        self.passphrase = passphrase
        self.lifetime = lifetime
        self.renewal_delay = renewal_delay
        self.verbose = verbose
        
        # JWT token state
        self.jwt_token = None
        self.renew_time = datetime.now(timezone.utc)
        
        # Snowflake JWT token state
        self.snowflake_jwt = None
        
        # Load the private key
        self._load_private_key()
        
        if self.verbose:
            logger.info(f"Initialized SnowflakeKeyPairAuth for user {user} in account {account}")
    
    def _load_private_key(self):
        """Load the private key from the specified file."""
        with open(self.private_key_file_path, 'rb') as pem_in:
            pemlines = pem_in.read()
            try:
                # Try to access the private key without a passphrase.
                self.private_key = load_pem_private_key(pemlines, None, default_backend())
            except TypeError:
                # If that fails, provide the passphrase.
                if self.passphrase is None:
                    from getpass import getpass
                    self.passphrase = getpass('Passphrase for private key: ')
                self.private_key = load_pem_private_key(pemlines, self.passphrase.encode(), default_backend())
    
    def prepare_account_name_for_jwt(self, raw_account):
        """
        Prepare the account identifier for use in the JWT.
        For the JWT, the account identifier must not include the subdomain or any region or cloud provider information.
        
        Args:
            raw_account (str): The specified account identifier.
            
        Returns:
            str: The account identifier in a form that can be used to generate the JWT.
        """
        account = raw_account
        if not '.global' in account:
            # Handle the general case.
            idx = account.find('.')
            if idx > 0:
                account = account[0:idx]
        else:
            # Handle the replication case.
            idx = account.find('-')
            if idx > 0:
                account = account[0:idx]
        # Use uppercase for the account identifier.
        return account.upper()
    
    def calculate_public_key_fingerprint(self):
        """
        Calculate the public key fingerprint from the private key.
        
        Returns:
            str: The public key fingerprint.
        """
        # Get the raw bytes of public key.
        public_key_raw = self.private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)

        # Get the sha256 hash of the raw bytes.
        sha256hash = hashlib.sha256()
        sha256hash.update(public_key_raw)

        # Base64-encode the value and prepend the prefix 'SHA256:'.
        public_key_fp = 'SHA256:' + base64.b64encode(sha256hash.digest()).decode('utf-8')
        
        if self.verbose:
            logger.info(f"Public key fingerprint is {public_key_fp}")

        return public_key_fp
    
    def get_jwt_token(self):
        """
        Generate a JWT token for Snowflake authentication.
        
        Returns:
            str: The JWT token.
        """
        now = datetime.now(timezone.utc)  # Fetch the current time

        # If the token has expired or doesn't exist, regenerate the token.
        if self.jwt_token is None or self.renew_time <= now:
            if self.verbose:
                logger.info(f"Generating a new token because the present time ({now}) is later than the renewal time ({self.renew_time})")
            
            # Calculate the next time we need to renew the token.
            self.renew_time = now + self.renewal_delay

            # Prepare the account name for JWT
            account_for_jwt = self.prepare_account_name_for_jwt(self.account)
            
            # Construct the fully qualified username in uppercase.
            qualified_username = account_for_jwt + "." + self.user.upper()
            
            # Generate the public key fingerprint for the issuer in the payload.
            public_key_fp = self.calculate_public_key_fingerprint()

            # Create our payload
            payload = {
                # Set the issuer to the fully qualified username concatenated with the public key fingerprint.
                self.ISSUER: qualified_username + '.' + public_key_fp,

                # Set the subject to the fully qualified username.
                self.SUBJECT: qualified_username,

                # Set the issue time to now.
                self.ISSUE_TIME: now,

                # Set the expiration time, based on the lifetime specified for this object.
                self.EXPIRE_TIME: now + self.lifetime
            }

            # Generate the actual token
            token = jwt.encode(payload, key=self.private_key, algorithm=self.JWT_ALGORITHM)
            
            # If you are using a version of PyJWT prior to 2.0, jwt.encode returns a byte string instead of a string.
            # If the token is a byte string, convert it to a string.
            if isinstance(token, bytes):
                token = token.decode('utf-8')
                
            self.jwt_token = token
            
            if self.verbose:
                logger.info(f"Generated a JWT with the following payload: {jwt.decode(self.jwt_token, key=self.private_key.public_key(), algorithms=[self.JWT_ALGORITHM])}")

        return self.jwt_token
    
    def exchange_token(self):
        """
        Exchange the JWT token for a Snowflake JWT token.
        
        Returns:
            str: The Snowflake JWT token.
        """
        # Get the JWT token
        token = self.get_jwt_token()
        
        # Prepare the scope
        scope_role = f'session:role:{self.role}' if self.role is not None else None
        scope = f'{scope_role} {self.endpoint}' if scope_role is not None else self.endpoint
        
        # Prepare the data for the token exchange
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'scope': scope,
            'assertion': token,
        }
        
        if self.verbose:
            logger.info(f"Token exchange data: {data}")
        
        # Determine the URL for the token exchange
        if self.snowflake_account_url:
            url = f'{self.snowflake_account_url}/oauth/token'
        else:
            url = f'https://{self.account}.snowflakecomputing.com/oauth/token'
        
        if self.verbose:
            logger.info(f"OAuth URL: {url}")
        
        # Make the request
        response = requests.post(url, data=data)
        
        if response.status_code != 200:
            raise Exception(f"Failed to exchange token: {response.status_code} - {response.text}")
        
        self.snowflake_jwt = response.text
        
        if self.verbose:
            logger.info(f"Snowflake JWT: {self.snowflake_jwt}")
        
        return self.snowflake_jwt
    
    def connect_to_spcs(self):
        """
        Connect to the Snowflake SPCS service using the Snowflake JWT token.
        
        Returns:
            dict: The response from the SPCS service.
        """
        # Get the Snowflake JWT token if we don't have one
        if self.snowflake_jwt is None:
            self.exchange_token()
        
        # Create the URL for the SPCS service
        spcs_url = f'https://{self.endpoint}{self.endpoint_path}'
        
        # Create the headers with the Snowflake JWT token
        headers = {'Authorization': f'Snowflake Token="{self.snowflake_jwt}"'}
        
        if self.verbose:
            logger.info(f"SPCS URL: {spcs_url}")
            logger.info(f"Headers: {headers}")
        
        # Make the request
        response = requests.post(spcs_url, headers=headers)
        
        if self.verbose:
            logger.info(f"SPCS response status: {response.status_code}")
            logger.info(f"SPCS response: {response.text}")
        
        # Try to parse the response as JSON
        try:
            return {
                'status_code': response.status_code,
                'response': response.json()
            }
        except json.JSONDecodeError:
            return {
                'status_code': response.status_code,
                'response': response.text
            }
    
    def authenticate(self):
        """
        Perform the full authentication flow: generate JWT, exchange for Snowflake JWT, and connect to SPCS.
        
        Returns:
            dict: The response from the SPCS service.
        """
        self.get_jwt_token()
        self.exchange_token()
        return self.connect_to_spcs()
