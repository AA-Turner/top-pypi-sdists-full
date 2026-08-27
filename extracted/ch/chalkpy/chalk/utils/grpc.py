from __future__ import annotations

import asyncio
import dataclasses
import threading
import time
from typing import TYPE_CHECKING, Awaitable, Callable, Literal, Protocol, Sequence, TypeVar, final

import grpc
import grpc.aio

from chalk._gen.chalk.server.v1.auth_pb2 import GetTokenRequest, GetTokenResponse
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk.client.client_headers import CHALK_ENV_ID_HEADER_LOWERCASE, CHALK_SERVER_HEADER_LOWERCASE
from chalk.config.web_identity import WebIdentityToken, get_web_identity_token

if TYPE_CHECKING:
    from chalk import EnvironmentId


@dataclasses.dataclass
class _ClientCallDetails(grpc.ClientCallDetails):
    method: str
    timeout: float | None
    metadata: grpc.Metadata | None
    credentials: grpc.CallCredentials | None


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
        self._auth_token: GetTokenResponse | None = None

    def get_token(self) -> GetTokenResponse:
        if self._auth_token is None or self._auth_token.expires_at.seconds - time.time() <= 60:
            self._auth_token = self._auth_stub.GetToken(
                GetTokenRequest(
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                    grant_type="client_credentials",
                ),
            )

        return self._auth_token


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
    """Async token refresher for use with grpc.aio channels."""

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
        self._auth_token: GetTokenResponse = initial_token
        self._lock: asyncio.Lock = asyncio.Lock()

    async def get_token(self) -> GetTokenResponse:
        if self._auth_token.expires_at.seconds - time.time() > 60:
            return self._auth_token
        async with self._lock:
            if self._auth_token.expires_at.seconds - time.time() > 60:
                return self._auth_token
            self._auth_token = await self._async_auth_stub.GetToken(  # pyright: ignore[reportGeneralTypeIssues]
                GetTokenRequest(
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                    grant_type="client_credentials",
                ),
            )
        return self._auth_token


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
