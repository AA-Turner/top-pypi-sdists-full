"""Tests for the lag-one flow delivery queue and pre/post attachment."""

import threading
from unittest.mock import MagicMock, patch

from runlayer_cli import __version__
from runlayer_cli.api import RunlayerClient
from runlayer_cli.flow_contract import (
    MAX_FLOWS_PER_ENVELOPE,
    attach_client_flows,
    build_envelope,
)
from runlayer_cli.flow_delivery import (
    FlowDeliveryQueue,
)
from runlayer_cli.models_mcp import PreRequest


def _summary(n: int) -> dict:
    return {"operation": "cli.call_tool", "status": "ok", "n": n}


class TestFlowDeliveryQueue:
    def test_drain_empty_returns_none(self):
        assert FlowDeliveryQueue().drain() is None

    def test_enqueue_drain_roundtrip(self):
        queue = FlowDeliveryQueue()
        queue.enqueue(_summary(1))
        queue.enqueue(_summary(2))
        envelope = queue.drain()
        assert envelope is not None
        assert envelope["v"] == 1
        assert envelope["cli_version"] == __version__
        assert envelope["dropped"] == 0
        assert [f["n"] for f in envelope["flows"]] == [1, 2]
        assert queue.drain() is None

    def test_drop_oldest_beyond_cap(self):
        queue = FlowDeliveryQueue()
        for n in range(MAX_FLOWS_PER_ENVELOPE + 3):
            queue.enqueue(_summary(n))
        envelope = queue.drain()
        assert envelope is not None
        assert envelope["dropped"] == 3
        assert len(envelope["flows"]) == MAX_FLOWS_PER_ENVELOPE
        assert envelope["flows"][0]["n"] == 3  # oldest three dropped

    def test_dropped_counter_resets_after_drain(self):
        queue = FlowDeliveryQueue()
        for n in range(MAX_FLOWS_PER_ENVELOPE + 1):
            queue.enqueue(_summary(n))
        queue.drain()
        queue.enqueue(_summary(99))
        envelope = queue.drain()
        assert envelope is not None
        assert envelope["dropped"] == 0

    def test_thread_safety_smoke(self):
        queue = FlowDeliveryQueue()
        drained: list[dict] = []

        def producer():
            for n in range(200):
                queue.enqueue(_summary(n))

        def consumer():
            for _ in range(50):
                envelope = queue.drain()
                if envelope:
                    drained.append(envelope)

        threads = [threading.Thread(target=producer) for _ in range(4)] + [
            threading.Thread(target=consumer) for _ in range(2)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        final = queue.drain()
        total = sum(len(e["flows"]) + e["dropped"] for e in drained)
        if final:
            total += len(final["flows"]) + final["dropped"]
        assert total == 800

    def test_build_envelope_shape(self):
        envelope = build_envelope([_summary(1)], dropped=2)
        assert set(envelope) == {"v", "cli_version", "os", "source", "flows", "dropped"}


class TestClientFlowAttachment:
    def _pre(self, client: RunlayerClient) -> dict:
        """Run client.pre against a mocked httpx.Client; return the JSON body."""
        mock_post = MagicMock(return_value=MagicMock(status_code=200))
        with patch("httpx.Client") as mock_httpx:
            mock_httpx.return_value.__enter__ = MagicMock(
                return_value=MagicMock(post=mock_post)
            )
            mock_httpx.return_value.__exit__ = MagicMock(return_value=False)
            client.pre("server-123", PreRequest(method="tools/list", params=None))
        return mock_post.call_args.kwargs["json"]

    def test_no_queue_body_unchanged(self):
        client = RunlayerClient(hostname="https://example.com", secret="k")
        body = self._pre(client)
        assert "client_flows" not in body

    def test_empty_queue_body_unchanged(self):
        client = RunlayerClient(
            hostname="https://example.com", secret="k", flow_queue=FlowDeliveryQueue()
        )
        body = self._pre(client)
        assert "client_flows" not in body

    def test_queued_flows_attached_lag_one(self):
        queue = FlowDeliveryQueue()
        queue.enqueue(_summary(1))
        client = RunlayerClient(
            hostname="https://example.com", secret="k", flow_queue=queue
        )
        body = self._pre(client)
        assert body["client_flows"]["flows"] == [_summary(1)]
        # Drained: the next request carries nothing.
        assert "client_flows" not in self._pre(client)

    def test_broken_queue_never_breaks_carrier(self):
        queue = FlowDeliveryQueue()
        queue.drain = MagicMock(side_effect=RuntimeError("boom"))  # type: ignore[method-assign]
        client = RunlayerClient(
            hostname="https://example.com", secret="k", flow_queue=queue
        )
        body = self._pre(client)
        assert "client_flows" not in body

    def test_shared_attach_helper_returns_fresh_dict_and_guards_double_attach(self):
        queue = FlowDeliveryQueue()
        queue.enqueue(_summary(1))
        original = {"method": "tools/list", "params": None}
        attached = attach_client_flows(original, queue.drain)
        # Returns a new dict; the caller's body is not mutated.
        assert "client_flows" not in original
        assert attached is not original
        # A body that already carries client_flows is left untouched (no re-drain).
        queue.enqueue(_summary(2))
        again = attach_client_flows(attached, queue.drain)
        assert again is attached
        assert again["client_flows"]["flows"] == [_summary(1)]

    def test_shared_attach_helper_handles_drain_failures(self):
        body = {"method": "tools/list"}
        assert attach_client_flows(body, None) is body

        broken_drain = MagicMock(side_effect=RuntimeError("boom"))
        assert attach_client_flows(body, broken_drain) is body

        drain = MagicMock(return_value={"flows": [_summary(1)]})
        attached = attach_client_flows(body, drain)
        assert attached is not body
        assert attached["client_flows"]["flows"] == [_summary(1)]
