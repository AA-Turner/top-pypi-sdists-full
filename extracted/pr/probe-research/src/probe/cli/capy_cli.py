"""`probe capy`: capture the researcher's Capy threads as Probe sessions.

Capy (capy.ai) is a coding agent whose loop runs on Capy's servers (registry
family `cloud`); its tools run on this computer (a thread on "This Mac") or on
a Capy machine. It runs no Probe hook and leaves no transcript here, so capture
pulls its threads from Capy's API instead:

  probe capy connect     takes the researcher's own Capy API key (from
                         $CAPY_API_KEY, --api-key-stdin or a hidden prompt,
                         never argv), finds their Capy user by their Probe
                         account's email, records the Capy projects to capture,
                         pairs a capture credential for the `capy` source (one
                         browser approval) or checks the one it has, and
                         installs a timer that runs `probe capy sync` every
                         SYNC_INTERVAL_SECONDS (the first sync starts then).
  probe capy sync        pulls new messages into the local mirror files
                         (cli/capy_discovery.py) and uploads them through the
                         shared upload journal, exactly as live capture uploads
                         any other agent's transcript (tap_core).
  probe capy status      what is connected, when the last sync ran, what failed.
  probe capy disconnect  stops it: removes the timer, the key, the sync record
                         and the capture credential (the server is told the
                         device is done).

The installer treats Capy like every other coding agent (`npx probe-research
install --agent capy`, or Capy ticked in its picker): it asks for the key and
the projects before it starts (`prepare`), then runs `connect` with them, and
prints the steps that put Probe inside Capy (`setup_steps`), which nothing on
this machine can do for it. Turning capture off, signing out and uninstalling
call `capture_off` / `disconnect` (`setup.release_credentials`), and the capture
plugin's session start runs a catch-up sync (`tap/cloud_catchup.py`).

Nothing here writes to Capy: every Capy call is a GET.

THE KEY. A Capy API key acts as its owner with their full role (Capy has no
per-key scopes). It is stored owner-only (0600) beside the capture credential
and sent to Capy's API and nowhere else. Use a key with an expiry.

OFF MEANS OFF. A `.disabled` killswitch in the capy capture folder (the same
contract every uploader honours) stops every sync before it reads anything,
and so does a capture credential Probe refused, until `connect` runs again.

OFFLINE IS NOT LOSS. Capy keeps every transcript and its read cursors never
expire, so a machine that was asleep for a week catches up on its next sync.
"""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import typer

from ..sdk.durable import now_iso, write_text_atomic
from . import capy_discovery as discovery

#: This harness's registry id (and its upload route's source).
SOURCE = "capy"
#: Where `connect` reads the key from (never stored from the environment).
ENV_API_KEY = "CAPY_API_KEY"

#: How often the timer syncs, and how long one sync may run before the
#: scheduler stops it (a hung sync must never block the next).
SYNC_INTERVAL_SECONDS = 600
SYNC_TIMEOUT_SECONDS = 30 * 60
#: A last sync older than this, with the timer installed, reads as stalled.
STALE_AFTER_SECONDS = 60 * 60
#: At most this many batches per session per sync; the rest waits for the next.
MAX_BATCHES_PER_SESSION = 64

TIMER_NAME = "probe-capy-sync"
LAUNCHD_LABEL = "ai.prbe.probe-capy-sync"
#: The environment a sync needs from the shell `connect` ran in, carried into
#: the timer (systemd and launchd start jobs with an almost empty one).
TIMER_ENV = (
    "HTTPS_PROXY", "HTTP_PROXY", "ALL_PROXY", "NO_PROXY",
    "https_proxy", "http_proxy", "all_proxy", "no_proxy",
    "REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "SSL_CERT_DIR",
    "PROBE_BASE_URL", "PROBE_CONFIG_PATH", "XDG_CONFIG_HOME", "XDG_STATE_HOME",
    "PROBE_TRANSCRIPT_STATE_DIR", "PROBE_CAPY_API_BASE", "PROBE_CAPY_THREADS_DIR",
    "PROBE_CAPY_TAP_PLUGIN_DIR",
)
# Never a credential: the capture token is read from its 0600 file at each
# sync, and the timer's own files are written owner-only all the same (a proxy
# URL may carry a password).


class TimerMode(str, Enum):
    SYSTEMD = "systemd"
    LAUNCHD = "launchd"
    CRON = "cron"  # printed for the researcher to add; not managed here


capy_app = typer.Typer(
    no_args_is_help=True,
    help="Capy (capy.ai): capture your Capy threads as Probe sessions",
)


# --- where things live ---------------------------------------------------------


def _harness():
    from probe.harness import get_registry

    return get_registry().get(SOURCE)


def state_dir() -> Path:
    """The capture state folder of the `capy` row (its capture credential, the
    Capy key, the sync record)."""
    from . import capabilities

    return capabilities.tap_plugin_dir(SOURCE)


def mirror_root() -> Path:
    """Where the mirror files go: the row's transcript root."""
    return _harness().transcript_root()


def config_path() -> Path:
    return state_dir() / "capy.json"


def sync_state_path() -> Path:
    return state_dir() / "sync-state.json"


def killswitch_path() -> Path:
    return state_dir() / ".disabled"


def refused_path() -> Path:
    """Written by a sync Probe refused the capture credential at, naming that
    destination; `connect` removes it. A file of its own, so `connect` never
    rewrites the sync record a running sync owns."""
    return state_dir() / "credential-refused"


def _lock_path() -> Path:
    return state_dir() / "sync.lock"


def _private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    with contextlib.suppress(OSError):
        os.chmod(path, 0o700)


def _write_private_json(path: Path, value: dict) -> None:
    _private_dir(path.parent)
    write_text_atomic(path, json.dumps(value, indent=2, sort_keys=True) + "\n", mode=0o600)


def _read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


@dataclass
class CapyConfig:
    api_key: str
    me_id: str
    me_email: str | None
    projects: list[dict]
    connected_at: str | None = None
    timer: str | None = None
    #: The Probe server capture was paired with. A sync from a shell that
    #: points Probe elsewhere ($PROBE_BASE_URL at staging, say) sends nothing:
    #: the capture credential and the threads belong to this one.
    base_url: str | None = None

    @property
    def project_ids(self) -> list[str]:
        return [str(p["id"]) for p in self.projects if p.get("id")]


def load_config() -> CapyConfig | None:
    raw = _read_json(config_path())
    if not raw.get("api_key") or not raw.get("me_id"):
        return None
    known = {f.name for f in dataclasses.fields(CapyConfig)}
    values = {k: v for k, v in raw.items() if k in known}
    values["projects"] = [p for p in values.get("projects") or [] if isinstance(p, dict)]
    return CapyConfig(**values)


def save_config(config: CapyConfig) -> None:
    _write_private_json(config_path(), dataclasses.asdict(config))


# --- upload --------------------------------------------------------------------


@dataclass
class UploadReport:
    batches: int = 0
    bytes_sent: int = 0
    deleted: int = 0
    errors: list[str] = field(default_factory=list)
    credential_refused: bool = False


#: The `safe_message` the journal gives a 401/403 (`session_journal._request_failure`).
_REFUSED = re.compile(r"^HTTP 40[13]\b")


def _file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return -1


