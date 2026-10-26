"""Two sessions' daemon runs in one process keep their own state (plan H1-H7).

The daemon host runs every session's worker as a thread of one process
(`probe.daemon.host`). Whatever one process per session got for free -- its own
environment, the model's refusal fallback and pushed settings, the alert gate,
the lease's identity -- each run must now keep apart from the others. Outside a
run (one session per process, and the tests that patch module globals) every
value is still the module global.
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
import time
from pathlib import Path

import pytest

from probe.daemon import alerts, lease, runctx
from probe.daemon import model as model_mod


@pytest.fixture
def environ():
    wrapped = runctx.install()
    try:
        yield wrapped
    finally:
        runctx.uninstall()


def _in_thread(fn):
    out: dict = {}

    def target():
        try:
            out["value"] = fn()
        except BaseException as exc:  # noqa: BLE001 -- re-raised on the test's thread
            out["error"] = exc

    t = threading.Thread(target=target)
    t.start()
    t.join(30)
    assert not t.is_alive()
    if "error" in out:
        raise out["error"]
    return out["value"]


def test_shared_is_the_module_global_outside_a_run_and_each_runs_own_inside(monkeypatch):
    monkeypatch.setattr(model_mod, "_PREFERRED_MODEL", "patched-by-a-test")
    assert model_mod._preferred.get() == "patched-by-a-test"
    a, b = runctx.Run("a"), runctx.Run("b")
    with runctx.enter(a):
        assert model_mod._preferred.get() is None
        model_mod._preferred.set("fallback-a")
    with runctx.enter(b):
        assert model_mod._preferred.get() is None
    with runctx.enter(a):
        assert model_mod._preferred.get() == "fallback-a"
    assert model_mod._PREFERRED_MODEL == "patched-by-a-test"


def test_pushed_settings_and_context_sizes_stay_with_the_run_that_heard_them():
    a, b = runctx.Run("a"), runctx.Run("b")
    headers = {model_mod.READER_GATE_HEADER: "on", model_mod.WRITER_GAP_HEADER: "90",
               model_mod.CONTEXT_CAP_HEADERS[model_mod.LANE_WRITE]: "150000"}
    with runctx.enter(a):
        model_mod.remember_pushed_settings(headers)
        model_mod.remember_context_sizes(headers)
        assert model_mod.reader_gate_mode() == model_mod.GateMode.ON
        assert model_mod.writer_min_gap_s() == 90
        assert model_mod.server_context_tokens(model_mod.LANE_WRITE) == 150_000
    with runctx.enter(b):
        assert model_mod.reader_gate_mode() == model_mod.GateMode.OFF
        assert model_mod.writer_min_gap_s() == 0
        assert model_mod.server_context_tokens(model_mod.LANE_WRITE) is None


def test_the_served_fallback_model_is_sent_only_by_the_session_it_was_served_to():
    class Request:
        def __init__(self):
            self.url = type("U", (), {"path": "/v1/companion/chat/completions"})()
            self.headers = {}

    class Response:
        def __init__(self, served):
            self.request = Request()
            self.headers = {model_mod.SERVED_MODEL_HEADER: served}

    a, b = runctx.Run("a"), runctx.Run("b")
    with runctx.enter(a):
        asyncio.run(model_mod._remember_served_model(Response("claude-sonnet-5")))
        sent = Request()
        asyncio.run(model_mod._prefer_served_model(sent))
        assert sent.headers[model_mod.PREFER_MODEL_HEADER] == "claude-sonnet-5"
    with runctx.enter(b):
        sent = Request()
        asyncio.run(model_mod._prefer_served_model(sent))
        assert model_mod.PREFER_MODEL_HEADER not in sent.headers


def test_each_run_reads_its_own_environment_in_tasks_to_thread_and_its_executor(environ, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_KEY", "the-process-key")

    def run_as(name: str):
        run = runctx.Run(name, env={"PROBE_DAEMON_KEY": f"key-{name}", "HOME": f"/home/{name}"})
        with runctx.enter(run):
            async def body():
                loop = asyncio.get_running_loop()
                loop.set_default_executor(runctx.executor(run))
                in_task = os.environ["PROBE_DAEMON_KEY"]
                in_thread = await asyncio.to_thread(os.getenv, "PROBE_DAEMON_KEY")
                in_executor = await loop.run_in_executor(None, os.getenv, "PROBE_DAEMON_KEY")
                home = await asyncio.to_thread(lambda: str(Path.home()))
                return in_task, in_thread, in_executor, home

            return asyncio.run(body())

    assert _in_thread(lambda: run_as("a")) == ("key-a", "key-a", "key-a", "/home/a")
    assert _in_thread(lambda: run_as("b")) == ("key-b", "key-b", "key-b", "/home/b")
    assert os.environ["PROBE_DAEMON_KEY"] == "the-process-key"


def test_a_write_inside_a_run_never_reaches_the_process_or_another_run(environ, monkeypatch):
    monkeypatch.delenv("PROBE_RUNCTX_PROBE", raising=False)
    a = runctx.Run("a", env={})
    with runctx.enter(a):
        os.environ["PROBE_RUNCTX_PROBE"] = "a"
        assert os.environ.copy() == {"PROBE_RUNCTX_PROBE": "a"}
    assert "PROBE_RUNCTX_PROBE" not in os.environ
    with runctx.enter(runctx.Run("b", env={})):
        assert "PROBE_RUNCTX_PROBE" not in os.environ


def test_the_endpoint_and_model_names_are_each_runs_own(environ, monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "none"))
    base = {"XDG_CONFIG_HOME": str(tmp_path / "none"), "HOME": str(tmp_path)}
    a = runctx.Run("a", env={**base, "PROBE_DAEMON_KEY": "ka", "PROBE_BASE_URL": "https://a.example",
                             "PROBE_COMPANION_MODEL": "model-a"})
    b = runctx.Run("b", env={**base, "PROBE_DAEMON_KEY": "kb", "PROBE_BASE_URL": "https://b.example"})
    with runctx.enter(a):
        ep = model_mod.endpoint()
        assert (ep.base_url, ep.key, model_mod._lane_model(model_mod.LANE_WRITE)) == ("https://a.example", "ka",
                                                                                     "model-a")
    with runctx.enter(b):
        ep = model_mod.endpoint()
        assert (ep.base_url, ep.key, model_mod._lane_model(model_mod.LANE_WRITE)) == ("https://b.example", "kb",
                                                                                     "default")


def test_a_runs_own_context_size_wins_inside_the_run(environ):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import agent as agent_mod

    with runctx.enter(runctx.Run("a", env={"PROBE_DAEMON_CONTEXT_TOKENS": "180000"})):
        assert agent_mod.writer_context_tokens() == 180_000
    with runctx.enter(runctx.Run("b", env={})):
        assert agent_mod.writer_context_tokens() == agent_mod.CONTEXT_TOKENS


def test_the_alert_gate_is_each_runs_own(monkeypatch):
    monkeypatch.setattr(alerts, "_base_url", None)
    with runctx.enter(runctx.Run("hosted")):
        alerts.configure("https://api.research.prbe.ai")
        assert alerts._base.get() == "https://api.research.prbe.ai"
    with runctx.enter(runctx.Run("self-hosted")):
        alerts.configure("https://probe.internal.example")
        assert alerts._base.get() == "https://probe.internal.example"
    with runctx.enter(runctx.Run("unconfigured")):
        assert alerts._base.get() is None
    assert alerts._base_url is None


def test_two_runs_of_one_session_in_one_process_never_both_hold_its_lease(environ, monkeypatch, tmp_path):
    env = {"XDG_STATE_HOME": str(tmp_path / "state"), "HOME": str(tmp_path)}
    sessions = tmp_path / "state" / "probe" / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "s1.state").write_text("daemon")
    old, new = runctx.Run("s1", env=dict(env)), runctx.Run("s1", env=dict(env))
    with runctx.enter(old):
        assert lease.renew("s1")
        assert lease.held("s1")
        assert lease.may_write("s1") is None
    record = json.loads((sessions / "s1.writer").read_text())
    assert record["pid"] == os.getpid() and record["owner"] == old.token
    with runctx.enter(new):
        assert not lease.held("s1")
        assert lease.may_write("s1") == "another daemon process holds the session's write lease"
        from probe.daemon import worker as worker_mod

        assert worker_mod._foreign_lease("s1")
    with runctx.enter(old):
        assert lease.release("s1", lease.REASON_HANDOVER)
    with runctx.enter(new):
        assert lease.renew("s1") and lease.held("s1")


def test_a_lease_without_an_owner_is_a_per_process_workers_as_before(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    sessions = tmp_path / "state" / "probe" / "sessions"
    sessions.mkdir(parents=True)
    (sessions / "s1.state").write_text("daemon")
    assert lease.renew("s1")
    record = json.loads((sessions / "s1.writer").read_text())
    assert "owner" not in record  # the format every reader (tap, CLI, hooks) knows
    assert lease.held("s1") and lease.may_write("s1") is None
    with runctx.enter(runctx.Run("s1")):
        assert not lease.held("s1")  # a hosted run never takes a per-process worker's lease as its own


def test_relative_path_variables_are_made_absolute_against_the_session_folder(tmp_path):
    env = {"PROBE_CONFIG_PATH": "conf/probe.json", "SSL_CERT_DIR": f"certs{os.pathsep}/etc/ssl/certs",
           "SSL_CERT_FILE": "/abs/ca.pem", "XDG_STATE_HOME": "~/state", "PATH": "bin"}
    out = runctx.absolute_paths(env, str(tmp_path))
    assert out["PROBE_CONFIG_PATH"] == str(tmp_path / "conf" / "probe.json")
    assert out["SSL_CERT_DIR"] == f"{tmp_path / 'certs'}{os.pathsep}/etc/ssl/certs"
    assert out["SSL_CERT_FILE"] == "/abs/ca.pem"
    assert out["XDG_STATE_HOME"] == "~/state"  # the reader expands it, as before
    assert out["PATH"] == "bin"  # not a path variable here: a command search list
    assert env["PROBE_CONFIG_PATH"] == "conf/probe.json"  # a copy


def test_two_workers_in_one_process_keep_their_stores_and_state_folders_apart(environ, monkeypatch, tmp_path):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import worker as worker_mod

    made = {}
    for name in ("a", "b"):
        home = tmp_path / name
        (home / "state" / "probe" / "sessions").mkdir(parents=True)
        (home / "state" / "probe" / "sessions" / f"sid-{name}.state").write_text("daemon")
        project = home / "project"
        project.mkdir()
        transcript = project / "t.jsonl"
        transcript.write_text("")
        run = runctx.Run(f"sid-{name}", env={"HOME": str(home), "XDG_STATE_HOME": str(home / "state"),
                                              "XDG_CONFIG_HOME": str(home / "config")})

        def build(run=run, project=project, transcript=transcript, name=name):
            with runctx.enter(run):
                w = worker_mod.Worker(worker_mod.Session(f"sid-{name}", transcript, project, "claude_code"))
                assert w._renew()
                return str(w.store.path) if hasattr(w.store, "path") else str(worker_mod.store_path(f"sid-{name}"))

        made[name] = _in_thread(build)
    assert made["a"].startswith(str(tmp_path / "a" / "state"))
    assert made["b"].startswith(str(tmp_path / "b" / "state"))
    for name in ("a", "b"):
        assert (tmp_path / name / "state" / "probe" / "sessions" / f"sid-{name}.writer").exists()


def test_every_child_the_daemon_starts_passes_its_environment():
    """A child started without `env=` inherits the process's C-level environment,
    not the run's (`runctx.ContextEnviron`): in the daemon host it would run with
    another session's -- or the host's -- variables."""
    import ast

    root = Path(__import__("probe.daemon", fromlist=["x"]).__file__).parent
    spawners = {"subprocess": {"Popen", "run", "call", "check_call", "check_output"},
                "asyncio": {"create_subprocess_exec", "create_subprocess_shell"}}

    def passes_env(node: ast.Call) -> bool:
        # `env=None` is the process's environment again.
        return any(k.arg == "env" and not (isinstance(k.value, ast.Constant) and k.value.value is None)
                   for k in node.keywords)

    missing, seen = [], 0
    for path in sorted(root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            owner = node.func.value
            owner_name = owner.id if isinstance(owner, ast.Name) else getattr(owner, "attr", "")
            if node.func.attr in spawners.get(owner_name, ()):
                seen += 1
                if not passes_env(node):
                    missing.append(f"{path.relative_to(root)}:{node.lineno}")
    assert seen >= 3, "the scan found none of the daemon's spawn sites: its shape changed"
    assert missing == []


# ---------------------------------------------------------------------------
# A stop asked of a run (`worker.Stopper`): every moment it can arrive, from the
# run's own thread (a per-process signal) or another (the host's `stop`).
# ---------------------------------------------------------------------------


class _Stoppable:
    def __init__(self):
        self.calls: list[int] = []

    def begin_stopping(self):
        self.calls.append(threading.get_ident())


def test_a_stop_before_the_worker_exists_begins_as_soon_as_it_does():
    from probe.daemon import worker as worker_mod

    stopper, worker = worker_mod.Stopper(), _Stoppable()
    stopper.request()  # SIGTERM while the libraries load
    stopper.bind(worker)  # run_session, right after Worker(session): before the sweeps, as before
    assert stopper.asked and worker.calls == [threading.get_ident()]


def test_a_signal_before_the_loop_starts_begins_stopping_at_once():
    from probe.daemon import worker as worker_mod

    stopper, worker = worker_mod.Stopper(), _Stoppable()
    stopper.bind(worker)
    stopper.request()  # the handler, on the run's own thread, during the sweeps
    assert worker.calls == [threading.get_ident()]


def test_a_stop_from_another_thread_before_the_loop_is_taken_on_the_loop():
    from probe.daemon import worker as worker_mod

    stopper, worker = worker_mod.Stopper(), _Stoppable()
    stopper.bind(worker)
    _in_thread(lambda: stopper.request())  # the host's `stop`: never another thread's call into the worker
    assert worker.calls == []

    async def body():
        stopper.bind(worker, asyncio.get_running_loop())
        return threading.get_ident()

    assert worker.calls == [asyncio.run(body())]


def test_a_stop_while_the_loop_runs_reaches_the_loops_thread():
    from probe.daemon import worker as worker_mod

    stopper, worker = worker_mod.Stopper(), _Stoppable()

    async def body():
        stopper.bind(worker, asyncio.get_running_loop())
        stopper.request()  # a signal, on the loop's thread: at once
        assert len(worker.calls) == 1
        await asyncio.to_thread(stopper.request)  # the host's, from another thread
        await asyncio.sleep(0)
        return threading.get_ident()

    me = asyncio.run(body())
    assert worker.calls == [me, me]


def test_a_stop_after_the_runs_loop_closed_never_raises():
    """A SIGTERM in run_session's crash report or `finally`, or the host's stop for a
    run that just ended: the old handler never raised there; a raise would skip
    the lease release and exit 1, which the service counts as a crash."""
    from probe.daemon import worker as worker_mod

    for unbound in (True, False):
        stopper, worker = worker_mod.Stopper(), _Stoppable()

        async def body():
            stopper.bind(worker, asyncio.get_running_loop())
            if unbound:
                stopper.unbind()  # what run_session's loop does as it ends

        asyncio.run(body())
        stopper.request()
        _in_thread(lambda: stopper.request())
        assert stopper.asked


def test_a_signal_inside_the_stoppers_lock_never_hangs_the_worker(tmp_path):
    """Per process the stop handler runs on the thread that may be inside the
    stopper's lock (`bind`): it must not wait on it."""
    import subprocess
    import sys
    import textwrap

    code = textwrap.dedent("""
        import os, signal
        from probe.daemon.worker import Stopper
        st = Stopper()
        signal.signal(signal.SIGTERM, lambda s, f: st.request())
        with st._lock:
            os.kill(os.getpid(), signal.SIGTERM)
            for _ in range(1000):
                pass
        print("asked" if st.asked else "not asked")
    """)
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60,
                          env=dict(os.environ))
    assert proc.stdout.strip() == "asked", proc.stderr


