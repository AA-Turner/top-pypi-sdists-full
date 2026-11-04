"""Where a run opens when its caller names no project: ONE order for the SDK, the CLI and
offline runs (session-project D3). Network-free: the create path checks what it names
(twin: app/runs). With nothing named, a run in a daemon session waits for the daemon's pick,
a person at a terminal is asked, and anything else is refused saying what fits (plan T2, T3)."""

from __future__ import annotations

import contextlib
import os
import sys
import time
from collections.abc import Callable, Iterator, Mapping
from typing import Any, NamedTuple

from probe.foundation.compat.compat import StrEnum

from .... import agent_session, errors, session_marker, writer_requests
from ....settings.settings import ProjectSource, Settings

#: The run metadata key that says which unnamed home a run opened in (D4).
HOME_SOURCE_KEY = "home_source"
#: The run metadata key for how long the run waited for the daemon's pick, in seconds.
HOME_WAIT_KEY = "home_wait_s"
#: How long a run waits for the daemon to pick its session's project, in seconds. A writer
#: request queued behind a bite already running waits for it (~70 s seen), then ~20 s to pick.
HOME_WAIT_S = 90.0
HOME_POLL_S = 0.5
#: What the waiting run asks the session's daemon writer (`probe ask --writer`'s file format).
HOME_REQUEST_TEXT = "A run is starting and needs this session's project: set it now with `probe session home set`."
#: How an `id:` ref is spelled: only ever the id (`Client._project_named`).
ID_PREFIX = "id:"


class HomeSource(StrEnum):
    """Which rule named a run's home (`resolve_run_home`), first match wins."""

    EXPLICIT = "explicit"  # project= / experiment= (--project / --experiment), or resolve(project=)
    ENV = "env"  # PROBE_PROJECT
    SESSION = "session"  # this session's project (`probe session home set`, the daemon's)
    CONTEXT = "context"  # this computer's active project (`probe project use`)
    PICKED = "picked"  # typed by the person at this terminal when nothing named one (`ProjectPicker`)


#: Homes nobody typed for this run: said aloud on stderr and kept in its metadata.
NOTICED_SOURCES = frozenset({HomeSource.SESSION, HomeSource.CONTEXT, HomeSource.PICKED})

_NOTICE_REASONS = {
    HomeSource.SESSION: "this session's project, set by the Probe daemon",
    HomeSource.CONTEXT: "this computer's active project from `probe project use`",
    HomeSource.PICKED: "picked just now",
}


class MissingHome(StrEnum):
    """Why nothing will name a run's home (`get_missing_home_case`); each has its own fix."""

    HAND_RUN = "hand_run"  # no coding agent in the environment: a person ran it
    NOT_DAEMON = "not_daemon"  # an agent session the Probe daemon does not record
    DAEMON_DOWN = "daemon_down"  # the `daemon` state, but its worker is not running
    DAEMON_SLOW = "daemon_slow"  # the daemon did not pick one within HOME_WAIT_S
    DAEMON_ITSELF = "daemon_itself"  # the daemon's own `probe` command (`PROBE_DAEMON_SESSION`)
    ELSEWHERE = "elsewhere"  # the session's project is set, but on another server or team


#: Every way to name a project, for the agent cases.
_NAME_ONE = ("Pass project= (CLI: --project), set PROBE_PROJECT, or run `probe project use <slug>`; "
             "if none fits, `probe project create <slug> --kind <kind>`.")
MISSING_HOME_FIXES = {
    MissingHome.HAND_RUN: (
        'probe: this run needs a project. Pass one: probe.init(project="<slug or id>"), or set one for '
        "this computer: probe project use <slug>. Your projects: probe project list. "
        "None fits: probe project create <slug> --kind <kind>"),
    MissingHome.NOT_DAEMON: (
        "probe: this run needs a project. The Probe daemon does not record this session, so nothing "
        "will set this session's project (`probe session home show`). " + _NAME_ONE),
    MissingHome.DAEMON_DOWN: (
        "probe: this run needs a project. This session's Probe daemon is not running, so nothing will "
        "set this session's project; `probe doctor` says why. " + _NAME_ONE),
    MissingHome.DAEMON_ITSELF: (
        "probe: this run needs a project, and the Probe daemon picks this session's project itself: "
        "pass --project, or set the session's project first (`probe session home set <project>`)."),
    MissingHome.ELSEWHERE: (
        "probe: this run needs a project. This session's project is set on another Probe server or "
        "team than this run's credential (`probe session home show`). " + _NAME_ONE),
    MissingHome.DAEMON_SLOW: (
        f"probe: this run needs a project. The Probe daemon did not set this session's project within "
        f"{int(HOME_WAIT_S)} s (`probe session home show` prints it once set). " + _NAME_ONE),
}


