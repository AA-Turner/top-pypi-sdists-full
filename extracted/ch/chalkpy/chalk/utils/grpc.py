from __future__ import annotations

import asyncio
import concurrent.futures
import dataclasses
import math
import os
import random
import threading
import time
from typing import TYPE_CHECKING, Awaitable, Callable, Literal, Optional, Protocol, Sequence, TypeVar, final

import grpc
import grpc.aio

from chalk._gen.chalk.server.v1.auth_pb2 import GetTokenRequest, GetTokenResponse
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk.client.client_headers import CHALK_ENV_ID_HEADER_LOWERCASE, CHALK_SERVER_HEADER_LOWERCASE
from chalk.clogging import chalk_logger
from chalk.config.web_identity import WebIdentityToken, get_web_identity_token

if TYPE_CHECKING:
    from chalk import EnvironmentId


@dataclasses.dataclass
class _ClientCallDetails(grpc.ClientCallDetails):
    method: str
    timeout: float | None
    metadata: grpc.Metadata | None
    credentials: grpc.CallCredentials | None


# Token refresh policy, shared by the sync and async refreshers.
#
# The exchange runs in the auth interceptor, before the caller's RPC and outside its deadline.
# To keep it off the request path, refresh starts halfway through the token's lifetime and runs
# in the background while the cached token keeps being served.

_REFRESH_AT_FRACTION = 0.5
# Per-refresher jitter on the refresh point, so processes started together don't refresh together.
_REFRESH_JITTER_FRACTION = 0.1
# Within this many seconds of expiry, callers wait for the refresh instead of using the cached token.
_BLOCKING_FLOOR_SECONDS = 60.0
_EXCHANGE_TIMEOUT_SECONDS = 10.0
# Minimum time between successful exchanges, so an already-expired or very short-lived token
# doesn't cause an exchange per request.
_MIN_REFRESH_INTERVAL_SECONDS = 30.0
# Exponential backoff between failed exchanges.
_RETRY_BACKOFF_INITIAL_SECONDS = 1.0
_RETRY_BACKOFF_MAX_SECONDS = 30.0
# Refresh interval for tokens with no expires_at.
_NO_EXPIRY_REFRESH_SECONDS = 60.0 * 60.0


@dataclasses.dataclass(frozen=True)
class _CachedToken:
    """A token response and when to start refreshing it. Immutable so it can be read without a lock."""

    response: GetTokenResponse
    refresh_at: float

    @property
    def expires_at(self) -> float:
        """Expiry in epoch seconds, or inf if unset."""
        if not self.response.HasField("expires_at"):
            return math.inf
        return self.response.expires_at.seconds


def _refresh_at(response: GetTokenResponse, issued_at: float, jitter: float) -> float:
    if not response.HasField("expires_at"):
        return issued_at + _NO_EXPIRY_REFRESH_SECONDS
    lifetime = response.expires_at.seconds - issued_at
    if lifetime <= 0:
        # Already expired (or clock skew). Still serve it, but don't retry right away.
        return issued_at + _MIN_REFRESH_INTERVAL_SECONDS
    refresh_at = issued_at + lifetime * _REFRESH_AT_FRACTION * (1.0 + jitter)
    return min(refresh_at, response.expires_at.seconds - _BLOCKING_FLOOR_SECONDS)


def _retry_backoff(consecutive_failures: int, jitter: float) -> float:
    # Jittered so processes that failed during the same outage don't retry in lockstep.
    backoff = _RETRY_BACKOFF_INITIAL_SECONDS * 2.0 ** min(consecutive_failures - 1, 32)
    return min(backoff, _RETRY_BACKOFF_MAX_SECONDS) * (1.0 + jitter)


def _draw_jitter() -> float:
    return random.uniform(-_REFRESH_JITTER_FRACTION, _REFRESH_JITTER_FRACTION)


def _token_request(client_id: str, client_secret: str) -> GetTokenRequest:
    return GetTokenRequest(
        client_id=client_id,
        client_secret=client_secret,
        grant_type="client_credentials",
    )


