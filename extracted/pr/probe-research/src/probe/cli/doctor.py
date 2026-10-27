"""`probe doctor` — read-only diagnostic over the same state the wizard renders.

Two renderings, one state struct (see capabilities.py). The menu shows it as
toggles; this prints it.

The line that earns this command its place is LAST UPDATE ATTEMPT. Auto-update
runs detached, so it cannot report failure through the SessionStart hook that
spawned it. Without a recorded attempt, an auto-updater that has been silently
failing for a month is indistinguishable from one that works. `claude doctor`
solves it the same way.

Read-only and fail-soft throughout: this is the command someone runs when things
are already broken, so it must never be the thing that breaks.
"""

from __future__ import annotations

import dataclasses
import json
import os
import shutil
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

from probe.cli import agent_rules, autoupdate, codex_config, plugin_cli
from probe.cli.capabilities import (
    TAP_PLUGIN_NAME,
    Capabilities,
    DeviceState,
    DeviceStateOutcome,
    McpCredential,
    PluginState,
    TokenSource,
    tap_token_env,
    tracking_plugin_name,
)

#: Why a Codex MCP reads unknown in a files-only read (`collect(local=True)`).
CODEX_MCP_NOT_CHECKED = (
    "not checked: Codex keeps an OAuth login where only `codex mcp list` reads it "
    "(`probe status --refresh` asks it)"
)

_OK = "ok"
_OFF = "off"
_MISSING = "not installed"

# TokenSource.ENVIRONMENT has no entry here on purpose: which env var it
# names varies by source (tap_token_env()), so it is computed at each call
# site instead of being a third static string that can only ever be right
# for one agent.
_SOURCE_LABEL = {
    TokenSource.PAIRED_FILE: "paired device token",
    TokenSource.PROBE_CONFIG: "probe CLI config (ingest_token)",
}



def _team_note_rows() -> list[str]:
    """Whether the team note is actually syncing on this machine.

    THE FAILURE THIS EXISTS FOR IS SILENT. The sync runs from session hooks, and
    hooks do not always run: Codex skips a hook whose hash changed until the
    researcher re-approves it, an MDM policy can disable non-managed hooks
    outright, and a plugin that was never installed has none. In every one of
    those cases the file simply stops syncing -- edits accumulate locally, the
    document the team reads never changes, and nothing anywhere reports it. The
    dirty flag below is the only place that turns that into something a person
    can see.
    """
    from ..sdk.config import resolve
    from . import team_note_file

    try:
        where = team_note_file.paths_for(resolve())
        document = where.document.read_text(encoding="utf-8") if where.document.exists() else None
        base = where.base.read_text(encoding="utf-8") if where.base.exists() else None
        meta = json.loads(where.meta.read_text(encoding="utf-8")) if where.meta.exists() else {}
    except (OSError, UnicodeDecodeError, ValueError):
        return ["Team note", _row("Local file", "unreadable")]

    rows = ["Team note", _row("Local file", str(where.document))]
    if document is None:
        rows.append(_row("State", "not seeded yet -- runs at the next session start"))
        rows.extend(_parked_rows(where))
        return rows
    rows.append(_row("Synced version", str(meta.get("version", "unknown"))))
    if base is not None and document != base:
        rows.append(
            _row(
                "Unsynced edits",
                "YES -- this file has local changes the team has not seen. "
                "`probe notes sync` sends them; if this persists, your session "
                "hooks are not running (`/hooks` on Codex re-approves them).",
            )
        )
    else:
        rows.append(_row("Unsynced edits", "none"))
    rows.extend(_parked_rows(where))
    return rows


def _snapshot_ref_rows(cwd: str | None = None) -> list[str]:
    """Old code-snapshot refs in the repo doctor runs in (plan 2.6).

    The once-per-repo capture notice can be missed (a script's stderr goes to a
    log nobody reads), so the count is also here, where someone looks when
    things are wrong. Nothing outside a git repo; never deletes (D10).
    """
    import os

    from ..sdk import snapshot as _snapshot

    try:
        here = cwd or os.getcwd()
        in_repo, reason = _snapshot._repo_check(here)
        if not in_repo:
            return ["Code capture", _row("Old snapshot refs", f"unknown ({reason})")] if reason else []
        refs = _snapshot.old_snapshot_refs(here)
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return []
    if not refs:
        return ["Code capture", _row("Old snapshot refs", "none in this repo")]
    return [
        "Code capture",
        _row(
            "Old snapshot refs",
            f"{len(refs)} in this repo (refs/probe/snapshots/*, from earlier Probe "
            "versions; `git push --mirror` publishes them). Review with "
            "`probe snapshot-prune-refs --dry-run`.",
        ),
    ]


def _parked_rows(where) -> list[str]:
    """PARKED COPIES ARE TEXT NOBODY IS SENDING.

    The sync parks a leftover per-harness document, or one written under another
    credential, rather than deleting it -- so this is the one place a person can
    find out it is there and whose it is (the session-start hook tells the model;
    a headless machine has no such channel).

    Reported EVEN WHEN THE DOCUMENT IS ABSENT, which is the case that matters
    most: parking the only copy leaves no document at all, and a "not seeded
    yet" row with nothing after it reads as "nothing here" over text that is
    sitting on disk unsent.
    """
    from . import team_note_file

    try:
        parked = team_note_file.parked_copies(where)
    except Exception:  # noqa: BLE001 - a diagnostic must never be the thing that fails
        return []
    rows = []
    for path, owner, kind in parked:
        if owner is None:
            whose = (
                "no owner stamp -- unknown; read it before folding anything in, and check "
                "it is your team's"
            )
        elif owner != where.owner:
            whose = "a DIFFERENT credential -- another team's note; do not fold it in"
        elif kind == "legacy":
            whose = (
                "a leftover per-agent copy: read it, fold anything still true into the file "
                "above, then delete it. It is never sent on its own"
            )
        else:
            whose = "your own unsent work: it is taken back automatically on your next sync"
        rows.append(_row("Parked copy", f"{path} ({whose})"))
    return rows

def _interrupted_import_rows() -> list[str]:
    """Name any import this machine stopped part-way through.

    There is no boot service for background imports on purpose, so a machine
    that restarts mid-import leaves a job that is complete in every way except
    that nothing is running it. Its journals are intact and one menu entry
    resumes it -- but only for someone who already knows to look. This is a
    read of state that is already on disk, in the one command people run when
    they suspect something is wrong.
    """
    try:
        from . import import_jobs

        stalled = [
            job for job in import_jobs.list_jobs()
            if job.get("state") == import_jobs.State.INTERRUPTED
        ]
    except Exception:  # noqa: BLE001 -- diagnostics must never fail the report
        return []
    if not stalled:
        return []
    label = "import" if len(stalled) == 1 else "imports"
    return [_row(
        "Unfinished work",
        f"{len(stalled)} {label} stopped part-way. Resume: `probe wizard --action imports`",
    )]


def _pi_capture_rows() -> list[str]:
    """Why capture may be silent on pi, in the two ways doctor can actually see.

    THE FILTER IS THE CONDITION THAT COST A CUSTOMER SIX TRANSCRIPTS. pi's
    `packages` entry takes an `extensions` filter, and a filter that does not
    name our entry point loads the package's skills and its MCP manifest but
    not `index.ts` -- so the skills appear, the MCP tools answer, `probe
    session status` says tracking is on, and nothing ever spawns a daemon.
    Every other signal on the machine reads healthy. This row is the only
    place that condition is visible, which is the whole reason it exists.

    `PI_SESSION_ID` is read directly rather than through
    `agent_session.session_id_from_env()`, which is the resolver everywhere
    else. That resolver answers for whichever agent it DETECTS, and this
    function has already been narrowed to pi by the caller -- so on a machine
    where `PROBE_AGENT=pi` is exported into a Claude Code shell it would hand
    back a Claude Code session id, and the row beneath would report pi's
    capture state for a session pi never had. Naming pi's own variable here
    cannot attribute another agent's session to pi; it can only fall silent,
    which is the safe direction for a row about a session that is not running.

    Fail-soft like every other helper in this module: a diagnostic must never
    be the thing that breaks, so an unreadable settings file or an unaskable
    daemon question drops its row rather than raising through the report.
    """
    import os

    from probe.cli import capture_state, pi_config

    rows: list[str] = []
    try:
        # The session's cwd, so a PROJECT-scope filter is reported exactly as a
        # global one is -- pi applies both, and reporting only the global file
        # would name the wrong file to edit.
        entry = pi_config.merged_package_entry(cwd=os.getcwd())
    except Exception:  # noqa: BLE001 -- diagnostics must never fail the report
        entry = None
    if entry is not None and entry.installed and entry.extension_filtered_out:
        rows.append(
            _row(
                "pi extension",
                f"filtered out in {entry.scope} settings.json; "
                "capture relies on the CLI fallback",
            )
        )

    session_id = os.environ.get("PI_SESSION_ID", "")
    if session_id:
        try:
            state = capture_state.session_capture_state(session_id, "pi")
        except Exception:  # noqa: BLE001 -- see above
            state = None
        if state is not None:
            rows.append(_row("Capture (this session)", state.reason))
    return rows


