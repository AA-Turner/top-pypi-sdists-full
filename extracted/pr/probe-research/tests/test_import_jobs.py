"""Durable import scheduling, without reading research files or contacting APIs."""

from __future__ import annotations

import json
import multiprocessing
import os
import signal
import textwrap
import threading
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

from probe.cli import import_jobs as jobs


@pytest.fixture
def queued(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    launches = []

    class Child:
        pid = os.getpid()

        def wait(self):
            return 0

    def spawn(argv, **kwargs):
        launches.append((argv, kwargs))
        return Child()

    monkeypatch.setattr(jobs.subprocess, "Popen", spawn)
    return launches


def _enqueue(approval="review-1", *, kind=jobs.Kind.TRANSCRIPTS):
    return jobs.enqueue(
        kind,
        {"approval_id": approval, "sources": ["claude_code"],
         "scope": {"customer_id": "lab", "workspace_id": "workspace"}},
        "Approved conversations" if kind == jobs.Kind.TRANSCRIPTS else "Approved folder",
    )


def test_enqueue_preserves_approval_and_detaches_every_descriptor(queued):
    payload = {"sources": ["claude_code"], "approval_id": "review-1"}
    job = jobs.enqueue("transcripts", payload, "My conversations")
    payload["sources"].append("codex")
    saved = jobs.get_job(job["id"])
    assert saved["payload"]["sources"] == ["claude_code"]
    argv, launch = queued[0]
    assert argv[:3] == [jobs.sys.executable, "-u", "-c"]
    assert "from probe.cli.import_jobs import main" in argv[3]
    assert argv[4] == str(jobs._source_root())
    assert argv[5] == job["id"]
    assert launch["stdin"] == jobs.subprocess.DEVNULL
    assert launch["stdout"] is launch["stderr"]
    assert launch["start_new_session"] and launch["close_fds"]
    assert "shell" not in launch and "env" not in launch
    assert Path(job["log_path"]).stat().st_mode & 0o777 == 0o600
    folder = Path(job["log_path"]).parent
    assert folder.stat().st_mode & 0o777 == 0o700
    assert (folder / "job.json").stat().st_mode & 0o777 == 0o600


def test_identical_approval_runs_once_and_success_is_not_rescheduled(queued, monkeypatch):
    first = _enqueue()
    assert _enqueue()["id"] == first["id"]
    assert len(queued) == 1
    calls = []
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: calls.append(args) or ["Finished."])
    assert jobs.run_worker(first["id"]) == 0
    assert jobs.resume(first["id"])["state"] == jobs.State.SUCCEEDED
    assert _enqueue()["state"] == jobs.State.SUCCEEDED
    assert jobs.run_worker(first["id"]) == 0
    assert len(calls) == len(queued) == 1
    assert _enqueue("new-approved-fingerprints")["id"] != first["id"]


def test_worker_records_progress_and_keeps_full_log_with_short_report(queued, monkeypatch):
    job = _enqueue()
    snapshots = []

    def execute(kind, payload, progress):
        assert kind == jobs.Kind.TRANSCRIPTS and payload == job["payload"]
        progress("Uploading approved session", completed=2, total=3)
        snapshots.append(jobs.get_job(job["id"]))
        return [f"Result {index}" for index in range(30)]

    monkeypatch.setattr(jobs, "_dispatch", execute)
    assert jobs.run_worker(job["id"]) == 0
    assert snapshots[0]["state"] == jobs.State.RUNNING
    assert snapshots[0]["progress"] == {
        "message": "Uploading approved session", "completed": 2, "total": 3,
    }
    saved = jobs.get_job(job["id"])
    assert saved["attempt"] == 1 and saved["pid"] is None
    assert saved["report"] == [f"Result {index}" for index in range(10, 30)]
    log = Path(saved["log_path"]).read_text()
    assert "Result 0\n" in log and "Result 29\n" in log
    assert "Uploading approved session" in log


def test_connection_retry_keeps_approval_owner_and_caps_backoff(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job["log_path"]).parent
    dispatches, waits = [], []

    def dispatch(kind, payload, progress):
        dispatches.append((kind, payload))
        progress("Uploading approved sessions", completed=1, total=2)
        if len(dispatches) <= 8:
            raise jobs.RetryableJobError("Saved session receipts will resume.")
        return ["Both sessions imported."]

    def sleep(delay):
        saved = jobs.get_job(job["id"])
        assert saved["state"] == jobs.State.RUNNING and saved["error"] is None
        assert saved["progress"]["waiting_for_connection"]
        assert saved["progress"]["completed"] == 1
        assert saved["progress"]["total"] == 2
        assert saved["progress"]["retry_in"] == delay
        assert saved["progress"]["network_retries"] == len(waits) + 1
        with jobs._try_lock(folder / "worker.lock") as acquired:
            assert not acquired
        with jobs._try_lock(folder.parent / "transcripts.lock") as acquired:
            assert not acquired
        assert jobs.recover_jobs()[0]["state"] == jobs.State.RUNNING
        waits.append(delay)

    monkeypatch.setattr(jobs, "_dispatch", dispatch)
    monkeypatch.setattr(jobs.time, "sleep", sleep)
    assert jobs.run_worker(job["id"]) == 0
    assert waits == [2, 4, 8, 16, 32, 60, 60, 60]
    assert dispatches == [(jobs.Kind.TRANSCRIPTS, job["payload"])] * 9
    assert len(queued) == 1
    assert jobs.get_job(job["id"])["attempt"] == 1


