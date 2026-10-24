"""The debug log: one zip with what it takes to debug how Probe works with the agent.

`probe doctor --bundle` builds it (and `--send` sends it): the desktop app's
"Send a debug log" row runs `probe doctor --bundle --send --json` and reads the
last stdout line (plan B9; the contract's "CLI output the app reads"). It is
`probe.core.report`'s LOCAL scope: the same readers and the same scrubber as
the staff report, with whole files and more sources.

    README.txt   when and where it was made, versions, what each folder holds,
                 the sources that were skipped and why, what was trimmed
    probe/       `probe doctor`, `probe status --json`, the CLI config (tokens
                 redacted), auto-update and install records, run locks, the
                 outbox's counts, `which -a probe`, `uv tool list`
    service/     the Probe service's folder (logs, guard, last stop, registry,
                 recorders, starts, updater), its actions' logs, the keeper's
                 units, and the live `service.status` / `session.list` answers
                 when the service replies within 2 s
    sessions/    every live session and the 10 most recent others: worker log
                 and output, lease, switch, lock, cursors, tap logs, tap
                 offsets and outbox COUNTS -- never a store, a trace or a message
    daemon/      `daemon-errors.log`, the stop journal, the daemon's settings
    agents/      per coding agent: its version, its config files whole
                 (credential files are listed, never read), the Probe plugins'
                 manifests and hooks, each recent transcript by path, size,
                 time, line count, last event type and model -- never its
                 content -- and each recent project's settings
    system/      OS, kernel, CPUs, load, memory, disks, uptime, container,
                 locale, limits; the environment of this command, of the
                 service and of each live agent process; Probe's processes
    network/     the base URL's DNS answer, a timed `GET /v1/client-version`,
                 which proxy variables are set

REDACTION, every file: the credential scanner and the SDK scrubber over all
text; every value under a credential-like name (`report.CREDENTIAL_NAME`) in
every config and every environment, header values (names kept), OAuth and
account blocks dropped whole, prompt history dropped; a config that does not
parse whole is listed, never copied; command lines keep only the program and
flag names (`report.redact_argv`: every positional argument and flag value is
`<arg>`), and only this user's processes are listed. Home paths stay: the
file is the person's own, and paths are the diagnosis.

BOUNDS: each log is its last 5 MiB (a config is parsed whole, up to 32 MiB,
or only listed); the whole log at most 90 MiB before compression and the zip
at most 25 MiB, the two together at most 115 MiB (the server's upload relay
inspects the zip in memory; past any of them, the oldest log lines go first,
README.txt says so, and the send checks both again before anything is sent);
each file 10 s and the whole collection 60 s (a source that runs over keeps the
files it finished and stops at its next one). A source that fails or runs out of time is listed in `skipped` and in
README.txt, never fatal. Windows: what needs `/proc`, `ps` or a UNIX socket
is skipped and says so.

The zip is written 0600 under `<state>/probe/debug/` (the newest 3 kept) or
wherever `--out` says. Sending it: `POST /v1/diagnostics/bundles` for an
upload slot, the zip sent with exactly the slot's method, URL and headers,
then `POST /v1/diagnostics/bundles/<id>/complete`.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import threading
import time
import zipfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from probe._compat import StrEnum
from probe.core import report
from probe.core.report import Failure, Scope

ROUTE = "/v1/diagnostics/bundles"
SCHEMA = 1
FILE_CAP = 5 * 1024 * 1024
#: The server's limits (contract rev 5b, server PR #3325): the API's upload
#: relay inspects the zip in memory and stops at 128 MiB, so the zip is at most
#: `SEND_CAP` AND the zip plus its uncompressed bytes at most `RELAY_CAP`, or
#: the PUT fails 422. The uncompressed cap leaves room for a full-size zip.
SEND_CAP = 25 * 1024 * 1024
#: 120 MiB in the contract, kept under it by a margin (the relay stops at 128).
RELAY_CAP = 115 * 1024 * 1024
UNCOMPRESSED_CAP = RELAY_CAP - SEND_CAP
SOURCE_BUDGET_S = 10.0
TOTAL_BUDGET_S = 60.0
COMMAND_TIMEOUT_S = 5.0
SERVICE_LIVE_BUDGET_S = 2.0
KEEP_BUNDLES = 3
RECENT_SESSIONS = 10
RECENT_TRANSCRIPTS = 10
RECENT_ACTIONS = 20
MAX_PROCESSES = 300
#: How the desktop app names its own version to the CLI it runs.
APP_VERSION_ENV = "PROBE_APP_VERSION"
#: The zip PUT's own bound: 25 MiB on a slow uplink.
UPLOAD_PUT_TIMEOUT_S = 120.0
WINDOWS = os.name == "nt"
#: A file whose NAME says it holds a credential is listed, never read.
_CREDENTIAL_FILE = ("auth", "credential", "token", "secret", "password", ".key", "cookie")
#: Environment variables an agent process shows Probe (plan B9): how Probe meets it.
_AGENT_ENV_PREFIXES = ("PROBE_", "CLAUDE", "CODEX_", "PI_", "KIMI_", "ANTHROPIC_", "OPENAI_", "XDG_")
_AGENT_ENV_NAMES = ("PATH", "HOME", "SHELL", "VIRTUAL_ENV", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE",
                    "NODE_EXTRA_CA_CERTS", "NO_PROXY", "no_proxy")


def _agent_binaries() -> frozenset[str]:
    """Process names (or argv[0] basenames) of the coding agents, from the
    registry: each one's binary, and the name it gives its own process where
    that differs (Kimi Code's `process_title`)."""
    from probe.harness import get_registry

    return frozenset(name for h in get_registry().all() for name in (h.binary, h.process_title) if name)


@dataclass
class Entry:
    data: bytes
    #: A log: trimmed from its oldest lines when the bundle is over a cap.
    log: bool = False


@dataclass
class Collection:
    """`collect(Scope.LOCAL)`: every file the zip will hold, by zip path."""

    files: dict[str, Entry] = field(default_factory=dict)
    skipped: dict[str, str] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    harnesses: list[str] = field(default_factory=list)
    session_ids: list[str] = field(default_factory=list)
    started_at: float = 0.0
    #: Seconds each source took (README.txt lists them).
    timings: dict[str, float] = field(default_factory=dict)


@dataclass
class Bundle:
    path: Path
    bytes: int
    files: int
    skipped: list[str]
    harnesses: list[str]
    session_ids: list[str]


# ---------------------------------------------------------------------------
# One source's output
# ---------------------------------------------------------------------------


class _Cancelled(Exception):
    """The collector stopped waiting for this source: it stops at its next file."""


class Sink:
    """What one source writes. Every text is scrubbed here, once: a source never
    writes raw bytes into the zip.

    Each file is one step: the collector gives every step its own budget
    (`SOURCE_BUDGET_S`, measured from the last finished file) and keeps the
    files that finished when a later one runs over. Once it stops waiting it
    sets `cancel`, and the source's next step raises `_Cancelled`, so abandoned
    work stops at the next file instead of burning CPU in the background."""

    def __init__(self) -> None:
        self.files: dict[str, Entry] = {}
        self.notes: list[str] = []
        self.cancel = threading.Event()
        self.lock = threading.Lock()
        #: When the last step finished (monotonic), and what runs now.
        self.progress = time.monotonic()
        self.current = ""
        self.last = ""

    def step(self, what: str = "") -> None:
        """A step finished (or a long one is still moving): stop here if the
        collector gave up, else reset this step's budget."""
        if self.cancel.is_set():
            raise _Cancelled
        self.progress = time.monotonic()
        self.current = what

    def _put(self, path: str, entry: Entry) -> None:
        if self.cancel.is_set():
            raise _Cancelled
        with self.lock:
            self.files[path] = entry
        self.last = path
        self.step()

    def check(self) -> None:
        """Stop here if the collector gave up (inside a long step: a config walk)."""
        if self.cancel.is_set():
            raise _Cancelled

    def snapshot(self) -> tuple[dict[str, Entry], list[str]]:
        with self.lock:
            return dict(self.files), list(self.notes)

    def text(self, path: str, text: str, *, log: bool = False) -> None:
        self.step(path)
        self._put(path, Entry(report.scrub_for(text, Scope.LOCAL).encode("utf-8"), log=log))

    def json(self, path: str, value: object) -> None:
        self.step(path)
        clean = report.redact_tree(value, Scope.LOCAL)
        self._put(path, Entry((json.dumps(clean, indent=2, ensure_ascii=False, default=str) + "\n").encode()))

    def log_file(self, path: str, source: Path) -> bool:
        if not source.is_file():  # a FIFO would block the read forever
            return False
        self.step(path)
        text = report.read_tail(source, FILE_CAP)
        if text is None:
            return False
        try:
            if source.stat().st_size > FILE_CAP:
                self.notes.append(f"{path}: only its last {FILE_CAP // (1024 * 1024)} MiB")
        except OSError:
            pass
        self.text(path, text, log=True)
        return True

    def config_file(self, path: str, source: Path) -> bool:
        """A config file. JSON and TOML are parsed WHOLE and redacted as a tree;
        one that does not parse (or is too big) is only listed, never written as
        text. Any other small text file (a plist, a cursor) is scrubbed as text."""
        if not source.is_file():
            return False
        self.step(path)
        if credential_file(source):
            self.json(path + ".listing.json", describe(source))
            return False
        name = source.name.lower()
        if name.endswith((".json", ".toml")) or name == "service.run":
            clean, why = report.read_config(source, check=self.check)
            if clean is None:
                self.json(path + ".listing.json", {**describe(source), "not_parsed": why})
                return False
            self._put(path, Entry(clean.encode("utf-8")))
            return True
        text = report.read_tail(source, FILE_CAP)
        if text is None:
            return False
        self.text(path, text)
        return True


def credential_file(path: Path) -> bool:
    name = path.name.lower()
    return any(word in name for word in _CREDENTIAL_FILE)


def describe(path: Path) -> dict:
    """A file by metadata only: never its content."""
    try:
        st = path.stat()
    except OSError:
        return {"path": str(path), "exists": False}
    return {"path": str(path), "bytes": st.st_size,
            "modified": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime))}