def _row(label: str, value: str) -> str:
    return f"  {label:<24} {value}"


def _dropped_with_rows() -> list[str]:
    """The packages added beside the CLI (`uv tool install --with`) that an
    update had to leave out, and the exact command that adds them back
    (`updater.dropped_with_command`). Nothing when there are none."""
    try:
        from probe.cli import updater

        found = updater.dropped_with_command()
    except Exception:  # noqa: BLE001 -- a diagnostic line, never a failed doctor
        return []
    if not found:
        return []
    missing, command = found
    return [
        _row("Left out", f"{', '.join(missing)} (would not install beside the last update)"),
        _row("Add back", command),
    ]


#: How many floating runs one look counts before saying "N+".
UNFILED_LIMIT = 200

#: Lines of the daemon's device error log `doctor` shows.
DAEMON_ERROR_LINES = 5


def unfiled_summary(client) -> dict:
    """Floating runs waiting to be filed (daemon v2), for doctor and `session status`.

    `state` is "ok" (with `count`, `more`, `oldest_created_at`, `oldest_age_s`),
    "unknown" when the backend predates floating runs (it ignores the filter and
    lists filed runs, which must never be counted as unfiled), or "unreadable"
    with the reason. Never raises.
    """
    from probe.sdk import errors

    try:
        found = client.unfiled_runs(limit=UNFILED_LIMIT)
    except errors.CapabilityUnavailable:
        return {"state": "unknown", "reason": "this backend predates floating runs"}
    except Exception as exc:  # noqa: BLE001 - a diagnostic must never crash
        return {"state": "unreadable", "reason": str(exc)[:200] or type(exc).__name__}
    return {"state": "ok", **found}


def name_account() -> str | None:
    """The signed-in account's email, asked the old way (`/v1/me` over the SDK
    client: its own timeout, the environment's proxies), or None.

    For the one decision that must not go on a guess: redeeming an install code
    switches the device's account irreversibly, and is confirmed only when the
    account being replaced can be named. When the wizard's one call could not
    name it -- a slow server, a network it could not cross -- ask this way."""
    try:
        from probe.sdk.config import resolve

        settings = resolve()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None
    return _check_login(settings).logged_in_as or None


def fetch_unfiled() -> dict | None:
    """The unfiled-runs summary on its own, for a screen that shows it.

    The wizard's one server call carries no unfiled count (its menu never shows
    one), so its Diagnose screen asks for it here, once, when it is chosen.
    None when signed out; never raises."""
    try:
        from probe.sdk.client import Client
        from probe.sdk.config import resolve
        from probe.sdk.surface import Surface

        settings = resolve()
        if not settings.token:
            return None
        with Client(settings=settings, async_writes=False, surface=Surface.CLI.value) as client:
            return unfiled_summary(client)
    except Exception as exc:  # noqa: BLE001 - a diagnostic must never crash
        return {"state": "unreadable", "reason": str(exc)[:200] or type(exc).__name__}


def describe_unfiled(summary: dict | None) -> str | None:
    """One line for a person: "3, oldest 2h ago", "200+, oldest 3d ago or more"."""
    if not summary:
        return None
    if summary.get("state") != "ok":
        return f"{summary.get('state', 'unknown')} ({summary.get('reason') or 'no answer'})"
    count = int(summary.get("count") or 0)
    if count == 0:
        return "none"
    more = bool(summary.get("more"))
    if summary.get("oldest_age_s") is None:
        return f"{count}{'+' if more else ''}, oldest of unknown age"
    # Listed newest first, so past the limit the true oldest is older still.
    age = _format_age(summary["oldest_age_s"])
    return f"{count}{'+' if more else ''}, oldest {age}{' or earlier' if more else ''}"


def daemon_error_lines(limit: int = DAEMON_ERROR_LINES) -> list[str]:
    """The last lines of the daemon's device-level error log, `<state>/probe/daemon-errors.log`."""
    try:
        from probe.sdk import session_marker

        path = session_marker.state_dir() / "daemon-errors.log"
        with path.open("rb") as handle:
            handle.seek(0, 2)
            size = handle.tell()
            handle.seek(max(0, size - 16384))
            tail = handle.read().decode("utf-8", errors="replace")
    except OSError:
        return []
    return [line for line in tail.splitlines() if line.strip()][-limit:]


def _daemon_rows(caps: Capabilities | None = None) -> list[str]:
    """The Probe daemon (the `daemon` state): default, key, this session, spend,
    the runs it has yet to file, its AI libraries and its recent errors.

    Read-only and local apart from the unfiled count, which `collect()` fetched.
    The daemon is the capture daemon's child, so capture being off is named as
    the cause rather than left for the reader to connect.
    """
    from probe.cli import companion, reasoning_summaries
    from probe.cli import setup as wizard
    from probe.sdk import agent_session, session_marker

    rows = ["Probe daemon"]
    default = session_marker.default_session_state()
    rows.append(_row("New sessions start", session_marker.state_label(default)))
    rows.append(
        _row(
            "Daemon key",
            "held (read + write; deletes go to the trash only)"
            if wizard.companion_token_held()
            else "none — Who records in the wizard (switch it to the daemon, or Enter on it) approves one",
        )
    )
    rows.extend(_who_records_rows())
    for source in reasoning_summaries.SOURCES:
        if session_marker.recorder(source) == session_marker.RECORDER_DAEMON:
            label = reasoning_summaries.LABELS[source]
            rows.append(_row(f"{label}'s reasoning", reasoning_summaries.doctor_value(source)))
    session_id = agent_session.session_id_from_env()
    if session_id:
        status = session_marker.daemon_status(session_id)
        if status is not None:
            live, reason = status
            rows.append(_row("This session", "daemon" if live == session_marker.DAEMON_LIVE else f"daemon (degraded: {reason})"))
        rows.extend(_reader_rows(session_id))
    # The device's daemon token counter (`daemon/device.json`, UTC days): a meter, no fuse reads it.
    spent = companion.tokens_today()
    rows.append(_row("Model tokens today", "unreadable" if spent is None else f"{spent:,} (UTC day)"))
    read_spent = _reader_tokens_today()
    if read_spent:
        rows.append(_row("Reader tokens today", f"{read_spent:,} (UTC day)"))
    unfiled = describe_unfiled(caps.unfiled_runs if caps is not None else None)
    if unfiled:
        rows.append(_row("Unfiled runs", unfiled))
    if caps is not None and caps.daemon_ai_libraries is not None:
        rows.append(
            _row(
                "AI libraries",
                "missing — Who records in the wizard (switch it to the daemon, or Enter on it) installs them"
                if caps.daemon_ai_libraries == "missing"
                else f"installed (Pydantic AI {caps.daemon_ai_libraries})",
            )
        )
    errors_seen = daemon_error_lines()
    for index, line in enumerate(errors_seen):
        rows.append(_row("Recent errors" if index == 0 else "", line[:200]))
    rows.append(_row("Diagnostic reports", _diagnostic_reports()))
    return rows


def _diagnostic_reports() -> str:
    """Whether the daemon and the Probe service send the Probe team a report
    when they misbehave (`probe.core.report`), and the last one sent."""
    try:
        from probe.core import report

        return report.doctor_row()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return "unknown"


