"""The module-level layer: probe.init() / probe.log() / probe.finish().

The W&B ergonomic, minus the process-wide global that makes it dangerous. These
tests are mostly about the binding rules, because that is the part that differs.
"""

from __future__ import annotations

import atexit
import json
import os
import subprocess
import sys
import textwrap
import threading
import types
from pathlib import Path
import warnings

import pytest

import probe
from probe.sdk import diagnostics, fluent
from tests.conftest import make_client, open_run
from tests.served_fake_app import child_env, serve


@pytest.fixture(autouse=True)
def _clean_binding():
    """The layer keeps process state on purpose, so tests must not inherit it."""
    fluent._current.set(None)
    fluent._process_default = None
    fluent._exit_status = "completed"
    fluent._exit_recorded = False
    fluent._exit_exception = None
    fluent._exit_code = None
    fluent._exit_via = None
    yield
    fluent._current.set(None)
    fluent._process_default = None
    fluent._unbound.clear()
    fluent._reinit_dropped, fluent._reinit_new_run = 0, None
    fluent._exit_exception = None
    fluent._exit_code = None
    fluent._exit_via = None


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    """Make a bare `probe.init()` build a client wired to the fake backend, so the
    owned-client path (the one init actually takes in real use) is under test."""
    built = []

    def factory(*_a, **_kw):
        client = make_client(app, tmp_spool=tmp_path / "spool")
        built.append(client)
        return client

    monkeypatch.setattr(fluent, "Client", factory)
    app.seed_experiment("e1")
    return built


# -- the basic round trip ------------------------------------------------------
def test_init_log_finish(app, wired):
    run = probe.init(experiment="e1", name="r1")
    probe.log({"loss": 0.4}, step=1)
    probe.finish()

    assert app.runs[run.id]["status"] == "completed"
    assert app.metrics_inserted == 1


def test_init_can_explicitly_create_project_experiment_and_run(app, wired):
    run = probe.init(
        project="folding",
        experiment="new-experiment",
        question="temp 0.7 wins",
        name="r1",
    )
    probe.finish()

    # (The fixture's seeded experiment is filed under a project of its own.)
    (project,) = [p for pid, p in app.projects.items() if pid not in app.seeded_home_projects]
    (experiment,) = [row for row in app.experiments.values() if row["slug"] == "new-experiment"]
    assert experiment["project_id"] == project["id"]
    assert app.runs[run.id]["experiment_id"] == experiment["id"]


def test_active_run_is_none_until_init(app, wired):
    assert probe.active_run() is None
    run = probe.init(experiment="e1", name="r1")
    assert probe.active_run() is run
    probe.finish()
    assert probe.active_run() is None


def test_logging_with_no_active_run_says_so(app, wired):
    """The failure mode this replaces is W&B's: log() before init() silently
    starts a run, or drops the call. Neither is recoverable from the outside."""
    with pytest.raises(probe.errors.RosError, match="no active run"):
        probe.log({"loss": 0.4})


def test_init_returns_a_real_run_handle(app, wired):
    """It is not a proxy — the explicit API stays the implementation, so
    everything on Run is reachable without going through this layer."""
    run = probe.init(experiment="e1", name="r1")
    assert isinstance(run, probe.Run)
    run.link(wandb_run_id="abc")
    probe.finish()
    assert app.runs[run.id]["foreign_keys"] == {"wandb_run_id": "abc"}


def test_init_is_usable_as_a_context_manager(app, wired):
    with probe.init(experiment="e1", name="r1") as run:
        probe.log({"loss": 0.4})
    assert app.runs[run.id]["status"] == "completed"


# -- binding rules -------------------------------------------------------------
def test_a_worker_thread_reaches_the_run(app, wired):
    """The reason there is a process default at all. Threads start with an EMPTY
    context, so a contextvar alone would leave a DataLoader worker — or any
    library logging from a thread — silently unable to find the run."""
    run = probe.init(experiment="e1", name="r1")
    seen = {}

    def worker():
        seen["run"] = probe.active_run()
        probe.log({"loss": 0.1}, step=1)

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    probe.finish()

    assert seen["run"] is run


def test_a_scoped_init_shadows_rather_than_hijacks(app, wired):
    """W&B's global is last-writer-wins process-wide, so a second run started
    anywhere silently steals every subsequent log(). Here the context is
    consulted first, so the thread's own init cannot redirect the main thread."""
    outer = probe.init(experiment="e1", name="outer")
    inner_seen = {}

    def worker():
        inner = probe.init(experiment="e1", name="inner")
        inner_seen["run"] = probe.active_run()
        assert inner_seen["run"] is inner

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()

    # the main thread still logs into its OWN run, not the thread's
    assert probe.active_run() is outer
    assert inner_seen["run"] is not outer


# -- client ownership ----------------------------------------------------------
def test_finish_closes_the_client_init_built(app, wired):
    probe.init(experiment="e1", name="r1")
    (built,) = wired
    probe.finish()
    assert built.transport._client.is_closed


def test_a_caller_supplied_client_is_left_open(app, client):
    """Closing it would kill a transport — and any other run's heartbeat — that
    the caller is still using. Ownership follows who built it."""
    app.seed_experiment("e1")
    probe.init(client=client, experiment="e1", name="r1")
    probe.finish()
    assert not client.transport._client.is_closed


def test_finish_twice_is_a_no_op(app, wired):
    probe.init(experiment="e1", name="r1")
    probe.finish()
    assert probe.finish() is None


def test_a_failed_init_does_not_leak_its_client(app, wired):
    """init() builds a client before it knows the run will open. A transport left
    behind here would keep a connection pool — and later, heartbeat threads —
    alive with nothing able to close them."""
    with pytest.raises(probe.errors.RosError):
        probe.init(experiment="does-not-exist-and-has-no-question", name="r1")
    (built,) = wired
    assert built.transport._client.is_closed
    assert probe.active_run() is None


# -- exit handling -------------------------------------------------------------
def test_atexit_completes_a_run_the_script_forgot_to_close(app, wired):
    """A clean script that never calls finish() would otherwise sit `running`
    until the server reaper marks it crashed — the wrong answer for one that
    worked."""
    run = probe.init(experiment="e1", name="r1")
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "completed"


def test_atexit_does_not_claim_success_after_an_unhandled_exception(app, wired):
    """atexit still runs after a traceback prints, so guessing `completed` for
    every exit would record a lie."""
    run = probe.init(experiment="e1", name="r1")
    try:
        raise ValueError("boom")
    except ValueError as exc:
        fluent._excepthook(type(exc), exc, exc.__traceback__)
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "failed"


def test_an_interrupt_is_canceled_not_failed(app, wired):
    """`canceled` is a real status here, and "I stopped it" is different
    information from "it broke"."""
    run = probe.init(experiment="e1", name="r1")
    exc = KeyboardInterrupt()
    fluent._excepthook(KeyboardInterrupt, exc, None)
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "canceled"


def test_atexit_is_silent_when_nothing_is_active(app, wired):
    fluent._finish_at_exit()  # must not raise


# -- regressions caught in pre-landing review ---------------------------------
def test_finish_from_another_thread_clears_the_binding_everywhere(app, wired):
    """finish() can only clear the contextvar of the thread that CALLS it. A
    worker closing the run must not leave the main thread logging into a
    completed one, so the binding itself carries the closed flag."""
    probe.init(experiment="e1", name="r1")
    thread = threading.Thread(target=probe.finish)
    thread.start()
    thread.join()

    assert probe.active_run() is None
    with pytest.raises(probe.errors.RosError, match="no active run"):
        probe.log({"loss": 0.4})


def test_the_excepthook_is_captured_once_and_never_chains_to_itself(app, wired):
    """Unsynchronised, two concurrent init()s could both pass the installed check
    and the second would capture _excepthook as its own predecessor — every later
    uncaught exception then recurses until the stack blows."""
    probe.init(experiment="e1", name="r1")
    first = fluent._hooks()["excepthook"]
    probe.finish()
    probe.init(experiment="e1", name="r2")
    assert fluent._hooks()["excepthook"] is first
    assert fluent._hooks()["excepthook"] is not fluent._excepthook


def test_a_new_run_does_not_inherit_the_previous_exit_status(app, wired):
    """_exit_status is process-wide, so without a reset a run that follows a
    failed one would be closed as failed at exit."""
    probe.init(experiment="e1", name="r1")
    fluent._excepthook(ValueError, ValueError("boom"), None)
    probe.finish()

    run = probe.init(experiment="e1", name="r2")
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "completed"


# -- probe.context(...) --------------------------------------------------------
def test_context_is_on_the_public_surface():
    import probe.sdk

    assert "context" in probe.__all__ and "context" in probe.sdk.__all__
    assert probe.context is fluent.context is probe.sdk.context
    assert probe.sdk.FailureContext is type(probe.context())


def test_context_with_no_active_run_is_a_no_op(app, wired):
    """Unlike log(), never an error: `probe.context` sits in library loops that
    may or may not run under probe.init()."""
    with pytest.raises(ValueError) as caught:
        with probe.context(batch_id="b7", epoch=3):
            raise ValueError("bad")
    assert not hasattr(caught.value, "_probe_failure_context")


def test_log_inside_context_goes_out_unlabeled_on_the_same_series(app, wired):
    """The regression the brief is about, through the ambient door an agent
    actually uses: the batch id must not reach a metric point."""
    import json

    run = probe.init(experiment="e1", name="r1")
    for i in range(3):
        with probe.context(batch_id=f"batch-{i}", epoch=0):
            probe.log({"loss": 0.5}, step=i)
    probe.finish()

    bodies = [
        json.loads(r.content)
        for r in app.requests
        if r.method == "POST" and r.url.path == f"/v1/runs/{run.id}/metrics"
    ]
    points = [point for body in bodies for point in body["points"]]
    assert [p["step_index"] for p in points] == [0, 1, 2]
    for point in points:
        assert point["dimensions"] == {}
        assert "labels" not in point
    assert "batch-" not in json.dumps(bodies)
    # One series, not three one-point tiles.
    assert {(p["key"], json.dumps(p["dimensions"], sort_keys=True)) for p in points} == {
        ("loss", "{}")
    }


# -- how the process ends: sys.exit, forks, ranks (plan 2.1) -------------------
_TERMINAL = {"completed", "failed", "canceled", "crashed"}
#: Spelled out rather than read from `fluent`: the test states the contract.
_RANK_VARS = ("RANK", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK")
_SIZE_VARS = ("WORLD_SIZE", "SLURM_NTASKS", "OMPI_COMM_WORLD_SIZE")


@pytest.fixture
def hooks(monkeypatch):
    """A fresh install over production-shaped predecessors, undone afterwards.

    `_install_exit_hooks` runs once per process, so without this a test would
    exercise whatever an earlier test (in any file) left installed. The
    predecessors behave like the real ones -- the previous `sys.exit` RAISES --
    and count their calls."""
    calls: dict[str, list] = {"exit": [], "excepthook": []}

    def prior_exit(code=None):
        calls["exit"].append(code)
        raise SystemExit(code)

    def prior_excepthook(exc_type, exc, tb):
        calls["excepthook"].append(exc_type)

    was_registered = getattr(sys, "_probe_exit_hooks", None) is not None
    monkeypatch.setattr(sys, "exit", prior_exit)
    monkeypatch.setattr(sys, "excepthook", prior_excepthook)
    # The chain lives on `sys`; removing it is what makes the next init() a
    # first install. monkeypatch puts the earlier one back afterwards.
    monkeypatch.delattr(sys, "_probe_exit_hooks", raising=False)
    yield calls
    atexit.unregister(fluent._finish_at_exit)
    if was_registered:
        atexit.register(fluent._finish_at_exit)


@pytest.fixture
def diagnostics_on(monkeypatch):
    # The suite pins PROBE_TELEMETRY=off, which also silences diagnostics.
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "on")


