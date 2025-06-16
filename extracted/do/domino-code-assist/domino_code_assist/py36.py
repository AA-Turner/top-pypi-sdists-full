import os
from typing import List

import requests
from requests.auth import AuthBase, HTTPBasicAuth

from domino_code_assist.domino_api import AppInfo, IDominoApi
from domino_code_assist.settings import settings

DOMINO_TOKEN_FILE_KEY_NAME = "DOMINO_TOKEN_FILE"
DOMINO_USER_API_KEY_KEY_NAME = "DOMINO_USER_API_KEY"
host = settings.domino_alternative_api_host or settings.domino_api_host


class BearerAuth(AuthBase):
    """
    Class for authenticating requests by user supplied token.
    """

    def __init__(self, auth_token=None, domino_token_file=None):
        self.auth_token = auth_token
        self.domino_token_file = domino_token_file

    def _from_token_file(self):
        with open(self.domino_token_file, "r") as token_file:
            return token_file.readline().rstrip()

    def __call__(self, r):
        """
        Override the default __call__ method for the AuthBase base class

        More more info, see:
        https://docs.python-requests.org/en/master/user/advanced/
        """
        auth_token = self._from_token_file() if self.domino_token_file else self.auth_token
        r.headers["Authorization"] = "Bearer " + auth_token
        return r


def get_auth_by_type(api_key=None, auth_token=None, domino_token_file=None):
    """
    Return appropriate authentication object for requests.

    If no authentication credential is provided, the call fails with an AssertError

    Precedence in the case of multiple credentials is:
        1. auth_token string
        2. domino_token_file
        3. api_key
        4. domino_token_file_from_env
        5. api_key_from_env
    """

    if auth_token is not None:
        return BearerAuth(auth_token=auth_token)
    elif domino_token_file is not None:
        return BearerAuth(domino_token_file=domino_token_file)
    elif api_key is not None:
        return HTTPBasicAuth("", api_key)
    else:
        # In the case that no authentication type was passed when this method
        # called, fall back to deriving the auth info from the environment.
        api_key_from_env = os.getenv(DOMINO_USER_API_KEY_KEY_NAME)
        domino_token_file_from_env = os.getenv(DOMINO_TOKEN_FILE_KEY_NAME)
        if api_key_from_env or domino_token_file_from_env:
            return get_auth_by_type(api_key=api_key_from_env, domino_token_file=domino_token_file_from_env)
        else:
            # All attempts failed -- nothing to do but raise an error.
            raise RuntimeError("Unable to authenticate: no authentication provided")


def get(url, **kwargs):
    return requests.Session().get(url, auth=get_auth_by_type(), **kwargs)


def post(url, data, json, **kwargs):
    return requests.Session().post(url, auth=get_auth_by_type(), data=data, json=json, **kwargs)


class Py36DominoApi(IDominoApi):
    def get_datasource_list(self):
        return []

    def get_datasource_names(self):
        return []

    def sync(self, commit_message: str):
        pass

    def get_app_status(self):
        return None

    def app_publish(self, hardwareTierId):
        pass

    def app_unpublish(self):
        pass

    def get_app_id(self):
        pass

    def get_user_info(self):
        return get(f"{host}/v4/users/self").json()

    def get_domino_version(self) -> str:
        return get(f"{host}/version").json().get("version")

    def sync_files(self, commit_message: str):
        return {}

    def get_useable_environments(self):
        return []

    def get_current_environment_id(self):
        return "not-supported"

    def get_app_info(self) -> List[AppInfo]:
        return []
