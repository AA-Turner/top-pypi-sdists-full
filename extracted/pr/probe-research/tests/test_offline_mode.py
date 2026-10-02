"""`PROBE_MODE=offline` and `probe sync` (plan 2.12).

Recording makes no network call at all; a later sync with the current login
creates the run once (by its creation key), lands every write on it with the
client's own times, and closes it. The fake backend is production-shaped: it
replays a creation key, derives liveness 'offline', and keeps `started_at`.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import socket
import warnings
from collections import Counter

import httpx
import pytest

import probe
from probe import errors
from probe.sdk import fluent, offline
from probe.sdk.journal import Journal, drain
from tests.conftest import make_client


@pytest.fixture(autouse=True)
def _clean_binding(monkeypatch):
    # An offline run cannot attach, so a PROBE_RUN_ID leaked by another test
    # in this worker would refuse every init here.
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    # Record against the server the tests sync to (`make_client`'s base URL):
    # `probe sync` refuses a queue recorded against another one.
    monkeypatch.setenv("PROBE_BASE_URL", "http://test")
    fluent._current.set(None)
    fluent._process_default = None
    yield
    fluent._current.set(None)
    fluent._process_default = None


@pytest.fixture
def outbox(tmp_path, monkeypatch):
    root = tmp_path / "outbox"
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(root))
    return root


class NoNetwork:
    """Every way out of the process fails the test while armed: an online
    client, an httpx send, a socket connect. `restore()` brings the network
    back without undoing anything else the test patched."""

    def __init__(self) -> None:
        self.sent: list = []
        self._patch = pytest.MonkeyPatch()

    def arm(self) -> "NoNetwork":
        real_send = httpx.Client.send
        sent = self.sent

        def refuse_client(*_a, **_kw):
            raise AssertionError("offline init built an online Client")

        def send(client, request, *a, **kw):
            sent.append(request)
            return real_send(client, request, *a, **kw)

        def connect(*_a, **_kw):
            raise AssertionError("offline mode opened a socket")

        self._patch.setattr(fluent, "Client", refuse_client)
        self._patch.setattr(httpx.Client, "send", send)
        self._patch.setattr(socket.socket, "connect", connect)
        return self

    def restore(self) -> None:
        self._patch.undo()


@pytest.fixture
def no_network():
    guard = NoNetwork().arm()
    yield guard
    guard.restore()


def _record(n: int = 3, **kw):
    """One offline run: `n` stepped points, a span, a close."""
    run = probe.init(mode="offline", **{"project": "p1", "name": "offline-run", **kw})
    for step in range(n):
        probe.log({"loss": 1.0 / (step + 1)}, step=step)
    with probe.span("eval"):
        pass
    probe.finish()
    return run


@pytest.fixture
def lab(app):
    app.seed_experiment("e1")
    client = make_client(app)
    client.create_project("p1", "P1", kind="general")
    client.close()
    return app


def _sync(app, root=None, **kw):
    client = make_client(app)
    try:
        offline.require_server(client)
        return [offline.sync_dir(d, client, **kw) for d in offline.find_offline_dirs(root)]
    finally:
        client.close()


def _points(app, run_id):
    bodies = [
        json.loads(r.content)
        for r in app.requests
        if r.method == "POST" and r.url.path == f"/v1/runs/{run_id}/metrics"
    ]
    return [p for body in bodies for p in body["points"]]


# -- recording: no network -------------------------------------------------------
def test_recording_offline_makes_no_network_call(outbox, no_network):
    run = _record(n=50)
    assert no_network.sent == [], "nothing may be sent while offline"
    assert run.id.startswith("local:")
    assert run._client.transport.refused == 0, "not even a refused attempt"
    (directory,) = offline.find_offline_dirs()
    ops = [op for _, op in Journal(directory).pending()]
    assert ops[0]["kind"] == offline.CREATE_KIND, "the create is FIRST in the run's lane"
    assert ops[-1]["method"] == "PATCH" and ops[-1]["body"]["status"] == "completed"
    assert {op["run_ref"] for op in ops} == {run.id}
    manifest = offline.read_manifest(directory)
    assert manifest["creation_key"] == run.id.split(":", 1)[1]


def test_the_detached_worker_never_drains_an_offline_queue(outbox, no_network, app):
    """Isolation: the machine-wide drain works on the outbox root only."""
    _record()
    client = make_client(app)
    report = drain(Journal(outbox), client_factory=lambda _ctx: client)
    assert report.delivered == 0
    assert app.runs == {}
    (directory,) = offline.find_offline_dirs()
    assert Journal(directory).pending(), "the offline queue is untouched"


def test_disabled_and_offline_refuse_to_attach(outbox, monkeypatch):
    monkeypatch.setenv("PROBE_RUN_ID", "some-run")
    with pytest.raises(errors.ValidationError, match="PROBE_RUN_ID"):
        probe.init(mode="offline", project="p1")


@pytest.mark.parametrize("policy", ["auto", "resume"])
def test_offline_refuses_a_conflict_policy_it_cannot_honour(outbox, policy):
    with pytest.raises(errors.ValidationError, match="offline"):
        probe.init(mode="offline", project="p1", on_conflict=policy)


# -- syncing ----------------------------------------------------------------------
def test_a_thousand_logs_sync_as_one_run_with_client_times(outbox, no_network, lab, monkeypatch):
    run = _record(n=1000)
    local_start = offline.read_manifest(offline.find_offline_dirs()[0])["recorded_at"]
    no_network.restore()  # the network is back
    (result,) = _sync(lab)

    assert result["clean"], result
    assert len(lab.runs) == 1
    (row,) = lab.runs.values()
    assert result["run_id"] == row["id"]
    assert row["liveness_mode"] == "offline"
    assert row["started_at"] == local_start, "the client's start, not the sync time"
    assert row["status"] == "completed"
    assert sorted(p["step_index"] for p in _points(lab, row["id"])) == list(range(1000))
    create = next(r for r in lab.requests if r.method == "POST" and r.url.path.endswith("/runs"))
    assert json.loads(create.content)["creation_key"] == run.id.split(":", 1)[1]
    finish = [
        json.loads(r.content)
        for r in lab.requests
        if r.method == "PATCH" and r.url.path == f"/v1/runs/{row['id']}"
    ]
    assert finish[-1]["ended_at"] >= local_start
    assert all("local:" not in r.url.path for r in lab.requests)


def test_syncing_twice_does_not_duplicate(outbox, no_network, lab, monkeypatch):
    _record()
    no_network.restore()
    _sync(lab)
    before = len(lab.requests)
    (again,) = _sync(lab)
    assert again["clean"] and again["delivered"] == 0
    assert len(lab.runs) == 1
    assert [r for r in lab.requests[before:] if r.method == "POST" and r.url.path.endswith("/runs")] == []


def test_two_copies_of_one_queue_sync_into_one_run(outbox, no_network, lab, tmp_path, monkeypatch):
    """A queue copied off an air-gapped node and synced from two machines."""
    _record(n=5)
    (directory,) = offline.find_offline_dirs()
    copy = tmp_path / "copied" / directory.name
    shutil.copytree(directory, copy)
    no_network.restore()
    (first,) = _sync(lab)
    delivered_first = _points(lab, first["run_id"])
    (second,) = _sync(lab, copy)
    assert first["clean"] and second["clean"], second
    assert len(lab.runs) == 1
    assert first["run_id"] == second["run_id"]
    # COUNTS, not a set: a set would read 5 whether each point went out once,
    # twice or ten times. The first sync sends each of the 5 exactly once; the
    # copy, which cannot know the first went out, re-sends each exactly once
    # more, and the server keeps a stepped point first-write-wins on its
    # (step, key) identity, so the run still holds 5 (app/telemetry/store.py).
    assert len(delivered_first) == 5
    sent = Counter((p["step_index"], p["key"], p["value"]) for p in _points(lab, first["run_id"]))
    assert len(sent) == 5 and set(sent.values()) == {2}, sent


def test_a_crash_between_create_and_mapping_replays_the_create(outbox, no_network, lab, monkeypatch):
    _record()
    no_network.restore()
    real = offline._write_mapping
    calls = []

    def crash_once(*a, **kw):
        calls.append(a)
        if len(calls) == 1:
            raise OSError("killed before the mapping reached disk")
        return real(*a, **kw)

    monkeypatch.setattr(offline, "_write_mapping", crash_once)
    (first,) = _sync(lab)
    assert not first["clean"]
    assert len(lab.runs) == 1, "the create landed; its mapping did not"
    (second,) = _sync(lab)
    assert second["clean"], second
    assert len(lab.runs) == 1, "the replayed create found the same run"


def test_a_missing_project_dead_letters_with_the_override_hint(outbox, no_network, lab, monkeypatch):
    _record(project="gone-project")
    no_network.restore()
    (result,) = _sync(lab)
    assert not result["clean"]
    assert lab.runs == {}
    assert any("probe sync --project" in e for e in result["errors"])
    (directory,) = offline.find_offline_dirs()
    assert [op["kind"] for _, op in Journal(directory).failed()] == [offline.CREATE_KIND]
    assert Journal(directory).pending(), "the run's data waits for its create"

    (fixed,) = _sync(lab, project="p1")
    assert fixed["clean"], fixed
    (row,) = lab.runs.values()
    assert row["status"] == "completed"


def test_sync_refuses_another_tenant(outbox, no_network, lab, monkeypatch):
    _record()
    (directory,) = offline.find_offline_dirs()
    manifest = offline.read_manifest(directory)
    manifest["customer_id"] = "another-team"
    (directory / offline.MANIFEST_NAME).write_text(json.dumps(manifest))
    no_network.restore()
    client = make_client(lab)
    me = client.me()
    with pytest.raises(errors.ScopeError, match="another-team"):
        offline.sync_dir(directory, client)
    assert me.get("customer_id") != "another-team"
    assert lab.runs == {}


def test_sync_refuses_a_server_without_offline_create(outbox, no_network, lab, monkeypatch):
    _record()
    no_network.restore()
    lab.supports_offline_create = False
    client = make_client(lab)
    with pytest.raises(errors.CapabilityUnavailable):
        offline.require_server(client)


def test_an_artifact_recorded_offline_is_staged_and_uploaded_at_sync(
    outbox, no_network, lab, tmp_path, monkeypatch
):
    ckpt = tmp_path / "ckpt.bin"
    ckpt.write_bytes(b"weights" * 100)
    run = probe.init(mode="offline", project="p1", name="with-artifact")
    run.log_artifact("ckpt", path=str(ckpt))
    probe.finish()
    ckpt.unlink()  # the queue must be self-contained
    no_network.restore()
    (result,) = _sync(lab)
    assert result["clean"], result
    (row,) = lab.runs.values()
    stored = lab.artifacts.get(row["id"], [])
    assert len(stored) == 1, "the staged bytes landed on the synced run"
    assert not stored[0].get("is_reference"), "an upload, not a pointer to a gone file"


def test_supersede_opens_rN_at_sync_and_replays_the_same_slot(outbox, lab):
    online = make_client(lab)
    online.run(project="p1", name="first", external_id="job-1", heartbeat=False)
    online.close()
    guard = NoNetwork().arm()
    try:
        _record(external_id="job-1", on_conflict="supersede")
    finally:
        guard.restore()  # never leak the trap into the rest of the worker
    (result,) = _sync(lab)
    assert result["clean"], result
    (again,) = _sync(lab)
    assert again["clean"] and len(lab.runs) == 2, "a re-sync replays the same -r2 slot"
    assert result["clean"], result
    externals = sorted(r["external_id"] for r in lab.runs.values())
    assert externals == ["job-1", "job-1-r2"]


# -- the init fallback ---------------------------------------------------------------
class _Clock:
    def __init__(self):
        self.now = 50.0

    def monotonic(self):
        return self.now

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += max(0.0, seconds)


def test_init_falls_back_offline_and_replays_the_exact_lost_create(
    outbox, app, tmp_path, monkeypatch
):
    """The create LANDED and its answer was lost; then the API stayed down.
    The offline queue replays that exact request, so the sync finds the run the
    server already has instead of making a second one."""
    from probe.sdk import transport

    app.seed_experiment("e1")
    monkeypatch.setattr(transport, "time", _Clock())
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "5")
    monkeypatch.setenv("PROBE_INIT_FALLBACK", "offline")
    real = app.handler
    state = {"down": False}

    def flaky(request):
        if state["down"]:
            raise httpx.ConnectError("refused", request=request)
        if request.method == "POST" and request.url.path.endswith("/runs"):
            real(request)  # committed...
            state["down"] = True  # ...and the API goes away with the answer
            raise httpx.ReadTimeout("lost", request=request)
        return real(request)

    app.handler = flaky
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "s"))
    run = probe.init(experiment="e1", name="r1")
    assert run.id.startswith("local:")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert len(app.runs) == 1, "the lost create is on the server"

    app.handler = real
    (result,) = _sync(app)
    assert result["clean"], result
    assert len(app.runs) == 1, "replayed, not duplicated"
    (row,) = app.runs.values()
    assert row["status"] == "completed"
    assert [p["step_index"] for p in _points(app, row["id"])] == [0]


def test_without_the_fallback_init_still_raises(outbox, app, monkeypatch):
    from probe.sdk import transport

    monkeypatch.setattr(transport, "time", _Clock())
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "2")

    def down(request):
        raise httpx.ConnectError("refused", request=request)

    app.handler = down
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app))
    with pytest.raises(errors.TransportError):
        probe.init(experiment="e1")
    assert offline.find_offline_dirs() == []


def test_a_refusal_never_falls_back(outbox, app, monkeypatch):
    monkeypatch.setenv("PROBE_INIT_FALLBACK", "offline")
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app))
    with pytest.raises(errors.NotFoundError):
        probe.init(project="no-such-project")
    assert offline.find_offline_dirs() == []


# -- the CLI --------------------------------------------------------------------------
def test_probe_sync_lists_then_delivers(outbox, no_network, lab, monkeypatch, capsys):
    from probe import cli

    _record()
    no_network.restore()
    capsys.readouterr()  # the recording's own notices
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))

    assert cli.main(["sync", "--list"]) == 2
    listed = json.loads(capsys.readouterr().out)
    assert [r["state"] for r in listed] == ["unsynced"]

    assert cli.main(["sync"]) == 0
    synced = json.loads(capsys.readouterr().out)
    assert synced[0]["state"] == "synced" and synced[0]["run_id"] in lab.runs

    assert cli.main(["sync", "--list"]) == 0
    assert [r["state"] for r in json.loads(capsys.readouterr().out)] == ["synced"]


# -- torchrun / SLURM: `probe sync` finds what a rank recorded -------------------------
@pytest.mark.parametrize("rank_var", ["RANK", "SLURM_PROCID"])
def test_probe_sync_finds_a_run_a_torchrun_or_slurm_rank_recorded(
    tmp_path, monkeypatch, no_network, lab, capsys, rank_var
):
    """Under torchrun/SLURM the outbox is per rank (`<outbox>/rank-0/`), and the
    offline queue used to land inside it, where `probe sync` -- run on a login
    node, with no RANK set -- never looked: `probe sync --list` printed [] and
    exited 0."""
    from probe import cli

    monkeypatch.delenv("PROBE_OUTBOX_DIR", raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for var in ("RANK", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK", "LOCAL_RANK"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv(rank_var, "0")
    _record()
    monkeypatch.delenv(rank_var)  # the sync runs where no rank is set
    no_network.restore()
    capsys.readouterr()
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))

    assert cli.main(["sync", "--list"]) == 2
    assert [r["state"] for r in json.loads(capsys.readouterr().out)] == ["unsynced"]
    assert cli.main(["sync"]) == 0
    (row,) = lab.runs.values()
    assert row["status"] == "completed"


def test_probe_sync_also_scans_every_rank_outbox(outbox, no_network, monkeypatch):
    """A queue under a rank's own outbox (`<outbox>/rank-3/offline/<key>`) --
    recorded with that rank dir as PROBE_OUTBOX_DIR, or by an SDK that put
    offline runs there -- is found from the outbox root."""
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(outbox / "rank-3"))
    _record()
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(outbox))
    (found,) = offline.find_offline_dirs()
    assert found.parent == outbox / "rank-3" / offline.OFFLINE_DIRNAME


@pytest.mark.parametrize("args", [["sync"], ["sync", "--list"]], ids=["sync", "list"])
def test_probe_sync_with_nothing_found_says_where_it_looked_and_exits_1(outbox, capsys, args):
    from probe import cli

    assert cli.main(args) == 1
    err = capsys.readouterr().err
    assert "no offline runs found" in err
    assert str(outbox / "offline") in err and "rank-*" in err


# -- a long offline run: the op ceiling ------------------------------------------------
def test_a_long_offline_run_is_not_cut_off_by_the_op_ceiling(outbox, no_network, lab, monkeypatch):
    """Nothing drains an offline queue until `probe sync`, so the ceiling meant
    for a stalled drainer (PROBE_OUTBOX_MAX_PENDING, 500k) used to drop every
    point past it -- and the close with them."""
    from probe.sdk import journal as journal_module

    monkeypatch.setattr(journal_module, "MAX_PENDING_OPS", 10)
    _record(n=50)
    (directory,) = offline.find_offline_dirs()
    ops = [op for _, op in Journal(directory).pending()]
    assert len(ops) > 10
    assert ops[-1]["method"] == "PATCH" and ops[-1]["body"]["status"] == "completed"
    # Control: an ordinary queue with the same ceiling still refuses.
    ordinary = Journal(outbox / "ordinary")
    with pytest.raises(journal_module.OutboxFull):
        for i in range(11):
            ordinary.append_http("POST", "/v1/runs/r/metrics", {"points": [{"i": i}]}, run_ref="r")
    no_network.restore()
    (result,) = _sync(lab)
    assert result["clean"], result
    (row,) = lab.runs.values()
    assert row["status"] == "completed"
    assert sorted(p["step_index"] for p in _points(lab, row["id"])) == list(range(50))


def test_an_offline_run_on_a_full_disk_still_queues_its_close(outbox, no_network, monkeypatch):
    """The free-space floor still protects the disk (points are refused there,
    with a recorded gap), but the close is the one op it never refuses."""
    from probe.sdk import journal as journal_module

    monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 10**18)
    _record(n=5)
    (directory,) = offline.find_offline_dirs()
    ops = [op for _, op in Journal(directory).pending()]
    assert not [op for op in ops if str(op.get("path", "")).endswith("/metrics")], "the floor held"
    assert ops[-1]["method"] == "PATCH" and ops[-1]["body"]["status"] == "completed"


# -- the init fallback: freeze only a create that may have landed ----------------------
def _offline_create(directory) -> dict:
    (op,) = [op for _, op in Journal(directory).pending() if op["kind"] == offline.CREATE_KIND]
    return op["create"]


def _fallback_env(monkeypatch):
    from probe.sdk import transport

    monkeypatch.setattr(transport, "time", _Clock())
    monkeypatch.setenv("PROBE_INIT_TIMEOUT_SEC", "5")
    monkeypatch.setenv("PROBE_INIT_FALLBACK", "offline")


def test_a_fallback_whose_create_never_left_records_a_real_offline_create(
    outbox, app, tmp_path, monkeypatch
):
    """Every attempt at the create was refused: it never left this machine, so
    nothing can be on the server. The queue used to replay the ONLINE body --
    a heartbeat-owned run the reaper may call crashed mid-sync, started at the
    sync, ended before it started. It records a real offline create instead,
    under the key the online create used."""
    app.seed_experiment("e1")
    _fallback_env(monkeypatch)
    real = app.handler
    sent: list[dict] = []

    def refuse_creates(request):
        if request.method == "POST" and request.url.path.endswith("/runs"):
            sent.append(json.loads(request.content))
            raise httpx.ConnectError("refused", request=request)
        return real(request)

    app.handler = refuse_creates
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "s"))
    run = probe.init(experiment="e1", name="r1")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert run.id.startswith("local:") and sent and app.runs == {}
    (directory,) = offline.find_offline_dirs()
    create = _offline_create(directory)
    assert create["body"]["offline"] is True and "heartbeat" not in create["body"]
    assert create["creation_key"] == sent[0]["creation_key"]
    assert create["request"]["body"] == sent[0], "the sent request is kept, byte for byte"
    recorded = offline.read_manifest(directory)["recorded_at"]

    app.handler = real
    before = len(app.requests)
    (result,) = _sync(app)
    assert result["clean"], result
    (row,) = app.runs.values()
    assert row["liveness_mode"] == "offline"
    assert row["started_at"] == recorded, "the real start, not the sync time"
    assert row["status"] == "completed" and row["ended_at"] >= row["started_at"]
    creates = [
        json.loads(r.content)
        for r in app.requests[before:]
        if r.method == "POST" and r.url.path.endswith("/runs")
    ]
    assert [c.get("offline") for c in creates] == [True], "the kept request was never replayed"


def test_a_fallback_after_a_refused_create_does_not_replay_the_refusal(
    outbox, lab, tmp_path, monkeypatch
):
    """The server REFUSED the create (a real 409: the external_id is taken),
    then the API went away while init resolved the conflict. The refused
    request used to be frozen: replayed at sync, refused again, and the run's
    data stranded behind it (and `--project` cannot move a frozen create)."""
    online = make_client(lab)
    online.run(project="p1", name="first", external_id="job-1", heartbeat=False)
    online.close()
    _fallback_env(monkeypatch)
    real = lab.handler
    state = {"down": False}

    def refuse_then_go_down(request):
        if state["down"]:
            raise httpx.ConnectError("refused", request=request)
        response = real(request)
        if request.method == "POST" and request.url.path.endswith("/runs"):
            assert response.status_code == 409
            state["down"] = True
        return response

    lab.handler = refuse_then_go_down
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    run = probe.init(project="p1", name="second", external_id="job-1", on_conflict="supersede")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert run.id.startswith("local:")
    create = _offline_create(offline.find_offline_dirs()[0])
    assert create["body"]["offline"] is True and create["on_conflict"] == "supersede"

    lab.handler = real
    (result,) = _sync(lab)
    assert result["clean"], result
    assert sorted(r["external_id"] for r in lab.runs.values()) == ["job-1", "job-1-r2"]
    (retry,) = [r for r in lab.runs.values() if r["external_id"] == "job-1-r2"]
    assert [p["step_index"] for p in _points(lab, retry["id"])] == [0]


def test_a_create_lost_then_refused_is_found_by_its_key_at_sync(outbox, app, tmp_path, monkeypatch):
    """The server already declared creation keys, so the transport retried the
    create like a read: the first attempt LANDED and lost its answer, every
    later one was refused. The failure init sees is a refused connection, but
    the run is on the server: at sync the offline create is told its key is
    taken, and the kept request, replayed exactly, finds that run."""
    app.seed_experiment("e1")
    _fallback_env(monkeypatch)
    real = app.handler
    state = {"down": False}

    def land_then_go_down(request):
        if state["down"]:
            raise httpx.ConnectError("refused", request=request)
        if request.method == "POST" and request.url.path.endswith("/runs"):
            real(request)
            state["down"] = True
            raise httpx.ReadTimeout("lost", request=request)
        return real(request)

    def knows_creation_keys(*_a, **_k):
        client = make_client(app, tmp_spool=tmp_path / "s")
        assert client.supports_feature("run_creation_key")  # cached: creates retry like reads
        return client

    app.handler = land_then_go_down
    monkeypatch.setattr(fluent, "Client", knows_creation_keys)
    probe.init(experiment="e1", name="r1")
    probe.finish()
    assert len(app.runs) == 1
    (directory,) = offline.find_offline_dirs()
    assert _offline_create(directory).get("request") is not None

    app.handler = real
    (result,) = _sync(app)
    assert result["clean"], result
    assert len(app.runs) == 1, "replayed, not duplicated"
    key = offline.read_manifest(directory)["creation_key"]
    assert offline.read_mapping(directory)[key]["via"] == "online"
    assert any("reached the server online" in w for w in result["warnings"]), result


def test_init_never_replays_a_create_an_earlier_init_left(outbox, app, monkeypatch):
    """A client reused across inits keeps what its last failed create left; an
    init that fails before any create of its own must not freeze that one."""
    _fallback_env(monkeypatch)

    def down(request):
        raise httpx.ConnectError("refused", request=request)

    app.handler = down
    client = make_client(app)
    stale = "stale" * 4
    client._last_run_create = {
        "path": "/v1/runs",
        "body": {"name": "earlier", "creation_key": stale},
        "landed": False,
    }
    run = probe.init(client=client, experiment="e1", name="r2")
    probe.finish()
    assert run.id.startswith("local:")
    create = _offline_create(offline.find_offline_dirs()[0])
    assert "request" not in create and create["creation_key"] != stale


# -- identity and the process's warning state ------------------------------------------
def test_a_run_recorded_with_no_known_team_syncs_but_says_so(
    outbox, no_network, lab, monkeypatch, capsys
):
    from probe import cli

    _record()
    (directory,) = offline.find_offline_dirs()
    assert offline.read_manifest(directory)["customer_id"] is None, "precondition: never reached the API"
    assert _offline_create(directory)["body"]["metadata"]["offline_owner"] == offline.UNKNOWN_OWNER
    no_network.restore()
    capsys.readouterr()
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))
    assert cli.main(["sync"]) == 0
    out = capsys.readouterr()
    (result,) = json.loads(out.out)
    assert any("unknown" in w for w in result["warnings"]), result
    assert "the team it was recorded for is unknown" in out.err
    (row,) = lab.runs.values()
    assert row["metadata"]["offline_owner"] == offline.UNKNOWN_OWNER


def test_opening_an_offline_run_leaves_the_process_warning_filters_alone(
    outbox, no_network, monkeypatch
):
    """`warnings.catch_warnings()` swaps the PROCESS-WIDE filter list (and is not
    thread-safe): while an offline client was built, every other thread's
    warnings were silenced. The client says it drains by hand instead."""
    from probe.sdk.client import Client

    seen: list = []
    real_init = Client.__init__

    def spy(self, *a, **kw):
        seen.append(warnings.filters)
        return real_init(self, *a, **kw)

    monkeypatch.setattr(Client, "__init__", spy)
    before = warnings.filters
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        inside = warnings.filters
        _record()
    assert seen and all(filters is inside for filters in seen), "the filters were swapped"
    assert warnings.filters is before
    assert not [w for w in caught if "no background drainer" in str(w.message)]


# -- config updates recorded offline (re-review MED-1) ----------------------------------
def test_config_updates_recorded_offline_land_at_sync(outbox, no_network, lab, capsys):
    """`update_config`, `run.config.x = ...` and `run.config.update(...)` used
    to be dropped offline with a warning blaming the server: the offline client
    answered "unsupported" to every feature. They queue now, and the syncing
    server stores them."""
    run = probe.init(mode="offline", project="p1", name="cfg", config={"a": 1})
    probe.update_config({"lr": 0.1})
    run.config.bs = 32
    run.config.update({"opt": "adam"})
    probe.log({"loss": 1.0}, step=0)
    probe.finish()
    assert "cannot merge" not in capsys.readouterr().err
    assert run.config["lr"] == 0.1 and run.config["bs"] == 32
    no_network.restore()
    (result,) = _sync(lab)
    assert result["clean"], result
    (row,) = lab.runs.values()
    assert row["config"] == {"a": 1, "lr": 0.1, "bs": 32, "opt": "adam"}


def test_config_updates_a_sync_server_cannot_merge_are_reported(outbox, no_network, lab):
    """The server decides at sync. One without `run_config_merge` would answer
    200 and drop the field: the sync says so and is not clean."""
    run = probe.init(mode="offline", project="p1", name="cfg", config={"a": 1})
    run.config.bs = 32
    probe.finish()
    no_network.restore()
    lab.supports_config_merge = False
    (result,) = _sync(lab)
    assert not result["clean"]
    assert any("run_config_merge" in w and "1 config update" in w for w in result["warnings"]), result


def test_refresh_on_an_offline_run_is_a_no_op(outbox, no_network):
    run = probe.init(mode="offline", project="p1", name="r")
    assert run.refresh() is run
    assert run._client.transport.refused == 0
    probe.finish()


# -- the fallback and on_conflict's default (re-review MED-2) ---------------------------
def _crashed_incumbent(lab, external_id="job-1"):
    online = make_client(lab)
    first = online.run(project="p1", name="first", external_id=external_id, heartbeat=False)
    online.close()
    lab.runs[first.id]["status"] = "crashed"
    return first.id


def _down(request):
    raise httpx.ConnectError("refused", request=request)


def test_the_fallback_refuses_an_external_id_left_on_the_default_conflict_policy(
    outbox, lab, tmp_path, monkeypatch, capsys
):
    """Online, the default ("auto") RESUMES a crashed run of the same
    external_id -- a SLURM requeue. The fallback used to record it offline as
    on_conflict='error', so the sync hit a 409 and stranded the run. Offline
    cannot resume, so the fallback does not engage and init raises its own
    failure, naming the choice."""
    _crashed_incumbent(lab)
    _fallback_env(monkeypatch)
    lab.handler = _down
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    with pytest.warns(UserWarning, match=r"on_conflict \('auto'\).*supersede"):
        with pytest.raises(errors.TransportError):
            probe.init(project="p1", name="second", external_id="job-1")
    assert offline.find_offline_dirs() == []


def test_the_fallback_records_an_external_id_with_an_explicit_policy(outbox, lab, tmp_path, monkeypatch):
    """Control: the caller said what a collision means, so the fallback engages
    and the sync delivers the run as a retry of the crashed one, with the
    lineage an online supersede records."""
    incumbent = _crashed_incumbent(lab)
    _fallback_env(monkeypatch)
    real = lab.handler
    lab.handler = _down
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    run = probe.init(project="p1", name="second", external_id="job-1", on_conflict="supersede")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert run.id.startswith("local:")
    lab.handler = real
    (result,) = _sync(lab)
    assert result["clean"], result
    (retry,) = [r for r in lab.runs.values() if r["external_id"] == "job-1-r2"]
    assert retry["foreign_keys"] == {"retry_of": incumbent, "retry_attempt": 2}
    assert "superseded" in lab.runs[incumbent]["tags"]


def test_a_refused_offline_create_names_a_fix_that_works(outbox, lab, monkeypatch, capsys):
    """PROBE_MODE=offline with an external_id a crashed run already holds: the
    sync is refused with the incumbent named and `--on-conflict supersede` as
    the fix -- which then delivers it (the old hint named `--project`, which
    cannot help a 409)."""
    from probe import cli

    incumbent = _crashed_incumbent(lab)
    guard = NoNetwork().arm()
    try:
        _record(external_id="job-1")
    finally:
        guard.restore()
    (directory,) = offline.find_offline_dirs()
    (refused,) = _sync(lab)
    assert not refused["clean"]
    assert any("--on-conflict supersede" in e and incumbent in e and "crashed" in e for e in refused["errors"])
    assert [op["kind"] for _, op in Journal(directory).failed()] == [offline.CREATE_KIND]

    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))
    capsys.readouterr()
    assert cli.main(["sync", "--on-conflict", "supersede"]) == 0, capsys.readouterr().err
    (retry,) = [r for r in lab.runs.values() if r["external_id"] == "job-1-r2"]
    assert retry["status"] == "completed"
    assert [p["step_index"] for p in _points(lab, retry["id"])] == [0, 1, 2]
    assert retry["foreign_keys"]["retry_of"] == incumbent


def test_a_create_refused_on_a_retry_is_not_dropped_as_delivered(outbox, lab, monkeypatch):
    """The drain reads a 409 naming `existing_id` on a RETRIED op as that op's
    own earlier delivery and drops it. A create refused only on its second
    attempt (the first hit a transient error) used to vanish that way with no
    mapping, stranding every write behind it for good."""
    _crashed_incumbent(lab)
    guard = NoNetwork().arm()
    try:
        _record(external_id="job-1")
    finally:
        guard.restore()
    (directory,) = offline.find_offline_dirs()
    from probe.sdk import transport

    monkeypatch.setattr(transport, "time", _Clock())
    real = lab.handler

    def busy(request):
        if request.method == "POST" and request.url.path.endswith("/runs"):
            return httpx.Response(503, json={"detail": "busy"})
        return real(request)

    lab.handler = busy
    (first,) = _sync(lab)
    assert not first["clean"]
    ((_, create),) = [(p, op) for p, op in Journal(directory).pending() if op["kind"] == offline.CREATE_KIND]
    assert create["attempts"] >= 1, "precondition: the create was tried and kept"
    lab.handler = real
    (second,) = _sync(lab)
    assert not second["clean"]
    assert [op["kind"] for _, op in Journal(directory).failed()] == [offline.CREATE_KIND]
    assert Journal(directory).pending(), "its writes wait behind it"
    assert any("--on-conflict supersede" in e for e in second["errors"])


# -- the fallback's sent create: the server decides (re-review MED-3) -------------------
def test_a_gateway_503_outage_records_a_real_offline_run(outbox, lab, tmp_path, monkeypatch):
    """The API is down and the load balancer answers 503 to EVERY request.
    Nothing reached the app, but a 503 "may have landed", so the online body
    used to be frozen and replayed at sync: a heartbeat-owned run started at
    sync time, its end clamped to it (duration 0). The offline create goes
    first now and, its key being free, IS the run."""
    _fallback_env(monkeypatch)
    real = lab.handler
    lab.handler = lambda request: httpx.Response(503, text="no healthy upstream", request=request)
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    run = probe.init(name="lb")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert run.id.startswith("local:")
    (directory,) = offline.find_offline_dirs()
    recorded = offline.read_manifest(directory)["recorded_at"]
    lab.handler = real
    before = len(lab.requests)
    (result,) = _sync(lab)
    assert result["clean"], result
    (row,) = lab.runs.values()
    assert row["liveness_mode"] == "offline"
    assert row["started_at"] == recorded, "the real start, not the sync time"
    creates = [
        json.loads(r.content)
        for r in lab.requests[before:]
        if r.method == "POST" and r.url.path.endswith("/runs")
    ]
    assert len(creates) == 1 and creates[0]["offline"] is True and "heartbeat" not in creates[0]


def test_a_create_committed_behind_a_gateway_503_is_found_not_duplicated(
    outbox, lab, tmp_path, monkeypatch
):
    """The other half: the app COMMITTED the create and the gateway still
    answered 503. The offline create is told the key is taken (422
    creation_key_reused); the kept request, replayed exactly, finds the run."""
    _fallback_env(monkeypatch)
    real = lab.handler
    state = {"down": False}

    def commit_then_503(request):
        if state["down"]:
            return httpx.Response(503, text="no healthy upstream", request=request)
        if request.method == "POST" and request.url.path.endswith("/runs"):
            real(request)
            state["down"] = True
            return httpx.Response(503, text="no healthy upstream", request=request)
        return real(request)

    lab.handler = commit_then_503
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    probe.init(project="p1", name="lb")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert len(lab.runs) == 1
    lab.handler = real
    (result,) = _sync(lab)
    assert result["clean"], result
    assert len(lab.runs) == 1, "one run: the key's"
    (row,) = lab.runs.values()
    assert row["status"] == "completed"
    assert [p["step_index"] for p in _points(lab, row["id"])] == [0]


def test_the_fallback_does_not_engage_after_a_create_that_landed(outbox, app, tmp_path, monkeypatch, capsys):
    """init failed AFTER its create came back: the run is on the server, and an
    offline copy under a fresh key would be a second run."""
    from probe.sdk.client import Client

    app.seed_experiment("e1")
    _fallback_env(monkeypatch)

    def announce_fails(run):
        raise errors.TransportError("the API went away after the create")

    monkeypatch.setattr(Client, "_opened", staticmethod(announce_fails))
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "s"))
    with pytest.warns(UserWarning, match="second run"):
        with pytest.raises(errors.TransportError):
            probe.init(experiment="e1", name="r1")
    assert len(app.runs) == 1
    assert offline.find_offline_dirs() == [], "no second, offline run"


# -- writes dropped while recording (re-review LOW-4) ------------------------------------
def test_writes_the_disk_floor_dropped_are_on_the_close_and_in_the_sync_report(
    outbox, no_network, lab, monkeypatch, capsys
):
    from probe.sdk import journal as journal_module

    run = probe.init(mode="offline", project="p1", name="floor")
    monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 10**18)
    for step in range(5):
        probe.log({"loss": 1.0}, step=step)
    with pytest.warns(UserWarning, match=r"probe_finish\.dropped_writes=5"):
        result = probe.finish()
    assert result["dropped_writes"] == 5
    (directory,) = offline.find_offline_dirs()
    close = [op for _, op in Journal(directory).pending()][-1]["body"]
    assert close["summary_metrics"]["probe_finish"]["dropped_writes"] == 5
    monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 0)
    no_network.restore()
    (synced,) = _sync(lab)
    assert synced["state"] == "synced" and not synced["clean"]
    assert synced["dropped_writes"] == 5
    assert any("5 write(s) were dropped while recording" in w for w in synced["warnings"])
    assert run.id.startswith("local:")


# -- where it was recorded (re-review LOW-5) ---------------------------------------------
def test_sync_refuses_a_queue_recorded_against_another_server(outbox, no_network, lab, monkeypatch):
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.elsewhere.example")
    _record()
    no_network.restore()
    (directory,) = offline.find_offline_dirs()
    client = make_client(lab)
    with pytest.raises(errors.ScopeError, match="api.elsewhere.example"):
        offline.sync_dir(directory, client)
    assert lab.runs == {}
    allowed = offline.sync_dir(directory, client, allow_mismatch=True)
    assert allowed["clean"] and any("--allow-mismatch" in w for w in allowed["warnings"])


def test_sync_refuses_another_login_context_when_the_team_is_unknown(outbox, no_network, lab, monkeypatch):
    _record()
    no_network.restore()
    (directory,) = offline.find_offline_dirs()
    monkeypatch.setattr(offline, "_context_name", lambda: "another-team-login")
    client = make_client(lab)
    with pytest.raises(errors.ScopeError, match=re.escape("`probe wizard --action account`")):
        offline.sync_dir(directory, client)
    # Control: with the recorded team known, the tenant check decides and a
    # renamed context is only mentioned.
    manifest = offline.read_manifest(directory)
    manifest["customer_id"] = client.me()["customer_id"]
    (directory / offline.MANIFEST_NAME).write_text(json.dumps(manifest))
    result = offline.sync_dir(directory, client)
    assert result["clean"] and any("login context" in w for w in result["warnings"])


# -- the re-filing flags' scope (re-review LOW-6) ----------------------------------------
def test_sync_project_in_a_scan_moves_only_refused_runs(outbox, no_network, lab, monkeypatch, capsys):
    from probe import cli

    lab_client = make_client(lab)
    lab_client.create_project("p2", "P2", kind="general")
    lab_client.close()
    _record(name="orphan", project="gone-project")
    no_network.restore()
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))
    assert cli.main(["sync"]) == 2  # the orphan's create is refused
    guard = NoNetwork().arm()
    try:
        _record(name="healthy")  # recorded later, never synced yet
    finally:
        guard.restore()
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))
    capsys.readouterr()
    assert cli.main(["sync", "--project", "p2"]) == 0, capsys.readouterr().err
    homes = {r["name"]: r.get("project_id") for r in lab.runs.values()}
    ids = make_client(lab)
    p1, p2 = (ids.resolve_or_raise("project", slug)["id"] for slug in ("p1", "p2"))
    assert homes == {"healthy": p1, "orphan": p2}, "the healthy run kept the project it was recorded for"


def test_sync_project_on_a_named_folder_moves_that_run(outbox, no_network, lab, monkeypatch, capsys):
    from probe import cli

    lab_client = make_client(lab)
    p2 = lab_client.create_project("p2", "P2", kind="general")
    lab_client.close()
    _record(name="moved")
    (directory,) = offline.find_offline_dirs()
    no_network.restore()
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))
    capsys.readouterr()
    assert cli.main(["sync", str(directory), "--project", "p2"]) == 0, capsys.readouterr().err
    (row,) = lab.runs.values()
    assert row["project_id"] == p2["id"]


# -- second re-review LOWs ----------------------------------------------------------------
def test_a_fallback_create_whose_project_is_gone_names_the_fix(outbox, lab, tmp_path, monkeypatch):
    """The fallback's create carries the project id init resolved. Deleted
    before the sync, the POST is a 404: it used to dead-letter as a bare "not
    found". It names `--project` now, and that re-files it."""
    doomed = make_client(lab).create_project("doomed", "Doomed", kind="general")
    _fallback_env(monkeypatch)
    real = lab.handler

    def refuse_creates(request):
        if request.method == "POST" and request.url.path.endswith("/runs"):
            raise httpx.ConnectError("refused", request=request)
        return real(request)

    lab.handler = refuse_creates
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    run = probe.init(project="doomed", name="r1")
    probe.log({"loss": 0.5}, step=0)
    probe.finish()
    assert run.id.startswith("local:")
    assert _offline_create(offline.find_offline_dirs()[0])["path"] == f"/v1/projects/{doomed['id']}/runs"
    lab.handler = real
    online = make_client(lab)
    online.transport.request("DELETE", f"/v1/projects/{doomed['id']}")
    (directory,) = offline.find_offline_dirs()
    (refused,) = _sync(lab)
    assert not refused["clean"] and lab.runs == {}
    assert any("--project <slug>" in e and "gone" in e for e in refused["errors"]), refused
    (fixed,) = _sync(lab, directory, project="p1", amend_all=True)
    assert fixed["clean"], fixed
    (row,) = lab.runs.values()
    assert row["project_id"] == online.resolve_or_raise("project", "p1")["id"]
    assert [p["step_index"] for p in _points(lab, row["id"])] == [0]


