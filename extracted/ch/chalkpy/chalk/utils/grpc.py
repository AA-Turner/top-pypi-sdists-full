from __future__ import annotations

import dataclasses
import time
from typing import TYPE_CHECKING, Callable, Literal, Sequence, TypeVar, final

import grpc

from chalk._gen.chalk.server.v1.auth_pb2 import GetTokenRequest, GetTokenResponse
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub

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
            ("x-chalk-server", server),
            *additional_headers,
        ]
        if environment_id is not None:
            self._constant_headers.append(("x-chalk-env-id", environment_id))

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
            ("x-chalk-server", server),
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
            headers_dict: dict[str, str | bytes] = dict(self._headers)
            headers_dict.update(client_call_details.metadata)
            headers = tuple(headers_dict.items())
        return continuation(
            _ClientCallDetails(
                method=client_call_details.method,
                timeout=client_call_details.timeout,
                metadata=headers,
                credentials=client_call_details.credentials,
            ),
            request,
        )