@final
class TokenRefresher:
    def __init__(
        self,
        auth_stub: AuthServiceStub,
        client_id: str,
        client_secret: str,
    ):
        self._auth_stub = auth_stub
        self._client_id = client_id
        self._client_secret = client_secret
        self._cached: Optional[_CachedToken] = None
        self._jitter = _draw_jitter()
        # Guards _attempt. Never held during the exchange.
        self._lock = threading.Lock()
        # Latest exchange. Callers share it (including its failure) until it finishes and
        # _next_attempt_at passes, so concurrent callers don't each run their own exchange.
        self._attempt: Optional[concurrent.futures.Future[GetTokenResponse]] = None
        self._owner_pid = os.getpid()
        self._next_attempt_at = 0.0
        self._consecutive_failures = 0

    def get_token(self) -> GetTokenResponse:
        cached = self._cached
        now = time.time()
        if cached is not None and now < cached.refresh_at:
            return cached.response
        attempt = self._get_or_start_attempt()
        if cached is None or now >= cached.expires_at:
            return attempt.result()
        if now >= cached.expires_at - _BLOCKING_FLOOR_SECONDS:
            # Near expiry: wait for the new token, but fall back to the still-valid one on failure.
            try:
                return attempt.result()
            except Exception:
                return cached.response
        return cached.response

    def _bind_process(self) -> None:
        """Reset the lock and in-flight attempt after a fork.

        Both can be inherited mid-refresh: the lock stays held and the attempt never resolves,
        since the refresh thread doesn't exist in the child.
        """
        pid = os.getpid()
        if pid == self._owner_pid:
            return
        self._owner_pid = pid
        self._lock = threading.Lock()
        self._attempt = None

    def _get_or_start_attempt(self) -> concurrent.futures.Future[GetTokenResponse]:
        # Must run before acquiring the lock, which may have been inherited locked.
        self._bind_process()
        with self._lock:
            attempt = self._attempt
            if attempt is not None and (not attempt.done() or time.time() < self._next_attempt_at):
                return attempt
            attempt = concurrent.futures.Future()
            self._attempt = attempt
            try:
                threading.Thread(
                    target=self._run_attempt,
                    args=(attempt,),
                    name="chalk-token-refresh",
                    daemon=True,
                ).start()
            except BaseException as e:
                # e.g. interpreter shutdown. Fail the attempt so waiters don't hang.
                self._record_failure()
                attempt.set_exception(e)
            return attempt

    def _run_attempt(self, attempt: concurrent.futures.Future[GetTokenResponse]) -> None:
        issued_at = time.time()
        try:
            response = self._auth_stub.GetToken(
                _token_request(self._client_id, self._client_secret),
                timeout=_EXCHANGE_TIMEOUT_SECONDS,
            )
        except BaseException as e:
            chalk_logger.warning("Chalk token refresh failed", exc_info=True)
            # Before set_exception, so waiters see the updated backoff.
            self._record_failure()
            attempt.set_exception(e)
            return
        self._cached = _CachedToken(response, _refresh_at(response, issued_at, self._jitter))
        self._consecutive_failures = 0
        self._next_attempt_at = time.time() + _MIN_REFRESH_INTERVAL_SECONDS
        attempt.set_result(response)

    def _record_failure(self) -> None:
        # Measured from when the attempt finished, not when it started.
        self._consecutive_failures += 1
        self._next_attempt_at = time.time() + _retry_backoff(self._consecutive_failures, self._jitter)


class TokenProvider(Protocol):
    """The subset of a token refresher that the authenticated interceptors rely on.

    Implemented by both `TokenRefresher`, which exchanges client credentials, and
    `WebIdentityTokenRefresher`, which reads a rotating JWT from disk.
    """

    def get_token(self) -> GetTokenResponse: ...


class AsyncTokenProvider(Protocol):
    """The async counterpart of `TokenProvider`."""

    async def get_token(self) -> GetTokenResponse: ...