def test_allow_mismatch_applies_only_to_a_named_folder(outbox, no_network, lab, monkeypatch, capsys):
    from probe import cli

    monkeypatch.setenv("PROBE_BASE_URL", "https://api.elsewhere.example")
    _record()
    no_network.restore()
    (directory,) = offline.find_offline_dirs()
    monkeypatch.setattr(cli, "Client", lambda **kw: make_client(lab))
    capsys.readouterr()
    assert cli.main(["sync", "--allow-mismatch"]) == 2, "a scan never delivers across servers"
    assert lab.runs == {}
    assert "applies only to a run whose folder you name" in capsys.readouterr().err
    assert cli.main(["sync", str(directory), "--allow-mismatch"]) == 0
    (row,) = lab.runs.values()
    assert row["status"] == "completed"


# -- #2019's requeue takeover never steals a run mid-sync --------------------------------
def test_a_relaunch_cannot_take_over_an_offline_run_mid_sync(outbox, lab, tmp_path, monkeypatch):
    """A relaunch with the offline run's external_id and the default
    on_conflict asks the server to take the `running` incumbent over once it
    is silent -- and an offline run is silent while `probe sync` delivers it.
    The server refuses inside the sync grace (409 + a retry past any wait
    budget), so the relaunch gets its normal conflict and the sync finishes
    on the run it created."""
    guard = NoNetwork().arm()
    try:
        _record(n=4, name="job", external_id="job-1")
    finally:
        guard.restore()
    real = lab.handler
    seen = {"metrics": 0}

    def stall_after_the_first_write(request):
        if request.method == "POST" and request.url.path.endswith("/metrics"):
            seen["metrics"] += 1
            if seen["metrics"] > 1:
                return httpx.Response(503, json={"detail": "busy"})
        return real(request)

    from probe.sdk import transport

    monkeypatch.setattr(transport, "time", _Clock())
    lab.handler = stall_after_the_first_write
    (partial,) = _sync(lab)
    assert not partial["clean"]
    (row,) = lab.runs.values()
    assert row["status"] == "running" and row["liveness_mode"] == "offline"
    lab.run_silence[row["id"]] = 10_000.0  # long past any takeover threshold
    lab.handler = real

    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(lab, tmp_spool=tmp_path / "s"))
    with pytest.raises(errors.ConflictError, match="supersede"):
        probe.init(project="p1", name="job", external_id="job-1")
    assert lab.runs[row["id"]]["status"] == "running"
    assert lab.runs[row["id"]].get("write_epoch", 1) == 1, "not taken over"
    assert len(lab.runs) == 1

    (done,) = _sync(lab)
    assert done["clean"], done
    assert lab.runs[row["id"]]["status"] == "completed"
    assert sorted(p["step_index"] for p in _points(lab, row["id"])) == [0, 1, 2, 3]