def _who_records_rows() -> list[str]:
    """One "Who records" row per coding agent set up here, and for an agent whose
    daemon profile is its package's settings entry (pi), the package's version
    against the floor the daemon needs and whether a project overrides it."""
    from pathlib import Path

    from probe.cli import pi_config
    from probe.cli import setup as wizard
    from probe.harness import get_registry
    from probe.sdk import session_marker

    daemon = session_marker.RECORDER_DAEMON
    machine_daemon = any(session_marker.recorder(s) == daemon for s in wizard.RECORDER_SOURCES)
    rows: list[str] = []
    for harness in get_registry().installable():
        if harness.id not in wizard.RECORDER_SOURCES:
            continue
        by_settings = harness.lean_profile == wizard.LEAN_SETTINGS_FILTER
        profile = pi_config.entry_profile() if by_settings else None
        if by_settings and profile is None:
            continue  # pi is not set up here: nothing records for it
        who = session_marker.recorder(harness.id)
        value = wizard.RECORDER_WORDS.get(who, who)
        if profile is not None and profile not in (who, pi_config.PROFILE_TRACKING_OFF):
            value += f" (but its Probe package is on the {profile} profile: switch Who records again)"
        if machine_daemon and who != daemon:
            value += " — can use the daemon now: `probe wizard` › Who records, Enter"
        rows.append(_row(f"Who records ({harness.label})", value))
        if not by_settings or not (who == daemon or machine_daemon):
            continue
        version = pi_config.installed_package_version()
        floor = ".".join(str(part) for part in pi_config.DAEMON_MIN_PACKAGE_VERSION)
        have = ".".join(str(part) for part in version) if version else "unknown"
        ready = version is not None and version >= pi_config.DAEMON_MIN_PACKAGE_VERSION
        rows.append(_row(f"{harness.label} Probe package", have if ready else f"{have} (the daemon needs {floor}+)"))
        merged = pi_config.merged_package_entry(cwd=Path.cwd())
        if who == daemon and merged.installed and merged.scope == "project":
            rows.append(_row("", f"this folder's .pi/settings.json overrides {harness.label}'s Probe package"))
    return rows


def _reader_tokens_today() -> int:
    from probe.daemon import store as daemon_store

    try:
        return daemon_store.device_tokens_today(lane=daemon_store.LANE_READ)
    except Exception:  # noqa: BLE001 -- a diagnostic never fails on a counter
        return 0


def _reader_rows(session_id: str) -> list[str]:
    """This session's reader (daemon reads): its state as the researcher's line,
    how its turns ended and how the main agent's asks ended. Read-only: the
    store is opened read-only, the mailbox only listed."""
    import sqlite3

    from probe.daemon import mailbox
    from probe.daemon.store import store_path

    rows: list[str] = []
    status = mailbox.read_status(session_id)
    state = status.get("state")
    if state:
        line = ("running" if state == mailbox.Status.OK else
                mailbox.researcher_line(state, reason=status.get("reason", "")))
        rows.append(_row("Reader", line or state))
    path = store_path(session_id)
    if not path.is_file():
        return rows
    try:
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=1.0)
        try:
            turns = dict(db.execute("SELECT coalesce(outcome, 'running'), count(*) FROM read_turns GROUP BY 1"))
            asks = dict(db.execute("SELECT state, count(*) FROM read_asks GROUP BY 1"))
        finally:
            db.close()
    except sqlite3.Error:  # an older store has no reader tables, or it is busy
        return rows
    if turns:
        rows.append(_row("Reader turns", " · ".join(f"{n} {k}" for k, n in sorted(turns.items()))))
    if asks:
        rows.append(_row("Asks", " · ".join(f"{n} {k}" for k, n in sorted(asks.items()))))
    return rows


def _version_comparison() -> tuple[tuple, float | None]:
    """Grade this machine against the CACHED manifest. Never hits the network.

    `probe doctor` must work offline and must not add a network round trip to a
    diagnostic command, so it reads the manifest the session-start hook already
    keeps warm. A stale or absent cache yields no rows and an age of None, which
    the renderer states as "could not check" -- the one thing it must never do is
    let an unreadable manifest print as though everything is current.
    """
    from probe import version_policy
    from probe.cli import versions as versions_mod

    try:
        manifest, fetched_at, _ok = version_policy.read_cache()
    except Exception:
        return ((), None)
    if not isinstance(manifest, dict):
        return ((), None)
    try:
        rows = tuple(versions_mod.compare(manifest))
    except Exception:
        return ((), None)
    age = max(0.0, time.time() - fetched_at) if fetched_at else None
    return (rows, age)


def tap_behind_warning(rows, source: str | None = None, plugin: str | None = None) -> str | None:
    """A warning when the transcript tap is behind the manifest's `tap.latest`.

    The Versions block already grades the tap, but as one row among four; a tap
    left behind by `probe update` went unnoticed exactly that way, while it is
    the component whose staleness costs captured sessions. So it is repeated
    under Warnings, with the way out.

    What it says about sessions already open is what the update will do to
    them (`updater.follows_without_restart`): where they follow an update (the
    prompt hook hands an old watcher to the Probe service, which records on the
    newest installed tap), they move with no restart; only elsewhere does a
    session keep the old copy until it restarts. It said "until it restarts"
    everywhere, and on every machine the service had already moved. `plugin`:
    the agent's installed Probe plugin (None when it has none: then a watcher
    from before the hand-back has nothing to move it).
    """
    from probe.sdk.session_marker import WIZARD_HINT

    for row in rows:
        if row.kind == "tap" and row.behind and row.latest:
            head = (
                f"the transcript tap is {row.installed}, behind the published {row.latest}; "
                f"the wizard's Update updates it ({WIZARD_HINT}); "
            )
            if _sessions_follow(source, row.latest, plugin):
                return head + "open sessions move to it by themselves, with no restart"
            return head + "a session started before the update keeps running the old copy until it restarts"
    return None


def _sessions_follow(source: str | None, tap: str, plugin: str | None) -> bool:
    """Do `source`'s open sessions move to tap `tap` once it is installed, with
    no restart (`updater.follows_without_restart`, the update's own verdict, on
    the state now: its Probe plugin `plugin`, its sessions on older taps)? A
    prediction: an agent proven only from what is installed (Kimi Code) is
    never said to follow a tap not installed yet.
    Never raises: unknown (its sessions could not be looked at) keeps the
    restart line."""
    try:
        from probe.cli import updater
        from probe.cli.capabilities import agent_source

        source = source or agent_source()
        stale = updater.stale_tap_sessions(source, tap)
        if stale is None:
            return False
        result = updater.PluginResult(True, True, False, None, plugin, "", tap_after=tap, tap_running_stale=stale)
        return updater.follows_without_restart(source, result, predicting=True)
    except Exception:  # noqa: BLE001 - see docstring
        return False


def _format_age(seconds: float | None) -> str:
    if seconds is None:
        return "unknown age"
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def _version_rows(caps: Capabilities) -> list[str]:
    """The Versions block: one line per component, good news included.

    Printing the current components too is the point of this section. Reporting
    only what is wrong is what made silence ambiguous -- a clean machine and a
    machine nothing had ever checked produced byte-identical output.
    """
    if not caps.version_rows:
        return [
            _row("Checked against", "no cached manifest — could not check"),
            _row("", "the wizard's Update fetches it and compares"),
        ]
    from probe.cli.versions import render as render_versions

    lines = [line for line in render_versions(list(caps.version_rows))]
    age = caps.version_manifest_age_s
    lines.append(_row("Checked against", f"manifest fetched {_format_age(age)}"))
    # A comparison is only as current as the thing compared against. Past a day
    # the cache is well beyond both the 15m TTL and the 1h failure backoff, which
    # means fetches have been failing -- worth saying, because every verdict above
    # is then graded against a manifest that may predate several releases.
    if age is not None and age > 86400:
        lines.append(
            _row("", "manifest is over a day old — version checks may be failing")
        )
    return lines


def codex_hook_rows(caps: Capabilities) -> list[str]:
    """The "Codex hooks" section when Codex is installed (asks Codex, ~0.2s), else none.

    Codex skips a hook it has not approved without a word, and a Probe update
    that changes a hooks.json entry needs that approval again: the one failure
    no other row can see, because nothing of Probe's runs to report it.
    """
    # Whenever Codex is installed, whichever agent this report is for: a plain
    # terminal reports for Claude Code, and that is where someone checks.
    if not caps.codex_available:
        return []
    from probe.cli import codex_hooks

    return codex_hooks.rows(codex_hooks.status(), _row)