@final
class WebIdentityTokenRefresher:
    """Duck-types `TokenRefresher`, but reads a rotating JWT from disk instead of exchanging credentials.

    Rotation is observed because `get_web_identity_token` re-reads the file once
    its cache deadline lapses; this class only adapts the result to the shape the
    interceptors expect. The JWT carries no engine routing, so `engines`,
    `grpc_engines`, and `environment_id_to_name` are left empty -- callers must
    treat those as "the issuer told us nothing" rather than as an error.
    """

    def __init__(self, token_file: str):
        super().__init__()
        self._token_file = token_file
        self._lock = threading.Lock()
        self._cached: tuple[WebIdentityToken, GetTokenResponse] | None = None

    def get_token(self) -> GetTokenResponse:
        token = get_web_identity_token(self._token_file)
        with self._lock:
            cached = self._cached
            # `get_web_identity_token` returns the same frozen object for the whole
            # cache window, so identity tells us the proto is still current and we
            # build it once per rotation rather than once per RPC.
            if cached is not None and cached[0] is token:
                return cached[1]
            response = GetTokenResponse(
                access_token=token.value,
                token_type="Bearer",
                primary_environment=token.environment_id,
            )
            if token.expires_at is not None:
                response.expires_at.FromSeconds(int(token.expires_at))
            self._cached = (token, response)
            return response


@final
class AsyncWebIdentityTokenRefresher:
    """The async counterpart of `WebIdentityTokenRefresher`."""

    def __init__(self, token_file: str):
        super().__init__()
        self._inner = WebIdentityTokenRefresher(token_file)

    async def get_token(self) -> GetTokenResponse:
        # Deliberately not run in an executor: on the common path this is a dict
        # lookup, and even on a miss it is a small local file read that happens at
        # most once per cache window. An executor hop would cost more than it saves.
        return self._inner.get_token()


RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")


@final
class AuthenticatedChalkClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
):
    """
    This GRPC Client Interceptor, adds an auth token and default
    Chalk headers to a grpc channel.
    """

    def __init__(
        self,
        refresher: TokenProvider,
        environment_id: EnvironmentId | None,
        server: Literal["go-api", "engine"],
        additional_headers: list[tuple[str, str]],
    ):
        self._refresher: TokenProvider = refresher
        self._constant_headers = [
            (CHALK_SERVER_HEADER_LOWERCASE, server),
            *additional_headers,
        ]
        if environment_id is not None:
            self._constant_headers.append((CHALK_ENV_ID_HEADER_LOWERCASE, environment_id))

    def _with_auth(self, client_call_details: grpc.ClientCallDetails) -> _ClientCallDetails:
        headers: dict[str, str | bytes] = dict(self._constant_headers)
        headers["authorization"] = f"Bearer {self._refresher.get_token().access_token}"
        if client_call_details.metadata:
            headers.update(client_call_details.metadata)
        return _ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=tuple(headers.items()),
            credentials=client_call_details.credentials,
        )

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, RequestType], grpc.CallFuture[ResponseType]],
        client_call_details: grpc.ClientCallDetails,
        request: RequestType,
    ) -> grpc.CallFuture[ResponseType]:
        return continuation(self._with_auth(client_call_details), request)

    def intercept_unary_stream(
        self,
        continuation: Callable[[grpc.ClientCallDetails, RequestType], grpc.CallIterator[ResponseType]],
        client_call_details: grpc.ClientCallDetails,
        request: RequestType,
    ) -> grpc.CallIterator[ResponseType]:
        return continuation(self._with_auth(client_call_details), request)


