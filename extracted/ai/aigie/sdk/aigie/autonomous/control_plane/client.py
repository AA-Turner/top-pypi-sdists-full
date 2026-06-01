"""ControlStreamClient — bidirectional gRPC stream to the Kytte platform.

Proto firewall (ADR §3.7): this module has ZERO imports from codec or _pb.
All proto conversion functions and the gRPC Stub class are injected at
construction time by the caller (typically ControlStreamClientFactory or
tests).  This keeps the static import graph clean: import-linter sees no
edge from client -> codec -> _pb.

Usage::

    from aigie.autonomous.control_plane import _client_factory
    client = _client_factory.make_client(endpoint, api_key, ...)
    client.start()
"""

from __future__ import annotations

import contextlib
import dataclasses
import logging
import queue
import threading
import time
from collections.abc import Callable
from typing import Any

import grpc
from opentelemetry import propagate as _propagate

import aigie.telemetry as _telemetry
from aigie.autonomous.control_plane.reconnect import BackoffPolicy
from aigie.autonomous.directives import Directive
from aigie.autonomous.metrics import kytte_platform_unreachable_seconds
from aigie.autonomous.outcome import OutcomeReport

logger = logging.getLogger(__name__)

tracer = _telemetry.get_tracer("aigie.autonomous")

_PING_INTERVAL_S = 30.0
_GAUGE_TICK_S = 1.0
_DEFAULT_GRPC_PORT = 50051


def _derive_grpc_target(endpoint: str) -> str:
    """Convert the SDK's HTTP-style platform endpoint to a gRPC host:port target.

    gRPC channel ctor expects ``host:port`` (no scheme, no path). The HTTP
    endpoint stored on the client (e.g. ``http://kytte-agent:8000/api``) is
    parsed; the host is preserved and the port is replaced with the gRPC port
    from ``AIGIE_GRPC_PORT`` env (default 50051). Already-clean ``host:port``
    strings are passed through unchanged.
    """
    import os
    from urllib.parse import urlparse

    grpc_port = int(os.environ.get("AIGIE_GRPC_PORT", _DEFAULT_GRPC_PORT))
    # Already-clean host:port — no scheme, no path.
    if "://" not in endpoint and "/" not in endpoint:
        host, _, port = endpoint.partition(":")
        return f"{host}:{port or grpc_port}"
    parsed = urlparse(endpoint)
    host = parsed.hostname or endpoint
    return f"{host}:{grpc_port}"


# ---------------------------------------------------------------------------
# Codec interface (injected — no import of codec or _pb here)
# ---------------------------------------------------------------------------


class _CodecInterface:
    """Container for codec functions injected into ControlStreamClient.

    This indirection keeps client.py free of any codec/pb import,
    satisfying the import-linter proto-firewall contract (ADR §3.7).
    """

    def __init__(
        self,
        outcome_to_proto: Callable[[OutcomeReport], Any],
        proto_to_directive: Callable[[Any], Directive],
        make_hello_envelope: Callable[[str, str, str, Callable[[], str]], Any],
        make_outcome_envelope: Callable[[Any], Any],
        make_ping_envelope: Callable[[], Any],
        stub_cls: Any,  # pb_grpc.ControlPlaneStub
        codec_error_cls: type,
    ) -> None:
        self.outcome_to_proto = outcome_to_proto
        self.proto_to_directive = proto_to_directive
        self.make_hello_envelope = make_hello_envelope
        self.make_outcome_envelope = make_outcome_envelope
        self.make_ping_envelope = make_ping_envelope
        self.stub_cls = stub_cls
        self.codec_error_cls = codec_error_cls


# ---------------------------------------------------------------------------
# Gauge updater thread
# ---------------------------------------------------------------------------


class _CallDetailsWithMetadata(grpc.ClientCallDetails):
    """Minimal ClientCallDetails replacement carrying injected metadata."""

    def __init__(self, original: Any, metadata: list) -> None:
        self.method = original.method
        self.timeout = original.timeout
        self.metadata = metadata
        self.credentials = original.credentials


class _TraceparentClientInterceptor(
    grpc.UnaryUnaryClientInterceptor,
    grpc.UnaryStreamClientInterceptor,
    grpc.StreamUnaryClientInterceptor,
    grpc.StreamStreamClientInterceptor,
):
    """Injects W3C traceparent into outbound gRPC call metadata."""

    def _inject(self, client_call_details: Any) -> _CallDetailsWithMetadata:
        metadata = list(client_call_details.metadata or [])
        carrier: dict[str, str] = {}
        _propagate.inject(carrier)
        for k, v in carrier.items():
            metadata.append((k.lower(), v))
        return _CallDetailsWithMetadata(client_call_details, metadata)

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return continuation(self._inject(client_call_details), request)

    def intercept_unary_stream(self, continuation, client_call_details, request):
        return continuation(self._inject(client_call_details), request)

    def intercept_stream_unary(self, continuation, client_call_details, request_iterator):
        return continuation(self._inject(client_call_details), request_iterator)

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        return continuation(self._inject(client_call_details), request_iterator)