def test_connection_wait_interruption_remains_recoverable(queued, monkeypatch):
    job = _enqueue()

    def offline(*args):
        raise jobs.RetryableJobError("Completed uploads are saved.")

    def interrupt(delay):
        raise jobs._Interrupted

    monkeypatch.setattr(jobs, "_dispatch", offline)
    monkeypatch.setattr(jobs.time, "sleep", interrupt)
    assert jobs.run_worker(job["id"]) == 130
    assert jobs.get_job(job["id"])["state"] == jobs.State.INTERRUPTED
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: ["Saved uploads resumed."])
    assert jobs.recover_jobs()[0]["id"] == job["id"]
    assert jobs.run_worker(job["id"]) == 0
    assert jobs.get_job(job["id"])["attempt"] == 2


@pytest.mark.parametrize("status", [400, 401, 402, 403, 404, 408, 409, 422, 429, 500, 502, 503, 504])
def test_retry_classification_only_accepts_temporary_http_statuses(status):
    import httpx
    from urllib.error import HTTPError
    from probe.sdk.errors import error_for

    errors = [
        error_for(status, "private server response"),
        HTTPError("https://private.invalid", status, "private", None, None),
        httpx.HTTPStatusError("private", request=httpx.Request("GET", "https://private.invalid"),
                              response=httpx.Response(status)),
    ]
    assert all(jobs.is_retryable_error(exc) == (status in (408, 429) or status >= 500) for exc in errors)


def test_retry_classification_preserves_typed_causes_and_rejects_ambiguous_errors():
    import errno
    import socket
    from urllib.error import URLError
    import httpx
    from probe.sdk.errors import AuthError, TransportError

    for exc in [TransportError("private"), ConnectionError(), TimeoutError(), socket.gaierror(),
                httpx.ReadTimeout("private"), URLError(ConnectionRefusedError()),
                URLError(OSError(errno.ENETUNREACH, "private")),
                jobs.RetryableJobError("Saved work can retry.")]:
        wrapper = RuntimeError("outer")
        wrapper.__cause__ = exc
        assert jobs.is_retryable_error(wrapper)
    for exc in [ValueError("network failed"), OSError("offline"), FileNotFoundError(),
                URLError("unknown failure"), URLError(PermissionError()),
                jobs.JobError("Account changed."), AuthError("Sign in.")]:
        assert not jobs.is_retryable_error(exc)
    for exc in [jobs.JobError("Model needs attention."), AuthError("Sign in.")]:
        exc.__cause__ = TimeoutError()
        assert not jobs.is_retryable_error(exc)


@pytest.mark.parametrize("error", [jobs.JobError("Sign in to the approved account."), RuntimeError("secret-token")])
def test_failure_needs_explicit_retry_and_does_not_persist_unknown_error_text(queued, monkeypatch, error):
    job = _enqueue()

    def fail(*args):
        raise error

    monkeypatch.setattr(jobs, "_dispatch", fail)
    assert jobs.run_worker(job["id"]) == 1
    failed = jobs.get_job(job["id"])
    assert failed["state"] == jobs.State.FAILED
    assert failed["error"] == (
        str(error) if isinstance(error, jobs.JobError) else "Import failed (RuntimeError)."
    )
    assert jobs.recover_jobs()[0]["state"] == jobs.State.FAILED
    assert _enqueue()["state"] == jobs.State.FAILED
    assert len(queued) == 1
    assert "secret-token" not in json.dumps(failed) + Path(failed["log_path"]).read_text()
    assert jobs.resume(job["id"])["state"] == jobs.State.QUEUED
    assert len(queued) == 2


@pytest.mark.parametrize("payload", [{"access_token": "secret"}, {"scope": {"api-key": "secret"}}, {"env": {}}])
def test_credentials_are_rejected_before_writing_any_job(queued, payload):
    with pytest.raises(jobs.JobError, match="credentials"):
        jobs.enqueue("transcripts", payload, "Unsafe")
    assert jobs.list_jobs() == []
    assert not queued


def test_unknown_or_invalid_ids_do_not_create_directories(queued):
    for job_id in ("../outside", "f" * 32):
        with pytest.raises(jobs.JobError):
            jobs.get_job(job_id)
    assert not jobs.default_dir().exists()


def test_pid_reuse_does_not_leave_an_orphan_queued_forever(queued):
    job = _enqueue()
    folder = Path(job["log_path"]).parent
    jobs._update(folder, pid=os.getpid(), pid_identity="previous-boot-and-process")
    assert jobs.get_job(job["id"])["state"] == jobs.State.INTERRUPTED
    assert jobs.recover_jobs()[0]["id"] == job["id"]
    assert len(queued) == 2


def test_listing_during_launch_does_not_mark_the_new_job_interrupted(queued, monkeypatch):
    spawn = jobs.subprocess.Popen
    observed = []

    def during_launch(argv, **kwargs):
        observed.append(jobs.get_job(argv[5])["state"])
        return spawn(argv, **kwargs)

    monkeypatch.setattr(jobs.subprocess, "Popen", during_launch)
    assert _enqueue()["state"] == jobs.State.QUEUED
    assert observed == [jobs.State.QUEUED]


