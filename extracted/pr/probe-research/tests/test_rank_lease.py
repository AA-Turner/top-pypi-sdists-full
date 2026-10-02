"""A non-zero rank's lease-only writer on rank 0's run (plan 2.8 with (a) / (b)).

`_rank_lease.hold` is what the Lightning logger and the Hugging Face callback
call on every rank but 0, once rank 0 has broadcast its run id and epoch. The
real two-rank torchrun tests live in tests/framework_integrations/ (skipped
without the frameworks); these pin the rules framework-free: the lease's
shape, that the rank sends nothing but its beats and its release, the
verdict the release carries, and that a server without leases gets nothing.
"""

from __future__ import annotations

import json

import pytest

from probe.integrations import _rank_lease
from probe.sdk import fluent
from tests.conftest import make_client, open_run

_RANK_VARS = (
    "RANK", "WORLD_SIZE", "LOCAL_RANK",
    "SLURM_PROCID", "SLURM_NTASKS", "SLURM_LOCALID",
    "OMPI_COMM_WORLD_RANK", "OMPI_COMM_WORLD_SIZE", "OMPI_COMM_WORLD_LOCAL_RANK",
)


def _reset_exit_record() -> None:
    fluent._exit_status = "completed"
    fluent._exit_recorded = False
    fluent._exit_exception = None
    fluent._exit_code = None
    fluent._exit_via = None


@pytest.fixture(autouse=True)
def exits(monkeypatch):
    """No rank env from the machine running the suite, no real atexit
    registration (it would outlive the test), no exit record inherited."""
    for var in _RANK_VARS:
        monkeypatch.delenv(var, raising=False)
    registered: list = []
    monkeypatch.setattr(_rank_lease, "_at_exit", registered.append)
    _reset_exit_record()
    yield registered
    for lease in list(_rank_lease._LEASES.values()):
        lease.release()
    _rank_lease._LEASES.clear()
    _reset_exit_record()


@pytest.fixture
def app(app):
    app.supports_leases = True
    return app


def _rank_client(app, tmp_path, name: str = "rank1"):
    return make_client(app, tmp_spool=tmp_path / name)


def _requests_since(app, start: int) -> list:
    return app.requests[start:]


def _body(request) -> dict:
    return json.loads(request.content) if request.content else {}


def test_a_rank_joins_as_a_lease_only_writer(client, app, tmp_path, exits):
    """Lightning's own launcher and ddp_spawn set no RANK: the lease names
    the rank it was given and NO world size (a declared size would make the
    server wait for a slot 0 that rank 0's lease, read from the same empty
    env, never names). It is released at exit, with its verdict."""
    owner = open_run(client, experiment="e", name="r")
    start = len(app.requests)
    lease = _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=_rank_client(app, tmp_path))

    held = app.leases[owner.id][lease.session_id]
    assert (held["role"], held["rank"]) == ("rank", 1)
    assert "world_size" not in held
    assert lease.run._sends_terminal_status is False
    assert exits == [lease._release_at_exit]  # released when the process exits
    sent = {(r.method, r.url.path) for r in _requests_since(app, start)}
    assert sent <= {
        ("GET", "/v1/server/features"),
        ("GET", f"/v1/runs/{owner.id}"),
        ("POST", f"/v1/runs/{owner.id}/writers/{lease.session_id}/beat"),
    }, sent

    lease.release()
    assert held["exit_status"] == "completed" and held["released_at"]
    assert app.runs[owner.id]["status"] == "running", "one rank's release does not end the run"
    after = [r for r in _requests_since(app, start) if r.method == "PATCH"]
    assert after == [], "a rank sends no run fields and no status"
    owner.finish()
    assert app.runs[owner.id]["status"] == "completed"


def test_under_torchrun_the_rank_fields_come_from_the_env_like_rank_zeros(
    client, app, tmp_path, monkeypatch
):
    monkeypatch.setenv("RANK", "3")
    monkeypatch.setenv("WORLD_SIZE", "4")
    monkeypatch.setenv("LOCAL_RANK", "1")
    owner = open_run(client, experiment="e", name="r")
    lease = _rank_lease.hold(owner.id, owner.write_epoch, rank=3, client=_rank_client(app, tmp_path))
    held = app.leases[owner.id][lease.session_id]
    assert (held["role"], held["rank"], held["world_size"], held["local_rank"]) == ("rank", 3, 4, 1)


def test_a_server_without_leases_gets_nothing_from_a_rank(client, app, tmp_path):
    """Never a run-level heartbeat: from every rank it would keep the run
    alive after rank 0 is gone, which is the failure 2.8 exists to catch."""
    app.supports_leases = False
    owner = open_run(client, experiment="e", name="r")
    start = len(app.requests)
    assert _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=_rank_client(app, tmp_path)) is None
    assert [r.url.path for r in _requests_since(app, start)] == ["/v1/server/features"]