def _command(argv: list[str], timeout: float = COMMAND_TIMEOUT_S) -> str:
    """One command's output (stdout then stderr) and exit status, as text."""
    try:
        done = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False,
                              stdin=subprocess.DEVNULL, errors="replace")
    except FileNotFoundError:
        return f"$ {' '.join(argv)}\nnot found\n"
    except subprocess.TimeoutExpired:
        return f"$ {' '.join(argv)}\ntimed out after {timeout:g} s\n"
    except OSError as exc:
        return f"$ {' '.join(argv)}\nfailed: {exc}\n"
    return f"$ {' '.join(argv)}\nexit {done.returncode}\n{done.stdout}{done.stderr}"


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------


def _probe_files(sink: Sink) -> None:
    """The CLI's own records: its config (tokens redacted), auto-update, the
    side-by-side installs, run locks, the outbox's counts."""
    from probe.sdk.config import config_path

    sink.config_file("probe/config.json", config_path())
    root = report.state_root()
    try:
        entries = sorted(root.iterdir()) if root.is_dir() else []
    except OSError:
        entries = []
    for path in entries:
        if not path.is_file():
            continue
        if path.suffix == ".json":
            if path.name == "device.json" or credential_file(path):
                sink.json(f"probe/{path.name}.listing.json", describe(path))
            else:
                sink.config_file(f"probe/{path.name}", path)
        elif path.suffix == ".log" and not path.name.startswith("daemon-errors"):
            sink.log_file(f"probe/{path.name}", path)
    from probe import version_policy

    sink.config_file("probe/version-check.json", version_policy.cache_path())
    facts: dict = {}
    with contextlib.suppress(Exception):
        from probe._shared import installs

        active = installs.active()
        root_dir = installs.versions_root()
        facts["installs"] = {
            "record": installs.record(),
            "active": str(active) if active else None,
            "versions": sorted(p.name for p in root_dir.iterdir()) if root_dir.is_dir() else [],
        }
    with contextlib.suppress(Exception):
        from probe._shared import run_lock

        facts["live_runs"] = run_lock.live_runs()
    with contextlib.suppress(Exception):
        from probe.sdk.journal import Journal

        status = Journal.read_status()
        # Counts only: an op's body is the researcher's data.
        facts["outbox"] = {k: v for k, v in (status or {}).items() if isinstance(v, (int, float, bool, str))
                           and k != "last_error"}
    sink.json("probe/installs-and-runs.json", facts)


def _probe_doctor(sink: Sink) -> None:
    from probe.cli import doctor as doctor_impl
    from probe.cli import service_calls

    caps = doctor_impl.collect(local=True)
    sink.text("probe/doctor.txt", doctor_impl.render(caps, service=service_calls.view()) + "\n")


def _probe_status(sink: Sink) -> None:
    from probe.core import reads

    sink.json("probe/status.json", reads.status(refresh=False))


def _probe_commands(sink: Sink) -> None:
    which = ["where", "probe"] if WINDOWS else ["which", "-a", "probe"]
    lines = [_command(which)]
    try:
        from probe.harness import get_registry

        for harness in get_registry().all():
            if harness.binary:
                lines.append(f"{harness.binary}: {shutil.which(harness.binary) or 'not on PATH'}\n")
    except Exception:  # noqa: BLE001
        pass
    lines.append(f"python: {sys.executable}\n")
    sink.text("probe/which.txt", "".join(lines))
    sink.text("probe/uv-tool-list.txt", _command(["uv", "tool", "list", "--show-paths"]))


