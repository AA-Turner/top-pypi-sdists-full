import asyncio
import logging
import threading
from datetime import datetime
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class S2SClient:
    """
    A general-purpose Service-to-Service (S2S) connector for obtaining bearer tokens
    for authentication in service-to-service communication.
    """

    def __init__(
        self,
        auth_url,
        username,
        password,
        tenant: str = "shops",
        scope: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        s2s_token_key: str = "id_token",
        s2s_expires_in: str = "expires_in",
    ):
        """
        Initializes the S2SClient with the necessary authentication parameters.

        Args:
            auth_url (str): The base URL of the authentication server.
            tenant (str): The tenant identifier.
            client_id (str): The client identifier (service name).
            client_secret (str): The client secret (API key).
            s2s_token_key (str): The S2S token key which will be used from S2S response
            s2s_expires_in (str): The S2S token expires in.
        """
        self.auth_url = auth_url
        self.tenant = tenant
        self.username = username
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = httpx.AsyncClient()
        self.s2s_token = None
        self.token_expires = -1
        self.s2s_token_key = s2s_token_key
        self.s2s_expires_in = s2s_expires_in
        self.raw_token_response = None

    async def _refresh_access_token(self):
        """
        Refreshes the access token by making a POST request to the authentication server.
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Define the data payload
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": self.scope,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = await self.session.post(
            self.auth_url + "/oauth/v2/token", headers=headers, data=data
        )
        if response.status_code == 200:
            logger.debug("Token was fetched")
            self.raw_token_response = response.json()
            self.s2s_token = self.raw_token_response[self.s2s_token_key]
            self.token_expires = (
                datetime.now().timestamp() + self.raw_token_response[self.s2s_expires_in]
            )
        else:
            raise Exception(f"Failed to get access token: {response.text}")

    async def get_token(self):
        """
        Returns a valid access token, refreshing it if necessary.

        Returns:
            str: The access token.
        """
        if datetime.now().timestamp() >= self.token_expires or not self.s2s_token:
            await self._refresh_access_token()
        return self.s2s_token


class HttpxS2SAuth(httpx.Auth):
    def __init__(self, connector: S2SClient, s2s_token_header: str = "X-Service-Token"):
        self.connector = connector
        self._sync_lock = threading.RLock()
        self._async_lock = asyncio.Lock()
        self.s2s_token_header = s2s_token_header

    def sync_get_token(self):
        raise RuntimeError("Cannot use a async authentication class with httpx.AsyncClient")

    def sync_auth_flow(self, request):
        raise RuntimeError("Cannot use a async authentication class with httpx.AsyncClient")

    async def async_get_token(self):
        async with self._async_lock:
            return await self.connector.get_token()

    async def async_auth_flow(self, request):
        token = await self.async_get_token()
        request.headers[self.s2s_token_header] = f"Bearer {token}"
        yield request
