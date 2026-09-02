import os

from typing import Optional, Dict, TypedDict

from httpx._types import ProxyTypes
from typing_extensions import Unpack

from novita_sandbox.core.api.metadata import package_version

REQUEST_TIMEOUT: float = 60.0  # 60 seconds
LEGACY_REQUEST_TIMEOUT: float = 1800.0  # 30 minutes

KEEPALIVE_PING_INTERVAL_SEC = 50  # 50 seconds
KEEPALIVE_PING_HEADER = "Keepalive-Ping-Interval"
DEFAULT_NOVITA_DOMAIN = "us-phx-1.sandbox.novita.ai"
SUPPORTED_NOVITA_DOMAIN = DEFAULT_NOVITA_DOMAIN

LEGACY_NOVITA_DOMAINS = [
    "sandbox.novita.ai",
    "us-01.sandbox.novita.ai",
    "us-ga-01.sandbox.novita.ai",
    "us-ga-1.sandbox.novita.ai",
    "sandbox-dev.novita.ai",
    "us-01.sandbox-dev.novita.ai",
    "us-ga-01.sandbox-dev.novita.ai",
    "us-ca-1.sandbox-dev.novita.ai",
]
LATEST_LEGACY_SDK_VERSION = "1.2.5b2"


def is_legacy_domain(domain: str) -> bool:
    if not domain:
        raise ValueError("domain cannot be empty")
    return domain in LEGACY_NOVITA_DOMAINS


def validate_domain(domain: str):
    if not domain:
        raise ValueError("domain cannot be empty")


class ApiParams(TypedDict, total=False):
    """
    Parameters for a request.

    In the case of a sandbox, it applies to all **requests made to the returned sandbox**.
    """

    request_timeout: Optional[float]
    """Timeout for the request in **seconds**, defaults to 60 seconds."""

    headers: Optional[Dict[str, str]]
    """Additional headers to send with the request."""

    api_key: Optional[str]
    """Novita API key to use for authentication, defaults to `NOVITA_API_KEY` environment variable."""

    domain: Optional[str]
    """Novita AI sandbox domain to use for authentication, defaults to `NOVITA_DOMAIN` or `us-phx-1.sandbox.novita.ai`."""

    api_url: Optional[str]
    """URL to use for the API, defaults to `https://api.<domain>`. For internal use only."""

    debug: Optional[bool]
    """Whether to use debug mode, defaults to `NOVITA_DEBUG` environment variable."""

    proxy: Optional[ProxyTypes]
    """Proxy to use for the request. In case of a sandbox it applies to all **requests made to the returned sandbox**."""

    sandbox_url: Optional[str]
    """URL to connect to sandbox, defaults to `NOVITA_SANDBOX_URL` environment variable."""


class ConnectionConfig:
    """
    Configuration for the connection to the API.
    """

    envd_port = 49983

    @staticmethod
    def _domain():
        return os.getenv("NOVITA_DOMAIN") or DEFAULT_NOVITA_DOMAIN

    @staticmethod
    def _debug():
        return os.getenv("NOVITA_DEBUG", "false").lower() == "true"

    @staticmethod
    def _api_key():
        return os.getenv("NOVITA_API_KEY")

    @staticmethod
    def _api_url():
        return os.getenv("NOVITA_API_URL")

    @staticmethod
    def _sandbox_url():
        return os.getenv("NOVITA_SANDBOX_URL")

    @staticmethod
    def _access_token():
        return os.getenv("NOVITA_ACCESS_TOKEN")

    def __init__(
        self,
        domain: Optional[str] = None,
        debug: Optional[bool] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        sandbox_url: Optional[str] = None,
        access_token: Optional[str] = None,
        request_timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None,
        extra_sandbox_headers: Optional[Dict[str, str]] = None,
        proxy: Optional[ProxyTypes] = None,
    ):
        self.domain = domain or ConnectionConfig._domain()
        validate_domain(self.domain)
        self.is_legacy_domain = is_legacy_domain(self.domain)
        self.debug = debug or ConnectionConfig._debug()
        self.api_key = api_key or ConnectionConfig._api_key()
        self.access_token = access_token or ConnectionConfig._access_token()
        self.headers = headers or {}
        self.headers["User-Agent"] = f"novita-sandbox-python-sdk/{package_version}"
        self.__extra_sandbox_headers = extra_sandbox_headers or {}

        self.proxy = proxy

        default_request_timeout = (
            LEGACY_REQUEST_TIMEOUT if self.is_legacy_domain else REQUEST_TIMEOUT
        )
        self.request_timeout = ConnectionConfig._get_request_timeout(
            default_request_timeout,
            request_timeout,
        )

        self.api_url = (
            api_url
            or ConnectionConfig._api_url()
            or ("http://localhost:3000" if self.debug else f"https://api.{self.domain}")
        )

        self._sandbox_url: Optional[str] = (
            sandbox_url or ConnectionConfig._sandbox_url()
        )

    @staticmethod
    def _get_request_timeout(
        default_timeout: Optional[float],
        request_timeout: Optional[float],
    ):
        if request_timeout == 0:
            return None
        elif request_timeout is not None:
            return request_timeout
        else:
            return default_timeout

    def get_request_timeout(self, request_timeout: Optional[float] = None):
        return self._get_request_timeout(self.request_timeout, request_timeout)

    def get_sandbox_url(self, sandbox_id: str, sandbox_domain: str) -> str:
        if self._sandbox_url:
            return self._sandbox_url  # type: ignore[return-value]

        return f"{'http' if self.debug else 'https'}://{self.get_host(sandbox_id, sandbox_domain, self.envd_port)}"

    def get_host(self, sandbox_id: str, sandbox_domain: str, port: int) -> str:
        """
        Get the host address to connect to the sandbox.
        You can then use this address to connect to the sandbox port from outside the sandbox via HTTP or WebSocket.

        :param port: Port to connect to
        :param sandbox_domain: Domain to connect to
        :param sandbox_id: Sandbox to connect to

        :return: Host address to connect to
        """
        if self.debug:
            return f"localhost:{port}"

        return f"{port}-{sandbox_id}.{sandbox_domain}"

    def get_api_params(
        self,
        **opts: Unpack[ApiParams],
    ) -> dict:
        """
        Get the parameters for the API call.

        This is used to avoid passing the following attributes to the API call:
        - access_token
        - api_url

        It also returns a copy, so the original object is not modified.

        :return: Dictionary of parameters for the API call
        """
        headers = opts.get("headers")
        request_timeout = opts.get("request_timeout")
        api_key = opts.get("api_key")
        api_url = opts.get("api_url")
        domain = opts.get("domain")
        debug = opts.get("debug")
        proxy = opts.get("proxy")
        effective_domain = domain if domain is not None else self.domain
        validate_domain(effective_domain)

        req_headers = self.headers.copy()
        if headers is not None:
            req_headers.update(headers)

        return dict(
            ApiParams(
                api_key=api_key if api_key is not None else self.api_key,
                api_url=api_url if api_url is not None else self.api_url,
                domain=effective_domain,
                debug=debug if debug is not None else self.debug,
                request_timeout=self.get_request_timeout(request_timeout),
                headers=req_headers,
                proxy=proxy if proxy is not None else self.proxy,
            )
        )

    @property
    def sandbox_headers(self):
        """
        We need this separate as we use the same header for Novita access token to API and envd access token to sandbox.
        """
        return {
            **self.headers,
            **self.__extra_sandbox_headers,
        }


Username = str
"""
User used for the operation in the sandbox.
"""

default_username: Username = "user"
"""
Default user used for the operation in the sandbox.
"""