def test_a_hosted_worker_asks_its_owner_and_a_process_worker_its_parent(monkeypatch):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import worker as worker_mod

    seen = []
    monkeypatch.setattr(worker_mod, "parent_gone", lambda sup, ppid: seen.append((sup, ppid)) or False)
    w = worker_mod.Worker.__new__(worker_mod.Worker)
    w.supervisor, w.parent_pid, w.supervisor_gone = (42, "start"), 7, None
    assert w._parent_gone() is False and seen == [((42, "start"), 7)]
    w.supervisor_gone = lambda: True
    assert w._parent_gone() is True and len(seen) == 1


def test_a_runs_printed_form_never_shows_its_environment():
    run = runctx.Run("s1", env={"PROBE_DAEMON_KEY": "secret-key"})
    run.slots["x"] = "secret-slot"
    assert "secret" not in repr(run) and "s1" in repr(run)


def test_a_stop_from_another_thread_begins_inside_the_runs_own_context():
    """The host's `stop` comes from its control thread, which runs as no session:
    `begin_stopping` must still see the run (its `.finishing` mark is the
    session's own state folder, not the host's)."""
    from probe.daemon import worker as worker_mod

    run, seen = runctx.Run("s1"), []

    class W:
        def begin_stopping(self):
            seen.append(runctx.current())

    stopper = worker_mod.Stopper()

    async def body():
        stopper.bind(W(), asyncio.get_running_loop())
        t = threading.Thread(target=stopper.request)  # a bare thread: no run of its own
        t.start()
        await asyncio.to_thread(t.join)
        await asyncio.sleep(0)

    def as_the_run():
        with runctx.enter(run):
            asyncio.run(body())

    _in_thread(as_the_run)
    assert seen == [run]


