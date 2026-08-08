import datetime
import json
import time
import typing as t
from hashlib import blake2b
from urllib.parse import urljoin

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from pydantic import BaseModel, ValidationError

from taktile_auth._logging import get_logger
from taktile_auth._metrics import emit_metric
from taktile_auth.counter import SharedCounter
from taktile_auth.exceptions import InvalidAuthException, TaktileAuthException
from taktile_auth.recursion import RecursionGate, RecursionMode
from taktile_auth.schemas.session import SessionState, parse_session_prefix
from taktile_auth.schemas.token import TaktileIdToken
from taktile_auth.settings import settings
from taktile_auth.utils.cache import Cache

logger = get_logger()

ALGORITHM = "RS256"
PUBLIC_KEY_CACHE_KEY = "_jwks"
PUBLIC_KEY_REFRESH_MARKER = "_refresh:_jwks"
REFRESH_MARKER_PREFIX = "_refresh:"


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
        cache_speedup_time: datetime.timedelta = datetime.timedelta(minutes=settings.CACHE_SPEEDUP_TIME_MINUTES),
        cache_fallback_time: datetime.timedelta = datetime.timedelta(minutes=settings.CACHE_FALLBACK_TIME_MINUTES),
        salt: t.Optional[str] = None,
        cert: t.Optional[t.Tuple[str, str]] = None,
        # PEP-295 recursion accounting. Explicit ``recursion_check_enabled``
        # gates the feature; defaults to off. When enabled, a
        # ``recursion_counter`` is mandatory — the gate has nowhere to
        # accumulate hops otherwise. ``recursion_mode`` controls whether
        # threshold crossings raise (``error``) or just emit metrics
        # (``warn``).
        recursion_check_enabled: bool = False,
        recursion_counter: t.Optional[SharedCounter] = None,
        recursion_mode: RecursionMode = settings.RECURSION_MODE,
        # PEP-76 scope narrowing: when set, every mint is downscoped to
        # this org/workspace. Cache keys do NOT include the scope, so a
        # scoped instance needs its own cache (realm) — never share one
        # across scopes.
        organization_id: t.Optional[str] = None,
        workspace_id: t.Optional[str] = None,
        # RFC 8707 resource indicator. When set, every mint asks for this
        # audience; like the scope above, cache keys do not include it.
        resource: t.Optional[str] = None,
        # Audiences this client will accept when validating a token. Matching
        # is exact: a value that is a prefix of another grants nothing.
        audiences: t.Optional[t.List[str]] = None,
    ) -> None:
        self.public_key_url = urljoin(url, ".well-known/jwks.json")
        self.access_token_url = urljoin(url, "api/v1/login/access-token")
        self.cert = cert
        self._cache = cache
        self._cache_speedup_time = cache_speedup_time
        self._cache_fallback_time = cache_fallback_time
        self._salt = salt
        self._organization_id = organization_id
        self._workspace_id = workspace_id
        self._resource = resource
        self._audiences = list(audiences) if audiences else [settings.ENV]
        self._recursion_gate: t.Optional[RecursionGate] = None

        if recursion_check_enabled and recursion_counter is None:
            # Miswired: feature flag flipped on but no counter to
            # accumulate hops in.
            logger.error(
                "recursion_check_enabled=True but no recursion_counter provided; PEP-295 hop counting disabled"
            )
        elif recursion_check_enabled:
            assert recursion_counter is not None  # narrows type for mypy
            self._recursion_gate = RecursionGate(counter=recursion_counter, mode=recursion_mode)

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
                if datetime.datetime.utcnow() < insert_time + datetime.timedelta(
                    minutes=settings.CACHE_PUBLIC_KEY_SPEEDUP_TIME_MINUTES
                ):
                    return self._extract_key(jwks, kid)

                # Past speedup window — use a marker to avoid stampeding
                try:
                    won_marker = self._cache.put_marker(
                        PUBLIC_KEY_REFRESH_MARKER,
                        ttl_seconds=settings.AUTH_SERVER_TIMEOUT_SECONDS,
                    )
                except Exception:
                    won_marker = True
                if not won_marker:
                    logger.info("Public key refresh already in progress, using cached key")
                    return self._extract_key(jwks, kid)
                logger.info(
                    "Public key cache stale, refreshing from %s",
                    self.public_key_url,
                )

        try:
            response = requests.get(
                self.public_key_url,
                timeout=settings.AUTH_SERVER_TIMEOUT_SECONDS,
                cert=self.cert,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            if jwks is not None:
                logger.warning(
                    "Failed to fetch public key from %s, using cached key",
                    self.public_key_url,
                )
                return self._extract_key(jwks, kid)
            raise TaktileAuthException("No public key found") from None
        else:
            jwks = response.json()
            if self._cache is not None:
                now = int(datetime.datetime.timestamp(datetime.datetime.utcnow()))
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
        # PEP-295: any wire-format prefix is opaque to JWT validation —
        # strip before handing the token to PyJWT so callers can pass the
        # raw header value transparently.
        _, inner_token = parse_session_prefix(token)
        try:
            public_key = self.get_public_key(key=key, kid=kid)
            payload = jwt.decode(
                inner_token,
                public_key,
                algorithms=[ALGORITHM],
                audience=self._audiences,
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
        weight: int = 1,
    ) -> t.Tuple[TaktileIdToken, SessionState]:
        if not session_state.api_key and not session_state.jwt:
            raise InvalidAuthException("no-auth-proved")

        method = "id_token" if session_state.jwt else "cache"
        t0 = time.perf_counter()
        success = True
        try:
            self._record_recursion_hop(session_state=session_state, weight=weight)

            if session_state.jwt:
                return (
                    self.decode_id_token(token=session_state.jwt, key=key, kid=kid),
                    session_state,
                )

            if cache_response := self._get_from_cache(session_state=session_state, key=key):
                session_state.jwt = cache_response.token
                should_refresh = not cache_response.is_in_speedup_window

                # If local cache is stale, consult backing store (DDB)
                # — another instance may have already refreshed.
                if should_refresh:
                    cache_response = self._get_from_cache(
                        session_state=session_state,
                        key=key,
                        skip_local_cache=True,
                    )
                    if cache_response:
                        session_state.jwt = cache_response.token
                        should_refresh = not cache_response.is_in_speedup_window
                    else:
                        # Another instance may have purged the entry — drop the local copy too.
                        session_state.jwt = None
            else:
                should_refresh = False

            # Avoid multiple concurrent workers refreshing the same token
            # simultaneously (stampede). We use a cache marker as a simple
            # lock: the first worker to set it wins and performs the refresh,
            # while others skip the refresh and keep using the current
            # (still valid) token a little past its speedup window.
            if should_refresh and self._cache and session_state.api_key:
                cache_key = self._get_cache_key(str(session_state.api_key))
                marker_key = f"{REFRESH_MARKER_PREFIX}{cache_key}"
                try:
                    won_marker = self._cache.put_marker(
                        marker_key,
                        ttl_seconds=settings.AUTH_SERVER_TIMEOUT_SECONDS,
                    )
                except Exception:
                    # Fall through if the cache doesn't support put_marker
                    won_marker = True

                if not won_marker:
                    logger.info("JWT refresh already in progress, using cached token")
                    should_refresh = False
                else:
                    logger.info("JWT cache stale, refreshing from taktile-api")

            if not session_state.jwt or should_refresh:
                tapi_response = self._refresh_jwt(session_state=session_state)

                if isinstance(tapi_response, AuthClient.JWTResponseSuccess):
                    method = "refresh"
                    session_state.jwt = tapi_response.token
                    if self._cache:
                        expires = datetime.datetime.utcnow() + self._cache_fallback_time
                        self._cache.put(
                            self._get_cache_key(str(session_state.api_key)),
                            tapi_response.token,
                            time_to_live=int(datetime.datetime.timestamp(expires)),
                        )
                elif isinstance(
                    tapi_response,
                    AuthClient.JWTResponseAllowedFailure,
                ):
                    if session_state.jwt:
                        return (
                            self.decode_id_token(
                                token=session_state.jwt,
                                key=key,
                                kid=kid,
                            ),
                            session_state,
                        )
                    else:
                        raise InvalidAuthException(
                            "Invalid authentication credentials"
                            " provided (no cached token). Check"
                            " again your credentials."
                        ) from tapi_response.exception
                elif isinstance(
                    tapi_response,
                    AuthClient.JWTResponseForbiddenFailure,
                ):
                    # Purge so an outage cannot revive a revoked key. HTTPError only:
                    # transport errors also land here and must keep the fallback.
                    if self._cache and isinstance(tapi_response.exception, requests.exceptions.HTTPError):
                        self._cache.delete(self._get_cache_key(str(session_state.api_key)))
                    raise InvalidAuthException(
                        "Invalid authentication credentials provided. Check again your credentials."
                    ) from tapi_response.exception

            return (
                self.decode_id_token(token=session_state.jwt, key=key, kid=kid),
                session_state,
            )
        except Exception:
            success = False
            raise
        finally:
            duration_ms = (time.perf_counter() - t0) * 1000
            emit_metric(
                "GetAccessDuration",
                duration_ms,
                {"Method": method, "Success": str(success)},
            )

    def _get_from_cache(
        self,
        *,
        session_state: SessionState,
        key: t.Optional[str],
        skip_local_cache: bool = False,
    ) -> t.Optional[CacheResponse]:
        """
        Take a look at PEP 76: Auth Cache Router for details on this logic
        """

        if self._cache is None or session_state.api_key is None:
            return None

        cache_key = self._get_cache_key(str(session_state.api_key))
        try:
            cached_jwt = self._cache.get(cache_key, skip_local_cache=skip_local_cache)
        except TypeError:
            logger.warning("Cache does not support skip_local_cache, falling back to local cache")
            cached_jwt = self._cache.get(cache_key)

        if not cached_jwt:
            return None

        try:
            token = self.decode_id_token(token=cached_jwt, key=key)
        except InvalidAuthException:
            self._cache.delete(cache_key)
            return None

        issue_time = datetime.datetime.fromtimestamp(float(token.iat))

        is_in_speedup_window = datetime.datetime.utcnow() < issue_time + self._cache_speedup_time

        return AuthClient.CacheResponse(token=cached_jwt, is_in_speedup_window=is_in_speedup_window)

    def fetch_jwt(
        self,
        *,
        session_state: SessionState,
        expires_seconds: int,
        organization_id: t.Optional[str] = None,
        workspace_id: t.Optional[str] = None,
        roles: t.Optional[t.Sequence[str]] = None,
        resource: t.Optional[str] = None,
    ) -> t.Union[
        JWTResponseSuccess,
        JWTResponseAllowedFailure,
        JWTResponseForbiddenFailure,
    ]:
        """
        Take a look at PEP 76: Auth Cache Router for details on this logic.

        ``organization_id`` / ``workspace_id`` / ``roles`` forward as
        query params to ``/access-token`` so the auth server mints a
        scope-narrowed JWT. ``roles`` is sent as a repeated query param
        (``?roles=a&roles=b``) and subsets the mint to the named roles.
        Omit all of them for an unscoped mint (backwards-compatible
        default).

        ``resource`` is the RFC 8707 resource indicator: the audience the
        minted token is for. An auth server that does not implement it
        ignores the param and mints its default audience.
        """
        # PEP-295 prefix is for *customer* hop accounting. The internal
        # access-token exchange is not a hop — the prefix would only
        # corrupt the credential the taktile-api auth server validates
        # (e.g. ``X-Api-Key: <uuid7>+<api_key>`` is not a valid api key).
        # Send bare wire format here; the caller's ``session_state``
        # still carries the prefix for downstream emission.
        bare_state = SessionState(
            api_key=session_state.api_key,
            jwt=session_state.jwt,
            session_prefix=None,
        )
        params: t.Dict[str, t.Any] = {"expires_seconds": expires_seconds}
        if organization_id is not None:
            params["organization_id"] = organization_id
        if workspace_id is not None:
            params["workspace_id"] = workspace_id
        if roles is not None:
            params["roles"] = list(roles)
        if resource is not None:
            params["resource"] = resource
        try:
            res = requests.post(
                self.access_token_url,
                headers=bare_state.to_auth_headers(),
                timeout=settings.AUTH_SERVER_TIMEOUT_SECONDS,
                params=params,
                cert=self.cert,
            )
            res.raise_for_status()
            id_token = res.json()["id_token"]
            return AuthClient.JWTResponseSuccess(token=id_token)

        except requests.exceptions.Timeout as exc:
            return AuthClient.JWTResponseAllowedFailure(exception=exc)
        except requests.exceptions.HTTPError as exc:
            if exc.response.status_code in (404, 429, 499) or exc.response.status_code >= 500:
                return AuthClient.JWTResponseAllowedFailure(exception=exc)
            return AuthClient.JWTResponseForbiddenFailure(exception=exc)
        except Exception as exc:
            return AuthClient.JWTResponseForbiddenFailure(exception=exc)

    def _refresh_jwt(
        self, *, session_state: SessionState
    ) -> t.Union[
        JWTResponseSuccess,
        JWTResponseAllowedFailure,
        JWTResponseForbiddenFailure,
    ]:
        return self.fetch_jwt(
            session_state=session_state,
            expires_seconds=int(self._cache_fallback_time.total_seconds()),
            organization_id=self._organization_id,
            workspace_id=self._workspace_id,
            resource=self._resource,
        )

    def _get_cache_key(self, key: str) -> str:
        salt = self._salt if self._salt else ""
        return blake2b(f"{salt}{key}".encode()).hexdigest()

    def _record_recursion_hop(self, *, session_state: SessionState, weight: int) -> None:
        """PEP-295 hop accounting.

        - **First hop** (no inbound prefix): the auth check originates
          at the edge of our system. Mint a fresh session prefix so
          downstream services can chain, but **skip the DDB write** —
          single-hop requests should pay zero recursion latency.

        - **Subsequent hop** (prefix already present): an upstream
          service stamped this request. Record the weight against the
          existing prefix; ``record_hop`` raises ``LoopDetectedException``
          under ``error`` mode if the abort threshold is crossed.

        No-op when no gate is configured or the caller opts out via
        ``weight=0``.
        """
        if self._recursion_gate is None or weight <= 0:
            return
        if not session_state.session_prefix:
            session_state.session_prefix = self._recursion_gate.start_session()
            return
        self._recursion_gate.record_hop(
            session_prefix=session_state.session_prefix,
            weight=weight,
        )

    def is_recursion_aborted(self, session_prefix: t.Optional[str]) -> bool:
        """Whether ``session_prefix`` has crossed the PEP-295 abort threshold.

        Lets a downstream consumer turn a failure into a terminal recursion
        stop. ``False`` when recursion checking is disabled or no prefix is
        given.
        """
        if self._recursion_gate is None or not session_prefix:
            return False
        return self._recursion_gate.is_aborted(session_prefix)