def _run_gauge_updater(
    stop_event: threading.Event,
    disconnected_at_ref: list[float | None],
    lock: threading.Lock,
) -> None:
    """Tick every second; update kytte_platform_unreachable_seconds gauge."""
    while not stop_event.is_set():
        with lock:
            disconnected_at = disconnected_at_ref[0]
        if disconnected_at is not None:
            elapsed = time.monotonic() - disconnected_at
            kytte_platform_unreachable_seconds.set(elapsed)
        stop_event.wait(timeout=_GAUGE_TICK_S)


# ---------------------------------------------------------------------------
# Dispatch helpers
# ---------------------------------------------------------------------------


def _dispatch_server_envelope(
    envelope: Any,
    rule_cache_version: str,
    on_directive: Callable[[Directive], None],
    codec: _CodecInterface,
) -> None:
    """Dispatch one ServerEnvelope to the appropriate callback."""
    which = envelope.WhichOneof("msg")
    if which == "directive":
        _dispatch_directive(envelope, rule_cache_version, on_directive, codec)
    elif which in ("ping", "hello_ack", None):
        pass
    else:
        logger.debug("unknown ServerEnvelope field: %s", which)


def _dispatch_directive(
    envelope: Any,
    rule_cache_version: str,
    on_directive: Callable[[Directive], None],
    codec: _CodecInterface,
) -> None:
    try:
        d = codec.proto_to_directive(envelope.directive)
        d = dataclasses.replace(d, rule_cache_version=rule_cache_version)
    except Exception as exc:
        if isinstance(exc, codec.codec_error_cls):
            logger.warning("codec error decoding directive: %s", exc)
            return
        raise
    try:
        on_directive(d)
    except Exception:
        logger.exception("on_directive callback raised")


# ---------------------------------------------------------------------------
# ControlStreamClient
# ---------------------------------------------------------------------------


