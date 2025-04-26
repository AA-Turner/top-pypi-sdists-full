import os
from dataclasses import dataclass
from typing import Optional

import grpc
from flytekit.clients.auth_helper import (
    RemoteClientConfigStore,
    get_authenticator,
)
from flytekit.configuration import Config, PlatformConfig

from union._config import _get_authenticated_channel
from union.filesystems._middleware import (
    StreamStreamClientServiceAccountMetadataInterceptor,
    StreamUnaryClientServiceAccountMetadataInterceptor,
    UnaryStreamClientAuthInterceptor,
    UnaryStreamClientServiceAccountMetadataInterceptor,
    UnaryUnaryClientAuthInterceptor,
    UnaryUnaryClientServiceAccountMetadataInterceptor,
)

_ENDPOINT = "localhost:8080"
MAX_MESSAGE_LENGTH = 100 * 1024 * 1024
COMMON_GRPC_OPTIONS = [
    ("grpc.max_message_length", MAX_MESSAGE_LENGTH),
    ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
    ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
]


def _get_endpoint() -> str:
    endpoint = os.environ.get("OBJECT_STORE_ENDPOINT")
    if endpoint is not None and endpoint != "":
        return endpoint

    endpoint = os.environ.get("object_store_endpoint")
    if endpoint is not None and endpoint != "":
        return endpoint

    return _ENDPOINT


def _is_remote(endpoint: str) -> bool:
    return endpoint != _ENDPOINT


def _create_channel_for_execution_environment():
    endpoint = _get_endpoint()

    interceptors = None
    if _is_remote(endpoint):
        unary_unary_auth_interceptor = UnaryUnaryClientServiceAccountMetadataInterceptor()
        unary_stream_auth_interceptor = UnaryStreamClientServiceAccountMetadataInterceptor()
        stream_unary_auth_interceptor = StreamUnaryClientServiceAccountMetadataInterceptor()
        stream_stream_auth_interceptor = StreamStreamClientServiceAccountMetadataInterceptor()
        interceptors = [
            unary_unary_auth_interceptor,
            unary_stream_auth_interceptor,
            stream_unary_auth_interceptor,
            stream_stream_auth_interceptor,
        ]

    channel = grpc.aio.insecure_channel(
        endpoint,
        options=COMMON_GRPC_OPTIONS,
        interceptors=interceptors,
    )
    return channel


def _create_secure_channel_from_config(
    platform_cfg: PlatformConfig, sync_channel: Optional[grpc.Channel] = None
) -> grpc.aio.Channel:
    # Add authenticator interceptor that uses the original channel. Use a sync channel
    # here to get the credentials.
    if sync_channel is None:
        sync_channel = _get_authenticated_channel(platform_cfg)

    authenticator = get_authenticator(platform_cfg, RemoteClientConfigStore(sync_channel))
    if authenticator.get_credentials() is None:
        authenticator.refresh_credentials()

    return grpc.aio.secure_channel(
        platform_cfg.endpoint,
        credentials=grpc.ssl_channel_credentials(),
        options=COMMON_GRPC_OPTIONS,
        interceptors=[
            UnaryUnaryClientAuthInterceptor(authenticator),
            UnaryStreamClientAuthInterceptor(authenticator),
        ],
    )


@dataclass
class RemoteConnection:
    channel: grpc.aio._channel
    in_execution_env: bool


def _create_channel(config: Optional[Config] = None) -> RemoteConnection:
    endpoint = _get_endpoint()
    if _is_remote(endpoint) or config is None:
        return RemoteConnection(channel=_create_channel_for_execution_environment(), in_execution_env=True)
    return RemoteConnection(_create_secure_channel_from_config(config.platform), in_execution_env=False)
