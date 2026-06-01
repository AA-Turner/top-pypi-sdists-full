"""
Wrapped requests module with proxy and CA certificate support.

This module provides a pre-configured requests session that automatically
uses the configured proxy and CA certificate settings.
"""

import logging
import requests
import threading
from typing import Optional, Any, Dict, Union
from requests.adapters import HTTPAdapter

# from requests.packages.urllib3.util.retry import Retry

from .proxy import HttpsProxy, CaBundlePath

logger = logging.getLogger("AuthProxyRequests")

DEFAULT_TIMEOUT = (5, 300)  # (connect_timeout, read_timeout) in seconds


class ConfiguredSession(requests.Session):
    """A requests Session subclass with automatic proxy and CA configuration."""

    def __init__(self):
        super().__init__()
        self._configure_session()

    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        return super().request(method, url, **kwargs)

    def _configure_session(self):
        """Configure the session with proxy and CA settings.

        Raises:
            ValueError: If HttpsProxy or CA bundle configuration fails
        """
        # Configure proxy settings - HttpsProxy must be configured
        self.trust_env = False
        proxy_url = HttpsProxy()
        self.proxies = {"https": proxy_url, "http": proxy_url}
        logger.info(f"Use HTTPS proxy: {proxy_url}")

        # Configure CA certificate file path
        # Note: CaBundlePath() may raise ValueError if path is set but file doesn't exist.
        ca_bundle_path = CaBundlePath()
        if not ca_bundle_path:
            raise ValueError(
                "COZE_OUTBOUND_AUTH_PROXY_CA_PATH environment variable is not configured. "
                "Please set this variable to configure the CA bundle file path."
            )
        self.verify = ca_bundle_path
        logger.info(f"Use CA bundle: {ca_bundle_path}")

        # self._configure_adapter()

    # def _configure_adapter(self):
    #     """Configure retry strategy and mount adapter."""
    #     retry_strategy = Retry(
    #         total=2,
    #         backoff_factor=1,
    #         status_forcelist=[429, 500, 502, 503, 504],
    #     )
    #     adapter = HTTPAdapter(max_retries=retry_strategy)
    #     self.mount("http://", adapter)
    #     self.mount("https://", adapter)


# Default session will be created on first use
_default_session = None
_session_lock = threading.Lock()


def _get_default_session() -> ConfiguredSession:
    """Get or create the default configured session."""
    global _default_session
    if _default_session is None:
        with _session_lock:
            if _default_session is None:
                _default_session = ConfiguredSession()
    return _default_session


def get(url: str, **kwargs: Any) -> requests.Response:
    """Send a GET request with configured proxy and CA settings."""
    return _get_default_session().get(url, **kwargs)


def post(
    url: str,
    data: Optional[Union[Dict[str, Any], str, bytes]] = None,
    json: Optional[Any] = None,
    **kwargs: Any,
) -> requests.Response:
    """Send a POST request with configured proxy and CA settings."""
    return _get_default_session().post(url, data=data, json=json, **kwargs)


def put(
    url: str, data: Optional[Union[Dict[str, Any], str, bytes]] = None, **kwargs: Any
) -> requests.Response:
    """Send a PUT request with configured proxy and CA settings."""
    return _get_default_session().put(url, data=data, **kwargs)


def delete(url: str, **kwargs: Any) -> requests.Response:
    """Send a DELETE request with configured proxy and CA settings."""
    return _get_default_session().delete(url, **kwargs)


def head(url: str, **kwargs: Any) -> requests.Response:
    """Send a HEAD request with configured proxy and CA settings."""
    return _get_default_session().head(url, **kwargs)


def options(url: str, **kwargs: Any) -> requests.Response:
    """Send an OPTIONS request with configured proxy and CA settings."""
    return _get_default_session().options(url, **kwargs)


def patch(
    url: str, data: Optional[Union[Dict[str, Any], str, bytes]] = None, **kwargs: Any
) -> requests.Response:
    """Send a PATCH request with configured proxy and CA settings."""
    return _get_default_session().patch(url, data=data, **kwargs)


def request(method: str, url: str, **kwargs: Any) -> requests.Response:
    """Send a request with the specified method and configured settings."""
    return _get_default_session().request(method, url, **kwargs)


def session() -> ConfiguredSession:
    """Create a new configured session instance."""
    return ConfiguredSession()


# Expose common requests exceptions and constants
from requests import exceptions, codes, status_codes
from requests.exceptions import (
    RequestException,
    ConnectionError,
    HTTPError,
    URLRequired,
    TooManyRedirects,
    Timeout,
    JSONDecodeError,
)

__all__ = [
    # Main functions
    "get",
    "post",
    "put",
    "delete",
    "head",
    "options",
    "patch",
    "request",
    "session",
    "ConfiguredSession",
    # Exceptions
    "RequestException",
    "ConnectionError",
    "HTTPError",
    "URLRequired",
    "TooManyRedirects",
    "Timeout",
    "JSONDecodeError",
    # Constants
    "codes",
    "status_codes",
    "exceptions",
]
