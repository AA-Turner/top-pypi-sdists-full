import datetime
import json
import typing as t
from hashlib import blake2b
from urllib.parse import urljoin

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from pydantic import BaseModel, ValidationError

from taktile_auth.exceptions import InvalidAuthException, TaktileAuthException
from taktile_auth.schemas.session import SessionState
from taktile_auth.schemas.token import TaktileIdToken
from taktile_auth.settings import settings
from taktile_auth.utils.cache import Cache

ALGORITHM = "RS256"
PUBLIC_KEY_CACHE_KEY = "_jwks"


def _get_auth_server_url(env: str) -> str:
    if env == "local":
        return "http://taktile-api.local.taktile.com:8000"
    if env == "prod":
        return "https://taktile-api.taktile.com"
    return f"https://taktile-api.{env}.taktile.com"


class AuthClient:
    class JWTResponseSuccess(BaseModel):
        token: str

    class JWTResponseAllowedFailure(BaseModel):
        """A failure which allows us to use the cache"""

        exception: t.Any

    class JWTResponseForbiddenFailure(BaseModel):
        """A failure which doesn't allow us to use the cache"""

        exception: t.Any

    class CacheResponse(BaseModel):
        """Response from the cache"""

        token: str
        is_in_speedup_window: bool

    def __init__(
        self,
        url: str = _get_auth_server_url(settings.ENV),
        cache: t.Optional[Cache] = None,
        cache_speedup_time: datetime.timedelta = datetime.timedelta(
            minutes=settings.CACHE_SPEEDUP_TIME_MINUTES
        ),
        cache_fallback_time: datetime.timedelta = datetime.timedelta(
            minutes=settings.CACHE_FALLBACK_TIME_MINUTES
        ),
        salt: t.Optional[str] = None,
    ) -> None:
        self.public_key_url = urljoin(url, ".well-known/jwks.json")
        self.access_token_url = urljoin(url, "api/v1/login/access-token")
        self._cache = cache
        self._cache_speedup_time = cache_speedup_time
        self._cache_fallback_time = cache_fallback_time
        self._salt = salt

    def _extract_key(self, jwk: t.Any, kid: str) -> t.Any:
        for k in jwk["keys"]:
            if k["kid"] == kid:
                return RSAAlgorithm.from_jwk(k)
        raise InvalidAuthException("invalid-public-key")

    def get_public_key(
        self,
        *,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Any:
        jwks: t.Any = None

        if key is not None:
            return self._extract_key(json.loads(key), kid)

        if self._cache is not None:
            cached = self._cache.get(PUBLIC_KEY_CACHE_KEY)
            if cached:
                timestamp, jwks = json.loads(cached)
                insert_time = datetime.datetime.fromtimestamp(timestamp)
                if (
                    datetime.datetime.utcnow()
                    < insert_time
                    + datetime.timedelta(
                        minutes=settings.CACHE_PUBLIC_KEY_SPEEDUP_TIME_MINUTES
                    )
                ):
                    return self._extract_key(jwks, kid)

        try:
            response = requests.get(
                self.public_key_url,
                timeout=settings.AUTH_SERVER_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            if jwks is not None:
                return self._extract_key(jwks, kid)
            raise TaktileAuthException("No public key found") from None
        else:
            jwks = response.json()
            if self._cache is not None:
                now = int(
                    datetime.datetime.timestamp(datetime.datetime.utcnow())
                )
                expires = datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=settings.CACHE_PUBLIC_KEY_FALLBACK_TIME_MINUTES
                )
                self._cache.put(
                    PUBLIC_KEY_CACHE_KEY,
                    json.dumps((now, jwks)),
                    time_to_live=int(datetime.datetime.timestamp(expires)),
                )
            return self._extract_key(jwks, kid)

    def decode_id_token(
        self,
        *,
        token: t.Optional[str] = None,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> TaktileIdToken:
        if not token:
            raise InvalidAuthException("no-auth-provided")
        try:
            public_key = self.get_public_key(key=key, kid=kid)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=[ALGORITHM],
                audience=settings.ENV,
            )
            return TaktileIdToken(**payload)
        except jwt.ExpiredSignatureError as exc:
            raise InvalidAuthException("signature-expired") from exc
        except (jwt.PyJWTError, ValidationError) as exc:
            raise InvalidAuthException("could-not-validate") from exc

    def get_access(
        self,
        *,
        session_state: SessionState,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Tuple[TaktileIdToken, SessionState]:
        if not session_state.api_key and not session_state.jwt:
            raise InvalidAuthException("no-auth-proved")

        if session_state.jwt:
            return (
                self.decode_id_token(
                    token=session_state.jwt, key=key, kid=kid
                ),
                session_state,
            )

        if cache_response := self._get_from_cache(
            session_state=session_state, key=key
        ):
            session_state.jwt = cache_response.token
            should_refresh = not cache_response.is_in_speedup_window
        else:
            should_refresh = False

        if not session_state.jwt or should_refresh:
            tapi_response = self._refresh_jwt(session_state=session_state)

            if isinstance(tapi_response, AuthClient.JWTResponseSuccess):
                session_state.jwt = tapi_response.token
                if self._cache:
                    expires = (
                        datetime.datetime.utcnow() + self._cache_fallback_time
                    )
                    self._cache.put(
                        self._get_cache_key(str(session_state.api_key)),
                        tapi_response.token,
                        time_to_live=int(datetime.datetime.timestamp(expires)),
                    )
            elif isinstance(
                tapi_response, AuthClient.JWTResponseAllowedFailure
            ):
                if session_state.jwt:
                    return (
                        self.decode_id_token(
                            token=session_state.jwt, key=key, kid=kid
                        ),
                        session_state,
                    )
                else:
                    raise InvalidAuthException(
                        "Invalid authentication credentials provided "
                        "(no cached token). Check again your credentials."
                    ) from tapi_response.exception
            elif isinstance(
                tapi_response, AuthClient.JWTResponseForbiddenFailure
            ):
                raise InvalidAuthException(
                    "Invalid authentication credentials provided. "
                    "Check again your credentials."
                ) from tapi_response.exception

        return (
            self.decode_id_token(token=session_state.jwt, key=key, kid=kid),
            session_state,
        )

    def _get_from_cache(
        self, *, session_state: SessionState, key: t.Optional[str]
    ) -> t.Optional[CacheResponse]:
        """
        Take a look at PEP 76: Auth Cache Router for details on this logic
        """

        if self._cache is None or session_state.api_key is None:
            return None

        cached_jwt = self._cache.get(
            self._get_cache_key(str(session_state.api_key))
        )

        if not cached_jwt:
            return None

        try:
            token = self.decode_id_token(token=cached_jwt, key=key)
        except InvalidAuthException:
            self._cache.delete(self._get_cache_key(str(session_state.api_key)))
            return None

        issue_time = datetime.datetime.fromtimestamp(float(token.iat))

        is_in_speedup_window = (
            datetime.datetime.utcnow() < issue_time + self._cache_speedup_time
        )

        return AuthClient.CacheResponse(
            token=cached_jwt, is_in_speedup_window=is_in_speedup_window
        )

    def fetch_jwt(
        self, *, session_state: SessionState, expires_seconds: int
    ) -> t.Union[
        JWTResponseSuccess,
        JWTResponseAllowedFailure,
        JWTResponseForbiddenFailure,
    ]:
        """
        Take a look at PEP 76: Auth Cache Router for details on this logic
        """
        try:
            res = requests.post(
                self.access_token_url,
                headers=session_state.to_auth_headers(),
                timeout=settings.AUTH_SERVER_TIMEOUT_SECONDS,
                params={"expires_seconds": expires_seconds},
            )
            res.raise_for_status()
            id_token = res.json()["id_token"]
            return AuthClient.JWTResponseSuccess(token=id_token)

        except requests.exceptions.Timeout as exc:
            return AuthClient.JWTResponseAllowedFailure(exception=exc)
        except requests.exceptions.HTTPError as exc:
            if (
                exc.response.status_code in (404, 429, 499)
                or exc.response.status_code >= 500
            ):
                return AuthClient.JWTResponseAllowedFailure(exception=exc)
            return AuthClient.JWTResponseForbiddenFailure(exception=exc)
        except Exception as exc:
            return AuthClient.JWTResponseForbiddenFailure(exception=exc)

    def _refresh_jwt(self, *, session_state: SessionState) -> t.Union[
        JWTResponseSuccess,
        JWTResponseAllowedFailure,
        JWTResponseForbiddenFailure,
    ]:
        return self.fetch_jwt(
            session_state=session_state,
            expires_seconds=int(self._cache_fallback_time.total_seconds()),
        )

    def _get_cache_key(self, key: str) -> str:
        salt = self._salt if self._salt else ""
        return blake2b(f"{salt}{key}".encode()).hexdigest()
