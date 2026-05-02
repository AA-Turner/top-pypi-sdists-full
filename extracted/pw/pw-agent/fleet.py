"""Fleet — share live state across pw-agent instances on the same machine
(or, in cloud mode, across all your machines via the broker).

Each pw-agent writes a heartbeat describing what it's doing:
  - hostname + PID + start time
  - cwd + git branch
  - active model + connection mode
  - recently touched files
  - last activity timestamp

Two-tier discovery:
  1. Local file:  ~/.pw-agent/fleet/<machine_id>.json
     Catches siblings on the same filesystem (e.g. multiple terminals).
  2. Broker sync: POST to /api/v1/agents/heartbeat with bearer token.
     Catches siblings on other machines under the same PastaWater
     account. Best-effort — failures fall back to local-only.

Other pw-agents (or the model via the query_fleet tool) can read both
sources to see what siblings are working on across the whole fleet.

Stale heartbeats (>5 min) are filtered out: locally pruned on read,
and the broker side has Redis TTL.
"""

import json
import os
import socket
import time
from typing import Optional

import requests


DEFAULT_FLEET_DIR = os.path.expanduser("~/.pw-agent/fleet")
HEARTBEAT_TTL = 300  # seconds — anything older is considered stale


def _machine_id() -> str:
    """Stable identifier for this pw-agent process."""
    try:
        host = socket.gethostname()
    except Exception:
        host = "unknown"
    return f"{host}-{os.getpid()}"


def _fleet_file(machine_id: str = "") -> str:
    mid = machine_id or _machine_id()
    return os.path.join(DEFAULT_FLEET_DIR, f"{mid}.json")


class FleetHeartbeat:
    """Writes and updates this pw-agent's state for fleet visibility.

    Two storage tiers: local file (always) + broker push (if cloud client).
    """

    def __init__(self, agent):
        self.agent = agent
        self.machine_id = _machine_id()
        self.started_at = time.time()
        self.path = _fleet_file(self.machine_id)
        os.makedirs(DEFAULT_FLEET_DIR, exist_ok=True)
        self.touched_files: list[str] = []  # recent file activity
        self._broker_disabled = False  # Switches on after first failure
        self._write_initial()

    def _git_branch(self) -> str:
        try:
            import subprocess
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.agent.cwd,
                capture_output=True,
                text=True,
                timeout=2,
            )
            return result.stdout.strip() or ""
        except Exception:
            return ""

    def _build_state(self) -> dict:
        client = self.agent.client
        mode = "cloud"
        if client and client.direct_mode:
            mode = "direct"
        return {
            "machine_id": self.machine_id,
            "hostname": self.machine_id.rsplit("-", 1)[0],
            "pid": os.getpid(),
            "started_at": self.started_at,
            "last_active": time.time(),
            "cwd": self.agent.cwd,
            "git_branch": self._git_branch(),
            "model": client.model if client else "unknown",
            "mode": mode,
            "plan_mode": getattr(self.agent, "plan_mode", False),
            "voice_mode": getattr(self.agent, "voice_mode", False),
            "session_turns": sum(1 for m in self.agent.conversation if m.get("role") == "user"),
            "recent_files": self.touched_files[-10:],
        }

    def _write_initial(self):
        state = self._build_state()
        try:
            with open(self.path, "w") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass
        self._push_to_broker(state)

    def update(self):
        """Refresh the heartbeat file (and broker if available). Cheap — call after every turn."""
        state = self._build_state()
        try:
            with open(self.path, "w") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass
        self._push_to_broker(state)

    def _push_to_broker(self, state: dict):
        """Best-effort push to broker for cross-machine discovery.

        Only runs in cloud mode (broker token available). Disables itself
        after the first failure to avoid spamming a down broker.
        """
        if self._broker_disabled:
            return
        client = self.agent.client
        if not client or client.direct_mode or not getattr(client, "token", ""):
            return
        try:
            client.session.post(
                f"{client.api_url}/api/v1/agents/heartbeat",
                json={"machine_id": self.machine_id, "state": state},
                timeout=5,
            )
        except Exception:
            # Don't disable on a single failure — broker might be flaky.
            # But if it keeps failing, the next call will try again with
            # the same low timeout. Acceptable cost.
            pass

    def note_file(self, path: str):
        """Record a file the agent touched (read/wrote)."""
        if path not in self.touched_files:
            self.touched_files.append(path)
            if len(self.touched_files) > 20:
                self.touched_files.pop(0)

    def cleanup(self):
        """Remove our heartbeat file (and broker entry) on exit."""
        try:
            if os.path.exists(self.path):
                os.unlink(self.path)
        except Exception:
            pass
        # Best-effort broker cleanup
        client = self.agent.client
        if client and not client.direct_mode and getattr(client, "token", ""):
            try:
                client.session.delete(
                    f"{client.api_url}/api/v1/agents/heartbeat",
                    params={"machine_id": self.machine_id},
                    timeout=3,
                )
            except Exception:
                pass