def _service_files(sink: Sink) -> None:
    """The service's folder, whole: its logs, its records (credential-named
    variables in `recorders.json` redacted), its actions' newest logs. The hook
    queue holds hook events (an agent's prompts among them): counted only."""
    from probe.service import paths

    folder = paths.service_dir()
    root = paths.root_dir()
    for base, prefix in ((folder, "service"), (root, "service/shared")):
        try:
            entries = sorted(base.iterdir()) if base.is_dir() else []
        except OSError:
            entries = []
        for path in entries:
            if path.is_dir():
                if path.name == paths.ACTIONS_DIRNAME:
                    _newest(sink, path, f"{prefix}/actions", RECENT_ACTIONS)
                elif path.name == paths.HOOK_QUEUE_DIRNAME:
                    names = [p.name for p in path.iterdir()] if path.is_dir() else []
                    sink.json(f"{prefix}/hooks-queue.json", {
                        "waiting": sum(n.endswith(".json") for n in names),
                        "taken": sum(n.endswith(".done") for n in names),
                        "drained_by": _small(path / paths.HOOK_QUEUE_DRAINER),
                    })
                continue
            name = path.name
            if not path.is_file() or name.endswith((".lock", ".sock")) or name == "service.stopping":
                continue
            if ".log" in name:
                sink.log_file(f"{prefix}/{name}", path)
            else:
                sink.config_file(f"{prefix}/{name}", path)


def _small(path: Path, cap: int = 256) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:cap].strip()
    except OSError:
        return None


def _newest(sink: Sink, folder: Path, prefix: str, count: int) -> None:
    try:
        files = sorted((p for p in folder.iterdir() if p.is_file()), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        return
    for path in files[:count]:
        if path.suffix == ".log":
            sink.log_file(f"{prefix}/{path.name}", path)
        else:
            sink.text(f"{prefix}/{path.name}", report.read_tail(path, FILE_CAP) or "")
    if len(files) > count:
        sink.notes.append(f"{prefix}: the newest {count} of {len(files)} files")


def _keeper(sink: Sink) -> None:
    from probe.service import keeper

    found = {}
    for path in (keeper._systemd_dir() / f"{keeper.NAME}.service",  # noqa: SLF001 -- the keeper's own paths
                 keeper._systemd_dir() / f"{keeper.NAME}.timer",  # noqa: SLF001
                 keeper._plist_path(),  # noqa: SLF001
                 keeper._task_marker(),  # noqa: SLF001
                 keeper._off_path()):  # noqa: SLF001
        found[str(path)] = path.exists()
        if path.is_file():
            sink.config_file(f"service/keeper/{path.name}", path)
    sink.json("service/keeper/installed.json", found)


def _service_live(sink: Sink) -> None:
    """The service's own answers, raw (workers, background work, the hook queue,
    the status line, notes and the guard included), when it replies in 2 s."""
    if os.name != "posix":
        raise _Skip("not read on this platform (the service is asked over a UNIX socket here)")
    from probe.cli import service_calls

    if not service_calls._reachable():  # noqa: SLF001 -- the same two stats `probe status` makes
        raise _Skip("the Probe service is not running")
    from probe.service import client
    from probe.service.protocol import Client, Method

    deadline = time.monotonic() + SERVICE_LIVE_BUDGET_S

    def left(conn) -> None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError
        conn.sock.settimeout(remaining)

    try:
        with client.Connection.open(SERVICE_LIVE_BUDGET_S) as conn:
            left(conn)
            conn.hello(Client.CLI, report._cli_version())  # noqa: SLF001
            left(conn)
            status = conn.call(Method.STATUS)
            left(conn)
            listing = conn.call(Method.SESSION_LIST)
    except TimeoutError:
        raise _Skip(f"the Probe service did not answer within {SERVICE_LIVE_BUDGET_S:g} s") from None
    except (OSError, ValueError, client.ServiceError) as exc:
        raise _Skip(f"the Probe service could not be asked ({type(exc).__name__})") from None
    sink.json("service/live-status.json", status)
    sink.json("service/live-sessions.json", listing)


class _Skip(Exception):
    """A source with nothing to read here: listed with its reason, not a failure."""


def _chosen_sessions() -> list[tuple[str, Path, bool]]:
    """(sid, state root, live): every live session, then the 10 most recently
    active others this machine's daemon folder knows."""
    chosen: dict[str, tuple[str, Path, bool]] = {}
    for session in report.live_sessions():
        sid = session["sid"]
        root = Path(session["state_dir"]) if isinstance(session.get("state_dir"), str) else report.state_root()
        chosen[sid] = (sid, root, True)
    daemon = report.state_root() / "daemon"
    recent: dict[str, float] = {}
    for pattern in ("*.log", "sessions/*"):
        with contextlib.suppress(OSError):
            for path in daemon.glob(pattern):
                sid = path.stem if path.suffix == ".log" else path.name
                if report._UUID_EXACT.match(sid):  # noqa: SLF001
                    with contextlib.suppress(OSError):
                        recent[sid] = max(recent.get(sid, 0.0), path.stat().st_mtime)
    others = [sid for sid in sorted(recent, key=recent.get, reverse=True) if sid not in chosen]
    for sid in others[:RECENT_SESSIONS]:
        chosen[sid] = (sid, report.session_state_root(sid), False)
    return list(chosen.values())


def _sessions(sink: Sink) -> None:
    index = []
    for sid, root, live in _chosen_sessions():
        sink.step(f"session {sid}")
        base = f"sessions/{sid}"
        safe = report._safe(sid)  # noqa: SLF001
        daemon = root / "daemon"
        trace = daemon / "sessions" / safe
        listing: dict = {}
        sink.log_file(f"{base}/worker.log", trace / "worker.log")
        for name in ("meta.json", "reader.cursor", "writer.cursor"):
            if (trace / name).is_file():
                sink.config_file(f"{base}/trace-{name}", trace / name)
        for name in ("reader.jsonl", "writer.jsonl"):
            # The model's full exchanges: content, so metadata only.
            if (trace / name).exists():
                listing[f"trace/{name}"] = describe(trace / name)
        with contextlib.suppress(OSError):
            for path in sorted(daemon.glob(f"{safe}.*")):
                if path.name.endswith((".sqlite", ".sqlite-wal", ".sqlite-shm", ".jsonl")):
                    listing[f"daemon/{path.name}"] = describe(path)
                elif path.suffix == ".log":
                    sink.log_file(f"{base}/worker-output.log", path)
                elif path.is_file() and path.stat().st_size <= 64 * 1024:
                    sink.config_file(f"{base}/daemon-{path.name}", path)
        markers = root / "sessions"
        with contextlib.suppress(OSError):
            for path in sorted(markers.glob(f"{sid}*")):
                if path.is_file() and not path.name.endswith(".jsonl") and path.stat().st_size <= 64 * 1024:
                    sink.config_file(f"{base}/marker-{path.name}", path)
                elif path.exists():
                    listing[f"sessions/{path.name}"] = describe(path)
        for harness_id, path in report.tap_log_paths(sid):
            sink.log_file(f"{base}/tap-{harness_id}.log", path)
            companion = path.with_name(f"{safe}.companion.log")
            if companion.is_file():
                sink.log_file(f"{base}/tap-{harness_id}.companion.log", companion)
        tap = _tap_rows(sid)
        if tap:
            sink.json(f"{base}/tap-offsets-and-outbox.json", tap)
        sink.json(f"{base}/listing.json", listing)
        index.append({"sid": sid, "live": live, "state_dir": str(root)})
    sink.json("sessions/index.json", index)


def _tap_rows(sid: str) -> dict:
    """The tap's offsets for this session's transcripts and its outbox COUNTS
    (never a body), read-only from each tap's `state.db`."""
    import sqlite3

    found: dict = {}
    try:
        from probe.harness import get_registry

        harnesses = [h for h in get_registry().captured() if h.capture is not None]
    except Exception:  # noqa: BLE001
        return found
    for harness in harnesses:
        db = harness.capture.state_dir() / "state.db"
        if not db.is_file():
            continue
        try:
            conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=1.0)
        except sqlite3.Error:
            continue
        try:
            offsets = [dict(zip(("path", "cwd", "last_line_no", "last_seen_at", "size", "byte_offset"), row))
                       for row in conn.execute(
                           "SELECT path, cwd, last_line_no, last_seen_at, size, byte_offset FROM file_offsets "
                           "WHERE session_id = ?", (sid,))]
            outbox = conn.execute(
                "SELECT COUNT(*), MIN(created_at), MAX(attempt_count) FROM outbox WHERE session_id = ?", (sid,)
            ).fetchone()
            found[harness.id] = {"offsets": offsets, "outbox": {
                "batches": outbox[0], "oldest_created_at": outbox[1], "most_attempts": outbox[2]}}
        except sqlite3.Error as exc:
            found[harness.id] = {"error": type(exc).__name__}
        finally:
            conn.close()
    return found