@final
class UnauthenticatedChalkClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
):
    """
    This GRPC Client Interceptor, adds an auth token and default
    Chalk headers to a grpc channel.
    """

    def __init__(
        self,
        additional_headers: Sequence[tuple[str, str]],
        server: Literal["go-api", "engine"],
    ):
        self._headers = (
            (CHALK_SERVER_HEADER_LOWERCASE, server),
            *additional_headers,
        )

    def _with_headers(self, client_call_details: grpc.ClientCallDetails) -> _ClientCallDetails:
        headers_dict: dict[str, str | bytes] = dict(self._headers)
        if client_call_details.metadata is not None:
            headers_dict.update(client_call_details.metadata)
        return _ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=tuple(headers_dict.items()),
            credentials=client_call_details.credentials,
        )

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, RequestType], grpc.CallFuture[ResponseType]],
        client_call_details: grpc.ClientCallDetails,
        request: RequestType,
    ) -> grpc.CallFuture[ResponseType]:
        return continuation(self._with_headers(client_call_details), request)

    def intercept_unary_stream(
        self,
        continuation: Callable[[grpc.ClientCallDetails, RequestType], grpc.CallIterator[ResponseType]],
        client_call_details: grpc.ClientCallDetails,
        request: RequestType,
    ) -> grpc.CallIterator[ResponseType]:
        return continuation(self._with_headers(client_call_details), request)


@final
class AsyncTokenRefresher:
    """Async token refresher for use with grpc.aio channels. Same refresh policy as `TokenRefresher`."""

    def __init__(
        self,
        initial_token: GetTokenResponse,
        async_auth_stub: AuthServiceStub,
        client_id: str,
        client_secret: str,
    ):
        self._async_auth_stub = async_auth_stub
        self._client_id = client_id
        self._client_secret = client_secret
        self._jitter = _draw_jitter()
        self._cached = _CachedToken(initial_token, _refresh_at(initial_token, time.time(), self._jitter))
        # Shared like TokenRefresher._attempt. No lock needed since starting one never awaits.
        self._attempt: Optional[asyncio.Task[GetTokenResponse]] = None
        self._next_attempt_at = 0.0
        self._consecutive_failures = 0

    async def get_token(self) -> GetTokenResponse:
        cached = self._cached
        now = time.time()
        if now < cached.refresh_at:
            return cached.response
        attempt = self._get_or_start_attempt()
        if now >= cached.expires_at:
            # Shield so a cancelled caller doesn't cancel the shared exchange.
            return await asyncio.shield(attempt)
        if now >= cached.expires_at - _BLOCKING_FLOOR_SECONDS:
            try:
                return await asyncio.shield(attempt)
            except asyncio.CancelledError:
                raise
            except Exception:
                return cached.response
        return cached.response

    def _get_or_start_attempt(self) -> asyncio.Task[GetTokenResponse]:
        loop = asyncio.get_running_loop()
        attempt = self._attempt
        if (
            attempt is not None
            # A client reused across event loops (e.g. repeated asyncio.run) can hold a task
            # from a closed loop, which will never finish.
            and attempt.get_loop() is loop
            # Cancelled means its loop shut down, not a failure to share.
            and not attempt.cancelled()
            and (not attempt.done() or time.time() < self._next_attempt_at)
        ):
            return attempt
        attempt = loop.create_task(self._run_attempt())
        # Retrieve the exception so an unawaited background failure isn't reported as
        # "exception was never retrieved". _run_attempt already logs it.
        attempt.add_done_callback(lambda t: t.cancelled() or t.exception())
        self._attempt = attempt
        return attempt

    async def _run_attempt(self) -> GetTokenResponse:
        issued_at = time.time()
        try:
            response: GetTokenResponse = (
                await self._async_auth_stub.GetToken(  # pyright: ignore[reportGeneralTypeIssues]
                    _token_request(self._client_id, self._client_secret),
                    timeout=_EXCHANGE_TIMEOUT_SECONDS,
                )
            )
        except asyncio.CancelledError:
            raise
        except Exception:
            chalk_logger.warning("Chalk token refresh failed", exc_info=True)
            self._consecutive_failures += 1
            self._next_attempt_at = time.time() + _retry_backoff(self._consecutive_failures, self._jitter)
            raise
        self._cached = _CachedToken(response, _refresh_at(response, issued_at, self._jitter))
        self._consecutive_failures = 0
        self._next_attempt_at = time.time() + _MIN_REFRESH_INTERVAL_SECONDS
        return response