# -- a second init (#2016's reinit) ------------------------------------------------------
def test_a_second_offline_init_closes_the_first_offline_run(outbox, no_network, capsys):
    """`reinit="finish_previous"` (the default) applies offline too: the first
    run's close is queued (with `probe_finish.closed_by`), and the new run is
    the bound one."""
    first = probe.init(mode="offline", project="p1", name="first")
    probe.log({"loss": 1.0}, step=0)
    second = probe.init(mode="offline", project="p1", name="second")
    assert fluent.active_run() is second and first is not second
    first_ops = [op for _, op in Journal(first.offline_dir).pending()]
    close = first_ops[-1]["body"]
    assert first_ops[-1]["method"] == "PATCH" and close["status"] == "completed"
    assert close["summary_metrics"]["probe_finish"]["closed_by"] == "reinit"
    assert close["summary_metrics"]["probe_finish"]["offline"] is True
    assert "could not be delivered" not in capsys.readouterr().err
    probe.finish()


def test_an_offline_create_new_run_is_left_unbound(outbox, no_network):
    bound = probe.init(mode="offline", project="p1", name="bound")
    extra = probe.init(mode="offline", project="p1", name="extra", reinit="create_new")
    assert fluent.active_run() is bound
    extra.finish()
    assert fluent._unbound == [], "its close let go of it"
    probe.finish()