def test_restored_settings_and_task_models_are_each_runs_own():
    """Cost round 7's state (#3403): the settings a worker restores from its store
    until the first chat answer, and the task models it built (each holding an HTTP
    client of its run's loop), belong to the run that made them."""
    a, b = runctx.Run("a"), runctx.Run("b")
    with runctx.enter(a):
        model_mod.restore_pushed({model_mod.WRITER_PROMPT_WAITS_HEADER: "on"})
        assert model_mod.writer_prompt_waits()
        model_mod._task_models.get()[("w", "task", "u", "k")] = "a's model"
    with runctx.enter(b):
        assert not model_mod.writer_prompt_waits()
        assert model_mod._restored.get() == set()
        assert model_mod._task_models.get() == {}
    with runctx.enter(a):
        model_mod._confirm_restored({})  # a's first chat answer did not carry it: dropped for a only
        assert not model_mod.writer_prompt_waits()
    assert model_mod._RESTORED == set() and model_mod._TASK_MODELS == {}


# -- an idle hosted run's wait (plan M2, #3407) ---------------------------------------


def _idle_worker(monkeypatch):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import worker as worker_mod

    monkeypatch.setenv(worker_mod.IDLE_AFTER_ENV, "1")
    monkeypatch.setenv(worker_mod.IDLE_POLL_ENV, "0.6")
    w = worker_mod.Worker.__new__(worker_mod.Worker)
    w.wakeable, w.stopping, w.clock = True, False, time.monotonic
    w.changed_at = time.monotonic() - 10  # idle
    return w