#: Sessions, recorders or holds `doctor` lists one by one before it counts the rest.
SERVICE_ROWS_SHOWN = 5


def _short(sid: object) -> str:
    text = str(sid or "?")
    return text if len(text) <= 12 else text[:12] + "…"


def _session_state(session: dict) -> str:
    """What a "Sessions" row says after the mode: nothing for a live session.
    A session in mode off is never `alive` to the service, whatever its agent
    does, so it is "(off)" while its agent runs (`service_calls.live_off`),
    "(ended)" once it does not."""
    from probe.cli import service_calls

    if session.get("alive"):
        return ""
    return " (off)" if service_calls.live_off(session) else " (ended)"


def _recorder_state(recorder: dict) -> str:
    """"recording" only while the recorder holds its session's claim
    (`recording`): a thread alive in its retry wait, or one whose session
    another recorder (its own `tap watch`) holds, records nothing. A tap before
    0.10.5 publishes no claim (null): its thread's life is all there is. A
    session that is off (`off`) is captured by nobody, whatever the claim."""
    if not recorder.get("alive"):
        return "stopped"
    if recorder.get("off") is True:
        # Held: it may hold the session's claim (so an older tap's `tap watch`
        # hands the session over), and records nothing.
        return "not capturing: Probe is off"
    return "not recording" if recorder.get("recording") is False else "recording"


def service_rows(view: dict) -> list[str]:
    """The Probe service's own view (`service_calls.view()`): the "Probe
    service" section. Pure, like `render`."""
    from probe.cli import service_calls
    from probe.cli.service_calls import Reach

    rows = ["Probe service"]
    reach = view.get("reach")
    if reach == Reach.NOT_RUNNING:
        rows.append(_row("Status", f"not running -- {service_calls.STARTS_WITH}"))
        return rows
    if reach == Reach.UNSUPPORTED:
        rows.append(_row("Status", "does not run on this system yet"))
        return rows
    if reach != Reach.ANSWERED:
        rows.append(_row("Status", f"{reach}: {view.get('error') or 'no answer'}"))
        return rows
    started = view.get("started_at")
    since = f", since {service_calls.when(started)}" if started else ""
    rows.append(
        _row("Status", f"{view.get('state') or 'running'} (version {view.get('version') or 'unknown'}, "
                       f"pid {view.get('pid')}{since})")
    )

    def listed(label: str, items: list, text) -> None:
        if not items:
            rows.append(_row(label, "none"))
            return
        for index, item in enumerate(items[:SERVICE_ROWS_SHOWN]):
            rows.append(_row(label if index == 0 else "", text(item)))
        if len(items) > SERVICE_ROWS_SHOWN:
            rows.append(_row("", f"+{len(items) - SERVICE_ROWS_SHOWN} more"))

    sessions = view.get("sessions") or []
    listed(
        "Sessions",
        sessions,
        lambda s: f"{_short(s.get('sid'))} {s.get('harness')} {s.get('mode')}" + _session_state(s),
    )
    listed(
        "Recorded by the service",
        view.get("recorders") or [],
        lambda r: f"{_short(r.get('sid'))} "
        + _recorder_state(r)
        + (f", last {r['last']}" if r.get("last") else "")
        + (f", {r['failures']} restart(s)" if r.get("failures") else ""),
    )
    listed("Hook hosts", view.get("hook_hosts") or [], lambda h: f"{h.get('root')} (pid {h.get('pid')})")
    unreached = view.get("hints_unreached") or []
    if unreached:
        from probe.harness import registry

        def agent(harness: object) -> str:
            row = registry.get_registry().find(harness) if isinstance(harness, str) else None
            return row.label if row is not None else "the agent"

        # Its deliverer (a hook or extension) loaded before an update is dead or
        # old: a new process loads the current one (`/reload` is not enough on pi).
        listed(
            "Hints not reaching",
            unreached,
            lambda u: f"{_short(u.get('sid'))} ({u.get('missed')} missed, quit {agent(u.get('harness'))} "
            "and resume the session)",
        )
    listed(
        "Runs in flight",
        view.get("runs") or [],
        lambda r: f"{r.get('run')} (pid {r.get('pid')}, since {service_calls.when(r.get('since'))})",
    )
    imports = view.get("imports") or []
    if imports:
        listed(
            "Imports running",
            imports,
            lambda i: f"{_short(i.get('job_id'))} (pid {i.get('pid')}, since {service_calls.when(i.get('since'))})",
        )
    update = view.get("update") or {}
    rows.append(_row("Updates", service_calls.update_text(update)))
    app_text = service_calls.app_update_text(update.get("app"))
    if app_text:
        rows.append(_row("Desktop app", app_text))
    if update.get("deferred_reason"):
        since_text = service_calls.when(update.get("deferred_since") or update.get("deferred_at"))
        rows.append(_row("Update deferred", f"{update['deferred_reason']} (since {since_text})"))
    return rows