def _daemon(sink: Sink) -> None:
    root = report.state_root()
    for name in ("daemon-errors.log", "daemon-errors.log.1"):
        sink.log_file(f"daemon/{name}", root / name)
    for name in ("device.json", "reasoning-summaries.json"):
        path = (root / "daemon" / name) if name == "device.json" else (root / name)
        if path.is_file():
            sink.config_file(f"daemon/{name}", path)
    try:
        from probe.harness import get_registry

        for harness in get_registry().captured():
            if harness.capture is None:
                continue
            path = harness.capture.state_dir() / "logs" / "stop-daemon.jsonl"
            if path.is_file():
                sink.log_file(f"daemon/stop-daemon-{harness.id}.jsonl", path)
    except Exception:  # noqa: BLE001
        pass
    sink.json("daemon/environment.json", {k: v for k, v in os.environ.items() if k.startswith("PROBE_DAEMON")})


def _agent(harness) -> Callable[[Sink], None]:
    def source(sink: Sink) -> None:
        base = f"agents/{harness.id}"
        home = harness.home_dir()
        facts: dict = {"label": harness.label, "home": str(home) if home else None, "binary": harness.binary}
        # The cheap facts first: a config that stalls its step costs itself, not them.
        if harness.binary and shutil.which(harness.binary):
            if _another_program(harness):
                facts["binary_is_another_program"] = True
            else:
                sink.text(f"{base}/version.txt", _command([harness.binary, "--version"]))
        else:
            facts["binary_on_path"] = False
        transcripts = _transcripts(harness, sink)
        _AGENT_CWDS.extend(t["cwd"] for t in transcripts if t.get("cwd"))
        sink.json(f"{base}/transcripts.json", transcripts)
        facts["recent_models"] = sorted({t["model"] for t in transcripts if t.get("model")})
        sink.json(f"{base}/facts.json", facts)
        if home is not None and home.is_dir():
            for path in sorted(home.iterdir()):
                # Its settings, not its caches (`stats-cache.json`).
                if path.is_file() and path.suffix in (".json", ".toml") and "cache" not in path.name.lower():
                    sink.config_file(f"{base}/home/{path.name}", path)
            _plugin_files(sink, home, f"{base}/home")
        from probe.cli import plugin_cli

        if harness.id == plugin_cli.CLAUDE:
            # Claude Code keeps its account and per-project state beside its folder.
            outside = Path.home() / ".claude.json"
            if outside.is_file():
                sink.config_file(f"{base}/claude.json", outside)

    return source


def _another_program(harness) -> bool:
    """Whether the program on PATH under the agent's name is someone else's: pi's two-letter name
    is confirmed by its `--help` (`pi_config.pi_binary_available`, as the wizard does), so another
    package's program of that name is not taken for the agent."""
    from probe.cli import pi_config

    return harness.id == pi_config.HARNESS_ID and not pi_config.pi_binary_available()


#: The working folders of the recent sessions each agent source found (for `projects`).
_AGENT_CWDS: list[str] = []
#: Plugin records and the Probe plugins' manifests and hooks, under an agent's folder.
_PLUGIN_RECORDS = ("installed_plugins.json", "known_marketplaces.json", "installed.json")


def _plugin_files(sink: Sink, home: Path, prefix: str) -> None:
    plugins = home / "plugins"
    if not plugins.is_dir():
        return
    for name in _PLUGIN_RECORDS:
        if (plugins / name).is_file():
            sink.config_file(f"{prefix}/plugins/{name}", plugins / name)
    found = 0
    for dirpath, dirnames, filenames in os.walk(plugins):
        depth = Path(dirpath).relative_to(plugins).parts
        if len(depth) >= 6:
            dirnames[:] = []
        if "probe" not in dirpath.lower():
            continue
        for name in filenames:
            if name in ("plugin.json", "hooks.json", "package.json") and found < 40:
                path = Path(dirpath) / name
                sink.config_file(f"{prefix}/plugins/{path.relative_to(plugins).as_posix()}", path)
                found += 1


def _transcripts(harness, sink: Sink | None = None) -> list[dict]:
    """The newest transcripts, by metadata: path, size, time, line count, last
    event type, the model last used and the working folder -- never content."""
    root = harness.transcript_root()
    if root is None or not root.is_dir():
        return []
    try:
        pattern = harness.transcript_pattern()
        # Main sessions only: a subagent's transcript is part of its parent's.
        files = [p for p in root.glob(pattern) if p.is_file() and "subagents" not in p.parts]
    except Exception:  # noqa: BLE001
        return []
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    rows = []
    for path in files[:RECENT_TRANSCRIPTS]:
        if sink is not None:
            sink.step(f"transcript {path.name}")
        row = describe(path)
        row.update(_transcript_shape(path))
        rows.append(row)
    return rows