def _exit_spans(app, run_id):
    return [
        s
        for s in app.spans.get(run_id, [])
        if s["span_type"] == "process" and s["name"] == "exit"
    ]


def _diagnostic_spans(app, run_id):
    return [s for s in app.spans.get(run_id, []) if s["span_type"] == diagnostics.SPAN_TYPE]


def _terminal_patches(app, run_id) -> list[str]:
    """The verdicts this run was sent, in order: a terminal status PATCH, or
    (SDK reliability 2.8, a server with leases) a lease release's
    `exit_status` -- the same verdict, sent the way that server takes it."""
    statuses = []
    for request in app.requests:
        if request.method == "PATCH" and request.url.path == f"/v1/runs/{run_id}":
            status = json.loads(request.content or b"{}").get("status")
            if status in _TERMINAL:
                statuses.append(status)
        elif request.method == "POST" and request.url.path.startswith(
            f"/v1/runs/{run_id}/writers/"
        ) and request.url.path.endswith("/release"):
            status = json.loads(request.content or b"{}").get("exit_status")
            if status in _TERMINAL:
                statuses.append(status)
    return statuses


def test_a_nonzero_sys_exit_fails_the_run_and_records_the_code(app, wired, hooks, diagnostics_on):
    """`sys.exit(2)` raises a SystemExit no excepthook ever sees, so atexit
    closed it `completed`. The code is also the crash email's only cause when
    nothing was raised: it reads the latest process span's `exit_code`."""
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit) as caught:
        sys.exit(2)
    assert caught.value.code == 2, "the exit itself must be untouched"
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "failed"
    (span,) = _exit_spans(app, run.id)
    assert span["attributes"]["exit_code"] == 2
    assert span["attributes"]["via"] == "sys.exit"
    assert span["started_at"] and span["ended_at"]
    assert not _diagnostic_spans(app, run.id), "nothing was in flight to diagnose"
    # Evidence first: a span behind the terminal PATCH races a closed run.
    order = [(r.method, r.url.path) for r in app.requests]
    assert order.index(("POST", f"/v1/runs/{run.id}/spans")) < order.index(
        ("PATCH", f"/v1/runs/{run.id}")
    )


@pytest.mark.parametrize("args", [(), (0,), (None,), (False,)], ids=["bare", "0", "None", "False"])
def test_a_clean_sys_exit_completes(app, wired, hooks, args):
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit):
        sys.exit(*args)
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "completed"
    assert not _exit_spans(app, run.id)


def test_an_exit_with_a_message_fails_with_code_one(app, wired, hooks):
    """`sys.exit("config not found")` prints the message and exits 1."""
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit):
        sys.exit("config not found")
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "failed"
    (span,) = _exit_spans(app, run.id)
    assert span["attributes"]["exit_code"] == 1


def _lightning_fit():
    """Lightning 2.6 `trainer/call.py`: Ctrl-C is caught and turned into an exit."""
    try:
        raise KeyboardInterrupt
    except KeyboardInterrupt:
        sys.exit(1)


def _hydra_main():
    """Hydra 1.3 `_internal/utils.py`: the task's exception is printed and
    swallowed, then the process exits 1 -- the excepthook never runs."""
    try:
        raise RuntimeError("bad learning rate")
    except Exception:
        sys.exit(1)


def test_the_lightning_ctrl_c_shape_is_canceled_with_no_diagnostic(
    app, wired, hooks, diagnostics_on
):
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit):
        _lightning_fit()
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "canceled"
    assert not _diagnostic_spans(app, run.id), "Ctrl-C is a decision, not a defect"


def test_the_hydra_shape_fails_with_the_swallowed_exception_as_its_diagnostic(
    app, wired, hooks, diagnostics_on
):
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit):
        _hydra_main()
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "failed"
    (diagnostic,) = _diagnostic_spans(app, run.id)
    assert diagnostic["attributes"]["exception"][0]["type"] == "RuntimeError"
    (span,) = _exit_spans(app, run.id)
    assert span["attributes"]["exit_code"] == 1


# pytest reports the thread's SystemExit; the real threading.excepthook ignores it.
@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_sys_exit_in_a_worker_thread_does_not_end_the_run(app, wired, hooks):
    """It ends that thread, not the process: the script carries on and exits 0."""
    run = probe.init(experiment="e1", name="r1")
    thread = threading.Thread(target=sys.exit, args=(3,))
    thread.start()
    thread.join()
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "completed"
    assert not _exit_spans(app, run.id)


def test_a_notebook_exit_records_nothing(app, wired, hooks, monkeypatch):
    """ipykernel catches the SystemExit and the kernel carries on."""
    monkeypatch.setitem(sys.modules, "ipykernel", types.ModuleType("ipykernel"))
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit):
        sys.exit(2)
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "completed"


def test_the_hooks_that_were_there_first_each_run_exactly_once(app, wired, hooks):
    """Chained, never replaced -- pdb, Hydra and Lightning install their own --
    and a second init() must not wrap the wrapper."""
    probe.init(experiment="e1", name="r1")
    probe.finish()
    probe.init(experiment="e1", name="r2")

    with pytest.raises(SystemExit):
        sys.exit(4)
    sys.excepthook(ValueError, ValueError("boom"), None)

    assert hooks["exit"] == [4]
    assert hooks["excepthook"] == [ValueError]
    assert sys.exit is fluent._exit and fluent._hooks()["exit"] is not fluent._exit


def test_hooks_inherited_by_another_process_record_and_close_nothing(app, wired, hooks):
    """What a forked child sees: the parent's hooks and binding, a different pid.
    The subprocess test below forks for real; this pins every entry point."""
    run = probe.init(experiment="e1", name="r1")
    sys._probe_exit_hooks["pid"] = os.getpid() + 1

    with pytest.raises(SystemExit):
        sys.exit(3)
    sys.excepthook(ValueError, ValueError("child"), None)
    fluent.note_exit("failed", ValueError("child"))
    fluent._finish_at_exit()

    assert fluent._exit_status == "completed"
    assert app.runs[run.id]["status"] == "running"
    assert hooks["exit"] == [3] and hooks["excepthook"] == [ValueError], "still chained"


def test_note_exit_reports_what_no_process_hook_sees(app, wired, diagnostics_on):
    """Lightning turns SIGTERM into SIGTERMException, a code-less SystemExit:
    the process exits 0 through no hook. The integration's on_exception says so."""

    class SIGTERMException(SystemExit):
        """lightning.pytorch.utilities.exceptions.SIGTERMException's shape."""

    run = probe.init(experiment="e1", name="r1")
    fluent.note_exit("failed", SIGTERMException())
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "failed"
    (diagnostic,) = _diagnostic_spans(app, run.id)
    assert diagnostic["attributes"]["exception"][0]["type"] == "SIGTERMException"
    assert not _exit_spans(app, run.id), "no code is known, and the process exits 0"


def test_note_exit_canceled_files_no_diagnostic(app, wired, diagnostics_on):
    run = probe.init(experiment="e1", name="r1")
    fluent.note_exit("canceled", KeyboardInterrupt())
    fluent._finish_at_exit()

    assert app.runs[run.id]["status"] == "canceled"
    assert not _diagnostic_spans(app, run.id)


def test_note_exit_refuses_a_status_the_close_cannot_send(app, wired):
    probe.init(experiment="e1", name="r1")
    with pytest.raises(probe.errors.ValidationError, match="note_exit"):
        fluent.note_exit("crashed")


def test_a_new_run_does_not_inherit_the_previous_exception_or_code(app, wired, diagnostics_on):
    """The exception slot is process-wide like the status: without a reset a
    run following a crashed one would carry its crash report."""
    probe.init(experiment="e1", name="r1")
    fluent._excepthook(ValueError, ValueError("boom"), None)
    probe.finish()

    run = probe.init(experiment="e1", name="r2")
    fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "completed"
    assert not _diagnostic_spans(app, run.id)
    assert not _exit_spans(app, run.id)


# -- the interim rank rule (until per-writer leases, plan 2.8) -----------------
@pytest.fixture
def shared_run(app, wired, monkeypatch):
    """A run a launcher opened and exported, the way `probe exec` does."""
    for var in (*_RANK_VARS, *_SIZE_VARS):
        monkeypatch.delenv(var, raising=False)
    launcher = make_client(app)
    run = launcher.run(experiment="e1", name="shared", heartbeat=False, capture_outputs=False)
    monkeypatch.setenv("PROBE_RUN_ID", run.id)
    monkeypatch.setenv("PROBE_RUN_EPOCH", str(run.write_epoch))
    yield run.id
    launcher.close()


@pytest.mark.parametrize("var", _RANK_VARS)
def test_a_nonzero_rank_on_a_shared_run_sends_no_terminal_status(
    app, shared_run, hooks, monkeypatch, var
):
    """Every rank attaches to the same run. The first one out closed it for all
    of them, and a later rank's `completed` overwrote an earlier `failed`."""
    monkeypatch.setenv(var, "3")
    run = probe.init()
    assert run.id == shared_run
    probe.log({"loss": 0.5}, step=1)
    with pytest.raises(SystemExit):
        sys.exit(2)
    fluent._finish_at_exit()

    assert _terminal_patches(app, shared_run) == []
    assert app.runs[shared_run]["status"] == "running"
    assert app.metric_points_posted[shared_run], "the rank's data is still delivered"
    (span,) = _exit_spans(app, shared_run)
    assert span["attributes"]["exit_code"] == 2 and span["attributes"]["rank"] == 3


def test_rank_zero_still_closes_the_shared_run(app, shared_run, hooks, monkeypatch):
    monkeypatch.setenv("RANK", "0")
    monkeypatch.setenv("SLURM_PROCID", "0")
    probe.init()
    with pytest.raises(SystemExit):
        sys.exit(2)
    fluent._finish_at_exit()

    assert _terminal_patches(app, shared_run) == ["failed"]


def test_a_worker_is_rank_zero_only_if_every_scheme_agrees(app, shared_run, monkeypatch):
    """srun + torchrun: SLURM_PROCID numbers the node, RANK the worker."""
    monkeypatch.setenv("SLURM_PROCID", "0")
    monkeypatch.setenv("RANK", "5")
    probe.init()
    probe.finish()

    assert _terminal_patches(app, shared_run) == []


def test_a_nonzero_rank_that_opened_its_own_run_still_closes_it(app, wired, hooks, monkeypatch):
    """The rule is about a SHARED run. A rank that created its own owns it."""
    monkeypatch.delenv("PROBE_RUN_ID", raising=False)
    monkeypatch.setenv("RANK", "3")
    run = probe.init(experiment="e1", name="rank-3")
    with pytest.raises(SystemExit):
        sys.exit(2)
    fluent._finish_at_exit()

    assert _terminal_patches(app, run.id) == ["failed"]


