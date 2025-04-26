from abc import ABC, abstractmethod
import threading

from authlib.oauth2.rfc6749 import OAuth2Token
from authlib.integrations.requests_client import OAuth2Session

from .constants import OPENID_SCOPE
from .discovery import ArthurOIDCMetadata


class ArthurAPISession(ABC):
    """
    The ArthurSession is an interface that allows users to retrieve a token for use with the Arthur API.
    Calling the token() method may refresh the token if it's within leeway seconds of expiration.
    The session object is thread safe, only one thread will be able to refresh it at a time.
    """

    @abstractmethod
    def token(self, leeway=30) -> OAuth2Token:
        pass

    @abstractmethod
    def host(self) -> str:
        pass


class _ArthurRefreshTokenAPISession(ArthurAPISession):
    """
    This class takes an OAuth2Session and creates a wrapper to automatically refresh it when asked for.
    Note, this is not meant to be used directly, but should be returned from other authorization flows.
    """

    def __init__(
        self,
        oauth_session: OAuth2Session,
        metadata: ArthurOIDCMetadata,
    ):
        self._oauth_session = oauth_session
        self._metadata = metadata
        self._lock = threading.Lock()

    def token(self, leeway=30) -> OAuth2Token:
        with self._lock:
            if self._oauth_session.token.is_expired(leeway):
                self._oauth_session.refresh_token(url=self._metadata.token_endpoint)
            return self._oauth_session.token

    def host(self) -> str:
        return self._metadata.arthur_host


class ArthurClientCredentialsAPISession(ArthurAPISession):
    """
    This class takes an OAuth2 client ID and secret and creates a wrapper to automatically refresh the token
    when asked for.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        metadata: ArthurOIDCMetadata,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self._oauth_session = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=OPENID_SCOPE,
        )
        self._metadata = metadata
        self._lock = threading.Lock()

    def token(self, leeway=30) -> OAuth2Token:
        with self._lock:
            if (
                self._oauth_session.token is None
                or self._oauth_session.token.is_expired(leeway)
            ):
                self._oauth_session.fetch_token(url=self._metadata.token_endpoint)
            return self._oauth_session.token

    def host(self) -> str:
        return self._metadata.arthur_host
