"""In-process stub gRPC server for SDK integration tests and local development.

This module is part of control_plane/ and may import from _pb directly.
"""

from __future__ import annotations

import queue
import threading
from collections.abc import Iterator
from concurrent import futures

import grpc

from aigie.autonomous.control_plane._pb import pb, pb_grpc

# Sentinel object used to signal the send loop to exit.
_STOP = object()


class StubControlPlaneServicer(pb_grpc.ControlPlaneServicer):
    """Programmable in-process servicer for SDK tests.

    Test drivers interact via:
    - ``push_directive(directive)`` — enqueue a RemediationDirective to send.
    - ``push_ping(ping)`` — enqueue a Ping to send.
    - ``self.received_outcomes`` — list of OutcomeReport received.
    - ``self.received_pings`` — list of Ping received from client.
    - ``set_remediation_context(directive_id, ctx)`` — pre-load context map.
    """

    def __init__(self) -> None:
        self._send_queue: queue.Queue[object] = queue.Queue()
        self.received_outcomes: list[pb.OutcomeReport] = []
        self.received_pings: list[pb.Ping] = []
        self._context_map: dict[str, pb.RemediationContext] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Test-driver helpers
    # ------------------------------------------------------------------

    def push_directive(self, directive: pb.RemediationDirective) -> None:
        """Enqueue a RemediationDirective to be sent to the client."""
        env = pb.ServerEnvelope(directive=directive)
        self._send_queue.put(env)

    def push_ping(self, ping: pb.Ping) -> None:
        """Enqueue a Ping to be sent to the client."""
        env = pb.ServerEnvelope(ping=ping)
        self._send_queue.put(env)

    def set_remediation_context(self, directive_id: str, ctx: pb.RemediationContext) -> None:
        """Pre-load a RemediationContext for GetRemediationContext lookups."""
        with self._lock:
            self._context_map[directive_id] = ctx

    def stop_stream(self) -> None:
        """Signal the active Stream RPC to exit its send loop."""
        self._send_queue.put(_STOP)

    # ------------------------------------------------------------------
    # gRPC service implementation
    # ------------------------------------------------------------------

    def Stream(
        self,
        request_iterator: Iterator[pb.ClientEnvelope],
        context: grpc.ServicerContext,
    ) -> Iterator[pb.ServerEnvelope]:
        """Bidirectional streaming RPC.

        Handshake: expects Hello as first client message, yields hello_ack.
        Then enters a concurrent send/receive loop until cancelled or stopped.
        """
        hello_ack = self._do_handshake(request_iterator, context)
        if hello_ack is None:
            return
        yield hello_ack

        # Start background thread that reads incoming client messages.
        recv_thread = threading.Thread(
            target=self._receive_loop,
            args=(request_iterator, context),
            daemon=True,
        )
        recv_thread.start()

        # Main (generator) thread drives the send loop.
        yield from self._send_loop(context)
        recv_thread.join(timeout=2)

    def _do_handshake(
        self,
        request_iterator: Iterator[pb.ClientEnvelope],
        context: grpc.ServicerContext,
    ) -> pb.ServerEnvelope | None:
        """Read the first ClientEnvelope, expect Hello, return hello_ack envelope."""
        try:
            first = next(request_iterator)
        except StopIteration:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "expected Hello first")
            return None
        if not first.HasField("hello"):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "expected Hello first")
            return None
        ack = pb.ServerEnvelope(hello_ack=first.hello)
        return ack

    def _receive_loop(
        self,
        request_iterator: Iterator[pb.ClientEnvelope],
        context: grpc.ServicerContext,
    ) -> None:
        """Background thread: drain incoming ClientEnvelope messages."""
        try:
            for envelope in request_iterator:
                if not context.is_active():
                    break
                which = envelope.WhichOneof("msg")
                if which == "outcome":
                    with self._lock:
                        self.received_outcomes.append(envelope.outcome)
                elif which == "ping":
                    with self._lock:
                        self.received_pings.append(envelope.ping)
        except Exception:  # noqa: BLE001 — stream closed on client side is normal
            pass

    def _send_loop(self, context: grpc.ServicerContext) -> Iterator[pb.ServerEnvelope]:
        """Yield ServerEnvelope messages from the internal queue."""
        while context.is_active():
            try:
                item = self._send_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            if item is _STOP:
                break
            yield item  # type: ignore[misc]

    def GetRemediationContext(
        self,
        request: pb.GetRemediationContextRequest,
        context: grpc.ServicerContext,
    ) -> pb.RemediationContext:
        """Unary RPC: return pre-loaded context or NOT_FOUND."""
        with self._lock:
            ctx = self._context_map.get(request.directive_id)
        if ctx is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"no context for directive_id={request.directive_id!r}",
            )
            return pb.RemediationContext()
        return ctx


class StubControlPlaneServer:
    """Thin wrapper around a grpc.Server hosting StubControlPlaneServicer.

    Usage::

        with StubControlPlaneServer() as srv:
            channel = grpc.insecure_channel(f"127.0.0.1:{srv.port}")
            stub = pb_grpc.ControlPlaneStub(channel)
            ...
            srv.servicer.push_directive(...)
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self._host = host
        self._requested_port = port
        self._actual_port: int = 0
        self._servicer = StubControlPlaneServicer()
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        pb_grpc.add_ControlPlaneServicer_to_server(self._servicer, self._server)
        self._actual_port = self._server.add_insecure_port(f"{host}:{port}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def port(self) -> int:
        """Actual bound port (OS-assigned when port=0 was requested)."""
        return self._actual_port

    @property
    def servicer(self) -> StubControlPlaneServicer:
        """The servicer instance; use for test assertions and driving."""
        return self._servicer

    def start(self) -> None:
        """Start the gRPC server."""
        self._server.start()

    def stop(self, grace: float = 2) -> None:
        """Stop the gRPC server, waiting up to *grace* seconds."""
        self._servicer.stop_stream()
        self._server.stop(grace)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> StubControlPlaneServer:
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.stop()


if __name__ == "__main__":
    srv = StubControlPlaneServer(host="127.0.0.1", port=50051)
    srv.start()
    print("stub server ready on :50051")
    try:
        import time

        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        srv.stop()