def test_a_nonzero_rank_closing_explicitly_leaves_the_verdict_alone(app, shared_run, monkeypatch):
    monkeypatch.setenv("RANK", "1")
    probe.init()
    probe.finish("completed")
    with probe.init() as run:
        probe.log({"loss": 0.1}, step=2)
    run.finish("failed")

    assert _terminal_patches(app, shared_run) == []
    assert app.runs[shared_run]["status"] == "running"


def test_a_nonzero_rank_bounded_finish_queues_no_terminal_op(app, wired, shared_run, monkeypatch):
    """PROBE_FINISH_TIMEOUT_SEC -- set by exactly the cluster jobs that have
    ranks -- journals the close behind undelivered data. Not for this rank."""
    from probe.sdk import errors

    monkeypatch.setenv("RANK", "1")
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "0.1")
    probe.init()
    client = wired[-1]
    original = client.transport.request

    def metrics_down(method, path, *a, **kw):
        if method == "POST" and path.endswith("/metrics"):
            raise errors.TransportError("net down")
        return original(method, path, *a, **kw)

    monkeypatch.setattr(client.transport, "request", metrics_down)
    probe.log({"loss": 0.5}, step=1)
    probe.finish()

    queued = [op for _, op in client.journal.pending() if op.get("run_ref") == shared_run]
    assert [op["method"] for op in queued] == ["POST"], "the data waits; no close behind it"
    assert _terminal_patches(app, shared_run) == []


# -- real processes ------------------------------------------------------------
def _run_child(app, code: str, **env: str) -> subprocess.CompletedProcess:
    with serve(app) as url:
        return subprocess.run(
            [sys.executable, "-c", textwrap.dedent(code)],
            env=child_env(url, **env),
            capture_output=True,
            text=True,
            timeout=120,
        )


def test_a_real_process_exiting_2_closes_its_run_failed(app):
    """The whole path in a real interpreter: wrapper, atexit, finish."""
    app.seed_experiment("e1")
    proc = _run_child(
        app,
        """
        import sys, probe
        probe.init(experiment="e1", name="r1")
        sys.exit(2)
        """,
    )
    assert proc.returncode == 2, proc.stderr[-2000:]
    (run_id,) = app.runs
    assert _terminal_patches(app, run_id) == ["failed"]
    (span,) = _exit_spans(app, run_id)
    assert span["attributes"]["exit_code"] == 2


def test_a_forked_child_exiting_does_not_close_the_parents_run(app):
    """The child inherits the wrapped sys.exit, the atexit registration and the
    binding. Its exit must leave the run to the parent: one terminal PATCH, the
    parent's."""
    app.seed_experiment("e1")
    proc = _run_child(
        app,
        """
        import os, sys, probe
        probe.init(experiment="e1", name="r1")
        pid = os.fork()
        if pid == 0:
            sys.exit(3)
        _, status = os.waitpid(pid, 0)
        assert os.waitstatus_to_exitcode(status) == 3, status
        """,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    (run_id,) = app.runs
    assert _terminal_patches(app, run_id) == ["completed"]
    assert not _exit_spans(app, run_id)


# -- review fixes: codes the OS reports, closed runs stay closed, ranks, reload --
@pytest.mark.parametrize(
    ("code", "status", "reported"),
    [(-1, "failed", 255), (256, "completed", 0), (255, "failed", 255), (257, "failed", 1)],
)
def test_the_recorded_code_is_the_one_the_os_reports(app, wired, hooks, code, status, reported):
    """`sys.exit(-1)` exits 255 (submitit does it on preemption); stored as -1
    it read as "killed by a signal" and mailed a false SIGHUP crash. And
    `sys.exit(256)` exits 0, so the run completed."""
    run = probe.init(experiment="e1", name="r1")
    with pytest.raises(SystemExit) as caught:
        sys.exit(code)
    assert caught.value.code == code, "the exit itself is untouched"
    fluent._finish_at_exit()

    assert _terminal_patches(app, run.id) == [status]
    assert [s["attributes"]["exit_code"] for s in _exit_spans(app, run.id)] == (
        [reported] if reported else []
    )


def test_an_explicitly_finished_run_is_not_closed_again_at_exit(app, wired, hooks):
    """`run.finish("failed")`, then the script ends: the exit used to PATCH
    `completed` over the script's own verdict."""
    run = probe.init(experiment="e1", name="r1")
    run.finish("failed")
    fluent._finish_at_exit()
    assert _terminal_patches(app, run.id) == ["failed"]


def test_a_gate_after_a_finished_with_block_does_not_reopen_the_verdict(app, wired, hooks):
    """Training finished inside the block; a check after it exits 2. The run
    completed; turning it `failed` queued a crash email about a run that worked."""
    with probe.init(experiment="e1", name="r1") as run:
        probe.log({"loss": 0.1}, step=1)
    with pytest.raises(SystemExit):
        sys.exit(2)
    fluent._finish_at_exit()

    assert _terminal_patches(app, run.id) == ["completed"]
    assert not _exit_spans(app, run.id)


def test_the_hydra_shape_around_a_with_block_files_one_diagnostic(
    app, wired, hooks, diagnostics_on
):
    def task():
        with probe.init(experiment="e1", name="r1"):
            raise RuntimeError("bad learning rate")

    def hydra_main():
        try:
            task()
        except Exception:
            sys.exit(1)

    with pytest.raises(SystemExit):
        hydra_main()
    fluent._finish_at_exit()

    (run_id,) = app.runs
    assert _terminal_patches(app, run_id) == ["failed"]
    (diagnostic,) = _diagnostic_spans(app, run_id)
    assert diagnostic["attributes"]["exception"][0]["type"] == "RuntimeError"


def _interrupt():
    raise KeyboardInterrupt


@pytest.mark.parametrize(
    ("body", "status", "code"),
    [
        (lambda: sys.exit(0), "completed", None),
        (lambda: sys.exit(2), "failed", 2),
        (_lightning_fit, "canceled", 1),
        (_interrupt, "canceled", None),
    ],
    ids=["exit-0", "exit-2", "lightning-ctrl-c", "ctrl-c"],
)
def test_a_with_block_reads_how_its_body_ended_like_the_process_hooks(
    app, wired, hooks, diagnostics_on, body, status, code
):
    """Every SystemExit used to close the block's run `failed` and file the
    SystemExit as its crash report -- `sys.exit(0)` included."""
    with pytest.raises((SystemExit, KeyboardInterrupt)) as caught:
        with probe.init(experiment="e1", name="r1") as run:
            body()
    if caught.type is KeyboardInterrupt:
        # ...and then reaches the excepthook, which must not close it again.
        fluent._excepthook(KeyboardInterrupt, caught.value, None)
    fluent._finish_at_exit()

    assert _terminal_patches(app, run.id) == [status]
    assert not _diagnostic_spans(app, run.id)
    spans = _exit_spans(app, run.id)
    assert [s["attributes"]["exit_code"] for s in spans] == ([code] if code else [])


@pytest.mark.parametrize(
    "env",
    [{"RANK": "-1"}, {"RANK": "3", "WORLD_SIZE": "1"}, {"SLURM_PROCID": "2", "SLURM_NTASKS": "1"}],
    ids=["negative", "rank-with-world-of-one", "slurm-single-task"],
)
def test_a_rank_that_is_not_a_distributed_rank_still_closes_the_run(
    app, shared_run, hooks, monkeypatch, env
):
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    probe.init()
    fluent._finish_at_exit()
    assert _terminal_patches(app, shared_run) == ["completed"]


def test_a_rank_in_a_real_world_still_stands_down(app, shared_run, hooks, monkeypatch):
    monkeypatch.setenv("RANK", "3")
    monkeypatch.setenv("WORLD_SIZE", "8")
    probe.init()
    fluent._finish_at_exit()
    assert _terminal_patches(app, shared_run) == []


def test_under_a_finalizing_launcher_an_unrecorded_exit_leaves_the_close_to_it(
    app, shared_run, hooks, monkeypatch
):
    """No hook saw how the process ends, so `completed` is a guess -- and the
    launcher holds the real exit code. The data still goes."""
    monkeypatch.setenv("PROBE_EXEC_FINALIZES", shared_run)
    probe.init()
    probe.log({"loss": 0.5}, step=1)
    fluent._finish_at_exit()

    assert _terminal_patches(app, shared_run) == []
    assert app.metric_points_posted[shared_run]


def test_under_a_finalizing_launcher_a_recorded_exit_still_speaks(
    app, shared_run, hooks, monkeypatch
):
    """Lightning's Ctrl-C exits 1, which the launcher would call `failed`; the
    child knows better."""
    monkeypatch.setenv("PROBE_EXEC_FINALIZES", shared_run)
    probe.init()
    with pytest.raises(SystemExit):
        _lightning_fit()
    fluent._finish_at_exit()

    assert _terminal_patches(app, shared_run) == ["canceled"]


def test_reloading_the_module_keeps_sys_exit_working(app):
    """The chain lives on `sys`: a reload used to reset it to None (every exit
    a TypeError) or make the wrapper its own predecessor (RecursionError)."""
    app.seed_experiment("e1")
    proc = _run_child(
        app,
        """
        import importlib, sys, probe
        from probe.sdk import fluent
        probe.init(experiment="e1", name="r1")
        probe.finish()
        importlib.reload(fluent)
        fluent.init(experiment="e1", name="r2")
        sys.exit(3)
        """,
    )
    assert proc.returncode == 3, proc.stderr[-2000:]
    assert "Error" not in proc.stderr, proc.stderr[-2000:]
    statuses = sorted(app.runs[r]["status"] for r in app.runs)
    assert statuses == ["completed", "failed"]


def test_a_launcher_finalizing_another_run_leaves_this_one_to_its_job(
    app, shared_run, hooks, monkeypatch
):
    """A sweep driver under `probe exec` opens run B and hands PROBE_RUN_ID=B
    to a job, which inherits the driver's launcher flag. Nobody finalizes B:
    the job must close it, or B is reaped `crashed` and mails a false alarm."""
    monkeypatch.setenv("PROBE_EXEC_FINALIZES", "the-driver-run")
    probe.init()
    fluent._finish_at_exit()
    assert _terminal_patches(app, shared_run) == ["completed"]


@pytest.mark.parametrize("shape", ["with", "run.finish"])
def test_a_run_the_script_closed_still_releases_its_client_at_exit(app, wired, hooks, shape):
    """The exit stands down for a closed run, but the client init() built must
    still close: that is the last export pass, the hand-off of anything left
    to the background uploader, and the sealed outbox producer record."""
    if shape == "with":
        with probe.init(experiment="e1", name="r1"):
            probe.log({"loss": 0.1}, step=1)
    else:
        run = probe.init(experiment="e1", name="r1")
        probe.log({"loss": 0.1}, step=1)
        run.finish()
    (client,) = wired
    assert not client.transport._client.is_closed

    fluent._finish_at_exit()

    assert client.transport._client.is_closed
    assert probe.active_run() is None
    assert _terminal_patches(app, _only_run(app)) == ["completed"], "closed once, by the script"


def _only_run(app):
    (run_id,) = app.runs
    return run_id


@pytest.mark.parametrize(
    "body",
    [
        "with probe.init(experiment='e1', name='r1'):\n    probe.log({'loss': 0.1}, step=1)\n",
        "run = probe.init(experiment='e1', name='r1')\nprobe.log({'loss': 0.1}, step=1)\nrun.finish()\n",
    ],
    ids=["with", "run.finish"],
)
def test_a_real_process_seals_its_outbox_producer_after_closing_its_own_run(app, body):
    """Only a default client registers an outbox producer, so this runs for
    real: the record must read `closed`, as it does for a plain script -- a
    producer left `open` by an exited process reads as a crashed writer."""
    app.seed_experiment("e1")
    proc = _run_child(app, "import probe\n" + body)
    assert proc.returncode == 0, proc.stderr[-2000:]
    records = [
        json.loads(path.read_text())
        for path in Path(os.environ["PROBE_OUTBOX_DIR"]).rglob("producers/*.json")
    ]
    assert records and {r.get("state") for r in records} == {"closed"}, records


def test_note_exit_inside_a_with_block_outranks_a_code_less_exit(
    app, wired, hooks, diagnostics_on
):
    """Lightning on SIGTERM: on_exception -> note_exit("failed", exc), then a
    SystemExit with no code leaves the block, which alone reads as success."""

    class SIGTERMException(SystemExit):
        """lightning.pytorch.utilities.exceptions.SIGTERMException's shape."""

    with pytest.raises(SIGTERMException):
        with probe.init(experiment="e1", name="r1") as run:
            exc = SIGTERMException()
            fluent.note_exit("failed", exc)
            raise exc
    fluent._finish_at_exit()

    assert _terminal_patches(app, run.id) == ["failed"]
    (diagnostic,) = _diagnostic_spans(app, run.id)
    assert diagnostic["attributes"]["exception"][0]["type"] == "SIGTERMException"


def test_a_code_less_exit_with_nothing_noted_still_completes(app, wired, hooks):
    with pytest.raises(SystemExit):
        with probe.init(experiment="e1", name="r1") as run:
            raise SystemExit
    assert _terminal_patches(app, run.id) == ["completed"]


# -- a second probe.init() (plan (j), reinit) ----------------------------------
def _summary(app, run_id) -> dict:
    row = app.runs[run_id]
    return row.get("summary_metrics") or row.get("summary") or {}


def test_a_second_init_closes_the_first_run(app, wired, capsys, monkeypatch):
    """Before, the first run was abandoned: nothing closed it, the reaper called
    it `crashed`, and its heartbeat and client ran until the process died."""
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "3600")  # a live beat thread
    first = probe.init(experiment="e1", name="r1")
    beat = first._hb_stop
    assert beat is not None and not beat.is_set()

    second = probe.init(experiment="e1", name="r2")

    assert second.id != first.id
    assert _terminal_patches(app, first.id) == ["completed"]
    assert _summary(app, first.id)["probe_finish"] == {"closed_by": "reinit"}
    assert beat.is_set(), "the first run's heartbeat must stop"
    assert wired[0].transport._client.is_closed, "and the client init built for it"
    assert probe.active_run() is second
    assert app.runs[second.id]["status"] == "running"
    out = [line for line in capsys.readouterr().out.splitlines() if "closed run" in line]
    assert len(out) == 1 and first.slug in out[0]


