"""Async gRPC client for ``kytte.ingest.v1.IngestService``.

One unary RPC: ``IngestSpans``. Channel is created lazily on first send and
reused across calls.
"""

import logging
from typing import Any  # noqa: TID251 — generated proto types are dynamically typed.

import grpc

from aigie._grpc import _DEFAULT_GRPC_PORT, split_host_port
from aigie.ingest._pb.kytte.ingest.v1 import ingest_pb2 as _ingest_pb2
from aigie.ingest._pb.kytte.ingest.v1 import ingest_pb2_grpc as pb_grpc

pb: Any = _ingest_pb2

logger = logging.getLogger(__name__)

# The buffer's flush_interval is typically a few seconds; cap each send so a
# sluggish gateway can't stall subsequent flushes.
_DEFAULT_TIMEOUT_S = 30.0


class IngestClient:
    """Long-lived gRPC client wrapping a single channel + stub.

    Thread-safety: ``grpc.aio.Channel`` is coroutine-safe for concurrent
    unary calls, so we don't add a lock.
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        *,
        use_tls: bool = False,
        timeout_s: float = _DEFAULT_TIMEOUT_S,
    ) -> None:
        host, port = split_host_port(endpoint)
        self._target = f"{host}:{port or _DEFAULT_GRPC_PORT}"
        self._use_tls = use_tls
        self._timeout_s = timeout_s
        self._metadata: tuple[tuple[str, str], ...] = (("x-api-key", api_key),) if api_key else ()
        self._channel: grpc.aio.Channel | None = None
        self._stub: pb_grpc.IngestServiceStub | None = None

    @property
    def target(self) -> str:
        return self._target

    def _ensure_channel(self) -> pb_grpc.IngestServiceStub:
        if self._stub is not None:
            return self._stub
        if self._use_tls:
            creds = grpc.ssl_channel_credentials()
            self._channel = grpc.aio.secure_channel(self._target, creds)
        else:
            self._channel = grpc.aio.insecure_channel(self._target)
        self._stub = pb_grpc.IngestServiceStub(self._channel)
        logger.debug("IngestClient channel opened: target=%s tls=%s", self._target, self._use_tls)
        return self._stub

    async def send_spans(self, spans: list[pb.Span]) -> pb.IngestSpansResponse:
        """Send a batch of finalized spans.

        Raises ``grpc.aio.AioRpcError`` on transport failure.
        """
        stub = self._ensure_channel()
        return await stub.IngestSpans(
            pb.IngestSpansRequest(spans=spans),
            metadata=self._metadata,
            timeout=self._timeout_s,
        )

    async def close(self) -> None:
        if self._channel is not None:
            await self._channel.close()
            self._channel = None
            self._stub = None