def test_a_poke_during_a_look_is_never_lost(monkeypatch):
    """The watcher pokes while the run is mid-look (after it read its inputs): the
    next wait ends at once, never a whole IDLE_POLL_S later."""
    w = _idle_worker(monkeypatch)

    async def body():
        event = asyncio.Event()
        event.set()  # the poke that landed during the look
        started = time.monotonic()
        await w.pause(2.0, event)
        first = time.monotonic() - started
        started = time.monotonic()
        await w.pause(2.0, event)  # nothing new since: the whole idle wait
        return first, time.monotonic() - started

    first, second = asyncio.run(body())
    assert first < 0.2 and 0.4 < second < 1.5


def test_a_poke_alone_never_ends_idleness(monkeypatch):
    """A spurious poke (an answer in another session's folder) costs one look, not
    a minute of looks every 2 s: idle until a look finds something new."""
    w = _idle_worker(monkeypatch)
    before = w.changed_at

    async def body():
        event = asyncio.Event()
        event.set()
        await w.pause(2.0, event)

    asyncio.run(body())
    assert w.changed_at == before


def test_the_watcher_looks_at_every_stream_the_run_reads(environ, monkeypatch, tmp_path):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import worker as worker_mod

    home = tmp_path / "h"
    (home / "state" / "probe" / "sessions").mkdir(parents=True)
    (home / "state" / "probe" / "sessions" / "sid-w.state").write_text("daemon")
    project = home / "project"
    project.mkdir()
    transcript = project / "t.jsonl"
    transcript.write_text("")
    helper = project / "t" / "subagents" / "agent-1.jsonl"  # a helper agent's own log
    helper.parent.mkdir(parents=True)
    helper.write_text("")
    run = runctx.Run("sid-w", env={"HOME": str(home), "XDG_STATE_HOME": str(home / "state"),
                                    "XDG_CONFIG_HOME": str(home / "config")})

    def check():
        with runctx.enter(run):
            w = worker_mod.Worker(worker_mod.Session("sid-w", transcript, project, "claude_code"))
            read: list = []
            real = Path.stat

            def stat(self, *a, **k):
                read.append(str(self))
                return real(self, *a, **k)

            monkeypatch.setattr(Path, "stat", stat)
            try:
                w._end_offsets()  # every stream the run reads
            finally:
                monkeypatch.setattr(Path, "stat", real)
            watched = {str(p) for p in w.wake_paths()}
            return [p for p in read if p not in watched], str(helper) in watched

    missing, helper_watched = _in_thread(check)
    assert missing == [] and helper_watched
