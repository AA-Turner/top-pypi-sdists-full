import logging
import re
import sys
from datetime import datetime, timezone
from http.cookiejar import CookieJar
from importlib import metadata
from ssl import SSLContext
from time import sleep
from typing import Optional, Union, Generator, Any, Type, Literal, Mapping

import jwt
from httpx import Client, BaseTransport, URL, Request, Response, Auth, Timeout, post
from httpx._client import EventHook
from httpx._types import CertTypes
from packaging.version import Version
from pydantic import field_validator, Field, AliasChoices, PrivateAttr
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, InitSettingsSource

from ipfabric.tools.shared import raise_for_status, valid_snapshot, ProxyTypes, TimeoutTypes

logger = logging.getLogger("ipfabric")

RE_VERSION = re.compile(r"v?(\d(\.\d*)?)")


def log_request(request: Request):
    logger.debug(f"Request event hook: {request.method} {request.url} - Waiting for response")


def log_response(response: Response):
    request = response.request
    logger.debug(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")


class RateLimiter:
    def __init__(self, api_version: str = None):
        self.os_api_version = api_version

    def deprecated(self, response: Response):
        if response.headers.get("deprecation", False) == "true":
            version = response.url.path.split("/")[2]
            if version == self.os_api_version:
                logger.warning(
                    f"API endpoint '{response.url.path}' has deprecation header set and will be removed in a future release."
                )
            else:
                logger.info(
                    f"API endpoint '{response.url.path}' is using older API version, "
                    f"current IP Fabric version is {self.os_api_version}."
                )

    @staticmethod
    def rate_limit(response: Response, request: Request):
        reset = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = reset - int(datetime.now(timezone.utc).timestamp()) + 0.5
        if wait > 0:
            logger.warning(f"Rate Limit Reached. Waiting for {wait} seconds.")
            sleep(wait)
        return request


class JWTToken(Auth, RateLimiter):
    """Used for streamlit."""

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        response = yield request
        self.deprecated(response)

        if response.status_code == 429 and response.headers.get("X-RateLimit-Remaining", None) == "0":
            yield self.rate_limit(response, request)
        if response.status_code == 401:
            logger.warning("Access Token has expired, please refresh IP Fabric or log in again.")
        return response


class TokenAuth(Auth, RateLimiter):
    def __init__(self, token: str, api_version: str = None) -> None:
        super().__init__(api_version)
        self._auth_header = token

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["X-API-Token"] = self._auth_header

        response = yield request
        self.deprecated(response)
        if response.status_code == 429 and response.headers.get("X-RateLimit-Remaining", None) == "0":
            yield self.rate_limit(response, request)
        return response


class AccessToken(Auth, RateLimiter):
    def __init__(
        self,
        cookie_jar: CookieJar,
        username: str,
        password: str,
        base_url: URL,
        verify: Optional[Union[SSLContext, str, bool]],
        api_version: str = None,
    ):
        super().__init__(api_version)
        self.cookie_jar = cookie_jar
        self._login(username, password, base_url, verify)

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        response = yield request
        self.deprecated(response)

        if response.status_code == 429 and response.headers.get("X-RateLimit-Remaining", None) == "0":
            yield self.rate_limit(response, request)
        if response.status_code == 401:
            response.read()
            if "API_EXPIRED_ACCESS_TOKEN" in response.text:
                # Use refreshToken in Cookies to get new accessToken & Response updates accessToken in shared CookieJar
                resp = raise_for_status(post(response.url.join("/api/auth/token"), cookies=self.cookie_jar))
                request.headers["Cookie"] = "accessToken=" + resp.cookies["accessToken"]  # Update request
                yield request
        return response

    def _login(
        self, username: str, password: str, base_url: URL, verify: Optional[Union[SSLContext, str, bool]]
    ) -> None:
        raise_for_status(
            post(
                base_url.join("auth/login"),
                json=dict(username=username, password=password),
                cookies=self.cookie_jar,
                verify=verify,
            )
        )


class MyInitSettingsSource(InitSettingsSource):
    def __init__(self, settings_cls, init_kwargs: dict[str, Any]):
        timeout = init_kwargs.pop("timeout", "DEFAULT")
        init_kwargs = {k: v for k, v in init_kwargs.items() if v is not None}
        if timeout != "DEFAULT":
            init_kwargs["timeout"] = timeout
        super().__init__(settings_cls, init_kwargs)


class Setup(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ipf_", extra="allow")
    base_url: Union[str, URL] = Field(None, validation_alias=AliasChoices("base_url", "ipf_url"))
    api_version: Optional[Union[int, float, str]] = Field(
        None, validation_alias=AliasChoices("api_version", "ipf_version")
    )
    auth: Optional[Any] = Field(None, alias="auth", exclude=True)
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    snapshot_id: Union[str, None] = Field("$last", validation_alias=AliasChoices("snapshot_id", "ipf_snapshot"))
    verify: Union[SSLContext, bool, str] = True
    timeout: Union[TimeoutTypes, Literal["DEFAULT"]] = Timeout(timeout=5.0)
    nvd_api_key: Optional[str] = Field(None, alias="nvd_api_key")
    debug: bool = False
    http2: bool = True
    proxy: Optional[Union[ProxyTypes, None]] = None
    mounts: Optional[Mapping[str, Optional[BaseTransport]]] = None
    cert: Optional[Union[CertTypes, None]] = None
    event_hooks: Optional[Mapping[str, list[EventHook]]] = None
    _cookie_jar: CookieJar = PrivateAttr(default_factory=CookieJar)
    client: Optional[Client] = Field(None, exclude=True)
    os_version: Optional[str] = Field(None)
    _os_api_version: Optional[str] = PrivateAttr(None)
    _auth_type: Optional[str] = PrivateAttr(None)

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
        event_hooks = {"request": [log_request], "response": [log_response]} if self.debug else self.event_hooks
        self.client = Client(
            base_url=self.base_url,
            cookies=self._cookie_jar,
            http2=self.http2,
            verify=self.verify,
            timeout=self.timeout,
            headers={
                "User-Agent": f'python-ipfabric-sdk/{metadata.version("ipfabric")} (Python {sys.version.split(" ")[0]})'
            },
            event_hooks=event_hooks,
            proxy=self.proxy,
            mounts=self.mounts,
            cert=self.cert,
        )
        if not (self.auth or self.token) and not (self.username and self.password):
            raise RuntimeError("IP Fabric Authentication not provided.")
        self.api_version, self.os_version, self._os_api_version = self.check_version(self.api_version)
        self.base_url = self.base_url.join(f"api/{self.api_version}/")
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

    def _get_auth_from_auth(self) -> Auth:
        """Separate auth handling logic"""
        if isinstance(self.auth, str):
            return self._check_jwt(self.auth)
        elif isinstance(self.auth, tuple):
            return self._get_access_token_auth(self.auth[0], self.auth[1])
        self._auth_type = type(self.client.auth)
        return self.auth

    def _get_access_token_auth(self, username: str, password: str) -> Auth:
        """Separate auth handling logic"""
        self._auth_type = "USER_PASS_ACCESS_TOKEN"
        return AccessToken(
            self._cookie_jar,
            username,
            password,
            self.base_url,
            self.verify,
            api_version=self._os_api_version,
        )

    @property
    def update_attrs(self) -> dict:
        return {
            "base_url": self.base_url,
            "api_version": self.api_version,
            "auth": self._auth_type,
            "timeout": self.client.timeout,
            "_os_version": self.os_version,
            "_os_api_version": self._os_api_version,
            "debug": self.debug,
            "_client": self.client,
            "verify": self.verify,
            "proxy": self.proxy,
            "mounts": self.mounts,
            "cert": self.cert,
            "event_hooks": self.event_hooks,
            "http2": self.http2,
            "nvd_api_key": self.nvd_api_key,
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
    def _convert_url(cls, v: Union[URL, str]) -> URL:
        if isinstance(v, str):
            v = URL(v)
        return v

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
