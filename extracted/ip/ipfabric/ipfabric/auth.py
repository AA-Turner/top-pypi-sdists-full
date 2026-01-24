import logging
import random
import re
import sys
from datetime import datetime, timezone
from importlib import metadata
from time import sleep
from typing import Optional, Union, Any, Type, Literal
from urllib.parse import urlparse, urljoin, ParseResult

import jwt
from niquests import (
    Session,
    Request,
    Response,
    PreparedRequest,
    RetryConfiguration,
    TimeoutConfiguration,
    LifeCycleHook,
)

# See https://github.com/jawah/niquests/issues/324 for the PathLike import
from niquests.typing import TLSVerifyType, TimeoutType, ProxyType, TLSClientCertType, PathLike  # noqa: F401
from niquests.auth import AuthBase
from niquests.cookies import extract_cookies_to_jar
from niquests.exceptions import RetryError, HTTPError
from packaging.version import Version
from pydantic import field_validator, Field, AliasChoices, PrivateAttr, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, InitSettingsSource

from ipfabric.tools.shared import raise_for_status, valid_snapshot

logger = logging.getLogger("ipfabric")

RE_VERSION = re.compile(r"v?(\d(\.\d*)?)")


def log_request(request: PreparedRequest):
    # TODO: Figure out why these don't print
    logger.debug(f"Request event hook: {request.method} {request.url} - Waiting for response")


