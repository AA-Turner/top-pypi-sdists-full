"""`probe capy`: capture the researcher's Capy threads as Probe sessions.

Capy (capy.ai) is a cloud coding agent (registry family `cloud`): its agent
runs on Capy's servers and its tools on a Capy machine, so there is nothing to
install on this one and no hook to start capture. Instead:

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
        if pulled.sessions:
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


def _capture_customer(token: str, base_url: str) -> str | None:
    """The team a capture credential uploads to (its receipts answer names it),
    or None when the credential is refused or the server cannot say."""
    from probe.sdk.tls import ssl_context

    from ..tap_core.session_journal import DeliveryPending, ReconciliationRequired, Wire

    try:
        return Wire(base_url, token, SOURCE, context=ssl_context()).receipts(str(uuid.uuid4()))["customer_id"]
    except (DeliveryPending, ReconciliationRequired, KeyError):
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
    from probe.sdk.config import resolve

    from . import capabilities, setup, tui

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

    account = _probe_account()
    email = str(account.get("email") or "").strip()
    if not email:
        typer.echo("Sign in to Probe first (`probe login`): your Capy user is found by your Probe email.", err=True)
        raise typer.Exit(1)

    api = discovery.CapyAPI(key)
    try:
        projects = api.projects()
        users = api.users()
    except discovery.CapyAuthError:
        typer.echo("Capy refused that key. Check it under Capy Settings > API.", err=True)
        raise typer.Exit(1) from None
    except discovery.CapyError as exc:
        typer.echo(f"Could not reach Capy: {exc}", err=True)
        raise typer.Exit(1) from None

    # Only the researcher's own threads are captured, so "me" is never a
    # choice: it is the Capy member with the Probe account's email.
    user = discovery.resolve_me(users, email=email)
    if user is None:
        typer.echo(
            f"No member of this Capy organization has the email {email} (your Probe "
            "account's). Capture only takes your own threads, so it needs the same email "
            "on both.",
            err=True,
        )
        raise typer.Exit(1)
    chosen = _choose_projects(projects, project or [], interactive)

    credential = capabilities.resolved_capture_credential(SOURCE)
    team = account.get("customer_id")
    if credential is not None and _capture_customer(*credential) != team:
        # Refused, revoked, or another team's: a fresh approval replaces it.
        credential = None
    if credential is None:
        typer.echo("Approve capture for your Capy threads in your browser.")
        _, messages = setup.authorize(
            ["capture"],
            base_url=resolve().base_url,
            capture_sources=[SOURCE],
            open_browser=not no_browser,
            on_prompt=lambda prompt: typer.echo(f"  {prompt.verification_uri_complete}"),
        )
        for line in messages:
            typer.echo(line)
        if capabilities.resolved_capture_credential(SOURCE) is None:
            typer.echo("Capture was not approved, so nothing was connected.", err=True)
            raise typer.Exit(1)
    killswitch_path().unlink(missing_ok=True)
    refused_path().unlink(missing_ok=True)  # a refused credential's verdict no longer applies

    config = CapyConfig(
        api_key=key,
        me_id=str(user["id"]),
        me_email=user.get("email"),
        projects=[{"id": p.get("id"), "name": p.get("name")} for p in chosen],
        connected_at=now_iso(),
    )
    names = ", ".join(str(p.get("name") or p.get("id")) for p in chosen)
    typer.echo(
        f"Connected as {config.me_email}; capturing threads you start in {names}, "
        f"into Probe team {team}."
    )
    mode = None
    if not no_timer and capabilities.TokenSource.PAIRED_FILE not in capabilities.capture_token_sources(SOURCE):
        # The timer runs without this shell's environment (and never carries a
        # credential), so a token set only in $PROBE_CAPY_TAP_TOKEN is one it
        # cannot see: every timed sync would say "not paired".
        typer.echo(
            "No timer installed: the capture credential comes from $PROBE_CAPY_TAP_TOKEN, "
            "which the timer cannot see. Unset it and run `probe capy connect` to pair this "
            "machine, or run `probe capy sync` yourself."
        )
    elif not no_timer:
        mode, line = install_timer()
        typer.echo(line)
    config.timer = mode.value if mode else None
    save_config(config)
    if mode in (TimerMode.SYSTEMD, TimerMode.LAUNCHD):
        typer.echo("The first sync can take a while for a long history: `probe capy status` shows it.")
    elif not no_sync:
        _print_report(sync_once(), quiet=False)


def _print_report(report: SyncReport, *, quiet: bool) -> None:
    if not report.ran:
        if not (quiet and report.skipped in (Skip.BUSY, Skip.NOT_CONNECTED)):
            typer.echo(report.reason or "nothing ran", err=True)
        return
    if quiet and report.ok:
        return
    up = report.upload
    typer.echo(
        f"Synced {report.pulled_sessions} Capy session(s) from {report.threads_mine} of your threads: "
        f"{report.new_bytes} new bytes, {up.batches} batch(es) uploaded"
        + (f", {up.deleted} deleted by your team" if up.deleted else "")
        + "."
    )
    if report.budget_spent:
        typer.echo(
            f"Read {discovery.MAX_CALLS_PER_SYNC} Capy pages this sync; the next sync goes on from here.",
            err=quiet,
        )
    if report.auth_failed:
        typer.echo("Capy refused the key: run `probe capy connect` with a new one.", err=True)
    if up.credential_refused:
        typer.echo("Probe refused the capture credential: run `probe capy connect` again.", err=True)
    for line in (report.errors + up.errors)[:10]:
        typer.echo(f"  ! {line}", err=True)


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


@capy_app.command("disconnect")
def disconnect_cmd(
    keep_capture: bool = typer.Option(
        False, "--keep-capture", help="keep the capture credential (only remove the key, timer and sync record)"
    ),
) -> None:
    """Stop capturing Capy threads: remove the timer, the key, the sync record and the capture credential."""
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
    typer.echo(
        "Capy disconnected. Sessions already uploaded stay in Probe; the local mirror files "
        f"stay in {mirror_root()} (delete them if you like)."
    )
    if hint:
        typer.echo(hint)
