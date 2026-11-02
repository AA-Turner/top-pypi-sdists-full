"""The drainer kind is picked once per client (`pick_drainer`), and the worker kind's per-write
liveness probe is one non-blocking flock that is never throttled while a worker lives."""

from __future__ import annotations

import json
import os
import signal
import time

import pytest

from probe.sdk.client.client import Client
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.outbox import drainers
from probe.sdk.delivery.outbox.drainer import DrainerKind, pick_drainer
from probe.sdk.delivery.outbox.lease import _lease_is_free, _lease_path
from probe.sdk.settings.settings import Settings
from probe._shared import oscompat

from tests.conftest import make_client
from tests.fake_delivery_server import point_values, running_server, wait_for


def _settings() -> Settings:
    return Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token=None, hmac_secret=None)


@pytest.fixture
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_EXPORT_INTERVAL_SEC", raising=False)


def _client(tmp_path, **kw) -> Client:
    kw.setdefault("settings", _settings())
    kw.setdefault("journal", Journal(tmp_path / "outbox", context={"name": None, "base_url": "http://test"}))
    return Client(async_writes=True, **kw)


def test_the_default_client_picks_the_detached_worker(isolated, tmp_path):
    with _client(tmp_path) as client:
        assert client._drainer.kind is DrainerKind.WORKER


def test_a_drain_interval_picks_the_thread(isolated, tmp_path):
    with _client(tmp_path, drain_interval=0.5) as client:
        assert client._drainer.kind is DrainerKind.THREAD


def test_the_export_interval_env_picks_the_thread(isolated, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_EXPORT_INTERVAL_SEC", "0.5")
    with _client(tmp_path) as client:
        assert client._drainer.kind is DrainerKind.THREAD
        assert client._drain_interval == 0.5


def test_an_offline_client_never_takes_the_export_interval_env(isolated, tmp_path, monkeypatch):
    """Only `probe sync` delivers an offline run's queue: an env exporter only sent it through
    the offline transport, which refuses everything (the drain charges that nothing either)."""
    import warnings

    from probe.sdk.delivery.offline.client import OfflineClient

    monkeypatch.setenv("PROBE_EXPORT_INTERVAL_SEC", "0.2")
    journal = Journal(tmp_path / "offline", context={"name": None, "base_url": "http://test"})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        client = OfflineClient(_settings(), journal)
    with client:
        assert client._drainer.kind is DrainerKind.NONE
        assert client._drain_interval is None


def test_a_custom_transport_without_an_interval_picks_nobody(app, tmp_path):
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    assert client._drainer.kind is DrainerKind.NONE
    assert pick_drainer(client).kind is DrainerKind.NONE


def _held_lease(journal_dir):
    journal = Journal(journal_dir)
    journal._ensure()
    handle = open(_lease_path(journal), "a+")
    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    return handle


def test_wake_with_the_lease_held_runs_no_spawn_checks(tmp_path, monkeypatch):
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or False)
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    handle = _held_lease(tmp_path / "outbox")
    try:
        for _ in range(5):
            drainer.wake()
    finally:
        handle.close()
    assert calls == [], "a live worker's lease answers the probe: no status read, no spawn"


def test_with_the_lease_held_a_write_still_starts_the_receipt_namespace_once_a_second(tmp_path, monkeypatch):
    """Review I15: a held root lease skipped `maybe_spawn` entirely, so the queues its worker may
    not serve (the receipt namespace beside an older worker, an env credential's queue, the
    adopted ones) got no worker from any write. They are kicked at most once a second."""
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or False)
    receipts = Journal.for_receipts(Journal(tmp_path / "outbox").dir)
    receipts._ensure()
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    handle = _held_lease(tmp_path / "outbox")
    try:
        for _ in range(5):
            drainer.wake()
        assert calls == [str(receipts.dir)], "one kick of the side queue, not one per write"
        drainer.side_kicked_at -= drainers.detached.SIDE_KICK_SECONDS  # a second later
        drainer.wake()
        assert calls == [str(receipts.dir)] * 2
    finally:
        handle.close()


def test_a_side_worker_just_spawned_is_given_time_to_take_its_lease(tmp_path, monkeypatch):
    """Final review of #3794: a side queue's worker that takes over a second to start (slow
    imports on a busy box) was forked again by the next second's kick, ~0.9 CPU-s a time. After
    a side spawn the kicks wait `SIDE_SPAWN_GRACE_SECONDS`."""
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or True)
    receipts = Journal.for_receipts(Journal(tmp_path / "outbox").dir)
    receipts._ensure()
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    handle = _held_lease(tmp_path / "outbox")
    try:
        drainer.wake()
        assert calls == [str(receipts.dir)]
        drainer.side_kicked_at -= drainers.detached.SIDE_KICK_SECONDS  # a second later
        drainer.wake()
        assert calls == [str(receipts.dir)], "forked again while the first was still starting"
    finally:
        handle.close()

def test_wake_with_the_lease_free_runs_maybe_spawn_every_write(tmp_path, monkeypatch):
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or False)
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    Journal(tmp_path / "outbox")._ensure()
    drainer.wake()
    drainer.wake()
    assert len(calls) == 2, "a probe that spawned nothing must not arm the throttle"