def list_fleet(prune_stale: bool = True, client=None) -> list[dict]:
    """Return all live pw-agent heartbeats from local files + broker.

    client: optional LLMClient. If provided and in cloud mode, also fetches
    cross-machine heartbeats from /api/v1/agents/heartbeats and merges them
    with local results (de-duped by machine_id).

    Stale local files (>5 min) are pruned on read. Stale broker entries are
    auto-expired by Redis TTL.
    """
    now = time.time()
    by_machine_id: dict[str, dict] = {}

    # Local file tier
    if os.path.isdir(DEFAULT_FLEET_DIR):
        try:
            entries = os.listdir(DEFAULT_FLEET_DIR)
        except OSError:
            entries = []

        for fname in entries:
            if not fname.endswith(".json"):
                continue
            path = os.path.join(DEFAULT_FLEET_DIR, fname)
            try:
                with open(path, "r") as f:
                    state = json.load(f)
            except Exception:
                continue

            last = state.get("last_active", 0)
            age = now - last
            if age > HEARTBEAT_TTL:
                if prune_stale:
                    try:
                        os.unlink(path)
                    except Exception:
                        pass
                continue

            state["age_seconds"] = int(age)
            state["_source"] = "local"
            mid = state.get("machine_id", fname.removesuffix(".json"))
            by_machine_id[mid] = state

    # Broker tier — fetch cross-machine heartbeats if a cloud client is provided
    if client and not client.direct_mode and getattr(client, "token", ""):
        try:
            resp = client.session.get(
                f"{client.api_url}/api/v1/agents/heartbeats",
                timeout=5,
            )
            if resp.status_code == 200:
                data = resp.json() or {}
                for entry in data.get("agents", []):
                    mid = entry.get("machine_id", "")
                    if not mid:
                        continue
                    # Local file is authoritative if it's the same machine
                    # (it has fresher data — broker is async-pushed)
                    existing = by_machine_id.get(mid)
                    if existing and existing.get("_source") == "local":
                        # Mark that we also see it on the broker
                        existing["_source"] = "local+broker"
                        continue
                    entry["_source"] = "broker"
                    if "age_seconds" not in entry:
                        entry["age_seconds"] = int(now - entry.get("last_active", now))
                    by_machine_id[mid] = entry
        except Exception:
            pass  # Best-effort — fall through to local-only

    results = list(by_machine_id.values())
    results.sort(key=lambda s: s.get("last_active", 0), reverse=True)
    return results


def format_fleet(states: list[dict] = None, exclude_self: bool = False, client=None) -> str:
    """Format the fleet list as readable text for the model or terminal."""
    if states is None:
        states = list_fleet(client=client)

    self_id = _machine_id()
    if exclude_self:
        states = [s for s in states if s.get("machine_id") != self_id]

    if not states:
        return "No other pw-agent instances active right now."

    # Count by source
    local_count = sum(1 for s in states if s.get("_source", "").startswith("local"))
    broker_count = sum(1 for s in states if s.get("_source") == "broker")
    parts = []
    if local_count:
        parts.append(f"{local_count} local")
    if broker_count:
        parts.append(f"{broker_count} remote")
    source_summary = f" ({', '.join(parts)})" if parts else ""

    lines = [f"Fleet: {len(states)} pw-agent instance(s) active{source_summary}"]
    lines.append("")
    for s in states:
        is_self = s.get("machine_id") == self_id
        markers = []
        if is_self:
            markers.append("this session")
        src = s.get("_source", "")
        if src == "broker":
            markers.append("remote")
        marker_str = f" ({', '.join(markers)})" if markers else ""

        lines.append(f"━━━ {s.get('machine_id', '?')}{marker_str}")
        lines.append(f"    cwd: {s.get('cwd', '?')}")
        if s.get("git_branch"):
            lines.append(f"    branch: {s['git_branch']}")
        lines.append(f"    model: {s.get('model', '?')} ({s.get('mode', '?')})")
        modes = []
        if s.get("plan_mode"):
            modes.append("plan")
        if s.get("voice_mode"):
            modes.append("voice")
        if modes:
            lines.append(f"    flags: {', '.join(modes)}")
        lines.append(f"    turns: {s.get('session_turns', 0)}, last active {s.get('age_seconds', 0)}s ago")
        if s.get("recent_files"):
            files = s["recent_files"][-5:]
            lines.append(f"    recent files: {', '.join(files)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def query_fleet(question: str = "", client=None) -> str:
    """Tool entry point: returns a fleet summary for the model.

    Pass an LLMClient as `client` to also pull cross-machine heartbeats
    from the broker. Without it, returns local-only.
    """
    states = list_fleet(client=client)
    return format_fleet(states, client=client)