def _transcript_shape(path: Path) -> dict:
    lines = 0
    try:
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                lines += chunk.count(b"\n")
    except OSError:
        return {}
    shape: dict = {"lines": lines}
    tail = report.read_tail(path, 512 * 1024) or ""
    for line in reversed(tail.splitlines()):
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        if "last_event_type" not in shape:
            shape["last_event_type"] = _word(event.get("type"))
        for holder in (event, event.get("message"), event.get("payload")):
            if isinstance(holder, dict):
                if "model" not in shape and _word(holder.get("model")):
                    shape["model"] = _word(holder.get("model"))
                if "cwd" not in shape and isinstance(holder.get("cwd"), str):
                    shape["cwd"] = holder["cwd"][:1024]
        if {"last_event_type", "model", "cwd"} <= set(shape):
            break
    return shape


def _word(value: object) -> str | None:
    """A short identifier (an event type, a model name), never free text."""
    if isinstance(value, str) and 0 < len(value) <= 128 and not any(c.isspace() for c in value):
        return value
    return None


#: A recent session's own folder settings (plan B9: each session's project folder).
_PROJECT_FILES = (".claude/settings.json", ".claude/settings.local.json", ".mcp.json", ".probe.config",
                  ".pi/settings.json", ".codex/config.toml")


def _projects(sink: Sink) -> None:
    index = []
    for number, cwd in enumerate(dict.fromkeys(_AGENT_CWDS)):
        if number >= RECENT_TRANSCRIPTS:
            break
        folder = Path(cwd)
        found = []
        for name in _PROJECT_FILES:
            if (folder / name).is_file():
                sink.config_file(f"agents/projects/{number}/{name}", folder / name)
                found.append(name)
        index.append({"n": number, "cwd": cwd, "files": found})
    sink.json("agents/projects/index.json", index)


def _system(sink: Sink) -> None:
    facts: dict = {
        "os": report.os_label(),
        "platform": platform.platform(),
        "python": sys.version,
        "executable": sys.executable,
        "cpus": os.cpu_count(),
        "hostname": socket.gethostname(),
        "locale": {k: os.environ.get(k) for k in ("LANG", "LC_ALL", "LC_CTYPE")},
        "timezone": time.tzname,
        "shell": os.environ.get("SHELL") or os.environ.get("COMSPEC"),
        "container": _container(),
    }
    with contextlib.suppress(Exception):
        facts["load"] = os.getloadavg()
    with contextlib.suppress(Exception):
        import psutil

        memory = psutil.virtual_memory()
        facts["memory"] = {"total": memory.total, "available": memory.available, "percent": memory.percent}
        facts["boot_time"] = psutil.boot_time()
        facts["uptime_s"] = int(time.time() - psutil.boot_time())
    disks = {}
    for label, path in (("home", Path.home()), ("state", report.state_root())):
        with contextlib.suppress(OSError):
            probe_at = path if path.exists() else path.parent
            usage = shutil.disk_usage(probe_at)
            disks[label] = {"path": str(path), "total": usage.total, "free": usage.free}
    facts["disks"] = disks
    with contextlib.suppress(Exception):
        import resource

        facts["limits"] = {name: resource.getrlimit(getattr(resource, name))
                           for name in ("RLIMIT_NOFILE", "RLIMIT_NPROC", "RLIMIT_AS") if hasattr(resource, name)}
    pid = _service_pid()
    facts["service_pid"] = pid
    if pid:
        with contextlib.suppress(Exception):
            import psutil

            process = psutil.Process(pid)
            facts["service_open_files"] = process.num_fds() if hasattr(process, "num_fds") else None
    sink.json("system/os.json", facts)


def _container() -> dict:
    facts = {"dockerenv": os.path.exists("/.dockerenv"), "containerenv": os.path.exists("/run/.containerenv")}
    with contextlib.suppress(OSError):
        cgroup = Path("/proc/1/cgroup").read_text(encoding="utf-8", errors="replace")
        facts["cgroup_names_container"] = any(w in cgroup for w in ("docker", "kubepods", "containerd", "lxc"))
    return facts


def _service_pid() -> int | None:
    folder = report.service_dir()
    if folder is None:
        return None
    text = _small(folder / "service.lock", 64) or ""
    for word in text.replace(",", " ").split():
        if word.isdigit():
            return int(word)
    data = report.read_json(folder / "service.lock")
    if isinstance(data, dict) and isinstance(data.get("pid"), int):
        return data["pid"]
    return None


def _running(pid: int) -> bool:
    try:
        import psutil

        return psutil.pid_exists(pid)
    except Exception:  # noqa: BLE001 -- unknown: try to read it
        return True


def _environment(sink: Sink) -> None:
    sink.json("system/env-this-command.json", report.redact_env(dict(os.environ), Scope.LOCAL))


def process_environment(pid: int) -> dict[str, str] | None:
    """Another process's environment: `/proc/<pid>/environ` on Linux, `ps -E`
    on macOS; None where neither can be read (Windows, another user's)."""
    if sys.platform.startswith("linux"):
        try:
            raw = Path(f"/proc/{pid}/environ").read_bytes()
        except OSError:
            return None
        env: dict[str, str] = {}
        for item in raw.split(b"\0"):
            name, eq, value = item.partition(b"=")
            if eq and name:
                env[name.decode("utf-8", "replace")] = value.decode("utf-8", "replace")
        return env
    if sys.platform == "darwin":
        try:
            done = subprocess.run(["ps", "-E", "-ww", "-o", "command=", "-p", str(pid)], capture_output=True,
                                  text=True, timeout=COMMAND_TIMEOUT_S, check=False, errors="replace")
        except (OSError, subprocess.SubprocessError):
            return None
        env = {}
        for word in done.stdout.split():
            name, eq, value = word.partition("=")
            if eq and name and name.replace("_", "").isalnum() and name[0].isalpha() and name.upper() == name:
                env[name] = value
        return env or None
    return None


def _service_environment(sink: Sink) -> None:
    pid = _service_pid()
    if not pid or not _running(pid):
        raise _Skip("the Probe service is not running")
    env = process_environment(pid)
    if env is None:
        raise _Skip("its environment cannot be read on this platform")
    sink.json("system/env-probe-service.json", {"pid": pid, "env": report.redact_env(env, Scope.LOCAL)})


def _agent_environments(sink: Sink) -> None:
    """Each live agent process's view of Probe: its PROBE_*, CLAUDE_*, CODEX_*
    (and the like) and proxy variables, credential values redacted."""
    found = 0
    for session in report.live_sessions():
        owner = session.get("owner")
        if not isinstance(owner, dict) or not isinstance(owner.get("pid"), int):
            continue
        env = process_environment(owner["pid"])
        if env is None:
            continue
        kept = {k: v for k, v in env.items()
                if k.startswith(_AGENT_ENV_PREFIXES) or k in _AGENT_ENV_NAMES or k.lower().endswith("_proxy")}
        sink.json(f"system/env-agents/{session.get('harness', 'agent')}-{owner['pid']}.json", {
            "sid": session["sid"], "pid": owner["pid"], "env": report.redact_env(kept, Scope.LOCAL)})
        found += 1
    if not found and WINDOWS:
        raise _Skip("agent processes' environments cannot be read on Windows")