def test_a_spawn_arms_the_throttle(tmp_path, monkeypatch):
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or True)
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    Journal(tmp_path / "outbox")._ensure()
    drainer.wake()
    drainer.wake()
    assert len(calls) == 1


def test_an_upload_waiting_for_a_promoter_still_runs_maybe_spawn(tmp_path, monkeypatch):
    """`maybe_spawn` starts a promote-only child beside an older worker that never promotes:
    a held lease alone must not skip that."""
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or False)
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    handle = _held_lease(tmp_path / "outbox")
    (tmp_path / "outbox" / "waiting" / "abc.json").write_text("{}")
    try:
        drainer.wake()
    finally:
        handle.close()
    assert len(calls) == 1


def test_a_forced_kick_skips_the_probe_and_the_throttle(tmp_path, monkeypatch):
    calls: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: calls.append(d) or True)
    drainer = drainers.detached.DetachedDrainer(tmp_path / "outbox")
    handle = _held_lease(tmp_path / "outbox")
    try:
        drainer.wake()  # held: nothing
        drainer.kick(force=True)
        drainer.kick(force=True)
    finally:
        handle.close()
    assert len(calls) == 2


def _worker_pid(queue) -> int | None:
    try:
        return int(json.loads((queue / ".worker-caps.json").read_text())["pid"])
    except (OSError, ValueError, KeyError, TypeError):
        return None


@pytest.fixture
def worker_env(monkeypatch, tmp_path):
    """What a REAL worker child inherits: an isolated config and an env token."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_process_test")
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_OUTBOX_DIR", raising=False)
    monkeypatch.delenv("PROBE_EXPORT_INTERVAL_SEC", raising=False)


def test_a_write_after_the_worker_died_is_delivered_without_finish(worker_env, tmp_path, monkeypatch):
    """Outside voice O1: worker alive at t=0, killed at t=1, one write at t=2, then silence.
    No later write and no `finish()` re-kicks it, so that write's own probe must."""
    monkeypatch.setenv("PROBE_SEND_INTERVAL_SEC", "0")
    monkeypatch.setenv("PROBE_OUTBOX_LINGER_S", "30")  # the worker stays until it is killed
    run_id = "6f1c1d1e-0000-4000-8000-000000000001"
    with running_server() as server:
        monkeypatch.setenv("PROBE_BASE_URL", server.url)
        client = Client(
            async_writes=True,
            journal=Journal(tmp_path / "outbox", context={"name": None, "base_url": server.url}),
        )
        queue = client.journal.dir
        try:
            client.write("POST", f"/v1/runs/{run_id}/metrics", _row(1.0, 0))
            assert wait_for(lambda: point_values(server) == [1.0], 30), "the first write never landed"
            assert wait_for(lambda: _worker_pid(queue) is not None, 10)
            # Settled too (its op file gone): a kill between the answer and the unlink would
            # rightly send 1.0 again, which is not what this test is about.
            assert wait_for(lambda: not list((queue / "ops").glob("*.json")), 10)
            os.kill(_worker_pid(queue), getattr(signal, "SIGKILL", signal.SIGTERM))  # t=1: the worker dies between two writes
            assert wait_for(lambda: _lease_is_free(Journal(queue)), 10)
            time.sleep(1.0)  # past the spawn throttle, as a training loop between two writes
            client.write("POST", f"/v1/runs/{run_id}/metrics", _row(2.0, 1))
            # t=2 and then silence: no write, no flush(), no finish().
            assert wait_for(lambda: point_values(server) == [1.0, 2.0], 30), f"the last write was stranded: {point_values(server)}"
        finally:
            pid = _worker_pid(queue)
            if pid:
                try:
                    os.kill(pid, getattr(signal, "SIGKILL", signal.SIGTERM))  # Windows: TerminateProcess
                except OSError:
                    pass


def _row(value: float, step: int) -> dict:
    return {"points": [{"key": "loss", "value": value, "step_index": step}]}


class _Exporter:
    def __init__(self, alive: bool) -> None:
        self.alive = alive
        self.closed = 0

    def close(self, timeout: float = 5.0) -> None:
        self.closed += 1


@pytest.mark.parametrize("alive", [True, False])
def test_a_hand_off_stops_the_exporter_through_the_drainer(isolated, tmp_path, monkeypatch, alive):
    """Review (client.py hand-off): `hand_off_delivery` closed `_exporter` itself, past the
    drainer it picked. It now goes through `Drainer.close`, which keeps a DEAD exporter in
    place (an auth block: rebuilding it would retry the rejected credential)."""
    kicks: list = []
    monkeypatch.setattr(drainers.detached, "maybe_spawn", lambda d=None: kicks.append(d) or False)
    with _client(tmp_path, drain_interval=0.5) as client:
        closes: list = []
        real_close = client._drainer.close
        monkeypatch.setattr(client._drainer, "close", lambda timeout=None: closes.append(timeout) or real_close(timeout))
        exporter = _Exporter(alive)
        client._exporter = exporter
        client.hand_off_delivery()
        assert closes == [None] and exporter.closed == 1
        assert (client._exporter is None) is alive, "only a live exporter is cleared"
        assert kicks, "and the queue is handed to a detached worker"
        client._exporter = None