def log_response(response: Response):
    request = response.request
    logger.debug(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")


class RateLimiter(AuthBase):
    def __init__(self, api_version: str = None):
        self.os_api_version = api_version

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Add the rate limit handler to the request."""
        if self.rate_limit not in r.hooks["response"]:
            r.register_hook("response", self.rate_limit)
        if self.deprecated not in r.hooks["response"]:
            r.register_hook("response", self.deprecated)
        return r

    def deprecated(self, response: Response):
        if response.headers.get("deprecation", False) == "true":
            path = urlparse(response.url).path
            sunset = response.headers.get("sunset", None)
            if path.split("/")[2] == self.os_api_version:
                msg = f"API endpoint '{path}' has deprecation header set and will be removed in a future release."
                msg += f" Sunset date is {sunset}." if sunset else ""
                logger.warning(msg)
            else:
                # TODO: Change to new versioning scheme.
                logger.info(
                    f"API endpoint '{path}' is using older API version, current IP Fabric version is {self.os_api_version}."
                )

    @staticmethod
    def send_prepared_request(response: Response, prep: PreparedRequest, **kwargs) -> Response:
        _r = response.connection.send(prep, **kwargs)
        _r.history = [*response.history, response]
        _r.request = prep
        return _r

    def prepare_and_send(self, response: Response, **kwargs) -> Response:
        response.close()
        prep = response.request.copy()
        extract_cookies_to_jar(prep._cookies, response.request, response.raw)
        prep.prepare_cookies(prep._cookies)
        return self.send_prepared_request(response, prep, **kwargs)

    def rate_limit(self, response: Response, **kwargs):
        if response.status_code != 429:
            return response
        retry = response.connection.max_retries

        reset = int(response.headers.get("X-RateLimit-Reset", 0))
        _ = retry.backoff_jitter * random.random()  # nosemgrep: bandit.B311
        wait = reset - int(datetime.now(timezone.utc).timestamp()) + _

        retries = len([_ for _ in response.history if _.status_code in retry.status_forcelist])
        if retries >= retry.status:
            raise RetryError("Max retry limit reached", response=response)
        if wait > 0:
            print(f"Rate Limit Reached. Waiting for {wait} seconds.")
            sleep(wait)
            _r = self.prepare_and_send(response, **kwargs)
            if _r.status_code == 429 and _r.headers.get("X-RateLimit-Remaining", None) == "0":
                self.rate_limit(_r, **kwargs)

            return _r
        return response


class JWTToken(RateLimiter):
    """Used for streamlit."""

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Add the token to the request headers."""
        super().__call__(r)
        if self.auth_flow not in r.hooks["response"]:
            r.register_hook("response", self.auth_flow)
        return r

    @staticmethod
    def auth_flow(response: Response) -> Response:
        if response.status_code == 401:
            logger.warning("Access Token has expired, please refresh IP Fabric or log in again.")
        return response


class TokenAuth(RateLimiter):
    def __init__(self, token: str, api_version: str = None) -> None:
        super().__init__(api_version)
        self._auth_header = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Add the token to the request headers."""
        super(TokenAuth, self).__call__(r)
        r.headers["X-API-Token"] = self._auth_header
        return r


class AccessToken(RateLimiter):
    def __init__(
        self,
        username: str,
        password: str,
        base_url: AnyUrl,
        api_version: str = None,
    ):
        super().__init__(api_version)
        self.base_url = base_url
        self.username = username
        self.password = password

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Add the token to the request headers."""
        super().__call__(r)
        if self.auth_flow not in r.hooks["response"]:
            r.register_hook("response", self.auth_flow)
        return r

    def auth_flow(self, response: Response, **kwargs) -> Response:
        if response.status_code == 401 and not response.request._cookies.get("accessToken"):
            return self.login(response, **kwargs)
        elif response.status_code == 401 and "API_EXPIRED_ACCESS_TOKEN" in response.text:
            return self.refresh(response, **kwargs)
        return response

    def login(self, response: Response, **kwargs) -> Response:
        response.close()
        auth_prep = Request(
            method="POST",
            url=urljoin(self.base_url, "auth/login"),
            json={"username": self.username, "password": self.password},
            headers={"Content-Type": "application/json"},
        ).prepare()
        auth = response.connection.send(auth_prep, **kwargs)
        if auth.status_code != 200:
            raise HTTPError("Failed to Authenticate", response=auth, request=auth_prep)

        prep = self.prepare_auth(auth, response)
        return self.send_prepared_request(response, prep, **kwargs)

    def refresh(self, response: Response, **kwargs) -> Response:
        # Use refreshToken in Cookies to get new accessToken & Response updates accessToken in shared CookieJar
        response.close()
        reauth_prep = Request(
            method="POST",
            url=urljoin(self.base_url, "/api/auth/token"),
            headers={"Content-Type": "application/json"},
        ).prepare()
        reauth = response.connection.send(reauth_prep, **kwargs)
        if reauth.status_code != 200:
            raise HTTPError("Failed to Reauthenticate", response=reauth, request=reauth_prep)
        prep = self.prepare_auth(reauth, response)
        return self.send_prepared_request(response, prep, **kwargs)

    @staticmethod
    def prepare_auth(auth: Response, response: Response) -> PreparedRequest:
        auth.close()
        response.history.append(auth)
        prep = response.request.copy()
        extract_cookies_to_jar(prep._cookies, auth.request, auth.raw)
        prep.prepare_cookies(prep._cookies)
        return prep


class MyInitSettingsSource(InitSettingsSource):
    def __init__(self, settings_cls, init_kwargs: dict[str, Any]):
        timeout = init_kwargs.pop("timeout", "DEFAULT")
        init_kwargs = {k: v for k, v in init_kwargs.items() if v is not None}
        if timeout != "DEFAULT":
            init_kwargs["timeout"] = float(timeout) if isinstance(timeout, str) else timeout
        super().__init__(settings_cls, init_kwargs)


class Setup(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ipf_", extra="allow")
    base_url: AnyUrl = Field(None, validation_alias=AliasChoices("base_url", "ipf_url"))
    api_version: Optional[Union[int, float, str]] = Field(
        None, validation_alias=AliasChoices("api_version", "ipf_version")
    )
    auth: Optional[Any] = Field(None, alias="auth", exclude=True)
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    snapshot_id: Union[str, None] = Field("$last", validation_alias=AliasChoices("snapshot_id", "ipf_snapshot"))
    nvd_api_key: Optional[str] = Field(None, alias="nvd_api_key")

    verify: TLSVerifyType = True
    timeout: Union[None, TimeoutType, Literal["DEFAULT"]] = TimeoutConfiguration(connect=5.0, read=5.0)
    proxy: Optional[ProxyType] = None
    cert: Optional[TLSClientCertType] = None
    http2: bool = True
    event_hooks: Optional[dict[str, list[LifeCycleHook]]] = Field(default_factory=dict)
    retry_config: Optional[RetryConfiguration] = Field(None, description="Retries configuration for niquests client.")
    debug: bool = False
    psql: bool = False

    _client: Optional[Session] = PrivateAttr(None)
    _os_version: Optional[str] = PrivateAttr(None)
    _os_api_version: Optional[str] = PrivateAttr(None)
    _auth_type: Optional[str] = PrivateAttr(None)

    @property
    def client(self) -> Session:
        return self._client

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            MyInitSettingsSource(settings_cls, init_settings.init_kwargs),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

    def model_post_init(self, __context):
        self._client = Session(
            base_url=str(self.base_url),
            disable_http2=not self.http2,
            timeout=self.timeout,
            retries=self.retry_config,
        )

        self.client.verify = self.verify
        self.client.cert = self.cert
        self.client.proxies = self.proxy
        self.client.headers["User-Agent"] = (
            f'python-ipfabric-sdk/{metadata.version("ipfabric")} (Python {sys.version.split(" ")[0]})'
        )
        for k, v in self.event_hooks.items():
            self.client.hooks[k].extend(v)
        if self.debug:
            self.client.hooks["pre_request"].append(log_request)
            self.client.hooks["response"].append(log_response)

        if not (self.auth or self.token) and not (self.username and self.password):
            raise RuntimeError("IP Fabric Authentication not provided.")
        self.api_version, self._os_version, self._os_api_version = self.check_version(self.api_version)
        if Version(self._os_api_version[1:]) < Version("7.5"):
            self.base_url = urljoin(self.base_url, f"api/{self.api_version}/")
        else:
            self.psql = True
            self.base_url = urljoin(self.base_url, "api/")
        self.client.base_url = self.base_url
        self._verify_auth()

    def _verify_auth(self):
        if self.auth:
            self.client.auth = self._get_auth_from_auth()
        elif self.token:
            self.client.auth = self._check_jwt(self.token)
        elif self.username and self.password:
            self.client.auth = self._get_access_token_auth(self.username, self.password)

    def _check_jwt(self, token):
        try:
            jwt.decode(token, options={"verify_signature": False})  # NOSONAR
            self.client.cookies.set("accessToken", token)
            self._auth_type = "JWT_AUTH"
            return JWTToken(api_version=self._os_api_version)
        except jwt.exceptions.DecodeError:
            self._auth_type = "API_TOKEN_AUTH"
            return TokenAuth(token, api_version=self._os_api_version)

    def _get_auth_from_auth(self) -> Any:
        """Separate auth handling logic"""
        if isinstance(self.auth, str):
            return self._check_jwt(self.auth)
        elif isinstance(self.auth, tuple):
            return self._get_access_token_auth(self.auth[0], self.auth[1])
        self._auth_type = type(self.client.auth)
        return self.auth

    def _get_access_token_auth(self, username: str, password: str) -> AccessToken:
        """Separate auth handling logic"""
        self._auth_type = "USER_PASS_ACCESS_TOKEN"
        return AccessToken(
            username,
            password,
            self.base_url,
            api_version=self._os_api_version,
        )

    @property
    def update_attrs(self) -> dict:
        return {
            "base_url": self.base_url,
            "api_version": self.api_version,
            "auth": self._auth_type,
            "timeout": self.client.timeout,
            "_os_version": self._os_version,
            "_os_api_version": self._os_api_version,
            "debug": self.debug,
            "_client": self.client,
            "verify": self.verify,
            "proxy": self.proxy,
            "http2": self.http2,
            "nvd_api_key": self.nvd_api_key,
            "_psql": self.psql,
        }

    def check_version(self, custom_api_version) -> tuple:
        """Checks API Version and returns the version to use in the URL and the OS Version

        Returns:
            api_version, os_version
        """
        cfg_version = Version(custom_api_version)
        api_version = f"v{cfg_version.major}.{cfg_version.minor}"

        resp = raise_for_status(self.client.get("/api/version")).json()
        os_api_version = Version(resp["apiVersion"])

        if os_api_version.major != cfg_version.major:
            raise RuntimeError(
                f"OS Major Version `{os_api_version.major}` does not match SDK Major Version `{cfg_version.major}`."
            )

        if cfg_version.minor > os_api_version.minor:
            logger.warning(
                f"Specified SDK Version `{api_version}` is greater than "
                f"OS API Version `{os_api_version}`, using OS Version."
            )
            api_version = f"v{os_api_version.base_version}"

        return api_version, resp["releaseVersion"], resp["apiVersion"]

    @field_validator("api_version")
    @classmethod
    def _valid_version(cls, v: Union[None, int, float, str]) -> Union[None, str]:
        if not v:
            return metadata.version("ipfabric")
        re_version = RE_VERSION.match(str(v))
        if not re_version:
            raise ValueError(f"IPF_VERSION ({v}) is not valid, must be like `v#` or `v#.#`.")
        elif re_version and re_version.group(2):
            return "v" + RE_VERSION.match(str(v)).group(1)
        else:
            return "v" + RE_VERSION.match(str(v)).group(1) + ".0"

    @field_validator("base_url")
    @classmethod
    def _convert_url(cls, v: Union[ParseResult, str]) -> str:
        if isinstance(v, str):
            v = urlparse(v)
        return str(v)

    @field_validator("snapshot_id")
    @classmethod
    def _valid_snapshot(cls, v: Union[None, str]) -> str:
        return valid_snapshot(v, init=True)

    @field_validator("verify")
    @classmethod
    def _verify(cls, v: Union[bool, int, str]) -> Union[bool, str]:
        if isinstance(v, bool):
            return v
        elif isinstance(v, int):
            return bool(v)
        elif v.lower() in {"0", "off", "f", "false", "n", "no", "1", "on", "t", "true", "y", "yes"}:
            return False if v.lower() in {0, "0", "off", "f", "false", "n", "no"} else True
        else:
            return v

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Needed for context"""
        pass
