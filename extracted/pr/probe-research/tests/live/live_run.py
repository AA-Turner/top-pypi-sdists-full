#!/usr/bin/env python3
"""The live run: open sessions keep recording, and their hooks keep working,
across automatic Probe updates, with no restart (release plan section 10,
decisions D24-D27, D46; eng review Part D, D2 "long-running-session survival test").

    python agent/tests/live/live_run.py --smoke                 # ~22 min, local
    python agent/tests/live/live_run.py --duration-min 300      # the 5 h release run
    python agent/tests/live/live_run.py --help

What it builds, all under one scratch root (`--root`, default a fresh temp dir)
and a scratch HOME inside it -- never this machine's real `~/.local/state/probe`,
`~/.claude`, `~/.codex` or its real Probe service:

  private update server   one stub HTTP server on 127.0.0.1 is BOTH
                          * the Probe API the CLI, tap, hooks and updater call
                            (`/v1/client-version`, `/v1/me`, the tap's ingest
                            routes, update reports; everything else is answered
                            and recorded as unhandled); it RECORDS every upload
                          * a PEP 503 package index (`/simple/`) holding only this
                            checkout's own wheels at versions N, N+1, N+2
                          plus a local plugin marketplace folder (the checkout's
                          plugins with their versions rewritten) that a stand-in
                          `claude` plugin manager installs from.
  the CLI                 `uv tool install probe-research[all]` from that index,
                          as a real user's install: `probe` and `python -m
                          probe.service` run from the uv tool env.
  sessions                K long-lived stand-in Claude Code sessions
                          (`session_agent.py`), each writing a real-looking
                          transcript and firing every hooks.json entry exactly as
                          Claude Code runs it. SessionStart starts `tap watch`
                          through the tap plugin's real hook, so the service
                          registration is the real one.
  updates                 at the scheduled times the driver publishes N+1, then
                          N+2 (wheel into the index, manifest bump, plugin folders
                          into the marketplace) and runs `probe service
                          check-now`; the service updates on its own from there.
                          After each update lands, a NEW short session (`n<k>`)
                          starts on the new plugins.

Checks (report.json `checks`, each pass / fail / skip): every transcript line
accepted exactly once, in order, finalized at the end (`recording.*`, also by a
marker in each line's text); no ingest protocol violation; no live session
stalled; each tap stayed up; every hook exited 0 inside its timeout and every
event fired (`hooks.*`); after each plugin update the open sessions' prompt hooks
ran the INSTALLED version (`hooks.handover`: every plugin tree the run builds adds
one prompt-lane route that logs the folder it ran from -- the run's own test
releases carry it, never the checkout); no `probe` call that met the update
barrier outlived its budget; sessions stayed registered with the service; the
service and the installs end on N+2; only the run's own versions appeared; each
release landed in time (`update.applied`: the service's 15-min check_now
cooldown counts in); the daemon worker held its lock. Findings (not checks) name
what the run saw besides: deferrals, cycles the service called ok that its update
report called failed, a restart into an older CLI, slow SessionEnd hooks.

THE TEST-ONLY UPDATE CHANNEL (D27). Nothing here can reach the real channel's
releases EXCEPT the public PyPI index itself, and only when the update child does
not see the private index -- which is exactly the bug the run then reports:

  base_url    `~/.config/probe/config.json` (what the wizard writes) and
              PROBE_BASE_URL in every session's env point at the stub. The
              service's children read the config file (their env is clean).
  index       `--index-via login-shell` (default, the release gate): UV_INDEX
              `probe-live=<stub>/simple/` is exported in the scratch HOME's login
              profiles (~/.profile, ~/.bash_profile, ~/.zprofile, ~/.zshenv) and in
              every session's env. The Probe service starts with a clean env
              (`probe.service.client.ENV_ALLOWLIST`), so its scheduled update child
              sees UV_INDEX only once R1's D11 (login-shell import of the
              allowlisted variables) is in. Before that, the child resolves
              probe-research from PyPI: the run sees a version that is not one of
              its own and fails `install.local_channel_only` (finding D11).
              `--index-via uv-config` also writes `~/.config/uv/uv.toml` with that
              index, which every `uv` under this HOME reads whatever its env: use
              it to exercise everything else on a branch without D11.
  plugins     `claude plugin marketplace update` re-copies the local marketplace
              folder; the marketplace is registered from that folder, never git.

STAND-INS (no API keys exist in this repo's CI secrets; D26):
  * Claude Code sessions: `session_agent.py` (scripted turns, no model).
  * `claude plugin ...`: `standin_claude.py` (Claude Code's file layout).
  * the daemon worker (`--daemon-session`): `real` runs the real `probe daemon
    worker` (the `daemon` extra is installed) against the stub, whose model
    gateway answers 503, so the worker runs, holds its session lock and keeps
    retrying; `standin` runs a process that only holds the lock and exits on
    SIGTERM; `none` runs no daemon session. Either way the tap's real supervisor
    (`tap/companion_supervisor.py`) starts and restarts it.
  * the Probe API and the package index: the stub above.
  Real: the CLI, the service, the updater, the tap, every hook script, uv.

WINDOWS (R1: the tap and pi do not start the service there): hooks run under Git
Bash, the service-only checks are reported "skipped (Windows, R1)", and updates
are applied the way a non-POSIX machine applies them, `probe wizard --action
update --yes` (what the plugin's SessionStart hook spawns there).

Output (`--out`, default `<root>/out`): `report.json`, `summary.txt` and the logs
(service.log, update.log, tap logs, hook/tool/line logs, the stub's request and
upload record, probe-call timings). Exit 1 when any check fails, 2 on a harness
error. The end phase (sessions ending through the report) is bounded by
`--end-budget-min`: past it a watchdog names the step it hung in, writes the
report from what the run has (`meta.partial`) and exits 2. Commands the driver
runs write to temporary files, never pipes, so a process they leave behind
(the service `probe service stop` talks to) cannot hold the driver.

Stdlib only (plus the checkout's own `tap.service` client, imported from the tap
plugin folder). Run it with any Python >= 3.10.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import html
import json
import os
import platform
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import uuid
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HERE = Path(__file__).resolve().parent
AGENT = HERE.parents[1]
TAP_ROOT = AGENT / "plugins" / "probe-research-tap"
MAIN_PLUGIN = "probe-research"
TAP_PLUGIN = "probe-research-tap"
MARKETPLACE = "research-os-agent"
PLUGIN_IDS = (f"{MAIN_PLUGIN}@{MARKETPLACE}", f"{TAP_PLUGIN}@{MARKETPLACE}")
DIST = "probe-research"
INDEX_NAME = "probe-live"
WINDOWS = os.name == "nt"
#: `probe.service.barrier.WAIT_S`: how long a `probe` started under the update
#: barrier may wait for the update before it gives up.
BARRIER_WAIT_S = 10.0
#: `probe.service.updater.CHECK_NOW_COOLDOWN_S`: a check_now within this of the
#: last finished cycle answers `recent`.
CHECK_NOW_COOLDOWN_S = 15 * 60
MARKER_RE = re.compile(r"LIVE-RUN-MARK ([a-z]\d+) L(\d{6})")
CURSORS = ("batch_seq", "source_byte_end", "source_line_end", "event_end", "prefix_sha256")
CUSTOMER = "live-run"
#: Added to the prompt lane of every plugin tree the run builds (the run's own
#: test releases, never the checkout): which plugin folder a session's prompt
#: hooks really ran from. A session keeps the hooks.json of the version it
#: started with; `dispatch.py`'s hand-over must run the INSTALLED version's
#: routes, and this line is how the run sees that it did.
CANARY_LOG = ".live-run/route-canary.log"
CANARY_ROUTE = {
    "type": "command",
    "command": "/bin/bash -c 'printf \"%s %s %s\\n\" \"$(date +%s)\" \"${CLAUDE_CODE_SESSION_ID:-none}\" "
               "\"${CLAUDE_PLUGIN_ROOT:-none}\" >> \"$HOME/" + CANARY_LOG + "\"'",
    "timeout": 2,
}


class Check:
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


# -- small helpers -------------------------------------------------------------


_log_lock = threading.Lock()
_log_file: Path | None = None
T0 = time.time()


def log(message: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')} +{(time.time() - T0) / 60:6.2f}m] {message}"
    with _log_lock:
        print(line, flush=True)
        if _log_file is not None:
            with contextlib.suppress(OSError), _log_file.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path: Path, data, indent: int | None = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=indent)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def run_bounded(argv: list[str], *, env: dict | None = None, timeout: float = 600,
                cwd: str | None = None) -> subprocess.CompletedProcess:
    """`subprocess.run(capture_output=True, timeout=...)`, minus its two hangs.

    Its output goes to temporary FILES, never pipes. A pipe is read to its end,
    and the end comes only when every process holding its write side closes it:
    a grandchild that inherited it (the service `probe service stop` starts, a
    daemon worker) keeps it open. POSIX then waited out the whole `timeout`
    after the command itself had exited; Windows, where CPython collects the
    output again WITHOUT a timeout after killing a command that timed out,
    waited forever (a Windows run sat 20+ min after `final_uploads_complete`).
    Here only the command is waited for, at most `timeout`, then killed: exit
    124, as before. Text is decoded as UTF-8 (PYTHONUTF8=1 on the runners)."""
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            child = subprocess.Popen(argv, env=env, cwd=cwd, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
        except OSError as exc:
            return subprocess.CompletedProcess(argv, 127, "", f"cannot run {argv[0]}: {exc}")
        note = ""
        try:
            code = child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            child.kill()
            with contextlib.suppress(subprocess.TimeoutExpired):
                child.wait(timeout=10)
            code, note = 124, f"timed out after {timeout}s"
        texts = []
        for handle in (out, err):
            size = os.fstat(handle.fileno()).st_size
            if hasattr(os, "pread"):
                # The offset is shared with a grandchild still writing: never move it.
                data = os.pread(handle.fileno(), size, 0)
            else:
                handle.seek(0)
                data = handle.read(size)
            texts.append(data.decode("utf-8", "replace"))
    stderr = f"{texts[1]}\n{note}" if note and texts[1] else (note or texts[1])
    return subprocess.CompletedProcess(argv, code, texts[0], stderr)


def read_jsonl(path: Path) -> list[dict]:
    out = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                with contextlib.suppress(ValueError):
                    value = json.loads(line)
                    if isinstance(value, dict):
                        out.append(value)
    except OSError:
        pass
    return out


def bump(version: str, patch: int) -> str:
    major, minor = version.split(".")[:2]
    return f"{major}.{minor}.{patch}"


def pid_alive(pid: int | None) -> bool:
    if not isinstance(pid, int) or pid <= 1:
        return False
    if WINDOWS:
        out = run_bounded(["tasklist", "/FI", f"PID eq {pid}", "/NH"], timeout=30).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True
    return True


def flock_held(path: Path) -> bool | None:
    """Is this lock file held (the daemon worker's `<sid>.lock`)? None: no fcntl."""
    try:
        import fcntl
    except ImportError:
        return None
    try:
        handle = open(path, "rb")  # noqa: SIM115
    except OSError:
        return False
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
    except OSError:
        return True
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return False
    finally:
        handle.close()


def git_bash() -> str | None:
    """Git for Windows' bash (what Claude Code runs hooks with on Windows)."""
    for candidate in (
        os.environ.get("CLAUDE_CODE_GIT_BASH_PATH"),
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
        shutil.which("bash"),
    ):
        if candidate and Path(candidate).is_file():
            return candidate
    return None


_WATCHER_DIR: list = []


def watcher_dir() -> Path:
    """Where the hooks keep a session's watcher files: `/tmp`, and on Windows
    the folder Git Bash maps its `/tmp` to (what the hooks hand the tap as
    PROBE_TAP_WATCHER_DIR), never `\\tmp` on the current drive."""
    if not WINDOWS:
        return Path("/tmp")
    if not _WATCHER_DIR:
        folder = None
        bash = git_bash()
        if bash:
            with contextlib.suppress(OSError, subprocess.SubprocessError):
                done = subprocess.run([bash, "-c", "cygpath -w /tmp"], capture_output=True, text=True, timeout=30,
                                      check=False)
                folder = done.stdout.strip() or None
        _WATCHER_DIR.append(Path(folder) if folder else Path(tempfile.gettempdir()))
    return _WATCHER_DIR[0]


# -- the layout -----------------------------------------------------------------


@dataclass
class Layout:
    root: Path
    out: Path

    def __post_init__(self) -> None:
        self.home = self.root / "home"
        self.bin = self.root / "bin"
        self.agents = self.root / "agents"
        self.build = self.root / "build"
        self.index = self.root / "index"
        self.market = self.root / "marketplace"
        self.trees = self.root / "plugin-trees"
        self.work = self.root / "work"
        self.run = self.root / "run"
        self.stub = self.root / "stub"
        self.claude = self.home / ".claude"
        self.config = self.home / ".config"
        self.state = self.home / ".local" / "state"
        self.data = self.home / ".local" / "share"
        self.cache = self.home / ".cache"
        self.local_bin = self.home / ".local" / "bin"
        self.probe_state = self.state / "probe"
        # Windows (R3): `%LOCALAPPDATA%\probe\service` (`probe.service.paths.root_dir`).
        self.service_dir = (self.home / "AppData" / "Local" / "probe" / "service") if WINDOWS \
            else self.probe_state / "service"
        self.tap_state = self.claude / "plugins" / TAP_PLUGIN
        self.live = self.home / ".live-run"

    @property
    def machine_dir(self) -> Path:
        """The service's own folder: `service/<machine key>/` since R1 (D8),
        the shared folder before."""
        with contextlib.suppress(OSError):
            for folder in sorted(self.service_dir.iterdir()):
                if folder.is_dir() and (folder / "service.lock").exists():
                    return folder
        return self.service_dir

    def make(self) -> None:
        for path in (self.home, self.bin, self.agents, self.build, self.index, self.market, self.trees,
                     self.work, self.run, self.stub, self.out, self.claude, self.config, self.state, self.data,
                     self.cache, self.local_bin, self.live):
            path.mkdir(parents=True, exist_ok=True)

    @property
    def real_probe(self) -> Path:
        return self.local_bin / ("probe.exe" if WINDOWS else "probe")

    @property
    def shim_probe(self) -> Path:
        return self.bin / ("probe.cmd" if WINDOWS else "probe")


# -- versions --------------------------------------------------------------------


@dataclass
class Versions:
    cli: list[str]
    plugin: list[str]
    tap: list[str]

    @classmethod
    def from_checkout(cls) -> Versions:
        cli = re.search(r'^version = "([^"]+)"', (AGENT / "pyproject.toml").read_text(), re.M).group(1)
        plugin = read_json(AGENT / "plugins" / MAIN_PLUGIN / ".claude-plugin" / "plugin.json")["version"]
        tap = read_json(TAP_ROOT / ".claude-plugin" / "plugin.json")["version"]
        # Patch numbers no real release uses, so every version on this machine is
        # recognisably one of the run's own (and newer than anything released).
        return cls(
            cli=[bump(cli, 9001 + k) for k in range(3)],
            plugin=[bump(plugin, 9001 + k) for k in range(3)],
            tap=[bump(tap, 9001 + k) for k in range(3)],
        )

    def manifest(self, k: int) -> dict:
        return {
            "cli": {"latest": self.cli[k], "min": "0.177.0"},
            "plugin": {"latest": self.plugin[k], "min": "0.90.0"},
            "tap": {"latest": self.tap[k], "min": "0.6.0"},
        }


# -- the stub Probe API + package index -------------------------------------------


class StubState:
    """Everything the stub knows and records. One lock for all of it."""

    def __init__(self, layout: Layout, tokens: dict) -> None:
        self.layout = layout
        self.tokens = tokens
        self.lock = threading.Lock()
        self.manifest: dict = {}
        self.streams: dict = {}  # (source, sid) -> {"stream", "receipts", "batches"}
        self.violations: list[dict] = []
        self.unhandled: dict = {}
        self.counts: dict = {}
        self.index_hits: list[dict] = []
        self.requests_log = (layout.stub / "requests.jsonl").open("a", encoding="utf-8")
        self.batches_log = (layout.stub / "batches.jsonl").open("a", encoding="utf-8")
        self.model_calls = 0

    def record(self, entry: dict) -> None:
        with self.lock:
            self.requests_log.write(json.dumps(entry) + "\n")
            self.requests_log.flush()
            key = f"{entry['method']} {entry['route']}"
            self.counts[key] = self.counts.get(key, 0) + 1

    def stream_of(self, source: str, sid: str) -> dict:
        return self.streams.setdefault((source, sid), {"stream": None, "receipts": {}, "batches": []})

    def receipts(self, source: str, sid: str, after: int, limit: int | None) -> dict:
        with self.lock:
            st = self.stream_of(source, sid)
            body = {
                "protocol_version": 2,
                "customer_id": CUSTOMER,
                "source": source,
                "session_id": sid,
                "uploader_device_id": "live-run-device",
            }
            if st["stream"] is None:
                return {**body, "state": "absent", "receipts": []}
            rows = [r for seq, r in sorted(st["receipts"].items()) if seq > after]
            return {**body, "state": "ready", "stream": dict(st["stream"]),
                    "receipts": rows[:limit] if limit else rows}

    def accept(self, source: str, raw: bytes) -> tuple[int, dict]:
        try:
            data = json.loads(raw)
            sid = data["session_id"]
            seq = int(data["batch_seq"])
        except (ValueError, KeyError, TypeError) as exc:
            return 422, {"detail": f"invalid batch: {exc}"}
        sha = hashlib.sha256(raw).hexdigest()
        text = raw.decode("utf-8", "replace")
        with self.lock:
            st = self.stream_of(source, sid)
            previous = st["receipts"].get(seq)
            if previous is not None:
                if previous["body_sha256"] != sha:
                    self._violation(sid, seq, "a second, different body for an accepted batch_seq")
                    return 409, {"detail": "batch identity already accepted with different content"}
                self._batch(st, data, raw, sha, text, "duplicate")
                return 202, {"protocol_version": 2, "status": "duplicate", "receipt": previous}
            stream = st["stream"]
            problems = []
            if data.get("protocol_version") != 2:
                problems.append(f"protocol {data.get('protocol_version')} (the stub offers 2 only)")
            if stream is None:
                if seq != 0:
                    problems.append(f"first batch is seq {seq}")
                if data.get("source_line_start") not in (0, None):
                    problems.append(f"first batch starts at line {data.get('source_line_start')}")
            else:
                if data.get("stream_id") != stream["stream_id"]:
                    problems.append("another stream_id for an existing stream")
                if seq != stream["last_seq"] + 1:
                    problems.append(f"seq {seq} after {stream['last_seq']}")
                if data.get("source_line_start") != stream["source_line_end"]:
                    problems.append(
                        f"lines start at {data.get('source_line_start')}, stream ends at {stream['source_line_end']}"
                    )
                if data.get("source_byte_start") != stream["source_byte_end"]:
                    problems.append(
                        f"bytes start at {data.get('source_byte_start')}, stream ends at {stream['source_byte_end']}"
                    )
            if problems:
                self._violation(sid, seq, "; ".join(problems))
                return 409, {"detail": "batch does not continue the stream: " + "; ".join(problems)}
            receipt = {k: data[k] for k in CURSORS}
            receipt.update(body_sha256=sha, finalized=bool(data.get("finalize")))
            st["receipts"][seq] = receipt
            st["stream"] = {
                "stream_id": data["stream_id"],
                "last_seq": seq,
                "source_byte_end": data["source_byte_end"],
                "source_line_end": data["source_line_end"],
                "event_end": data["event_end"],
                "prefix_sha256": data["prefix_sha256"],
                "finalized": bool(data.get("finalize")),
                "snapshot_byte_end": None,
                "snapshot_sha256": None,
            }
            self._batch(st, data, raw, sha, text, "accepted")
            return 202, {"protocol_version": 2, "status": "accepted", "receipt": receipt}

    def _violation(self, sid: str, seq: int, what: str) -> None:
        entry = {"t": time.time(), "session_id": sid, "batch_seq": seq, "what": what}
        self.violations.append(entry)
        log(f"stub: INGEST VIOLATION {entry}")

    def _batch(self, st: dict, data: dict, raw: bytes, sha: str, text: str, status: str) -> None:
        markers = [f"{m.group(1)}:{int(m.group(2))}" for m in MARKER_RE.finditer(text)]
        entry = {
            "t": time.time(),
            "status": status,
            "session_id": data["session_id"],
            "batch_seq": data["batch_seq"],
            "line_start": data.get("source_line_start"),
            "line_end": data.get("source_line_end"),
            "byte_start": data.get("source_byte_start"),
            "byte_end": data.get("source_byte_end"),
            "event_start": data.get("event_start"),
            "event_end": data.get("event_end"),
            "events": len(data.get("events") or []),
            "finalize": bool(data.get("finalize")),
            "bytes": len(raw),
            "sha256": sha,
            "markers": markers,
        }
        st["batches"].append(entry)
        self.batches_log.write(json.dumps(entry) + "\n")
        self.batches_log.flush()

    def snapshot(self) -> dict:
        with self.lock:
            return {
                sid: {"batches": list(st["batches"]), "stream": dict(st["stream"]) if st["stream"] else None}
                for (_source, sid), st in self.streams.items()
            }


def make_handler(state: StubState):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = "probe-live-stub/1"

        def log_message(self, *_args) -> None:  # quiet: requests.jsonl has them
            pass

        def _send(self, code: int, body, content_type: str = "application/json") -> int:
            data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)
            return len(data)

        def _body(self) -> bytes:
            length = int(self.headers.get("Content-Length") or 0)
            return self.rfile.read(length) if length else b""

        def _handle(self) -> None:
            started = time.time()
            parts = urlsplit(self.path)
            path = parts.path
            query = parse_qs(parts.query)
            raw = self._body() if self.command in ("POST", "PUT", "PATCH") else b""
            route, code, sent = path, 500, 0
            try:
                route, code, payload, ctype = self._route(path, query, raw)
                sent = self._send(code, payload, ctype)
            except Exception as exc:  # noqa: BLE001 -- the stub must never die
                log(f"stub: {self.command} {path} failed: {exc!r}")
                sent = self._send(500, {"detail": f"stub error: {exc!r}"})
            state.record({
                "t": started, "method": self.command, "path": path, "route": route, "status": code,
                "in": len(raw), "out": sent, "ms": round((time.time() - started) * 1000, 1),
                "ua": (self.headers.get("User-Agent") or "")[:80],
                "auth": bool(self.headers.get("Authorization")),
            })

        def _route(self, path: str, query: dict, raw: bytes):
            method = self.command
            if path.startswith("/simple"):
                return self._index(path)
            if path.startswith("/files/"):
                name = Path(path).name
                target = state.layout.index / name
                if not target.is_file():
                    return "/files/<wheel>", 404, {"detail": "no such file"}, "application/json"
                with state.lock:
                    state.index_hits.append({"t": time.time(), "file": name})
                return "/files/<wheel>", 200, target.read_bytes(), "application/octet-stream"
            if path == "/v1/client-version":
                with state.lock:
                    manifest = json.loads(json.dumps(state.manifest))
                return path, 200, manifest, "application/json"
            if path == "/v1/me":
                return path, 200, {
                    "id": "user-live-run", "user_id": "user-live-run", "email": "live-run@example.invalid",
                    "customer_id": CUSTOMER, "team": {"id": CUSTOMER, "name": "Live run"},
                }, "application/json"
            if path == "/ingest/v1/sessions/status":
                return path, 200, {"ingest_enabled": True, "reason": None}, "application/json"
            m = re.fullmatch(r"/ingest/v1/sessions/([a-z_]+)/([^/]+)/receipts", path)
            if m and method == "GET":
                after = int((query.get("after") or ["-1"])[0])
                limit = query.get("limit")
                body = state.receipts(m.group(1), m.group(2), after, int(limit[0]) if limit else None)
                return "/ingest/v1/sessions/<source>/<sid>/receipts", 200, body, "application/json"
            m = re.fullmatch(r"/ingest/v1/sessions/([a-z_]+)/([^/]+)/(title|media)", path)
            if m and method == "POST":
                route = f"/ingest/v1/sessions/<source>/<sid>/{m.group(3)}"
                return route, 200, ({"status": "ok"} if m.group(3) == "title" else {"status": "have"}), \
                    "application/json"
            m = re.fullmatch(r"/ingest/v1/sessions/([a-z-]+)", path)
            if m and method == "POST":
                code, body = state.accept(m.group(1).replace("-", "_"), raw)
                return "/ingest/v1/sessions/<route>", code, body, "application/json"
            if path == "/v1/client/update-reports" and method == "POST":
                with contextlib.suppress(OSError):
                    with (state.layout.stub / "update-reports.jsonl").open("a", encoding="utf-8") as handle:
                        handle.write(raw.decode("utf-8", "replace") + "\n")
                return path, 202, {"status": "accepted"}, "application/json"
            if path.startswith("/v1/companion/"):
                with state.lock:
                    state.model_calls += 1
                # No model behind the stub: the daemon worker's gateway is down. The
                # worker keeps running (and holding its session lock), retrying.
                return "/v1/companion/*", 503, {"detail": "live-run stub: no model gateway"}, "application/json"
            route = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f-]{27,}", "<id>", path)
            with state.lock:
                state.unhandled[f"{method} {route}"] = state.unhandled.get(f"{method} {route}", 0) + 1
            if method == "GET":
                return route, 200, {}, "application/json"
            return route, 200, {"status": "ok"}, "application/json"

        def _index(self, path: str):
            files = sorted(p.name for p in state.layout.index.glob("*.whl"))
            if path.rstrip("/") == "/simple":
                body = "<html><body><a href=\"/simple/probe-research/\">probe-research</a></body></html>"
                return "/simple/", 200, body.encode(), "text/html"
            project = path.rstrip("/").split("/")[-1]
            if project.replace("_", "-").lower() != DIST:
                return "/simple/<other>", 404, b"not here", "text/plain"
            with state.lock:
                state.index_hits.append({"t": time.time(), "file": "/simple/probe-research/"})
            links = []
            for name in files:
                digest = hashlib.sha256((state.layout.index / name).read_bytes()).hexdigest()
                links.append(f'<a href="/files/{html.escape(name)}#sha256={digest}">{html.escape(name)}</a><br/>')
            body = "<html><body>\n" + "\n".join(links) + "\n</body></html>"
            return "/simple/probe-research/", 200, body.encode(), "text/html"

        def do_GET(self) -> None:  # noqa: N802
            self._handle()

        def do_HEAD(self) -> None:  # noqa: N802
            self._handle()

        def do_POST(self) -> None:  # noqa: N802
            self._handle()

        def do_PUT(self) -> None:  # noqa: N802
            self._handle()

        def do_PATCH(self) -> None:  # noqa: N802
            self._handle()

        def do_DELETE(self) -> None:  # noqa: N802
            self._handle()

    return Handler


