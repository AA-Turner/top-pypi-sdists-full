"""
This module contains a subset of //tobikodata/tcloud/auth.py that only is
concerened with the ability to load and refresh a tcloud JWT token.  It also
providers a PublicHttpClient child class that uses tcloud JWT tokens to
authenticate.  There is code duplication between this and tcloud due to the
isolation that tcloud needs.
"""

import logging
import os
import stat
import time
import typing as t
from pathlib import Path

from authlib.integrations.requests_client import OAuth2Session
from httpx import Auth, HTTPStatusError, Request, Response
from ruamel.yaml import YAML

from tobikodata.http_client.public import PublicHttpClient

# Yaml
yaml = YAML()

# This is duplicated from tcloud in order to avoid pulling in tcloud deps into
# http client
SCOPE = os.environ.get("TCLOUD_SCOPE", "tbk:scope:projects")
"""The scopes to request from the tobiko auth service"""

TCLOUD_PATH = Path(os.environ.get("TCLOUD_HOME", Path.home() / ".tcloud"))
"""The location of the tcloud config folder"""

CLIENT_ID = os.environ.get("TCLOUD_CLIENT_ID", "f695a000-bc5b-43c2-bcb7-8e0179ddff0c")
"""The OAuth client ID to use"""

CLIENT_SECRET = os.environ.get("TCLOUD_CLIENT_SECRET")
"""The OAuth client secret to use for the client credentials (service-to-service) flow"""

TOKEN_URL = os.environ.get("TCLOUD_TOKEN_URL", "https://cloud.tobikodata.com/auth/token")
"""The OAuth token endpoint to use"""


class SSOAuth:
    """
    This class handles the OAuth flows and CLI process for refreshing an ID
    Token from tcloud.  Authentication initially must be done with tcloud.
    """

    def __init__(
        self,
        token_url: str,
        client_id: str,
        scope: str,
        auth_yaml_path: Path,
        client_secret: t.Optional[str] = None,
        logger: t.Optional[logging.Logger] = None,
    ) -> None:
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.logger = logger or logging.getLogger(__name__)

        if not auth_yaml_path.exists():
            auth_yaml_path.mkdir(parents=True, exist_ok=True)
        self._auth_yaml_path = auth_yaml_path
        self.session = OAuth2Session(self.client_id, self.client_secret, scope=self.scope)
        self.token_info = self._load_auth_yaml()

    @property
    def _auth_yaml_file(self) -> Path:
        return self._auth_yaml_path / "auth.yaml"

    def _delete_auth_yaml(self) -> None:
        """
        Removes the auth.yaml file if it exists.
        """
        auth_file = self._auth_yaml_file
        if auth_file.exists() and os.access(auth_file, os.W_OK):
            os.remove(auth_file)

    def _load_auth_yaml(self) -> t.Optional[t.Dict]:
        """
        Loads the full auth.yaml file that might exist in the CLI config folder.
        """
        auth_file = self._auth_yaml_file

        if auth_file.exists() and os.access(auth_file, os.R_OK):
            with auth_file.open("r") as fd:
                return yaml.load(fd.read())

        return None

    def _save_auth_yaml(self, data: t.Dict) -> None:
        """
        Saves the given dictionary to auth.yaml

        Args:
            data: The dictionary to save
        """
        auth_file = self._auth_yaml_file

        with auth_file.open("w") as fd:
            yaml.dump(data, fd)
        os.chmod(auth_file, stat.S_IWUSR | stat.S_IRUSR)

    def id_token(self) -> t.Optional[str]:
        """
        Returns the id_token needed for SSO.  Will return the one saved on disk,
        unless it's expired.  If the token on disk is expired, it will try to
        refresh it.
        """

        if self.token_info:
            # If we are within 5 minutes of expire time, run refresh
            if self.token_info.get("expires_at", 0.0) > (time.time() + 300):
                # We have a current token on disk, return it
                return self.token_info["id_token"]

            # Our token is expired, refresh it if possible
            try:
                refreshed_token = self.refresh_token()

                if refreshed_token:
                    return refreshed_token

                # We failed to refresh, logout
                self._delete_auth_yaml()

            except Exception:
                # We failed to refresh, logout
                self._delete_auth_yaml()

        if self.client_secret:
            # We should get a new token
            return self.login_with_client_credentials()

        return None

    def login_with_client_credentials(self) -> t.Optional[str]:
        try:
            self.session.fetch_token(
                self.token_url,
                grant_type="client_credentials",
            )
            return self._create_token_info(self.session.token)["id_token"]
        except Exception:
            raise ValueError(
                "Error logging in with client credentials from sqlmesh. Please make sure that the TCLOUD_CLIENT_ID and TCLOUD_CLIENT_SECRET environment variables are set to the right values."
            )

    def refresh_token(self) -> t.Optional[str]:
        # Can we use client credentials?
        if self.client_secret:
            return self.login_with_client_credentials()

        if not self.token_info:
            self.logger.error("Not currently authenticated")
            return None

        current_refresh_token = self.token_info["refresh_token"]

        if not current_refresh_token:
            self.logger.error("Refresh token not available")
            return None

        self.logger.info("Refreshing authentication token")
        self.session.refresh_token(
            self.token_url, refresh_token=current_refresh_token, scope=self.token_info["scope"]
        )

        return self._create_token_info(self.session.token)["id_token"]

    def _create_token_info(self, token: t.Dict) -> t.Dict:
        self.token_info = {
            "scope": token["scope"],
            "token_type": token["token_type"],
            "expires_at": token["expires_at"],
            "access_token": token["access_token"],
            "id_token": token["id_token"],
        }

        if "refresh_token" in token:
            self.token_info["refresh_token"] = token["refresh_token"]

        self._save_auth_yaml(self.token_info)

        return self.token_info