def test_starting_worker_waits_for_status_read_probe(queued, monkeypatch):
    job = _enqueue()
    entered, release, starting = threading.Event(), threading.Event(), threading.Event()
    outcomes = []
    original_try_lock = jobs._try_lock

    @contextmanager
    def pause_status_probe(path):
        with original_try_lock(path) as acquired:
            if acquired and path.name == "worker.lock" and threading.current_thread() is reader:
                entered.set()
                assert release.wait(5)
            yield acquired

    def start_worker():
        starting.set()
        outcomes.append(jobs.run_worker(job["id"]))

    monkeypatch.setattr(jobs, "_try_lock", pause_status_probe)
    monkeypatch.setattr(jobs, "_dispatch", lambda *a: ["Imported once."])
    reader = threading.Thread(target=jobs.get_job, args=(job["id"],))
    worker = threading.Thread(target=start_worker)
    reader.start()
    try:
        assert entered.wait(5)  # A real status read owns state.lock + worker.lock.
        worker.start()
        assert starting.wait(5)
        worker.join(.2)
        assert worker.is_alive(), "A transient status probe made the worker exit before starting"
    finally:
        release.set()
        reader.join(5)
        if worker.ident is not None:
            worker.join(5)
    assert not reader.is_alive() and not worker.is_alive()
    assert outcomes == [0]
    finished = jobs.get_job(job["id"])
    assert finished["state"] == jobs.State.SUCCEEDED and finished["attempt"] == 1
    assert finished["report"] == ["Imported once."]


def test_process_lock_blocks_a_second_worker_for_the_same_job(queued, monkeypatch):
    job = _enqueue()
    context = multiprocessing.get_context("fork")
    started, release = context.Event(), context.Event()

    def execute(*args):
        started.set()
        assert release.wait(5)
        return ["Done once."]

    monkeypatch.setattr(jobs, "_dispatch", execute)
    first = context.Process(target=jobs.run_worker, args=(job["id"],))
    second = context.Process(target=jobs.run_worker, args=(job["id"],))
    first.start()
    try:
        assert started.wait(5)
        second.start()
        second.join(3)
        assert second.exitcode == 0
        assert jobs.get_job(job["id"])["state"] == jobs.State.RUNNING
    finally:
        release.set()
        first.join(5)
        if second.pid and second.is_alive():
            second.kill()
            second.join()
        if first.is_alive():
            first.kill()
            first.join()
    assert first.exitcode == 0
    assert jobs.get_job(job["id"])["attempt"] == 1


def test_distinct_transcript_approvals_serialize_the_whole_upload_and_digest_pass(queued, monkeypatch):
    first_job, second_job = _enqueue("first"), _enqueue("second")
    context = multiprocessing.get_context("fork")
    first_started, second_started, release = context.Event(), context.Event(), context.Event()

    def execute(kind, payload, progress):
        if payload["approval_id"] == "first":
            first_started.set()
            assert release.wait(5)
        else:
            second_started.set()
        return ["The durable journal prevents another completed digest."]

    monkeypatch.setattr(jobs, "_dispatch", execute)
    first = context.Process(target=jobs.run_worker, args=(first_job["id"],))
    second = context.Process(target=jobs.run_worker, args=(second_job["id"],))
    first.start()
    try:
        assert first_started.wait(5)
        second.start()
        assert not second_started.wait(0.2)
        assert jobs.get_job(second_job["id"])["state"] == jobs.State.QUEUED
    finally:
        release.set()
        first.join(5)
        if second.pid:
            second.join(5)
        for process in (first, second):
            if process.pid and process.is_alive():
                process.kill()
                process.join()
    assert first.exitcode == second.exitcode == 0
    assert second_started.is_set()


@pytest.mark.parametrize("signal_number", [signal.SIGTERM, signal.SIGKILL])
def test_interrupted_worker_resumes_the_same_approval_and_checkpoint(queued, monkeypatch, tmp_path, signal_number):
    job = _enqueue()
    checkpoint = tmp_path / "completed-session"
    context = multiprocessing.get_context("fork")
    started = context.Event()

    def execute(kind, payload, progress):
        assert payload == job["payload"]
        if not checkpoint.exists():
            checkpoint.write_text("First session already completed.")
            started.set()
            context.Event().wait(10)
        return [checkpoint.read_text(), "Remaining approved sessions completed."]

    monkeypatch.setattr(jobs, "_dispatch", execute)
    worker = context.Process(target=jobs.run_worker, args=(job["id"],))
    worker.start()
    try:
        assert started.wait(5)
        os.kill(worker.pid, signal_number)
        worker.join(5)
    finally:
        if worker.is_alive():
            worker.kill()
            worker.join()
    interrupted = jobs.get_job(job["id"])
    assert interrupted["state"] == jobs.State.INTERRUPTED
    assert interrupted["payload"] == job["payload"]
    resumed = jobs.recover_jobs()[0]
    assert resumed["id"] == job["id"]
    assert jobs.run_worker(job["id"]) == 0
    completed = jobs.get_job(job["id"])
    assert completed["attempt"] == 2
    assert completed["report"] == [
        "First session already completed.", "Remaining approved sessions completed.",
    ]


def test_edited_approval_is_rejected_before_dispatch(queued, monkeypatch):
    job = _enqueue()
    record = Path(job["log_path"]).with_name("job.json")
    edited = json.loads(record.read_text())
    edited["payload"]["sources"].append("codex")
    record.write_text(json.dumps(edited))
    monkeypatch.setattr(jobs, "_dispatch", lambda *args: pytest.fail("Changed approval ran"))
    with pytest.raises(jobs.JobError, match="could not be read"):
        jobs.run_worker(job["id"])


