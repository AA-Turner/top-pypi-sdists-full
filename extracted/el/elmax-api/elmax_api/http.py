"""
This module handles HTTP api calls to the Elmax WEB endpoint, implemented by the `Elmax` class
"""

import asyncio
import datetime
import functools
import logging
import ssl
import time
from enum import Enum
from socket import socket
from typing import Dict, List, Optional, Union
from abc import ABC, abstractmethod
import httpx
import jwt
from yarl import URL
from packaging import version

from elmax_api.constants import BASE_URL, ENDPOINT_LOGIN, USER_AGENT, ENDPOINT_DEVICES, ENDPOINT_DISCOVERY, \
    ENDPOINT_REFRESH, ENDPOINT_STATUS_ENTITY_ID, DEFAULT_HTTP_TIMEOUT, BUSY_WAIT_INTERVAL, ENDPOINT_LOCAL_CMD, \
    DEFAULT_PANEL_PIN, VERSION_REFRESH_SUPPORT
from elmax_api.exceptions import ElmaxBadLoginError, ElmaxApiError, ElmaxNetworkError, ElmaxBadPinError, \
    ElmaxPanelBusyError
from elmax_api.model.command import Command
from elmax_api.model.panel import PanelEntry, PanelStatus, EndpointStatus

_LOGGER = logging.getLogger(__name__)
_JWT_ALGS = ["HS256"]


async def helper(f, *args, **kwargs):
    if asyncio.iscoroutinefunction(f):
        return await f(*args, **kwargs)
    else:
        return f(*args, **kwargs)


_MIN_VERSION_REFRESH_SUPPORT = version.parse(VERSION_REFRESH_SUPPORT)

def async_auth(func, *method_args, **method_kwargs):
    """
    Asynchronous decorator used to check validity of JWT token.
    It takes care to verify the validity of a JWT token before issuing the method call.
    In case the JWT is expired, or close to expiration date, it tries to renew it.
    """

    @functools.wraps(func, *method_args, **method_kwargs)
    async def wrapper(*args, **kwargs):
        # Check whether the client has a valid token to be used. We consider valid tokens with expiration time
        # > 10minutes. If not, try to login first and then proceed with the function call.
        now = time.time()
        _instance = args[0]
        assert isinstance(_instance, GenericElmax)
        exp_time = _instance.token_expiration_time
        if exp_time == 0:
            _LOGGER.debug("The API client was not authorized yet. Login will be attempted.")
            await _instance.login()
        elif exp_time < 0:
            _LOGGER.debug("The API client token is expired. Login will be attempted.")
            await _instance.login()
        elif (exp_time - now) < 60:
            _LOGGER.debug(
                "The API client token is going to be expired soon. "
                "Login will be attempted right now to refresh it."
            )
            await _instance.renew_token()
        # At this point, we assume the client has a valid token to use for authorized APIs. So let's use it.
        result = await helper(func, *args, **kwargs)
        return result

    return wrapper


