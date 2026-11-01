"""gather install, service and session facts, each within its own time budget."""

from __future__ import annotations
import platform
import re
import threading
from collections.abc import Callable
OS_MAX_CHARS = 128
_HARNESS = re.compile(r"^[a-z][a-z0-9_]{0,31}$")


# ---------------------------------------------------------------------------
# Sources, each in its own budget
# ---------------------------------------------------------------------------


def run_source(name: str, fn: Callable[[], object], budget_s: float,
               skipped: dict[str, str]) -> object | None:
    """`fn()` within `budget_s` seconds of wall-clock time, or None with the
    reason in `skipped`. A source that hangs (a stale network mount, a CLI that
    never answers) is abandoned on its daemon thread: it costs its own source,
    never the report."""
    result: list[object] = []
    error: list[BaseException] = []

    def target() -> None:
        try:
            result.append(fn())
        except BaseException as exc:  # noqa: BLE001 -- recorded as the source's reason
            error.append(exc)

    worker = threading.Thread(target=target, name=f"probe-report-{name}", daemon=True)
    worker.start()
    worker.join(budget_s)
    if worker.is_alive():
        skipped[name] = f"timed out after {budget_s:g} s"
        return None
    if error:
        exc = error[0]
        skipped[name] = f"failed: {type(exc).__name__}"
        return None
    return result[0] if result else None


def _cli_version() -> str:
    try:
        from probe.shared.updates import updates as versions

        return versions.cli_version()
    except Exception:  # noqa: BLE001
        from probe import __version__

        return __version__


def install_facts() -> dict:
    """Versions, how the CLI was installed, the side-by-side installs (active
    and rejected), the daemon's AI libraries and whether the daemon key is held."""
    facts: dict = {}
    try:
        from probe.shared.updates import updates as versions

        facts["versions"] = versions.local_versions()
    except Exception as exc:  # noqa: BLE001
        facts["versions"] = {"cli": _cli_version(), "error": type(exc).__name__}
    try:
        from probe.cli import updater

        facts["install_method"] = updater.detect_install().method
    except Exception:  # noqa: BLE001
        facts["install_method"] = None
    try:
        from probe.shared.updates import installs

        active = installs.active()
        facts["installs"] = {
            "active": active.name if active is not None else None,
            "rejected": sorted(installs.rejected()),
        }
    except Exception:  # noqa: BLE001
        facts["installs"] = None
    try:
        from probe.cli.daemon_cli import located_ai_libraries

        facts["ai_libraries"] = located_ai_libraries() or "missing"
    except Exception:  # noqa: BLE001
        facts["ai_libraries"] = None
    facts["daemon_key_held"] = daemon_key() is not None
    facts["python"] = platform.python_version()
    return facts


#: The service's own records a report carries whole (small JSON files).
SERVICE_RECORDS = ("guard.json", "last-stop.json", "last-crash.json", "service.run", "starts.json", "update.json")


def service_facts(scope: Scope) -> dict:
    """The Probe service's records: the guard's verdict, how it last stopped
    (and crashed), its recent starts, the updater's record, and whether the
    keeper that restarts it is installed."""
    folder = service_dir()
    facts: dict = {"folder_exists": bool(folder and folder.is_dir())}
    if folder is None:
        return facts
    for name in SERVICE_RECORDS:
        data = read_json(folder / name)
        if data is not None:
            facts[name] = redact_tree(data, scope)
    facts["keeper"] = keeper_installed()
    return facts


def keeper_installed() -> bool | None:
    try:
        from probe.service import keeper

        return bool(
            keeper._plist_path().exists()  # noqa: SLF001 -- the keeper's own install paths
            or (keeper._systemd_dir() / f"{keeper.NAME}.timer").exists()  # noqa: SLF001
            or keeper._task_marker().exists()  # noqa: SLF001
        )
    except Exception:  # noqa: BLE001
        return None


def session_facts(sid: str, scope: Scope) -> dict:
    """One session, from its registered state folder: its write lease, its
    switch, whether its worker's lock file is there, and its trace folder's
    reader cursors. Small records only."""
    root = session_state_root(sid)
    facts: dict = {"sid": sid, "state_dir_registered": root != state_root()}
    sessions = root / "sessions"
    facts["lease"] = redact_tree(read_json(sessions / f"{sid}.writer"), scope)
    try:
        facts["state"] = (sessions / f"{sid}.state").read_text(encoding="utf-8").strip()[:32] or None
    except OSError:
        facts["state"] = None
    daemon = root / "daemon"
    facts["worker_lock"] = (daemon / f"{_safe(sid)}.lock").exists()
    trace = daemon / "sessions" / _safe(sid)
    cursors = {}
    for name in ("reader.cursor", "writer.cursor"):
        try:
            cursors[name] = (trace / name).read_text(encoding="utf-8").strip()[:32]
        except OSError:
            continue
    facts["cursors"] = cursors
    for session in registry_sessions():
        if session.get("sid") == sid:
            facts["registered"] = {k: session.get(k) for k in ("harness", "mode", "generation", "registered_at",
                                                                 "heartbeat_at")}
    folder = service_dir()
    recorders = read_json(folder / "recorders.json") if folder else None
    hosted = recorders.get("sessions") if isinstance(recorders, dict) else None
    facts["hosted_recorder"] = bool(
        isinstance(hosted, list) and any(isinstance(s, dict) and s.get("sid") == sid for s in hosted)
    )
    return facts


def os_label() -> str:
    """`darwin 24.1 arm64`: the system, its release, the machine."""
    label = f"{platform.system().lower()} {platform.release()} {platform.machine()}".strip()
    return label[:OS_MAX_CHARS]


def _harness_slug(value: object) -> str | None:
    return value if isinstance(value, str) and _HARNESS.match(value) else None
from probe.shared.reports.logs import read_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.reports import Scope  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.scrub import redact_tree  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.sessions import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _safe,
    daemon_key,
    registry_sessions,
    service_dir,
    session_state_root,
    state_root,
)