def tcloud_sso(
    token_url: str = TOKEN_URL,
    client_id: str = CLIENT_ID,
    scope: str = SCOPE,
    auth_yaml_path: Path = TCLOUD_PATH,
    client_secret: t.Optional[str] = CLIENT_SECRET,
    logger: t.Optional[logging.Logger] = None,
) -> SSOAuth:
    return SSOAuth(
        token_url=token_url,
        client_id=client_id,
        scope=scope,
        auth_yaml_path=auth_yaml_path,
        client_secret=client_secret,
        logger=logger,
    )


class SSORequestAuth(Auth):
    def __init__(self, id_token: str) -> None:
        self.id_token = id_token

    def auth_flow(self, request: Request) -> t.Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.id_token}"
        yield request


UNAUTHENTICATED_MESSAGE = 'You are not authenticated. Please either specify a token in your project config, or run "tcloud auth login" if using Tobiko Cloud single sign on.'


class AuthHttpClient(PublicHttpClient):
    """
    This client retries on authentication failures using the TCloud token if available
    """

    def __init__(self, sso: t.Optional[SSOAuth] = None, *args: t.Any, **kwargs: t.Any):
        self.sso = sso or tcloud_sso()
        super().__init__(*args, **kwargs)

    def _call(self, *args: t.Any, **kwargs: t.Any) -> Response:
        old_auth = self._client.auth
        has_auth = old_auth or ("headers" in kwargs and "Authorization" in kwargs["headers"])

        if self.sso.client_secret or not has_auth:
            # Since we don't have a token configured, let's see if we already
            # have a token, if so use it
            id_token = self.sso.id_token()
            if id_token:
                self._client.auth = SSORequestAuth(id_token)

        try:
            response = super()._call(*args, **kwargs)
            return response
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPStatusError(
                    UNAUTHENTICATED_MESSAGE, request=e.request, response=e.response
                )
            raise e
        except self.error_class as e:
            if e.status_code == 401:
                raise self.error_class(UNAUTHENTICATED_MESSAGE, status_code=401)
            raise e
        finally:
            self._client.auth = old_auth