def destination_key(token: str, base_url: str) -> str:
    """Which Probe destination an `uploaded` record speaks for: a new capture
    credential or another server is a different destination, and nothing
    recorded against the old one may skip the new one's receipts."""
    return hashlib.sha256(f"{base_url}\n{token}".encode()).hexdigest()[:16]


def upload(
    sessions: list[discovery.MirroredSession],
    *,
    token: str,
    base_url: str,
    uploaded: dict,
    wire: Any = None,
) -> UploadReport:
    """Send each mirror's new lines through the shared upload journal.

    Live semantics, as the tap's own loop: each session is reserved live
    against the server's current receipts (so a stream another machine moved
    on is adopted, never contradicted), its new complete lines staged and
    delivered in batches, and a finished one (archived, done, or quiet for a
    day) frozen and finalized; new messages later reopen it. `uploaded`
    (session id -> {"size", "finished"}) records what already went to THIS
    destination, so an idle session costs no request. Mutated in place.
    """
    from probe.sdk.tls import ssl_context

    from ..tap_core.session_identity import validate_identity
    from ..tap_core.session_journal import (
        DeliveryPending,
        Journal,
        ProtocolRestarted,
        ReconciliationRequired,
        SessionDeleted,
        SourceRewritten,
        Wire,
        recoverable,
    )

    report = UploadReport()
    pending = [
        s for s in sessions
        if (uploaded.get(s.session_id) or {}) != {"size": _file_size(s.path), "finished": s.finished}
    ]
    if not pending:
        return report
    wire = wire or Wire(base_url, token, SOURCE, context=ssl_context())
    for session in pending:
        sid = session.session_id
        journal = None
        try:
            remote = wire.receipts(sid)
            # One journal per session: its live ownership is released as soon
            # as the session is done, never held for the whole sync.
            journal = Journal(wire.base_url, remote["customer_id"], SOURCE)
            if journal.is_deleted(sid):
                report.deleted += 1
                uploaded[sid] = {"size": _file_size(session.path), "finished": session.finished}
                continue
            if not journal.claim_live(sid):
                report.errors.append(f"session {sid}: another sync holds it; left for the next one")
                continue
            journal.ensure(
                sid,
                session.path,
                remote,
                historical=False,
                provenance=validate_identity(session.path, SOURCE, sid),
                cwd=session.cwd,
            )
            if session.finished:
                journal.ensure(
                    sid, session.path, wire.receipts(sid),
                    historical=True, cwd=session.cwd, complete_lines_only=True,
                )
                journal.update(sid, finalize_requested=True)
            complete = False
            for _ in range(MAX_BATCHES_PER_SESSION):
                state = journal.get(sid) or {}
                try:
                    body = journal.stage(
                        sid,
                        cwd=session.cwd,
                        finalize=bool(state.get("finalize_requested")),
                        historical_only=not state.get("live_enabled", False),
                    )
                    if body is None:
                        complete = True
                        break
                    journal.deliver(sid, wire)
                except ProtocolRestarted:
                    continue
                except ReconciliationRequired as exc:
                    if not recoverable(exc) or journal.reconcile_pending(sid, wire) is None:
                        raise
                    continue
                report.batches += 1
                report.bytes_sent += len(body)
            journal.release_snapshot(sid)
            if complete:
                uploaded[sid] = {"size": _file_size(session.path), "finished": session.finished}
            # Otherwise the batch budget ran out: the next sync goes on.
        except SessionDeleted:
            if journal is not None:
                with contextlib.suppress(sqlite3.Error, OSError):
                    journal.mark_deleted(sid, session.path)
            report.deleted += 1
            uploaded[sid] = {"size": _file_size(session.path), "finished": session.finished}
        except SourceRewritten:
            report.errors.append(f"session {sid}: its mirror changed under the upload; skipped")
        except DeliveryPending as exc:
            message = exc.safe_message or "delivery pending"
            if _REFUSED.match(message):
                report.credential_refused = True
            report.errors.append(f"session {sid}: {message}")
        except (ReconciliationRequired, OSError, sqlite3.Error) as exc:
            report.errors.append(f"session {sid}: {getattr(exc, 'safe_message', None) or type(exc).__name__}")
        except Exception as exc:  # noqa: BLE001 -- one session's failure never stops the others
            report.errors.append(f"session {sid}: failed ({type(exc).__name__})")
        finally:
            if journal is not None:
                journal.close()
    return report


# --- one sync ------------------------------------------------------------------


class Skip(str, Enum):
    """Why a sync read nothing."""

    NOT_CONNECTED = "not connected: run `probe capy connect`"
    NOT_PAIRED = "capture is not paired for Capy: run `probe capy connect` again"
    TURNED_OFF = "capture is turned off for Capy on this machine (.disabled); `probe capy connect` turns it back on"
    REFUSED = "Probe refused the capture credential at the last sync: run `probe capy connect` again"
    BUSY = "another sync is running"
    OTHER_SERVER = (
        "Probe points at another server than the one Capy was connected to ($PROBE_BASE_URL?); "
        "nothing was sent. `probe capy connect` pairs Capy with this one"
    )
    NO_LOCK = "could not take the sync lock"


@dataclass
class SyncReport:
    skipped: Skip | None = None
    pulled_sessions: int = 0
    new_bytes: int = 0
    threads_seen: int = 0
    threads_mine: int = 0
    upload: UploadReport = field(default_factory=UploadReport)
    errors: list[str] = field(default_factory=list)
    auth_failed: bool = False
    #: The Capy call budget ran out: the next sync goes on from here.
    budget_spent: bool = False

    @property
    def ran(self) -> bool:
        return self.skipped is None

    @property
    def reason(self) -> str | None:
        return self.skipped.value if self.skipped else None

    @property
    def ok(self) -> bool:
        return self.ran and not self.errors and not self.upload.errors and not self.auth_failed


def _try_lock():
    """The machine-wide sync lock, or a Skip saying why not."""
    from probe._shared import oscompat

    _private_dir(state_dir())
    try:
        handle = open(_lock_path(), "a+")
    except OSError:
        return Skip.NO_LOCK
    try:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return Skip.BUSY
    except OSError:
        handle.close()
        return Skip.NO_LOCK
    return handle