def render(caps: Capabilities, codex_hooks: list[str] | None = None, service: dict | None = None) -> str:
    """The full report. Pure, so it can be asserted in tests without a machine.

    `codex_hooks` is `codex_hook_rows(caps)`, gathered by the caller because it
    asks Codex; omitted, the section is left out. `service` is
    `service_calls.view()`, likewise (it asks the Probe service).
    """
    lines: list[str] = ["Probe Research doctor", ""]

    lines.append("Versions")
    lines.extend(_version_rows(caps))
    lines.append("")

    lines.append("Install")
    lines.append(_row("CLI version", caps.cli_version or "unknown"))
    lines.append(_row("Install method", caps.install_method or "unknown"))
    if caps.agent_source == "pi":
        # Capabilities has no `pi_available` field (only claude_available /
        # codex_available -- both source-independent booleans this dataclass
        # has carried since before pi existed), and inventing one is a real
        # field-shape change this pass did not want to make silently. The old
        # ternary's `else` defaulted straight to `caps.claude_available` here
        # too, so a pi report showed "Claude Code CLI: ok" -- true about the
        # wrong agent. Honest and unresolved beats confidently wrong: say
        # what this does not check instead.
        # "pi CLI", not "pi extension": this row occupies the slot that holds
        # "Claude Code CLI" / "Codex CLI" below, so it was always about the
        # BINARY. The label only became wrong once the rows underneath started
        # reporting the extension for real -- two adjacent "pi extension" rows,
        # the first saying doctor does not track it and the second tracking it.
        lines.append(_row("pi CLI", "see `pi --version`; not tracked by doctor"))
        # What doctor CAN see about pi: whether our own extension entry point
        # is filtered out of the package, and whether a daemon is live for this
        # session. Both are silent failures everywhere else.
        lines.extend(_pi_capture_rows())
    elif caps.agent_source == plugin_cli.KIMI:
        lines.extend(_kimi_rows())
    else:
        agent_label = "Codex CLI" if caps.agent_source == "codex" else "Claude Code CLI"
        agent_available = (
            caps.codex_available if caps.agent_source == "codex" else caps.claude_available
        )
        # The VERSION beside the tick. "installed" was all this said while an
        # entire customer's imports failed on a flag their build predated, and the
        # first place anyone would look for that is `probe doctor`.
        agent_state = _OK if agent_available else _MISSING
        if agent_available and caps.agent_version:
            agent_state = f"{agent_state} ({caps.agent_version})"
        lines.append(_row(agent_label, agent_state))
    lines.append("")

    lines.append("Account")
    lines.append(_row("Logged in as", caps.logged_in_as or "not logged in"))
    lines.append(_row("Endpoint", caps.base_url or "unknown"))
    # WHICH of this device's saved accounts answered. Without it, "not logged
    # in" on a machine holding three contexts sends someone hunting for a lost
    # credential when the real answer is that a different one is active.
    if caps.config_context:
        lines.append(_row("Saved account", caps.config_context))
    lines.extend(_interrupted_import_rows())
    lines.append("")

    lines.append("CLI + MCP")
    lines.append(
        _row(
            "Plugin",
            tracking_plugin_name(caps.agent_source) if caps.tracking_plugin_installed else _MISSING,
        )
    )
    if caps.agent_source == "codex":
        mcp_status = (
            "logged in"
            if caps.mcp_authenticated is True
            else "not logged in"
            if caps.mcp_authenticated is False
            else "unknown"
        )
        lines.append(_row("MCP OAuth", mcp_status))
    # The MCP answer every surface prints (Capabilities.mcp_state): "on" only
    # when the credential this agent's MCP sends is there; a login it needs
    # names the command, and the daemon profile says the daemon reads.
    lines.append(_row("MCP", caps.mcp_status()))
    lines.append("")

    if codex_hooks:
        lines.extend(codex_hooks)
        lines.append("")

    lines.append("Session capture")
    tap_name = TAP_PLUGIN_NAME
    lines.append(_row("Plugin", tap_name if caps.capture_plugin_installed else _MISSING))
    capture_status = "capturing" if caps.capture_on else _OFF
    if caps.capture_on and caps.capture_python_missing:
        # Installed, paired and switched on, and still nothing records: the tap
        # found no interpreter to run on (`capture_python_missing`).
        capture_status = f"not running: needs Python 3.11 or newer ({caps.capture_python_missing})"
    lines.append(_row("Status", capture_status))
    if caps.capture_device_id:
        lines.append(_row("Paired device", caps.capture_device_id))
    if caps.capture_awaiting_confirmation:
        lines.append(_row("Killswitch", "ON — waiting for Install to confirm capture (run `probe wizard`)"))
    elif caps.capture_killswitched:
        lines.append(_row("Killswitch", "ON — capture is disabled locally"))
    # The last time this machine's probe CLI deliberately stopped the uploader.
    # A daemon found dead WITHOUT a matching stop here was killed by something
    # else — surfacing the event makes a "transcripts missing" report carry its
    # own cause either way.
    if caps.capture_last_stop:
        lines.append(_row("Last daemon stop", caps.capture_last_stop))
    # Every source is listed, not just the winning one. A user who thinks capture
    # is off deserves to see the credential that is keeping it alive.
    for source in caps.capture_token_sources:
        if source is TokenSource.ENVIRONMENT:
            label = f"{tap_token_env(caps.agent_source)} environment variable"
        else:
            label = _SOURCE_LABEL[source]
        lines.append(_row("Credential from", label))
    if caps.capture_credential_valid is False:
        lines.append(_row("Credential check", "rejected — re-run `probe wizard`"))
    elif caps.capture_token_sources and caps.capture_credential_valid is None:
        lines.append(_row("Credential check", "unknown (offline or endpoint unavailable)"))
    if not caps.capture_token_sources:
        lines.append(_row("Credential", "none — this device is not paired"))
    lines.append("")

    lines.extend(_daemon_rows(caps))
    lines.append("")

    lines.append("Agent rules")
    # pi is no longer capture-only, so this asks the same real question every
    # other source gets. `agent_rules.memory_path("pi")` resolves pi's own
    # ~/.pi/agent/AGENTS.md (it used to fall through to Claude Code's
    # CLAUDE.md, which meant a machine with both agents configured could have
    # `apply_agent_rules` silently install into the wrong file); with that
    # fixed and the wizard offering the capability, the old
    # "not applicable -- pi is capture-only here" row was reporting a limit
    # that no longer exists.
    lines.append(
        _row(
            f"Global {agent_rules.memory_path(caps.agent_source).name}",
            "installed" if caps.agent_rules_installed else "not added",
        )
    )
    # Reported separately from installed/absent. A block from an older release
    # still LOADS, so it reads as working while teaching superseded wording --
    # and this file is the one copy no release can reach, so nothing else would
    # ever surface it. `probe wizard` rewrites it in place.
    if caps.agent_rules_stale:
        lines.append(
            _row("", "outdated wording -- `probe agent-rules refresh` (session start also does this)")
        )
    lines.append("")

    lines.extend(_team_note_rows())
    lines.append("")

    snapshot_rows = _snapshot_ref_rows()
    if snapshot_rows:
        lines.extend(snapshot_rows)
        lines.append("")

    lines.append("Auto-update")
    lines.append(_row(
        "Enabled",
        "yes (on by default for this install)" if caps.auto_update_by_default
        else "yes" if caps.auto_update_enabled else "no",
    ))
    lines.append(_row("Last attempt", caps.last_update_attempt or "never run on this device"))
    # A SEPARATE line, never folded into the one above. Once the run lock exists,
    # a box that has been training all week is deliberately not updating -- and
    # with only a last-attempt timestamp that is byte-identical to an auto-updater
    # that died. This is the line that tells them apart.
    if caps.last_update_skip:
        lines.append(_row("Deferred", caps.last_update_skip))
    lines.extend(_dropped_with_rows())
    if caps.live_runs:
        shown = ", ".join(caps.live_runs[:3])
        if len(caps.live_runs) > 3:
            shown += f", +{len(caps.live_runs) - 3} more"
        lines.append(_row("Runs in flight", shown))

    if service is not None:
        lines.append("")
        lines.extend(service_rows(service))

    lines.append("")
    lines.append("Outbox")
    if caps.outbox_status is None:
        lines.append(_row("Queue", "never used"))
    else:
        status = caps.outbox_status
        lines.append(_row("Pending", str(status.get("pending") or 0)))
        lines.append(_row("Dead-lettered", str(status.get("failed") or 0)))
        from ..sdk.journal import auth_blocked_since

        blocked = auth_blocked_since(status)
        if blocked:
            lines.append(_row("Auth-blocked since", str(blocked)))
        if status.get("paused"):
            until = status.get("paused_until")
            lines.append(_row("Paused", f"until {until} (`probe outbox resume`)" if until else "yes (`probe outbox resume`)"))
        if status.get("last_error"):
            lines.append(_row("Last error", str(status["last_error"])))
        rescue = status.get("rescue") or {}
        for fp, writes in (rescue.get("rescued") or {}).items():
            lines.append(
                _row("Rescued", f"credential {fp}: {writes} write(s) of a revoked token, sending "
                     "with your login (same team and user)")
            )
        if rescue.get("adopted_waiting") and not rescue.get("rescued"):
            waiting = rescue["adopted_waiting"]
            lines.append(
                _row("Rescued earlier", f"{waiting} write(s) queued to go out with your login; "
                     "`probe outbox drain` says why any stay")
            )
        for fp, why in (rescue.get("cannot_rescue") or {}).items():
            lines.append(
                _row("Stranded", f"credential {fp}: cannot be sent with your login ({why}); "
                     "`probe outbox status` says what to do")
            )

    if caps.warnings:
        lines.append("")
        lines.append("Warnings")
        for warning in caps.warnings:
            lines.append(f"  ! {warning}")

    return "\n".join(lines)


def _device_problems(caps: Capabilities, recorder: str | None) -> list[str]:
    """What the full report's device sections say is wrong (the daemon, the
    outbox), for `summary`: the sections themselves stay in the report. Only
    states that are a problem whenever they hold: the daemon's error log also
    takes routine notes (a reinstall), and an outbox's last error can belong
    to a queue already emptied, so both stay in the full report alone."""
    from probe.sdk import session_marker

    from probe.cli import setup as wizard

    found: list[str] = []
    if recorder == session_marker.RECORDER_DAEMON and not wizard.companion_token_held():
        found.append("The Probe daemon has no key: press Enter on Who records to approve one.")
    if recorder == session_marker.RECORDER_DAEMON and caps.daemon_ai_libraries == "missing":
        found.append("The Probe daemon's AI libraries are missing: press Enter on Who records to install them.")
    status = caps.outbox_status or {}
    if status:
        from ..sdk.journal import auth_blocked_since

        if status.get("failed"):
            found.append(f"Outbox: {status['failed']} write(s) dead-lettered (`probe outbox status`).")

        if auth_blocked_since(status):
            found.append(f"Outbox: blocked on its credential since {auth_blocked_since(status)} (`probe outbox status`).")
        if status.get("paused"):
            found.append("Outbox: paused (`probe outbox resume`).")
        if (status.get("rescue") or {}).get("cannot_rescue"):
            found.append("Outbox: writes stranded under a revoked credential (`probe outbox status`).")
    return found


