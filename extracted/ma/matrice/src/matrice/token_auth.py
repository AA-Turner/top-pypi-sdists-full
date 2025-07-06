"""Module for custom authentication"""

import json
import os
import sys
from datetime import datetime, timezone
import requests
from dateutil.parser import parse
from requests.auth import AuthBase


class RefreshToken(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, access_key, secret_key):
        self.bearer_token = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.VALIDATE_ACCESS_KEY_URL = (
            f"https://{os.environ.get('ENV', 'prod')}.backend.app.matrice.ai/v1/user/validate_access_key"
        )

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        self.set_bearer_token()
        r.headers["Authorization"] = self.bearer_token
        return r

    def set_bearer_token(self):
        """Obtain a bearer token using the provided access key and secret key."""
        payload_dict = {
            "accessKey": self.access_key,
            "secretKey": self.secret_key,
        }
        payload = json.dumps(payload_dict)
        headers = {"Content-Type": "text/plain"}
        try:
            response = requests.request(
                "GET",
                self.VALIDATE_ACCESS_KEY_URL,
                headers=headers,
                data=payload,
                timeout=20,
            )
        except Exception as e:
            print("Error while making request to the auth server")
            print(e)
            sys.exit(0)
        if response.status_code != 200:
            print("Error response from the auth server")
            print(response.text)
            sys.exit(0)
        res_dict = response.json()
        if res_dict["success"]:
            self.bearer_token = "Bearer " + res_dict["data"]["refreshToken"]
        else:
            print("The provided credentials are incorrect!!")
            sys.exit(0)


class AuthToken(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(
        self,
        access_key,
        secret_key,
        refresh_token,
    ):
        self.bearer_token = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.refresh_token = refresh_token
        self.expiry_time = datetime.now(timezone.utc)
        self.REFRESH_TOKEN_URL = (
            f"https://{os.environ.get('ENV', 'prod')}.backend.app.matrice.ai/v1/user/refresh"
        )

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        self.set_bearer_token()
        r.headers["Authorization"] = self.bearer_token
        return r

    def set_bearer_token(self):
        """Obtain an authentication bearer token using the provided refresh token."""
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.request(
                "POST",
                self.REFRESH_TOKEN_URL,
                headers=headers,
                auth=self.refresh_token,
                timeout=20,
            )
        except Exception as e:
            print("Error while making request to the auth server")
            print(e)
            sys.exit(0)
        if response.status_code != 200:
            print("Error response from the auth server")
            print(response.text)
            sys.exit(0)
        res_dict = response.json()
        if res_dict["success"]:
            self.bearer_token = "Bearer " + res_dict["data"]["token"]
            self.expiry_time = parse(res_dict["data"]["expiresAt"])
        else:
            print("The provided credentials are incorrect!!")
            sys.exit(0)