class GenericElmax(ABC):
    """
    Abstract Elmax HTTP client.
    This class takes care of handling API calls against the ELMAX API cloud endpoint.
    It handles data marshalling/unmarshalling, login and token renewal upon expiration.
    """

    def __init__(self, base_url: str = BASE_URL, current_panel_id: str = None,
                 current_panel_pin: str = DEFAULT_PANEL_PIN,
                 timeout: float = DEFAULT_HTTP_TIMEOUT, ssl_context: Optional[ssl.SSLContext] = None):
        """Base constructor.

        Args:
            base_url: API server base-URL
            current_panel_id: Panel id of the preferred panel
            current_panel_pin: Panel PIN of the preferred panel
            timeout: The default timeout, in seconds, to set up for the inner HTTP client
            ssl_contex: an SSL context to override the default one
        """
        self._raw_jwt = None
        self._jwt = None
        self._areas = self._outputs = self._zones = []
        self._current_panel_id = current_panel_id
        self._current_panel_pin = current_panel_pin
        self._base_url = URL(base_url)
        # Build the SSL context we trust
        sslcontext = ssl_context if ssl_context is not None else True
        self._ssl_context = sslcontext
        self._http_client = httpx.AsyncClient(timeout=timeout, verify=sslcontext)

    @classmethod
    async def retrieve_server_certificate(cls, hostname: str, port: int):
        try:
            pem_server_certificate = ssl.get_server_certificate((hostname, port))
            return pem_server_certificate
        except (socket.gaierror, ConnectionRefusedError) as ex:
            raise ElmaxNetworkError from ex

    def set_default_timeout(self, timeout: float):
        """Sets the default timeout (in seconds) for the HTTP client"""
        self._http_client.timeout = timeout

    async def _request(
            self,
            method: "Elmax.HttpMethod",
            url: str,
            data: Optional[Dict] = None,
            authorized: bool = False,
            timeout: float = DEFAULT_HTTP_TIMEOUT,
            retry_attempts: int = 3
    ) -> Dict:
        """
        Executes an HTTP API request against a given endpoint, parses the output and returns the
        json to the caller. It handles most basic IO exceptions.
        If the API returns a non 200 response, this method raises an `ElmaxApiError`

        Args:
            method: HTTP method to use for the HTTP request
            url: Target request URL
            data: Json data/Data to post in POST messages. Ignored when issuing GET requests
            authorized: When set, the request is performed passing the stored authorization token
            timeout: timeout in seconds for a single attempt
            retry_attempts: number of retry attempts in case of 422 (panel busy)

        Returns:
            Dict: The dictionary object containing authenticated JWT data

        Raises:
            ElmaxApiError: Whenever a non 200 return code is returned by the remote server
            ElmaxNetworkError: If the http request could not be completed due to a network error
            ElmaxPanelBusyError: If the number of retries have been exhausted while the panel returned a busy state (422)
        """
        retry_attempt = 0
        while retry_attempt < retry_attempts:
            try:
                response_data = await self._internal_request(method=method, url=url, data=data, authorized=authorized,
                                                             timeout=timeout)
                _LOGGER.debug(response_data)
                return response_data
            except ElmaxApiError as e:
                if e.status_code == 422:
                    retry_attempt += 1
                    _LOGGER.error("Panel is busy. Command will be retried in a moment.")
                    await asyncio.sleep(BUSY_WAIT_INTERVAL)
                else:
                    raise
        raise ElmaxPanelBusyError()

    async def _internal_request(
            self,
            method: "Elmax.HttpMethod",
            url: str,
            data: Optional[Dict] = None,
            authorized: bool = False,
            timeout: float = DEFAULT_HTTP_TIMEOUT
    ) -> Dict:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if authorized:
            headers["Authorization"] = f"JWT {self._raw_jwt}"

        try:
            if method == Elmax.HttpMethod.GET:
                response = await self._http_client.get(str(url), headers=headers, params=data, timeout=timeout)
            elif method == Elmax.HttpMethod.POST:
                response = await self._http_client.post(str(url), headers=headers, json=data, timeout=timeout)
            else:
                raise ValueError("Invalid/Unhandled method. Expecting GET or POST")

            _LOGGER.debug(
                "HTTP Request %s %s -> Status code: %d",
                str(method),
                url,
                response.status_code,
            )
            if response.status_code != 200:
                _LOGGER.error(
                    "Api call failed. Method=%s, Url=%s, Data=%s. Response code=%d. Response content=%s",
                    method,
                    url,
                    str(data),
                    response.status_code,
                    str(response.content),
                )
                raise ElmaxApiError(status_code=response.status_code)

            # The current API version does not return an error description nor an error http
            #  status code for invalid logins. Instead, an empty body is returned. In that case we
            #  assume the login failed due to invalid user/pass combination
            response_content = response.text
            if response_content == '':
                raise ElmaxBadLoginError()

            return response.json()

        # Wrap any other HTTP/NETWORK error
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            _LOGGER.exception("An unhandled error occurred while executing API Call.")
            raise ElmaxNetworkError("A network error occurred")

    @property
    def ssl_context(self) -> ssl.SSLContext:
        return self._ssl_context

    @property
    def base_url(self) -> URL:
        return self._base_url

    @property
    def current_panel_id(self) -> str:
        return self._current_panel_id

    def set_current_panel(self, panel_id: str, panel_pin: str = DEFAULT_PANEL_PIN):
        self._current_panel_id = panel_id
        self._current_panel_pin = panel_pin

    @property
    def is_authenticated(self) -> bool:
        """
        Specifies whether the client has been granted a JWT which is still valid (not expired)

        Returns:
            bool: True if there is a valid JWT token, False if there's no token or if it is expired
        """
        if self._jwt is None:
            # The user did not log in yet
            return False
        if self._jwt.get("exp", 0) <= time.time():
            self._jwt = None
            return False
        return True

    @property
    def token_expiration_time(self) -> int:
        """
        Returns the expiration timestamp of the stored JWT token.

        Returns:
            int: The timestamp of expiration or -1 if no token was present.
        """
        if self._jwt is None:
            return 0
        return self._jwt.get("exp", -1)

    @async_auth
    async def logout(self) -> None:
        """
        Invalidate the current token

        TODO:
            * Check if there is a HTTP API to invalidate the current token
        """
        self._jwt = None

    @abstractmethod
    async def login(self, *args, **kwargs) -> Dict:
        """
        Acquires a token and stores it internally.

        """
        raise NotImplemented()

    @abstractmethod
    async def renew_token(self, *args, **kwargs) -> Dict:
        """
        Renews the token used by the API client.

        """
        raise NotImplemented()

    @abstractmethod
    @async_auth
    async def get_current_panel_status(self, *args, **kwargs) -> PanelStatus:
        """
        Fetches the status of the local control panel.
        Returns: The current status of the control panel

        Raises:
             ElmaxBadPinError: Whenever the provided PIN is incorrect or in any way refused by the server
             ElmaxApiError: in case of underlying api call failure
        """
        raise NotImplemented()

    @async_auth
    async def get_endpoint_status(self, endpoint_id: str) -> EndpointStatus:
        """
        Fetches the panel status only for the given endpoint_id

        Args:
            control_panel_id: Id of the control panel to fetch status from
            endpoint_id: Id of the device to fetch data for

        Returns: The current status of the given endpoint
        """
        url = self._base_url / ENDPOINT_STATUS_ENTITY_ID / endpoint_id
        response_data = await self._request(Elmax.HttpMethod.GET, url=url, authorized=True)
        status = EndpointStatus.from_api_response(response_entry=response_data)
        return status

    @async_auth
    @abstractmethod
    async def execute_command(self,
                              endpoint_id: str,
                              command: Union[Command, str],
                              extra_payload: Dict = None,
                              retry_attempts: int = 3) -> Optional[Dict]:
        """
        Executes a command against the given endpoint
        Args:
            endpoint_id: EndpointID against which the command should be issued
            command: Command to issue. Can either be a string or a `Command` enum value
            extra_payload: Dictionary of extra payload to be issued to the endpoint
            retry_attempts: Maximum retry attempts in case of 422 error (panel busy)

        Returns: Json response data, if any, returned from the API
        """
        raise NotImplemented()

    @async_auth
    async def _execute_command(self,
                               url: str,
                               extra_payload: Dict = None,
                               retry_attempts: int = 3) -> Optional[Dict]:

        if extra_payload is not None and not isinstance(extra_payload, dict):
            raise ValueError("The extra_payload parameter must be a dictionary")

        response_data = await self._request(Elmax.HttpMethod.POST, url=url, authorized=True, data=extra_payload,
                                            retry_attempts=retry_attempts)
        _LOGGER.debug(response_data)
        return response_data

    def get_authenticated_username(self) -> Optional[str]:
        """
        Returns the username associated to the current JWT token, if any.
        In case the user is not authenticated, returns None
        """
        if self._jwt is None:
            return None
        return self._jwt.get("email")

    class HttpMethod(Enum):
        """Enumerative helper for supported HTTP methods of the Elmax API"""

        GET = "get"
        POST = "post"


