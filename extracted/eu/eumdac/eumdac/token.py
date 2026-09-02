"""Module containing classes to handle the token authentication."""

from __future__ import annotations

import abc
import sys
import time
from configparser import ConfigParser
from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple
from urllib.parse import quote as url_quote

import requests
from importlib import resources as importlib_resources
from requests.auth import AuthBase, HTTPBasicAuth

from eumdac.request import post
import eumdac.common
from eumdac.errors import EumdacError

from eumdac.logging import logger

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional

    if sys.version_info < (3, 9):
        from typing import Iterable, Mapping
    else:
        from collections.abc import Iterable, Mapping


class URLs(ConfigParser):
    """Dictionary-like ConfigParser based storage of EUMDAC related URLs"""

    def __init__(self, inifile: Optional[str] = None) -> None:
        super().__init__()
        if inifile:
            self.read(inifile)
        else:
            if sys.version_info >= (3, 9):
                with importlib_resources.as_file(
                    importlib_resources.files("eumdac") / "endpoints.ini"
                ) as path:
                    self.read(path)
            else:  # python < 3.9
                with importlib_resources.path("eumdac", "endpoints.ini") as path:
                    self.read(path)

    def get(  # type: ignore[override]
        self,
        section: str,
        option: str,
        raw: bool = False,
        vars: Optional[Mapping[str, str]] = None,
        fallback: str = "",
    ) -> str:
        """Get an option value for the given section"""
        if vars is not None:
            vars = {k: url_quote(str(v).encode()).replace("%", "%%") for k, v in vars.items()}
        return super().get(section, option, raw=raw, vars=vars, fallback=fallback)


class Credentials(NamedTuple):
    """Pair of Consumer Key and Secret authentication parameters.

    Attributes
    ----------
    - `consumer_key` : *str*
    - `consumer_secret` : *str*
    """

    consumer_key: str
    consumer_secret: str


class HTTPBearerAuth(AuthBase):
    """Attaches HTTP Bearer Authentication to the given Request object.

    Attributes
    ----------
    - `token`: *str*
        Bearer token
    """

    def __init__(self, token: str) -> None:
        """
        Parameters
        ----------
        - `token` : *str*
            Token to use for authentication
        """
        self.token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """Returns the given 'request' with the Bearer authentication parameter attached to the headers."""
        request.headers["authorization"] = f"Bearer {self.token}"
        return request


class BaseToken(metaclass=abc.ABCMeta):
    """Base class from which all eumdac authentication implementations derive"""

    urls: URLs

    @property
    def auth(self) -> Optional[AuthBase]:
        """To be overloaded in subclasses, shall return a configured AuthBase instance."""
        # overload in subclasses
        pass


class AccessToken(BaseToken):
    """EUMETSAT API access token

    Handles requesting of API tokens and their renewal after expiration.
    The str representation of AccessToken instances will be the current token value.

    Attributes
    ----------
    - `request_margin` : *int*
        seconds before expiration to start requesting a new token
    """

    request_margin: int = 2  # seconds
    _expiration: int = 0
    _access_token: str = ""

    credentials: Credentials
    validity_period: int  # seconds
    urls: URLs
    cache: bool  # does nothing, cache is always on in the server

    def __init__(
        self,
        credentials: Iterable[str],
        validity: int = 86400,
        cache: bool = True,  # does nothing
        urls: Optional[URLs] = None,
    ) -> None:
        """Initializes the AccessToken, but does not request a token.

        Parameters
        ----------
        - `credentials`: *(consumer_key, consumer_secret)*
            Authentication credentials in the form of a pair of key and secret.
        - `cache`: *bool, default: False*
            Set to false to always request new tokens, even if the current one has not expired.
        - `validity`: *int*
            Validity period for tokens, in seconds
        - `urls`: *URLs, optional*
            URLs instance to be used, will be initialized to the default if not provided.
        """
        self.credentials = Credentials(*credentials)
        self.validity_period = validity
        self.urls = urls or URLs()
        self.cache = cache

    def __str__(self) -> str:
        """Return the current token in str form."""
        return self.access_token

    @property
    def expiration(self) -> datetime:
        """Expiration of the current token string"""
        # Generate a token only when uninitialized
        if self._expiration == 0:
            self._update_token_data()
        return datetime.fromtimestamp(self._expiration)

    @property
    def access_token(self) -> str:
        """Token string"""
        expires_in = self._expiration - time.time()
        if expires_in > 0:
            logger.debug(f"Current token {self._access_token} expires in {expires_in} seconds.")
        else:
            # If we don't have a token, just get one
            logger.debug(f"Requesting new token")
            self._update_token_data()
            expires_in = self._expiration - time.time()

        # Renew token when if  there's less than request_margin time to expire
        if expires_in < self.request_margin:
            tries = 0
            previous_token = self._access_token
            logger.debug(
                f"Token expires in {expires_in:.2f}, starting renewal of {self._access_token}."
            )
            # Loop until we are sure we got the new token
            while (
                tries < 20
                and self._access_token == previous_token
                or expires_in < self.request_margin
            ):
                tries += 1
                time.sleep(0.5)
                logger.debug(f"Requesting new token...")
                self._update_token_data()
                logger.debug(f"Received/previous {self._access_token}/{previous_token})")
                expires_in = self._expiration - time.time()
            if tries >= 100:
                raise EumdacError(
                    f"Could not get fresh token from server, got {self._access_token}, which expires {datetime.fromtimestamp(self._expiration)}"
                )

        return self._access_token

    @property
    def auth(self) -> AuthBase:
        """Authentication object using the current token"""
        return HTTPBearerAuth(self.access_token)

    def _update_token_data(self) -> None:
        """Request a new token and renew the expiration time"""
        auth = HTTPBasicAuth(*self.credentials)
        now = time.time()
        response = post(
            self.urls.get("token", "token"),
            auth=auth,
            data={"grant_type": "client_credentials", "validity_period": self.validity_period},
            headers=eumdac.common.headers,
        )
        response.raise_for_status()
        token_data = response.json()
        self._expiration = now + token_data["expires_in"]
        self._access_token = token_data["access_token"]

    def _revoke(self) -> None:
        """Revoke the current token"""
        auth = HTTPBasicAuth(*self.credentials)
        response = post(
            self.urls.get("token", "revoke"),
            auth=auth,
            data={"grant_type": "client_credentials", "token": self._access_token},
            headers=eumdac.common.headers,
        )
        response.raise_for_status()
        self._expiration = 0
        self._access_token = ""


class AnonymousAccessToken(BaseToken):
    """Token class for anonymous access, provides no authentication parameters."""

    def __init__(self, urls: Optional[URLs] = None):
        """Init the token."""
        self.urls = urls or URLs()

    @property
    def auth(self) -> Optional[AuthBase]:
        """Return None"""
        return None