def _fake_worker_package(tmp_path, monkeypatch, hook):
    """Use real worker code with a harmless lane and no customer configuration."""
    source = tmp_path / "worker-source"
    for package in ("probe", "probe/cli", "probe/sdk", "probe/_shared"):
        folder = source / package
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "__init__.py").write_text("")
    (source / "probe/cli/import_jobs.py").write_text(Path(jobs.__file__).read_text())
    # Its 3.11-only names come from here (plan 2.11), on every Python.
    (source / "probe/_compat.py").write_text(
        Path(jobs.__file__).parents[1].joinpath("_compat.py").read_text()
    )
    (source / "probe/sdk/durable.py").write_text(
        Path(jobs.__file__).parents[1].joinpath("sdk/durable.py").read_text()
    )
    # durable's file lock and atomic replace (fcntl on POSIX, msvcrt on Windows).
    (source / "probe/_shared/oscompat.py").write_text(
        Path(jobs.__file__).parents[1].joinpath("_shared/oscompat.py").read_text()
    )
    (source / "probe/cli/backfill.py").write_text("def stop_all(): pass\n")
    (source / "probe/cli/backfill_transcripts.py").write_text(textwrap.dedent(hook))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PYTHONPATH", "relative/missing-source")
    monkeypatch.setattr(jobs, "_source_root", lambda: source)
    return source


def _await_job(job_id, predicate):
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        job = jobs.get_job(job_id)
        if predicate(job):
            return job
        time.sleep(0.03)
    raise AssertionError(f"Worker did not reach expected state: {job}")


@pytest.mark.parametrize("fail", [False, True])
def test_real_detached_worker_uses_pinned_source_and_canonical_module(tmp_path, monkeypatch, fail):
    source = _fake_worker_package(tmp_path, monkeypatch, """
        import os
        from pathlib import Path
        from . import import_jobs

        def run_background_job(payload, *, progress):
            if payload['fail']:
                raise import_jobs.JobError('The approved account is unavailable.')
            assert import_jobs._active_job is not None
            progress('Source is pinned', completed=1, total=1)
            return [str(Path(__file__).resolve()), f'detached={os.getsid(0) == os.getpid()}']
    """)
    job = jobs.enqueue("transcripts", {"fail": fail}, "Harmless detached worker")
    finished = _await_job(job["id"], lambda current: current["state"] in {"succeeded", "failed"})
    if fail:
        assert finished["error"] == "The approved account is unavailable."
    else:
        assert finished["state"] == jobs.State.SUCCEEDED
        assert finished["report"] == [str(source / "probe/cli/backfill_transcripts.py"), "detached=True"]


def test_bootstrap_failure_is_not_an_endless_automatic_recovery(tmp_path, monkeypatch):
    source = _fake_worker_package(tmp_path, monkeypatch, "")
    (source / "probe/cli/import_jobs.py").write_text("raise RuntimeError('Broken installation')\n")
    job = jobs.enqueue("transcripts", {"approval": "reviewed"}, "Failed bootstrap")
    failed = _await_job(job["id"], lambda current: current["state"] == jobs.State.FAILED)
    assert failed["attempt"] == 0
    assert "could not start" in failed["error"]
    assert jobs.recover_jobs()[0]["state"] == jobs.State.FAILED


def test_recovery_reclaims_a_real_orphan_agent_before_next_attempt(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import subprocess
        import sys
        from pathlib import Path
        from . import import_jobs

        def run_background_job(payload, *, progress):
            checkpoint = Path(payload['checkpoint'])
            if checkpoint.exists():
                return ['Resumed after the previously approved checkpoint.']
            child = import_jobs.spawn_child(
                [sys.executable, '-c', 'import time; time.sleep(30)'],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, start_new_session=True,
            )
            checkpoint.write_text(str(child.pid))
            progress('Agent registered', completed=1, total=2)
            child.wait()
            import_jobs.unregister_child(child.pid)
            return ['Completed.']
    """)
    job = jobs.enqueue("transcripts", {"checkpoint": str(tmp_path / "checkpoint")}, "Orphan recovery")
    active = _await_job(job["id"], lambda current: current["progress"]["message"] == "Agent registered")
    child = active["children"][0]
    try:
        assert child["pid"] == child["pgid"] and jobs._alive(child["pid"], child["identity"])
        os.kill(active["pid"], signal.SIGKILL)
        _await_job(job["id"], lambda current: current["state"] == jobs.State.INTERRUPTED)
        jobs.resume(job["id"])
        finished = _await_job(job["id"], lambda current: current["state"] == jobs.State.SUCCEEDED)
        assert finished["attempt"] == 2
        assert not jobs._alive(child["pid"], child["identity"])
        assert finished["children"] == []
        assert finished["report"] == ["Resumed after the previously approved checkpoint."]
    finally:
        if jobs._alive(active["pid"], active["pid_identity"]):
            os.kill(active["pid"], signal.SIGKILL)
        jobs._reclaim_children(Path(job["log_path"]).parent)


def test_worker_death_before_registration_closes_gate_before_agent_executes(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import subprocess
        import sys
        import time
        from pathlib import Path
        from . import import_jobs

        def run_background_job(payload, *, progress):
            def pause_before_registration(pid):
                Path(payload['started']).write_text(str(pid))
                time.sleep(30)

            import_jobs.register_child = pause_before_registration
            import_jobs.spawn_child(
                [sys.executable, '-c', 'from pathlib import Path; '
                 + 'Path(' + repr(payload['must_not_run']) + ').write_text("started")'],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, start_new_session=True,
            )
            return []
    """)
    started, forbidden = tmp_path / "started", tmp_path / "must-not-run"
    job = jobs.enqueue(
        "transcripts", {"started": str(started), "must_not_run": str(forbidden)}, "Launch gate",
    )
    active = _await_job(job["id"], lambda current: current["state"] == jobs.State.RUNNING and started.exists())
    pid = int(started.read_text())
    identity = jobs._process_identity(pid)
    try:
        os.kill(active["pid"], signal.SIGKILL)
        deadline = time.monotonic() + 5
        while jobs._alive(pid, identity) and time.monotonic() < deadline:
            time.sleep(0.03)
        assert not jobs._alive(pid, identity)
        assert not forbidden.exists()
    finally:
        if jobs._alive(active["pid"], active["pid_identity"]):
            os.kill(active["pid"], signal.SIGKILL)
        if jobs._alive(pid, identity):
            os.killpg(pid, signal.SIGKILL)


