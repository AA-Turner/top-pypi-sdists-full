#!/usr/bin/env python3
"""A scripted stand-in for one long-lived Claude Code session (live-run harness only).

    session_agent.py --config <session.json>

Started by `live_run.py` as `<run>/agents/claude` (a link to the interpreter
named `claude`, so the tap's owner walk, `tap/owner.py`, finds this process as
the session's agent, exactly as it finds Claude Code). It does what Claude Code
does for a session that is left open for hours, minus the model:

  * at start, reads Claude Code's install ledger
    (`$CLAUDE_CONFIG_DIR/plugins/installed_plugins.json`) for each enabled
    plugin, and loads `<installPath>/hooks/hooks.json` ONCE: like Claude Code,
    a session keeps the hooks (and `CLAUDE_PLUGIN_ROOT`) it started with, however
    often the plugins are updated under it;
  * fires each event's hooks the way Claude Code runs them: every matching
    entry's `command` through a shell (`/bin/sh -c`, Git Bash on Windows), in
    parallel, the event's JSON payload on stdin, `CLAUDE_PLUGIN_ROOT` set to that
    plugin's folder, killed at the entry's `timeout` (60 s when it has none);
  * appends realistic transcript lines to `~/.claude/projects/<slug>/<sid>.jsonl`
    every few seconds: a turn is UserPromptSubmit -> user line -> assistant
    text -> tool_use (Bash or Read) -> PreToolUse -> the tool runs -> PostToolUse
    -> tool_result -> assistant text -> Stop. Every few turns the Bash tool runs
    `probe --version` from inside the session (the PATH shim times it);
  * fires PreCompact (`trigger: auto`) on its 2nd turn and every `compact_every`
    turns, and on the next turn after the driver touches `compact_file` (it
    does after each update lands);
  * when `stop_file` appears: finishes its turn (and its first compaction
    turn, at least 2 turns in all), fires SessionEnd, exits.

Records, for the driver's checks:
  hook_log    one JSON line per hook run: event, plugin, version, exit, duration,
              timeout, timed_out, stdout_json_ok, stderr tail
  lines_log   one JSON line per transcript line: n (0-based), kind, marker
  tool_log    one JSON line per Bash tool run
  status_file {"phase", "lines", "turns", "pid", "plugins": [{id, root, version,
              events}]} (atomically replaced): `events`, what each plugin's loaded
              hooks.json declares, is what the driver holds hook coverage to

Each line that can carry text carries a marker `LIVE-RUN-MARK <label> L<n>`, so
the driver can find it in what the stub API received.

Stdlib only.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import json
import os
import random
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path

DEFAULT_HOOK_TIMEOUT_S = 60.0
MODEL = "claude-opus-4-5-20251101"
CLAUDE_VERSION = "2.1.140"


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _append_jsonl(path: Path, record: dict, lock: threading.Lock) -> None:
    with lock:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, separators=(",", ":")) + "\n")


def _atomic_json(path: Path, data: dict) -> None:
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def _matches(matcher, tool: str) -> bool:
    """Claude Code's matcher: empty or `*` is every tool, a plain name or an
    `A|B` list is exact, anything else a regex search."""
    if matcher in (None, "", "*"):
        return True
    if not isinstance(matcher, str):
        return False
    if re.fullmatch(r"[A-Za-z0-9_|]+", matcher):
        return tool in matcher.split("|")
    try:
        return re.search(matcher, tool) is not None
    except re.error:
        return False


class Session:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.label = cfg["label"]
        self.sid = cfg["sid"]
        self.cwd = cfg["cwd"]
        self.transcript = Path(cfg["transcript"])
        self.transcript.parent.mkdir(parents=True, exist_ok=True)
        self.hook_log = Path(cfg["hook_log"])
        self.lines_log = Path(cfg["lines_log"])
        self.tool_log = Path(cfg["tool_log"])
        self.status_file = Path(cfg["status_file"])
        self.stop_file = Path(cfg["stop_file"])
        self.env = dict(cfg["env"])
        if not sys.platform.startswith("linux"):
            # Windows and macOS: this stand-in runs as python (Linux names a
            # shebang script's process after the script, `claude`), which `tap
            # owner` (looking for a `claude` ancestor) cannot name; it names
            # itself, as Claude Code's own process would be found (R2, R3).
            self.env.setdefault("PROBE_SERVICE_OWNER_PID", str(os.getpid()))
        self.shell = cfg.get("shell") or ["/bin/sh", "-c"]
        self.turn_every_s = float(cfg.get("turn_every_s", 20))
        self.line_gap_s = float(cfg.get("line_gap_s", 3))
        self.probe_tool_every = int(cfg.get("probe_tool_every", 4))
        self.compact_every = int(cfg.get("compact_every") or 0)
        #: The workload every session does however soon it is stopped: through
        #: its first compaction turn. A late session the run starts as it ends
        #: (its update landed at the deadline) is stopped before its 2nd turn.
        self.min_turns = 2 if self.compact_every > 0 else 1
        self.compact_file = Path(cfg["compact_file"]) if cfg.get("compact_file") else None
        self.lines = 0
        self.turns = 0
        self.parent_uuid: str | None = None
        self.log_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.rng = random.Random(self.sid)
        self.stopping = False
        self.plugins = self._load_plugins()
        self.phase = "starting"

    # -- plugins and hooks ---------------------------------------------------

    def _load_plugins(self) -> list[dict]:
        config_dir = Path(self.cfg["claude_config_dir"])
        try:
            ledger = json.loads((config_dir / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            ledger = {}
        loaded = []
        for plugin_id in self.cfg["plugins"]:
            entries = (ledger.get("plugins") or {}).get(plugin_id) or []
            if not entries:
                continue
            root = entries[0]["installPath"]
            try:
                hooks = json.loads((Path(root) / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
            except (OSError, ValueError, KeyError):
                hooks = {}
            version = entries[0].get("version")
            events = sorted(
                event for event, groups in hooks.items()
                if any(h.get("type", "command") == "command" and isinstance(h.get("command"), str)
                       for g in groups or [] for h in g.get("hooks") or [])
            )
            loaded.append({"id": plugin_id, "root": root, "version": version, "hooks": hooks, "events": events})
        return loaded

    def _payload(self, event: str, **extra) -> dict:
        payload = {
            "session_id": self.sid,
            "transcript_path": str(self.transcript),
            "cwd": self.cwd,
            "hook_event_name": event,
        }
        if event not in ("SessionStart", "SessionEnd"):
            payload["permission_mode"] = "default"
        payload.update(extra)
        return payload

    def _run_one(self, plugin: dict, event: str, hook: dict, payload: bytes, results: list) -> None:
        timeout = hook.get("timeout")
        timeout_s = float(timeout) if isinstance(timeout, (int, float)) and timeout > 0 else DEFAULT_HOOK_TIMEOUT_S
        env = dict(self.env)
        env["CLAUDE_PLUGIN_ROOT"] = plugin["root"]
        started = time.time()
        record = {
            "t": started,
            "session": self.label,
            "event": event,
            "plugin": plugin["id"],
            "version": plugin["version"],
            "timeout_s": timeout_s,
        }
        try:
            child = subprocess.Popen(
                [*self.shell, hook["command"]],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.cwd,
                env=env,
            )
        except OSError as exc:
            record.update(exit=None, duration_s=0.0, timed_out=False, error=f"spawn: {exc}")
            results.append(record)
            return
        timed_out = False
        try:
            out, err = child.communicate(payload, timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            with contextlib.suppress(OSError):
                child.kill()
            try:
                out, err = child.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                out, err = b"", b"(output pipe still held after the kill)"
                for stream in (child.stdout, child.stderr):
                    with contextlib.suppress(Exception):
                        stream.close()
        duration = time.time() - started
        text = (out or b"").decode("utf-8", "replace").strip()
        json_ok = None
        if text:
            try:
                json.loads(text.splitlines()[-1])
                json_ok = True
            except ValueError:
                json_ok = False
        record.update(
            exit=child.poll(),
            duration_s=round(duration, 3),
            timed_out=timed_out,
            stdout_bytes=len(out or b""),
            stdout_json_ok=json_ok,
            stderr_tail=(err or b"").decode("utf-8", "replace")[-400:],
        )
        results.append(record)

    def fire(self, event: str, tool: str = "", **extra) -> list[dict]:
        payload = json.dumps(self._payload(event, **extra)).encode("utf-8")
        threads, results = [], []
        for plugin in self.plugins:
            for group in plugin["hooks"].get(event) or []:
                if event in ("PreToolUse", "PostToolUse") and not _matches(group.get("matcher"), tool):
                    continue
                for hook in group.get("hooks") or []:
                    if hook.get("type", "command") != "command" or not isinstance(hook.get("command"), str):
                        continue
                    thread = threading.Thread(target=self._run_one, args=(plugin, event, hook, payload, results))
                    thread.start()
                    threads.append(thread)
        for thread in threads:
            thread.join()
        for record in results:
            _append_jsonl(self.hook_log, record, self.log_lock)
        return results

    # -- the transcript ------------------------------------------------------

    def _marker(self) -> str:
        return f"LIVE-RUN-MARK {self.label} L{self.lines:06d}"

    def _base(self, kind: str) -> dict:
        this = str(uuid.uuid4())
        record = {
            "parentUuid": self.parent_uuid,
            "isSidechain": False,
            "userType": "external",
            "cwd": self.cwd,
            "sessionId": self.sid,
            "version": CLAUDE_VERSION,
            "gitBranch": "main",
            "type": kind,
            "uuid": this,
            "timestamp": _now_iso(),
        }
        self.parent_uuid = this
        return record

    def _write(self, record: dict, kind: str, marker: str | None) -> None:
        with self.write_lock:
            line = json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n"
            with self.transcript.open("a", encoding="utf-8") as handle:
                handle.write(line)
                handle.flush()
            _append_jsonl(self.lines_log, {"n": self.lines, "kind": kind, "marker": marker, "t": time.time()},
                          self.log_lock)
            self.lines += 1
        self._status()

    def user_text(self, text: str) -> None:
        marker = self._marker()
        record = self._base("user")
        record["message"] = {"role": "user", "content": f"{text} ({marker})"}
        self._write(record, "user", marker)

    def assistant_text(self, text: str) -> None:
        marker = self._marker()
        record = self._base("assistant")
        record["message"] = {
            "id": f"msg_{uuid.uuid4().hex[:24]}",
            "type": "message",
            "role": "assistant",
            "model": MODEL,
            "content": [{"type": "text", "text": f"{text} ({marker})"}],
            "stop_reason": None,
            "stop_sequence": None,
            "usage": {"input_tokens": 120, "output_tokens": 40, "cache_creation_input_tokens": 0,
                      "cache_read_input_tokens": 2048},
        }
        record["requestId"] = f"req_{uuid.uuid4().hex[:24]}"
        self._write(record, "assistant", marker)

    def tool_use(self, name: str, tool_input: dict, marker: str | None) -> str:
        tool_id = f"toolu_{uuid.uuid4().hex[:24]}"
        record = self._base("assistant")
        record["message"] = {
            "id": f"msg_{uuid.uuid4().hex[:24]}",
            "type": "message",
            "role": "assistant",
            "model": MODEL,
            "content": [{"type": "tool_use", "id": tool_id, "name": name, "input": tool_input}],
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {"input_tokens": 80, "output_tokens": 30, "cache_creation_input_tokens": 0,
                      "cache_read_input_tokens": 2048},
        }
        record["requestId"] = f"req_{uuid.uuid4().hex[:24]}"
        self._write(record, "tool_use", marker)
        return tool_id

    def tool_result(self, tool_id: str, output: str, is_error: bool) -> None:
        record = self._base("user")
        record["message"] = {
            "role": "user",
            "content": [{"tool_use_id": tool_id, "type": "tool_result", "content": output[:2000], "is_error": is_error}],
        }
        record["toolUseResult"] = {"stdout": output[:2000], "stderr": "", "interrupted": False, "isImage": False}
        self._write(record, "tool_result", None)

    # -- status ----------------------------------------------------------------

    def _status(self) -> None:
        with contextlib.suppress(OSError):
            _atomic_json(
                self.status_file,
                {
                    "label": self.label,
                    "sid": self.sid,
                    "pid": os.getpid(),
                    "phase": self.phase,
                    "lines": self.lines,
                    "turns": self.turns,
                    "last_write": time.time(),
                    "plugins": [{k: p[k] for k in ("id", "root", "version", "events")} for p in self.plugins],
                },
            )

    # -- the session -----------------------------------------------------------

    def _sleep(self, seconds: float) -> None:
        end = time.time() + seconds
        while time.time() < end and not self.stop_file.exists():
            time.sleep(min(0.5, max(0.0, end - time.time())))

    def _gap(self) -> None:
        self._sleep(self.line_gap_s * (0.6 + 0.8 * self.rng.random()))

    def run_bash(self, command: str) -> tuple[str, bool]:
        started = time.time()
        env = dict(self.env)
        try:
            done = subprocess.run(
                [*self.shell, command], cwd=self.cwd, env=env, capture_output=True, timeout=120,
                stdin=subprocess.DEVNULL,
            )
            code, out = done.returncode, (done.stdout + done.stderr).decode("utf-8", "replace")
        except subprocess.TimeoutExpired:
            code, out = None, "(timed out after 120 s)"
        except OSError as exc:
            code, out = None, f"(could not run: {exc})"
        _append_jsonl(
            self.tool_log,
            {"t": started, "session": self.label, "command": command, "exit": code,
             "duration_s": round(time.time() - started, 3), "output_tail": out[-300:]},
            self.log_lock,
        )
        return out, code != 0

    def _compact_due(self, n: int) -> bool:
        """The driver asked (an update landed), or the schedule: turn 2, then every `compact_every`."""
        asked = False
        if self.compact_file is not None and self.compact_file.exists():
            with contextlib.suppress(OSError):
                self.compact_file.unlink()
            asked = True
        return asked or (self.compact_every > 0 and (n == 2 or n % self.compact_every == 0))

    def turn(self) -> None:
        self.turns += 1
        n = self.turns
        if self._compact_due(n):
            # Before a compaction Claude Code fires PreCompact; no transcript line here.
            self.fire("PreCompact", trigger="auto", custom_instructions="")
        prompt = f"Turn {n}: look at the run outputs and tell me what changed"
        self.fire("UserPromptSubmit", prompt=f"{prompt} ({self._marker()})")
        self.user_text(prompt)
        self._gap()
        self.assistant_text(f"Turn {n}: checking the working directory first")
        self._gap()
        if n % self.probe_tool_every == 0:
            name, command = "Bash", "probe --version"
        elif n % 3 == 0:
            name, command = "Read", ""
        else:
            name, command = "Bash", "ls -la && date"
        if name == "Bash":
            marker = self._marker()
            tool_input = {"command": f"{command}  # {marker}", "description": f"turn {n} check"}
            tool_id = self.tool_use("Bash", tool_input, marker)
            self.fire("PreToolUse", tool="Bash", tool_name="Bash", tool_input=tool_input, tool_use_id=tool_id)
            output, failed = self.run_bash(command)
            self.fire(
                "PostToolUse", tool="Bash", tool_name="Bash", tool_input=tool_input, tool_use_id=tool_id,
                tool_response={"stdout": output[:2000], "stderr": "", "interrupted": False, "isImage": False},
            )
        else:
            path = os.path.join(self.cwd, "notes.md")
            tool_input = {"file_path": path}
            tool_id = self.tool_use("Read", tool_input, None)
            self.fire("PreToolUse", tool="Read", tool_name="Read", tool_input=tool_input, tool_use_id=tool_id)
            try:
                output, failed = Path(path).read_text(encoding="utf-8")[:2000], False
            except OSError as exc:
                output, failed = str(exc), True
            self.fire(
                "PostToolUse", tool="Read", tool_name="Read", tool_input=tool_input, tool_use_id=tool_id,
                tool_response={"type": "text", "file": {"filePath": path, "content": output[:2000]}},
            )
        self._gap()
        self.tool_result(tool_id, output, failed)
        self._gap()
        self.assistant_text(f"Turn {n}: done; nothing unusual in the outputs")
        self.fire("Stop", stop_hook_active=False)

    def run(self) -> int:
        self._status()
        self.fire("SessionStart", source="startup", model=MODEL)
        post = self.cfg.get("post_start")
        if post:
            with contextlib.suppress(Exception):
                subprocess.run(post, env=self.env, timeout=60, capture_output=True)
        self.phase = "running"
        self._status()
        while self.turns < self.min_turns or not self.stop_file.exists():
            began = time.time()
            self.turn()
            self._sleep(max(1.0, self.turn_every_s - (time.time() - began)))
        self.phase = "ending"
        self._status()
        self.fire("SessionEnd", reason="prompt_input_exit")
        self.phase = "ended"
        self._status()
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="session_agent")
    parser.add_argument("--config", required=True)
    args = parser.parse_args(argv)
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    session = Session(cfg)

    def stop(_signum, _frame):
        with contextlib.suppress(OSError):
            session.stop_file.touch()

    for name in ("SIGTERM", "SIGINT"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), stop)
    return session.run()


if __name__ == "__main__":
    sys.exit(main())