@pytest.mark.parametrize("reinit", ["default", "finish_previous", True, None])
def test_every_spelling_of_finish_previous_closes_the_first(app, wired, reinit):
    first = probe.init(experiment="e1", name="r1")
    probe.init(experiment="e1", name="r2", reinit=reinit)
    assert _terminal_patches(app, first.id) == ["completed"]


@pytest.mark.parametrize("reinit", ["return_previous", False])
def test_return_previous_returns_the_open_run_and_names_what_it_ignored(app, wired, reinit):
    first = probe.init(experiment="e1", name="r1")
    with pytest.warns(UserWarning, match=r"ignored experiment, name"):
        again = probe.init(experiment="e1", name="r2", reinit=reinit)

    assert again is first
    assert _terminal_patches(app, first.id) == []
    assert len(app.runs) == 1
    assert len(wired) == 1, "no client is built for a run that is not opened"


def test_create_new_leaves_the_first_open_and_bound(app, wired):
    first = probe.init(experiment="e1", name="r1")
    second = probe.init(experiment="e1", name="r2", reinit="create_new")

    assert second.id != first.id
    assert probe.active_run() is first, "create_new does not rebind"
    probe.log({"loss": 0.1}, step=1)
    assert app.metric_points_posted[first.id]
    assert not app.metric_points_posted.get(second.id)
    assert _terminal_patches(app, first.id) == [] == _terminal_patches(app, second.id)

    # Neither is left for the reaper: the exit closes both.
    fluent._finish_at_exit()
    assert _terminal_patches(app, first.id) == ["completed"]
    assert _terminal_patches(app, second.id) == ["completed"]


def test_an_unknown_reinit_is_refused_before_anything_opens(app, wired):
    with pytest.raises(probe.errors.ValidationError, match="reinit"):
        probe.init(experiment="e1", name="r1", reinit="finish_all")
    assert wired == [] and app.runs == {}


def test_an_init_in_a_worker_thread_leaves_the_outer_run_open(app, wired):
    """The worker sees the main thread's run through the process default, but
    it is not the worker's "previous": its own init shadows, never closes."""
    outer = probe.init(experiment="e1", name="outer")
    seen = {}

    def worker():
        seen["inner"] = probe.init(experiment="e1", name="inner")

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()

    assert _terminal_patches(app, outer.id) == []
    assert probe.active_run() is outer
    assert seen["inner"].id != outer.id


def test_a_reinit_inside_a_with_block_closes_the_run_once(app, wired):
    """`__exit__` used to PATCH the run a second time, after the reinit had."""
    with probe.init(experiment="e1", name="r1") as first:
        second = probe.init(experiment="e1", name="r2")
    assert _terminal_patches(app, first.id) == ["completed"]
    assert _summary(app, first.id)["probe_finish"]["closed_by"] == "reinit"
    assert probe.active_run() is second


def test_a_run_joined_through_probe_run_id_is_returned_never_finished(app, shared_run):
    """Its launcher owns the close."""
    first = probe.init()
    with pytest.warns(UserWarning, match="PROBE_RUN_ID"):
        again = probe.init(capture_outputs=True)
    also = probe.init(reinit="create_new")

    assert again is first and also is first
    assert _terminal_patches(app, shared_run) == []


def test_both_runs_sweep_their_outputs(app, wired, tmp_path, monkeypatch):
    """With both open, each run's sweep saw the other alive over the same folder
    and skipped. Closing the first before the second opens lets both sweep."""
    from probe.sdk import ephemeral, outputs

    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    monkeypatch.setenv("PROBE_CAPTURE_LOG", "0")
    monkeypatch.setenv(ephemeral.ENV, "0")
    monkeypatch.setattr(outputs, "_shared_warned", set())

    first = probe.init(experiment="e1", name="r1", capture_outputs=True)
    (work / "first.txt").write_text("from the first run")
    second = probe.init(experiment="e1", name="r2", capture_outputs=True)
    (work / "second.txt").write_text("from the second run")
    probe.finish()

    def names(run):
        return {a["name"] for a in app.artifacts.get(run.id, [])}

    assert names(first) == {"outputs/first.txt"}
    assert names(second) == {"outputs/second.txt"}


def _refuse(app, monkeypatch, method, path, status_code):
    """`method path` answers `status_code`; every other route stays healthy."""
    import httpx

    real = app._dispatch

    def dispatch(request):
        if request.method == method and request.url.path == path:
            app.requests.append(request)
            return httpx.Response(status_code, json={"detail": "injected"})
        return real(request)

    monkeypatch.setattr(app, "_dispatch", dispatch)


def _refuse_run_patch(app, monkeypatch, run_id, status_code):
    _refuse(app, monkeypatch, "PATCH", f"/v1/runs/{run_id}", status_code)


def test_an_outage_during_the_close_queues_it_behind_the_data(app, wired, monkeypatch):
    """Bounded: at most min(PROBE_FINISH_TIMEOUT_SEC, 10) s, then the close is
    queued BEHIND the undelivered writes, still saying why it happened."""
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "0.2")
    first = probe.init(experiment="e1", name="r1")
    _refuse(app, monkeypatch, "POST", f"/v1/runs/{first.id}/metrics", 503)
    probe.log({"loss": 0.5}, step=1)

    with pytest.warns(UserWarning, match=r"closed run .*queued"):
        second = probe.init(experiment="e1", name="r2")

    assert probe.active_run() is second
    queued = [op for _, op in wired[0].journal.pending() if op.get("run_ref") == first.id]
    assert [op["method"] for op in queued] == ["POST", "PATCH"], "the close waits behind the data"
    accounting = queued[-1]["body"]["summary"]["probe_finish"]
    assert accounting["closed_by"] == "reinit" and accounting["deferred"] is True
    # 1.10: the queued close carries the run's epoch, so a relaunch that took
    # the run over can refuse it when it finally lands.
    assert first.write_epoch is not None
    assert queued[-1]["body"]["write_epoch"] == first.write_epoch


def test_the_close_is_bounded_even_with_no_finish_timeout_set(app, wired, monkeypatch):
    """Unset, a finish() is the hard barrier and refuses to close over pending
    writes. A reinit caps it instead (10 s; shortened here)."""
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)
    monkeypatch.setattr(fluent, "_REINIT_FLUSH_CAP_S", 0.2)
    first = probe.init(experiment="e1", name="r1")
    _refuse(app, monkeypatch, "POST", f"/v1/runs/{first.id}/metrics", 503)
    probe.log({"loss": 0.5}, step=1)

    with pytest.warns(UserWarning, match=r"closed run .*queued"):
        probe.init(experiment="e1", name="r2")

    queued = [op for _, op in wired[0].journal.pending() if op.get("run_ref") == first.id]
    assert [op["method"] for op in queued] == ["POST", "PATCH"]


def test_a_crash_after_a_reinit_inside_a_with_block_is_not_filed_on_the_closed_run(
    app, wired, client, diagnostics_on
):
    """The block's exception still propagates; the run the reinit closed gets
    neither a second PATCH nor a crash report it never had. (A caller-supplied
    client, so the report COULD still be delivered.)"""
    with pytest.raises(ValueError, match="after the reinit"):
        with probe.init(client=client, experiment="e1", name="r1") as first:
            probe.init(experiment="e1", name="r2")
            raise ValueError("after the reinit")

    assert _terminal_patches(app, first.id) == ["completed"]
    assert not _diagnostic_spans(app, first.id)


def test_a_503_while_closing_warns_and_queues_the_close(app, wired, monkeypatch):
    """The new run is what the caller is waiting for. An outage closing the old
    one is at most 10 s (here PROBE_FINISH_TIMEOUT_SEC) and a warning."""
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "0.2")
    first = probe.init(experiment="e1", name="r1")
    _refuse_run_patch(app, monkeypatch, first.id, 503)

    with pytest.warns(UserWarning, match=r"closed run .*queued"):
        second = probe.init(experiment="e1", name="r2")

    assert probe.active_run() is second
    queued = [op for _, op in wired[0].journal.pending() if op.get("run_ref") == first.id]
    (close,) = [op for op in queued if op["method"] == "PATCH"]
    assert close["body"]["status"] == "completed"
    assert close["body"]["summary"]["probe_finish"]["closed_by"] == "reinit"