class RunHome(NamedTuple):
    """`(project, experiment, source)` as refs the create path takes; `source` is None when
    nothing names a home. `name`: the session home's slugs, for the notice and its errors.
    `waited_s`: how long the run waited for the daemon to pick it (`wait_for_session_home`)."""

    project: str | None
    experiment: str | None
    source: HomeSource | None
    name: str | None = None
    waited_s: float | None = None


def get_session_id(env: Mapping[str, str] | None = None) -> str | None:
    """This conversation's id: the coding agent's own variable, else the one a launcher or the
    daemon forwarded (`PROBE_AGENT_SESSION`, which every daemon `probe` call carries)."""
    own = agent_session.session_id_from_env(env)
    if own:
        return own
    forwarded = agent_session.forwarded_agent_session(env)
    return forwarded[1] if forwarded else None


def load_customer_id(settings: Settings) -> str | None:
    """The team this credential belongs to, from what this machine already recorded
    (no request), or None when it never looked."""
    from ....delivery.outbox.drain.accounts import recorded_account
    from ....delivery.outbox.drain.credentials import credential_fingerprint

    account = recorded_account(credential_fingerprint(settings.token, None))
    if account is not None:
        return account[0]
    from ....delivery.offline.offline import cached_identity

    return cached_identity(settings).get("customer_id")


def load_session_home(settings: Settings, env: Mapping[str, str] | None = None) -> dict | None:
    """This session's run home, when it was decided on this credential's server and team
    (Codex O2); else None. A team this machine never looked up is not a mismatch: a home
    from another team names ids this one does not have, so its create fails loudly."""
    session_id = get_session_id(env)
    record = session_marker.read_run_home(session_id) if session_id else None
    if record is None or record["base_url"].rstrip("/") != settings.base_url.rstrip("/"):
        return None
    team = record.get("customer_id")
    if team and load_customer_id(settings) not in (None, team):
        return None
    return record


def resolve_run_home(
    project: str | None,
    experiment: str | None,
    settings: Settings,
    env: Mapping[str, str] | None = None,
) -> RunHome:
    """The run's home: what the caller named, else `PROBE_PROJECT`, else this session's
    project, else `probe project use`, else none. Only when NEITHER is named: beside an
    experiment an ambient project would scope its tenant-wide lookup (DESIGN.md)."""
    if project or experiment:
        return RunHome(project, experiment, HomeSource.EXPLICIT)
    source = settings.project_source
    if settings.project and source is not ProjectSource.CONTEXT:
        return RunHome(settings.project, None, HomeSource.ENV if source is ProjectSource.ENV else HomeSource.EXPLICIT)
    record = load_session_home(settings, env)
    if record is not None:
        return _home_from_record(record)
    if settings.project:
        return RunHome(settings.project, None, HomeSource.CONTEXT)
    return RunHome(None, None, None)


def _home_from_record(record: dict, waited_s: float | None = None) -> RunHome:
    """A session home record as the run's home: by id, so a renamed one is still found."""
    if record.get("experiment_id"):
        # The experiment alone, by id: it is found wherever it is filed now (Codex O1).
        name = f"{record['project']}/{record['experiment']}"
        return RunHome(None, ID_PREFIX + record["experiment_id"], HomeSource.SESSION, name, waited_s)
    return RunHome(ID_PREFIX + record["project_id"], None, HomeSource.SESSION, record["project"], waited_s)


def get_missing_home_case(env: Mapping[str, str] | None = None) -> MissingHome | None:
    """Why nothing will name this run's home, or None when this session's daemon is running
    and may still pick it (`wait_for_session_home`). Local files only."""
    session_id = get_session_id(env)
    if not session_id:
        # A coding agent with no session id (an older one) is still no person at a prompt.
        return MissingHome.NOT_DAEMON if agent_session.detect_agent(env) else MissingHome.HAND_RUN
    if (env if env is not None else os.environ).get(agent_session.DAEMON_SESSION_ENV):
        return MissingHome.DAEMON_ITSELF  # the daemon's own command: it would wait for itself
    state = session_marker.session_state(session_id)
    if state != session_marker.STATE_DAEMON:
        return MissingHome.NOT_DAEMON
    # The worker renews its lease every poll: a live lease is a running worker (240 s TTL). A
    # fresh hand-over (a resumed session's next worker taking over) is not a stopped daemon.
    status = session_marker.daemon_status(session_id, state)
    if status is None or (status[0] != session_marker.DAEMON_LIVE and status[1] != session_marker.DAEMON_HANDOVER):
        return MissingHome.DAEMON_DOWN
    return None


def build_missing_home_error(env: Mapping[str, str] | None = None) -> errors.ProjectRequired:
    """`ProjectRequired` with the fix that fits why nothing named a home."""
    case = get_missing_home_case(env)
    return errors.ProjectRequired(MISSING_HOME_FIXES[case] if case is not None else "")


