from typing import List, Optional, Tuple

import grpc
from grpc import aio

# gRPC channel options shared by the sync and async channels.
CHANNEL_OPTIONS: List[Tuple[str, object]] = [
    ("grpc.keepalive_time_ms", 30000),
    ("grpc.keepalive_timeout_ms", 5000),
    ("grpc.keepalive_permit_without_calls", True),
    ("grpc.http2.max_pings_without_data", 0),
    ("grpc.http2.min_time_between_pings_ms", 10000),
    ("grpc.http2.min_ping_interval_without_data_ms", 300000),
    ("grpc.http2.write_buffer_size", 0),
    ("grpc.http2.max_frame_size", 4194304),
    ("grpc.max_receive_message_length", 10 * 1024 * 1024),
]


class SeltzClient:
    """Low-level gRPC client for Seltz API."""

    def __init__(
        self, endpoint: str, api_key: Optional[str] = None, insecure: bool = False
    ):
        """Initialize the Seltz gRPC client.

        Args:
            endpoint (str, optional, default=grpc.seltz.ai):
                The API endpoint for the Seltz API.

            api_key (str, optional, default=None):
                The API key for authenticating with the Seltz API.

            insecure (bool, optional, default=False):
                Whether to use insecure connection.
        """

        if insecure:
            channel = grpc.insecure_channel(endpoint, options=CHANNEL_OPTIONS)

        else:
            channel = grpc.secure_channel(
                endpoint, grpc.ssl_channel_credentials(), options=CHANNEL_OPTIONS
            )

        self.channel = channel
        self.api_key = api_key


class AsyncSeltzClient:
    """Low-level asyncio gRPC client for the Seltz API."""

    def __init__(
        self, endpoint: str, api_key: Optional[str] = None, insecure: bool = False
    ):
        """Initialize the async Seltz gRPC client.

        Args:
            endpoint (str):
                The API endpoint for the Seltz API.

            api_key (str, optional, default=None):
                The API key for authenticating with the Seltz API.

            insecure (bool, optional, default=False):
                Whether to use an insecure connection.
        """

        if insecure:
            channel = aio.insecure_channel(endpoint, options=CHANNEL_OPTIONS)

        else:
            channel = aio.secure_channel(
                endpoint, grpc.ssl_channel_credentials(), options=CHANNEL_OPTIONS
            )

        self.channel: aio.Channel = channel
        self.api_key = api_key