def sync_once(*, api: discovery.CapyAPI | None = None, wire: Any = None, now: float | None = None) -> SyncReport:
    """Pull, then upload. One at a time per machine: a second sync while one is
    running does nothing (the running one covers it)."""
    from . import capabilities

    config = load_config()
    if config is None:
        return SyncReport(skipped=Skip.NOT_CONNECTED)
    if killswitch_path().exists():
        return SyncReport(skipped=Skip.TURNED_OFF)
    credential = capabilities.resolved_capture_credential(SOURCE)
    if credential is None and wire is None:
        return SyncReport(skipped=Skip.NOT_PAIRED)
    token, base_url = credential or ("", "")
    if config.base_url and base_url and base_url.rstrip("/") != config.base_url.rstrip("/"):
        return SyncReport(skipped=Skip.OTHER_SERVER)
    lock = _try_lock()
    if isinstance(lock, Skip):
        return SyncReport(skipped=lock)
    try:
        destination = destination_key(token, base_url)
        try:
            refused = refused_path().read_text(encoding="utf-8").strip()
        except OSError:
            refused = ""
        if refused == destination:
            return SyncReport(skipped=Skip.REFUSED)
        state = _read_json(sync_state_path())
        api = api or discovery.CapyAPI(
            config.api_key, max_calls=discovery.MAX_CALLS_PER_SYNC, max_seconds=discovery.MAX_SECONDS_PER_SYNC
        )
        report = SyncReport()
        # Kept after every thread that read something, and again on the way
        # out of an exception. SIGTERM (the scheduler's timeout) runs no
        # `finally`, which is why the per-thread save matters: a kill loses at
        # most one thread's record, and the mirror's recorded size makes the
        # next read check every id rather than duplicate one.
        save = lambda: _write_private_json(sync_state_path(), state)  # noqa: E731
        try:
            pulled = discovery.pull(
                api, root=mirror_root(), me=config.me_id, projects=config.project_ids,
                state=state, now=now, on_thread=save,
            )
        except (OSError, ValueError) as exc:
            pulled = discovery.PullResult(errors=[f"pull failed: {type(exc).__name__}"])
        finally:
            save()
        report.pulled_sessions = len(pulled.sessions)
        report.new_bytes = sum(s.new_bytes for s in pulled.sessions)
        report.threads_seen, report.threads_mine = pulled.threads_seen, pulled.threads_mine
        report.errors = list(pulled.errors)
        report.auth_failed = pulled.auth_failed
        report.budget_spent = pulled.budget_spent
        uploaded = state.setdefault("uploaded", {}).setdefault(destination, {})
        if pulled.sessions and killswitch_path().exists():
            # Turned off while this sync was pulling: off means nothing more is
            # sent. The mirror keeps what was read; a thread uploads with its
            # next message after capture is back on.
            report.errors.append("capture was turned off during this sync: nothing was uploaded")
        elif pulled.sessions:
            try:
                report.upload = upload(pulled.sessions, token=token, base_url=base_url, uploaded=uploaded, wire=wire)
            finally:
                save()
        if report.upload.credential_refused:
            write_text_atomic(refused_path(), destination + "\n", mode=0o600)
        state["last_sync"] = {
            "at": now_iso(),
            "ok": report.ok,
            "auth_failed": report.auth_failed,
            "credential_refused": report.upload.credential_refused,
            "errors": (report.errors + report.upload.errors)[:20],
            "sessions": report.pulled_sessions,
            "threads_seen": report.threads_seen,
            "threads_mine": report.threads_mine,
            "batches": report.upload.batches,
            "capy_calls": api.calls_made,
            "budget_spent": report.budget_spent,
        }
        _write_private_json(sync_state_path(), state)
        return report
    finally:
        lock.close()


# --- the timer -----------------------------------------------------------------


def _installed_probe() -> str | None:
    """The persistent `probe` on PATH, as PATH names it (not resolved: an
    upgrade may move the target, never the entry point), and only if it knows
    `probe capy` (an older install would fail every run)."""
    found = shutil.which("probe")
    if not found:
        return None
    try:
        ok = subprocess.run([found, "capy", "--help"], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.SubprocessError):
        ok = False
    return os.path.abspath(found) if ok else None


def _systemd_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return (Path(base) if base else Path.home() / ".config") / "systemd" / "user"


def _launchd_plist() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"


def _run(argv: list[str]) -> bool:
    try:
        return subprocess.run(argv, capture_output=True, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def _run_output(argv: list[str]) -> str:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=30).stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def _timer_env() -> dict[str, str]:
    return {name: os.environ[name] for name in TIMER_ENV if os.environ.get(name)}