def test_reclaim_never_signals_a_reused_process_id(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job["log_path"]).parent
    jobs._update(folder, children=[{"pid": os.getpid(), "pgid": os.getpid(), "identity": "old-start"}])
    monkeypatch.setattr(jobs.os, "killpg", lambda *args: pytest.fail("Reused process group was signaled"))
    jobs._reclaim_children(folder)
    assert jobs.get_job(job["id"])["children"] == []


@pytest.mark.parametrize("corruption", ["invalid-json", "changed-approval", "missing-status-field"])
def test_one_unreadable_record_does_not_hide_or_restart_other_jobs(queued, corruption):
    broken, healthy = _enqueue("broken"), _enqueue("healthy")
    record = Path(broken["log_path"]).with_name("job.json")
    if corruption == "invalid-json":
        record.write_text("{unfinished")
    else:
        value = json.loads(record.read_text())
        if corruption == "changed-approval":
            value["payload"]["sources"].append("codex")
        else:
            del value["created_at"]
        record.write_text(json.dumps(value))
    unchanged = record.read_bytes()
    rows = {job["id"]: job for job in jobs.recover_jobs()}
    assert rows[healthy["id"]]["state"] == jobs.State.QUEUED
    diagnostic = rows[broken["id"]]
    assert diagnostic["state"] == jobs.State.FAILED
    assert diagnostic["label"] == "Unreadable saved import"
    assert diagnostic["readable"] is False and diagnostic["retryable"] is False
    assert len(queued) == 2
    assert record.read_bytes() == unchanged
    with pytest.raises(jobs.JobError):
        jobs.resume(broken["id"])
    assert len(queued) == 2


def test_clear_stops_active_queued_and_agent_workers_before_removing_only_local_jobs(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import sys, time
        from . import import_jobs

        def run_background_job(payload, *, progress):
            if payload.get('complete'):
                return ['Completed research stays on the server.']
            import_jobs.spawn_child([sys.executable, '-c', 'import time; time.sleep(60)'])
            while True:
                progress('Reading source', completed=1, total=3)
                time.sleep(.02)
    """)
    completed = jobs.enqueue('transcripts', {'complete': True}, 'Finished')
    _await_job(completed['id'], lambda job: job['state'] == jobs.State.SUCCEEDED)
    active = jobs.enqueue('transcripts', {'number': 1}, 'Running')
    saved = _await_job(active['id'], lambda job: bool(job.get('children')))
    queued_job = jobs.enqueue('transcripts', {'number': 2}, 'Queued')
    queued_saved = _await_job(queued_job['id'], lambda job: job['state'] == jobs.State.QUEUED
                              and job['attempt'] == 1)
    workers = [(saved['pid'], saved['pid_identity']),
               (queued_saved['pid'], queued_saved['pid_identity']),
               (saved['children'][0]['pid'], saved['children'][0]['identity'])]
    source = tmp_path / 'original-transcript.jsonl'
    source.write_text('original source')
    receipts = jobs.default_dir().parent / 'transcript-receipts.json'
    receipts.write_text('acknowledged delivery stays idempotent')
    try:
        assert jobs.clear_all() == 3
        assert all(not jobs._alive(pid, identity) for pid, identity in workers)
        assert jobs.list_jobs() == jobs.recover_jobs() == []
        assert not any(jobs._ID.fullmatch(path.name) for path in jobs.default_dir().iterdir())
        time.sleep(.1)  # Let late reapers observe the terminated subprocesses.
        assert jobs.list_jobs() == []
        assert source.read_text() == 'original source'
        assert receipts.read_text() == 'acknowledged delivery stays idempotent'
        assert jobs.clear_all() == 0
    finally:
        for pid, identity in workers:
            if jobs._alive(pid, identity):
                os.kill(pid, signal.SIGKILL)


def test_cleared_job_cannot_be_recreated_by_late_progress_read_or_resume(queued):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=None, launch_pid=None)
    assert jobs.clear_all() == 1
    with pytest.raises((jobs.JobError, FileNotFoundError)):
        jobs.get_job(job['id'])
    with pytest.raises((jobs.JobError, FileNotFoundError)):
        jobs.resume(job['id'])
    with pytest.raises((jobs.JobError, FileNotFoundError)):
        jobs._update(folder, progress={'completed': 2})
    assert not folder.exists()
    assert jobs.recover_jobs() == []
    assert _enqueue()['id'] == job['id']
    assert len(queued) == 2


def test_clear_does_not_signal_reused_pid_or_follow_symlinks(queued, tmp_path, monkeypatch):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=os.getpid(), pid_identity='previous-boot', launch_identity='previous-boot')
    source = tmp_path / 'research-files'
    source.mkdir()
    (source / 'keep.txt').write_text('keep')
    (folder.parent / ('e' * 32)).symlink_to(source, target_is_directory=True)
    signals = []
    kill = os.kill
    monkeypatch.setattr(jobs.os, 'kill', lambda pid, number: signals.append((pid, number)) or kill(pid, number))
    assert jobs.clear_all() == 1
    assert not any(number for _, number in signals)
    assert (source / 'keep.txt').read_text() == 'keep'


def test_clear_force_stops_a_worker_that_ignores_termination(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import signal, time

        def run_background_job(payload, *, progress):
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            progress('Ignoring termination', completed=1, total=2)
            while True:
                time.sleep(.1)
    """)
    job = jobs.enqueue('transcripts', {'test': 'stubborn'}, 'Stubborn worker')
    active = _await_job(job['id'], lambda current: current['progress']['message'] == 'Ignoring termination')
    try:
        assert jobs.clear_all() == 1
        assert not jobs._alive(active['pid'], active['pid_identity'])
        assert jobs.list_jobs() == []
    finally:
        if jobs._alive(active['pid'], active['pid_identity']):
            os.kill(active['pid'], signal.SIGKILL)