def _ours(info: dict) -> bool:
    """This user's process (a shared node runs other people's agents too).
    Unknown owner: not ours."""
    if hasattr(os, "getuid"):
        uids = info.get("uids")
        return uids is not None and getattr(uids, "real", None) == os.getuid()
    try:
        import getpass

        return bool(info.get("username")) and str(info["username"]).split("\\")[-1] == getpass.getuser()
    except Exception:  # noqa: BLE001
        return False


def _processes(sink: Sink) -> None:
    """This user's Probe processes, agents and their Pythons: pid, parent,
    start, memory, and the command line reduced to its program and flag names
    (`report.redact_argv`: a prompt or a password is a positional argument or a
    flag value)."""
    import psutil

    agents = _agent_binaries()
    rows = []
    attrs = ["pid", "ppid", "name", "create_time", "memory_info", "cmdline",
             "uids" if hasattr(os, "getuid") else "username"]
    for process in psutil.process_iter(attrs):
        info = process.info
        if not _ours(info):
            continue
        argv = [str(a) for a in (info.get("cmdline") or [])]
        joined = " ".join(argv).lower()
        name = (info.get("name") or "").lower()
        first = Path(argv[0]).name.lower() if argv else ""
        if "probe" not in joined and name not in agents and first not in agents:
            continue
        memory = info.get("memory_info")
        if len(rows) >= MAX_PROCESSES:
            sink.notes.append(f"system/processes.json: the first {MAX_PROCESSES} matching processes")
            break
        rows.append({
            "pid": info.get("pid"),
            "ppid": info.get("ppid"),
            "name": info.get("name"),
            "started": info.get("create_time"),
            "rss": getattr(memory, "rss", None),
            "cmdline": report.redact_argv(argv),
        })
    sink.json("system/processes.json", rows)


def _network(sink: Sink) -> None:
    from urllib.parse import urlsplit

    import httpx

    url = report.base_url() or ""
    facts: dict = {"base_url": url}
    proxies = sorted(k for k in os.environ if k.lower() in (
        "http_proxy", "https_proxy", "all_proxy", "no_proxy"))
    facts["proxy_variables_set"] = proxies
    parts = urlsplit(url)
    if parts.hostname:
        try:
            started = time.monotonic()
            answers = socket.getaddrinfo(parts.hostname, parts.port or (443 if parts.scheme == "https" else 80))
            facts["dns"] = {"addresses": sorted({a[4][0] for a in answers}),
                            "ms": int((time.monotonic() - started) * 1000)}
        except OSError as exc:
            facts["dns"] = {"error": str(exc)[:200]}
        try:
            from probe.sdk.tls import ssl_context

            started = time.monotonic()
            with httpx.Client(base_url=url, timeout=httpx.Timeout(5.0, connect=3.0), verify=ssl_context()) as http:
                answer = http.get("/v1/client-version")
            facts["client_version"] = {"status": answer.status_code,
                                       "ms": int((time.monotonic() - started) * 1000)}
        except Exception as exc:  # noqa: BLE001 -- the failure is the finding
            facts["client_version"] = {"error": type(exc).__name__, "detail": str(exc)[:200]}
    sink.json("network/reach.json", facts)


def _sources() -> list[tuple[str, Callable[[Sink], None]]]:
    sources: list[tuple[str, Callable[[Sink], None]]] = [
        ("probe", _probe_files),
        ("probe_doctor", _probe_doctor),
        ("probe_status", _probe_status),
        ("probe_commands", _probe_commands),
        ("service_files", _service_files),
        ("service_keeper", _keeper),
        ("service_live", _service_live),
        ("sessions", _sessions),
        ("daemon", _daemon),
    ]
    try:
        from probe.harness import get_registry

        sources.extend((f"agent_{h.id}", _agent(h)) for h in get_registry().all())
    except Exception:  # noqa: BLE001
        pass
    sources.extend([
        ("agent_projects", _projects),
        ("system", _system),
        ("env_this_command", _environment),
        ("env_probe_service", _service_environment),
        ("env_agents", _agent_environments),
        ("processes", _processes),
        ("network", _network),
    ])
    return sources


# ---------------------------------------------------------------------------
# collect, trim, zip
# ---------------------------------------------------------------------------


def collect(*, deadline_s: float | None = None, source_budget_s: float = SOURCE_BUDGET_S) -> Collection:
    """Every source, all within `deadline_s` (default `TOTAL_BUDGET_S`), each
    FILE within `source_budget_s` of the one before it. Never raises: a source
    that fails or runs over keeps the files it finished and is listed in
    `skipped`; the collector stops waiting for it and it stops at its next file."""
    collection = Collection(started_at=time.time())
    deadline = time.monotonic() + (TOTAL_BUDGET_S if deadline_s is None else deadline_s)
    _AGENT_CWDS.clear()
    for name, fn in _sources():
        if deadline - time.monotonic() <= 0.5:
            collection.skipped[name] = "the debug log's time budget ran out first"
            continue
        sink = Sink()
        outcome: list[str] = []

        def run(fn=fn, sink=sink, outcome=outcome) -> None:
            try:
                fn(sink)
            except _Skip as exc:
                outcome.append(str(exc))
            except _Cancelled:
                pass
            except BaseException as exc:  # noqa: BLE001 -- recorded as the source's reason
                outcome.append(f"failed: {type(exc).__name__}")

        began = time.monotonic()
        worker = threading.Thread(target=run, name=f"probe-debug-{name}", daemon=True)
        worker.start()
        stopped = ""
        while True:
            worker.join(0.05)
            if not worker.is_alive():
                break
            now = time.monotonic()
            if now - sink.progress > source_budget_s:
                what = sink.current or (f"the step after {sink.last}" if sink.last else "its first step")
                stopped = f"stopped: {what} took over {source_budget_s:g} s"
                break
            if now >= deadline:
                stopped = "stopped: the debug log's time budget ran out"
                break
        if stopped:
            sink.cancel.set()  # the source stops at its next file
        files, notes = sink.snapshot()
        collection.timings[name] = round(time.monotonic() - began, 2)
        if stopped or outcome:
            reason = stopped or outcome[0]
            collection.skipped[name] = f"{reason} (kept {len(files)} files)" if files and stopped else reason
        collection.files.update(files)
        collection.notes.extend(notes)
    live = report.live_sessions()
    # The server files the log under every session and coding agent it holds, so staff find it
    # from any of them: the live sessions and the recent ones it has a folder for, and each agent
    # whose folder it filled, not only the sessions that happened to be live at that moment.
    collection.harnesses = list(dict.fromkeys(
        h for h in (*(report._harness_slug(s.get("harness")) for s in live),  # noqa: SLF001
                    *_harnesses_with_files(collection.files)) if h))[:report.MAX_HARNESSES]
    from probe.sdk import agent_session

    sids = [s["sid"] for s in live] + [path.split("/")[1] for path in sorted(collection.files)
                                       if path.startswith("sessions/") and path.count("/") >= 2]
    own = agent_session.session_id_from_env()
    if own:
        sids.insert(0, own)
    collection.session_ids = list(dict.fromkeys(
        s.lower() for s in sids if report._UUID_EXACT.match(s)))[:report.MAX_SESSION_IDS]  # noqa: SLF001
    return collection