class Elmax(GenericElmax):
    """
    Class implementing the Cloud HTTP API.
    """

    def __init__(self, username: str, password: str):
        """Client constructor.

        Args:
            username: username to use for logging in
            password: password to use for logging in
        """
        super(Elmax, self).__init__(base_url=BASE_URL)
        self._username = username
        self._password = password

    @async_auth
    async def list_control_panels(self) -> List[PanelEntry]:
        """
        Lists the control panels available for the given user

        Returns:
            List[PanelEntry]: The list of fetched `ControlPanel` devices discovered via the API
        """
        res = []
        url = self._base_url / ENDPOINT_DEVICES

        response_data = await self._request(
            method=Elmax.HttpMethod.GET, url=url, authorized=True
        )
        for response_entry in response_data:
            res.append(PanelEntry.from_api_response(response_entry=response_entry))
        return res

    async def renew_token(self, *args, **kwargs) -> Dict:
        """
        Renews the token used by the API client.
        This implementation simply triggers a new login and return the JWT to the caller
        """
        return await self.login()

    async def login(self, *args, **kwargs) -> Dict:
        """
        Connects to the API ENDPOINT and returns the access token to be used within the client

        Raises:
            ElmaxBadLoginError: if the login attempt fails due to bad username/password credentials
            ValueError: in case the json response is malformed
        """
        url = self._base_url / ENDPOINT_LOGIN
        data = {
            "username": self._username,
            "password": self._password,
        }
        try:
            response_data = await self._request(
                method=Elmax.HttpMethod.POST, url=url, data=data, authorized=False
            )
        except ElmaxApiError as e:
            if e.status_code == 401:
                raise ElmaxBadLoginError()
            raise

        if "token" not in response_data:
            raise ValueError("Missing token parameter in json response")

        jwt_token = response_data["token"]
        if not jwt_token.startswith("JWT "):
            raise ValueError("API did not return JWT token as expected")
        jt = jwt_token.split("JWT ")[1]

        # We do not need to verify the signature as this is usually something the server
        # needs to do. We will just decode it to get information about user/claims.
        # Moreover, since the JWT is obtained over a HTTPS channel, we do not need to verify
        # its integrity/confidentiality as the ssl does this for us
        self._jwt = jwt.decode(
            jt, algorithms=_JWT_ALGS, options={"verify_signature": False}
        )
        self._raw_jwt = (
            jt  # keep an encoded version of the JWT for convenience and performance
        )
        return self._jwt

    @async_auth
    async def get_panel_status(self,
                               control_panel_id: str,
                               pin: Optional[str] = DEFAULT_PANEL_PIN) -> PanelStatus:
        """
        Fetches the control panel status.

        Args:
            control_panel_id: Id of the control panel to fetch status from
            pin: security pin (optional)

        Returns: The current status of the control panel

        Raises:
             ElmaxBadPinError: Whenever the provided PIN is incorrect or in any way refused by the server
             ElmaxApiError: in case of underlying api call failure
        """
        url = self._base_url / ENDPOINT_DISCOVERY / control_panel_id / str(pin)
        try:
            response_data = await self._request(Elmax.HttpMethod.GET, url=url, authorized=True)
        except ElmaxApiError as e:
            if e.status_code == 403:
                raise ElmaxBadPinError() from e
            else:
                raise

        panel_status = PanelStatus.from_api_response(response_entry=response_data)
        return panel_status

    @async_auth
    async def execute_command(self,
                              endpoint_id: str,
                              command: Union[Command, str],
                              extra_payload: Dict = None,
                              retry_attempts: int = 3) -> Optional[Dict]:
        """
        Executes a command against the given endpoint
        Args:
            endpoint_id: EndpointID against which the command should be issued
            command: Command to issue. Can either be a string or a `Command` enum value
            extra_payload: Dictionary of extra payload to be issued to the endpoint
            retry_attempts: Maximum retry attempts in case of 422 error (panel busy)

        Returns: Json response data, if any, returned from the API
        """
        if isinstance(command, Command):
            cmd_str = str(command.value)
        elif isinstance(command, str):
            cmd_str = command
        else:
            raise ValueError("Invalid/unsupported command")

        url = self._base_url / endpoint_id / cmd_str
        return await self._execute_command(url=url, extra_payload=extra_payload, retry_attempts=retry_attempts)

    @async_auth
    async def get_current_panel_status(self, *args, **kwargs) -> PanelStatus:
        if self._current_panel_id is None:
            raise RuntimeError("Unset/Invalid current control panel ID.")
        return await self.get_panel_status(control_panel_id=self._current_panel_id, pin=self._current_panel_pin)