# -- reads and writes (lineage plan 3, F6) ------------------------------------------


@pytest.fixture
def recorder(monkeypatch, tmp_path):
    """Read (and write) capture ON for an offline run, its spools under tmp."""
    from probe.sdk import inputs

    monkeypatch.setenv(inputs.READS_ENV, "1")
    # The suite turns output capture off; writes follow that switch.
    monkeypatch.delenv(inputs.OUTPUTS_ENV, raising=False)
    monkeypatch.delenv(inputs.CHILD_DIR_ENV, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    inputs._active.clear()
    inputs._hash_results.clear()
    yield inputs
    inputs._active.clear()


def _lineage_ops(directory):
    return [
        (op["path"].rsplit("/", 1)[1], op)
        for _, op in Journal(directory).pending()
        if op.get("method") == "POST" and op["path"].endswith(("/inputs", "/outputs"))
    ]


def test_an_offline_run_records_reads_and_writes_and_sync_delivers_them(
    outbox, no_network, lab, recorder, tmp_path
):
    """Recorded with no network, queued behind the run's writes and ahead of
    its close, delivered by `probe sync` onto the real run -- with the times
    the recording machine observed, never the sync's."""
    import hashlib

    data = tmp_path / "data.bin"
    data.write_bytes(b"d" * 500)
    out = tmp_path / "model.bin"
    sent_before = len(no_network.sent)  # `lab` seeded its project through the fake
    run = probe.init(mode="offline", project="p1", name="lineage")
    data.read_bytes()
    out.write_bytes(b"m" * 700)
    probe.finish()
    assert len(no_network.sent) == sent_before, "recording made no request"
    (directory,) = offline.find_offline_dirs()
    ops = [op for _, op in Journal(directory).pending()]
    routes = [op["path"] for op in ops if op.get("method") == "POST" and op["path"].startswith(f"/v1/runs/{run.id}/")]
    assert routes == [f"/v1/runs/{run.id}/inputs", f"/v1/runs/{run.id}/outputs"]
    assert ops[-1]["method"] == "PATCH", "the close is still last"
    assert not recorder.run_dir(run.id).exists(), "the spools went into the queue"

    no_network.restore()
    before_sync = offline.now_iso()
    (result,) = _sync(lab)
    assert result["clean"], result
    real = result["run_id"]
    reads = [r for b in lab.run_inputs[real] for r in b["inputs"]]
    writes = [r for b in lab.run_outputs[real] for r in b["outputs"]]
    assert [(r["path"], r["content_hash"]) for r in reads if r["path"] == str(data)] == [
        (str(data), hashlib.sha256(b"d" * 500).hexdigest())
    ]
    assert [(r["path"], r["content_hash"]) for r in writes] == [(str(out), hashlib.sha256(b"m" * 700).hexdigest())]
    # Observed while recording: every time is before the sync began.
    stamps = [r["first_seen_at"] for r in reads] + [
        r[k] for r in writes for k in ("first_written_at", "last_modified_at")
    ]
    assert all(stamp < before_sync for stamp in stamps), (stamps, before_sync)
    assert all("local:" not in r.url.path for r in lab.requests)


def test_capture_reads_false_offline_records_nothing(outbox, no_network, recorder, tmp_path):
    run = probe.init(mode="offline", project="p1", name="quiet", capture_reads=False)
    (tmp_path / "x.bin").write_bytes(b"x" * 100)
    probe.finish()
    (directory,) = offline.find_offline_dirs()
    assert _lineage_ops(directory) == []
    assert not recorder.is_recording(run.id)


def test_capture_outputs_false_offline_records_reads_only(outbox, no_network, recorder, tmp_path):
    data = tmp_path / "in.bin"
    data.write_bytes(b"i" * 100)
    probe.init(mode="offline", project="p1", name="reads-only", capture_outputs=False)
    data.read_bytes()
    (tmp_path / "out.bin").write_bytes(b"o" * 100)
    probe.finish()
    (directory,) = offline.find_offline_dirs()
    assert [route for route, _ in _lineage_ops(directory)] == ["inputs"]


def test_a_sync_server_without_the_lineage_features_drops_those_lists(
    outbox, no_network, lab, recorder, tmp_path
):
    """Queued on the promise that the SYNC server decides: one that cannot
    take a list gets it dropped with a warning, never dead-lettered."""
    probe.init(mode="offline", project="p1", name="old-server")
    (tmp_path / "in.bin").write_bytes(b"i" * 100)
    (tmp_path / "in.bin").read_bytes()
    (tmp_path / "out.bin").write_bytes(b"o" * 100)
    probe.finish()
    no_network.restore()
    lab.supports_run_outputs = False
    (result,) = _sync(lab)
    assert result["clean"] and result["dead_lettered"] == 0, result
    assert any("run_outputs" in w and "1 list(s)" in w for w in result["warnings"]), result
    assert lab.run_inputs[result["run_id"]]
    assert not [r for r in lab.requests if r.url.path.endswith("/outputs")]


def test_a_lineage_list_queued_after_the_sync_check_is_still_gated(
    outbox, no_network, lab, recorder, tmp_path, monkeypatch
):
    """P1 (review of 6e78909f0): `probe sync` checked the features once,
    before the drain; a recovery appending an /outputs op after that check
    sent it to a server without `run_outputs`. Delivery itself now asks."""
    run = probe.init(mode="offline", project="p1", name="race", capture_reads=False)
    probe.finish()
    no_network.restore()
    lab.supports_run_outputs = False
    real = offline._drop_untaken_lineage

    def check_then_race(journal, client):
        dropped = real(journal, client)
        # A concurrent recovery lands its list right after the check.
        journal.append_http("POST", f"/v1/runs/{run.id}/outputs", {"outputs": [], "coverage": {}},
                            run_ref=run.id, blocking=False)
        return dropped

    monkeypatch.setattr(offline, "_drop_untaken_lineage", check_then_race)
    (result,) = _sync(lab)
    assert not [r for r in lab.requests if r.url.path.endswith("/outputs")]
    assert result["clean"] and result["dead_lettered"] == 0, result
    assert any("run_outputs" in w for w in result["warnings"]), result


def test_an_offline_run_honours_ignore_for_what_it_reads(outbox, no_network, recorder, tmp_path, recwarn):
    """`ignore=` shapes the read and write lists an offline run records now:
    no longer "ignored", and an ignored file stays out of both."""
    kept, skipped = tmp_path / "train.bin", tmp_path / "weights.ckpt"
    kept.write_bytes(b"k" * 100)
    skipped.write_bytes(b"s" * 100)
    probe.init(mode="offline", project="p1", name="r", ignore=["*.ckpt"])
    kept.read_bytes()
    skipped.read_bytes()
    (tmp_path / "out.ckpt").write_bytes(b"o" * 100)
    probe.finish()
    assert not [w for w in recwarn if "ignored: ignore" in str(w.message)]
    (directory,) = offline.find_offline_dirs()
    lists = dict(_lineage_ops(directory))
    paths = [r["path"] for r in lists["inputs"]["body"]["inputs"]]
    assert str(kept) in paths and str(skipped) not in paths
    assert lists["outputs"]["body"]["outputs"] == []


def test_the_offline_lineage_features_are_the_recorders(recorder):
    assert set(offline.LINEAGE_ROUTES) == {recorder.FEATURE, recorder.OUTPUTS_FEATURE}
    assert "reads" not in offline.SKIPPED_CAPTURE


def test_a_dead_offline_runs_leftovers_go_into_its_own_queue(outbox, recorder, tmp_path):
    """`local:<key>` means nothing to a server: a recovery by a later ONLINE
    run on this machine queues an offline run's leftovers into that run's own
    queue for `probe sync`, and never sends them itself."""
    import subprocess
    import sys
    import time

    data = tmp_path / "left.bin"
    data.write_bytes(b"l" * 300)
    queue_dir = tmp_path / "offline-queue"
    Journal(queue_dir)._ensure()
    dead = int(subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                              capture_output=True, text=True, check=True).stdout)
    for ref, owner_queue in (("local:abc", str(queue_dir)), ("local:gone", str(tmp_path / "missing"))):
        directory = recorder.run_dir(ref)
        directory.mkdir(parents=True)
        (directory / "owner.json").write_text(
            json.dumps({"run_id": ref, "pid": dead, "offline_dir": owner_queue, "writes": True})
        )
        note = {"w": str(data), "t": "2026-09-26T00:00:00+00:00", "n": time.time_ns(), "o": "b" * 32,
                "b": None}
        # What the recorder last saw the file be while it lived: still true.
        ident = recorder._ident(os.stat(data))
        spool = directory / f"{recorder._host()}.{dead}.jsonl"
        spool.write_text(json.dumps(note) + "\n")
        recorder._sidecar(spool).write_text(json.dumps({str(data): list(ident)}))

    class _Online:
        journal = Journal(tmp_path / "online-outbox")

        @staticmethod
        def supports_feature(name):
            return True

    assert recorder.recover_orphans(_Online(), now=time.time() + 3600) == 1
    assert _Online.journal.pending() == []
    queued = [op for _, op in Journal(queue_dir).pending()]
    assert [op["path"] for op in queued] == ["/v1/runs/local:abc/inputs", "/v1/runs/local:abc/outputs"]
    assert queued[1]["body"]["outputs"][0]["path"] == str(data)
    import hashlib

    assert queued[1]["body"]["outputs"][0]["content_hash"] == hashlib.sha256(b"l" * 300).hexdigest()
    assert not recorder.run_dir("local:abc").exists() and not recorder.run_dir("local:gone").exists()