def wait_for_session_home(
    settings: Settings,
    env: Mapping[str, str] | None = None,
    *,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> RunHome:
    """Ask this session's daemon writer to pick the session's project and wait for it, at most
    HOME_WAIT_S, saying so on stderr; a daemon that stops meanwhile ends the wait early.
    Raises `ProjectRequired` (the fix for that case) when no project came."""
    session_id = get_session_id(env)
    if _is_home_elsewhere(settings, env):
        raise errors.ProjectRequired(MISSING_HOME_FIXES[MissingHome.ELSEWHERE])
    try:
        writer_requests.write_writer_request(session_id, HOME_REQUEST_TEXT)
    except (OSError, RuntimeError):
        pass  # best effort: the writer still sees the agent's request in the transcript
    _say(f"probe: waiting for the daemon to pick this session's project (up to {int(HOME_WAIT_S)} s)...")
    started = clock()
    while True:
        record = load_session_home(settings, env)
        if record is not None:
            return _home_from_record(record, waited_s=round(clock() - started, 1))
        if _is_home_elsewhere(settings, env):
            raise errors.ProjectRequired(MISSING_HOME_FIXES[MissingHome.ELSEWHERE])
        case = get_missing_home_case(env)
        if case is None and clock() - started >= HOME_WAIT_S:
            case = MissingHome.DAEMON_SLOW
        if case is not None:
            raise errors.ProjectRequired(MISSING_HOME_FIXES[case])
        sleep(HOME_POLL_S)


def _is_home_elsewhere(settings: Settings, env: Mapping[str, str] | None) -> bool:
    """The session has a home record, but for another server or team: waiting cannot help."""
    session_id = get_session_id(env)
    if not session_id or session_marker.read_run_home(session_id) is None:
        return False
    return load_session_home(settings, env) is None


def find_missing_home(client: Any, env: Mapping[str, str] | None = None) -> RunHome:
    """Nothing named the run's home: wait for this session's daemon to pick it, or ask the
    person at this terminal (no agent session); otherwise raise `ProjectRequired` with the fix
    that fits the case."""
    case = get_missing_home_case(env)
    if case is None:
        return wait_for_session_home(client.settings, env)
    if case is MissingHome.HAND_RUN:
        from ..projects.picker import ProjectPicker

        picker = ProjectPicker(client, env=env)
        if picker.can_ask():
            client.ensure_authenticated()  # a person signs in first, not mid-prompt
            picked = picker.pick()
            if picked is not None:
                return RunHome(ID_PREFIX + picked["id"], None, HomeSource.PICKED, picked.get("slug"))
    raise errors.ProjectRequired(MISSING_HOME_FIXES[case])


def mark_home_source(home: RunHome, run_kw: dict) -> None:
    """Record an unnamed home's source in the run's `metadata` (D4), and how long it waited."""
    if home.source in NOTICED_SOURCES:
        marks = {HOME_SOURCE_KEY: home.source.value}
        if home.waited_s is not None:
            marks[HOME_WAIT_KEY] = home.waited_s
        run_kw["metadata"] = {**(run_kw.get("metadata") or {}), **marks}


def make_notice(home: RunHome, filed_in: str | None) -> str | None:
    """The one line saying where a run went and why, for a home nobody typed (D4)."""
    reason = _NOTICE_REASONS.get(home.source) if home.source is not None else None
    where = home.name or filed_in or home.project or home.experiment
    if reason is None or not where:
        return None
    if home.waited_s is not None:
        return f"probe: run filed in {where} (picked by the daemon after {home.waited_s:g} s)"
    return f"probe: run filed in {where} ({reason}; pass project= or --project to choose another)"


def print_notice(home: RunHome, filed_in: str | None) -> None:
    """`make_notice` on stderr. Never raises: the run is already open."""
    line = make_notice(home, filed_in)
    if line is not None:
        _say(line)


def _say(line: str) -> None:
    """One line on stderr; never raises (a closed stderr is no reason to fail a run)."""
    try:
        print(line, file=sys.stderr, flush=True)
    except (OSError, ValueError):
        pass


@contextlib.contextmanager
def explain_missing_home(home: RunHome) -> Iterator[None]:
    """A session home whose project or experiment is gone (deleted, in the trash, another
    team's) fails naming the home and the fix, never falling through elsewhere (review F3)."""
    try:
        yield
    except errors.RosError as exc:
        gone = isinstance(exc, errors.NotFoundError) or exc.in_trash
        if home.source is not HomeSource.SESSION or not gone:
            raise
        named = errors.NotFoundError(
            f"this session's project {home.name} was not found with this credential ({exc}). "
            "`probe session home show` prints it; pass project= or --project to file this run elsewhere.",
            status=exc.status,
            detail=exc.detail,
        )
        named.in_trash = exc.in_trash
        raise named from exc
