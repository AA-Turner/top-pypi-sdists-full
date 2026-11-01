"""A client's writes land in the sink its mode picks, once; reassigning the mode picks again (step 8)."""

from __future__ import annotations

import gc
import warnings
import weakref

import httpx

from probe.sdk.client.client import Client
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.sink import SinkKind
from probe.sdk.delivery.sinks.offline import OfflineClient
from probe.sdk.delivery.transport.transport import Transport
from probe.sdk.settings.settings import Settings


def _settings() -> Settings:
    return Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token="ros_ing_cafef00d",
                    hmac_secret="s3cr3t", workspace="ws-mine")


def _client(tmp_path, *, async_writes: bool) -> Client:
    settings = _settings()
    transport = Transport(settings, client=httpx.Client(
        base_url="http://test", transport=httpx.MockTransport(lambda request: httpx.Response(200, json={}))))
    journal = Journal(str(tmp_path / "outbox"), context={"name": None, "base_url": settings.base_url})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return Client(settings=settings, transport=transport, journal=journal, async_writes=async_writes,
                      auto_drain=False)


def test_an_async_client_queues_and_a_sync_client_sends(tmp_path):
    assert _client(tmp_path / "a", async_writes=True)._delivery.sink.kind is SinkKind.JOURNALED
    assert _client(tmp_path / "s", async_writes=False)._delivery.sink.kind is SinkKind.DIRECT


def test_the_sink_is_picked_once_and_again_only_when_the_mode_changes(tmp_path):
    client = _client(tmp_path, async_writes=True)
    first = client._delivery.sink
    assert client._delivery.sink is first
    client.async_writes = False
    assert client._delivery.sink.kind is SinkKind.DIRECT
    client.async_writes = True
    assert client._delivery.sink is first


def test_strict_and_sync_writes_go_out_now_even_from_the_journal_sink(tmp_path):
    client = _client(tmp_path, async_writes=True)
    sink = client._delivery.sink
    assert sink.queues(strict=False, sync=False)
    assert not sink.queues(strict=True, sync=False)
    assert not sink.queues(strict=False, sync=True)


def test_an_offline_client_lands_in_the_offline_sink(tmp_path):
    journal = Journal(str(tmp_path / "offline"), context={"name": None, "base_url": "http://test"})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        client = OfflineClient(_settings(), journal)
    assert client._delivery.sink.kind is SinkKind.OFFLINE


def test_a_client_made_without_init_still_reaches_its_sinks(tmp_path):
    double = Client.__new__(Client)
    assert double._delivery.journaled.kind is SinkKind.JOURNALED


def test_a_dropped_client_is_freed_at_once_not_at_the_next_gc(tmp_path):
    """Delivery and its sinks hold the client weakly, so no cycle keeps its HTTP pool and journal."""
    client = _client(tmp_path, async_writes=True)
    assert client._delivery.sink.kind is SinkKind.JOURNALED
    held = weakref.ref(client)
    gc.disable()
    try:
        del client
        assert held() is None
    finally:
        gc.enable()