#: What an agent's source writes for every registered agent, installed or not.
_AGENT_ALWAYS = frozenset({"facts.json", "transcripts.json"})


def _harnesses_with_files(files: dict[str, Entry]) -> list[str]:
    """The coding agents the log holds something of, in registry order: its version (its own
    program on PATH answered `--version`), a recent transcript, or a file from its folder. Not the
    `facts.json` and empty `transcripts.json` written for every agent the registry knows, or every
    log names all of them."""
    try:
        from probe.harness import get_registry

        known = [h.id for h in get_registry().captured()]
    except Exception:  # noqa: BLE001
        return []
    found = set()
    for path, entry in files.items():
        parts = path.split("/", 2)
        if len(parts) < 3 or parts[0] != "agents":
            continue
        if parts[2] == "version.txt":
            # `_command`'s second line is the exit: a launcher that fails is no agent.
            if entry.data.split(b"\n", 2)[1:2] == [b"exit 0"]:
                found.add(parts[1])
        elif parts[2] not in _AGENT_ALWAYS:
            found.add(parts[1])
        elif parts[2] == "transcripts.json":
            try:
                if json.loads(entry.data):
                    found.add(parts[1])
            except ValueError:
                pass
    return [h for h in known if h in found]


def trim(files: dict[str, Entry], excess: int) -> list[str]:
    """Drop `excess` bytes from the logs, oldest lines first, each log giving
    up its share. Returns the logs that lost lines."""
    logs = {path: entry for path, entry in files.items() if entry.log and entry.data}
    total = sum(len(entry.data) for entry in logs.values())
    if excess <= 0 or total == 0:
        return []
    keep_ratio = max(0.0, (total - excess) / total)
    trimmed = []
    for path, entry in logs.items():
        keep = int(len(entry.data) * keep_ratio)
        if keep >= len(entry.data):
            continue
        tail = entry.data[len(entry.data) - keep:] if keep else b""
        newline = tail.find(b"\n")
        entry.data = tail[newline + 1:] if newline >= 0 else b""
        trimmed.append(path)
    return trimmed


def _readme(collection: Collection, trimmed: dict[str, str]) -> str:
    try:
        from probe.cli import versions

        local = versions.local_versions()
    except Exception:  # noqa: BLE001
        local = {"cli": report._cli_version()}  # noqa: SLF001
    made = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(collection.started_at))
    lines = [
        "Probe debug log",
        "",
        f"Made:       {made} on {socket.gethostname()} ({report.os_label()})",
        f"CLI:        {local.get('cli')}",
        f"Plugin:     {local.get('plugin')}",
        f"Tap:        {local.get('tap')}",
        f"App:        {os.environ.get(APP_VERSION_ENV) or 'not run by the desktop app'}",
        f"Python:     {platform.python_version()} ({sys.executable})",
        f"Server:     {report.base_url()}",
        "",
        "What each folder holds",
        "  probe/     probe doctor, probe status --json, the CLI config (tokens redacted), auto-update and",
        "             install records, run locks, outbox counts, which -a probe, uv tool list",
        "  service/   the Probe service's folder: logs, guard, last stop, registry, recorders, starts,",
        "             updater, its actions' logs, the keeper, and its live answers when it replied in 2 s",
        "  sessions/  every live session and the 10 most recent others: worker log and output, lease,",
        "             switch, lock, cursors, tap logs, tap offsets and outbox counts (never contents)",
        "  daemon/    daemon-errors.log, the stop journal, the daemon's settings",
        "  agents/    each coding agent's version, its config files (credential files listed, never",
        "             read), the Probe plugins' manifests and hooks, recent transcripts by metadata only",
        "             (path, size, time, lines, last event type, model) and recent projects' settings",
        "  system/    OS, CPUs, memory, disks, uptime, container, limits; the environment of this",
        "             command, of the Probe service and of each live agent process; Probe's processes",
        "  network/   the server's DNS answer, a timed GET /v1/client-version, proxy variables set",
        "",
        "Left out: every value under a credential-like name (token, key, secret, password, credential,",
        "auth, cookie, account and the like) in configs and environments; header values; OAuth and",
        "account blocks; configs that do not parse (listed only); credentials the scanner recognizes",
        "anywhere; conversation content (transcripts, prompt history, traces, stores, hook events,",
        "outbox bodies). command lines keep only the program and flag names: every argument and flag",
        "value is <arg>; only this user's processes are listed. Home folder paths are kept.",
        "",
    ]
    if collection.timings:
        lines.append("Sources (seconds)")
        lines.extend(f"  {name}: {seconds:g}" for name, seconds in collection.timings.items())
        lines.append("")
    if collection.skipped:
        lines.append("Skipped sources")
        lines.extend(f"  {name}: {why}" for name, why in sorted(collection.skipped.items()))
        lines.append("")
    notes = [*collection.notes, *(f"{path}: {why}" for path, why in sorted(trimmed.items()))]
    if notes:
        lines.append("Trimmed")
        lines.extend(f"  {note}" for note in notes)
        lines.append("")
    return "\n".join(lines)


def default_dir() -> Path:
    return report.state_root() / "debug"