def test_a_rejected_close_warns_and_never_raises(app, wired, monkeypatch):
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "3600")
    first = probe.init(experiment="e1", name="r1")
    beat = first._hb_stop
    _refuse_run_patch(app, monkeypatch, first.id, 422)

    with pytest.warns(UserWarning, match="did not close cleanly"):
        second = probe.init(experiment="e1", name="r2")

    assert probe.active_run() is second
    assert beat.is_set()
    assert wired[0].transport._client.is_closed


def test_run_finish_is_idempotent(app, client):
    """A second finish would overwrite the first verdict with its own guess."""
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1", heartbeat=False)
    first = run.finish()
    assert run.finish("failed") == first, "a repeat returns what the first close returned"
    assert _terminal_patches(app, run.id) == ["completed"]


def _close_fails(monkeypatch):
    from probe.sdk import run as run_module

    def refuse(self, *_a, **_kw):
        raise probe.errors.RosError(f"run {self.id} not closed: 1 outbox op(s) are undelivered")

    monkeypatch.setattr(run_module.Run, "finish", refuse)


def test_a_close_that_fails_at_exit_says_so(app, wired, hooks, monkeypatch):
    """`finish()` raising inside the exit hook was swallowed by a bare `pass`:
    the run sat `running` until the reaper called it `crashed`, and nothing
    on screen said why."""
    run = probe.init(experiment="e1", name="r1")
    _close_fails(monkeypatch)
    with pytest.warns(UserWarning, match=r"run .* was not closed at exit \(RosError: run .* not closed"):
        fluent._finish_at_exit()
    assert app.runs[run.id]["status"] == "running"


# The refused finish() keeps the run's lock file open (by design: an unclosed
# run keeps its claim), and under "error" its ResourceWarning at collection
# time is reported as unraisable. Unrelated to what this test pins.
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_the_failed_close_line_never_raises_even_under_w_error(app, wired, hooks, monkeypatch):
    probe.init(experiment="e1", name="r1")
    _close_fails(monkeypatch)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        fluent._finish_at_exit()  # must not raise


def test_a_real_process_prints_the_failed_close_on_stderr(app):
    app.seed_experiment("e1")
    proc = _run_child(
        app,
        """
        import probe
        from probe.sdk import errors, run as run_module
        probe.init(experiment="e1", name="r1")

        def refuse(self, *a, **kw):
            raise errors.RosError("the server is busy (503)")

        run_module.Run.finish = refuse
        """,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    assert "was not closed at exit (RosError: the server is busy (503))" in proc.stderr


# -- probe.update_config (plan (c)) --------------------------------------------
def test_update_config_is_on_the_public_surface_and_merges(app, wired):
    import probe.sdk

    assert "update_config" in probe.__all__ and "update_config" in probe.sdk.__all__
    run = probe.init(experiment="e1", name="r1", config={"lr": 0.1})
    probe.update_config({"bs": 64})
    probe.finish()
    assert app.runs[run.id]["config"] == {"lr": 0.1, "bs": 64}


def test_an_attached_job_records_its_config_from_rank_zero(app, wired, monkeypatch):
    """Under `probe exec` the launcher created the run without the script's
    config; init used to drop `config=` with an "ignored" warning."""
    wired_client = fluent.Client()
    launcher = open_run(wired_client, experiment="e1", name="r", heartbeat=False)
    monkeypatch.setenv("PROBE_RUN_ID", launcher.id)
    monkeypatch.delenv("RANK", raising=False)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        run = probe.init(config={"lr": 0.1, "bs": 32})
    probe.finish()
    assert run.id == launcher.id
    assert app.runs[launcher.id]["config"] == {"lr": 0.1, "bs": 32}
    assert not [w for w in caught if "ignored" in str(w.message)]
    wired_client.close()


def test_a_non_zero_rank_does_not_record_the_config(app, wired, monkeypatch):
    wired_client = fluent.Client()
    launcher = open_run(wired_client, experiment="e1", name="r", heartbeat=False)
    monkeypatch.setenv("PROBE_RUN_ID", launcher.id)
    monkeypatch.setenv("RANK", "3")
    probe.init(config={"lr": 0.1})
    probe.finish()
    assert app.runs[launcher.id]["config"] == {}
    wired_client.close()


# -- PROBE_MODE (plan 2.5) -------------------------------------------------------
@pytest.fixture
def no_client(monkeypatch):
    """Fail loudly if init builds a Client at all: disabled mode must not."""

    def refuse(*_a, **_kw):
        raise AssertionError("PROBE_MODE=disabled built a Client")

    monkeypatch.setattr(fluent, "Client", refuse)


def test_disabled_mode_records_nothing_and_touches_nothing(app, no_client, monkeypatch, tmp_path):
    outbox = tmp_path / "outbox-must-not-exist"
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(outbox))
    monkeypatch.setenv("PROBE_MODE", "disabled")

    run = probe.init(experiment="e1", name="r1", config={"lr": 0.1})
    assert probe.active_run() is run
    probe.log({"loss": 0.4}, step=1)
    with probe.span("eval"):
        probe.log_hw({"gpu/util": 0.5})
    probe.log_artifact("ckpt", uri="s3://bucket/ckpt")
    run.set_tags(["x"])
    run.expect({"loss": (0, 1)})
    probe.finish()

    assert probe.active_run() is None
    assert app.requests == []
    assert not outbox.exists()
    assert run.disabled and run.config == {"lr": 0.1}


def test_disabled_mode_takes_every_config_shape_online_takes(app, no_client):
    """`config=args` (an argparse Namespace) is THE W&B pattern (plan (c)). A
    disabled run used to raise TypeError on it -- `dict(Namespace)` -- so the
    same script crashed only when recording was turned off."""
    import argparse

    run = probe.init(mode="disabled", experiment="e1", config=argparse.Namespace(lr=0.1))
    run.config.batch = 32
    run.config.update(argparse.Namespace(wd=0.01))
    run.update_config({"seed": 7})
    probe.finish()
    assert run.config == {"lr": 0.1, "batch": 32, "wd": 0.01, "seed": 7}
    assert run.config.lr == 0.1
    assert app.requests == []


def test_disabled_mode_by_argument_and_as_a_context_manager(app, no_client):
    with probe.init(mode="disabled", experiment="e1") as run:
        probe.log({"loss": 0.4})
    assert run.status == "completed"
    assert app.requests == []


def test_disabled_mode_installs_no_exit_hooks(no_client, monkeypatch):
    # The hooks are keyed on `sys` (plan 2.1): without the key, the next init
    # that installs them would be a first install. monkeypatch restores both.
    monkeypatch.delattr(sys, fluent._HOOKS_ATTR, raising=False)
    exit_before, excepthook_before = sys.exit, sys.excepthook
    probe.init(mode="disabled")
    assert getattr(sys, fluent._HOOKS_ATTR, None) is None
    assert sys.exit is exit_before and sys.excepthook is excepthook_before
    probe.finish()


@pytest.mark.parametrize("mode", ["disable", "on"])
def test_an_unavailable_or_unknown_mode_refuses_instead_of_going_online(no_client, mode):
    """`disable` (a typo) must not quietly put a job on the network."""
    with pytest.raises(probe.errors.ValidationError):
        probe.init(mode=mode, experiment="e1")
    assert probe.active_run() is None


def test_online_mode_is_the_default(app, wired, monkeypatch):
    monkeypatch.setenv("PROBE_MODE", "ONLINE")
    run = probe.init(experiment="e1", name="r1")
    probe.finish()
    assert app.runs[run.id]["status"] == "completed"


def test_a_disabled_run_answers_every_run_property_with_a_value():
    """Code written against a real Run keeps working: a property is a value of
    its kind (never the no-op function the fallback hands a method), and a
    method whose real result is a collection answers an empty one."""
    import inspect

    from probe.sdk.disabled import DisabledRun
    from probe.sdk.run import Run

    run = DisabledRun()
    properties = [n for n, v in inspect.getmembers(Run) if isinstance(v, property) and not n.startswith("_")]
    assert properties, "Run has properties to mirror"
    for name in properties:
        assert not callable(getattr(run, name)), f"DisabledRun.{name} is a function, Run.{name} a value"
    for name in ("session_id", "write_epoch", "attached"):
        assert not callable(getattr(run, name))
    for name, fn in inspect.getmembers(Run, inspect.isfunction):
        if name.startswith("_"):
            continue
        returns = str(inspect.signature(fn).return_annotation)
        if returns.startswith(("list", "dict")) and not returns.endswith("None"):
            result = getattr(run, name)()
            assert isinstance(result, (list, dict)), f"DisabledRun.{name}() -> {result!r}"
    assert run.foreign_keys == {} and run.log_artifact("x", path="/nope") is None


def test_init_ignore_applies_to_an_attached_run(app, shared_run, hooks, tmp_path, monkeypatch):
    """`probe.init(ignore=...)` inside a job a launcher opened: the attach path
    drops creation kwargs, but not these (plan (n))."""
    monkeypatch.chdir(tmp_path)
    run = probe.init(ignore=["ckpt/", "*.bin"])
    assert run.id == shared_run
    rules = run._ignore_rules()
    assert rules is not None and rules.ignored(str(tmp_path / "ckpt" / "a.pt"))
    assert rules.ignored(str(tmp_path / "x.bin")) and not rules.ignored(str(tmp_path / "m.json"))
    fluent._finish_at_exit()


def test_init_rejects_a_bad_ignore_before_opening_anything(app, wired):
    with pytest.raises(probe.errors.ValidationError, match="ignore="):
        probe.init(experiment="e1", ignore=[1, 2])
    assert fluent._current.get() is None


@pytest.mark.parametrize(
    "snapshot,env_patterns,warned",
    [("1", "", ["*.bin"]), ("1", "*.bin", None), ("0", "", None)],
)
def test_an_attached_runs_ignore_says_it_cannot_reach_the_code_snapshot(
    app, shared_run, hooks, tmp_path, monkeypatch, snapshot, env_patterns, warned
):
    """#2045 re-review: the launcher took the code snapshot before this
    process started, so `ignore=` cannot change it -- said once, naming only
    the patterns the launcher never loaded, and only when it snapshotted."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", snapshot)
    monkeypatch.setenv("PROBE_IGNORE", env_patterns)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        probe.init(ignore=["*.bin"])
    said = [str(w.message) for w in caught if "code snapshot" in str(w.message)]
    if warned:
        assert len(said) == 1 and f"ignore={warned!r}" in said[0] and "PROBE_IGNORE" in said[0]
    else:
        assert said == []
    fluent._finish_at_exit()


def test_a_create_new_run_that_fails_to_close_at_exit_says_so(app, wired, hooks, monkeypatch):
    probe.init(experiment="e1", name="r1")
    probe.init(experiment="e1", name="r2", reinit="create_new")
    _close_fails(monkeypatch)
    with pytest.warns(UserWarning, match="was not closed at exit") as caught:
        fluent._finish_at_exit()
    assert len([w for w in caught if "was not closed at exit" in str(w.message)]) == 2



# -- reinit: whose run is "previous" (review of #2016) --------------------------
def test_an_asyncio_task_opens_its_own_run_beside_the_parents(app, wired):
    """A task inherits a COPY of the parent's context, so the parent's run was
    visible there -- and a task's init() took it for its own previous run,
    closed it, and the parent's next probe.log() raised."""
    import asyncio

    outer = probe.init(experiment="e1", name="outer")

    async def child(i):
        return probe.init(experiment="e1", name=f"task{i}")

    async def main():
        return await asyncio.gather(child(1), child(2))

    inner = asyncio.run(main())

    assert _terminal_patches(app, outer.id) == []
    assert all(r.id != outer.id for r in inner)
    assert all(_terminal_patches(app, r.id) == [] for r in inner), "siblings do not close each other"
    assert probe.active_run() is outer
    probe.log({"loss": 0.1}, step=1)
    assert app.metric_points_posted[outer.id]