def _cron_line(command: list[str]) -> str:
    """A crontab line. cron reads an unescaped `%` as a newline."""
    minutes = max(1, SYNC_INTERVAL_SECONDS // 60)
    env = " ".join(f"{k}={shlex.quote(v)}" for k, v in _timer_env().items())
    line = f"{env + ' ' if env else ''}{shlex.join(command)}".replace("%", "\\%")
    return f"*/{minutes} * * * * {line}"


def _write_private(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomic(path, data.decode("utf-8"), mode=0o600)


def install_timer() -> tuple[TimerMode | None, str]:
    """Install the periodic sync. Returns the mode (None when nothing could be
    set up) and one line saying what was done."""
    probe = _installed_probe()
    if probe is None:
        return None, (
            "No timer installed: no `probe` with `probe capy` on PATH (this may be a "
            "throwaway copy). Install the CLI (`uv tool install probe-research`), then run "
            "`probe capy connect` again."
        )
    command = [probe, "capy", "sync", "--quiet"]
    minutes = max(1, SYNC_INTERVAL_SECONDS // 60)
    system = platform.system()
    if system == "Darwin":
        import plistlib

        plist = _launchd_plist()
        _write_private(
            plist,
            plistlib.dumps(
                {
                    "Label": LAUNCHD_LABEL,
                    "ProgramArguments": command,
                    "StartInterval": SYNC_INTERVAL_SECONDS,
                    "RunAtLoad": True,
                    "EnvironmentVariables": _timer_env(),
                    "StandardOutPath": str(state_dir() / "timer.log"),
                    "StandardErrorPath": str(state_dir() / "timer.log"),
                }
            )
        )
        _run(["launchctl", "unload", str(plist)])
        if _run(["launchctl", "load", "-w", str(plist)]):
            return TimerMode.LAUNCHD, f"Syncs every {minutes} minutes (launchd: {LAUNCHD_LABEL}); the first one starts now."
        return None, f"Wrote {plist}; load it with `launchctl load -w {plist}`."
    if system == "Linux" and shutil.which("systemctl"):
        unit_dir = _systemd_dir()
        unit_dir.mkdir(parents=True, exist_ok=True)
        env_lines = "".join(
            f"Environment={_systemd_quote(f'{k}={v}')}\n" for k, v in _timer_env().items()
        )
        _write_private(
            unit_dir / f"{TIMER_NAME}.service",
            (
                "[Unit]\n"
                "Description=Probe: capture Capy threads\n\n"
                "[Service]\n"
                "Type=oneshot\n"
                f"TimeoutStartSec={SYNC_TIMEOUT_SECONDS}\n"
                f"{env_lines}"
                f"ExecStart={' '.join(_systemd_quote(part) for part in command)}\n"
            ).encode("utf-8"),
        )
        (unit_dir / f"{TIMER_NAME}.timer").write_text(
            "[Unit]\n"
            f"Description=Probe: capture Capy threads every {minutes} minutes\n\n"
            "[Timer]\n"
            f"OnCalendar=*:0/{minutes}\n"
            "Persistent=true\n\n"
            "[Install]\n"
            "WantedBy=timers.target\n",
            encoding="utf-8",
        )
        if _run(["systemctl", "--user", "daemon-reload"]) and _run(
            ["systemctl", "--user", "enable", "--now", f"{TIMER_NAME}.timer"]
        ):
            _run(["systemctl", "--user", "start", "--no-block", f"{TIMER_NAME}.service"])
            line = f"Syncs every {minutes} minutes (systemd user timer {TIMER_NAME}); the first one starts now."
            if "Linger=no" in _run_output(["loginctl", "show-user", os.environ.get("USER", ""), "-p", "Linger"]):
                line += (
                    " Your user services stop when you log out; to keep syncing, run "
                    "`loginctl enable-linger`."
                )
            return TimerMode.SYSTEMD, line
        return None, (
            f"Wrote {unit_dir / (TIMER_NAME + '.timer')}, but could not enable it (no user "
            f"session bus?). Start it with `systemctl --user enable --now {TIMER_NAME}.timer`."
        )
    return TimerMode.CRON, (
        f"No scheduler to manage here. Add this to your crontab to sync every {minutes} minutes:\n"
        f"  {_cron_line(command)}"
    )


def _systemd_quote(part: str) -> str:
    """One systemd unit word: `%` doubled (systemd reads `%x` as a specifier),
    quoted when it holds a space, quote or backslash."""
    part = part.replace("%", "%%")
    if not any(c in part for c in ' "\\'):
        return part
    return '"' + part.replace("\\", "\\\\").replace('"', '\\"') + '"'


def remove_timer(mode: str | None) -> str | None:
    """Remove the timer `connect` installed. Returns a line for the researcher
    when they must remove one by hand (a crontab line)."""
    if mode == TimerMode.CRON.value:
        return "Remove the `probe capy sync` line from your crontab (`crontab -e`)."
    if platform.system() == "Darwin":
        plist = _launchd_plist()
        if plist.exists():
            _run(["launchctl", "unload", "-w", str(plist)])
            plist.unlink(missing_ok=True)
        return None
    unit_dir = _systemd_dir()
    if (unit_dir / f"{TIMER_NAME}.timer").exists() and shutil.which("systemctl"):
        _run(["systemctl", "--user", "disable", "--now", f"{TIMER_NAME}.timer"])
        # And a sync already running: disabling the timer leaves its service be.
        _run(["systemctl", "--user", "stop", f"{TIMER_NAME}.service"])
    for suffix in (".timer", ".service"):
        (unit_dir / f"{TIMER_NAME}{suffix}").unlink(missing_ok=True)
    if shutil.which("systemctl"):
        _run(["systemctl", "--user", "daemon-reload"])
    return None


def timer_state(mode: str | None) -> str:
    """How the timer reads now: installed, manual (cron), or not installed."""
    if mode == TimerMode.CRON.value:
        return "manual (a crontab line you added)"
    if platform.system() == "Darwin":
        return "installed" if _launchd_plist().exists() else "not installed"
    if not (_systemd_dir() / f"{TIMER_NAME}.timer").exists():
        return "not installed"
    if shutil.which("systemctl") and not _run(["systemctl", "--user", "is-enabled", f"{TIMER_NAME}.timer"]):
        return "installed but not enabled"
    return "installed"


# --- facts for status and doctor ---------------------------------------------


def _age_seconds(stamp: Any) -> float | None:
    from datetime import datetime

    try:
        return time.time() - datetime.fromisoformat(str(stamp)).timestamp()
    except (TypeError, ValueError):
        return None


def doctor_facts() -> list[tuple[str, str]]:
    """What `probe doctor` and `probe capy status` show about Capy capture,
    from local files only. Empty when this machine never connected Capy."""
    from . import capabilities

    config = load_config()
    if config is None:
        return []
    credential = capabilities.resolved_capture_credential(SOURCE)
    paired = credential is not None
    try:
        refused = refused_path().read_text(encoding="utf-8").strip()
    except OSError:
        refused = ""
    refused = bool(credential) and refused == destination_key(*credential)
    last = _read_json(sync_state_path()).get("last_sync") or {}
    timer = timer_state(config.timer)
    facts = [
        ("Connected as", config.me_email or config.me_id),
        ("Projects", ", ".join(str(p.get("name") or p.get("id")) for p in config.projects) or "none"),
        ("Capture", "paired" if paired else "NOT paired -- run `probe capy connect`"),
        ("Timer", timer if timer != "not installed" else "not installed -- run `probe capy connect`"),
    ]
    if killswitch_path().exists():
        facts.append(("Capture", "turned off on this machine (.disabled)"))
    if not last:
        facts.append(("Last sync", "never"))
        return facts
    at = last.get("at")
    if last.get("auth_failed"):
        facts.append(("Last sync", f"{at}: Capy refused the key -- run `probe capy connect`"))
    elif refused:
        facts.append(("Last sync", f"{at}: Probe refused the capture credential -- run `probe capy connect`"))
    elif last.get("credential_refused"):
        facts.append(("Last sync", f"{at}: the capture credential was refused; reconnected since"))
    elif not last.get("ok"):
        first = (last.get("errors") or ["see `probe capy status`"])[0]
        facts.append(("Last sync", f"{at}: {first}"))
    else:
        facts.append(("Last sync", f"{at} (ok)"))
    age = _age_seconds(at)
    if timer == "installed" and age is not None and age > STALE_AFTER_SECONDS:
        facts.append(("Stalled", f"no sync for {int(age // 60)} minutes though the timer is installed"))
    if last.get("threads_seen") and not last.get("threads_mine"):
        facts.append(("Threads", f"none of the {last['threads_seen']} threads seen are yours ({config.me_email})"))
    return facts


# --- commands ------------------------------------------------------------------


def _probe_account() -> dict:
    """The signed-in Probe account (`/v1/me`): {} when it cannot be read."""
    from probe.sdk.client import Client
    from probe.sdk.config import resolve
    from probe.sdk.surface import Surface

    try:
        settings = resolve()
        if not settings.token:
            return {}
        with Client(settings=settings, async_writes=False, surface=Surface.CLI.value) as client:
            me = client.me()
    except Exception:  # noqa: BLE001 -- connect explains what it could not read
        return {}
    return me if isinstance(me, dict) else {}


#: `_capture_customer`'s answer when the server could not be asked (offline, a
#: 5xx): not evidence the credential belongs to another team.
UNREACHABLE = "unreachable"


def _capture_customer(token: str, base_url: str) -> str | None:
    """The team a capture credential uploads to (its receipts answer names it),
    None when the credential is refused, or UNREACHABLE when the server could
    not answer."""
    from probe.sdk.tls import ssl_context

    from ..tap_core.session_journal import DeliveryPending, ReconciliationRequired, Wire

    try:
        return Wire(base_url, token, SOURCE, context=ssl_context()).receipts(str(uuid.uuid4()))["customer_id"]
    except DeliveryPending as exc:
        # Only a server that could not answer (408/429/5xx, a dropped
        # connection) is unreachable; a 401/403 is a refused credential.
        return UNREACHABLE if exc.retryable else None
    except (ReconciliationRequired, KeyError):
        return None


def _choose_projects(available: list[dict], wanted: list[str], interactive: bool) -> list[dict]:
    if wanted:
        chosen = []
        for name in wanted:
            needle = name.strip().lower()
            match = next(
                (
                    p for p in available
                    if str(p.get("id") or "").lower() == needle
                    or str(p.get("name") or "").strip().lower() == needle
                ),
                None,
            )
            if match is None:
                raise typer.BadParameter(f"no Capy project named {name!r}", param_hint="--project")
            chosen.append(match)
        return chosen
    if not interactive:
        names = ", ".join(str(p.get("name") or p.get("id")) for p in available) or "(none)"
        raise typer.BadParameter(
            f"name the Capy projects to capture (your projects: {names})", param_hint="--project"
        )
    for index, project in enumerate(available, 1):
        typer.echo(f"  {index}. {project.get('name') or project.get('id')}")
    answer = typer.prompt("Capture which projects? (numbers, comma-separated, or 'all')")
    if answer.strip().lower() == "all":
        return list(available)
    picked = []
    for token in answer.replace(" ", "").split(","):
        if token.isdigit() and 1 <= int(token) <= len(available):
            picked.append(available[int(token) - 1])
    if not picked:
        raise typer.BadParameter("no project chosen")
    return picked


class ConnectRefused(Exception):
    """`connect` could not finish; the message says why, in the user's terms."""


class KeyRefused(ConnectRefused):
    """Capy refused the API key."""


class CapyUnreachable(ConnectRefused):
    """Capy's API could not be reached (the key may be fine)."""


class NoProjectChosen(ConnectRefused):
    """The researcher picked no project: their decision, not a failure."""


class ProjectsUnnamed(ConnectRefused):
    """A run with no terminal named no project (--project / --capy-project)."""


class ProjectNotFound(ConnectRefused):
    """A named project is not one of the key's Capy projects."""


class EmailNotFound(ConnectRefused):
    """No member of the Capy organization has the Probe account's email."""


@dataclass
class CapturePlan:
    """What connecting needs from the researcher, asked BEFORE any setup runs
    (`prepare`): the key Capy accepted, the projects they chose, and the
    organization's members (their Capy user is found among them by their Probe
    email once they are signed in). The installer asks for it on its review
    screen, so no human wait counts against its apply budget."""

    key: str
    projects: list[dict]
    users: list[dict]

    def __repr__(self) -> str:  # never print the key
        return f"CapturePlan(projects={[p.get('name') or p.get('id') for p in self.projects]!r})"


@dataclass
class Connected:
    config: CapyConfig
    team: str | None
    mode: TimerMode | None
    lines: list[str]
    #: The first sync `connect` ran because no system timer will (None when a
    #: timer will, or when it was told not to).
    report: SyncReport | None = None


def prepare(key: str, *, choose: Callable[[list[dict]], list[dict]]) -> CapturePlan:
    """Check the key with Capy and ask `choose` which projects to capture.
    Raises ConnectRefused with a message for the researcher."""
    api = discovery.CapyAPI(key)
    try:
        projects = api.projects()
        users = api.users()
    except discovery.CapyAuthError:
        raise KeyRefused("Capy refused that key. Check it under Capy Settings > API.") from None
    except discovery.CapyError as exc:
        raise CapyUnreachable(f"Could not reach Capy: {exc}") from None
    chosen = choose(projects)
    if not chosen:
        raise NoProjectChosen("No Capy project chosen, so nothing was connected.")
    return CapturePlan(key=key, projects=list(chosen), users=list(users))


def _email_refusal(email: str) -> EmailNotFound:
    return EmailNotFound(
        f"No member of this Capy organization has the email {email} (your Probe "
        "account's). Capture only takes your own threads, so it needs the same email "
        "on both."
    )


def connect(
    plan: CapturePlan,
    *,
    open_browser: bool = True,
    on_prompt: Callable[[Any], None] | None = None,
    timer: bool = True,
    first_sync: bool = True,
) -> Connected:
    """Everything `probe capy connect` does after `prepare`, for the command
    and the installer.

    Finds the researcher's Capy user by their Probe account's email, pairs (or
    re-checks) the capture credential for the `capy` source, turns capture back
    on, saves the connection and installs the timer. When no system timer will
    run (cron, or none could be installed) it syncs once right away, so
    connecting never leaves a connection that has uploaded nothing
    (`first_sync=False` skips that). Raises ConnectRefused with a message for
    the researcher; returns what was done as lines to show.
    """
    from probe.sdk.config import resolve

    from . import capabilities, setup

    lines: list[str] = []
    account = _probe_account()
    email = str(account.get("email") or "").strip()
    if not email:
        raise ConnectRefused("Sign in to Probe first (`probe login`): your Capy user is found by your Probe email.")

    # Only the researcher's own threads are captured, so "me" is never a
    # choice: it is the Capy member with the Probe account's email.
    user = discovery.resolve_me(plan.users, email=email)
    if user is None:
        raise _email_refusal(email)

    credential = capabilities.resolved_capture_credential(SOURCE)
    team = account.get("customer_id")
    owner = _capture_customer(*credential) if credential is not None else None
    if credential is not None and (
        owner not in (team, UNREACHABLE) or (owner == UNREACHABLE and _stopped_for_another_account())
    ):
        # Refused, revoked, or another team's: a fresh approval replaces it.
        # An unreachable server is not evidence of either -- unless capture was
        # stopped because the credential belongs to another team, which only a
        # fresh approval for this account may lift.
        credential = None
    if credential is None:
        _, messages = setup.authorize(
            ["capture"],
            base_url=resolve().base_url,
            capture_sources=[SOURCE],
            open_browser=open_browser,
            on_prompt=on_prompt,
        )
        lines.extend(messages)
        if capabilities.resolved_capture_credential(SOURCE) is None:
            raise ConnectRefused("Capture was not approved, so nothing was connected.")
    killswitch_path().unlink(missing_ok=True)
    refused_path().unlink(missing_ok=True)  # a refused credential's verdict no longer applies

    paired = capabilities.resolved_capture_credential(SOURCE)
    config = CapyConfig(
        api_key=plan.key,
        me_id=str(user["id"]),
        me_email=user.get("email"),
        projects=[{"id": p.get("id"), "name": p.get("name")} for p in plan.projects],
        connected_at=now_iso(),
        base_url=paired[1] if paired else None,
    )
    names = ", ".join(str(p.get("name") or p.get("id")) for p in plan.projects)
    lines.append(
        f"Connected as {config.me_email}; capturing threads you start in {names}, "
        f"into Probe team {team}."
    )
    mode = None
    if timer and capabilities.TokenSource.PAIRED_FILE not in capabilities.capture_token_sources(SOURCE):
        # The timer runs without this shell's environment (and never carries a
        # credential), so a token set only in $PROBE_CAPY_TAP_TOKEN is one it
        # cannot see: every timed sync would say "not paired".
        lines.append(
            "No timer installed: the capture credential comes from $PROBE_CAPY_TAP_TOKEN, "
            "which the timer cannot see. Unset it and run `probe capy connect` to pair this "
            "machine, or run `probe capy sync` yourself."
        )
    elif timer:
        mode, line = install_timer()
        lines.append(line)
    config.timer = mode.value if mode else None
    save_config(config)
    report = None
    if mode in (TimerMode.SYSTEMD, TimerMode.LAUNCHD):
        lines.append("The first sync can take a while for a long history: `probe capy status` shows it.")
    elif first_sync:
        report = sync_once()
        lines.extend(report_lines(report))
    return Connected(config=config, team=team, mode=mode, lines=lines, report=report)


def capture_off(*, uninstall: bool) -> list[str]:
    """Turn Capy capture off on this machine: `uninstall` disconnects (timer,
    key, sync record and credential gone); otherwise the `.disabled` killswitch
    stops every sync and `probe capy connect` (or the installer) turns it back
    on. Returns what to tell the researcher."""
    if uninstall:
        return disconnect()
    if load_config() is None:
        return []
    _turn_off("turned off by the installer")
    return [f"{label()} capture turned off; the connection is kept (`probe capy connect` turns it back on)."]


@capy_app.command("connect")
def connect_cmd(
    api_key_stdin: bool = typer.Option(
        False, "--api-key-stdin", help=f"read the Capy API key from stdin (default: ${ENV_API_KEY}, else a prompt)"
    ),
    project: list[str] = typer.Option(
        None, "--project", help="a Capy project to capture (id or name); repeat for more"
    ),
    no_timer: bool = typer.Option(False, "--no-timer", help="do not install the periodic sync"),
    no_sync: bool = typer.Option(False, "--no-sync", help="with --no-timer: do not sync right away"),
    no_browser: bool = typer.Option(False, "--no-browser", help="print the approval link instead of opening it"),
) -> None:
    """Connect your Capy account: capture the threads you start, as Probe sessions."""
    from . import tui

    interactive = tui.interactive()
    if api_key_stdin:
        key = sys.stdin.readline().strip()
    else:
        key = (os.environ.get(ENV_API_KEY) or "").strip()
        if not key and interactive:
            key = typer.prompt("Capy API key", hide_input=True).strip()
    if not key:
        raise typer.BadParameter(
            f"a Capy API key is required: set ${ENV_API_KEY}, pipe it to --api-key-stdin, or run interactively"
        )

    def on_prompt(prompt) -> None:
        typer.echo("Approve capture for your Capy threads in your browser.")
        typer.echo(f"  {prompt.verification_uri_complete}")

    try:
        plan = prepare(key, choose=lambda projects: _choose_projects(projects, project or [], interactive))
        done = connect(
            plan,
            open_browser=not no_browser,
            on_prompt=on_prompt,
            timer=not no_timer,
            first_sync=not no_sync,
        )
    except ConnectRefused as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from None
    for line in done.lines:
        typer.echo(line)


def report_lines(report: SyncReport) -> list[str]:
    """What one sync did, for a person: the summary, then each problem."""
    if not report.ran:
        return [report.reason or "nothing ran"]
    up = report.upload
    lines = [
        f"Synced {report.pulled_sessions} Capy session(s) from {report.threads_mine} of your threads: "
        f"{report.new_bytes} new bytes, {up.batches} batch(es) uploaded"
        + (f", {up.deleted} deleted by your team" if up.deleted else "")
        + "."
    ]
    if report.budget_spent:
        lines.append(f"Read {discovery.MAX_CALLS_PER_SYNC} Capy pages this sync; the next sync goes on from here.")
    if report.auth_failed:
        lines.append("Capy refused the key: run `probe capy connect` with a new one.")
    if up.credential_refused:
        lines.append("Probe refused the capture credential: run `probe capy connect` again.")
    lines.extend(f"  ! {line}" for line in (report.errors + up.errors)[:10])
    return lines


def _print_report(report: SyncReport, *, quiet: bool) -> None:
    if not report.ran:
        if not (quiet and report.skipped in (Skip.BUSY, Skip.NOT_CONNECTED)):
            typer.echo(report.reason or "nothing ran", err=True)
        return
    if quiet and report.ok:
        return
    summary, *rest = report_lines(report)
    typer.echo(summary)
    for line in rest:
        typer.echo(line, err=True)


@capy_app.command("sync")
def sync_cmd(
    quiet: bool = typer.Option(False, "--quiet", help="print only problems (the timer uses this)"),
) -> None:
    """Pull your new Capy messages and upload them now."""
    report = sync_once()
    _print_report(report, quiet=quiet)
    if report.skipped is Skip.BUSY or (quiet and report.skipped is Skip.NOT_CONNECTED):
        return
    if not report.ok:
        raise typer.Exit(1)


@capy_app.command("status")
def status_cmd() -> None:
    """Show what is connected and how the last sync went."""
    facts = doctor_facts()
    if not facts:
        typer.echo("Capy: not connected (run `probe capy connect`).")
        return
    typer.echo("Capy capture")
    for label, value in facts:
        typer.echo(f"  {label + ':':<14}{value}")
    root = mirror_root()
    typer.echo(f"  {'Mirrored:':<14}{len(list(root.glob('*.jsonl'))) if root.is_dir() else 0} sessions in {root}")
    for line in (_read_json(sync_state_path()).get("last_sync") or {}).get("errors") or []:
        typer.echo(f"    ! {line}")


def connected_here() -> bool:
    """Whether anything of Capy capture is set up on this machine: the
    connection, its capture credential, or its timer."""
    return any(
        path.exists()
        for path in (
            config_path(),
            state_dir() / ".token",
            _launchd_plist(),
            _systemd_dir() / f"{TIMER_NAME}.timer",
        )
    )


def disconnect(*, keep_capture: bool = False) -> list[str]:
    """Stop capturing Capy threads on this machine. Returns what to tell the researcher."""
    from . import capabilities

    config = load_config()
    hint = remove_timer(config.timer if config else None)
    config_path().unlink(missing_ok=True)
    # The sync record is per connection: a later connect (maybe to another
    # team) re-checks every session against its own receipts.
    sync_state_path().unlink(missing_ok=True)
    refused_path().unlink(missing_ok=True)
    if not keep_capture:
        with contextlib.suppress(Exception):
            capabilities.revoke_capture_device(SOURCE)
        (state_dir() / ".token").unlink(missing_ok=True)
    lines = [
        "Capy disconnected. Sessions already uploaded stay in Probe; the local mirror files "
        f"stay in {mirror_root()} (delete them if you like)."
    ]
    if hint:
        lines.append(hint)
    return lines


@capy_app.command("disconnect")
def disconnect_cmd(
    keep_capture: bool = typer.Option(
        False, "--keep-capture", help="keep the capture credential (only remove the key, timer and sync record)"
    ),
) -> None:
    """Stop capturing Capy threads: remove the timer, the key, the sync record and the capture credential."""
    for line in disconnect(keep_capture=keep_capture):
        typer.echo(line)


# --- the installer ---------------------------------------------------------------
#
# The installer lists Capy with the other coding agents. What it cannot do for
# Capy is put Probe inside it (Capy has no command or API for its MCP servers
# or plugins), so it prints `setup_steps`; what it can do is capture, through
# `prepare` (asked on its review screen) and `connect` (run while it applies).


class CaptureOutcome(str, Enum):
    """How the installer's Capy capture step ended (and whether that leaves
    the install unfinished: `blocks`)."""

    CONNECTED = "connected"
    #: Connected before this run; nothing to ask.
    ALREADY = "already connected"
    #: The researcher chose not to give a key or a project: their decision,
    #: said on the final screen, never a failed install.
    DECLINED = "declined"
    #: A run with no terminal had no key ($CAPY_API_KEY) or no project
    #: (--capy-project): capture was asked for and could not happen.
    MISSING = "missing"
    #: Capy or Probe refused (the key, the email, the approval).
    REFUSED = "refused"

    @property
    def blocks(self) -> bool:
        return self in (CaptureOutcome.MISSING, CaptureOutcome.REFUSED)


@dataclass
class CaptureAsk:
    """The answer the installer's review screen collected for Capy capture."""

    outcome: CaptureOutcome
    plan: CapturePlan | None = None
    lines: list[str] = field(default_factory=list)

    @property
    def pairs(self) -> bool:
        """Whether this run should pair a capture credential for Capy: only
        when a connection will exist (no key, no credential)."""
        return self.outcome in (CaptureOutcome.CONNECTED, CaptureOutcome.ALREADY)


#: Where the mirror publishes the Capy bundle and its guide (agent/tools/mirror_render.py).
MIRROR_REPO = "https://github.com/prbe-ai/research-os-agent"
GUIDE_URL = f"{MIRROR_REPO}/blob/main/capy/README.md"

#: How to connect later, named in every line that skips or refuses.
CONNECT_LATER = "Run `probe capy connect` to connect it later."


def label() -> str:
    return _harness().label


#: What the steps say when the deployment's MCP URL cannot be derived.
MCP_URL_UNKNOWN = "your Probe deployment's MCP URL"

#: The mirror folder Capy adds as one plugin: Probe's MCP server and the Capy
#: skills (agent/tools/mirror_render.py `cloud_plugin` writes its manifest).
PLUGIN_URL = f"{MIRROR_REPO}/tree/main/capy"


def _deployment_mcp(base_url: str | None) -> str | None:
    """The Probe deployment's MCP URL, or None when it cannot be derived.
    `base_url` is the root `--base-url`, which outranks the environment and
    the saved config (a self-hosted manual run passes nothing else)."""
    from probe.sdk.config import mcp_url, resolve

    return mcp_url(resolve(base_url=base_url).base_url)


def _plugin_fits(mcp: str | None) -> bool:
    """The plugin carries the hosted MCP server; any other deployment adds its
    own server and the skills by hand."""
    from probe.sdk.config import STOCK_MCP_URL

    return mcp == STOCK_MCP_URL


def setup_steps(base_url: str | None = None) -> list[str]:
    """What puts Probe inside Capy: one plugin, added in Capy's settings (Capy
    has no command or API for its plugins), so the installer prints it, and
    `probe wizard --action manual` does too. The plugin's skills reach every
    thread by their descriptions, so no AGENTS.md line is needed.
    agent/docs/capy.md is the full guide."""
    mcp = _deployment_mcp(base_url) or MCP_URL_UNKNOWN
    cloud = f"Threads on this computer use its `probe`; for threads in {label()}'s cloud, see {GUIDE_URL}"
    if _plugin_fits(mcp):
        return [
            f"Add Probe to {label()} once: Settings > MCP & plugins > Add > From GitHub repository:",
            f"     {PLUGIN_URL}",
            "   then Only me > Add plugin, and Connect its probe server (approve in Probe).",
            cloud,
        ]
    return [
        f"Add Probe to {label()} once, in two steps:",
        f"1. MCP server: in {label()}, Settings > MCP & plugins > add an MCP server named probe, Streamable HTTP:",
        f"     {mcp}",
        "   then Connect and approve in Probe.",
        "2. Skills, in your repository:",
        f"     npx skills add {PLUGIN_URL}/skills --agent universal",
        cloud,
    ]


def setup_summary(base_url: str | None = None) -> list[str]:
    """`setup_steps` in lines short enough for a wizard page, which wraps a long
    line mid-URL and breaks the copy."""
    mcp = _deployment_mcp(base_url)
    if _plugin_fits(mcp):
        return [
            f"One step in {label()}: Settings > MCP & plugins > Add >",
            "From GitHub repository, paste this, Only me, Add plugin:",
            f"  {PLUGIN_URL}",
            "then Connect its probe server and approve in Probe.",
        ]
    return [
        f"Add Probe to {label()} in two steps:",
        f"1. {label()} Settings > MCP & plugins: add an MCP server named",
        "   probe, Streamable HTTP, then Connect, with this URL:",
        f"   {mcp or MCP_URL_UNKNOWN}",
        "2. Add Probe's skills to your repository.",
        f"Both, ready to copy: `probe {SOURCE} setup`.",
    ]


@capy_app.command("setup")
def setup_cmd() -> None:
    """Print how to put Probe inside Capy (the plugin with its MCP server and
    skills), ready to copy. Capy has no command for it."""
    from probe.cli.main import _conn

    for line in setup_steps(base_url=_conn.base_url):
        typer.echo(line)


def wizard_status() -> tuple[str, bool] | None:
    """One line for the wizard's "On this device" block, and whether it is a
    problem. None when Capy was never connected here."""
    from . import capabilities

    config = load_config()
    if config is None:
        return None
    if killswitch_path().exists():
        return "capture off (killswitch set)", True
    credential = capabilities.resolved_capture_credential(SOURCE)
    if credential is None:
        return "capture not paired: run `probe capy connect`", True
    try:
        refused = refused_path().read_text(encoding="utf-8").strip()
    except OSError:
        refused = ""
    if refused == destination_key(*credential):
        return "Probe refused capture: run `probe capy connect`", True
    last = _read_json(sync_state_path()).get("last_sync") or {}
    if last.get("auth_failed"):
        return "Capy refused the key: run `probe capy connect`", True
    projects = len(config.projects)
    head = f"capture on · {projects} project{'s' if projects != 1 else ''}"
    age = _age_seconds(last.get("at")) if last else None
    if age is None:
        return f"{head} · not synced yet", False
    stalled = timer_state(config.timer) == "installed" and age > STALE_AFTER_SECONDS
    ago = f"{int(age // 60)} min ago" if age < 3 * 3600 else f"{int(age // 3600)} h ago"
    return f"{head} · last sync {ago}" + (" (stalled)" if stalled else ""), stalled or not last.get("ok")


def ask_capture(*, interactive: bool, projects: list[str] | None = None) -> CaptureAsk:
    """Collect what connecting needs, before the installer applies anything.

    Connected already (and no new --capy-project): the saved key and projects
    are checked again, so a key Capy now refuses, a project gone or an account
    that changed is asked about rather than read as connected. Otherwise the
    key comes from $CAPY_API_KEY or, with a terminal, a hidden prompt (asked
    again, with the reason, when Capy refuses it; empty skips); the projects
    from `projects` (--capy-project) or, with a terminal, a picker. Without a
    terminal a missing key or project is MISSING, never a guess. The Probe
    account's email is matched to a Capy member here, before any capture
    credential exists, when this machine is already signed in."""
    config = load_config()
    problem = None
    if config is not None and not projects:
        saved = set(config.project_ids)
        try:
            plan = prepare(config.api_key, choose=lambda available: [p for p in available if str(p.get("id")) in saved])
        except CapyUnreachable:
            # Cannot check it now; the connection stays as it is.
            return CaptureAsk(CaptureOutcome.ALREADY)
        except ConnectRefused as exc:
            problem = f"The saved {label()} connection no longer works: {exc}"
            if not interactive:
                return CaptureAsk(CaptureOutcome.REFUSED, lines=[f"{problem} {CONNECT_LATER}"])
        else:
            return _checked(CaptureAsk(CaptureOutcome.ALREADY, plan=plan))
    key = (os.environ.get(ENV_API_KEY) or "").strip() or (config.api_key if config is not None and not problem else "")
    if not key and not interactive:
        return CaptureAsk(
            CaptureOutcome.MISSING,
            lines=[f"{label()} capture needs a Capy API key in ${ENV_API_KEY} and --capy-project. {CONNECT_LATER}"],
        )
    choose = (
        (lambda available: _choose_projects_or_refuse(available, projects or []))
        if projects or not interactive
        else _choose_on_screen
    )
    while True:
        if not key:
            key = _ask_key(problem)
            if not key:
                return CaptureAsk(
                    CaptureOutcome.DECLINED, lines=[f"{label()} capture skipped: no key given. {CONNECT_LATER}"]
                )
        try:
            return _checked(CaptureAsk(CaptureOutcome.CONNECTED, plan=prepare(key, choose=choose)))
        except NoProjectChosen:
            return CaptureAsk(
                CaptureOutcome.DECLINED, lines=[f"{label()} capture skipped: no project chosen. {CONNECT_LATER}"]
            )
        except ProjectsUnnamed as exc:
            return CaptureAsk(CaptureOutcome.MISSING, lines=[f"{exc} {CONNECT_LATER}"])
        except (ProjectNotFound, CapyUnreachable) as exc:
            # Not the key's fault: asking for another key would not help.
            return CaptureAsk(CaptureOutcome.REFUSED, lines=[f"{exc} {CONNECT_LATER}"])
        except ConnectRefused as exc:
            if not interactive:
                return CaptureAsk(CaptureOutcome.REFUSED, lines=[f"{exc} {CONNECT_LATER}"])
            problem, key = str(exc), ""


def _checked(ask: CaptureAsk) -> CaptureAsk:
    """Refuse a plan whose Capy organization has no member with the signed-in
    Probe account's email, before the install pairs a capture credential for a
    connection `connect` would then refuse. Not signed in yet (a website code):
    `connect` checks it, and drops the credential if it fails."""
    email = str(_probe_account().get("email") or "").strip()
    if email and ask.plan is not None and discovery.resolve_me(ask.plan.users, email=email) is None:
        return CaptureAsk(CaptureOutcome.REFUSED, lines=[f"{_email_refusal(email)} {CONNECT_LATER}"])
    return ask


def _choose_projects_or_refuse(available: list[dict], wanted: list[str]) -> list[dict]:
    """`_choose_projects` without a terminal, its refusals as ConnectRefused."""
    try:
        return _choose_projects(available, wanted, interactive=False)
    except typer.BadParameter as exc:
        refusal = ProjectNotFound if wanted else ProjectsUnnamed
        raise refusal(f"{exc.message} (--capy-project).") from None


def _ask_key(problem: str | None = None) -> str:
    from . import tui

    key = tui.secret(
        f"Capture my {label()} threads",
        # Paragraphs, not pre-wrapped lines: the screen wraps them to its width.
        [
            *([problem, ""] if problem else []),
            "Paste a Capy API key (Capy Settings > API; give it an expiry). It is stored "
            "owner-only on this machine and sent to Capy's API only. Leave it empty to skip "
            f"{label()} capture for now.",
        ],
        "Capy API key",
    )
    return key.strip() if isinstance(key, str) else ""


def _choose_on_screen(projects: list[dict]) -> list[dict]:
    import questionary

    from . import tui

    if len(projects) <= 1:
        return list(projects)
    choices = [
        questionary.Choice(title=str(p.get("name") or p.get("id")), value=index)
        for index, p in enumerate(projects)
    ]
    message = tui.framed(
        f"Capture my {label()} threads",
        tui.wrap("Only threads you start are captured, in the projects you pick."),
        "Which Capy projects?",
    )
    picked = tui.ask(
        tui.checkbox(
            message, choices=choices, instruction="(space to toggle, enter to continue)",
            style=tui.style(), qmark=tui.qmark(), pointer=tui.pointer(),
        ),
        height=tui.content_height(message, choices),
    )
    if not isinstance(picked, list):
        return []
    return [projects[index] for index in picked]


def apply_capture(ask: CaptureAsk, *, on_prompt: Callable[[Any], None] | None = None) -> tuple[CaptureOutcome, list[str]]:
    """The installer's capture step for Capy: connect with the plan the review
    screen collected (re-checking a saved connection's account, team and
    timer), with the first sync in the background so a long history never
    holds the install up. A refused connect leaves no capture credential
    behind for a connection that does not exist."""
    if ask.plan is None:
        if ask.outcome is CaptureOutcome.ALREADY:
            if _stopped_for_another_account():
                return CaptureOutcome.REFUSED, [
                    f"! {label()} capture stays off: it was connected for another team, and Capy could "
                    f"not be reached to connect it to this one. {CONNECT_LATER}"
                ]
            killswitch_path().unlink(missing_ok=True)
            return CaptureOutcome.ALREADY, [f"{label()} capture is connected (Capy could not be reached to check it)."]
        return ask.outcome, [f"! {line}" if ask.outcome.blocks else line for line in ask.lines]
    try:
        done = connect(ask.plan, on_prompt=on_prompt, first_sync=False)
    except ConnectRefused as exc:
        if load_config() is None:
            _drop_credential()
        elif isinstance(exc, EmailNotFound):
            # The saved connection no longer matches the signed-in account
            # (another account, say), and this run may have paired a credential
            # for it: stop every upload until `probe capy connect` checks it.
            _turn_off(ANOTHER_ACCOUNT)
        return CaptureOutcome.REFUSED, [f"! {exc} {CONNECT_LATER}"]
    lines = list(done.lines)
    if done.mode not in (TimerMode.SYSTEMD, TimerMode.LAUNCHD):
        lines.append(start_background_sync())
    outcome = CaptureOutcome.ALREADY if ask.outcome is CaptureOutcome.ALREADY else CaptureOutcome.CONNECTED
    return outcome, lines


def _drop_credential() -> None:
    """Revoke and remove a capture credential with no connection behind it:
    only the paired file's, never one the researcher exported themselves."""
    from . import capabilities

    if capabilities.TokenSource.PAIRED_FILE not in capabilities.capture_token_sources(SOURCE):
        return
    with contextlib.suppress(Exception):
        capabilities.revoke_capture_device(SOURCE)
    (state_dir() / ".token").unlink(missing_ok=True)


#: The killswitch reason that only connecting for this account may lift.
ANOTHER_ACCOUNT = "connected for another account"


def _turn_off(reason: str) -> None:
    _private_dir(state_dir())
    write_text_atomic(killswitch_path(), f"{reason}\n", mode=0o600)


def _stopped_for_another_account() -> bool:
    try:
        return killswitch_path().read_text(encoding="utf-8").strip() == ANOTHER_ACCOUNT
    except OSError:
        return False


def after_sign_in() -> list[str]:
    """Called after any sign-in. A connected Capy capture whose credential
    belongs to another team than the account now signed in keeps uploading
    there (sign-in never moves it: the connection names one person's threads),
    so turn it off and say how to connect it to this account."""
    from . import capabilities

    if load_config() is None:
        return []
    credential = capabilities.resolved_capture_credential(SOURCE)
    if credential is None:
        return []
    team = _probe_account().get("customer_id")
    owner = _capture_customer(*credential)
    if not team or owner in (UNREACHABLE, None):
        return []
    if owner == team:
        if _stopped_for_another_account():
            # Signed back in to the team that owns it: its own stop lifts.
            killswitch_path().unlink(missing_ok=True)
            return [f"{label()} capture is back on: it belongs to this account's team."]
        return []
    _turn_off(ANOTHER_ACCOUNT)
    return [
        f"! {label()} capture is off: it was connected for another team. "
        f"`probe {SOURCE} connect` connects it to this account."
    ]


def start_background_sync() -> str:
    """Start one sync detached from this process (the install does not wait
    for a long history); its result is in `probe capy status`."""
    probe = _installed_probe()
    argv = [probe, SOURCE, "sync", "--quiet"] if probe else [sys.executable, "-m", "probe.cli.main", SOURCE, "sync", "--quiet"]
    try:
        subprocess.Popen(  # noqa: S603 -- a fixed argv, no shell
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            close_fds=True,
        )
    except OSError:
        return f"Could not start the first sync: run `probe {SOURCE} sync`."
    return f"The first sync runs in the background: `probe {SOURCE} status` shows it."