def test_clear_waits_for_process_shutdown_after_worker_lock_is_released(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import atexit, time
        from pathlib import Path

        def run_background_job(payload, *, progress):
            def shutdown():
                # run_worker has returned and released worker.lock, but the
                # interpreter still has process-exit work to finish.
                time.sleep(1)
                Path(payload['shutdown']).write_text('finished')

            atexit.register(shutdown)
            progress('Worker waiting')
            while True:
                time.sleep(.02)
    """)
    shutdown = tmp_path / 'shutdown-complete'
    job = jobs.enqueue('transcripts', {'shutdown': str(shutdown)}, 'Delayed process shutdown')
    active = _await_job(job['id'], lambda current: current['progress']['message'] == 'Worker waiting')
    try:
        assert jobs.clear_all() == 1
        assert shutdown.read_text() == 'finished'
        assert not jobs._alive(active['pid'], active['pid_identity'])
        assert not Path(job['log_path']).parent.exists()
        assert jobs.list_jobs() == []
    finally:
        if jobs._alive(active['pid'], active['pid_identity']):
            os.kill(active['pid'], signal.SIGKILL)


def test_cancel_preserves_progress_and_approval_until_explicit_resume_or_reimport(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    progress = {'completed': 1, 'total': 3, 'completion_ids': [['codex', 'already-saved']]}
    jobs._update(folder, pid=None, launch_pid=None, progress=progress, report=['Saved receipt'])
    canceled = jobs.cancel(job['id'])
    assert canceled['state'] == jobs.State.CANCELED
    assert canceled['payload'] == job['payload']
    assert canceled['report'] == ['Saved receipt']
    assert all(canceled['progress'][key] == value for key, value in progress.items())
    assert 'uploads already submitted may finish' in canceled['progress']['message']
    assert Path(job['log_path']).exists()
    assert jobs.cancel(job['id']) == canceled
    assert jobs.recover_jobs()[0] == canceled
    monkeypatch.setattr(jobs, '_dispatch', lambda *args: pytest.fail('Canceled work was restarted'))
    assert jobs.run_worker(job['id']) == 0
    assert len(queued) == 1

    resumed = jobs.resume(job['id'])
    assert resumed['state'] == jobs.State.QUEUED
    assert resumed['payload'] == canceled['payload']
    assert not resumed['cancel_requested']
    assert resumed['progress']['completed'] == 1
    assert len(queued) == 2
    jobs._update(folder, pid=None, launch_pid=None)
    jobs.cancel(job['id'])
    assert _enqueue()['state'] == jobs.State.QUEUED
    assert len(queued) == 3


def test_cancel_completed_job_is_unchanged_and_missing_job_is_an_error(queued, monkeypatch):
    job = _enqueue()
    monkeypatch.setattr(jobs, '_dispatch', lambda *args: ['All uploaded work remains in Probe.'])
    assert jobs.run_worker(job['id']) == 0
    completed = jobs.get_job(job['id'])
    assert jobs.cancel(job['id']) == completed
    with pytest.raises(jobs.JobError, match='not found'):
        jobs.cancel('a' * 32)
    with pytest.raises(jobs.JobError, match='Invalid'):
        jobs.cancel('../source')


def test_recovery_finishes_cancel_intent_after_canceller_crash_without_restarting(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=None, launch_pid=None, state=jobs.State.INTERRUPTED,
                 progress={'completed': 2, 'total': 5})

    def interrupted_cancel(folder):
        raise jobs.JobError('Stopping process failed')

    with monkeypatch.context() as context:
        context.setattr(jobs, '_signal_worker', interrupted_cancel)
        with pytest.raises(jobs.JobError, match='Stopping process failed'):
            jobs.cancel(job['id'])
    pending = jobs.get_job(job['id'])
    assert pending['cancel_requested']
    assert pending['state'] != jobs.State.CANCELED
    assert jobs.run_worker(job['id']) == 0
    assert jobs.recover_jobs()[0]['state'] == jobs.State.CANCELED
    assert jobs.get_job(job['id'])['progress']['completed'] == 2
    assert len(queued) == 1


def test_recovery_does_not_resume_cancellation_completed_after_its_status_read(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=None, launch_pid=None, state=jobs.State.INTERRUPTED)
    stale = jobs.get_job(job['id'])
    canceled = jobs.cancel(job['id'])
    original_get = jobs.get_job
    first = True

    def stale_status(*args, **kwargs):
        nonlocal first
        if first:
            first = False
            return stale
        return original_get(*args, **kwargs)

    monkeypatch.setattr(jobs, 'get_job', stale_status)
    assert jobs.recover_jobs() == [canceled]
    assert len(queued) == 1


def test_cancel_intent_wins_over_late_worker_completion_without_losing_counts(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=None, launch_pid=None)

    def finish_during_cancel(folder):
        late = jobs._update(folder, state=jobs.State.SUCCEEDED, finished_at=jobs.now_iso(),
                            progress={'completed': 2, 'total': 3}, report=['Receipt committed'])
        assert late['state'] != jobs.State.SUCCEEDED
        assert late['cancel_requested']

    monkeypatch.setattr(jobs, '_signal_worker', finish_during_cancel)
    canceled = jobs.cancel(job['id'])
    assert canceled['state'] == jobs.State.CANCELED
    assert canceled['progress']['completed'] == 2
    assert canceled['report'] == ['Receipt committed']


def test_cancel_does_not_signal_reused_pid_or_stop_other_jobs(queued, monkeypatch, tmp_path):
    directory = tmp_path / 'custom-jobs'
    job = jobs.enqueue('folder', {'approval': 'selected'}, 'Selected', directory=directory)
    other = jobs.enqueue('folder', {'approval': 'other'}, 'Other', directory=directory)
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=os.getpid(), pid_identity='previous-boot', launch_identity='previous-boot')
    signals = []
    kill = os.kill
    monkeypatch.setattr(jobs.os, 'kill', lambda pid, number: signals.append((pid, number)) or kill(pid, number))
    assert jobs.cancel(job['id'], directory=directory)['state'] == jobs.State.CANCELED
    assert not any(number for _, number in signals)
    assert jobs.get_job(other['id'], directory=directory) == other


def test_cancel_keeps_intent_and_refuses_terminal_state_while_worker_lock_is_owned(queued, monkeypatch):
    job = _enqueue()
    folder = Path(job['log_path']).parent
    jobs._update(folder, pid=None, launch_pid=None)
    ticks = iter(range(0, 100, 10))
    with jobs._try_lock(folder / 'worker.lock') as acquired:
        assert acquired
        with monkeypatch.context() as context:
            context.setattr(jobs.time, 'monotonic', lambda: next(ticks))
            with pytest.raises(jobs.JobError, match='still stopping'):
                jobs.cancel(job['id'])
        saved = jobs.get_job(job['id'])
        assert saved['state'] != jobs.State.CANCELED
        assert saved['cancel_requested']
    assert jobs.recover_jobs()[0]['state'] == jobs.State.CANCELED
    assert len(queued) == 1


def test_cancel_queued_worker_then_active_worker_preserves_other_job_and_receipts(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import sys, time
        from . import import_jobs

        def run_background_job(payload, *, progress):
            import_jobs.spawn_child([sys.executable, '-c', 'import time; time.sleep(60)'])
            while True:
                progress('Reading source', completed=1, total=3)
                time.sleep(.02)
    """)
    active = jobs.enqueue('transcripts', {'number': 1}, 'Running')
    saved = _await_job(active['id'], lambda job: bool(job.get('children'))
                       and job['progress'].get('completed') == 1)
    queued_job = jobs.enqueue('transcripts', {'number': 2}, 'Queued')
    queued_saved = _await_job(queued_job['id'], lambda job: job['state'] == jobs.State.QUEUED
                              and job['attempt'] == 1)
    workers = [(saved['pid'], saved['pid_identity']),
               (queued_saved['pid'], queued_saved['pid_identity']),
               (saved['children'][0]['pid'], saved['children'][0]['identity'])]
    source = tmp_path / 'original-transcript.jsonl'
    source.write_text('original source')
    receipts = jobs.default_dir().parent / 'transcript-receipts.json'
    receipts.write_text('acknowledged delivery stays idempotent')
    try:
        assert jobs.cancel(queued_job['id'])['state'] == jobs.State.CANCELED
        assert not jobs._alive(*workers[1])
        assert jobs._alive(*workers[0]) and jobs._alive(*workers[2])
        assert jobs.get_job(active['id'])['state'] == jobs.State.RUNNING
        assert next(job for job in jobs.recover_jobs() if job['id'] == queued_job['id'])['state'] == jobs.State.CANCELED
        canceled = jobs.cancel(active['id'])
        assert canceled['state'] == jobs.State.CANCELED
        assert canceled['progress']['completed'] == 1
        assert all(not jobs._alive(pid, identity) for pid, identity in workers)
        assert len(jobs.recover_jobs()) == 2
        assert all(job['state'] == jobs.State.CANCELED for job in jobs.list_jobs())
        assert source.read_text() == 'original source'
        assert receipts.read_text() == 'acknowledged delivery stays idempotent'
    finally:
        for pid, identity in workers:
            if jobs._alive(pid, identity):
                os.kill(pid, signal.SIGKILL)