def test_asyncio_to_thread_opens_its_own_run_beside_the_parents(app, wired):
    import asyncio

    outer = probe.init(experiment="e1", name="outer")

    async def main():
        return await asyncio.to_thread(lambda: probe.init(experiment="e1", name="worker"))

    worker = asyncio.run(main())
    assert worker.id != outer.id
    assert _terminal_patches(app, outer.id) == []
    assert probe.active_run() is outer


def test_a_task_that_opened_a_run_replaces_it_on_its_own_second_init(app, wired):
    import asyncio

    async def main():
        first = probe.init(experiment="e1", name="r1")
        second = probe.init(experiment="e1", name="r2")
        return first, second

    first, second = asyncio.run(main())
    assert _terminal_patches(app, first.id) == ["completed"]
    assert _terminal_patches(app, second.id) == []


def _notebook():
    """Cells the way ipykernel 6.17-7.3 runs them: each one its own asyncio
    task, sync cells in ONE persistent context, a top-level-await cell in a
    copy of it that is dropped when the cell ends."""
    import asyncio
    import contextvars

    if sys.version_info < (3, 11):
        # `create_task(context=)` is 3.11+; 3.10 cannot run a task in a given
        # context, so this harness cannot model ipykernel's cells there.
        pytest.skip("the notebook-cell harness needs create_task(context=), Python 3.11+")
    loop = asyncio.new_event_loop()
    kernel = contextvars.copy_context()

    def cell(fn, *, awaits=False):
        async def body():
            return fn()

        ctx = kernel.copy() if awaits else kernel
        return loop.run_until_complete(loop.create_task(body(), context=ctx))

    return loop, cell


def test_re_running_a_notebook_cell_closes_the_run_it_opened_before(app, wired):
    loop, cell = _notebook()
    try:
        first = cell(lambda: probe.init(experiment="e1", name="r1"))
        second = cell(lambda: probe.init(experiment="e1", name="r2"))
    finally:
        loop.close()
    assert _terminal_patches(app, first.id) == ["completed"]
    assert second.id != first.id


def test_a_sync_cell_after_an_await_cell_reaches_the_run_it_opened(app, wired):
    """The await cell's context variable dies with the cell; its run is still
    the process default, and a closed one in the kept context must not hide it."""
    loop, cell = _notebook()
    try:
        first = cell(lambda: probe.init(experiment="e1", name="r1"))
        second = cell(lambda: probe.init(experiment="e1", name="r2"), awaits=True)
        seen = cell(probe.active_run)
        cell(lambda: probe.log({"loss": 0.2}, step=1))
    finally:
        loop.close()
    assert _terminal_patches(app, first.id) == ["completed"]
    assert seen is second
    assert app.metric_points_posted[second.id]


def test_other_threads_wait_for_the_new_run_instead_of_raising(app, wired, monkeypatch):
    """Between closing the old run and binding the new one there was no run at
    all, and a DataLoader thread's probe.log() raised "no active run"."""
    import time as _time

    probe.init(experiment="e1", name="r1")
    real_close = fluent._close_binding
    outcome: dict = {}

    def log_from_another_thread():
        try:
            outcome["run"] = probe.active_run()
            probe.log({"loss": 0.3}, step=1)
            outcome["ok"] = True
        except Exception as exc:  # noqa: BLE001
            outcome["error"] = exc

    def slow_close(binding, **kw):
        real_close(binding, **kw)  # the old run is closed and unbound now
        thread = threading.Thread(target=log_from_another_thread)
        thread.start()
        outcome["thread"] = thread
        _time.sleep(0.2)  # the thread reaches probe.log() inside the gap

    monkeypatch.setattr(fluent, "_close_binding", slow_close)
    second = probe.init(experiment="e1", name="r2")
    outcome["thread"].join(5)

    assert outcome.get("ok"), outcome.get("error")
    assert outcome["run"] is second
    assert app.metric_points_posted[second.id]


def test_create_new_runs_closed_through_their_handles_release_their_clients(app, wired):
    probe.init(experiment="e1", name="bound")
    for i in range(5):
        run = probe.init(experiment="e1", name=f"sweep{i}", reinit="create_new")
        run.finish()
    probe.init(experiment="e1", name="after", reinit="create_new")
    open_clients = [c for c in wired[1:6] if not c.transport._client.is_closed]
    assert open_clients == []


def test_a_forked_child_opens_its_own_run_and_leaves_the_parents_alone(app):
    """The child inherits the parent's binding. Its init() used to close the
    parent's run -- deleting the PARENT's crash breadcrumb on the way."""
    app.seed_experiment("e1")
    proc = _run_child(
        app,
        """
        import os, probe
        from probe.sdk import diagnostics
        parent = probe.init(experiment="e1", name="parent")
        crumb = os.path.join(diagnostics._breadcrumb_dir(parent._client), parent.id + ".crash.json")
        print("PARENT", parent.id, flush=True)
        pid = os.fork()
        if pid == 0:
            probe.init(experiment="e1", name="child")
            probe.finish()
            os._exit(0)
        os.waitpid(pid, 0)
        print("CRUMB_KEPT", os.path.exists(crumb), flush=True)
        probe.log({"loss": 0.1}, step=1)
        probe.finish()
        """,
        PROBE_DIAGNOSTICS="on",
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    parent_id = next(line.split()[1] for line in proc.stdout.splitlines() if line.startswith("PARENT"))
    assert _terminal_patches(app, parent_id) == ["completed"], "only the parent's own close"
    assert "CRUMB_KEPT True" in proc.stdout
    child_ids = [rid for rid in app.runs if rid != parent_id]
    assert len(child_ids) == 1 and _terminal_patches(app, child_ids[0]) == ["completed"]


def test_a_forked_childs_exit_closes_none_of_the_parents_runs(app):
    app.seed_experiment("e1")
    proc = _run_child(
        app,
        """
        import os, sys, time, probe
        bound = probe.init(experiment="e1", name="parent")
        side = probe.init(experiment="e1", name="side", reinit="create_new")
        print("PARENT_RUNS", bound.id, side.id, flush=True)
        pid = os.fork()
        if pid == 0:
            probe.init(experiment="e1", name="child", reinit="create_new")
            sys.exit(0)
        os.waitpid(pid, 0)
        os._exit(0)  # the parent skips its own exit hook: only the child's shows
        """,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    bound_id, side_id = next(
        line.split()[1:3] for line in proc.stdout.splitlines() if line.startswith("PARENT_RUNS")
    )
    assert _terminal_patches(app, side_id) == []
    assert _terminal_patches(app, bound_id) == []


# -- reinit on #2011's close (review of #2016, MED3-6 + LOW) --------------------
def _crumb(run) -> Path:
    return Path(diagnostics._breadcrumb_dir(run._client)) / f"{run.id}.crash.json"


def _pending_for(client, run_id) -> list[dict]:
    return [op for _, op in client.journal.pending() if op.get("run_ref") == run_id]


def test_finish_after_execute_keeps_its_verdict_and_still_closes(app, wired, diagnostics_on):
    """`run.execute()` closes its run through set_status. The finish() after it
    used to either PATCH again (`failed` became `completed`) or return at once
    and leave the crash breadcrumb armed, which the next init() on the host
    then filed as a `hard_exit` on a run that had closed itself."""
    run = probe.init(experiment="e1", name="launcher")
    assert _crumb(run).exists()
    run.execute([sys.executable, "-c", "raise SystemExit(3)"])

    probe.finish()

    assert _terminal_patches(app, run.id) == ["failed"], "one verdict, the child's"
    assert not _crumb(run).exists(), "the close still disarmed the crumb"
    assert _pending_for(wired[0], run.id) == [], "and drained what execute() queued"
    assert diagnostics.sweep(make_client(app)) == []


def test_a_reinit_after_execute_keeps_its_verdict_and_still_closes(app, wired, diagnostics_on, capsys):
    first = probe.init(experiment="e1", name="launcher")
    first.execute([sys.executable, "-c", "raise SystemExit(3)"])

    second = probe.init(experiment="e1", name="next")

    assert _terminal_patches(app, first.id) == ["failed"]
    assert not _crumb(first).exists()
    assert wired[0].transport._client.is_closed
    assert probe.active_run() is second
    assert "closed run" not in capsys.readouterr().out, "it was not open to close"


def test_the_exit_hook_after_execute_keeps_its_verdict_and_still_closes(
    app, wired, hooks, diagnostics_on
):
    run = probe.init(experiment="e1", name="launcher")
    run.execute([sys.executable, "-c", "raise SystemExit(3)"])

    fluent._finish_at_exit()

    assert _terminal_patches(app, run.id) == ["failed"]
    assert not _crumb(run).exists()
    assert wired[0].transport._client.is_closed


def test_set_status_then_finish_runs_the_close_but_writes_no_second_verdict(
    app, client, monkeypatch
):
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1", heartbeat=False)
    finished = []
    run._hw_monitor = types.SimpleNamespace(finish=lambda timeout=None: finished.append(True))
    healthy = app._dispatch
    _refuse(app, monkeypatch, "POST", f"/v1/runs/{run.id}/metrics", 503)
    run.log({"loss": 0.5}, step=1)  # queued: the server is refusing it
    run.set_status("failed")
    monkeypatch.setattr(app, "_dispatch", healthy)

    run.finish()

    assert _terminal_patches(app, run.id) == ["failed"]
    assert finished == [True], "the hardware collector is stopped"
    assert app.metric_points_posted[run.id], "the queued write is delivered"
    assert _pending_for(client, run.id) == []


def test_drops_after_a_sent_verdict_are_warned_but_never_claimed_marked(app, client):
    """#2014's `dropped_writes` marker rides the terminal write, and after a
    bare `set_status` there is none to ride: the verdict stands (no second
    PATCH), the warning says the run could NOT be marked, and the report still
    counts the drops."""
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1", heartbeat=False)
    client.dropped_writes += 2  # two writes found the outbox full
    run.set_status("failed")

    with pytest.warns(UserWarning, match=r"dropped") as caught:
        report = run.finish()

    assert _terminal_patches(app, run.id) == ["failed"]
    assert report["dropped_writes"] == 2 and report["remaining"] == 0
    (warning,) = [str(w.message) for w in caught if "dropped" in str(w.message)]
    assert "could NOT be marked: its close (failed) was already sent" in warning
    assert "probe_finish" not in (app.runs[run.id].get("summary") or {})


def _hang(app, monkeypatch, run_id, *, hang_s=30.0) -> list:
    """Every request about ``run_id`` stalls like a hung server: it waits out
    the attempt's own read timeout (at most ``hang_s``), then times out."""
    import time as _time

    import httpx

    real = app._dispatch
    hung: list = []

    def dispatch(request):
        if f"/v1/runs/{run_id}" in request.url.path:
            read = (request.extensions.get("timeout") or {}).get("read")
            hung.append(request.method)
            _time.sleep(min(hang_s, hang_s if read is None else read))
            raise httpx.ReadTimeout("stalled", request=request)
        return real(request)

    monkeypatch.setattr(app, "_dispatch", dispatch)
    return hung


def test_a_reinit_against_a_hung_api_and_a_hashing_backlog_keeps_its_cap(
    app, wired, monkeypatch, tmp_path
):
    """The 10 s promise, with both things that used to break it: requests that
    hang until they time out (30 s each in prod) and read capture still
    hashing a file, which waited up to 30 s of its own outside any deadline."""
    import time as _time

    from probe.sdk import inputs

    monkeypatch.setenv(inputs.READS_ENV, "1")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "3600")
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)
    monkeypatch.setattr(fluent, "_REINIT_FLUSH_CAP_S", 1.0)
    release = threading.Event()
    monkeypatch.setattr(inputs, "hash_file", lambda *a, **k: release.wait(60) and ("x", None))
    inputs._hash_results.clear()
    try:
        first = probe.init(experiment="e1", name="r1", capture_reads=True)
        data = tmp_path / "dataset.bin"
        data.write_bytes(b"d" * 4096)
        data.read_bytes()  # the hasher picks it up and stalls on it
        _time.sleep(0.2)
        probe.log({"loss": 0.5}, step=1)
        hung = _hang(app, monkeypatch, first.id)

        began = _time.monotonic()
        with pytest.warns(UserWarning):
            second = probe.init(experiment="e1", name="r2", capture_reads=False)
        took = _time.monotonic() - began
    finally:
        release.set()
        inputs._active.clear()

    assert took < 1.0 + 1.0, f"a 1 s reinit cap took {took:.1f}s"
    assert hung, "the close did try the hung server"
    assert probe.active_run() is second
    queued = _pending_for(wired[0], first.id)
    assert queued and queued[-1]["method"] == "PATCH", "the close waits behind the data"