class ControlStreamClient:
    """Bidirectional gRPC stream to the Kytte platform control plane.

    Implements the StreamSink protocol so OutcomeReporter can use it directly.

    All proto types are injected via _CodecInterface — this module has no
    static dependency on codec or _pb (ADR §3.7 proto firewall).

    Thread model (ADR §3.5):
    - One daemon thread runs _run() which owns the gRPC stream.
    - send_outcome() pushes to a thread-safe queue read by the stream thread.
    - A separate gauge-updater thread ticks once per second while disconnected.
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None,
        on_directive: Callable[[Directive], None],
        codec: _CodecInterface,
        sdk_version: str = "0.2.40",
        sdk_language: str = "python",
        customer_id: str = "",
        rule_cache_version_provider: Callable[[], str] = lambda: "",
    ) -> None:
        self._endpoint = endpoint
        self._grpc_target = _derive_grpc_target(endpoint)
        self._api_key = api_key
        self._on_directive = on_directive
        self._codec = codec
        self._sdk_version = sdk_version
        self._sdk_language = sdk_language
        self._customer_id = customer_id
        self._rule_cache_version_provider = rule_cache_version_provider
        self._init_state()

    def _init_state(self) -> None:
        """Initialise threading primitives and mutable state (split from __init__)."""
        self._stop_event = threading.Event()
        self._send_queue: queue.Queue[OutcomeReport] = queue.Queue()
        self._conn_lock = threading.Lock()
        self._is_connected: bool = False
        self._rule_cache_version: str = ""
        self._disconnected_at_ref: list[float | None] = [None]
        self._gauge_lock = threading.Lock()
        # OutcomeReporter registers itself here via on_connected_callbacks.append
        self.on_connected_callbacks: list[Callable[[], None]] = []
        self._stream_thread: threading.Thread | None = None
        self._gauge_thread: threading.Thread | None = None
        self._backoff = BackoffPolicy()

    # ------------------------------------------------------------------
    # StreamSink protocol
    # ------------------------------------------------------------------

    def is_connected(self) -> bool:
        """True while a stream is established and not in backoff."""
        with self._conn_lock:
            return self._is_connected

    def send_outcome(self, outcome: OutcomeReport) -> None:
        """Enqueue an OutcomeReport for sending. Raises RuntimeError if not connected."""
        if not self.is_connected():
            raise RuntimeError("ControlStreamClient is not connected")
        self._send_queue.put(outcome)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Spawn daemon threads for gauge updater and stream."""
        self._gauge_thread = threading.Thread(
            target=_run_gauge_updater,
            args=(self._stop_event, self._disconnected_at_ref, self._gauge_lock),
            daemon=True,
            name="aigie-gauge-updater",
        )
        self._gauge_thread.start()
        self._stream_thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="aigie-control-stream",
        )
        self._stream_thread.start()

    def stop(self, grace: float = 2.0) -> None:
        """Signal stop and join the stream thread."""
        self._stop_event.set()
        if self._stream_thread is not None:
            self._stream_thread.join(timeout=grace)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_channel(self) -> grpc.Channel:
        """Open a gRPC channel.

        TODO(prod): use grpc.secure_channel with proper TLS credentials
        for production endpoints. Insecure for now (dev/stub-friendly).
        """
        return grpc.intercept_channel(
            grpc.insecure_channel(self._grpc_target),
            _TraceparentClientInterceptor(),
        )

    def _set_connected(self, value: bool) -> None:
        with self._conn_lock:
            self._is_connected = value
        if value:
            with self._gauge_lock:
                self._disconnected_at_ref[0] = None
            kytte_platform_unreachable_seconds.set(0)
            self._fire_on_connected()
        else:
            with self._gauge_lock:
                if self._disconnected_at_ref[0] is None:
                    self._disconnected_at_ref[0] = time.monotonic()

    def _fire_on_connected(self) -> None:
        for cb in list(self.on_connected_callbacks):
            try:
                cb()
            except Exception:
                logger.exception("on_connected_callback raised")

    def _client_envelope_generator(self):  # type: ignore[return]
        """Yield ClientEnvelope messages: Hello first, then outcomes + pings."""
        yield self._codec.make_hello_envelope(
            self._sdk_version,
            self._sdk_language,
            self._customer_id,
            self._rule_cache_version_provider,
        )
        last_ping = time.monotonic()
        while not self._stop_event.is_set():
            try:
                outcome = self._send_queue.get(timeout=1.0)
                yield self._codec.make_outcome_envelope(outcome)
                continue
            except queue.Empty:
                pass
            now = time.monotonic()
            if now - last_ping >= _PING_INTERVAL_S:
                yield self._codec.make_ping_envelope()
                last_ping = now

    def _handle_hello_ack(self, envelope: Any) -> None:
        ack = envelope.hello_ack
        logger.info(
            "control stream connected (sdk=%s customer=%s)",
            ack.sdk_version or self._sdk_version,
            ack.customer_id or self._customer_id,
        )
        self._backoff.reset()
        self._set_connected(True)

    def _process_response_stream(self, response_stream: Any) -> None:
        got_ack = False
        for envelope in response_stream:
            if self._stop_event.is_set():
                break
            which = envelope.WhichOneof("msg")
            if not got_ack:
                if which == "hello_ack":
                    self._handle_hello_ack(envelope)
                    got_ack = True
                else:
                    logger.warning("expected hello_ack, got %s — ignoring", which)
                continue
            _dispatch_server_envelope(
                envelope,
                self._rule_cache_version,
                self._on_directive,
                self._codec,
            )

    def _run_session_with_cleanup(self, channel: grpc.Channel) -> None:
        """Run one session and ensure channel is closed + connected=False on exit."""
        try:
            self._run_one_session(channel)
        except grpc.RpcError as exc:
            logger.warning("gRPC error on control stream: %s", exc)
        except Exception:
            logger.exception("unexpected error on control stream")
        finally:
            self._set_connected(False)
            with contextlib.suppress(Exception):
                channel.close()

    def _run(self) -> None:
        """Outer reconnect loop: connect → stream → backoff → repeat."""
        reconnect_count = 0
        with tracer.start_as_current_span("stream.session") as span:
            span.set_attribute("target", self._grpc_target)
            span.set_attribute("reconnect_count", reconnect_count)
            while not self._stop_event.is_set():
                self._run_session_with_cleanup(self._make_channel())
                if self._stop_event.is_set():
                    break
                reconnect_count += 1
                span.set_attribute("reconnect_count", reconnect_count)
                delay = self._backoff.next_delay_seconds()
                logger.debug("reconnecting in %.2fs", delay)
                self._stop_event.wait(timeout=delay)

    def _run_one_session(self, channel: grpc.Channel) -> None:
        """Open one bidi stream session and iterate until closed."""
        # pb_grpc.ControlPlaneStub is injected via _codec.stub_cls —
        # codec is the proto firewall (ADR §3.7). No _pb import here.
        stub = self._codec.stub_cls(channel)
        response_stream = stub.Stream(self._client_envelope_generator())
        self._process_response_stream(response_stream)