def test_cancel_connection_retry_stops_replay_and_keeps_observed_progress(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        from . import import_jobs

        def run_background_job(payload, *, progress):
            progress('Uploaded session', completed=1, total=4)
            raise import_jobs.RetryableJobError('Connection unavailable')
    """)
    job = jobs.enqueue('transcripts', {'test': 'retry'}, 'Retrying')
    active = _await_job(job['id'], lambda job: job['progress'].get('waiting_for_connection'))
    try:
        canceled = jobs.cancel(job['id'])
        assert canceled['state'] == jobs.State.CANCELED
        assert canceled['progress']['completed'] == 1
        assert 'waiting_for_connection' not in canceled['progress']
        assert not jobs._alive(active['pid'], active['pid_identity'])
        assert jobs.recover_jobs() == [canceled]
    finally:
        if jobs._alive(active['pid'], active['pid_identity']):
            os.kill(active['pid'], signal.SIGKILL)


def test_cancel_folder_stops_its_agent_and_leaves_session_worker_running(tmp_path, monkeypatch):
    source = _fake_worker_package(tmp_path, monkeypatch, """
        import sys, time
        from . import import_jobs

        def run_background_job(payload, *, progress):
            import_jobs.spawn_child([sys.executable, '-c', 'import time; time.sleep(60)'])
            while True:
                progress('Uploading saved work', completed=1, total=3)
                time.sleep(.02)
    """)
    (source / 'probe/cli/backfill_import.py').write_text(
        (source / 'probe/cli/backfill_transcripts.py').read_text())
    (source / 'probe/cli/backfill_coverage.py').write_text('class CoverageError(Exception): pass\n')
    sessions = jobs.enqueue('transcripts', {'number': 1}, 'Sessions')
    folder = jobs.enqueue('folder', {'number': 2}, 'Folder')
    running = [_await_job(job['id'], lambda row: bool(row['children'])
                          and row['progress'].get('completed') == 1) for job in (sessions, folder)]
    owned = [(row['pid'], row['pid_identity']) for row in running]
    agents = [(row['children'][0]['pid'], row['children'][0]['identity']) for row in running]
    try:
        canceled = jobs.cancel(folder['id'])
        assert canceled['state'] == jobs.State.CANCELED
        assert canceled['progress']['completed'] == 1
        assert not jobs._alive(*owned[1]) and not jobs._alive(*agents[1])
        assert jobs._alive(*owned[0]) and jobs._alive(*agents[0])
        assert jobs.get_job(sessions['id'])['state'] == jobs.State.RUNNING
    finally:
        jobs.cancel(sessions['id'])
        for pid, identity in [*owned, *agents]:
            if jobs._alive(pid, identity):
                os.kill(pid, signal.SIGKILL)


def test_cancel_retains_launch_ownership_when_worker_fails_before_parent_records_pid(tmp_path, monkeypatch):
    _fake_worker_package(tmp_path, monkeypatch, """
        import atexit, time
        from pathlib import Path
        from . import import_jobs

        def run_background_job(payload, *, progress):
            def shutdown():
                Path(payload['shutdown']).write_text('shutdown started')
                while True:
                    time.sleep(.02)

            atexit.register(shutdown)
            progress('Receipt saved', completed=1, total=3)
            raise import_jobs.JobError('The next file could not be read.')
    """)
    shutdown = tmp_path / 'shutdown-started'
    original_popen = jobs.subprocess.Popen
    children = []

    def fast_worker(*args, **kwargs):
        child = original_popen(*args, **kwargs)
        children.append(child)
        deadline = time.monotonic() + 8
        while not shutdown.exists():
            if time.monotonic() >= deadline:
                child.kill()
                child.wait()
                pytest.fail('Worker did not finish before parent publication')
            time.sleep(.02)
        return child

    monkeypatch.setattr(jobs.subprocess, 'Popen', fast_worker)
    job = jobs.enqueue('transcripts', {'shutdown': str(shutdown)}, 'Fast failure')
    try:
        assert job['state'] == jobs.State.FAILED
        assert job['pid'] is None
        assert job['progress']['completed'] == 1
        assert job['error'] == 'The next file could not be read.'
        assert job['launch_pid'] == children[0].pid
        assert jobs._alive(job['launch_pid'], job['launch_identity'])
        with jobs._try_lock(Path(job['log_path']).parent / 'worker.lock') as released:
            assert released  # The interpreter is still alive after worker cleanup.
        assert jobs.cancel(job['id'])['state'] == jobs.State.CANCELED
        assert not jobs._alive(job['launch_pid'], job['launch_identity'])
    finally:
        for child in children:
            if child.poll() is None:
                child.kill()
                child.wait()


@pytest.mark.parametrize('ignore_termination', [False, True])
def test_cancel_waits_for_process_exit_and_force_stops_uncooperative_worker(tmp_path, monkeypatch, ignore_termination):
    _fake_worker_package(tmp_path, monkeypatch, """
        import atexit, json, signal, time
        from pathlib import Path
        from . import import_jobs

        def run_background_job(payload, *, progress):
            def shutdown():
                # Keep the interpreter alive after worker.lock was released.
                time.sleep(.4)
                job = import_jobs._read(Path.cwd())
                Path(payload['shutdown']).write_text(json.dumps(job))

            atexit.register(shutdown)
            if payload['ignore']:
                signal.signal(signal.SIGTERM, signal.SIG_IGN)
            progress('Ready', completed=1, total=2)
            while True:
                time.sleep(.02)
    """)
    shutdown = tmp_path / 'shutdown-state.json'
    job = jobs.enqueue('transcripts', {'ignore': ignore_termination, 'shutdown': str(shutdown)}, 'Delayed exit')
    active = _await_job(job['id'], lambda job: job['progress']['message'] == 'Ready')
    try:
        canceled = jobs.cancel(job['id'])
        assert canceled['state'] == jobs.State.CANCELED
        assert not jobs._alive(active['pid'], active['pid_identity'])
        if not ignore_termination:
            during_shutdown = json.loads(shutdown.read_text())
            assert during_shutdown['state'] != jobs.State.CANCELED
            assert during_shutdown['cancel_requested']
        assert Path(job['log_path']).exists()
    finally:
        if jobs._alive(active['pid'], active['pid_identity']):
            os.kill(active['pid'], signal.SIGKILL)