def summary(caps_by_source: "dict[str, Capabilities]", *, recorder: str | None = None) -> list[str]:
    """Diagnose's page in the wizard: the verdict, a line for the device and
    one per coding agent, then the problems and what to do about each. The
    full report (`render`, every section for every agent: ~300 lines for four
    agents, most of it the device's own sections said four times) is what `c`
    copies and `probe doctor` prints."""
    from probe.cli import actions, codex_hooks
    from probe.cli import setup as wizard

    from probe.cli.capabilities import McpState

    per_agent: dict[str, list[str]] = {}
    for source, caps in caps_by_source.items():
        found = [*caps.warnings, *actions.problems(caps)]
        # Codex's own warning already says its MCP is not logged in.
        if caps.mcp_state == McpState.LOGIN_NEEDED and not any("not logged in" in w for w in found):
            found.append(f"MCP {caps.mcp_status()}")
        per_agent[source] = list(dict.fromkeys(found))
    # Each problem once, naming the agents that have it; one every agent has
    # is the device's, and goes unnamed.
    holders: dict[str, list[str]] = {}
    for source, found in per_agent.items():
        for w in found:
            holders.setdefault(w, []).append(source)
    problems = []
    for w, sources in holders.items():
        label = wizard.agent_label(sources)
        if len(per_agent) > 1 and len(sources) == len(per_agent):
            problems.append(w)
        else:
            problems.append(w if w.startswith(f"{label}:") else f"{label}: {w}")
    if any(caps.codex_available for caps in caps_by_source.values()):
        hooks = codex_hooks.status()
        if hooks is not None and hooks.untrusted:
            problems.append(
                f"Codex: {len(hooks.untrusted)} of {hooks.total} Probe hooks are off until approved; "
                "in Codex, type /hooks and approve the Probe Research hooks."
            )
        problems += [f"Codex warns: {warning[:200]}" for warning in (hooks.warnings if hooks else ())]
    first = next(iter(caps_by_source.values()), None)
    if first is not None:
        problems += _device_problems(first, recorder)
    count = len(problems)
    verdict = "no problems found" if not count else f"{count} problem{'' if count == 1 else 's'}"
    lines = [f"Probe Research doctor: {verdict}"]
    if first is not None:
        device = [first.logged_in_as or "not signed in", f"CLI {first.cli_version or 'not found'}"]
        if recorder:
            device.append(f"Who records: {recorder}")
        lines.append(" · ".join(device))
    if caps_by_source:
        width = max(len(wizard.agent_label(source)) for source in caps_by_source)
        lines.append("")
        lines += [
            f"  {wizard.agent_label(source):<{width}}   tracking {'on' if caps.tracking_on else 'off'}"
            f" · capture {wizard._capture_word(caps)}"  # the menu's words: a sign-in's lock says what lifts it
            for source, caps in caps_by_source.items()
        ]
    if problems:
        lines += ["", "Problems:", *(f"  {problem}" for problem in problems)]
    lines += ["", "c copies the full report; `probe doctor` prints it."]
    return lines


def stale_codex_token_warning() -> str | None:
    """Codex holding a read token this device has already replaced.

    `codex mcp list` reports `bearer_token` for ANY header, so Codex's own
    status cannot tell a current credential from a revoked one -- it says
    authenticated either way, and every call 401s. Comparing the configured
    header against the token we hold is the only local signal there is.

    Silent whenever either side is unknown: no entry, no stored token, or an
    unreadable config is not evidence of drift.
    """
    from probe.cli.capabilities import CODEX_MCP_NAME

    configured = codex_config.configured_bearer(CODEX_MCP_NAME)
    if not configured:
        return None
    from probe.cli.setup import current_mcp_token

    held = current_mcp_token()
    if not held or configured == held:
        return None
    # NAME THE OUTCOME, NOT ONE COMMAND. The first version of this line said
    # "re-run `probe wizard` to re-point it" while the wizard could not: its
    # repair sat behind two gates that both close in exactly this state (see
    # the work-list entry in main.py). The wizard does it now, and the wording
    # below stays true even if the repair moves again, because it says what
    # will happen rather than which command owns it.
    return (
        "the Codex MCP is using an older read token than this device holds; "
        "run `probe wizard` to re-point it"
    )


@dataclass(frozen=True)
class _LoginCheck:
    logged_in_as: str | None = None
    #: True accepted, False refused (the wizard's sign-in trigger), None unknown.
    api_credential_valid: bool | None = None
    unfiled: dict | None = None
    warnings: tuple[str, ...] = ()


def _check_login(settings) -> _LoginCheck:
    """The old way: `/v1/me` and the unfiled-runs list, with the SDK client."""
    if not settings.token:
        return _LoginCheck()
    try:
        from probe.sdk.client import Client
        from probe.sdk.surface import Surface

        with Client(settings=settings, async_writes=False, surface=Surface.CLI.value) as client:
            email = str(client.me().get("email") or "")
            # Runs the daemon (or a person) has yet to file. Its own
            # fail-soft: a backend without floating runs reads "unknown".
            return _LoginCheck(
                logged_in_as=email, api_credential_valid=True, unfiled=unfiled_summary(client)
            )
    except Exception as exc:  # noqa: BLE001
        from probe.sdk.errors import AuthError, ScopeError

        return _LoginCheck(
            api_credential_valid=False if isinstance(exc, (AuthError, ScopeError)) else None,
            warnings=(
                (f"could not verify login against {settings.base_url}: {exc}",)
                if settings.base_url
                else ()
            ),
        )


def _login_from_state(state: DeviceState, *, has_token: bool, base_url: str | None) -> _LoginCheck:
    """The login half of the wizard's one call, in `_check_login`'s shape."""
    if not has_token:
        return _LoginCheck()
    if state.answered and state.account_valid:
        return _LoginCheck(logged_in_as=state.account_email or "", api_credential_valid=True)
    if state.answered and state.account_valid is False:
        reason = "the server refused this credential"
    elif state.answered:
        reason = "the server could not check it"
    else:
        reason = state.error or "no answer"
    return _LoginCheck(
        api_credential_valid=False if state.answered and state.account_valid is False else None,
        warnings=(f"could not verify login against {base_url}: {reason}",) if base_url else (),
    )


def with_server_state(
    caps: Capabilities, state: DeviceState, *, has_token: bool, base_url: str | None
) -> Capabilities:
    """`caps` with the server's half read from `state`: the half `collect`
    reads through `device_state_scope`, for a caller that asked the server ONCE
    for every agent after their own checks (`probe status --refresh`). Nothing
    is asked here, so `state` carries a verdict for every agent with a capture
    credential, or says nothing is known (UNREACHABLE)."""
    login = _login_from_state(state, has_token=has_token, base_url=base_url)
    return dataclasses.replace(
        caps,
        logged_in_as=login.logged_in_as or None,
        api_credential_valid=login.api_credential_valid,
        capture_credential_valid=(
            state.capture.get(caps.agent_source) if caps.capture_token_sources else None
        ),
    )


#: The wizard's ONE server call for the `collect()` running in this context
#: (`capabilities.fetch_device_state`), as a zero-argument resolver -- usually
#: a pending future's bounded `result`. Scoped like the wizard scopes the agent
#: (`PROBE_AGENT`), so `collect()` keeps one signature for every caller.
_remote_state: ContextVar[Callable[[], DeviceState] | None] = ContextVar(
    "probe_wizard_device_state", default=None
)


@contextmanager
def device_state_scope(remote: Callable[[], DeviceState]) -> Iterator[None]:
    """Have `collect()` read the server's state from `remote` in this block."""
    token = _remote_state.set(remote)
    try:
        yield
    finally:
        _remote_state.reset(token)


