"""gRPC channel with Bearer-token auth interceptor.

Used internally by the runner and by the CLI. Not a public API.
"""

from __future__ import annotations

import functools
from typing import Any, Callable, List, NewType, Optional, Sequence, Tuple, cast

import grpc
from grpc import ChannelCredentials
from grpc._interceptor import _Channel as InterceptorChannel

from .config import ConfigContext, get_config_context

_MAX_MSG = 16 * 1024 * 1024
_DEFAULT_OPTIONS = [
    ("grpc.max_receive_message_length", _MAX_MSG),
    ("grpc.max_send_message_length", _MAX_MSG),
    ("grpc.keepalive_time_ms", 20_000),
    ("grpc.keepalive_timeout_ms", 10_000),
    ("grpc.keepalive_permit_without_calls", 1),
    ("grpc.http2.max_pings_without_data", 0),
]
_Metadata = NewType("_Metadata", List[Tuple[Any, Any]])


class Channel(InterceptorChannel):
    """gRPC channel that injects ``Authorization: Bearer <token>``."""

    def __init__(
        self,
        addr: str,
        token: Optional[str] = None,
        credentials: Optional[ChannelCredentials] = None,
        options: Optional[Sequence[Tuple[str, Any]]] = None,
        extra_metadata: Optional[List[Tuple[str, str]]] = None,
    ):
        option_map = {k: v for k, v in _DEFAULT_OPTIONS}
        if options:
            for key, value in options:
                option_map[key] = value
        options = list(option_map.items())
        if credentials:
            raw = grpc.secure_channel(addr, credentials, options=options)
        elif addr.endswith("443"):
            raw = grpc.secure_channel(addr, grpc.ssl_channel_credentials(), options=options)
        else:
            raw = grpc.insecure_channel(addr, options=options)

        super().__init__(channel=raw, interceptor=_AuthInterceptor(token, extra_metadata))


class _AuthInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    def __init__(self, token: Optional[str], extra: Optional[List[Tuple[str, str]]] = None):
        self._token = token
        self._extra = extra or []

    def _inject(self, details):
        md = list(details.metadata or [])
        if self._token:
            md.append(("authorization", f"Bearer {self._token}"))
        md.extend(self._extra)
        return details._replace(metadata=cast(_Metadata, md))

    def intercept_call(self, continuation, details, request):
        return continuation(self._inject(details), request)

    def intercept_call_stream(self, continuation, details, request_iterator):
        return continuation(self._inject(details), request_iterator)

    intercept_unary_unary = intercept_call
    intercept_unary_stream = intercept_call
    intercept_stream_unary = intercept_call_stream
    intercept_stream_stream = intercept_call_stream


# ── CLI helpers ─────────────────────────────────────────────────────────


def get_channel(ctx: Optional[ConfigContext] = None) -> Channel:
    ctx = ctx or get_config_context()
    if not ctx or not ctx.is_valid():
        raise RuntimeError("No valid config. Run 'capsule login' first.")
    return Channel(addr=f"{ctx.gateway_host}:{ctx.gateway_port}", token=ctx.token)


class ServiceClient:
    """Context-managed wrapper around a gRPC channel for the CLI."""

    def __init__(self, config: Optional[ConfigContext] = None) -> None:
        self._config = config
        self._channel: Optional[Channel] = None
        self._capsule_stub = None
        self._secret_stub = None
        self._filesystem_stub = None

    @classmethod
    def with_channel(cls, channel: Channel) -> ServiceClient:
        client = cls()
        client._channel = channel
        return client

    def __enter__(self) -> ServiceClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()

    @property
    def channel(self) -> Channel:
        if not self._channel:
            self._channel = get_channel(self._config)
        return self._channel

    @channel.setter
    def channel(self, value: Channel) -> None:
        self._channel = value

    @property
    def capsule(self):
        if not self._capsule_stub:
            from .clients.capsule import CapsuleServiceStub

            self._capsule_stub = CapsuleServiceStub(self.channel)
        return self._capsule_stub

    @property
    def secrets(self):
        if not self._secret_stub:
            from .clients.capsule import SecretServiceStub

            self._secret_stub = SecretServiceStub(self.channel)
        return self._secret_stub

    @property
    def filesystems(self):
        if not self._filesystem_stub:
            from .clients.capsule import FilesystemServiceStub

            self._filesystem_stub = FilesystemServiceStub(self.channel)
        return self._filesystem_stub

    def close(self) -> None:
        if self._channel:
            self._channel.close()


def pass_service_client(func: Callable) -> Callable:
    """Decorator: injects a ServiceClient as the first arg."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from . import terminal

        ctx = get_config_context()
        if not ctx or not ctx.is_valid():
            terminal.error("Not logged in. Run 'capsule login' first.")
            raise SystemExit(1)
        try:
            with ServiceClient(ctx) as client:
                return func(client, *args, **kwargs)
        except grpc.RpcError as e:
            code, details = e.code(), e.details()
            if code == grpc.StatusCode.UNAUTHENTICATED:
                terminal.error("Unauthorized. Run 'capsule login'.")
            elif code == grpc.StatusCode.UNAVAILABLE:
                terminal.error("Unable to connect to gateway.")
            elif code != grpc.StatusCode.CANCELLED:
                terminal.error(f"gRPC error: {code} — {details}")
            raise SystemExit(1)

    return wrapper