def test_create_new_runs_release_their_clients_when_their_handle_closes(app, wired):
    """Only the handle can close a `create_new` run. Its client stayed open
    (with its connection pool) until the next create_new, or exit."""
    probe.init(experiment="e1", name="bound")
    for i in range(3):
        run = probe.init(experiment="e1", name=f"sweep{i}", reinit="create_new")
        run.finish()
    with probe.init(experiment="e1", name="in-a-with", reinit="create_new"):
        pass
    assert [c for c in wired[1:] if not c.transport._client.is_closed] == []
    assert fluent._unbound == []
    assert not wired[0].transport._client.is_closed, "the bound run's client is untouched"


def test_a_reinit_over_dead_letters_keeps_closed_by_beside_the_count(app, wired, monkeypatch):
    """#2011's dead-letter close wrote a fresh `probe_finish`, dropping the
    reinit's `closed_by` (its deferred close did too)."""
    first = probe.init(experiment="e1", name="r1")
    _refuse(app, monkeypatch, "POST", f"/v1/runs/{first.id}/metrics", 422)
    probe.log({"loss": 0.5}, step=1)

    with pytest.warns(UserWarning, match="dead-lettered"):
        probe.init(experiment="e1", name="r2")

    assert _terminal_patches(app, first.id) == ["completed"]
    accounting = _summary(app, first.id)["probe_finish"]
    assert accounting["closed_by"] == "reinit" and accounting["dead_lettered"] == 1


def _interrupt_the_close(app, monkeypatch, run, where, interrupt=KeyboardInterrupt):
    """``interrupt`` lands in the close: in its terminal write, or earlier,
    while the hardware collector is being stopped."""
    if where == "terminal write":
        real = app._dispatch

        def dispatch(request):
            if request.method == "PATCH" and request.url.path == f"/v1/runs/{run.id}":
                raise interrupt()
            return real(request)

        monkeypatch.setattr(app, "_dispatch", dispatch)
    else:

        def stop(timeout=None):
            raise interrupt()

        run._hw_monitor = types.SimpleNamespace(finish=stop)


@pytest.mark.parametrize("where", ["terminal write", "hardware stop"])
@pytest.mark.parametrize(
    "interrupt", [KeyboardInterrupt, lambda: SystemExit(3)], ids=["ctrl-c", "sys.exit(3)"]
)
def test_ctrl_c_during_the_reinit_close_queues_canceled(app, wired, monkeypatch, where, interrupt):
    """The old run was left `running` and reaped `crashed`. A reinit's close is
    not the caller's choice, so an interrupt cutting it short queues
    `canceled` -- not the `failed` a SystemExit's code alone reads as
    (hardware stop). Once its terminal write is on the wire the server may
    already have applied it, so that same `completed` is queued again, never a
    `canceled` that would land later and overwrite it (terminal write)."""
    first = probe.init(experiment="e1", name="r1")
    _interrupt_the_close(app, monkeypatch, first, where, interrupt)

    with pytest.raises((KeyboardInterrupt, SystemExit)):
        probe.init(experiment="e1", name="r2")

    (close,) = [op for op in _pending_for(wired[0], first.id) if op["method"] == "PATCH"]
    assert close["body"]["status"] == ("completed" if where == "terminal write" else "canceled")
    assert close["body"]["summary"]["probe_finish"]["closed_by"] == "reinit"
    assert len(app.runs) == 1, "no new run was opened"


# -- review of #2016, round 3: the bound, a rejected verdict, the edges --------


class _HungSource:
    """A hardware source whose every call after the first hangs, like NVML on
    a failing GPU. Records the thread of each call."""

    families = frozenset({"gpu"})

    def __init__(self):
        self.threads: list[str] = []
        self.release = threading.Event()

    def sample(self, now):
        from probe.hw.types import HwSample

        self.threads.append(threading.current_thread().name)
        if len(self.threads) > 1:
            self.release.wait(30)
        return [HwSample(key="gpu/util", value=1.0, coords={"gpu": "0"}, agg="mean")]


def test_a_reinit_with_a_hung_hardware_query_keeps_its_bound(app, wired, monkeypatch):
    """`HwMonitor.finish()` joined the collector for 5 s, then sampled again ON
    THE CALLER'S THREAD, which hung with no limit: 13 s at a 1 s cap. It now
    waits within the close's deadline and never samples from the caller."""
    import time as _time

    from probe.hw.monitor import HwMonitor

    monkeypatch.setattr(fluent, "_REINIT_FLUSH_CAP_S", 1.0)
    first = probe.init(experiment="e1", name="r1")
    source = _HungSource()
    monitor = HwMonitor([source], emit=lambda points: None, interval=0.02)
    monitor.start()
    first._hw_monitor = monitor
    try:
        deadline = _time.monotonic() + 5
        while len(source.threads) < 2 and _time.monotonic() < deadline:
            _time.sleep(0.01)  # the collector is now inside its hung call
        began = _time.monotonic()
        second = probe.init(experiment="e1", name="r2")
        took = _time.monotonic() - began
    finally:
        source.release.set()
        monitor._thread.join(5)
    print(f"\nreinit with a hung hardware query: {took:.2f}s at a 1 s cap")
    # The bug this guards was 13s at a 1s cap, well over 2x the 3.0 bound
    # below; widened alongside the exporter test for the same CI jitter.
    assert took < 3.0, f"a 1 s reinit cap took {took:.1f}s"
    assert set(source.threads) == {"probe-hw-monitor"}, "sampled on the caller's thread"
    assert _terminal_patches(app, first.id) == ["completed"]
    assert probe.active_run() is second


def test_a_finish_that_stops_a_healthy_collector_still_flushes_its_windows():
    """The windows the collector completed still go out (the control for the
    test above), and so does the one open at the close: the collector's own
    last pass samples it (lane E3), never the caller's thread."""
    from probe.hw.grid import HW_STEP_SECONDS
    from probe.hw.monitor import HwMonitor
    from probe.hw.types import HwSample

    clock = types.SimpleNamespace(t=1_000_000.0)
    emitted: list = []
    calls: list = []

    class Source:
        families = frozenset({"system"})

        def sample(self, now):
            calls.append(threading.current_thread().name)
            return [HwSample("hw/cpu/utilization", 5.0, {}, "mean")]

    monitor = HwMonitor([Source()], emit=emitted.extend, clock=lambda: clock.t, interval=3600)
    monitor.tick()  # one window's sample, as the collector thread takes it
    monitor.start()
    clock.t += HW_STEP_SECONDS  # the window completed during shutdown
    monitor.finish(timeout=2.0)
    first = int(1_000_000.0 // HW_STEP_SECONDS)
    assert [(p.key, p.step) for p in emitted] == [
        ("hw/cpu/utilization", first),
        ("hw/cpu/utilization", first + 1),
    ]
    # The hand-driven tick above, then the collector's last pass.
    assert calls == [threading.current_thread().name, "probe-hw-monitor"], "finish() itself never sampled"


def test_a_reinit_with_an_exporter_stuck_mid_request_keeps_its_bound(app, tmp_path, monkeypatch):
    """Releasing the old client joined its exporter for up to 5 s AFTER the
    close's deadline: 6 s at a 1 s cap. The join now takes what is left of the
    bound, and what the exporter could not send stays queued."""
    import time as _time

    built = []

    def factory(*_a, **_kw):
        client = make_client(
            app, tmp_spool=tmp_path / f"spool{len(built)}", async_writes=True, drain_interval=0.05
        )
        built.append(client)
        return client

    monkeypatch.setattr(fluent, "Client", factory)
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "3600")
    monkeypatch.setattr(fluent, "_REINIT_FLUSH_CAP_S", 1.0)
    app.seed_experiment("e1")
    first = probe.init(experiment="e1", name="r1")
    hung = _hang(app, monkeypatch, first.id, hang_s=30.0)
    for i in range(3):
        probe.log({"loss": 0.5}, step=i)
    deadline = _time.monotonic() + 5
    while not hung and _time.monotonic() < deadline:
        _time.sleep(0.01)  # the exporter is inside a request now
    began = _time.monotonic()
    with pytest.warns(UserWarning, match="queued"):
        probe.init(experiment="e1", name="r2")
    took = _time.monotonic() - began
    print(f"\nreinit with the exporter stuck mid-request: {took:.2f}s at a 1 s cap")
    # The bug this guards was 6s (the old 5s post-deadline join) at a 1s cap;
    # 3.0 still proves the bound, with slack for a loaded CI runner.
    assert took < 3.0, f"a 1 s reinit cap took {took:.1f}s"
    queued = _pending_for(built[0], first.id)
    assert [op["method"] for op in queued].count("POST") >= 1, "the data stays queued"
    assert queued[-1]["method"] == "PATCH" and queued[-1]["body"]["status"] == "completed"


def test_a_held_commit_false_row_is_sent_inside_the_reinit_bound(app, wired, monkeypatch):
    """A `log(commit=False)` row was flushed BEFORE the close's deadline began,
    so under sync writes a hung API held it for the transport's own timeout
    (30 s in prod; 3 s here at a 1 s cap). It is now sent inside the deadline,
    and a row that runs out of time is queued, never dropped."""
    import time as _time

    monkeypatch.setattr(fluent, "_REINIT_FLUSH_CAP_S", 1.0)
    first = probe.init(experiment="e1", name="r1")
    probe.log({"loss": 0.5}, step=1, commit=False)
    _hang(app, monkeypatch, first.id, hang_s=3.0)
    began = _time.monotonic()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        probe.init(experiment="e1", name="r2")
    took = _time.monotonic() - began
    print(f"\nreinit holding a commit=False row against a hung API: {took:.2f}s at a 1 s cap")
    assert took < 1.5, f"a 1 s reinit cap took {took:.1f}s"
    queued = _pending_for(wired[0], first.id)
    rows = [op for op in queued if op["method"] == "POST" and op["path"].endswith("/metrics")]
    assert rows, "the held row is queued, not dropped"
    assert queued[-1]["method"] == "PATCH", "the close waits behind it"