def test_the_offline_close_keeps_to_its_time(outbox, no_network, recorder, monkeypatch):
    """P2 9: a reinit's close (10 s) or a SIGTERM's grace bounds the hashing
    wait, as an online close's does: at most half of it."""
    waits = []
    monkeypatch.setattr(recorder, "finalize", lambda client, run_id, wait_s=None, **_: waits.append(wait_s))
    run = probe.init(mode="offline", project="p1", name="short")
    run.finish(flush_timeout=10)
    assert waits == [5.0]
    # The default close (600 s): the recorder's own cap, 30 s.
    monkeypatch.setattr("probe.sdk.run.FINISH_TIMEOUT_DEFAULT_SECONDS", 600.0)
    probe.init(mode="offline", project="p1", name="default")
    probe.finish()
    assert waits[-1] == recorder.FINISH_WAIT_S


def test_sync_delivers_what_a_crashed_offline_run_read_and_wrote(outbox, no_network, lab, recorder, tmp_path):
    """P2 10: the run died before its close queued its lists; `probe sync`
    moves them from its spools into the queue before the check and the drain."""
    import subprocess
    import sys

    data = tmp_path / "read.bin"
    data.write_bytes(b"r" * 300)
    run = probe.init(mode="offline", project="p1", name="crashed", capture_reads=False)
    probe.finish()  # stands in for the queue a crashed run leaves (create, writes)
    dead = int(subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                              capture_output=True, text=True, check=True).stdout)
    directory = recorder.run_dir(run.id)
    directory.mkdir(parents=True)
    (directory / "owner.json").write_text(json.dumps({"run_id": run.id, "pid": dead, "writes": True}))
    st = os.stat(data)
    read = {"p": str(data), "d": st.st_dev, "i": st.st_ino, "s": st.st_size, "m": st.st_mtime_ns,
            "c": st.st_ctime_ns, "t": "2026-09-26T00:00:00+00:00"}
    (directory / f"{recorder._host()}.{dead}.jsonl").write_text(json.dumps(read) + "\n")
    no_network.restore()
    (result,) = _sync(lab)
    assert result["clean"], result
    reads = [r for b in lab.run_inputs[result["run_id"]] for r in b["inputs"]]
    assert [r["path"] for r in reads] == [str(data)]
    assert not directory.exists()