# -- the run ----------------------------------------------------------------------


@dataclass
class SessionInfo:
    label: str
    sid: str
    cwd: Path
    transcript: Path
    daemon: bool
    config: Path
    status_file: Path
    stop_file: Path
    hook_log: Path
    lines_log: Path
    tool_log: Path
    out_file: Path
    process: subprocess.Popen | None = None
    started_at: float | None = None
    ended_at: float | None = None
    #: A short session started after an update landed (`n<k>`): it ends itself here.
    stop_at: float | None = None
    #: Touched by the driver after each update lands: the session fires PreCompact next turn.
    compact_file: Path | None = None
    #: The session agent's exit status (None: it never exited, or was killed at the end).
    exit_code: int | None = None


@dataclass
class Publication:
    k: int
    version: str
    scheduled_min: float
    published_at: float | None = None
    landed_at: float | None = None
    #: The next release was published before this one landed.
    superseded: bool = False
    checks: list = field(default_factory=list)


class Run:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        root = Path(args.root).resolve() if args.root else Path(tempfile.mkdtemp(prefix="probe-live-"))
        out = Path(args.out).resolve() if args.out else root / "out"
        self.layout = Layout(root, out)
        self.versions = Versions.from_checkout()
        self.tokens = {
            "token": "probe_pat_liverun" + secrets.token_hex(8),
            "ingest_token": "ros_ing_liverun" + secrets.token_hex(8),
            "companion_token": "probe_cmp_liverun" + secrets.token_hex(8),
        }
        self.state: StubState | None = None
        self.server: ThreadingHTTPServer | None = None
        self.port = 0
        self.sessions: list[SessionInfo] = []
        self.publications: list[Publication] = []
        self.timeline_path = self.layout.out / "timeline.jsonl"
        self.samples: list[dict] = []
        self.events: list[dict] = []
        self.stop = threading.Event()
        self.monitor_thread: threading.Thread | None = None
        # Windows has a service since R3 (`--expect-hosted` there says so).
        self.service_ok = not WINDOWS or bool(getattr(args, "expect_hosted", False))
        self.t_sessions = 0.0
        self.observed_cli: set[str] = set()
        self.foreign_seen: set[str] = set()
        #: Sessions whose last uploads had not landed when `wait_final_uploads` gave
        #: up ({} once all landed; None while it never ran).
        self.final_missing: dict | None = None
        self.findings: list[dict] = []
        self.harness_errors: list[str] = []
        self.client = None  # the checkout's tap.service client, once HOME is ours
        self.tool_python: Path | None = None
        self.uv = shutil.which("uv")
        #: The interpreter behind this one (a venv's base): the hooks' `python3`,
        #: the session agents', the shims', and what the CLI's tool env is built on.
        self.base_python = Path(getattr(sys, "_base_executable", None) or sys.executable).resolve()
        self.python312 = args.python or str(self.base_python)
        #: The end phase (sessions ending through the report): the step it is at,
        #: the checks once they ran, and the watchdog that bounds it all.
        self.end_step = ""
        self.results: list[dict] = []
        self.end_done = threading.Event()
        self._watchdog: threading.Thread | None = None
        #: One report at a time: the main thread's, or the watchdog's partial one.
        self._report_lock = threading.Lock()

    # -- events -------------------------------------------------------------

    def event(self, kind: str, **detail) -> None:
        entry = {"t": time.time(), "min": round((time.time() - (self.t_sessions or T0)) / 60, 2), "kind": kind,
                 **detail}
        self.events.append(entry)
        with contextlib.suppress(OSError), self.timeline_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")
        log(f"{kind}: {json.dumps(detail)[:300]}")

    def minutes(self) -> float:
        return (time.time() - self.t_sessions) / 60 if self.t_sessions else 0.0

    # -- environment ----------------------------------------------------------

    def base_env(self) -> dict:
        """The scratch user's environment: nothing of this machine's own HOME,
        Probe settings or coding-agent session leaks in."""
        L = self.layout
        keep = ("LANG", "LC_ALL", "LC_CTYPE", "TZ", "TMPDIR", "TEMP", "TMP", "SYSTEMROOT", "SystemRoot", "COMSPEC",
                "PATHEXT", "WINDIR", "PROGRAMFILES", "ProgramFiles", "ProgramFiles(x86)", "PROGRAMDATA",
                "NUMBER_OF_PROCESSORS", "PROCESSOR_ARCHITECTURE", "OS", "SSL_CERT_FILE", "SSL_CERT_DIR",
                "REQUESTS_CA_BUNDLE", "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy",
                "no_proxy")
        env = {k: os.environ[k] for k in keep if k in os.environ}
        user = os.environ.get("USER") or os.environ.get("USERNAME") or "runner"
        # `bin` holds the shims (probe, claude) and links to uv and python3: never
        # this machine's own ~/.local/bin, whose real probe/claude/pi/codex an
        # update child would otherwise find.
        path = [str(L.bin), str(L.local_bin)]
        if WINDOWS:
            for tool in (self.uv, sys.executable):
                folder = str(Path(tool).parent)
                if folder not in path:
                    path.append(folder)
            path += [p for p in os.environ.get("PATH", "").split(os.pathsep) if p and p not in path]
        else:
            path += ["/usr/local/bin", "/opt/homebrew/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"]
        env.update({
            "HOME": str(L.home),
            "USER": user,
            "LOGNAME": user,
            "SHELL": "/bin/bash",
            "PATH": os.pathsep.join(path),
            "XDG_CONFIG_HOME": str(L.config),
            "XDG_STATE_HOME": str(L.state),
            "XDG_DATA_HOME": str(L.data),
            "XDG_CACHE_HOME": str(L.cache),
            "CLAUDE_CONFIG_DIR": str(L.claude),
            "CODEX_HOME": str(L.home / ".codex"),
            "PROBE_BASE_URL": self.base_url,
            "PYTHONUTF8": "1",
        })
        env.setdefault("LANG", "C.UTF-8")
        if WINDOWS:
            env.update({"USERPROFILE": str(L.home), "APPDATA": str(L.home / "AppData" / "Roaming"),
                        "LOCALAPPDATA": str(L.home / "AppData" / "Local")})
        if self.args.index_via == "login-shell":
            env["UV_INDEX"] = self.uv_index
        return env

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    @property
    def uv_index(self) -> str:
        return f"{INDEX_NAME}={self.base_url}/simple/"

    def run_cmd(self, argv: list, *, env: dict | None = None, timeout: float = 600, cwd: Path | None = None,
                label: str = "") -> subprocess.CompletedProcess:
        started = time.time()
        done = run_bounded([str(a) for a in argv], env=env or self.base_env(), timeout=timeout,
                           cwd=str(cwd) if cwd else None)
        name = label or Path(str(argv[0])).name
        with contextlib.suppress(OSError):
            with (self.layout.out / "commands.log").open("a", encoding="utf-8") as handle:
                handle.write(f"\n=== {time.strftime('%H:%M:%S')} {name} ({time.time() - started:.1f}s) exit "
                             f"{done.returncode}: {' '.join(str(a) for a in argv)[:400]}\n")
                handle.write((done.stdout or "")[-4000:])
                handle.write((done.stderr or "")[-4000:])
        return done

    # -- 1. the stub ------------------------------------------------------------

    def start_stub(self) -> None:
        self.state = StubState(self.layout, self.tokens)
        self.server = ThreadingHTTPServer(("127.0.0.1", self.args.port), make_handler(self.state))
        self.server.daemon_threads = True
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, name="stub", daemon=True).start()
        log(f"stub API + index on {self.base_url}")

    # -- 2. builds ------------------------------------------------------------------

    def build_wheels(self) -> None:
        env = self.base_env()
        env.pop("UV_INDEX", None)
        for k, version in enumerate(self.versions.cli):
            src = self.layout.build / f"cli-{version}"
            if src.exists():
                shutil.rmtree(src)
            src.mkdir(parents=True)
            for name in ("pyproject.toml", "README.md", "LICENSE"):
                shutil.copy2(AGENT / name, src / name)
            for name in ("src", "skills"):
                shutil.copytree(AGENT / name, src / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            text = (src / "pyproject.toml").read_text(encoding="utf-8")
            text = re.sub(r'^version = "[^"]+"', f'version = "{version}"', text, count=1, flags=re.M)
            (src / "pyproject.toml").write_text(text, encoding="utf-8")
            wheels = self.layout.build / f"wheels-{k}"
            done = self.run_cmd([self.uv, "build", "--wheel", "--out-dir", wheels, src], env=env, timeout=900,
                                label=f"uv build {version}")
            built = list(wheels.glob("*.whl"))
            if done.returncode != 0 or len(built) != 1:
                raise RuntimeError(f"building the {version} wheel failed: {done.stderr[-2000:]}")
            log(f"built {built[0].name}")

    def build_plugin_trees(self) -> None:
        for k in range(3):
            for name, version in ((MAIN_PLUGIN, self.versions.plugin[k]), (TAP_PLUGIN, self.versions.tap[k])):
                dst = self.layout.trees / str(k) / name
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(AGENT / "plugins" / name, dst,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
                for manifest in dst.glob(".*-plugin/plugin.json"):
                    data = read_json(manifest)
                    data["version"] = version
                    write_json(manifest, data)
                if name == MAIN_PLUGIN and self.args.canary_route:
                    routes = read_json(dst / "hooks" / "routes.json")
                    routes["hooks"]["UserPromptSubmit"].append({"lane": "prompt", "hooks": [CANARY_ROUTE]})
                    write_json(dst / "hooks" / "routes.json", routes)
                if name == TAP_PLUGIN:
                    init = dst / "tap" / "__init__.py"
                    init.write_text(re.sub(r'^__version__ = "[^"]+"', f'__version__ = "{version}"',
                                           init.read_text(encoding="utf-8"), count=1, flags=re.M), encoding="utf-8")
                    pyproject = dst / "pyproject.toml"
                    pyproject.write_text(re.sub(r'^version = "[^"]+"', f'version = "{version}"',
                                                pyproject.read_text(encoding="utf-8"), count=1, flags=re.M),
                                         encoding="utf-8")
        market = read_json(AGENT / ".claude-plugin" / "marketplace.json")
        market["plugins"] = [p for p in market["plugins"] if p["name"] in (MAIN_PLUGIN, TAP_PLUGIN)]
        write_json(self.layout.market / ".claude-plugin" / "marketplace.json", market)

    # -- 3. publishing ----------------------------------------------------------------

    def publish(self, k: int) -> None:
        """Release k: the wheel into the index, the plugins into the marketplace,
        then the manifest (the order a real release lands in)."""
        wheel = next((self.layout.build / f"wheels-{k}").glob("*.whl"))
        shutil.copy2(wheel, self.layout.index / wheel.name)
        for name in (MAIN_PLUGIN, TAP_PLUGIN):
            dst = self.layout.market / "plugins" / name
            staging = dst.with_name(f".{name}.staging")
            if staging.exists():
                shutil.rmtree(staging)
            shutil.copytree(self.layout.trees / str(k) / name, staging)
            if dst.exists():
                shutil.rmtree(dst)
            os.replace(staging, dst)
        with self.state.lock:
            self.state.manifest = self.versions.manifest(k)
        self.event("published", k=k, cli=self.versions.cli[k], plugin=self.versions.plugin[k],
                   tap=self.versions.tap[k])

    # -- 4. the scratch user's machine -------------------------------------------------

    def write_shims(self) -> None:
        L = self.layout
        python = sys.executable if WINDOWS else str(self.base_python)
        for name, script in (("probe", HERE / "probe_shim.py"), ("claude", HERE / "standin_claude.py")):
            if WINDOWS:
                (L.bin / f"{name}.cmd").write_text(f'@"{python}" "{script}" %*\r\n', encoding="utf-8")
            else:
                target = L.bin / name
                target.write_text(f"#!{python}\nimport runpy, sys\nsys.argv[0] = {str(script)!r}\n"
                                  f"runpy.run_path({str(script)!r}, run_name='__main__')\n", encoding="utf-8")
                target.chmod(0o755)
        if WINDOWS:
            self.windows_python3()
        if not WINDOWS:
            # The session agents' interpreter, named `claude` (`tap/owner.py` looks
            # for it); the hooks' `python3` and `uv`, without their folders.
            for link, target in ((L.agents / "claude", self.base_python), (L.bin / "python3", self.base_python),
                                 (L.bin / "uv", Path(self.uv).resolve())):
                with contextlib.suppress(FileNotFoundError):
                    link.unlink()
                link.symlink_to(target)

    def windows_python3(self) -> None:
        """Every hook runs `python3` (under Git Bash). Stock Windows has `python`
        only, or the Store's `python3` alias that opens the Store. Unless
        `--no-windows-python3-shim`, an extensionless `python3` script in the
        run's bin (Git Bash runs it by its shebang) stands in, and the run says so."""
        found = shutil.which("python3")
        works = False
        if found:
            with contextlib.suppress(Exception):
                works = subprocess.run([found, "--version"], capture_output=True, timeout=20).returncode == 0
        detail = f"python3 on PATH: {found or 'none'} ({'runs' if works else 'does not run'})"
        if works:
            self.event("windows_python3", detail=detail)
            return
        self.findings.append({
            "id": "windows-no-python3",
            "what": "every Probe hook and the tap's session-start run `python3`, which stock Windows does not "
                    "provide (plan section 8: do not rely on python3)",
            "evidence": [detail, "shimmed for the rest of this run" if self.args.windows_python3_shim
                         else "not shimmed: hooks fail open and nothing records"],
        })
        if self.args.windows_python3_shim:
            target = Path(sys.executable).as_posix()
            if re.match(r"^[A-Za-z]:/", target):
                target = "/" + target[0].lower() + target[2:]
            (self.layout.bin / "python3").write_text(f'#!/bin/sh\nexec "{target}" "$@"\n', encoding="utf-8",
                                                     newline="\n")
        self.event("windows_python3", detail=detail, shim=self.args.windows_python3_shim)

    def write_login_profiles(self) -> None:
        """What a researcher whose packages come from a private index has in their
        shell. R1's D11 imports it for the service's scheduled update children."""
        lines = [
            "# live-run: the private update channel (test-only; probe.service ENV_ALLOWLIST does not carry it)",
            f"export UV_INDEX='{self.uv_index}'",
            f"export PROBE_BASE_URL='{self.base_url}'",
            f'export PATH="{self.layout.bin}:{self.layout.local_bin}:$PATH"',
            "",
        ]
        for name in (".profile", ".bash_profile", ".zprofile", ".zshenv", ".bashrc"):
            (self.layout.home / name).write_text("\n".join(lines), encoding="utf-8")
        if self.args.index_via == "uv-config":
            # uv's user config: $XDG_CONFIG_HOME/uv (Linux, macOS), %APPDATA%\uv (Windows).
            folders = [self.layout.config / "uv"]
            if WINDOWS:
                folders.append(self.layout.home / "AppData" / "Roaming" / "uv")
            for folder in folders:
                folder.mkdir(parents=True, exist_ok=True)
                (folder / "uv.toml").write_text(
                    f'[[index]]\nname = "{INDEX_NAME}"\nurl = "{self.base_url}/simple/"\n', encoding="utf-8")

    def install_cli(self) -> None:
        extras = "all,daemon" if self.args.daemon_session == "real" else "all"
        done = self.run_cmd([self.uv, "tool", "install", f"{DIST}[{extras}]", "--python", self.python312],
                            timeout=900, label="uv tool install")
        if done.returncode != 0:
            raise RuntimeError(f"uv tool install failed: {done.stderr[-3000:]}")
        tool_dir = self.run_cmd([self.uv, "tool", "dir"], label="uv tool dir").stdout.strip()
        folder = Path(tool_dir) / DIST
        self.tool_python = folder / ("Scripts/python.exe" if WINDOWS else "bin/python")
        version = self.cli_version()
        if version != self.versions.cli[0]:
            raise RuntimeError(f"installed CLI reads {version!r}, expected {self.versions.cli[0]}")
        self.event("installed", cli=version, tool_python=str(self.tool_python))

    def cli_version(self, via_shim: bool = True) -> str | None:
        probe = self.layout.shim_probe if via_shim else self.layout.real_probe
        done = self.run_cmd([probe, "--version"], timeout=120, label="probe --version")
        text = (done.stdout or "").strip()
        version = text.split()[-1] if done.returncode == 0 and text else None
        if version:
            self.observed_cli.add(version)
        return version

    def tool_py(self, code: str, timeout: float = 120) -> subprocess.CompletedProcess:
        return self.run_cmd([self.tool_python, "-c", code], timeout=timeout, label="tool python")

    def configure(self) -> None:
        """What `probe wizard` leaves on a machine, written directly: sign-in
        (config.json), automatic updates, the plugins, the tap's state folder."""
        L = self.layout
        context = {"base_url": self.base_url, **self.tokens}
        write_json(L.config / "probe" / "config.json",
                   {"version": 2, "current_context": "default", "contexts": {"default": context}})
        if self.args.autoupdate_at == "start":
            self.enable_autoupdate()
        claude = [sys.executable, HERE / "standin_claude.py"]
        for argv in (["plugin", "marketplace", "add", L.market], *[["plugin", "install", p] for p in PLUGIN_IDS]):
            done = self.run_cmd([*claude, *argv], label="claude (stand-in)")
            if done.returncode != 0:
                raise RuntimeError(f"stand-in claude {' '.join(map(str, argv))} failed: {done.stderr}")
        L.tap_state.mkdir(parents=True, exist_ok=True)
        if self.args.tap_interval:
            write_json(L.tap_state / ".config", {"sync_interval_seconds": self.args.tap_interval})
        if self.args.daemon_session == "standin":
            (L.live / "standin-worker").write_text("1", encoding="utf-8")
        # Records runtime.json (the CLI's interpreter, which the service is started with).
        done = self.run_cmd([L.shim_probe, "service", "status"], timeout=120, label="probe service status")
        self.event("configured", service_status=(done.stdout or done.stderr).strip()[:200],
                   ledger=self.ledger_versions())

    def enable_autoupdate(self) -> None:
        done = self.tool_py("from probe._shared import autoupdate; print(autoupdate.save(enabled=True))")
        self.event("autoupdate_enabled", ok=done.returncode == 0, detail=(done.stdout or done.stderr)[-200:])

    def ledger_versions(self) -> dict:
        ledger = read_json(self.layout.claude / "plugins" / "installed_plugins.json", {}) or {}
        out = {}
        for plugin_id in PLUGIN_IDS:
            entries = (ledger.get("plugins") or {}).get(plugin_id) or []
            out[plugin_id.split("@")[0]] = entries[0].get("version") if entries else None
        return out

    # -- 5. sessions ------------------------------------------------------------------

    def session_env(self, info: SessionInfo) -> dict:
        env = self.base_env()
        env.update({
            "CLAUDECODE": "1",
            "CLAUDE_CODE_ENTRYPOINT": "cli",
            "CLAUDE_CODE_SESSION_ID": info.sid,
            "CLAUDE_PROJECT_DIR": str(info.cwd),
        })
        return env

    def new_session(self, label: str, daemon: bool) -> SessionInfo:
        L = self.layout
        sid = str(uuid.uuid4())
        cwd = (L.work / label).resolve()
        cwd.mkdir(parents=True, exist_ok=True)
        (cwd / "notes.md").write_text(f"# {label}\nloss 0.42 at step 100\n", encoding="utf-8")
        slug = re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
        info = SessionInfo(
            label=label, sid=sid, cwd=cwd, transcript=L.claude / "projects" / slug / f"{sid}.jsonl",
            daemon=daemon, config=L.run / f"{label}.json", status_file=L.run / f"{label}.status.json",
            stop_file=L.run / f"{label}.stop", hook_log=L.run / f"{label}.hooks.jsonl",
            lines_log=L.run / f"{label}.lines.jsonl", tool_log=L.run / f"{label}.tools.jsonl",
            out_file=L.run / f"{label}.out", compact_file=L.run / f"{label}.compact",
        )
        self.sessions.append(info)
        return info

    def make_sessions(self) -> None:
        for i in range(1, self.args.sessions + 1):
            self.new_session(f"s{i}", self.args.daemon_session != "none" and i == self.args.sessions)

    def start_late_session(self, k: int) -> None:
        """A NEW session once release k landed: it must start on the new plugins
        and record like the old ones (`n<k>`, `--late-session-min` long)."""
        if self.args.late_session_min <= 0:
            return
        info = self.new_session(f"n{k}", False)
        self.start_session(info)
        info.stop_at = time.time() + self.args.late_session_min * 60

    def request_compaction(self) -> None:
        """After an update lands: each open session fires PreCompact on its next
        turn, through the hooks it started with (and the dispatcher's hand-over)."""
        asked = []
        for info in self.sessions:
            if info.process is not None and info.process.poll() is None and info.compact_file is not None:
                with contextlib.suppress(OSError):
                    info.compact_file.touch()
                    asked.append(info.label)
        self.event("compaction_requested", sessions=asked)

    def stop_due_sessions(self) -> None:
        for info in list(self.sessions):
            if info.stop_at and time.time() >= info.stop_at and not info.stop_file.exists():
                with contextlib.suppress(OSError):
                    info.stop_file.touch()
                self.event("late_session_stopping", session=info.label)

    def start_session(self, info: SessionInfo) -> None:
        if WINDOWS:
            bash = git_bash()
            shell = [bash, "-c"] if bash else ["cmd", "/c"]
        else:
            shell = ["/bin/sh", "-c"]
        post = None
        if info.daemon:
            # Stand-in for the daemon-profile plugin's SessionStart: this session's
            # switch reads `daemon`, so the tap's supervisor starts a worker for it.
            post = [str(self.tool_python), "-c",
                    "from probe.sdk import session_marker as m;"
                    f"m.mark_session_profile({info.sid!r}, 'daemon');"
                    f"print(m.set_session_state({info.sid!r}, 'daemon'))"]
        cfg = {
            "label": info.label, "sid": info.sid, "cwd": str(info.cwd), "transcript": str(info.transcript),
            "plugins": list(PLUGIN_IDS), "claude_config_dir": str(self.layout.claude),
            "env": self.session_env(info), "shell": shell,
            "turn_every_s": self.args.turn_every_s, "line_gap_s": self.args.line_gap_s,
            "probe_tool_every": 4, "compact_every": self.args.compact_every, "compact_file": str(info.compact_file),
            "stop_file": str(info.stop_file), "status_file": str(info.status_file),
            "hook_log": str(info.hook_log), "lines_log": str(info.lines_log), "tool_log": str(info.tool_log),
            "post_start": post,
        }
        write_json(info.config, cfg)
        interpreter = sys.executable if WINDOWS else str(self.layout.agents / "claude")
        with info.out_file.open("ab") as out:
            info.process = subprocess.Popen(
                [interpreter, str(HERE / "session_agent.py"), "--config", str(info.config)],
                stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT, cwd=str(info.cwd),
                env=self.session_env(info),
            )
        info.started_at = time.time()
        self.event("session_started", session=info.label, sid=info.sid, pid=info.process.pid, daemon=info.daemon)

    # -- 6. watching ---------------------------------------------------------------------

    def load_client(self) -> None:
        if not self.service_ok:
            return
        sys.path.insert(0, str(TAP_ROOT))
        try:
            from tap.service import client  # the checkout's copy of probe.service.client
            from tap.service.protocol import Client, Method
        except Exception as exc:  # noqa: BLE001
            self.harness_errors.append(f"cannot import the tap's service client: {exc!r}")
            self.service_ok = False
            return
        self.client = (client, Client, Method)

    def service_call(self, method_name: str, params: dict | None = None):
        if self.client is None:
            return None
        client, Client, Method = self.client
        try:
            return client.call(getattr(Method, method_name), params, client=Client.CLI, client_version="live-run")
        except Exception:  # noqa: BLE001 -- not running, restarting, or busy
            return None

    def tap_pid(self, info: SessionInfo, suffix: str = "pid") -> int | None:
        """The session's `tap watch` wrapper (`pid`), or the Probe service that
        records it itself (`hosted`, R2 plan A2)."""
        raw = None
        with contextlib.suppress(OSError):
            raw = (watcher_dir() / f"probe-research-tap-watcher-{info.sid}.{suffix}").read_text().strip()
        return int(raw) if raw and raw.isdigit() else None

    def sample(self) -> dict:
        now = time.time()
        status = self.service_call("STATUS") if self.service_ok else None
        listing = self.service_call("SESSION_LIST") if self.service_ok else None
        listed = {s.get("sid"): s for s in (listing or {}).get("sessions", []) if isinstance(s, dict)} \
            if isinstance(listing, dict) else {}
        uploads = self.state.snapshot()
        recorders = {r.get("sid"): r for r in (status or {}).get("recorders") or [] if isinstance(r, dict)}
        per = {}
        for info in self.sessions:
            st = read_json(info.status_file, {}) or {}
            batches = [b for b in (uploads.get(info.sid) or {}).get("batches", []) if b["status"] == "accepted"]
            lock = self.layout.probe_state / "daemon" / f"{info.sid}.lock"
            per[info.label] = {
                "lines": st.get("lines"),
                "phase": st.get("phase"),
                "agent_alive": info.process is not None and info.process.poll() is None,
                "uploaded_lines": batches[-1]["line_end"] if batches else 0,
                "last_batch_t": batches[-1]["t"] if batches else None,
                "batches": len(batches),
                "tap_pid": self.tap_pid(info),
                # The service holds the session's journal claim (its recorder row's
                # `recording`), and its `.hosted` marker names it: the hooks' fast
                # path reads the marker. A recorder thread merely alive (waiting
                # to try again while the session's own `tap watch` records) is not.
                "hosted": (recorders.get(info.sid) or {}).get("recording") is True
                and pid_alive(self.tap_pid(info, "hosted")),
                # Recorded at all: its `tap watch`, or a live recorder thread in the
                # service. Not the `.hosted` marker (`hosted` above keeps it): a
                # resumed recorder starts up to RESUME_SPREAD_S (20 s) after its
                # service and rewrites the marker only then, so each restart could
                # read as "not recorded" for two samples, and a daemon session's
                # two updates failed `recording.tap_alive` with 3 such samples.
                "tap_alive": pid_alive(self.tap_pid(info)) or bool((recorders.get(info.sid) or {}).get("alive")),
                # The service's own word, no marker: what `recording.hosted` reads on
                # Windows, where the `.hosted` marker and its pid are Git Bash's.
                "recorded_by_service": (recorders.get(info.sid) or {}).get("recording") is True,
                "listed": info.sid in listed,
                "listed_mode": (listed.get(info.sid) or {}).get("mode"),
                "worker_lock": flock_held(lock) if info.daemon else None,
            }
        entry = {
            "t": now,
            "min": round(self.minutes(), 2),
            "service": {k: status.get(k) for k in ("service_version", "pid", "state", "sessions")} if status else None,
            "update": (status or {}).get("update"),
            "recorders": len(recorders),
            "hook_hosts": len((status or {}).get("hook_hosts") or []),
            "barrier": (self.layout.machine_dir / "update.barrier").exists(),
            "sessions": per,
        }
        self.samples.append(entry)
        with contextlib.suppress(OSError), (self.layout.out / "samples.jsonl").open("a", encoding="utf-8") as h:
            h.write(json.dumps(entry) + "\n")
        return entry

    def monitor(self) -> None:
        last_line = 0.0
        while not self.stop.is_set():
            try:
                self.stop_due_sessions()
                entry = self.sample()
                service = entry["service"] or {}
                version = service.get("service_version")
                if version:
                    self.observed_cli.add(version)
                if time.time() - last_line >= 60:
                    last_line = time.time()
                    parts = [f"{k}:{v['uploaded_lines']}/{v['lines']}{'' if v['tap_alive'] else '(tap down)'}"
                             f"{'' if v['listed'] or not self.service_ok else '(unlisted)'}"
                             for k, v in entry["sessions"].items()]
                    update = entry["update"] or {}
                    log(f"watch: service {version} pid {service.get('pid')} {service.get('state')} | "
                        f"update {update.get('step') or ('running' if update.get('in_progress') else 'idle')}"
                        f"{' deferred ' + str((update.get('deferred') or {}).get('reason')) if update.get('deferred') else ''}"
                        f" | uploaded/written {' '.join(parts)}")
            except Exception as exc:  # noqa: BLE001
                log(f"monitor error: {exc!r}")
            self.stop.wait(self.args.poll_s)

    # -- 7. updates --------------------------------------------------------------------------

    def schedule(self) -> list[float]:
        if self.args.updates_at:
            return [float(x) for x in self.args.updates_at.split(",")][:2]
        if self.args.smoke:
            return [3.0, 7.0]
        d = self.args.duration_min
        if d < 60:
            return [1.5, 3.0]
        return [round(d * 0.2, 1), round(d * 0.55, 1)]

    def installed_now(self) -> str | None:
        """The CLI version installed in the uv tool env, read from its dist-info
        folder: no process, so polling it never meets the update barrier or reads
        files `uv` is replacing."""
        if self.tool_python is None:
            return None
        env_root = self.tool_python.parent.parent
        found = sorted(env_root.glob("lib/python*/site-packages/probe_research-*.dist-info")) + \
            sorted(env_root.glob("Lib/site-packages/probe_research-*.dist-info"))
        versions = [p.name[len("probe_research-"):-len(".dist-info")] for p in found]
        if len(versions) != 1:
            return None  # mid-install: none, or the old and the new side by side
        self.observed_cli.add(versions[0])
        return versions[0]

    def trigger(self, pub: Publication) -> str:
        if WINDOWS:
            done = self.run_cmd([self.layout.shim_probe, "wizard", "--action", "update", "--yes"], timeout=900,
                                label="probe wizard --action update")
            outcome = "ran" if done.returncode == 0 else f"exit {done.returncode}"
        else:
            done = self.run_cmd([self.layout.shim_probe, "service", "check-now", "--trigger", "cli"], timeout=120,
                                label="probe service check-now")
            text = (done.stdout or "") + (done.stderr or "")
            m = re.search(r"update check (\w+)(?: \(([^)]*)\))?", text)
            outcome = (m.group(1) + (f" ({m.group(2)})" if m.group(2) else "")) if m else \
                f"exit {done.returncode}: {text.strip()[:120]}"
        pub.checks.append({"min": round(self.minutes(), 2), "outcome": outcome})
        self.event("check_now", k=pub.k, outcome=outcome)
        return outcome

    def landed(self, pub: Publication) -> bool:
        version = self.installed_now()
        if version and version not in self.versions.cli and version not in self.foreign_seen:
            self.foreign_seen.add(version)
            self.event("foreign_version", version=version,
                       note="a CLI version that is not one of the run's own: the update child did not use the "
                            "private index (D11)")
        return version == pub.version

    def drive_updates(self, end_at: float) -> None:
        for k, at in zip((1, 2), self.schedule()):
            self.publications.append(Publication(k=k, version=self.versions.cli[k], scheduled_min=at))
        for i, pub in enumerate(self.publications):
            following = self.publications[i + 1] if i + 1 < len(self.publications) else None
            while not self.stop.is_set() and self.minutes() < pub.scheduled_min:
                self.stop.wait(5)
            if self.stop.is_set() or time.time() >= end_at:
                return
            if pub.k == 1 and self.args.autoupdate_at == "first-publish":
                self.enable_autoupdate()
            self.publish(pub.k)
            pub.published_at = time.time()
            next_try = 0.0
            while not self.stop.is_set() and time.time() < end_at:
                if following is not None and self.minutes() >= following.scheduled_min:
                    # Its successor is due: publish that one; this one may never land.
                    pub.superseded = True
                    self.event("superseded", k=pub.k, cli=pub.version)
                    break
                if time.time() >= next_try:
                    self.trigger(pub)
                    # Windows runs the whole update in the foreground each time: not every minute.
                    next_try = time.time() + (60 if not WINDOWS else 300)
                if self.landed(pub):
                    pub.landed_at = time.time()
                    self.event("landed", k=pub.k, cli=pub.version,
                               after_min=round((pub.landed_at - pub.published_at) / 60, 2),
                               ledger=self.ledger_versions())
                    self.request_compaction()
                    self.start_late_session(pub.k)
                    break
                self.stop.wait(15)

    # -- 8. the end ----------------------------------------------------------------------------

    def end_sessions(self) -> None:
        for info in self.sessions:
            with contextlib.suppress(OSError):
                info.stop_file.touch()
        deadline = time.time() + 240
        for info in self.sessions:
            if info.process is None:
                continue
            try:
                info.exit_code = info.process.wait(timeout=max(1.0, deadline - time.time()))
            except subprocess.TimeoutExpired:
                self.harness_errors.append(f"session {info.label} did not end within 4 min; killed")
                info.process.kill()
                info.exit_code = None  # killed: no exit of its own (`sessions.ran` fails it)
            info.ended_at = time.time()
        self.event("sessions_ended", exits={i.label: i.exit_code for i in self.sessions})

    def wait_final_uploads(self) -> None:
        deadline = time.time() + self.args.final_wait_s
        missing: dict = {"all": "not checked"}
        while time.time() < deadline:
            uploads = self.state.snapshot()
            missing = {}
            for info in self.sessions:
                st = read_json(info.status_file, {}) or {}
                batches = [b for b in (uploads.get(info.sid) or {}).get("batches", []) if b["status"] == "accepted"]
                done = batches[-1]["line_end"] if batches else 0
                if done < (st.get("lines") or 0) or not (batches and batches[-1]["finalize"]):
                    missing[info.label] = f"{done}/{st.get('lines')}{'' if batches and batches[-1]['finalize'] else ' unfinalized'}"
            if not missing:
                self.final_missing = {}
                self.event("final_uploads_complete")
                return
            time.sleep(5)
        self.final_missing = missing
        self.event("final_uploads_incomplete", missing=missing)

    def wait_service_exit(self) -> float | None:
        if not self.service_ok:
            return None
        started = time.time()
        while time.time() - started < 90:
            if self.service_call("STATUS") is None:
                return time.time() - started
            time.sleep(2)
        return None

    def our_pids(self) -> list[tuple[int, str]]:
        """Processes the run started: whose command line names one of this run's
        session ids (the tap wrappers and daemons, daemon workers), or whose
        program lives under this run's root (the service and anything else run
        from the scratch tool env, the session agents). Ids are fresh UUIDs and
        the root a fresh folder; a process that merely MENTIONS the root (a shell
        tailing its log) is not one of them."""
        sids = [info.sid for info in self.sessions]
        root = str(self.layout.root)
        found = []
        if WINDOWS:
            return found
        out = run_bounded(["ps", "-axww", "-o", "pid=,command="], timeout=30).stdout
        for line in out.splitlines():
            pid, _, command = line.strip().partition(" ")
            program = command.split(" ", 1)[0]
            if pid.isdigit() and int(pid) != os.getpid() and (
                    program.startswith(root) or any(sid in command for sid in sids)):
                found.append((int(pid), command[:300]))
        return found

    def cleanup(self) -> None:
        """Leave nothing of the run running: only processes the run started."""
        for info in self.sessions:
            with contextlib.suppress(OSError):
                info.stop_file.touch()
            if info.process is not None and info.process.poll() is None:
                with contextlib.suppress(OSError):
                    info.process.terminate()
            if not WINDOWS:
                with contextlib.suppress(OSError):
                    (watcher_dir() / f"probe-research-tap-watcher-{info.sid}.shutdown").touch()
        if self.service_ok and self.service_call("STATUS") is not None:
            self.run_cmd([self.layout.real_probe, "service", "stop"], timeout=60, label="probe service stop")
        if not WINDOWS:
            # A daemon worker finishes its queue after SIGTERM (bounded by
            # probe.daemon.worker.FINISH_CAP_S): give it a little, then stop it.
            for sig, wait in ((signal.SIGTERM, 15), (signal.SIGKILL, 1)):
                pids = self.our_pids()
                if not pids:
                    break
                if sig == signal.SIGTERM:
                    self.event("left_running_at_cleanup", processes=pids)
                if sig == signal.SIGKILL:
                    workers = [c for _p, c in pids if " daemon worker " in f" {c} "]
                    self.findings.append({
                        "id": "processes-left-running",
                        "what": "processes of the run still ran 15 s after SIGTERM at cleanup, and were killed"
                                + ("; among them the daemon worker, which after SIGTERM finishes its queue for up "
                                   "to probe.daemon.worker.FINISH_CAP_S (35 min) and keeps its session lock -- and "
                                   "with it any deferred update -- that long" if workers else ""),
                        "evidence": pids,
                    })
                for pid, _command in pids:
                    with contextlib.suppress(OSError):
                        os.kill(pid, sig)
                deadline = time.time() + wait
                while time.time() < deadline and any(pid_alive(pid) for pid, _ in pids):
                    time.sleep(0.5)
            for info in self.sessions:
                for suffix in ("pid", "version", "owner", "stopping", "shutdown", "hosted"):
                    with contextlib.suppress(OSError):
                        (watcher_dir() / f"probe-research-tap-watcher-{info.sid}.{suffix}").unlink()
        if self.server is not None:
            self.server.shutdown()

    def collect(self) -> None:
        L, out = self.layout, self.layout.out / "logs"
        out.mkdir(parents=True, exist_ok=True)
        M = L.machine_dir
        copies = [
            (M / "service.log", "service.log"),
            (M / "service.log.1", "service.log.1"),
            (M / "update.log", "update.log"),
            (M / "update.json", "service-update.json"),
            (M / "sessions.json", "service-sessions.json"),
            (M / "recorders.json", "service-recorders.json"),
            (M / "guard.json", "service-guard.json"),
            (L.probe_state / "autoupdate.json", "autoupdate.json"),
            (L.live / "claude-standin.jsonl", "claude-standin.jsonl"),
            (L.live / "probe-calls.jsonl", "probe-calls.jsonl"),
            (L.stub / "requests.jsonl", "stub-requests.jsonl"),
            (L.stub / "batches.jsonl", "stub-batches.jsonl"),
            (L.stub / "update-reports.jsonl", "stub-update-reports.jsonl"),
            (L.claude / "plugins" / "installed_plugins.json", "installed_plugins.json"),
        ]
        for src, name in copies:
            if src.is_file():
                shutil.copy2(src, out / name)
        for folder, prefix in ((L.tap_state / "logs", "tap-"), (L.probe_state / "daemon", "daemon-"), (L.run, "")):
            if folder.is_dir():
                for src in folder.iterdir():
                    if src.is_file() and src.suffix in (".log", ".jsonl", ".out", ".json"):
                        shutil.copy2(src, out / f"{prefix}{src.name}")

    # -- 9. checks ---------------------------------------------------------------------------------

    def checks(self, service_exit_s: float | None) -> list[dict]:
        results: list[dict] = []

        def add(check_id: str, status: str, detail: str, **data) -> None:
            results.append({"id": check_id, "status": status, "detail": detail, **data})

        uploads = self.state.snapshot()
        win_skip = "skipped (Windows, R1: no service there)"

        # every planned session started, did its work and exited 0 on its own: a session
        # that failed at startup reads as "0 written / 0 uploaded" in every other check
        ran_bad = []
        for info in self.sessions:
            st = read_json(info.status_file, {}) or {}
            problems = []
            if info.process is None:
                problems.append("never started")
            elif info.exit_code is None:
                problems.append("did not exit by itself (still running, or killed at the end)")
            elif info.exit_code != 0:
                problems.append(f"exited {info.exit_code}")
            if st.get("phase") != "ended":
                problems.append(f"last phase {st.get('phase')!r}, not 'ended'")
            if not st.get("turns") or not st.get("lines"):
                problems.append(f"no workload ({st.get('turns') or 0} turns, {st.get('lines') or 0} lines)")
            if problems:
                ran_bad.append(f"{info.label}: " + "; ".join(problems))
        add("sessions.ran", Check.FAIL if ran_bad else Check.PASS,
            "; ".join(ran_bad) or f"all {len(self.sessions)} sessions started, wrote their turns and exited 0")

        # recording: every line once, no gaps, no duplicates, markers where they belong
        complete_bad, marker_bad, per_session = [], [], {}
        for info in self.sessions:
            lines = read_jsonl(info.lines_log)
            written = len(lines)
            accepted = [b for b in (uploads.get(info.sid) or {}).get("batches", []) if b["status"] == "accepted"]
            dupes = [b for b in (uploads.get(info.sid) or {}).get("batches", []) if b["status"] == "duplicate"]
            cursor, problems = 0, []
            for b in sorted(accepted, key=lambda b: b["batch_seq"]):
                if b["line_start"] != cursor:
                    problems.append(f"batch {b['batch_seq']} starts at line {b['line_start']}, expected {cursor}")
                cursor = b["line_end"]
            if cursor != written:
                problems.append(f"uploaded lines end at {cursor}, {written} written")
            if not accepted:
                problems.append("no finalized stream: the server accepted nothing")
            elif not accepted[-1]["finalize"]:
                problems.append("the last batch is not final (the session end was not delivered)")
            if problems:
                complete_bad.append(f"{info.label}: " + "; ".join(problems[:5]))
            seen: dict = {}
            for b in accepted:
                for marker in set(b["markers"]):
                    seen.setdefault(marker, []).append(b)
            missing, twice, misplaced = [], [], []
            for line in lines:
                marker = line.get("marker")
                if not marker:
                    continue
                key = f"{info.label}:{line['n']}"
                found = seen.get(key) or []
                if not found:
                    missing.append(line["n"])
                elif len(found) > 1:
                    twice.append(line["n"])
                elif not (found[0]["line_start"] <= line["n"] < found[0]["line_end"]):
                    misplaced.append(line["n"])
            if missing or twice or misplaced:
                marker_bad.append(f"{info.label}: {len(missing)} missing (first {missing[:5]}), {len(twice)} in two "
                                  f"batches (first {twice[:5]}), {len(misplaced)} outside their batch's lines")
            per_session[info.label] = {"sid": info.sid, "lines_written": written, "batches": len(accepted),
                                       "duplicate_posts": len(dupes), "uploaded_lines": cursor,
                                       "markers": sum(1 for line in lines if line.get("marker")),
                                       "daemon": info.daemon}
        add("recording.complete", Check.FAIL if complete_bad else Check.PASS,
            "; ".join(complete_bad) or "every session's lines were accepted once, in order, with no gap or overlap, "
            "and each stream ended with its final batch", sessions=per_session)
        add("recording.markers_once", Check.FAIL if marker_bad else Check.PASS,
            "; ".join(marker_bad) or "every marked line's marker reached the server in exactly one accepted batch, "
            "inside that batch's line range")
        missing = self.final_missing
        add("recording.final_uploads", Check.FAIL if missing or missing is None else Check.PASS,
            "the final uploads were never waited for" if missing is None else
            (f"after {self.args.final_wait_s:.0f} s, still missing: "
             + "; ".join(f"{k} {v}" for k, v in missing.items()) if missing else
             "every session's last lines and its finalize landed after it ended"))
        add("ingest.no_violations", Check.FAIL if self.state.violations else Check.PASS,
            f"{len(self.state.violations)} protocol violation(s): {self.state.violations[:3]}"
            if self.state.violations else "no batch broke its stream (order, cursors, conflicting re-sends)")

        # recording kept flowing while sessions were live (catches a stall after an update)
        stall_s = self.args.stall_s
        stalls = []
        for info in self.sessions:
            last_progress_t, last_uploaded = None, -1
            for s in self.samples:
                v = s["sessions"].get(info.label) or {}
                if v.get("phase") != "running":
                    continue
                if last_progress_t is None or v["uploaded_lines"] != last_uploaded:
                    last_progress_t, last_uploaded = s["t"], v["uploaded_lines"]
                    continue
                behind = (v.get("lines") or 0) - (v.get("uploaded_lines") or 0)
                if behind > 0 and s["t"] - last_progress_t > stall_s:
                    stalls.append(f"{info.label}: no upload for {(s['t'] - last_progress_t) / 60:.1f} min at "
                                  f"+{s['min']} min ({behind} lines behind)")
                    last_progress_t = s["t"]
        add("recording.no_stall", Check.FAIL if stalls else Check.PASS,
            "; ".join(stalls[:6]) or f"no live session went more than {stall_s / 60:.0f} min without an upload "
            "while it had lines to send")

        # taps survived (informational in detail, failure if a tap died and was not replaced)
        tap_down = []
        for info in self.sessions:
            downs = [s["min"] for s in self.samples
                     if (s["sessions"].get(info.label) or {}).get("phase") == "running"
                     and not (s["sessions"].get(info.label) or {}).get("tap_alive")]
            if len(downs) > 2:
                tap_down.append(f"{info.label}: tap watcher not running in {len(downs)} samples (first +{downs[0]} min)")
        if WINDOWS:
            add("recording.tap_alive", Check.SKIP, "skipped (Windows: the wrapper's pid file holds a Git Bash pid)")
        else:
            add("recording.tap_alive", Check.FAIL if tap_down else Check.PASS,
                "; ".join(tap_down) or "each session was recorded the whole session (its `tap watch` wrapper, "
                "or the Probe service)")
        # R2 (plan A2), R3 on Windows: the service records every session itself, its
        # own restarts (updates, a newer tap) included; `tap watch` only where it
        # cannot. POSIX reads the recorder AND its `.hosted` marker (what the hooks'
        # fast path reads); Windows the service's recorders alone (the marker's pid
        # is a Git Bash one there).
        if self.args.expect_hosted:
            field = "recorded_by_service" if WINDOWS else "hosted"
            unhosted = []
            for info in self.sessions:
                running = [s for s in self.samples
                           if (s["sessions"].get(info.label) or {}).get("phase") == "running"]
                hosted = [s for s in running if (s["sessions"].get(info.label) or {}).get(field)]
                if running and len(hosted) < 0.8 * len(running):
                    unhosted.append(f"{info.label}: recorded by the service in {len(hosted)} of "
                                    f"{len(running)} running samples")
            add("recording.hosted", Check.FAIL if unhosted else Check.PASS,
                "; ".join(unhosted) or "every session was recorded by the Probe service itself (no `tap watch`)")

        # hooks
        hooks = [r for info in self.sessions for r in read_jsonl(info.hook_log)]
        bad = [r for r in hooks if r.get("exit") != 0 or r.get("timed_out")]
        by_event: dict = {}
        for r in hooks:
            key = f"{r['event']} {r['plugin'].split('@')[0]}"
            agg = by_event.setdefault(key, {"runs": 0, "max_s": 0.0, "durations": [], "timeout_s": r["timeout_s"],
                                            "bad": 0, "versions": set()})
            agg["runs"] += 1
            agg["durations"].append(r["duration_s"])
            agg["max_s"] = max(agg["max_s"], r["duration_s"])
            agg["bad"] += int(r.get("exit") != 0 or bool(r.get("timed_out")))
            agg["versions"].add(r.get("version"))
        table = {}
        for key, agg in sorted(by_event.items()):
            durations = sorted(agg["durations"])
            table[key] = {"runs": agg["runs"], "bad": agg["bad"], "timeout_s": agg["timeout_s"],
                          "p50_s": durations[len(durations) // 2], "p95_s": durations[int(len(durations) * 0.95)],
                          "max_s": round(agg["max_s"], 3), "plugin_versions": sorted(v for v in agg["versions"] if v)}
        detail = (f"{len(bad)} of {len(hooks)} hook runs failed or ran past their timeout; first: "
                  + "; ".join(f"{r['session']} {r['event']} {r['plugin'].split('@')[0]} exit {r.get('exit')}"
                              f"{' TIMEOUT' if r.get('timed_out') else ''} {r['duration_s']}s "
                              f"{(r.get('stderr_tail') or '').strip()[-160:]!r}" for r in bad[:4])) if bad else \
            f"all {len(hooks)} hook runs exited 0 within their timeout"
        add("hooks.ok", Check.FAIL if bad else Check.PASS, detail, by_event=table)
        # Coverage against what each session LOADED (its plugins' hooks.json at its
        # start), plugin by plugin: never a hardcoded event list, which left out
        # PreCompact (an `exit 42` there passed both hook checks).
        fired = {r["event"] for r in hooks}
        uncovered = []
        for info in self.sessions:
            loaded = (read_json(info.status_file, {}) or {}).get("plugins") or []
            if not loaded:
                uncovered.append(f"{info.label}: loaded no plugin's hooks")
            ran = {(r["plugin"], r["event"]) for r in hooks if r.get("session") == info.label}
            for plugin in loaded:
                never = sorted(e for e in plugin.get("events") or [] if (plugin["id"], e) not in ran)
                if never:
                    uncovered.append(f"{info.label} {plugin['id'].split('@')[0]}: never fired {never}")
        add("hooks.fired", Check.FAIL if uncovered else Check.PASS,
            "; ".join(uncovered[:8]) or f"every event each session's loaded hooks.json declares ran, plugin by "
            f"plugin: {sorted(fired)}")
        self.handover_check(add)
        session_end_slow = [r for r in hooks if r["event"] == "SessionEnd" and r["duration_s"] > 1.5]
        if session_end_slow:
            self.findings.append({
                "id": "session-end-over-claude-phase-cap",
                "what": f"{len(session_end_slow)} SessionEnd hook run(s) took longer than Claude Code's 1.5 s "
                        "SessionEnd phase (CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS default); Claude Code would "
                        "cancel them there",
                "evidence": [f"{r['plugin'].split('@')[0]} {r['duration_s']}s" for r in session_end_slow[:6]],
            })

        # probe calls and the update barrier
        calls = [c for c in read_jsonl(self.layout.live / "probe-calls.jsonl") if "duration_s" in c]
        # A call already detached when it started (its parent is init: a hook's
        # background `notes sync --push-only`, double-forked) holds no agent up,
        # so its wait at the barrier is no budget overrun; it is counted apart.
        detached = [c for c in calls if c.get("ppid") == 1]
        over = [c for c in calls if c.get("barrier_at_start") and c["duration_s"] > BARRIER_WAIT_S + 5
                and c.get("ppid") != 1]
        busy = [c for c in calls if c.get("exit") == 75]
        long = sorted(calls, key=lambda c: -c["duration_s"])[:5]
        if WINDOWS:
            add("probe.barrier_budget", Check.SKIP, "skipped (Windows: the PATH shim cannot stand in front of "
                "probe.exe for Git Bash)")
        else:
            add("probe.barrier_budget", Check.FAIL if over else Check.PASS,
                (f"{len(over)} probe call(s) that met the update barrier ran past its {BARRIER_WAIT_S:.0f} s budget: "
                 + "; ".join(f"{' '.join(c['argv'][:3])} {c['duration_s']}s exit {c.get('exit')}" for c in over[:4]))
                if over else f"{len(calls)} probe calls; {sum(1 for c in calls if c.get('barrier_at_start'))} met the "
                f"update barrier and none an agent waited on ran past {BARRIER_WAIT_S:.0f} s ({len(detached)} detached "
                f"background calls not counted); {len(busy)} were turned away (exit 75)",
                slowest=[{"argv": c["argv"][:4], "s": c["duration_s"], "exit": c.get("exit"),
                          "barrier": c.get("barrier_at_start")} for c in long])
        tools = [t for info in self.sessions for t in read_jsonl(info.tool_log) if "probe" in t["command"]]
        tool_bad = [t for t in tools if t.get("exit") not in (0,)]
        if tool_bad:
            self.findings.append({
                "id": "probe-from-a-session-failed",
                "what": f"{len(tool_bad)} of {len(tools)} `probe --version` runs from inside a session's Bash tool "
                        "did not exit 0",
                "evidence": [f"{t['session']} +{(t['t'] - self.t_sessions) / 60:.1f}m exit {t.get('exit')} "
                             f"{t['duration_s']}s {t['output_tail'][-120:]!r}" for t in tool_bad[:5]],
            })

        # the service: sessions registered, final version, idle exit
        if not self.service_ok:
            for check_id in ("service.sessions_registered", "service.final_version", "service.idle_exit"):
                add(check_id, Check.SKIP, win_skip)
        else:
            gaps = []
            for info in self.sessions:
                streak_start, worst = None, 0.0
                live = [s for s in self.samples if (s["sessions"].get(info.label) or {}).get("phase") == "running"]
                for s in live[2:]:
                    if (s["sessions"][info.label] or {}).get("listed"):
                        streak_start = None
                        continue
                    streak_start = streak_start or s["t"]
                    worst = max(worst, s["t"] - streak_start + self.args.poll_s)
                if worst > self.args.unlisted_s:
                    gaps.append(f"{info.label}: not listed by session.list for {worst:.0f} s")
            add("service.sessions_registered", Check.FAIL if gaps else Check.PASS,
                "; ".join(gaps) or f"every running session stayed listed by the service (no gap over "
                f"{self.args.unlisted_s:.0f} s, service restarts included)")
            last = next((s["service"] for s in reversed(self.samples) if s.get("service")), None)
            final = (last or {}).get("service_version")
            add("service.final_version", Check.PASS if final == self.versions.cli[2] else Check.FAIL,
                f"the service last ran {final}, expected {self.versions.cli[2]}")
            add("service.idle_exit", Check.PASS if service_exit_s is not None else Check.FAIL,
                f"the service exited {service_exit_s:.0f} s after the last session ended" if service_exit_s is not None
                else "the service was still running 90 s after the last session ended")

        # installed versions, the channel, the updates themselves
        final_cli = self.cli_version(via_shim=False)
        ledger = self.ledger_versions()
        want = {"cli": self.versions.cli[2], MAIN_PLUGIN: self.versions.plugin[2], TAP_PLUGIN: self.versions.tap[2]}
        have = {"cli": final_cli, MAIN_PLUGIN: ledger.get(MAIN_PLUGIN), TAP_PLUGIN: ledger.get(TAP_PLUGIN)}
        add("install.final_versions", Check.PASS if have == want else Check.FAIL,
            f"installed {have}, expected {want}")
        if self.args.expect_side_by_side:
            # R2 (plan D5, D6): each CLI update installed beside the running one and
            # switched the tool path; the guard watched the last switch and kept it.
            tool = Path(self.tool_python).parent.parent
            target = tool.resolve() if tool.is_symlink() else None
            guard = read_json(self.layout.machine_dir / "guard.json", {}) or {}
            ok = (target is not None and target.parent.name == self.versions.cli[2]
                  and guard.get("ok") is True and guard.get("to") == self.versions.cli[2])
            add("install.side_by_side", Check.PASS if ok else Check.FAIL,
                f"the tool path names {target or 'a plain folder'}; the guard says {guard or 'nothing'}")
        foreign = sorted(v for v in self.observed_cli if v not in self.versions.cli)
        add("install.local_channel_only", Check.FAIL if foreign else Check.PASS,
            (f"CLI version(s) {foreign} appeared: the update did not come from the run's private index. The "
             "service's update child runs with a clean env (ENV_ALLOWLIST) and did not see UV_INDEX "
             "(D11; also: the updater's restating `uv tool install` drops the receipt's [tool.options] index)")
            if foreign else f"every CLI version seen was one of the run's own ({sorted(self.observed_cli)})")
        later_landed = {p.k for p in self.publications if p.landed_at}
        not_landed = [p for p in self.publications if p.published_at and not p.landed_at
                      and not (p.superseded and any(k > p.k for k in later_landed))]
        never = [p for p in self.publications if not p.published_at]
        slow = [p for p in self.publications if p.landed_at and p.published_at
                and p.landed_at - p.published_at > CHECK_NOW_COOLDOWN_S + self.args.update_slack_s]
        lines = []
        for p in self.publications:
            outcomes = ", ".join(f"+{c['min']}m {c['outcome']}" for c in p.checks[:8])
            if p.landed_at:
                lines.append(f"{p.version} landed {(p.landed_at - p.published_at) / 60:.1f} min after it was "
                             f"published ({outcomes})")
            elif p.published_at and p.superseded and any(k > p.k for k in later_landed):
                lines.append(f"{p.version} was superseded by the next release before it landed ({outcomes})")
            elif p.published_at:
                lines.append(f"{p.version} NEVER landed ({outcomes})")
            else:
                lines.append(f"{p.version} was never published (the run ended first)")
        failed = bool(not_landed or never or slow)
        add("update.applied", Check.FAIL if failed else Check.PASS, "; ".join(lines),
            publications=[p.__dict__ for p in self.publications])
        deferred = [s["update"]["deferred"] for s in self.samples if (s.get("update") or {}).get("deferred")]
        if deferred:
            reasons = sorted({str((d or {}).get("reason")) for d in deferred})
            self.findings.append({
                "id": "update-deferred",
                "what": f"the service reported the update deferred in {len(deferred)} samples, reasons {reasons}",
                "evidence": deferred[:3],
            })

        self.cycle_findings()

        # the daemon session
        daemon = [i for i in self.sessions if i.daemon]
        if not daemon:
            add("daemon.worker", Check.SKIP, "no daemon session (--daemon-session none)")
        elif WINDOWS:
            add("daemon.worker", Check.SKIP, "skipped (Windows: no fcntl lock to observe)")
        else:
            info = daemon[0]
            running = [s for s in self.samples if (s["sessions"].get(info.label) or {}).get("phase") == "running"]
            held = [s for s in running if (s["sessions"].get(info.label) or {}).get("worker_lock")]
            last_landed = max((p.landed_at for p in self.publications if p.landed_at), default=None)
            after = [s for s in held if last_landed and s["t"] > last_landed]
            ok = bool(held) and (last_landed is None or bool(after))
            add("daemon.worker", Check.PASS if ok else Check.FAIL,
                f"a worker held {info.label}'s session lock in {len(held)} of {len(running)} running samples"
                + (f"; {len(after)} of them after the last update landed" if last_landed else
                   "; no update landed, so no restart on new code could be seen"),
                mode=self.args.daemon_session, model_calls=self.state.model_calls)

        if self.state.unhandled:
            self.findings.append({"id": "stub-unhandled-routes",
                                  "what": "API routes the stub answered generically (not part of any check)",
                                  "evidence": dict(sorted(self.state.unhandled.items())[:30])})
        return results

    def handover_check(self, add) -> None:
        """After each plugin update, an open session's prompt hooks must run the
        newly installed plugin (Claude Code's `hand_over`), though Claude Code
        keeps the session on the hooks.json and CLAUDE_PLUGIN_ROOT it started with."""
        if not self.args.canary_route:
            add("hooks.handover", Check.SKIP, "no canary route (--no-canary-route)")
            return
        canary = []
        try:
            for line in (self.layout.home / CANARY_LOG).read_text(encoding="utf-8").splitlines():
                t, sid, root = (line.split(" ", 2) + ["", ""])[:3]
                canary.append((float(t), sid, Path(root.strip()).name))
        except (OSError, ValueError):
            pass
        landed = [p for p in self.publications if p.landed_at]
        if not canary:
            add("hooks.handover", Check.FAIL, "the canary route never ran: no prompt hook ran the plugin's routes")
            return
        if not landed:
            add("hooks.handover", Check.SKIP, "no update landed, so no hand-over could be seen")
            return
        bad, seen = [], []
        for info in self.sessions:
            if info.label.startswith("n"):
                continue
            for pub in landed:
                wanted = self.versions.plugin[pub.k]
                after = [c for c in canary if c[1] == info.sid and c[0] > pub.landed_at + 2]
                if not after:
                    continue
                first = after[0]
                rank = self.versions.plugin.index(first[2]) if first[2] in self.versions.plugin else -1
                if rank < pub.k:
                    bad.append(f"{info.label}: its first prompt after {wanted} landed ran {first[2] or 'no folder'}")
                else:
                    seen.append(f"{info.label}->{first[2]}")
        add("hooks.handover", Check.FAIL if bad else Check.PASS,
            "; ".join(bad) or "after every plugin update, each open session's next prompt ran the installed "
            f"version's routes, not the one it started with ({', '.join(seen[:6])}); the tap plugin's own hooks "
            "have no hand-over and keep the version a session started with")

    def cycle_findings(self) -> None:
        """What the service said about its own update cycles, against what the
        update child reported to the server and the versions it moved between."""
        cycles = {}
        for s in self.samples:
            last = (s.get("update") or {}).get("last_result")
            if isinstance(last, dict) and last.get("cycle_id"):
                cycles[last["cycle_id"]] = last
        reports = []
        for line in read_jsonl(self.layout.stub / "update-reports.jsonl"):
            reports.append(line)
        failed_reports = [r for r in reports if r.get("outcome") == "failed"]
        ok_cycles = [c for c in cycles.values() if c.get("ok")]
        if failed_reports and ok_cycles:
            self.findings.append({
                "id": "cycle-ok-while-update-failed",
                "what": f"{len(failed_reports)} update report(s) to the server said `failed`, while the service "
                        f"recorded {len(ok_cycles)} cycle(s) as ok (`update.status` last_result.ok): a CLI left "
                        "behind its target reads as a good update on the machine",
                "evidence": [{"report_cli": r.get("cli")} for r in failed_reports[:2]]
                + [{"cycle": c.get("cycle_id"), "steps": c.get("steps")} for c in ok_cycles[:2]],
            })
        for c in cycles.values():
            step = (c.get("steps") or {}).get("self") or {}
            before, after = step.get("from_version"), step.get("to_version")
            if before and after and before != after and self._older(after, before):
                self.findings.append({
                    "id": "service-restarted-into-an-older-cli",
                    "what": f"the update cycle installed {after} over {before} (a downgrade) and the service "
                            "restarted into it: nothing checks that the version it switches to is newer",
                    "evidence": {"cycle": c.get("cycle_id"), "self": step},
                })

    @staticmethod
    def _older(a: str, b: str) -> bool:
        def key(v: str):
            return tuple(int(x) for x in re.findall(r"\d+", v)[:3])
        try:
            return key(a) < key(b)
        except ValueError:
            return False

    # -- 10. report ----------------------------------------------------------------------------------

    def report(self, results: list[dict], started: float, *, partial: str | None = None) -> int:
        """Write report.json and summary.txt; the exit code. `partial`: the watchdog
        writes it, and names the end-phase step the run never left."""
        failed = [r for r in results if r["status"] == Check.FAIL]
        meta = {
            "result": "fail" if failed or self.harness_errors else "pass",
            "partial": f"written by the watchdog: the end phase hung in `{partial}`" if partial else None,
            "os": f"{platform.system()} {platform.release()} ({platform.machine()})",
            "python": sys.version.split()[0],
            "uv": (run_bounded([self.uv, "--version"], timeout=30).stdout or "").strip()
            if self.uv else None,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "wall_min": round((time.time() - started) / 60, 1),
            "session_min": round(self.minutes(), 1),
            "args": vars(self.args),
            "versions": {"cli": self.versions.cli, "plugin": self.versions.plugin, "tap": self.versions.tap},
            "updates_at_min": self.schedule(),
            "service_checks": "on" if self.service_ok else "skipped (Windows, R1)",
            "stand_ins": {
                "claude_code_sessions": "session_agent.py (scripted turns, real hooks.json entries, no model)",
                "claude_plugin_manager": "standin_claude.py (local marketplace folder)",
                "daemon_worker": {"real": "real `probe daemon worker`; the stub's model gateway answers 503",
                                  "standin": "lock-holding stand-in worker (probe_shim.py)",
                                  "none": "no daemon session"}[self.args.daemon_session],
                "probe_api_and_index": "in-process stub on 127.0.0.1",
            },
            "index_via": self.args.index_via,
            "root": str(self.layout.root),
        }
        report = {"meta": meta, "checks": results, "findings": self.findings, "harness_errors": self.harness_errors,
                  "events": self.events, "stub_routes": self.state.counts if self.state else {}}
        write_json(self.layout.out / "report.json", report)
        mark = {Check.PASS: "PASS", Check.FAIL: "FAIL", Check.SKIP: "skip"}
        lines = [
            f"Probe live run: {meta['result'].upper()}{f' (PARTIAL: the end phase hung in {partial})' if partial else ''}"
            f"  ({meta['os']}, {meta['session_min']} min of sessions, {len(self.sessions)} sessions)",
            f"versions N/N+1/N+2: CLI {', '.join(self.versions.cli)}; plugin {', '.join(self.versions.plugin)}; "
            f"tap {', '.join(self.versions.tap)}",
            f"updates published at +{self.schedule()} min; index via {self.args.index_via}; daemon session: "
            f"{self.args.daemon_session}; service checks: {meta['service_checks']}",
            "",
        ]
        for r in results:
            lines.append(f"[{mark[r['status']]}] {r['id']}: {r['detail']}")
        if self.findings:
            lines += ["", "Findings:"]
            for f in self.findings:
                lines.append(f"  - {f['id']}: {f['what']}")
        if self.harness_errors:
            lines += ["", "Harness errors:"] + [f"  - {e}" for e in self.harness_errors]
        complete = next((r for r in results if r["id"] == "recording.complete"), None)
        if complete and complete.get("sessions"):
            lines += ["", "Sessions (lines written / uploaded, batches, re-sent duplicates):"]
            for label, row in complete["sessions"].items():
                lines.append(f"  {label:4} {row['lines_written']:6} / {row['uploaded_lines']:6}  {row['batches']:4} "
                             f"batches  {row['duplicate_posts']:3} dup{'  (daemon mode)' if row['daemon'] else ''}")
        hooks = next((r for r in results if r["id"] == "hooks.ok"), None)
        if hooks and hooks.get("by_event"):
            lines += ["", "Hooks (runs / bad / p50 / p95 / max s, timeout):"]
            for key, row in hooks["by_event"].items():
                lines.append(f"  {key:38} {row['runs']:5} {row['bad']:3} {row['p50_s']:6.2f} {row['p95_s']:6.2f} "
                             f"{row['max_s']:6.2f}  ({row['timeout_s']:.0f}s) {row['plugin_versions']}")
        lines += ["", f"report: {self.layout.out / 'report.json'}"]
        text = "\n".join(lines) + "\n"
        (self.layout.out / "summary.txt").write_text(text, encoding="utf-8")
        print("\n" + text, flush=True)
        if self.harness_errors:
            return 2
        return 1 if failed else 0

    # -- the end phase's watchdog ----------------------------------------------------------------------

    def step(self, name: str) -> None:
        """The end phase is at `name` now: what the watchdog names if it never leaves."""
        self.end_step = name
        log(f"end phase: {name}")

    def end_budget_s(self) -> float:
        """`--end-budget-min`, never less than the end phase's own bounded waits
        (a longer `--final-wait-s` is a longer healthy end, not a hang)."""
        waits = 240 + self.args.final_wait_s + 90 + 30 + 76 + 120
        return max(self.args.end_budget_min * 60, waits)

    def begin_end_phase(self, started: float) -> None:
        """Arm the watchdog (once): the sessions are ending, or the run failed."""
        if self._watchdog is not None:
            return
        self._watchdog = threading.Thread(target=self.end_watchdog, args=(started, self.end_budget_s()),
                                          name="end-watchdog", daemon=True)
        self._watchdog.start()

    def end_watchdog(self, started: float, budget_s: float) -> None:
        """Bound the end phase: past `budget_s`, say which step it is stuck in, write
        the report from what the run has (marked partial, a harness error), exit 2.

        Its own bounded waits add up to about 11.5 min (`--end-budget-min` is 15):
        the sessions ending (4 min), their last uploads (`--final-wait-s`, 4 min),
        the service's exit (90 s), the monitor (30 s), cleanup (its service stop
        60 s, then 16 s), the copies and the report. Past all of them a step hangs:
        a Windows run (39880360841) sat 20+ min after `final_uploads_complete` with
        every session exited and the service healthy, and the job died with no report."""
        if self.end_done.wait(budget_s):
            return
        # The main thread writes its report holding the lock: a report that is
        # only slow finishes (and wins); one stuck past a minute more is a hang.
        locked = self._report_lock.acquire(timeout=60)
        if self.end_done.is_set():
            if locked:
                self._report_lock.release()
            return
        step = self.end_step or "(before the end phase)"
        what = (f"the end phase was still in `{step}` after {budget_s / 60:g} min: the watchdog wrote this "
                "report from what the run had, and exited")
        log(f"watchdog: {what}")
        self.harness_errors.append(what)
        with contextlib.suppress(Exception):
            self.event("end_phase_overran", step=step, after_min=round(budget_s / 60, 1))
        code = 2
        with contextlib.suppress(Exception):
            code = self.report(list(self.results), started, partial=step) or 2
        if step not in ("collect", "report"):
            # The logs too, unless the main thread got to them: bounded, after the report.
            copier = threading.Thread(target=self._collect_quietly,
                                      name="watchdog-collect", daemon=True)
            copier.start()
            copier.join(60)
        os._exit(code)

    def _collect_quietly(self) -> None:
        with contextlib.suppress(Exception):
            self.collect()

    # -- main -------------------------------------------------------------------------------------------

    def main(self) -> int:
        global _log_file
        started = time.time()
        L = self.layout
        L.make()
        _log_file = L.out / "driver.log"
        log(f"root {L.root}; out {L.out}")
        if not self.uv:
            raise RuntimeError("uv is not on PATH")
        results: list[dict] = []
        try:
            self.start_stub()
            self.build_wheels()
            self.build_plugin_trees()
            self.publish(0)
            self.write_shims()
            self.write_login_profiles()
            # From here the driver itself is the scratch user (its own service calls
            # find the scratch HOME's service).
            os.environ["HOME"] = str(L.home)
            if WINDOWS:
                # And where the service's folder and pipe name come from there.
                os.environ.update({"USERPROFILE": str(L.home), "APPDATA": str(L.home / "AppData" / "Roaming"),
                                   "LOCALAPPDATA": str(L.home / "AppData" / "Local")})
            self.install_cli()
            self.configure()
            self.load_client()
            self.make_sessions()
            self.t_sessions = time.time()
            for info in self.sessions:
                self.start_session(info)
                time.sleep(3)
            self.monitor_thread = threading.Thread(target=self.monitor, name="monitor", daemon=True)
            self.monitor_thread.start()
            end_at = self.t_sessions + self.duration_s()
            self.drive_updates(end_at)
            while not self.stop.is_set() and time.time() < end_at:
                self.stop.wait(5)
            self.begin_end_phase(started)
            self.step("end_sessions")
            self.end_sessions()
            self.step("wait_final_uploads")
            self.wait_final_uploads()
            self.step("wait_service_exit")
            service_exit_s = self.wait_service_exit()
            self.stop.set()
            self.step("monitor_join")
            if self.monitor_thread:
                self.monitor_thread.join(timeout=30)
            self.step("sample")
            self.sample()
            self.step("checks")
            results = self.results = self.checks(service_exit_s)
        except Exception as exc:  # noqa: BLE001
            self.harness_errors.append(f"{type(exc).__name__}: {exc}")
            log(traceback.format_exc())
        finally:
            self.begin_end_phase(started)
            self.stop.set()
            self.step("cleanup")
            with contextlib.suppress(Exception):
                self.cleanup()
            self.step("collect")
            with contextlib.suppress(Exception):
                self.collect()
        self.step("report")
        with self._report_lock:
            code = self.report(results, started)
            self.end_done.set()
        if not self.args.keep:
            for heavy in (L.cache, L.data / "uv", L.build):
                shutil.rmtree(heavy, ignore_errors=True)
        return code

    def duration_s(self) -> float:
        return (self.args.duration_min or (22 if self.args.smoke else 300)) * 60


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--duration-min", type=float, default=None,
                        help="minutes the sessions run (default 300; 22 with --smoke)")
    parser.add_argument("--smoke", action="store_true",
                        help="a short local run: updates published at 3 and 7 min. The second applies once the "
                             "service's 15-min check_now cooldown has passed (~18 min), so the run lasts 22 min")
    parser.add_argument("--updates-at", default=None,
                        help="minutes at which N+1 and N+2 are published, e.g. 60,165")
    parser.add_argument("--expect-hosted", action="store_true",
                        help="R2: fail unless the Probe service recorded the sessions itself (plan A2)")
    parser.add_argument("--expect-side-by-side", action="store_true",
                        help="R2: fail unless each update installed beside the running CLI, guarded (D5, D6)")
    parser.add_argument("--sessions", type=int, default=3, help="stand-in sessions (default 3)")
    parser.add_argument("--daemon-session", choices=("real", "standin", "none"), default="real",
                        help="run the last session in daemon mode with the real worker (default), a lock-holding "
                             "stand-in worker, or not at all")
    parser.add_argument("--index-via", choices=("login-shell", "uv-config"), default="login-shell",
                        help="how the private index is selected (see the module docstring)")
    parser.add_argument("--autoupdate-at", choices=("start", "first-publish"), default=None,
                        help="when automatic updates are switched on (default: start for runs of 60 min or more, "
                             "else at the first publish, so the 15-min check_now cooldown fits a short run)")
    parser.add_argument("--late-session-min", type=float, default=2.0,
                        help="after each update lands, a new session runs this long (0: none)")
    parser.add_argument("--turn-every-s", type=float, default=20.0, help="seconds between a session's turns")
    parser.add_argument("--compact-every", type=int, default=10,
                        help="a session fires PreCompact on its 2nd turn and every this many turns (and after "
                             "each update lands)")
    parser.add_argument("--line-gap-s", type=float, default=2.5, help="mean seconds between transcript lines")
    parser.add_argument("--tap-interval", type=int, default=None,
                        help="the tap's sync_interval_seconds (default: the tap's own cadence, 60 s active)")
    parser.add_argument("--poll-s", type=float, default=10.0, help="seconds between the driver's samples")
    parser.add_argument("--stall-s", type=float, default=300.0,
                        help="a live session with lines to send and no upload for this long fails recording.no_stall")
    parser.add_argument("--unlisted-s", type=float, default=90.0,
                        help="a running session missing from session.list for longer fails the check")
    parser.add_argument("--update-slack-s", type=float, default=600.0,
                        help="an update may land at most the 15-min cooldown plus this after it was published")
    parser.add_argument("--final-wait-s", type=float, default=240.0,
                        help="how long to wait for the sessions' final uploads after they end")
    parser.add_argument("--end-budget-min", type=float, default=15.0,
                        help="the end phase (sessions ending through the report) may take this long (never less "
                             "than its own waits, --final-wait-s included); past it a watchdog writes the report "
                             "from what the run has, marked partial, and exits 2")
    parser.add_argument("--python", default=None,
                        help="the Python the CLI's uv tool env is built on (default: the one running this)")
    parser.add_argument("--port", type=int, default=0, help="the stub's port (default: any free one)")
    parser.add_argument("--root", default=None, help="scratch root (default: a new temp dir)")
    parser.add_argument("--out", default=None, help="where the report and logs go (default: <root>/out)")
    parser.add_argument("--keep", action="store_true", help="keep the uv cache, tool env and builds")
    parser.add_argument("--no-canary-route", dest="canary_route", action="store_false",
                        help="do not add the hand-over canary route to the built plugin trees")
    parser.add_argument("--no-windows-python3-shim", dest="windows_python3_shim", action="store_false",
                        help="on Windows, do not stand in a `python3` for the hooks when the machine has none")
    args = parser.parse_args(argv)
    if args.compact_every < 1:
        parser.error("--compact-every must be at least 1: every plugin that declares PreCompact is held to it")
    if WINDOWS and args.daemon_session == "standin":
        # The stand-in worker holds its lock with fcntl (probe_shim.py), which Windows has not.
        parser.error("--daemon-session standin needs fcntl: on Windows use real or none")
    if args.duration_min is None:
        args.duration_min = 22.0 if args.smoke else 300.0
    if args.autoupdate_at is None:
        args.autoupdate_at = "start" if args.duration_min >= 60 else "first-publish"
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run = Run(args)

    def interrupted(signum, _frame):
        log(f"signal {signum}: ending the run")
        run.stop.set()

    for name in ("SIGTERM", "SIGINT"):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), interrupted)
    try:
        return run.main()
    except Exception:  # noqa: BLE001
        log(traceback.format_exc())
        return 2


if __name__ == "__main__":
    sys.exit(main())
