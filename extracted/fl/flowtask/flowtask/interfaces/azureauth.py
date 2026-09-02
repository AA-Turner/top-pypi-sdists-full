import msal
from navconfig.logging import logging
from ..conf import (
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_SECRET_ID,
)
"""
    AzureAuth Class

        Overview

        This class facilitates Azure Active Directory (AAD) authentication using the Microsoft Authentication Library (MSAL) for Python. It retrieves access tokens for a user or a client application based on provided credentials or cached tokens.

        .. table:: Properties
        :widths: auto

    +------------------------+----------+-----------+---------------------------------------------------------------------------------+
    | Name                   | Required | Summary                                                                                     |
    +------------------------+----------+-----------+---------------------------------------------------------------------------------+
    |  tenant_id (optional)  |   No     | Azure tenant ID (defaults to value from settings.settings.AZURE_TENANT_ID).                 |
    +------------------------+----------+-----------+---------------------------------------------------------------------------------+
    |  client_id (optional)  |   No     | Azure client application ID (defaults to value from settings.settings.AZURE_CLIENT_ID).     |
    +------------------------+----------+-----------+---------------------------------------------------------------------------------+
    |  client_secret         |   No     | Azure client application secret (defaults to value from settings.settings.AZURE_SECRET_ID). |
    +------------------------+----------+-----------+---------------------------------------------------------------------------------+
    |  scopes (optional)     |   No     | List of OAuth 2.0 scopes to request during token acquisition                                |
    |                        |          | (defaults to a list including "offline_access", "https://outlook.office365.com/.default",   |
    |                        |          | "email", "openid", and "profile").                                                          |
    +------------------------+----------+-----------+---------------------------------------------------------------------------------+

        Methods:
            * get_msal_client(client: bool = True): Returns an MSAL ClientApplication or ConfidentialClientApplication instance based on the client argument.
            * get_token(username: str = None, password: str = None) -> str: Acquires an access token using username/password or from cache if available. Raises an exception on failure.
            * binary_token(username: str = None, password: str = None) -> str: Retrieves an access token and constructs a binary auth string with user and token information.

        This class is likely used within other components or scripts to authenticate with Azure services.

"""  # noqa

DEFAULT_SCOPES = [
    "offline_access https://outlook.office365.com/.default email openid profile"
]

msal_logger = logging.getLogger("msal")
msal_logger.setLevel(logging.WARNING)


def generate_auth_string(user, token):
    return f"user={user}\x01Auth=Bearer {token}\x01\x01"


class AzureAuth:
    def get_msal_client(self, client: bool = True):
        if client is True:
            return msal.ClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret,
                validate_authority=True,
            )
        else:
            return msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret,
                validate_authority=True,
            )

    def __init__(
        self,
        tenant_id: str = None,
        client_id: str = None,
        client_secret: str = None,
        scopes: list = None,
    ) -> None:
        self.tenant_id = tenant_id if tenant_id else AZURE_TENANT_ID
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        # credentials:
        self.client_id = client_id if client_id else AZURE_CLIENT_ID
        self.client_secret = client_secret if client_secret else AZURE_SECRET_ID
        # Token URL
        self.token_uri = (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        )
        # scopes:
        self.scopes = scopes if scopes is not None else DEFAULT_SCOPES

    def get_token(self, username: str = None, password: str = None) -> str:
        result = None
        if username is not None:
            app = self.get_msal_client(client=True)
            account = app.get_accounts(username=username)
            if account:
                logging.info("Account(s) exists in cache, probably with token too")
                result = app.acquire_token_silent(self.scopes, account=account[0])
            else:
                result = app.acquire_token_by_username_password(
                    username, password, self.scopes
                )
        else:
            app = self.get_msal_client(client=False)
            result = app.acquire_token_silent(self.scopes, account=None)
            if not result:
                logging.info("No suitable token in cache.  Get new one.")
                result = app.acquire_token_for_client(scopes=self.scopes)
        if "access_token" in result:
            return result
        else:
            error = {
                "error": result.get("error"),
                "message": result.get("error_description"),
                "correlation_id": result.get("correlation_id"),
            }
            raise Exception(f"Unable to Access: {error!s}")

    def binary_token(self, username: str = None, password: str = None) -> str:
        result = self.get_token(username=username, password=password)
        return generate_auth_string(username, result["access_token"])