def test_a_sync_server_that_does_not_key_reads_gets_no_ids_and_no_late_hashes(
    outbox, no_network, lab, recorder, tmp_path, monkeypatch
):
    """P2 (review of cf383d2a9): the offline client takes every lineage
    feature, so its read rows carried observation ids and its late hashes
    were queued; synced to a server with run_inputs but not run_outputs
    (0290), a late hash became a SECOND row beside the unhashed one. Such a
    server now gets the rows without ids, and no late re-send."""
    import queue

    class _Unhashed(queue.Queue):
        """The background hasher never gets the read."""

        def put(self, item, block=True, timeout=None):  # noqa: ARG002
            return None

    data = tmp_path / "late.bin"
    data.write_bytes(b"l" * 300)
    monkeypatch.setattr(recorder, "_hash_queue", _Unhashed())
    run = probe.init(mode="offline", project="p1", name="late")
    data.read_bytes()
    with monkeypatch.context() as close:
        # The close runs out of time: the read goes unhashed, kept for later.
        close.setattr(recorder, "_hash_within", lambda todo, budget, deadline, own, **k: None)
        probe.finish()
    assert recorder._late_files(recorder.run_dir(run.id)), "the late hash is waiting"
    no_network.restore()
    lab.supports_run_outputs = False
    (result,) = _sync(lab)  # its recovery queues the late re-send first
    assert result["clean"] and result["dead_lettered"] == 0, result
    batches = lab.run_inputs[result["run_id"]]
    assert len(batches) == 1, "the late re-send was not delivered"
    assert all("observation_id" not in row for b in batches for row in b["inputs"])
    assert any("late hash" in w for w in result["warnings"]), result["warnings"]
