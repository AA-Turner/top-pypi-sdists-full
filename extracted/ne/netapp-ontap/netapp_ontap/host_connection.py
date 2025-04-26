# pylint: disable=line-too-long
"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This module defines a host connection object which is used to communicate with
the API host.
"""
import base64
import binascii
import copy
import logging
import urllib.parse
from contextlib import contextmanager
from http.client import responses
from threading import local
from typing import Generator, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  # type: ignore

from netapp_ontap import config  # pylint: disable=cyclic-import

# prevent "No handlers" message if consumer application doesn't configure logging at all
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

LOCAL_DATA = local()
LOCAL_DATA.host_context = None


class WrappedSession(requests.Session):
    """A wrapper for requests.Session to allow the 'verify' the property
    to override the REQUESTS_CA_BUNDLE environment variable.
    """

    # pylint: disable=too-many-positional-arguments,too-many-arguments
    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        if self.verify is False:
            verify = False

        return super().merge_environment_settings(url, proxies, stream, verify, cert)


class HostConnection:  # pylint: disable=too-many-instance-attributes
    """The HostConnection allows the client application to store their credentials
    and reuse them for each operation. There are three ways to use a connection
    object:

    * The first is to use the connection object as a context manager. Any operations
      on a resource that are called within the scope of the block will use that
      connection.
    * The second is to call set_connection() on a resource object. This
      will then be the connection used for all actions for that object only.
    * The third way is to call netapp_ontap.config.CONNECTION = connection. This
      connection instance will now be used for all actions on all resource
      objects (that do not otherwise set their own connection). This reduces
      the need to pass the connection around the application.

    Connections will be searched for in this order when executing an action.
    """

    # pylint: disable=too-many-positional-arguments,too-many-locals,too-many-arguments
    def __init__(
        self,
        host,
        username: Optional[str] = None,
        password: Optional[str] = None,
        cert: Optional[str] = None,
        key: Optional[str] = None,
        verify: bool = True,
        poll_timeout: int = 30,
        poll_interval: int = 5,
        headers: Optional[dict] = None,
        port: int = 443,
        protocol_timeouts: tuple = (6, 45),
        scheme: str = "https",
    ):
        """Store information needed to contact the API host

        Either username and password must be provided or certificate and key must
        be provided or the 'Authorization' must be provided in the headers.

        If verify is set to False, urllib3's InsecureRequestWarnings will also be
        silenced in the logs.

        Args:
            host: The API host that the library should talk to
            username: The user identifier known to the host
            password: The secret for the user
            cert: The file path to the users public certificate. The common
                name in the certificate must match the account name.
            key: A private key in PEM format
            verify: If an SSL connection is made to the host, this parameter
                controls how the validity of the trust chain of the certificate
                is handled. See the documentation for the requests library for more information:
                https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification
            poll_timeout: Time in seconds to poll on a job. This setting applies to all polling
                that uses this connection unless overridden as a parameter to poll(). Defaults
                to 30 seconds.
            poll_interval: Time in seconds to wait between polls on a job. This setting applies
                to all polling that uses this connection unless overridden as a parameter to
                poll(). Defaults to 5 seconds.
            headers: Any custom headers to be passed to each request using this connection object.
            port: The port that the library should talk to
            protocol_timeouts: A tuple to set the connection_timeout and read_timeout respectively in seconds.
                The default for connection_timeout=6 and read_timeout=45.
            scheme: The scheme to use for the connection. Defaults to https.
        """

        authentication_methods = 0
        if username and password is not None:
            authentication_methods += 1
        if cert and key:
            authentication_methods += 1
        elif headers and "Authorization" in headers:
            authentication_methods += 1

        if authentication_methods != 1:
            from netapp_ontap.error import (  # pylint: disable=cyclic-import,import-outside-toplevel
                NetAppRestError,
            )

            raise NetAppRestError(
                "There must be only one authentication method provided. The following four"
                " methods are the only types of authentication methods currently accepted."
                " 1. Username and password. 2. Cert and key. 3. An 'Authorization' header."
                " 4. An 'Authorization' header and a cert and key"
            )

        self.scheme = scheme
        self.host = host
        # check if the hostname is wrapped with [] and extract the name from there
        if (
            self.host
            and str(self.host).startswith("[")
            and str(self.host).endswith("]")
        ):
            self.host = self.host[1:-1]
        self.port = port
        self.username = username
        self.password = password
        self.cert = cert
        self.key = key
        self.verify = verify
        self.poll_timeout = poll_timeout
        self.poll_interval = poll_interval
        self.headers = headers
        self.protocol_timeouts = protocol_timeouts
        self._old_context = None  # type: Optional[HostConnection]
        self._request_session = None  # type: Optional[requests.Session]
        from netapp_ontap import utils  # pylint: disable=import-outside-toplevel

        self._using_ipv6: bool = utils._is_ip_v6(
            self.host
        )  # pylint: disable=protected-access

        if not self.verify:
            import urllib3  # pylint: disable=import-outside-toplevel

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def get_host_context() -> "Optional[HostConnection]":
        """Get the current host context, if any.

        Returns:
            A HostConnection object or None if not in a host connection context.
        """

        return getattr(LOCAL_DATA, "host_context", None)

    @property
    def basic_auth(self) -> Optional[Tuple[str, str]]:
        """Pulls the credentials out of the connection object.

        Returns:
            A tuple of username and password sufficient for passing to the requests library. Returns None if this connection is not configured for basic auth with a username and password.
        """

        if self.username and self.password is not None:
            return (self.username, self.password)
        return None

    @property
    def cert_auth(self) -> Optional[Tuple[str, str]]:
        """Pulls the certificate details out of the connection object.

        Returns:
            A tuple of cert and key sufficient for passing to the requests library. Returns None if this connection is not configured for cert auth with a cert and key.
        """

        if self.cert and self.key:
            return (self.cert, self.key)
        return None

    @property
    def bearer_auth(self) -> Optional[Tuple[str, str]]:
        """Pulls the header name and token out of the connection object.

        Returns:
            A tuple of the header name and token for passing to the requests library. Returns None if this connection is not configured for oauth2 yet
        """

        if (
            not self.headers
            or self.headers.get("Authorization", "").split()[0] != "Bearer"
        ):
            return None

        # Right now NetApp only supports 3 IDP (keycloak, auth0, adfs) which all use the JWT format
        # The following code checks to make sure that the token generally follows the JWT format before returning the tuple
        # The steps are taken from https://www.rfc-editor.org/rfc/rfc7519#section-7.2
        token = self.headers["Authorization"].split()[1]
        # 1 Verify that the JWT contains at least one period ('.') character.
        if "." not in token:
            return None
        # 2 Let the Encoded JOSE Header be the portion of the JWT before the first period ('.') character.
        header = token.split(".")[0]
        message = token.split(".")[1]
        # 3~9 Base64url decode the Encoded JOSE Header and Message following the restriction that no line breaks, whitespace, or other additional characters have been used.
        if " " in header or "\n" in header or " " in message or "\n" in message:
            return None
        try:
            for b64 in (header, message):
                b64 += "=" * (
                    (4 - len(b64) % 4) % 4
                )  # add padding as required to properly encode and decode with base64
                if base64.b64encode(base64.b64decode(b64)) != bytes(b64, "utf-8"):
                    return None
        except (ValueError, TypeError, binascii.Error):
            return None
        # Success! The our tuple is most likely a valid JWT
        return (
            self.headers["Authorization"].split()[0],
            self.headers["Authorization"].split()[1],
        )

    @property
    def origin(self) -> str:
        """The beginning of any REST endpoint.

        Returns:
            The origin part of the URL. For example, `http://1.2.3.4:8080`.
        """
        hostname = self.host
        if self._using_ipv6:
            hostname = f"[{hostname}]"

        return f"{self.scheme}://{hostname}:{self.port}"

    @property
    def request_headers(self) -> Optional[dict]:
        """Retrieves the headers set out of the connection object

        Returns:
            A dictionary consisting of header names and values for passing to the requests library. Returns None if no headers are configured.
        """

        if self.headers:
            return self.headers
        return None

    @request_headers.setter
    def request_headers(self, headers):
        """Set the request headers for the connection object"""
        if isinstance(headers, dict):
            self.headers = headers
        else:
            raise TypeError("Request headers must be specified as a 'dict' type")

    @contextmanager
    def with_headers(self, headers: dict) -> Generator["HostConnection", None, None]:
        """Manually set the headers field of the connection object"""
        old_headers = copy.deepcopy(self.request_headers)
        self.headers = headers
        yield self
        self.headers = old_headers
        self._request_session = None

    def __enter__(self):
        self._old_context = getattr(LOCAL_DATA, "host_context", None)
        LOCAL_DATA.host_context = self
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        LOCAL_DATA.host_context = self._old_context

    @property
    def session(self) -> requests.Session:
        """A `requests.Session` object which is used for all API calls.

        This session is reused for each API call made with this connection. Multiple
        requests may therefore be sent through the same TCP connection assuming
        the host supports keep-alive.

        Returns:
            A `requests.Session` object which is used for all API calls.
        """

        current_session = getattr(self, "_request_session", None)
        if not current_session:
            current_session = WrappedSession()

        if self.origin not in current_session.adapters:
            if config.RETRY_API_ON_ERROR:
                retry_strategy: Retry = LoggingRetry(
                    total=config.RETRY_API_ATTEMPTS,
                    status_forcelist=config.RETRY_API_ERROR_CODES,
                    allowed_methods=config.RETRY_API_HTTP_METHODS,
                    backoff_factor=config.RETRY_API_BACKOFF_FACTOR,
                )
            else:
                retry_strategy: Retry = LoggingRetry.from_int(5)  # type: ignore
            current_session.mount(
                self.origin,
                LoggingAdapter(
                    self, max_retries=retry_strategy, timeout=self.protocol_timeouts
                ),
            )
        if self.basic_auth:
            current_session.auth = self.basic_auth
        else:
            current_session.cert = self.cert_auth
        if self.request_headers:
            current_session.headers.update(self.request_headers)
        current_session.verify = self.verify

        import netapp_ontap  # pylint: disable=cyclic-import,import-outside-toplevel

        current_session.headers.update(
            {"X-Dot-Client-App": f"netapp-ontap-python-{netapp_ontap.__version__}"}
        )

        self._request_session = current_session
        return current_session


class LoggingRetry(Retry):
    """A custom Retry which logs API calls during a retry if logging is enabled"""

    def increment(  # type: ignore # pylint: disable=too-many-arguments
        self,
        method=None,
        url=None,
        response=None,
        error=None,
        _pool=None,
        _stacktrace=None,
    ) -> Retry:
        from netapp_ontap import (  # pylint: disable=cyclic-import,import-outside-toplevel
            utils,
        )

        if response is not None and utils.LOG_ALL_API_CALLS:
            requests_response = self._urllib3_to_requests(response)
            pretty_print_response(requests_response)
        return super().increment(
            method=method,
            url=url,
            response=response,
            error=error,
            _pool=_pool,
            _stacktrace=_stacktrace,
        )

    @staticmethod
    def _urllib3_to_requests(response) -> requests.Response:
        """Convert a urllib3 HTTPResponse to a requests Response"""
        resp = requests.Response()
        resp.raw = response
        resp.headers = response.headers
        resp.status_code = response.status
        return resp


class LoggingAdapter(HTTPAdapter):
    """A custom HTTPAdapter which logs API calls if logging is enabled"""

    def __init__(self, host_connection, *args, **kwargs):
        self.timeout = kwargs.pop("timeout", None)
        if self.timeout is None and host_connection is not None:
            self.timeout = host_connection.protocol_timeouts
        self.host_connection = host_connection
        super().__init__(*args, **kwargs)

    def send(  # pylint: disable=too-many-positional-arguments,too-many-arguments
        self,
        request,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
    ) -> requests.Response:
        timeout = timeout if timeout else self.timeout
        request.url = _percent_encode_spaces(request.url)
        from netapp_ontap import (  # pylint: disable=cyclic-import,import-outside-toplevel
            utils,
        )

        if utils.LOG_ALL_API_CALLS:
            pretty_print_request(request)
        response = super().send(
            request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
        )
        if cert and response.status_code == 401:
            del self.host_connection._request_session
        if utils.LOG_ALL_API_CALLS:
            pretty_print_response(response)
        elif response.status_code >= 400 and utils.DEBUG:
            pretty_print_request(request)
            pretty_print_response(response)
        return response


def pretty_print_request(request: requests.PreparedRequest) -> None:
    """Prints the complete request in a pretty way."""
    result = "\n-----------REQUEST-----------"
    result += f"\n{request.method} {request.url}\n"
    for k, v in request.headers.items():  # pylint: disable=invalid-name
        if k == "Authorization" and config.REDACT_AUTHORIZATION_HEADER:
            result += f"{k}: *****\n"
        else:
            result += f"{k}: {v}\n"
    if request.body and config.REDACT_SENSITIVE_FIELDS:
        from netapp_ontap import (  # pylint: disable=cyclic-import,import-outside-toplevel
            utils,
        )

        if isinstance(request.body, bytes):
            result += utils.redact_sensitive_fields(request.body.decode("utf-8"))
        else:
            result += utils.redact_sensitive_fields(request.body)

    else:
        result += str(request.body)
    result += "\n-----------------------------"

    LOGGER.debug(result)


def pretty_print_response(response: requests.Response) -> None:
    """Prints the complete response in a pretty way."""
    result = "\n-----------RESPONSE-----------"
    result += f"\n{response.status_code} {responses[response.status_code]}\n"
    result += "\n".join(f"{k}: {v}" for k, v in response.headers.items())
    if response.text and config.REDACT_SENSITIVE_FIELDS:
        from netapp_ontap import (  # pylint: disable=cyclic-import,import-outside-toplevel
            utils,
        )

        result += "\n" + utils.redact_sensitive_fields(response.text)
    else:
        result += "\n" + response.text
    result += "\n------------------------------"

    LOGGER.debug(result)


def _percent_encode_spaces(url: str) -> str:
    """ONTAP likes spaces in query parameters to be space encoded, but the requests
    library encodes them as + by default. Here, we will fix that up so that ONTAP
    will return correct responses.
    """

    parse_result = urllib.parse.urlparse(url)
    query_data = dict(urllib.parse.parse_qsl(parse_result.query))
    query_data_str = urllib.parse.urlencode(query_data, quote_via=urllib.parse.quote)
    return urllib.parse.urlunparse(parse_result._replace(query=query_data_str))
