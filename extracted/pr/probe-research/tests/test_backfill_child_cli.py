"""A second installed CLI must not defeat backfill's attribution contract."""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

import probe
from probe.cli import backfill as bf


@pytest.fixture
def isolated_launcher(monkeypatch):
    previous = bf._BACKFILL_CLI_BIN
    monkeypatch.setattr(bf, "_BACKFILL_CLI_BIN", None)
    yield
    if bf._BACKFILL_CLI_BIN is not None:
        bf._BACKFILL_CLI_BIN.cleanup()
    bf._BACKFILL_CLI_BIN = previous


@pytest.mark.parametrize("agent", [bf.Agent.CLAUDE, bf.Agent.CODEX, bf.Agent.PI])
def test_agent_shell_uses_current_cli_despite_older_path(tmp_path, monkeypatch, isolated_launcher, agent):
    stale = tmp_path / "old bin"
    stale.mkdir()
    marker = tmp_path / "wrong-cli-called"
    old_cli = stale / "probe"
    old_cli.write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 91\n")
    old_cli.chmod(0o700)
    monkeypatch.setenv("PATH", str(stale) + os.pathsep + os.environ["PATH"])
    monkeypatch.setenv("PROBE_AUTO_LOGIN", "0")
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("PROBE_VERSION_CACHE", str(tmp_path / "version.json"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(tmp_path / "device.json"))
    monkeypatch.setenv("PROBE_ATTRIBUTION", "ambient")
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "643ce138-4801-4409-b69c-ca30ab7605bc")
    monkeypatch.setenv("CLAUDE_CODE_VERSION", "2.1.219")
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append((self.path, dict(self.headers)))
            body = b'{"customer_id":"fixture"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setenv("PROBE_BASE_URL", f"http://127.0.0.1:{server.server_port}")
    monkeypatch.setenv("PROBE_TOKEN", "local-fixture-token")
    inherited_path = os.environ["PATH"]
    fake_agent = tmp_path / "fake_agent.py"
    fake_agent.write_text(
        "import json, os, subprocess, sys\n"
        "sys.stdin.read()\n"
        "p = subprocess.run(['/bin/bash', '-c', 'probe --version'], capture_output=True, text=True)\n"
        "q = subprocess.run(['/bin/bash', '-c', 'probe whoami'], capture_output=True, text=True)\n"
        "print(json.dumps({'type': 'result', 'result': json.dumps({"
        "'returncode': p.returncode, 'version': p.stdout.strip(), "
        "'whoami_returncode': q.returncode, 'principal': q.stdout.strip(), "
        "'attribution': os.environ.get('PROBE_ATTRIBUTION')})}), flush=True)\n"
    )
    monkeypatch.setattr(bf, "which_agent", lambda _: sys.executable)
    monkeypatch.setattr(bf, "agent_argv", lambda *a, **kw: [sys.executable, str(fake_agent)])
    try:
        ok, tail = bf.launch_agent(
            tmp_path, "Read the supplied source", agent=agent, workdir=tmp_path,
            progress=False, stream=io.StringIO(), timeout=10,
        )
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()
    assert ok, tail
    assert f"probe {probe.__version__}" in tail
    assert '"returncode": 0' in tail.replace('\\"', '"')
    assert '"whoami_returncode": 0' in tail.replace('\\"', '"')
    assert '"attribution": "backfill"' in tail.replace('\\"', '"')
    assert not marker.exists()
    assert os.environ["PATH"] == inherited_path
    assert os.environ["PROBE_ATTRIBUTION"] == "ambient"
    assert len(requests) == 1 and requests[0][0] == "/v1/me"
    headers = {key.lower(): value for key, value in requests[0][1].items()}
    assert "x-probe-agent" not in headers
    assert "x-probe-agent-session" not in headers


def test_launcher_quotes_interpreter_and_pins_package_and_attribution(tmp_path, monkeypatch, isolated_launcher):
    # The selected package has no console script. A different package on
    # PYTHONPATH and the ambient attribution must not replace that selection.
    interpreter = tmp_path / "python ' with $() spaces"
    interpreter.symlink_to(sys.executable)
    monkeypatch.setattr(bf.sys, "executable", str(interpreter))
    selected = tmp_path / "selected ' package"
    package = selected / "probe"
    (package / "cli").mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "cli/__init__.py").write_text(
        "import json, os, sys\n"
        "def main():\n"
        " print(json.dumps({'package': __file__, 'args': sys.argv[1:], "
        "'attribution': os.environ['PROBE_ATTRIBUTION']}))\n"
        " return 0\n"
    )
    monkeypatch.setattr(bf, "__file__", str(package / "cli/backfill.py"))
    shadow = tmp_path / "shadow"
    (shadow / "probe").mkdir(parents=True)
    (shadow / "probe/__init__.py").write_text("raise RuntimeError('wrong package')\n")
    env = bf._backfill_agent_env()
    env.update(PYTHONPATH=str(shadow), PROBE_ATTRIBUTION="ambient")
    result = subprocess.run(
        ["probe", "a quoted ' value", "$(not-a-command)", ""],
        env=env, cwd=shadow, capture_output=True, text=True, timeout=10, check=True,
    )
    row = json.loads(result.stdout)
    assert row == {
        "package": str(package / "cli/__init__.py"),
        "args": ["a quoted ' value", "$(not-a-command)", ""],
        "attribution": "backfill",
    }


def test_concurrent_units_share_a_live_private_launcher(isolated_launcher):
    with ThreadPoolExecutor(max_workers=4) as pool:
        directories = list(pool.map(lambda _: bf._backfill_cli_bin(), range(12)))
    assert len({id(directory) for directory in directories}) == 1
    launcher = Path(directories[0].name) / "probe"
    assert launcher.is_file() and os.access(launcher, os.X_OK)
    assert launcher.parent.stat().st_mode & 0o777 == 0o700
