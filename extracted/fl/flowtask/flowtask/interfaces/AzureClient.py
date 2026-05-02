import msal
from msal.authority import AuthorityBuilder, AZURE_PUBLIC
from navconfig.logging import logging
from .client import ClientInterface
from ..conf import (
    AZURE_ADFS_CLIENT_ID,
    AZURE_ADFS_CLIENT_SECRET,
    AZURE_ADFS_TENANT_ID,
    AZURE_ADFS_DOMAIN,
)
from ..exceptions import ComponentError


logging.getLogger("msal").setLevel(logging.INFO)
DEFAULT_SCOPES = ["https://graph.microsoft.com/.default"]
API_VERSION = "v1.0"


def generate_auth_string(user, token):
    return f"user={user}\x01Auth=Bearer {token}\x01\x01"


class AzureClient(ClientInterface):
    """
    AzureClient

    Overview

        The `AzureClient` class handles authentication and authorization for Azure Active Directory using the Microsoft
        Authentication Library (MSAL). This class provides methods to acquire tokens for secure API requests, particularly
        for the Microsoft Graph API. It supports both confidential client applications and user authentication.

    .. table:: Properties
    :widths: auto

        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | Name             | Required | Description                                                                                      |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | tenant_id        |   Yes    | The Azure AD tenant ID. Defaults to AZURE_ADFS_TENANT_ID from the configuration.                |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | client_id        |   Yes    | The client ID of the Azure AD application. Defaults to AZURE_ADFS_CLIENT_ID from the config.    |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | client_secret    |   Yes    | The client secret of the Azure AD application. Defaults to AZURE_ADFS_CLIENT_SECRET.            |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | scopes           |   No     | A list of scopes for the token request. Defaults to Microsoft Graph API scopes.                 |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | authority        |   Yes    | The authority URL for Azure AD authentication. Defaults to Azure AD instance authority.         |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+
        | credentials      |   Yes    | A dictionary containing the credentials for Azure AD authentication.                            |
        +------------------+----------+-----------+--------------------------------------------------------------------------------------+

    Return

        The methods in this class handle the acquisition of access tokens and the configuration of MSAL clients for
        interacting with Azure services. The tokens acquired can be used for authenticating API requests to services
        like Microsoft Graph.

    """  # noqa
    _credentials: dict = {"tenant_id": str, "client_id": str, "client_secret": str}

    def __init__(
        self,
        tenant_id: str = None,
        client_id: str = None,
        client_secret: str = None,
        scopes: list = None,
        **kwargs,
    ) -> None:
        self.tenant_id = tenant_id if tenant_id else AZURE_ADFS_TENANT_ID
        # credentials:
        self.client_id = client_id if client_id else AZURE_ADFS_CLIENT_ID
        self.client_secret = client_secret if client_secret else AZURE_ADFS_CLIENT_SECRET
        self._authority = AuthorityBuilder(AZURE_PUBLIC, AZURE_ADFS_DOMAIN)
        kwargs['no_host'] = True
        kwargs['credentials'] = kwargs.get(
            "credentials", {
                "client_id": self.client_id,
                "tenant_id": self.tenant_id,
                "client_secret": self.client_secret,
            }
        )
        super(AzureClient, self).__init__(
            **kwargs
        )
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self._resource = kwargs.get("resource", "https://graph.microsoft.com")
        self.userinfo_uri = "https://graph.microsoft.com/v1.0/me"
        self.issuer = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.token_uri = (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        )
        self.users_info = f"{self._resource}/{API_VERSION}/users"
        # scopes:
        self.scopes = scopes if scopes is not None else DEFAULT_SCOPES

    def binary_token(self, username: str = None, password: str = None) -> str:
        result = self.get_token(username=username, password=password)
        return generate_auth_string(username, result["access_token"])

    def get_msal_app(self):
        authority = self.authority if self.authority else self._authority
        return msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret,
            validate_authority=True,
        )

    def get_msal_client(self):
        authority = self.authority if self.authority else self._authority
        return msal.ClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret,
            validate_authority=True,
        )

    def get_token(self) -> str:
        if not self.app:
            self.app = self.get_msal_app()
        # Acquire token
        result = self.app.acquire_token_silent(self.scopes, account=None)
        if not result:
            result = self.app.acquire_token_for_client(scopes=self.scopes)
        if "access_token" in result:
            token_type = result.get("token_type")
            token = result.get("access_token")
            return token, token_type
        else:
            print(
                "Could not acquire token:",
                result.get("error"),
                result.get("error_description"),
            )
            raise ComponentError(
                "Could not acquire token: {0}".format(result.get("error_description"))
            )