@final
class AsyncAuthenticatedChalkClientInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
):
    """Async gRPC client interceptor that adds auth token and Chalk headers."""

    def __init__(
        self,
        refresher: AsyncTokenProvider,
        environment_id: "EnvironmentId | None",
        server: Literal["go-api", "engine"],
        additional_headers: list[tuple[str, str]],
    ):
        self._refresher = refresher
        self._constant_headers = [
            (CHALK_SERVER_HEADER_LOWERCASE, server),
            *additional_headers,
        ]
        if environment_id is not None:
            self._constant_headers.append((CHALK_ENV_ID_HEADER_LOWERCASE, environment_id))

    async def _with_auth(self, client_call_details: grpc.aio.ClientCallDetails) -> grpc.aio.ClientCallDetails:
        token = await self._refresher.get_token()
        headers: dict[str, str | bytes] = dict(self._constant_headers)
        headers["authorization"] = f"Bearer {token.access_token}"
        if client_call_details.metadata:
            headers.update(client_call_details.metadata)
        return grpc.aio.ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=tuple(headers.items()),  # pyright: ignore[reportArgumentType]
            credentials=client_call_details.credentials,
            wait_for_ready=getattr(client_call_details, "wait_for_ready", None),
        )

    async def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.aio.ClientCallDetails, RequestType], Awaitable[ResponseType]],
        client_call_details: grpc.aio.ClientCallDetails,
        request: RequestType,
    ):
        return await continuation(await self._with_auth(client_call_details), request)

    async def intercept_unary_stream(
        self,
        continuation: Callable[
            [grpc.aio.ClientCallDetails, RequestType], grpc.aio.UnaryStreamCall[RequestType, ResponseType]
        ],
        client_call_details: grpc.aio.ClientCallDetails,
        request: RequestType,
    ) -> grpc.aio.UnaryStreamCall[RequestType, ResponseType]:
        # grpc.aio's real continuation is a coroutine returning the stream call; await it.
        return await continuation(
            await self._with_auth(client_call_details), request
        )  # pyright: ignore[reportGeneralTypeIssues]


@final
class AsyncUnauthenticatedChalkClientInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
):
    """Async gRPC client interceptor that adds static Chalk headers (no auth)."""

    def __init__(
        self,
        additional_headers: Sequence[tuple[str, str]],
        server: Literal["go-api", "engine"],
    ):
        self._headers = (
            (CHALK_SERVER_HEADER_LOWERCASE, server),
            *additional_headers,
        )

    def _with_headers(self, client_call_details: grpc.aio.ClientCallDetails) -> grpc.aio.ClientCallDetails:
        headers_dict: dict[str, str | bytes] = dict(self._headers)
        if client_call_details.metadata is not None:
            headers_dict.update(client_call_details.metadata)
        return grpc.aio.ClientCallDetails(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=tuple(headers_dict.items()),  # pyright: ignore[reportArgumentType]
            credentials=client_call_details.credentials,
            wait_for_ready=getattr(client_call_details, "wait_for_ready", None),
        )

    async def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.aio.ClientCallDetails, RequestType], Awaitable[ResponseType]],
        client_call_details: grpc.aio.ClientCallDetails,
        request: RequestType,
    ):
        return await continuation(self._with_headers(client_call_details), request)

    async def intercept_unary_stream(
        self,
        continuation: Callable[
            [grpc.aio.ClientCallDetails, RequestType], grpc.aio.UnaryStreamCall[RequestType, ResponseType]
        ],
        client_call_details: grpc.aio.ClientCallDetails,
        request: RequestType,
    ) -> grpc.aio.UnaryStreamCall[RequestType, ResponseType]:
        # grpc.aio's real continuation is a coroutine returning the stream call; await it.
        return await continuation(
            self._with_headers(client_call_details), request
        )  # pyright: ignore[reportGeneralTypeIssues]
