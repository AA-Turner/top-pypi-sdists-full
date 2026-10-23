"""The tap's hooks with the Probe service recording the session (plan A2), end to end.

A real service, the real tap plugin and its real hook scripts: SessionStart
asks the service to record the session (no wrapper, no `tap watch`, the
`.hosted` marker names the service), each prompt's check reads that marker
and starts nothing, `probe status` reads the session as captured, and
SessionEnd finishes the recorder and clears the marker.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from probe.service.protocol import Method
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the hooks are POSIX shell")

TAP = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
HOOKS = TAP / "hooks"


def _hook(name: str, payload: dict, env: dict, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(HOOKS / name), *args], input=json.dumps(payload), text=True, capture_output=True,
        env=env, timeout=30, check=False,
    )


def test_a_hosted_session_from_start_to_end(service_home, tmp_path, monkeypatch):
    agent, owner = spawn_agent()
    sid = f"00000000-0000-4000-8000-{os.getpid():012d}"
    marker = Path(f"/tmp/probe-research-tap-watcher-{sid}.hosted")
    pid_file = Path(f"/tmp/probe-research-tap-watcher-{sid}.pid")
    try:
        plugin_dir = tmp_path / "state"
        (plugin_dir / "logs").mkdir(parents=True)
        config = tmp_path / "probe-config.json"
        config.write_text(json.dumps({"version": 2, "current_context": "default", "contexts": {
            "default": {"base_url": "http://127.0.0.1:1", "ingest_token": "ros_ing_faketoken"}}}))
        transcript = tmp_path / "t.jsonl"
        transcript.write_text(json.dumps({"type": "user", "sessionId": sid, "message": {"content": "hi"}}) + "\n")
        env = {
            **os.environ, "PROBE_TAP_HOSTED": "1", "PROBE_SERVICE_OWNER_PID": str(agent.pid),
            "PROBE_RESEARCH_TAP_PLUGIN_DIR": str(plugin_dir), "PROBE_CONFIG_PATH": str(config),
            "CLAUDE_PLUGIN_ROOT": str(TAP), "CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS": "6000",
        }
        for name in ("PROBE_RESEARCH_TAP_PLUGIN_DIR", "PROBE_CONFIG_PATH"):
            monkeypatch.setenv(name, env[name])
        status = service_home.start()
        payload = {"session_id": sid, "transcript_path": str(transcript), "cwd": str(tmp_path)}

        started = _hook("session-start.sh", payload, env)
        assert started.returncode == 0, started.stderr
        log = (plugin_dir / "logs" / f"{sid}.log").read_text()
        assert marker.read_text() == str(status["pid"]), log
        assert not pid_file.exists(), "no wrapper for a hosted session"
        assert "the Probe service records this session" in log
        assert wait_for(lambda: [r["sid"] for r in service_home.call(Method.STATUS)["recorders"]] == [sid], 5)
        assert sid in [s["sid"] for s in service_home.call(Method.SESSION_LIST)["sessions"]]

        # Every prompt's check: the marker names a live service, so nothing starts.
        checked = _hook("ensure-daemon.sh", payload, env)
        assert checked.returncode == 0 and not pid_file.exists()
        assert not (plugin_dir / "heal" / sid).exists(), "the fast path, not the cold one"

        # `probe status` and the self-heal read it as captured.
        from probe.cli import capture_state

        state = capture_state.session_capture_state(sid, "claude_code")
        assert state.running is True and state.pid == status["pid"]

        ended = _hook("session-end.sh", {**payload, "reason": "exit"}, env, "--wait")
        assert ended.returncode == 0, ended.stderr
        assert not marker.exists()
        assert wait_for(lambda: service_home.call(Method.STATUS)["recorders"] == [], 10), service_home.log()
    finally:
        kill_agent(agent)
        for suffix in (".hosted", ".pid", ".shutdown", ".owner", ".stopping", ".version"):
            Path(f"/tmp/probe-research-tap-watcher-{sid}{suffix}").unlink(missing_ok=True)


def test_switched_off_the_hooks_start_tap_watch_as_before(service_home, tmp_path):
    """PROBE_TAP_HOSTED=0 (the way back): the wrapper and its pid file, no marker."""
    agent, _owner = spawn_agent()
    sid = f"00000000-0000-4000-8001-{os.getpid():012d}"
    pid_file = Path(f"/tmp/probe-research-tap-watcher-{sid}.pid")
    try:
        plugin_dir = tmp_path / "state"
        (plugin_dir / "logs").mkdir(parents=True)
        (plugin_dir / ".token").write_text("ros_ing_faketoken")
        transcript = tmp_path / "t.jsonl"
        transcript.write_text("{}\n")
        env = {**os.environ, "PROBE_TAP_HOSTED": "0", "PROBE_SERVICE_OWNER_PID": str(agent.pid),
               "PROBE_RESEARCH_TAP_PLUGIN_DIR": str(plugin_dir), "CLAUDE_PLUGIN_ROOT": str(TAP),
               "PROBE_BASE_URL": "http://127.0.0.1:1"}
        service_home.start()
        payload = {"session_id": sid, "transcript_path": str(transcript), "cwd": str(tmp_path)}
        assert _hook("session-start.sh", payload, env).returncode == 0
        assert wait_for(lambda: pid_file.is_file() and pid_file.read_text().strip().isdigit(), 5)
        assert not Path(f"/tmp/probe-research-tap-watcher-{sid}.hosted").exists()
        assert service_home.call(Method.STATUS)["recorders"] == []
        _hook("session-end.sh", {**payload, "reason": "exit"}, env)
    finally:
        kill_agent(agent)
        if pid_file.is_file():
            try:
                os.killpg(int(pid_file.read_text().strip()), 15)
            except (OSError, ValueError):
                pass
        for suffix in (".hosted", ".pid", ".shutdown", ".owner", ".stopping", ".version"):
            Path(f"/tmp/probe-research-tap-watcher-{sid}{suffix}").unlink(missing_ok=True)