def _zip(files: dict[str, Entry], readme: str, path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle, zipfile.ZipFile(handle, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("README.txt", readme)
            for name in sorted(files):
                archive.writestr(name, files[name].data)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
    return path.stat().st_size


def build(out_dir: Path | None = None, *, deadline_s: float | None = None,
          uncompressed_cap: int = UNCOMPRESSED_CAP, send_cap: int = SEND_CAP, relay_cap: int = RELAY_CAP,
          collection: Collection | None = None) -> Bundle:
    """Collect, trim to the caps, and write `probe-debug-<date>-<time>.zip`."""
    collection = collection or collect(deadline_s=deadline_s)
    files = collection.files
    trimmed: dict[str, str] = {}
    total = sum(len(e.data) for e in files.values())
    if total > uncompressed_cap:
        for path in trim(files, total - uncompressed_cap):
            trimmed[path] = f"oldest lines dropped to fit the {uncompressed_cap // (1024 * 1024)} MiB cap"
    folder = Path(out_dir) if out_dir is not None else default_dir()
    if out_dir is None:
        folder.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            os.chmod(folder, 0o700)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime(collection.started_at))
    path = folder / f"probe-debug-{stamp}.zip"
    size = _zip(files, _readme(collection, trimmed), path)
    for _attempt in range(6):
        uncompressed = sum(len(e.data) for e in files.values())
        if size <= send_cap and size + uncompressed <= relay_cap:
            break
        # Shrink the logs by the overshoot (plus a margin), in uncompressed bytes.
        ratio = min(send_cap / size, (relay_cap - min(size, send_cap)) / max(uncompressed, 1))
        excess = int(uncompressed * (1 - ratio * 0.9))
        for log in trim(files, excess):
            trimmed[log] = (f"oldest lines dropped to fit the {send_cap // (1024 * 1024)} MiB zip and "
                            f"{relay_cap // (1024 * 1024)} MiB zip-plus-contents caps")
        size = _zip(files, _readme(collection, trimmed), path)
    if out_dir is None:
        _prune(folder)
    return Bundle(path=path, bytes=size, files=len(files) + 1, skipped=sorted(collection.skipped),
                  harnesses=collection.harnesses, session_ids=collection.session_ids)


def _prune(folder: Path) -> None:
    try:
        zips = sorted(folder.glob("probe-debug-*.zip"), key=lambda p: (p.stat().st_mtime, p.name), reverse=True)
    except OSError:
        return
    for old in zips[KEEP_BUNDLES:]:
        with contextlib.suppress(OSError):
            old.unlink()


# ---------------------------------------------------------------------------
# Sending
# ---------------------------------------------------------------------------


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def contents_bytes(path: Path) -> int:
    """The zip's uncompressed size: what the server's upload relay inspects
    beside the zip itself."""
    with zipfile.ZipFile(path) as archive:
        return sum(info.file_size for info in archive.infolist())


def upload(slot: dict, path: Path, *, timeout: float = UPLOAD_PUT_TIMEOUT_S) -> report.Reply:
    """The zip, sent with exactly the slot's method, URL and headers (no
    credential of ours: the slot carries its own capability). Never raises."""
    import httpx

    method = str(slot.get("method") or "PUT").upper()
    url = slot.get("url")
    headers = {str(k): str(v) for k, v in (slot.get("headers") or {}).items()
               if str(k).lower() != "content-length"}
    if not isinstance(url, str) or not url:
        return report.Reply(status=None, failure=Failure.SERVER)
    try:
        # Streamed with its length declared (a chunked PUT is refused): the
        # zip's exact size, which is also the `bytes` the slot was asked for.
        headers["Content-Length"] = str(path.stat().st_size)
        handle = open(path, "rb")  # noqa: SIM115 -- closed below
    except OSError:
        return report.Reply(status=None, failure=Failure.SERVER)
    try:
        from probe.sdk.tls import ssl_context

        with handle, httpx.Client(timeout=httpx.Timeout(timeout, connect=5.0), verify=ssl_context(),
                                  follow_redirects=False) as http:
            response = http.request(method, url, content=iter(lambda: handle.read(1 << 20), b""), headers=headers)
    except Exception:  # noqa: BLE001 -- no connection (DNS, TLS setup, a dropped link): offline
        return report.Reply(status=None, failure=Failure.OFFLINE)
    if response.status_code >= 400:
        failure = upload_failure(response.status_code)
        retry = response.headers.get("Retry-After")
        return report.Reply(status=response.status_code, failure=failure,
                            retry_after=float(retry) if retry and retry.isdigit() else None)
    return report.Reply(status=response.status_code, body={})


def upload_failure(status: int) -> Failure:
    """The contract's word for a refused PUT: 413 and 422 (the relay's
    inspection refused it) too large; 401 (the slot expired: a retry gets a new
    one, the login is fine), 403 (the team is gone), 408, 503 and the rest the
    server."""
    if status in (413, 422):
        return Failure.TOO_LARGE
    if status == 429:
        return Failure.RATE_LIMITED
    return Failure.SERVER


class Stage(StrEnum):
    """Which step of a send an answer came from."""

    CHECK = "check"
    CREATE = "create"
    UPLOAD = "upload"
    COMPLETE = "complete"


def send(bundle: Bundle) -> dict:
    """Upload a built bundle; the contract's last-line object either way."""
    return send_with_stage(bundle)[0]


def send_with_stage(bundle: Bundle) -> tuple[dict, Stage | None]:
    """`send`, with the step a failure came from (a 401 at UPLOAD is an
    expired slot, not a signed-out machine). Never raises: whatever goes wrong
    still answers the contract's object."""
    try:
        return _send(bundle)
    except Exception:  # noqa: BLE001 -- a bug or a local failure still answers
        return _failed(report.Reply(status=None, failure=Failure.SERVER), bundle), Stage.CHECK


def _send(bundle: Bundle) -> tuple[dict, Stage | None]:
    try:
        size = bundle.path.stat().st_size
        contents = contents_bytes(bundle.path)
        digest = _sha256(bundle.path)
    except (OSError, zipfile.BadZipFile):
        return _failed(report.Reply(status=None, failure=Failure.SERVER), bundle), Stage.CHECK
    # Past every trim: the server would answer 413, or its relay 422 after the
    # whole upload. Said before anything is sent.
    if size > SEND_CAP or size + contents > RELAY_CAP:
        return _failed(report.Reply(status=None, failure=Failure.TOO_LARGE), bundle), Stage.CHECK
    body = {
        "schema": SCHEMA,
        "bytes": size,
        "sha256": digest,
        "cli_version": report._cli_version()[:report.VERSION_MAX_CHARS],  # noqa: SLF001
        "os": report.os_label(),
        "harnesses": bundle.harnesses,
        "session_ids": bundle.session_ids,
    }
    app = (os.environ.get(APP_VERSION_ENV) or "").strip()
    if app:
        body["app_version"] = app[:report.VERSION_MAX_CHARS]
    created = report.api_call(lambda transport: transport.request("POST", ROUTE, json_body=body, idempotent=False))
    if not created.ok:
        return _failed(created, bundle), Stage.CREATE
    slot = (created.body or {}).get("upload")
    bundle_id = (created.body or {}).get("id")
    if not isinstance(slot, dict) or not isinstance(bundle_id, str) or not bundle_id:
        return _failed(report.Reply(status=created.status, failure=Failure.SERVER), bundle), Stage.CREATE
    put = upload(slot, bundle.path)
    if not put.ok:
        return _failed(put, bundle), Stage.UPLOAD
    done = report.api_call(
        lambda transport: transport.request("POST", f"/v1/diagnostics/bundles/{bundle_id}/complete",
                                            idempotent=False),
        tokens=[created.token] if created.token else None,
    )
    if not done.ok:
        return _failed(done, bundle), Stage.COMPLETE
    return {"id": bundle_id, "bytes": size, "files": bundle.files, "skipped": bundle.skipped,
            "path": str(bundle.path)}, None


def _failed(reply: report.Reply, bundle: Bundle | None) -> dict:
    return {"error": (reply.failure or Failure.SERVER).value, "status": reply.status,
            "retry_after": reply.retry_after, "path": str(bundle.path) if bundle else None}
