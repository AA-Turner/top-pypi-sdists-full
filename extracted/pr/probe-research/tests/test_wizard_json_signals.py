"""`probe wizard --json` and signals: a run a program stops still ends with `done`.

The desktop app cancels a run with SIGINT. That may stop it only while it waits
for a browser approval, when nothing is being written; anywhere else SIGINT is
ignored, by the run and by the child processes it starts, so it can never land
in the middle of a config write or a `claude plugin install`. SIGTERM stops it
anywhere, through its `finally` blocks, so it still writes `done`. Each test is
a real process sent a real signal.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import textwrap
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from probe._shared import oscompat
from probe.cli import wizard_lock
from tests.test_wizard_json_events import _child_env


class _ApprovalNeverComes(BaseHTTPRequestHandler):
    """A Probe server whose browser approval is never given: the device flow
    starts, and every token poll answers `authorization_pending`."""

    def log_message(self, *_args):
        pass

    def _send(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):  # noqa: N802 - http.server's name
        self.rfile.read(int(self.headers.get("Content-Length") or 0))
        if self.path.endswith("/auth/device/code"):
            self._send(201, {
                "device_code": "device-code", "user_code": "WDJB-MJHT",
                "verification_uri": "https://app.test/device",
                "verification_uri_complete": "https://app.test/device?code=WDJB-MJHT",
                "expires_in": 600, "interval": 1,
            })
        elif self.path.endswith("/auth/device/token"):
            self._send(400, {"detail": {"error": "authorization_pending"}})
        else:
            self._send(404, {"detail": "not here"})


def _lock_is_free() -> bool:
    with open(wizard_lock.lock_path(), "a+") as handle:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except BlockingIOError:
            return False
        return True


@pytest.fixture
def signalled_during_approval(tmp_path, monkeypatch, request):
    """`probe wizard --action login --json` sent `request.param` once its
    approval link is out: (events, exit status, lock free when `done` was read)."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ApprovalNeverComes)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    env = {**_child_env(tmp_path), "PROBE_BASE_URL": f"http://127.0.0.1:{server.server_port}"}
    child = subprocess.Popen(
        [sys.executable, "-m", "probe.cli", "wizard", "--action", "login", "--no-browser", "--json"],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, text=True,
    )
    events: list[dict] = []
    free_at_done = None
    # A signal that does not stop the run leaves it polling for ten minutes.
    watchdog = threading.Timer(60, child.kill)
    watchdog.start()
    try:
        for line in child.stdout:
            event = json.loads(line)
            events.append(event)
            if event["event"] == "device_prompt":
                time.sleep(0.3)  # into the poll loop
                child.send_signal(request.param)
            elif event["event"] == "done":
                free_at_done = _lock_is_free()
        child.wait(timeout=60)
    finally:
        watchdog.cancel()
        child.kill()
        server.shutdown()
    return events, child.returncode, free_at_done


@pytest.mark.parametrize("signalled_during_approval", [signal.SIGINT], indirect=True)
def test_sigint_during_the_approval_ends_the_stream_interrupted_result_done(signalled_during_approval):
    events, _, _ = signalled_during_approval
    assert [(e["event"], e.get("code")) for e in events[-3:]] == [
        ("error", "interrupted"), ("result", None), ("done", None),
    ]


@pytest.mark.parametrize("signalled_during_approval", [signal.SIGINT], indirect=True)
def test_sigint_during_the_approval_reads_as_exit_130(signalled_during_approval):
    events, code, _ = signalled_during_approval
    assert (code, events[-1]["ok"], events[-1]["exit_code"]) == (130, False, 130)


@pytest.mark.parametrize("signalled_during_approval", [signal.SIGINT, signal.SIGTERM], indirect=True)
def test_the_lock_is_free_by_the_time_done_is_read(signalled_during_approval):
    _, _, free_at_done = signalled_during_approval
    assert free_at_done is True


@pytest.mark.parametrize("signalled_during_approval", [signal.SIGTERM], indirect=True)
def test_sigterm_still_ends_with_done_and_exit_143(signalled_during_approval):
    events, code, _ = signalled_during_approval
    assert (code, events[-1]["event"], events[-1]["exit_code"]) == (143, "done", 143)


@pytest.mark.parametrize("signalled_during_approval", [signal.SIGTERM], indirect=True)
def test_sigterm_is_reported_as_interrupted(signalled_during_approval):
    events, _, _ = signalled_during_approval
    error = [e for e in events if e["event"] == "error"][-1]
    assert (error["code"], error["message"]) == ("interrupted", "stopped by SIGTERM")