def collect(*, local: bool = False, plugins: PluginState | None = None) -> Capabilities:
    """Snapshot this device. Every probe is individually fail-soft.

    Inside `device_state_scope` (the wizard) the server's half comes from its
    one call, resolved only AFTER the local checks so they run while the
    request is in flight: an answer means no network call here at all, and an
    older server without the route (`UNSUPPORTED`) means asking the old way.
    Outside it (`probe doctor`) this asks the old way, offline-first.

    `local` (`probe status` without --refresh) reads files only: no agent CLI
    runs and nothing is sent. The plugin lists come from the records the
    agents' own `plugin list` reads (`installed_plugins(local=True)`), Codex's
    MCP login from the header in its config.toml (what `codex mcp list` reports
    as `bearer_token`), and the server's half is unknown: no confirmed account
    (`logged_in_as` None), no verdict on any credential, no agent version. An
    OAuth Codex login is not in that file, so its MCP reads unknown, "not
    checked" (`CODEX_MCP_NOT_CHECKED`).

    `plugins`: this agent's plugin list, already read (`probe status --refresh`
    asks every agent's CLI at once), in place of asking here."""
    remote = None if local else _remote_state.get()
    from probe.cli import updater
    from probe.cli.capabilities import (
        TRACKING_PLUGIN_NAME,
        tracking_plugin_name,
    )
    from probe.cli.capabilities import (
        capture_device_id,
        capture_plugin_name,
        capture_token_sources,
        verify_capture_credential,
        agent_source,
        installed_plugins,
        tap_plugin_dir,
        CODEX_MCP_NAME,
        LEGACY_CODEX_TAP_PLUGIN_ID,
    )

    warnings: list[str] = []

    try:
        install_method = updater.detect_install().method
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        install_method = None

    base_url: str | None = None
    config_context: str | None = None
    has_token = False
    try:
        from probe.sdk.config import current_context_name, resolve

        settings = resolve()
        base_url = settings.base_url
        config_context = current_context_name()
        has_token = bool(settings.token)
    except Exception as exc:  # noqa: BLE001
        settings = None
        if base_url:
            warnings.append(f"could not verify login against {base_url}: {exc}")

    selected_agent = agent_source()
    # The profile's plugin: `probe-research-daemon` where the daemon records.
    TRACK = tracking_plugin_name(selected_agent)
    selected_tap = capture_plugin_name(selected_agent)
    if plugins is None:
        plugins = installed_plugins(source=selected_agent, local=local)
    try:
        from probe.cli import integration_repair

        unusable = integration_repair.unusable_plugins(selected_agent)
    except Exception:  # noqa: BLE001 -- a check, never a failed snapshot
        unusable = {}
    sources = capture_token_sources(selected_agent)
    # Resolved HERE, after the slowest local check above (the agent's own
    # plugin CLI), so that check ran while the request was in flight.
    state = remote() if remote is not None else None
    if local:
        login = _LoginCheck()
        credential_valid = None
    elif state is None or state.outcome is DeviceStateOutcome.UNSUPPORTED:
        # `probe doctor`, or a server that predates the one call: the old way.
        login = _check_login(settings) if settings is not None else _LoginCheck()
        credential_valid = verify_capture_credential(selected_agent) if sources else None
    else:
        login = _login_from_state(state, has_token=has_token, base_url=base_url)
        if not sources:
            credential_valid = None
        elif selected_agent in state.capture or not state.answered:
            credential_valid = state.capture.get(selected_agent)
        else:
            # Answered, but with no verdict for this agent: its credential is
            # paired to ANOTHER server and never rode in the call. Ask its own
            # server, the old way.
            credential_valid = verify_capture_credential(selected_agent)
    warnings[:0] = login.warnings
    logged_in_as = login.logged_in_as
    api_credential_valid = login.api_credential_valid
    unfiled = login.unfiled
    settings_autoupdate = autoupdate.load()

    if local:
        pass  # nothing was asked: "could not verify" would read as a failure
    elif credential_valid is False:
        warnings.append(
            "the capture credential was rejected by the ingest service; "
            "re-run `probe wizard` to pair this device again"
        )
    elif sources and credential_valid is None:
        warnings.append("could not verify the capture credential (offline or endpoint unavailable)")
    if LEGACY_CODEX_TAP_PLUGIN_ID in plugins:
        warnings.append(
            f"legacy {LEGACY_CODEX_TAP_PLUGIN_ID} is still installed and can race the unified tap; "
            "re-run `probe wizard` to remove it"
        )

    mcp_authenticated: bool | None = None
    codex_login_unread = False
    # The daemon profile installs no MCP, so there is no MCP login to check.
    if selected_agent == "codex" and TRACK == TRACKING_PLUGIN_NAME and TRACK in plugins:
        if local:
            from probe.cli import codex_config

            # `codex mcp list` answers `bearer_token` for any header there; an
            # OAuth login lives where only Codex can read it, so it is unknown.
            status = codex_config.BEARER_STATUS if codex_config.configured_bearer(CODEX_MCP_NAME) else None
            codex_login_unread = status is None
        else:
            status = plugin_cli.codex_mcp_auth_status(CODEX_MCP_NAME)
        if status is not None:
            mcp_authenticated = status in {"o_auth", "bearer_token"}
        if mcp_authenticated is False:
            warnings.append(
                "the probe-research MCP is installed but not logged in; "
                "re-run `probe wizard` to complete Codex OAuth"
            )

    # DRIFT IS CHECKED FOR ANY MACHINE THAT HAS A CODEX ENTRY, not just one
    # where Codex is the selected agent. A box with both agents installed
    # reports a single `agent_source`, so gating this on `== "codex"` made the
    # only local signal for a dead Codex token unreachable on exactly the
    # machines most likely to drift -- doctor printed "CLI + MCP: ok" while
    # every Codex call 401'd. `codex mcp list` cannot substitute: it reports
    # `bearer_token` for any header, valid or not.
    #
    # Unconditional is safe because the check is self-guarding: no configured
    # bearer, no held token, or the two agreeing all return None, and it reads
    # two files without shelling out.
    stale = stale_codex_token_warning()
    if stale:
        warnings.append(stale)

    if TokenSource.ENVIRONMENT in sources:
        token_env = tap_token_env(selected_agent)
        warnings.append(
            f"{token_env} is set in this shell. It overrides local pairing "
            "state, so capture can appear off in the menu yet still be on."
        )

    from probe.cli.capabilities import check_mcp

    # The per-agent MCP answer (Capabilities.mcp_state): Codex's reuses the
    # `codex mcp list` read above instead of asking again.
    mcp_kind, mcp_check = check_mcp(selected_agent, codex_auth=mcp_authenticated)
    if codex_login_unread and mcp_check is not None and mcp_check.credential == McpCredential.UNKNOWN:
        # Nothing ran: "`codex mcp list` did not answer" would be untrue.
        mcp_check = dataclasses.replace(mcp_check, what=CODEX_MCP_NOT_CHECKED)

    from probe.cli import versions as versions_mod

    rules_installed = agent_rules.is_installed()
    rules_stale = rules_installed and not agent_rules.is_current()

    version_rows, manifest_age = _version_comparison()
    tap_warning = tap_behind_warning(version_rows, selected_agent, "installed" if TRACK in plugins else None)
    if tap_warning:
        warnings.append(tap_warning)
    python_missing = capture_python_missing(selected_agent)
    if python_missing:
        warnings.append(
            "session capture cannot run: it needs Python 3.11 or newer, and the last "
            f"session start found {python_missing}. Install Python 3.11 or newer, "
            "then start a new session."
        )
    return Capabilities(
        # Not `__version__`: after the wizard's own Update that is the number
        # this process started with, while the Versions block above it grades
        # the upgrade. The two rows must agree.
        cli_version=versions_mod.cli_version(),
        version_rows=version_rows,
        version_manifest_age_s=manifest_age,
        install_method=install_method,
        claude_available=shutil.which("claude") is not None,
        agent_version=None if local else _agent_version(selected_agent),
        codex_available=shutil.which("codex") is not None,
        agent_source=selected_agent,
        logged_in_as=logged_in_as or None,
        api_credential_valid=api_credential_valid,
        base_url=base_url,
        config_context=config_context,
        # Installed means USABLE (plan clean-uninstall-reinstall R-T5): a record
        # whose files are gone, a disabled plugin, a project-scope install or
        # pi's filtered-out extension reads as not installed, so configure
        # puts it right instead of saying "Nothing to change".
        tracking_plugin_installed=TRACK in plugins and TRACK not in unusable,
        capture_plugin_installed=selected_tap in plugins and selected_tap not in unusable,
        legacy_capture_plugin_installed=LEGACY_CODEX_TAP_PLUGIN_ID in plugins,
        plugins_verified=plugins.verified,
        plugins_error=plugins.error,
        capture_token_sources=sources,
        capture_credential_valid=credential_valid,
        capture_killswitched=(tap_plugin_dir(selected_agent) / ".disabled").exists(),
        capture_awaiting_confirmation=_capture_awaiting_confirmation(selected_agent),
        capture_python_missing=python_missing,
        capture_device_id=capture_device_id(selected_agent),
        capture_last_stop=_capture_last_stop(),
        mcp_authenticated=mcp_authenticated,
        mcp_token_held=_mcp_token_held(),
        mcp_kind=mcp_kind,
        mcp_check=mcp_check,
        agent_rules_installed=rules_installed,
        agent_rules_stale=rules_stale,
        auto_update_enabled=settings_autoupdate.enabled,
        auto_update_by_default=settings_autoupdate.by_default,
        last_update_attempt=(
            _attempt_as_it_stands(
                settings_autoupdate.last_attempt, _probe_plugin_of(selected_agent, TRACK in plugins)
            ).describe()
            if settings_autoupdate.last_attempt
            else None
        ),
        last_update_attempt_summary=(
            settings_autoupdate.last_attempt.summary()
            if settings_autoupdate.last_attempt
            else None
        ),
        last_update_skip=(
            settings_autoupdate.last_skip.describe() if settings_autoupdate.last_skip else None
        ),
        live_runs=_live_runs(),
        outbox_status=_outbox_status(),
        unfiled_runs=unfiled,
        daemon_ai_libraries=_daemon_ai_libraries(),
        warnings=warnings,
    )


