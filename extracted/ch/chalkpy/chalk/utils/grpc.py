from __future__ import annotations

import asyncio
import dataclasses
import time
from typing import TYPE_CHECKING, Awaitable, Callable, Literal, Sequence, TypeVar, final

import grpc
import grpc.aio

from chalk._gen.chalk.server.v1.auth_pb2 import GetTokenRequest, GetTokenResponse
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk.client.client_headers import CHALK_ENV_ID_HEADER_LOWERCASE, CHALK_SERVER_HEADER_LOWERCASE

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


RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")


@final
class AuthenticatedChalkClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    """
    This GRPC Client Interceptor, adds an auth token and default
    Chalk headers to a grpc channel.
    """

    def __init__(
        self,
        refresher: TokenRefresher,
        environment_id: EnvironmentId | None,
        server: Literal["go-api", "engine"],
        additional_headers: list[tuple[str, str]],
    ):
        self._refresher: TokenRefresher = refresher
        self._constant_headers = [
            (CHALK_SERVER_HEADER_LOWERCASE, server),
            *additional_headers,
        ]
        if environment_id is not None:
            self._constant_headers.append((CHALK_ENV_ID_HEADER_LOWERCASE, environment_id))

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, RequestType], grpc.CallFuture[ResponseType]],
        client_call_details: grpc.ClientCallDetails,
        request: RequestType,
    ) -> grpc.CallFuture[ResponseType]:
        headers: dict[str, str | bytes] = dict(self._constant_headers)
        headers["authorization"] = f"Bearer {self._refresher.get_token().access_token}"
        if client_call_details.metadata:
            headers.update(client_call_details.metadata)
        return continuation(
            _ClientCallDetails(
                method=client_call_details.method,
                timeout=client_call_details.timeout,
                metadata=tuple(headers.items()),
                credentials=client_call_details.credentials,
            ),
            request,
        )


@final
class UnauthenticatedChalkClientInterceptor(grpc.UnaryUnaryClientInterceptor):
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

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, RequestType], grpc.CallFuture[ResponseType]],
        client_call_details: grpc.ClientCallDetails,
        request: RequestType,
    ) -> grpc.CallFuture[ResponseType]:
        if client_call_details.metadata is None:
            headers = self._headers
        else:
            headers = self._headers + tuple(client_call_details.metadata)
        return continuation(
            _ClientCallDetails(
                method=client_call_details.method,
                timeout=client_call_details.timeout,
                metadata=headers,
                credentials=client_call_details.credentials,
            ),
            request,
        )


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
class AsyncAuthenticatedChalkClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    """Async gRPC client interceptor that adds auth token and Chalk headers."""

    def __init__(
        self,
        refresher: AsyncTokenRefresher,
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

    async def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.aio.ClientCallDetails, RequestType], Awaitable[ResponseType]],
        client_call_details: grpc.aio.ClientCallDetails,
        request: RequestType,
    ):
        token = await self._refresher.get_token()
        metadata: tuple[tuple[str, str | bytes], ...] = (
            *self._constant_headers,
            ("authorization", f"Bearer {token.access_token}"),
            *(client_call_details.metadata or ()),
        )
        return await continuation(
            grpc.aio.ClientCallDetails(
                method=client_call_details.method,
                timeout=client_call_details.timeout,
                metadata=metadata,  # pyright: ignore[reportArgumentType]
                credentials=client_call_details.credentials,
                wait_for_ready=getattr(client_call_details, "wait_for_ready", None),
            ),
            request,
        )


@final
class AsyncUnauthenticatedChalkClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
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

    async def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.aio.ClientCallDetails, RequestType], Awaitable[ResponseType]],
        client_call_details: grpc.aio.ClientCallDetails,
        request: RequestType,
    ):
        if client_call_details.metadata is None:
            headers = self._headers
        else:
            headers = self._headers + tuple(client_call_details.metadata)
        return await continuation(
            grpc.aio.ClientCallDetails(
                method=client_call_details.method,
                timeout=client_call_details.timeout,
                metadata=headers,  # pyright: ignore[reportArgumentType]
                credentials=client_call_details.credentials,
                wait_for_ready=getattr(client_call_details, "wait_for_ready", None),
            ),
            request,
        )