# -- outside the approval, SIGINT changes nothing -------------------------------

#: `--action update` with the update replaced by one that starts a child
#: process (a `claude plugin install`, say), says `ready`, and finishes on `go`.
#: The test sends SIGINT to the whole process group between the two.
CHILD = textwrap.dedent(
    """
    import os, sys, time
    folder = sys.argv[1]
    open(os.path.join(folder, "child-ready"), "w").close()
    deadline = time.monotonic() + 60
    while not os.path.exists(os.path.join(folder, "go")) and time.monotonic() < deadline:
        time.sleep(0.02)
    """
)

SLOW_UPDATE = textwrap.dedent(
    """
    import importlib, os, subprocess, sys, time
    from probe.cli import bootstrap, upgrading
    main = importlib.import_module("probe.cli.main")
    bootstrap.ensure_persistent_install = lambda **_: bootstrap.BootstrapResult(False, True, "")
    folder = sys.argv[1]
    def wait_for(name):
        deadline = time.monotonic() + 60
        while not os.path.exists(os.path.join(folder, name)) and time.monotonic() < deadline:
            time.sleep(0.02)
    def perform_update(**_):
        child = subprocess.Popen([sys.executable, "-c", CHILD, folder])
        wait_for("child-ready")
        open(os.path.join(folder, "ready"), "w").close()
        wait_for("go")
        code = child.wait(timeout=60)
        open(os.path.join(folder, f"child-exit.{code}"), "w").close()
        return upgrading.UpdateOutcome(lines=["Updated."], ok=code == 0, restart_needed=False)
    upgrading.perform_update = perform_update
    raise SystemExit(main.main(sys.argv[2:]))
    """
).replace("CHILD,", f"{CHILD!r},")


@pytest.fixture
def sigint_mid_update(tmp_path):
    folder = tmp_path / "signals"
    folder.mkdir()
    child = subprocess.Popen(
        [sys.executable, "-c", SLOW_UPDATE, str(folder), "wizard", "--action", "update", "--yes",
         "--agent", "claude", "--json"],
        env=_child_env(tmp_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
        text=True, start_new_session=True,
    )
    try:
        deadline = time.monotonic() + 60
        while not (folder / "ready").exists():
            assert child.poll() is None and time.monotonic() < deadline, child.communicate()
            time.sleep(0.02)
        os.killpg(child.pid, signal.SIGINT)  # the run AND its child, as a terminal's Ctrl-C does
        time.sleep(0.3)
        (folder / "go").touch()
        out, err = child.communicate(timeout=60)
    finally:
        child.kill()
    return child.returncode, [json.loads(line) for line in out.splitlines()], folder, err


def test_sigint_outside_the_approval_lets_the_run_finish(sigint_mid_update):
    code, events, _, err = sigint_mid_update
    assert (code, events[-1]["event"], events[-1]["ok"]) == (0, "done", True), err


def test_sigint_outside_the_approval_does_not_reach_a_child_process(sigint_mid_update):
    _, _, folder, _ = sigint_mid_update
    assert [path.name for path in folder.glob("child-exit.*")] == ["child-exit.0"]


# -- what is left in the real stdout's buffer never follows `done` --------------

#: The update writes to `sys.__stdout__` and never flushes it: the interpreter
#: would flush that buffer at exit, after `done`, onto the real stdout.
UNFLUSHED = textwrap.dedent(
    """
    import importlib, sys
    from probe.cli import bootstrap, upgrading
    main = importlib.import_module("probe.cli.main")
    bootstrap.ensure_persistent_install = lambda **_: bootstrap.BootstrapResult(False, True, "")
    def perform_update(**_):
        sys.__stdout__.write("unflushed noise\\n")
        return upgrading.UpdateOutcome(lines=["Updated."], ok=True, restart_needed=False)
    upgrading.perform_update = perform_update
    raise SystemExit(main.main(sys.argv[1:]))
    """
)


@pytest.fixture
def unflushed_run(tmp_path):
    return subprocess.run(
        [sys.executable, "-c", UNFLUSHED, "wizard", "--action", "update", "--yes", "--json"],
        env=_child_env(tmp_path), capture_output=True, text=True, timeout=120,
    )


def test_text_left_in_the_real_stdouts_buffer_goes_to_stderr(unflushed_run):
    assert "unflushed noise" in unflushed_run.stderr, unflushed_run.stdout


def test_done_is_still_the_last_line_of_stdout(unflushed_run):
    assert json.loads(unflushed_run.stdout.splitlines()[-1])["event"] == "done"