def _probe_plugin_of(selected: str, selected_has_it: bool):
    """`plugin_after` for `updater.settle_stale_notes`: an agent's installed
    Probe plugin ("installed"), or None when it has none. The agent doctor runs
    for is known (`selected_has_it`, from its own plugin read); another is read
    from the record its own plugin list reads (`installed_plugins(local=True)`:
    files only, no agent CLI started). Unreadable: None, which keeps a watcher
    from before the hand-back on the restart line."""
    def plugin_after(source: str) -> str | None:
        if source == selected:
            return "installed" if selected_has_it else None
        try:
            from probe.cli.capabilities import installed_plugins

            return "installed" if tracking_plugin_name(source) in installed_plugins(source=source, local=True) \
                else None
        except Exception:  # noqa: BLE001 - see docstring
            return None

    return plugin_after


def _attempt_as_it_stands(attempt, plugin_after):
    """The last update attempt as `probe doctor` prints it: what it said about
    sessions still on an older tap as it stands now (`updater.settle_stale_notes`:
    gone once none is left, "they move ... no restart needed" where they follow).
    Every release before 0.304.0 told the person to restart them; the sessions
    move with no restart, and doctor kept printing "restart them" until the next
    update. Never raises: the attempt as recorded."""
    try:
        import dataclasses

        from probe.cli import updater

        settled = updater.settle_stale_notes(attempt.plugin_detail, plugin_after=plugin_after)
        return attempt if settled == attempt.plugin_detail else dataclasses.replace(attempt, plugin_detail=settled)
    except Exception:  # noqa: BLE001 - see docstring
        return attempt


def _mcp_token_held() -> bool:
    from probe.cli.setup import current_mcp_token

    return bool(current_mcp_token() or os.environ.get("PROBE_MCP_TOKEN"))


def _daemon_ai_libraries() -> str | None:
    try:
        from probe.cli.daemon_cli import located_ai_libraries

        return located_ai_libraries() or "missing"
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


def _capture_awaiting_confirmation(source: str) -> bool:
    try:
        from probe.cli import capture

        return capture.awaiting_confirmation(source)
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return False


def _capture_last_stop() -> str | None:
    try:
        from probe.cli import capture

        return capture.describe_last_stop()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


#: Left in the tap's state folder by its SessionStart when it found no Python
#: 3.11+ to run the tap on (`hooks/tap-python.sh` TAP_PYTHON_MISSING), holding
#: what it found instead; removed by the next one that finds one.
TAP_PYTHON_MISSING = ".python-missing"


def capture_python_missing(source: str) -> str | None:
    """What the tap's last SessionStart found instead of a Python 3.11+
    ("python3 3.9.6", "no python3"), or None when it found one.

    The hook is the one that knows: it resolves the interpreter the way it runs
    the tap, so this reads its verdict rather than guessing at its search."""
    from probe.cli.capabilities import tap_plugin_dir

    try:
        text = (tap_plugin_dir(source) / TAP_PYTHON_MISSING).read_text(encoding="utf-8")
    except (OSError, KeyError, ValueError):  # no tap for this agent, no file, not text
        return None
    lines = text.strip().splitlines()
    return (lines[0].strip()[:80] if lines else "") or "no python3 that runs"


def _agent_version(source: str) -> str | None:
    """The selected agent binary's version. Fail-soft, like every other probe.

    `agent_source()` speaks "claude_code"/"codex"; `Agent` is "claude"/"codex".
    Mapped explicitly rather than passed straight to `Agent(...)`: that raises
    on "claude_code", the fail-soft `except` swallows it, and the field reads
    None on every machine -- a version probe that reports nothing, forever,
    while looking like it works.

    pi DOES have an `Agent` member now, and it is still not asked here: it is
    not an importer (`backfill.IMPORTER_AGENTS` is the claude/codex pair this
    probe reports on, and `resolve_agent` refuses `--agent pi`), and its
    version is not a fact about the import this line describes. The old `else`
    here defaulted straight to `Agent.CLAUDE`, which reported Claude Code's OWN
    version string as if it were pi's -- correct-looking output for the wrong
    question. None, same as every other "cannot check" case this function
    already returns.
    """
    if source in ("pi", plugin_cli.KIMI):
        return None
    try:
        from probe.cli.backfill import Agent, agent_version

        agent = Agent.CODEX if source == "codex" else Agent.CLAUDE
        return agent_version(agent)
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


def _kimi_rows() -> list[str]:
    """Kimi Code's binary and version (Probe needs 2.1.1+), and whether its
    plugin list is one the wizard can manage (Kimi has no install command, so
    the wizard writes that file; a layout it does not know is left alone)."""
    from probe.cli import kimi_config

    rows = []
    if not kimi_config.binary_available():
        rows.append(_row("Kimi Code CLI", _MISSING))
        return rows
    version = kimi_config.kimi_version()
    state = f"{_OK} ({'.'.join(map(str, version))})" if version else _OK
    problem = kimi_config.version_floor_problem()
    rows.append(_row("Kimi Code CLI", f"{state} -- {problem}" if problem else state))
    doc, refused = kimi_config._read_installed()  # noqa: SLF001 -- the same check the installer runs
    if refused:
        rows.append(_row("Kimi plugin list", f"not managed: {refused}"))
    else:
        ours = sorted(
            p.get("id") for p in doc["plugins"] if isinstance(p, dict) and p.get("id") in kimi_config.PLUGIN_IDS
        )
        rows.append(_row("Kimi plugin list", ", ".join(ours) if ours else "no Probe plugins"))
    return rows


def _live_runs() -> list[str]:
    try:
        from probe.cli import run_lock

        return run_lock.live_runs()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return []


def _outbox_status() -> dict | None:
    """The outbox's status.json, read only (`collect` runs from `probe
    status`, which promises no request and no process)."""
    try:
        from probe.sdk.journal import Journal

        return Journal.read_status()
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None


def rescue_outbox() -> dict | None:
    """`probe doctor`'s fix: rescue, now, writes stranded under a dead
    credential of the logged-in account (`journal.rescue_stranded`; any
    `probe` command does it by itself every 10 minutes) and start sending
    them in the background. Under the one rescue lock; None when there is
    nothing to say, or another rescue is running."""
    try:
        from probe.sdk import outbox_worker
        from probe.sdk.journal import (
            Journal,
            _stored_login_fingerprint,
            _try_lock,
            rescue_lock_path,
            rescue_stranded,
        )

        root = Journal()
        if not outbox_worker.rescue_enabled() or root.paused:
            return None
        login = _stored_login_fingerprint(None)
        here = set(outbox_worker.env_fingerprints()) | ({login} if login else set())
        lock = rescue_lock_path()
        lock.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with _try_lock(lock) as mine:
            if not mine:
                return None
            report = rescue_stranded(root, here=here)
        if report.rescued or report.adopted_waiting:
            outbox_worker.spawn_rescuer(root)
        if not (report.rescued or report.refused or report.adopted_waiting):
            return None
        return {
            "rescued": dict(report.rescued),
            "cannot_rescue": {fp: str(why) for fp, why in report.refused.items()},
            "adopted_waiting": report.adopted_waiting,
        }
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return None