def test_a_verdict_the_server_rejects_is_reported_rejected_not_sent(app, client, monkeypatch):
    """`set_status("failed")` hit a 503 and was queued; the server then refused
    it for good (409). finish() said "its close (failed) was already sent" and
    counted the close as a data dead letter, while the run stayed `running`
    (the base branch said `close_rejected`)."""
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1", heartbeat=False)
    _refuse_run_patch(app, monkeypatch, run.id, 503)
    run.set_status("failed")
    _refuse_run_patch(app, monkeypatch, run.id, 409)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        report = run.finish()

    messages = [str(w.message) for w in caught]
    assert report["close_rejected"] is True
    assert "dead_lettered" not in report, "the only dead letter is the close itself"
    assert any("not closed: the terminal status was rejected" in m for m in messages), messages
    assert not any("already sent" in m for m in messages), messages
    assert app.runs[run.id]["status"] == "running"


def test_a_verdict_that_is_still_queued_is_not_called_sent(app, client, monkeypatch):
    """The control: a queued verdict the server has not answered yet stays
    queued, and finish() says so instead of "already sent"."""
    monkeypatch.setenv("PROBE_FINISH_TIMEOUT_SEC", "0.3")
    app.seed_experiment("e1")
    run = client.run(experiment="e1", name="r1", heartbeat=False)
    _refuse_run_patch(app, monkeypatch, run.id, 503)
    run.set_status("failed")

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        report = run.finish()

    messages = [str(w.message) for w in caught]
    assert not report.get("close_rejected")
    assert report["remaining"] == 1
    assert any("closing failed (queued)" in m for m in messages), messages
    (close,) = _pending_for(client, run.id)
    assert close["body"]["status"] == "failed"


def test_other_threads_logs_wait_at_most_the_cap_for_a_slow_new_run(app, wired, monkeypatch):
    """Another thread's probe.log() waited on the reinit lock for as long as
    the NEW run took to open (4 s for a 4 s create, ~122 s against an API that
    is down). It now waits at most the cap after the old run is let go, then
    drops the row with one warning -- it never raises into the loop -- and the
    new run's close counts it in `probe_finish.dropped_writes`. An artifact is
    dropped the same way; `span` and `update_config` raise, saying why."""
    import time as _time

    monkeypatch.setattr(fluent, "_REINIT_FLUSH_CAP_S", 0.5)
    probe.init(experiment="e1", name="r1")
    real_open = fluent._open_and_bind
    outcome: dict = {"took": []}

    def worker():
        for step in range(3):
            began = _time.monotonic()
            try:
                outcome.setdefault("returned", []).append(probe.log({"x": 1.0}, step=step))
            except Exception as exc:  # noqa: BLE001
                outcome["error"] = exc
            outcome["took"].append(_time.monotonic() - began)
        try:
            outcome["artifact"] = probe.log_artifact("ckpt", uri="s3://bucket/ckpt")
        except Exception as exc:  # noqa: BLE001
            outcome["error"] = exc
        for name, call in (("span", lambda: probe.span("eval")), ("config", lambda: probe.update_config({"a": 1}))):
            try:
                call()
                outcome[name] = "returned"
            except probe.errors.RosError as exc:
                outcome[name] = str(exc)

    def slow_open(*a, **k):
        thread = threading.Thread(target=worker)
        thread.start()
        outcome["thread"] = thread
        _time.sleep(3.0)  # a slow create of the new run
        return real_open(*a, **k)

    monkeypatch.setattr(fluent, "_open_and_bind", slow_open)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        second = probe.init(experiment="e1", name="r2")
        outcome["thread"].join(10)
    print(f"\nother thread's probe.log() calls during a 3 s create took {outcome['took']}")
    assert "error" not in outcome, outcome.get("error")
    assert outcome["returned"] == [None, None, None]
    assert max(outcome["took"]) < 1.0, outcome["took"]
    assert sum(outcome["took"]) < 1.2, "only the first call waits"
    drops = [w for w in caught if "still opening the next one" in str(w.message)]
    assert len(drops) == 1, [str(w.message) for w in caught]
    assert outcome["artifact"] is None
    assert "still opening the next one" in outcome["span"]
    assert "still opening the next one" in outcome["config"]
    probe.log({"x": 2.0}, step=9)
    assert app.metric_points_posted[second.id], "logging resumes on the new run"
    with pytest.warns(UserWarning, match=r"4 write\(s\) for run .* were dropped"):
        probe.finish()
    assert _summary(app, second.id)["probe_finish"]["dropped_writes"] == 4


def test_a_write_that_gives_up_just_as_the_new_run_binds_is_still_counted(app, wired, monkeypatch):
    """The window's edge: a write whose wait ran out lands after the reinit
    bound the new run. It is counted on that run, not lost from the count."""
    probe.init(experiment="e1", name="r1")
    second = probe.init(experiment="e1", name="r2")
    assert fluent._reinit_new_run is second
    fluent._drop_during_reinit("log")  # the late one
    with pytest.warns(UserWarning, match=r"1 write\(s\) for run .* were dropped"):
        probe.finish()
    assert _summary(app, second.id)["probe_finish"]["dropped_writes"] == 1


def test_ctrl_c_after_the_server_applied_the_reinit_close_keeps_it(app, wired, monkeypatch, tmp_path):
    """The server applied `completed`, then Ctrl-C cut the response off. The
    close had no answer, so the interrupt path queued `canceled`, which landed
    later and overwrote the `completed` (race from #2011). It now queues that
    same `completed` again: a replay that cannot change the verdict."""
    first = probe.init(experiment="e1", name="r1")
    real = app._dispatch

    def dispatch(request):
        response = real(request)
        if request.method == "PATCH" and request.url.path == f"/v1/runs/{first.id}":
            if json.loads(request.content or b"{}").get("status") == "completed":
                raise KeyboardInterrupt()
        return response

    monkeypatch.setattr(app, "_dispatch", dispatch)
    with pytest.raises(KeyboardInterrupt):
        probe.init(experiment="e1", name="r2")
    monkeypatch.setattr(app, "_dispatch", real)

    queued = [op["body"]["status"] for op in _pending_for(wired[0], first.id)]
    assert queued == ["completed"]
    make_client(app, tmp_spool=tmp_path / "spool").flush()  # the detached worker's pass
    assert app.runs[first.id]["status"] == "completed"
    assert _terminal_patches(app, first.id) == ["completed", "completed"]


def test_ctrl_c_while_the_close_hashes_reads_cancels_instead_of_completing(
    app, wired, monkeypatch, tmp_path
):
    """Read capture swallowed a Ctrl-C that landed while the close waited on
    hashing, so the close went on and marked the run `completed`. The
    interrupt now reaches the close, which queues `canceled` and re-raises."""
    from probe.sdk import inputs

    monkeypatch.setenv(inputs.READS_ENV, "1")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    first = probe.init(experiment="e1", name="r1", capture_reads=True)
    assert inputs.is_recording(first.id)

    def interrupted(*_a, **_k):
        raise KeyboardInterrupt()

    monkeypatch.setattr(inputs, "collect_all", interrupted)
    try:
        with pytest.raises(KeyboardInterrupt):
            probe.finish()
    finally:
        inputs._active.clear()

    assert _terminal_patches(app, first.id) == []
    (close,) = [op for op in _pending_for(wired[0], first.id) if op["method"] == "PATCH"]
    assert close["body"]["status"] == "canceled"


def test_a_run_closed_elsewhere_never_hands_its_thread_another_threads_run(app, wired):
    """A context whose run was closed from elsewhere fell through to the
    process default -- which, in a plain threaded script, can be ANOTHER
    thread's run: its logs landed there. Only a default bound on the same
    thread (a notebook's await cell) is reachable that way now."""
    first = probe.init(experiment="e1", name="main")
    closer = threading.Thread(target=probe.finish)  # sees `first` via the default
    closer.start()
    closer.join()
    opened: dict = {}
    ready, done = threading.Event(), threading.Event()

    def other_thread():
        opened["run"] = probe.init(experiment="e1", name="worker")
        ready.set()
        done.wait(10)
        probe.finish()

    worker = threading.Thread(target=other_thread)
    worker.start()
    try:
        assert ready.wait(10)
        assert fluent._process_default is not None and fluent._process_default.run is opened["run"]
        assert probe.active_run() is None
        with pytest.raises(probe.errors.RosError, match="no active run"):
            probe.log({"loss": 0.1}, step=1)
    finally:
        done.set()
        worker.join(10)
    assert first.id != opened["run"].id
    assert not app.metric_points_posted.get(opened["run"].id), "main's log landed in the worker's run"


def test_an_online_init_after_a_disabled_one_replaces_it_quietly(app, wired, capsys):
    """A `PROBE_MODE=disabled` run has no private surface: reading
    `_finish_called()` off it raised AttributeError out of the next init()."""
    disabled = probe.init(experiment="e1", name="off", mode="disabled")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        run = probe.init(experiment="e1", name="on")
    assert probe.active_run() is run and not getattr(run, "disabled", False)
    assert disabled.status == "completed"
    assert "closed run" not in capsys.readouterr().out, "nothing was recorded, so nothing to say"


def test_the_exit_hook_with_a_disabled_run_bound_does_not_raise(app, wired, hooks):
    probe.init(experiment="e1", name="r1")  # installs the exit hooks
    probe.finish()
    disabled = probe.init(experiment="e1", name="off", mode="disabled")
    fluent._finish_at_exit()  # must not raise
    assert disabled.status == "completed"


def test_a_disabled_init_after_an_online_one_closes_the_online_run(app, wired, capsys):
    """`probe.init(mode="disabled")` bound its no-op run over the open online
    one and left it `running` for the reaper, its client open. `reinit`
    applies to a disabled init too."""
    first = probe.init(experiment="e1", name="r1")
    disabled = probe.init(mode="disabled")
    assert getattr(disabled, "disabled", False) and probe.active_run() is disabled
    assert _terminal_patches(app, first.id) == ["completed"]
    assert _summary(app, first.id)["probe_finish"]["closed_by"] == "reinit"
    assert wired[0].transport._client.is_closed, "the online run's client was let go"
    assert "closed run" in capsys.readouterr().out


def test_a_disabled_init_keeps_the_online_run_on_return_previous_or_create_new(app, wired):
    first = probe.init(experiment="e1", name="r1")
    with pytest.warns(UserWarning, match="ignored name"):
        assert probe.init(mode="disabled", name="x", reinit="return_previous") is first
    side = probe.init(mode="disabled", reinit="create_new")
    assert getattr(side, "disabled", False)
    assert probe.active_run() is first, "a create_new run is never bound"
    assert _terminal_patches(app, first.id) == []
    probe.finish()
    assert _terminal_patches(app, first.id) == ["completed"]
