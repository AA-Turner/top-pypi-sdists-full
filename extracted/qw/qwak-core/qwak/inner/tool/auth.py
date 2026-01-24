import warnings
from filelock import FileLock

from qwak.inner.di_configuration.session import Session
from abc import ABC, abstractmethod
from typing import Optional

warnings.filterwarnings(action="ignore", module=".*jose.*")

import configparser  # noqa E402
import json  # noqa E402

import requests  # noqa E402
from jose import jwt  # noqa E402
from qwak.exceptions import QwakLoginException  # noqa E402
from qwak.inner.const import QwakConstants  # noqa E402


class BaseAuthClient(ABC):
    @abstractmethod
    def get_token(self) -> Optional[str]:
        pass

    @abstractmethod
    def login(self) -> None:
        pass

    @abstractmethod
    def get_base_url(self) -> str:
        """
        Returns the base URL for the authentication service.
        """
        return ""


class Auth0ClientBase(BaseAuthClient):
    _TOKENS_FIELD = "TOKENS"

    def __init__(
        self,
        api_key=None,
        auth_file=QwakConstants.QWAK_AUTHORIZATION_FILE,
        audience=QwakConstants.TOKEN_AUDIENCE,
    ):
        self._auth_file = auth_file
        self._config = configparser.ConfigParser()
        self._environment = Session().get_environment()
        self.jwks = requests.get(QwakConstants.AUTH0_JWKS_URI, timeout=60).json()
        self.token = None
        self.audience = audience
        self.api_key = api_key

    def get_base_url(self) -> str:
        return QwakConstants.QWAK_APP_URL

    # Returns Non if token is expired
    def get_token(self):
        if self._environment != Session().get_environment():
            self.token = None
            self.api_key = None
            self._environment = Session().get_environment()
        try:
            if not self.token:
                self._config.read(self._auth_file)
                self.token = json.loads(
                    self._config.get(
                        section=self._environment, option=self._TOKENS_FIELD
                    )
                )

            # Test that token isn't expired
            self.get_claims()
            return self.token
        except configparser.NoSectionError:
            self.login()
            return self.token
        except jwt.ExpiredSignatureError:
            self.login()
            return self.token

    def login(self):
        from qwak.clients.administration import AuthenticationClient

        if not self.api_key:
            from qwak.inner.di_configuration import UserAccountConfiguration

            user_account = UserAccountConfiguration().get_user_config()
            self.api_key = user_account.api_key

        self.token = AuthenticationClient().authenticate(self.api_key).access_token

        from pathlib import Path

        Path(self._auth_file).parent.mkdir(parents=True, exist_ok=True)
        self._config.read(self._auth_file)

        lock_path = f"{self._auth_file}.lock"  # Create a lock file
        with FileLock(lock_path):  # Use file lock
            with open(self._auth_file, "w") as configfile:
                self._config[self._environment] = {
                    self._TOKENS_FIELD: json.dumps(self.token)
                }

                self._config.write(configfile)

    def get_claims(self):
        try:
            if not self.token:
                self.get_token()
            unverified_header = jwt.get_unverified_header(self.token)
            rsa_key = {}
            for key in self.jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
            if rsa_key:
                payload = jwt.decode(
                    self.token,
                    rsa_key,
                    algorithms=QwakConstants.AUTH0_ALGORITHMS,
                    audience=self.audience,
                )
                claims = {}
                token_prefix = QwakConstants.TOKEN_AUDIENCE
                claims["exp"] = payload["exp"]
                for key in payload:
                    if key.startswith(token_prefix):
                        claims[key.split(token_prefix)[1]] = payload[key]
                return claims
            raise QwakLoginException()
        except jwt.ExpiredSignatureError as e:
            raise e
        except Exception:
            raise QwakLoginException()