class ElmaxLocal(GenericElmax):
    """
    Class implementing the Local HTTP API client.
    """

    def __init__(self, panel_api_url: str, panel_code: str, ssl_context: ssl.SSLContext = None):
        """Client constructor.

        Args:
            panel_api_url: API address of the Elmax Panel
            panel_code: authentication code to be used with the panel
            ssl_context: SSLContext object to use for SSL verification
        """
        super(ElmaxLocal, self).__init__(base_url=panel_api_url, ssl_context=ssl_context)
        # The current version of the local API does not expose the panel ID attribute,
        # so we use the panel IP as ID
        self.set_current_panel(panel_id=panel_api_url, panel_pin=panel_code)
        self._cached_current_panel_status: Optional[PanelStatus] = None

    @async_auth
    async def renew_token(self, *args, **kwargs) -> Dict:
        """
        Renews the token used by the API client.
        This implementation invokes the specific URL to renew the token
        """
        if not self.supports_token_refresh:
            _LOGGER.debug("Current panel does not support token refresh. Re-issuing a login.")
            return await self.login()

        url = self._base_url / ENDPOINT_REFRESH

        try:
            response_data = await self._request(
                method=Elmax.HttpMethod.POST, url=url, authorized=True
            )
        except ElmaxApiError as e:
            if e.status_code in (401, 403):
                raise ElmaxBadLoginError()
            raise

        if "token" not in response_data:
            raise ValueError("Missing token parameter in json response")

        jwt_token = response_data["token"]
        if not jwt_token.startswith("JWT "):
            raise ValueError("API did not return JWT token as expected")
        jt = jwt_token.split("JWT ")[1]

        # We do not need to verify the signature as this is usually something the server
        # needs to do. We will just decode it to get information about user/claims.
        # Moreover, since the JWT is obtained over a HTTPS channel, we do not need to verify
        # its integrity/confidentiality as the ssl does this for us
        self._jwt = jwt.decode(
            jt, algorithms=_JWT_ALGS, options={"verify_signature": False}
        )
        self._raw_jwt = (
            jt  # keep an encoded version of the JWT for convenience and performance
        )
        return self._jwt

    async def login(self, *args, **kwargs) -> Dict:
        """
        Connects to the Local ENDPOINT and returns the access token to be used within the client

        Raises:
            ElmaxBadLoginError: if the login attempt fails due to bad username/password credentials
            ValueError: in case the json response is malformed
        """
        url = self._base_url / ENDPOINT_LOGIN
        data = {
            "pin": self._current_panel_pin
        }
        try:
            response_data = await self._request(
                method=Elmax.HttpMethod.POST, url=url, data=data, authorized=False
            )
        except ElmaxApiError as e:
            if e.status_code in (401, 403):
                raise ElmaxBadLoginError()
            raise

        if "token" not in response_data:
            raise ValueError("Missing token parameter in json response")

        jwt_token = response_data["token"]
        if not jwt_token.startswith("JWT "):
            raise ValueError("API did not return JWT token as expected")
        jt = jwt_token.split("JWT ")[1]

        # We do not need to verify the signature as this is usually something the server
        # needs to do. We will just decode it to get information about user/claims.
        # Moreover, since the JWT is obtained over a HTTPS channel, we do not need to verify
        # its integrity/confidentiality as the ssl does this for us
        self._jwt = jwt.decode(
            jt, algorithms=_JWT_ALGS, options={"verify_signature": False}
        )
        self._raw_jwt = (
            jt  # keep an encoded version of the JWT for convenience and performance
        )
        return self._jwt

    @async_auth
    async def execute_command(self,
                              endpoint_id: str,
                              command: Union[Command, str],
                              extra_payload: Dict = None,
                              retry_attempts: int = 3) -> Optional[Dict]:
        """
        Executes a command against the given endpoint
        Args:
            endpoint_id: EndpointID against which the command should be issued
            command: Command to issue. Can either be a string or a `Command` enum value
            extra_payload: Dictionary of extra payload to be issued to the endpoint
            retry_attempts: Maximum retry attempts in case of 422 error (panel busy)

        Returns: Json response data, if any, returned from the API
        """
        if isinstance(command, Command):
            cmd_str = str(command.value)
        elif isinstance(command, str):
            cmd_str = command
        else:
            raise ValueError("Invalid/unsupported command")

        url = self._base_url / ENDPOINT_LOCAL_CMD / endpoint_id / cmd_str
        return await self._execute_command(url=url, extra_payload=extra_payload, retry_attempts=retry_attempts)

    @async_auth
    async def get_current_panel_status(self, *args, **kwargs) -> PanelStatus:
        """
        Fetches the control panel status.

        Returns: The current status of the control panel

        Raises:
             ElmaxBadPinError: Whenever the provided PIN is incorrect or in any way refused by the server
             ElmaxApiError: in case of underlying api call failure
        """
        url = self._base_url / ENDPOINT_DISCOVERY
        try:
            response_data = await self._request(Elmax.HttpMethod.GET, url=url, authorized=True)
        except ElmaxApiError as e:
            if e.status_code == 403:
                raise ElmaxBadPinError() from e
            else:
                raise

        panel_status = PanelStatus.from_api_response(response_entry=response_data)
        self._cached_current_panel_status = panel_status
        return panel_status

    @property
    def last_cached_panel_status(self) -> Optional[PanelStatus]:
        return self._cached_current_panel_status

    @property
    def supports_token_refresh(self) -> bool:
        if self.last_cached_panel_status is not None:
            return version.parse(self.last_cached_panel_status.accessory_release) >= _MIN_VERSION_REFRESH_SUPPORT

        _LOGGER.warning("No cached panel status. Could not determine the version of the panel")
        return False