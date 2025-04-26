import webbrowser
from time import sleep

from authlib.integrations.base_client import OAuthError
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc6749 import OAuth2Token
from click import echo
from pydantic import BaseModel

from .constants import OPENID_SCOPE
from .discovery import ArthurOIDCMetadata
from .session import _ArthurRefreshTokenAPISession, ArthurAPISession

CLIENT_ID = "scope-cli-client"


class _DeviceAuthorization(BaseModel, extra="allow"):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


class DeviceAuthorizer:
    """
    This class implements the OAuth2 Device Authorization Flow to generate a Session object with the Arthur API.
    """

    def __init__(self, arthur_host: str, client_id=CLIENT_ID):
        self.arthur_host = arthur_host
        self.metadata = ArthurOIDCMetadata(arthur_host)
        self.client_id = client_id
        self._oauth_sess = OAuth2Session(client_id=self.client_id, scope=OPENID_SCOPE)
        self._browser_open_f = webbrowser.open

    def authorize(self) -> ArthurAPISession:
        # create device code in IDP
        dev_code = self._create_device_code()
        # open browser for user to complete authorization
        if not self._browser_open_f(dev_code.verification_uri_complete):
            echo(
                f"Could not open browser, please visit {dev_code.verification_uri} "
                f"and enter the code {dev_code.user_code}."
            )
        # start poll
        token = None
        while not token:
            try:
                token = self._exchange_code_for_token(dev_code.device_code)
            except OAuthError:
                echo("Waiting for authorization to complete")
                sleep(dev_code.interval)

        return _ArthurRefreshTokenAPISession(
            oauth_session=self._oauth_sess,
            metadata=self.metadata,
        )

    def _create_device_code(self) -> _DeviceAuthorization:
        resp = self._oauth_sess.post(
            self.metadata.device_authorization_endpoint,
            data={"client_id": self.client_id, "scope": OPENID_SCOPE},
            withhold_token=True,  # noqa
        )
        return _DeviceAuthorization(**resp.json())

    def _exchange_code_for_token(self, device_code: str) -> OAuth2Token:
        return self._oauth_sess.fetch_token(
            url=self.metadata.token_endpoint,
            grant_type="urn:ietf:params:oauth:grant-type:device_code",
            device_code=device_code,
        )
