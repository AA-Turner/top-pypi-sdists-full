"""Inside `queue_only()` no write goes to the network, whatever the client's mode: the run-open
snapshot gate writes under a lock a close waits on, and a hung DNS lookup there held the close
(review of the Sender PR: a sync client, `PROBE_ASYNC=0`, sent straight through)."""

from __future__ import annotations

import warnings

import httpx
import pytest

from probe.sdk.client.client import Client
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.sender import queue_only
from probe.sdk.delivery.transport.transport import Transport
from probe.sdk.settings.settings import Settings

RUN = "11111111-1111-4111-8111-111111111111"


def _client(tmp_path, *, async_writes: bool | None, sent: list) -> Client:
    settings = Settings(base_url="http://test", token="ros_pat_deadbeef", workspace="ws-mine")

    def server(request: httpx.Request) -> httpx.Response:
        sent.append(f"{request.method} {request.url.path}")
        return httpx.Response(200, json={"ok": True})

    transport = Transport(settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(server)),
                          max_retries=0)
    journal = Journal(str(tmp_path / "outbox"), context={"name": None, "base_url": settings.base_url})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return Client(settings=settings, transport=transport, journal=journal, async_writes=async_writes,
                      auto_drain=False)


@pytest.mark.parametrize("async_writes", [False, None, True])
@pytest.mark.parametrize("flags", [{}, {"sync": True}])
def test_a_write_inside_queue_only_is_queued_never_sent(tmp_path, async_writes, flags):
    sent: list[str] = []
    client = _client(tmp_path, async_writes=async_writes, sent=sent)
    try:
        with queue_only():
            returned = client.write("PATCH", f"/v1/runs/{RUN}", {"env_ref": "sha256:abc"}, **flags)
        assert sent == []
        assert returned is None
        assert [op["path"] for _, op in client.journal.pending()] == [f"/v1/runs/{RUN}"]
    finally:
        client.close()


def test_outside_queue_only_a_sync_client_still_sends(tmp_path):
    sent: list[str] = []
    client = _client(tmp_path, async_writes=False, sent=sent)
    try:
        assert client.write("PATCH", f"/v1/runs/{RUN}", {"env_ref": "sha256:abc"}) == {"ok": True}
        assert sent == [f"PATCH /v1/runs/{RUN}"]
    finally:
        client.close()