def test_a_rank_on_a_legacy_run_only_releases(app, tmp_path):
    """A run an older client opened (no protocol): the rank's close must never
    write a status -- that would end the run for every rank."""
    old = make_client(app, tmp_spool=tmp_path / "old")
    app.supports_leases = False
    owner = open_run(old, experiment="e", name="r")
    app.supports_leases = True
    lease = _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=_rank_client(app, tmp_path))
    start = len(app.requests)
    lease.release("failed")
    assert not [r for r in _requests_since(app, start) if r.method == "PATCH"]
    assert app.runs[owner.id]["status"] == "running"
    assert app.leases[owner.id][lease.session_id]["exit_status"] == "failed"


def test_one_lease_per_run_and_a_new_run_releases_the_old(client, app, tmp_path):
    """A second Trainer on the same run keeps the lease the first took; a new
    run (rank 0 opened one per Trainer in a sweep loop, and closed the last)
    releases the lease on the old one first."""
    first = open_run(client, experiment="e", name="a")
    lease_a = _rank_lease.hold(first.id, first.write_epoch, rank=1, client=_rank_client(app, tmp_path, "a"))
    assert _rank_lease.hold(first.id, first.write_epoch, rank=1, client=_rank_client(app, tmp_path, "x")) is lease_a
    assert len(app.leases[first.id]) == 2  # the owner's and this rank's, once

    second = open_run(client, experiment="e", name="b")
    lease_b = _rank_lease.hold(second.id, second.write_epoch, rank=1, client=_rank_client(app, tmp_path, "b"))
    assert lease_a.released and not lease_b.released
    assert app.leases[first.id][lease_a.session_id]["exit_status"] == "completed"
    assert app.leases[second.id][lease_b.session_id]["released_at"] is None


def test_a_process_already_writing_the_run_takes_no_second_lease(client, app, tmp_path, monkeypatch):
    """The script's own probe.init() joined the run through PROBE_RUN_ID on
    this rank: that handle holds this process's lease already."""
    owner = open_run(client, experiment="e", name="r")
    monkeypatch.setattr(fluent, "active_run", lambda: owner)
    before = len(app.requests)
    assert _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=_rank_client(app, tmp_path)) is None
    assert len(app.requests) == before


@pytest.mark.parametrize(
    "recorded, in_flight, verdict",
    [
        (None, None, "completed"),
        ("failed", None, "failed"),  # the excepthook, or sys.exit(1)
        ("canceled", None, "canceled"),  # Ctrl-C
        (None, RuntimeError("boom"), "failed"),  # a worker exiting on an error
        (None, KeyboardInterrupt(), "canceled"),
        (None, SystemExit(0), "completed"),
        (None, SystemExit(2), "failed"),
        (None, type("SIGTERMException", (SystemExit,), {})(), "failed"),  # Lightning's, exit 0
    ],
)
def test_the_release_says_how_the_process_ended(client, app, tmp_path, recorded, in_flight, verdict):
    owner = open_run(client, experiment="e", name="r")
    lease = _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=_rank_client(app, tmp_path))
    if recorded is not None:
        fluent._record_exit(recorded)
    lease.release(in_flight=in_flight)
    assert app.leases[owner.id][lease.session_id]["exit_status"] == verdict


def test_the_release_happens_once_and_closes_only_its_own_client(client, app, tmp_path):
    closed: list[str] = []

    def spied(name: str):
        built = _rank_client(app, tmp_path, name)
        real = built.close
        built.close = lambda *a, **kw: (closed.append(name), real(*a, **kw))
        return built

    owner = open_run(client, experiment="e", name="r")
    lease = _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=spied("theirs"))
    lease.release("failed")
    lease.release("completed")
    releases = [r for r in app.lease_releases if r["session_id"] == lease.session_id]
    assert [r["body"]["exit_status"] for r in releases] == ["failed"]
    assert closed == [], "the caller's own client= is theirs to close"

    second = open_run(client, experiment="e", name="s")
    owned = _rank_lease.hold(second.id, second.write_epoch, rank=1, client_factory=lambda: spied("built"))
    owned.release()
    assert closed == ["built"]


def test_a_lease_is_released_only_by_the_process_that_took_it(client, app, tmp_path, monkeypatch):
    """A forked child inherits the parent's leases: its exit is not theirs."""
    owner = open_run(client, experiment="e", name="r")
    lease = _rank_lease.hold(owner.id, owner.write_epoch, rank=1, client=_rank_client(app, tmp_path))
    real = _rank_lease.os.getpid()
    with monkeypatch.context() as patched:
        patched.setattr(_rank_lease.os, "getpid", lambda: real + 1)
        lease.release()
    assert app.leases[owner.id][lease.session_id]["released_at"] is None
    lease.release()  # the process that took it
    assert app.leases[owner.id][lease.session_id]["released_at"]
