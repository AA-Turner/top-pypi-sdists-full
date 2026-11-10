"""What this coding-agent session has put in Probe, answerable without a network call.

The backend already knows: every write carries the session id (see
:mod:`probe.sdk.agent_session`), and ``GET /v1/sessions/{id}/work`` reads it back.
That answer is authoritative and costs 50-90ms. This module is the LOCAL CACHE of
it, because the consumer is a terminal status line that re-renders constantly and
must never touch the network, an auth token, or a `probe` process.

    ~/.local/state/probe/sessions/<session_id>.json

The division of labour is deliberate:

  a plugin hook REFRESHES this file in the background, from the server
  a status-line script READS it, in stdlib python, in about 30ms

One writer is instrumented anyway: the daemon, after each of its writes lands,
stores that write's project in ``<session_id>.scope`` (:mod:`probe.daemon.scope`),
and :func:`read` shows it in place of the server's guess at the project. Run ids,
liveness and capture still come from the refresh.

Refreshing from the server rather than instrumenting the SDK's create paths is
what makes the answer complete. A session's work can be created through the SDK,
the CLI, the hosted MCP, or a training script three processes deep; only one of
those runs code we could have hooked, and a status line that says "untracked"
because it missed a path is worse than no status line.

STALENESS IS THE ACCEPTED COST, and it is bounded by how often the refresher
runs, not by anything here. `updated_at` is carried so a reader can tell a fresh
answer from an abandoned one.

STDLIB ONLY, AND PYTHON 3.9. This file is vendored into the plugin's hooks
directory, where it executes under the SYSTEM python3 with no `probe` package
importable — macOS still ships 3.9, so nothing newer than that may appear here.
This file is kept as pieces in src/probe/sdk/marker/ (edit there). `tools/vendor.py`
joins them into src/probe/sdk/session_marker.py and the hooks' `_session_marker.py`,
which must stay byte-identical: `make sync-session-marker sync-daemon-plugin` refreshes
them, and tests/test_session_marker_parity.py fails CI whenever they differ.

FAIL-SOFT THROUGHOUT. Nothing here may raise into a caller: the writer runs beside
a research write that must survive a full disk, and the reader runs on a render
path where an exception is a broken prompt.
"""

from __future__ import annotations

import enum
import json
import math
import os
import re
import stat
import time
import unicodedata
from pathlib import Path

#: Mirrors probe.version_policy.STATE_DIRNAME. Duplicated rather than imported
#: because the vendored copy has no `probe` package to import from;
#: tests/test_session_marker.py asserts the two resolve to the same directory.
STATE_DIRNAME = "probe"
SESSIONS_DIRNAME = "sessions"

#: A marker older than this is not shown at all. A status line asserting a
#: project from a conversation someone abandoned last month is a lie with a
#: confident glyph on it; saying nothing is the honest answer.
MAX_AGE_SECONDS = 30 * 86400

#: `<session>.scope` beside the marker: the project the daemon's latest write
#: landed in (`write_scope`). Its own file because the refresh hook replaces the
#: marker whole. `prune` sweeps it with the rest of the directory.
SCOPE_SUFFIX = ".scope"
#: `<session>.home` beside it: where this session's runs go (`write_run_home`), set by
#: the daemon. Not a key in `.scope`, which every landed write rewrites. `prune` sweeps it.
HOME_SUFFIX = ".home"
#: `<session>.workspace` beside it: where a project this session creates is filed
#: (`write_session_workspace`), set by `probe example start` (agent-prompt install D68). `prune` sweeps it.
WORKSPACE_SUFFIX = ".workspace"
#: A bound on a project name this file stores or shows. Server slugs are
#: free-form TEXT; the segment elides a long one anyway, so this only keeps a
#: pathological value off the render path.
MAX_LABEL_CHARS = 1024
#: Unicode categories a label may not hold: controls (an escape sequence),
#: format characters (bidi overrides, zero-width), line and paragraph
#: separators, surrogates and private use. Not `Cn` (unassigned): the hook's
#: python can be older than the daemon's, and a newer emoji is unassigned there.
_UNPRINTABLE = frozenset({"Cc", "Cf", "Zl", "Zp", "Cs", "Co"})

#: How a message sends someone to fix this device from the chat (fixes-1107b): the
#: command the agent runs itself, never the wizard or "a terminal"
#: (tests/test_no_terminal_handoff.py). Here because every surface reaches this file
#: (the SDK imports it, the hooks vendor it); the tap, the pi extension, safe_warn and
#: two shell scripts copy SIGN_IN_HINT (tests/test_sign_in_hint_sync.py).
SIGN_IN_HINT = "run `npx -y probe-research sign-in --json`"
UPDATE_HINT = "run `npx -y probe-research update --json`"
#: The install, keeping every choice: it re-pairs capture and re-points the agents' MCP.
INSTALL_HINT = "run `npx -y probe-research install --yes --json`"
#: Checks every part of this machine's Probe and fixes what fails (the CLI's env included).
REPAIR_HINT = "run `npx -y probe-research repair --json`"
#: Who records -> the daemon again: its key from the sign-in, and its AI libraries. A
#: `--who-records` change records less by the gate's rule, so only on the person's ask (UC2).
DAEMON_HINT = ("ask your agent to set Who records to the daemon "
               "(`npx -y probe-research install --yes --json --who-records daemon --directed`)")

_ELLIPSIS = "…"  # …
#: The status line's one glyph. Its colour says the kind of state (green on, yellow read, red off or broken); the words
#: say it too, so nothing is lost with colour off.
_DOT = "●"  # ●
_INDENT = "  "  # the segment is concatenated after a chained neighbour: keep a gap
_GLYPH_WIDTH = 2  # the dot plus its trailing space

#: The segment's fields, joined: `● <state words> | <title> | <note>` (Richard 2026-11-07; no `Probe |` prefix, 11-08).
STATUS_DIVIDER = " | "

#: The one note a line carries, most serious first. Problems only, plus `transcripts off`, which is why a daemon chat
#: records nothing. Failure lines carry the status alone, never a command (Richard 2026-11-07).
NOTE_TRANSCRIPT_NOT_RECORDED = "session transcript not recorded"
NOTE_DAEMON_NOT_RECORDING = "daemon not recording"
NOTE_TRANSCRIPTS_OFF = "transcripts off"
NOTE_STATUS_UNAVAILABLE = "Probe status unavailable"
NOTE_SERVICE_DOWN = "Probe service down"
NOTE_SIGNED_OUT = "signed out of Probe"
NOTE_NOTHING_FILED = "nothing filed yet"  # the notice's, when the chat has filed nothing

#: The capture reason for transcripts turned off on purpose (`capture_state.TURNED_OFF_REASON`).
_CHOSEN_OFF_REASON = "turned off"
_MAX_LOWERED_CHARS = 24

#: Room for a title when a note shares the line: the length of Richard's example title (`BIRD SFT Fine Tuning`).
TITLE_ROOM_WITH_NOTE = 20
#: A title past this many characters is not one (the server's own name limit).
MAX_TITLE_LEN = 200
#: How many project titles the marker keeps (the last rows of the work read; the picked project is the last).
MAX_TITLE_ROWS = 32

#: The segment's ceiling in terminal columns, leading indent included: the widest line that must render whole,
#: `  ● on (daemon) | <20-column title> | session transcript not recorded` (72). Derived, so it moves when
#: the words do; only words reachable today count (a manual chat's `, manual` re-derives it).
MAX_SEGMENT_CHARS = (
    len(_INDENT) + _GLYPH_WIDTH + len("on (daemon)")
    + len(STATUS_DIVIDER) + TITLE_ROOM_WITH_NOTE + len(STATUS_DIVIDER) + len(NOTE_TRANSCRIPT_NOT_RECORDED)
)
#: The title's budget with no note: the same in every state, so it never moves when the state does.
MAX_TITLE_CHARS = (
    MAX_SEGMENT_CHARS - len(_INDENT) - _GLYPH_WIDTH
    - len("read (daemon)") - len(STATUS_DIVIDER)
)
#: Below this many columns a cut title names nothing: it is dropped (a guard against unbounded input).
_MIN_TITLE_CHARS = 8

# Basic SGR codes, never 256-colour: the line renders inside the user's own terminal theme.
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"
_RESET = "\033[0m"

# Session ids are uuids today; the bound and charset are the real guard, since
# this value becomes a filename. Matches agent_session._SESSION_RE deliberately:
# a value that could never have been sent as a header must never mint a file.
_SESSION_RE = re.compile(r"\A[A-Za-z0-9._:-]{8,200}\Z")


def valid_session_id(raw: object) -> bool:
    """Whether a value is safe to use as a marker filename."""
    return isinstance(raw, str) and bool(_SESSION_RE.match(raw))


def _home() -> Path:
    """`~`, or the SDK's private stand-in when this process has none (HOME
    unset and no passwd entry: `probe.foundation.durable.homedir`). The vendored hook copy has
    no `probe` package to import; there a missing home raises, as it always did."""
    try:
        from probe.sdk import homedir  # restructure-guard-ok: released hooks run this copy against older CLIs
    except ImportError:
        return Path.home()
    return homedir.home()


def state_dir() -> Path:
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else _home() / ".local" / "state"
    return base / STATE_DIRNAME


def sessions_dir() -> Path:
    return state_dir() / SESSIONS_DIRNAME


def marker_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + ".json")


#: How long `probe paper find` keeps the papers hook from holding a web search,
#: and how long one hold keeps it from holding another (`papers_hook.py`).
PAPER_FIND_WINDOW_S = 15 * 60


def paper_find_stamp_path(session_id: str) -> Path:
    """Touched by `probe paper find` when it starts: the session tried Probe's
    paper search, so the papers hook lets web searches through."""
    return sessions_dir() / (session_id + ".papers")


def paper_hold_stamp_path(session_id: str) -> Path:
    """Touched by the papers hook when it holds a web search."""
    return sessions_dir() / (session_id + ".papers-held")


def paper_cli_cache_path(session_id: str) -> Path:
    """The papers hook's per-session answer to "does the local CLI have
    `probe paper find`?" (asking, `probe paper find --help`, costs ~0.9 s)."""
    return sessions_dir() / (session_id + ".papers-cli")


# ---------------------------------------------------------------------------
# Read / write
# ---------------------------------------------------------------------------


def _read_marker(session_id: str) -> dict | None:
    """This session's cached work as the refresh hook stored it, or None.

    None for absent, unreadable, malformed, and EXPIRED alike — every one of
    them means "we cannot say what this session tracked", and a reader that
    had to tell them apart would only be able to render the same nothing.
    """
    if not valid_session_id(session_id):
        return None
    try:
        with open(marker_path(session_id), encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, ValueError):
        return None
    if not isinstance(state, dict):
        return None
    if not _fresh(state.get("updated_at")):
        return None
    return state


def _fresh(updated_at: object) -> bool:
    """Inside the age window. A future timestamp (clock skew, a restored backup)
    must not pin a file as fresh forever, so anything outside the window, either
    side, is expired -- and so is a value no clock wrote (NaN, an int too large
    for a float), which must not raise on a render path."""
    if isinstance(updated_at, bool) or not isinstance(updated_at, (int, float)):
        return False
    try:
        return math.isfinite(updated_at) and abs(time.time() - float(updated_at)) <= MAX_AGE_SECONDS
    except OverflowError:
        return False


def read(session_id: str) -> dict | None:
    """This session's cached work, or None — with the project the daemon last
    wrote to (`read_scope`) in place of the server's, when there is one.

    The server's `project` is a GUESS at what the session works on now: the last
    of the projects it touched, in an order that ties for every project of one
    session (each link row carries the SESSION's first sighting), so it falls to
    uuid order and never moves. The daemon's scope is where its writes actually
    landed. The scope only refines a marker: without one, nothing is installed
    to refresh it, and the answer is None as before. Every reader of the marker
    — the segment, the notice, `probe statusline show` — goes through here, so
    they cannot come to name different projects, and a name neither file may
    print (`_printable`) is dropped here for all of them.
    """
    state = _read_marker(session_id)
    if state is None:
        return None
    record = _read_scope_record(session_id)
    if record is not None:
        state = {**state, "project": record["project"]}
    elif state.get("project") is not None and not _printable(state.get("project")):
        state = {**state, "project": None}
    return {**state, "project_title": _pick_title(state, record)}


def _pick_title(state: dict, scope: "dict | None") -> "str | None":
    """The title for the winning slug: the newer of the marker's title map (refreshed from the server) and the
    daemon's scope title, each by when it was observed. None: neither knows one (the line shows the slug)."""
    slug = state.get("project")
    if not isinstance(slug, str):
        return None
    titles = state.get("project_titles")
    mapped = titles.get(slug) if isinstance(titles, dict) else None
    mapped = mapped if is_printable_title(mapped) else None
    scoped = scope.get("title") if scope is not None and scope.get("project") == slug else None
    scoped = scoped if is_printable_title(scoped) else None
    if mapped and scoped:
        mapped_at, scoped_at = _finite(state.get("titles_at")) or 0.0, _finite(scope.get("updated_at")) or 0.0
        return scoped if scoped_at > mapped_at else mapped
    return mapped or scoped


def scope_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + SCOPE_SUFFIX)


def _printable(value: object) -> bool:
    """A project name the segment can print: one bounded line, nothing a terminal
    or a bidi renderer would act on. It comes from the server, where slugs are
    free-form, so it is checked, not trusted."""
    return (isinstance(value, str) and 0 < len(value) <= MAX_LABEL_CHARS
            and all(unicodedata.category(ch) not in _UNPRINTABLE for ch in value))


#: Format characters a title may carry: ZWJ and the emoji variation selector build emoji (`👩‍🔬`); every other `Cf`
#: (bidi controls above all) stays refused.
_TITLE_ALLOWED_CF = frozenset({"\u200d", "\ufe0f"})


#: Combining marks a title may stack on one character: scripts with diacritics use up to 3; more draws over the
#: rows around it in many terminals (a teammate names the project).
MAX_TITLE_MARKS = 4


def _has_mark_stack(value: str) -> bool:
    run = 0
    for ch in value:
        run = run + 1 if unicodedata.category(ch) in ("Mn", "Me") else 0
        if run > MAX_TITLE_MARKS:
            return True
    return False


def is_printable_title(value: object) -> bool:
    """A project title the line can print: like `_printable`, but capped at the server's own name limit, letting the
    two characters emoji are built from through, and refusing a pile of combining marks."""
    return (isinstance(value, str) and 0 < len(value) <= MAX_TITLE_LEN
            and all(ch in _TITLE_ALLOWED_CF or unicodedata.category(ch) not in _UNPRINTABLE for ch in value)
            and not _has_mark_stack(value))


def write_scope(session_id: str, project: str, project_id: str | None = None, title: str | None = None) -> bool:
    """Record the project the daemon's latest write landed in (its slug, its id so a delete by id can clear it, and
    its title when the lookup read the project row). True when it landed; a title that fails `is_printable_title` is
    dropped and the slug kept.

    A file of its own, not a key in the marker: the refresh hook REPLACES the
    marker every few seconds from the server's answer, and a second writer's key
    would be gone at the next refresh.
    """
    if not valid_session_id(session_id) or not _printable(project):
        return False
    record = {"project": project, "project_id": project_id, "updated_at": time.time()}
    if is_printable_title(title):
        record["title"] = title
    return _publish_atomically(scope_path(session_id), json.dumps(record) + "\n")


def _read_scope_record(session_id: str) -> dict | None:
    if not valid_session_id(session_id):
        return None
    try:
        with open(scope_path(session_id), encoding="utf-8") as handle:
            record = json.load(handle)
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or not _fresh(record.get("updated_at")):
        return None
    return record if _printable(record.get("project")) else None


def read_scope(session_id: str) -> str | None:
    """The project the daemon last wrote to for this session, or None: absent,
    unreadable, malformed and expired alike, as in `_read_marker`."""
    record = _read_scope_record(session_id)
    return record["project"] if record is not None else None


def clear_scope(session_id: str, ref: str) -> bool:
    """Forget the stored project when `ref` (a slug or an id) names it: the daemon
    deleted it, and a label naming a project in the trash is the lie this file
    exists to stop. True when it was cleared."""
    record = _read_scope_record(session_id)
    project_id = record.get("project_id") if record is not None else None
    if record is None or not (ref == record.get("project")
                              or isinstance(project_id, str) and ref.lower() == project_id.lower()):
        return False
    try:
        os.unlink(scope_path(session_id))
        return True
    except OSError:
        return False


def home_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + HOME_SUFFIX)


def write_run_home(session_id: str, *, project: str, project_id: str, experiment: "str | None" = None,
                   experiment_id: "str | None" = None, base_url: str, customer_id: "str | None") -> bool:
    """Record where this session's runs go (`probe session home set`): the project, and the
    experiment when one is named, by slug and id, with the server and team they were
    resolved on. True when it landed. No expiry: the daemon replaces it when the work moves."""
    names_ok = _printable(project) and (experiment is None or _printable(experiment))
    ids_ok = (isinstance(project_id, str) and bool(project_id) and (experiment is None) == (experiment_id is None)
              and (experiment_id is None or isinstance(experiment_id, str) and bool(experiment_id)))
    if not valid_session_id(session_id) or not names_ok or not ids_ok or not isinstance(base_url, str):
        return False
    record = {"project": project, "project_id": project_id, "experiment": experiment,
              "experiment_id": experiment_id, "base_url": base_url, "customer_id": customer_id,
              "decided_at": time.time()}
    return _publish_atomically(home_path(session_id), json.dumps(record) + "\n")


def read_run_home(session_id: str) -> "dict | None":
    """This session's run home as `write_run_home` stored it, or None: absent,
    unreadable and malformed alike."""
    if not valid_session_id(session_id):
        return None
    try:
        with open(home_path(session_id), encoding="utf-8") as handle:
            record = json.load(handle)
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or not _printable(record.get("project")):
        return None
    experiment, experiment_id = record.get("experiment"), record.get("experiment_id")
    if not record.get("project_id") or not isinstance(record.get("project_id"), str):
        return None
    if not isinstance(record.get("base_url"), str):
        return None
    if (experiment, experiment_id) != (None, None) and not (_printable(experiment) and experiment_id
                                                            and isinstance(experiment_id, str)):
        return None
    return record


def clear_run_home(session_id: str) -> bool:
    """Forget this session's run home. True when there was one to forget."""
    if not valid_session_id(session_id):
        return False
    try:
        os.unlink(home_path(session_id))
        return True
    except OSError:
        return False


def get_session_workspace_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + WORKSPACE_SUFFIX)


def write_session_workspace(session_id: str, *, workspace_id: str, base_url: str,
                            customer_id: "str | None") -> bool:
    """Record the workspace a project this session creates is filed in, with the server and team
    it belongs to. True when it landed. It outranks this computer's own pin (D68)."""
    if not valid_session_id(session_id) or not _printable(workspace_id) or not isinstance(base_url, str):
        return False
    record = {"workspace_id": workspace_id, "base_url": base_url, "customer_id": customer_id,
              "decided_at": time.time()}
    return _publish_atomically(get_session_workspace_path(session_id), json.dumps(record) + "\n")


def read_session_workspace(session_id: str) -> "dict | None":
    """This session's workspace as `write_session_workspace` stored it, or None: absent,
    unreadable and malformed alike."""
    if not valid_session_id(session_id):
        return None
    try:
        with open(get_session_workspace_path(session_id), encoding="utf-8") as handle:
            record = json.load(handle)
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or not _printable(record.get("workspace_id")):
        return None
    return record if isinstance(record.get("base_url"), str) else None


def clear_session_workspace(session_id: str) -> bool:
    """Forget this session's workspace. True when there was one to forget."""
    if not valid_session_id(session_id):
        return False
    try:
        os.unlink(get_session_workspace_path(session_id))
        return True
    except OSError:
        return False


def write(session_id: str, state: dict) -> bool:
    """Replace this session's marker. True when it landed.

    Atomic, and stamped here rather than by the caller so `updated_at` always
    means "when this file was written" and cannot be back-dated by a stale
    refresher losing a race with a newer one.
    """
    if not valid_session_id(session_id):
        return False
    record = dict(state)
    record["updated_at"] = time.time()
    path = marker_path(session_id)
    tmp = path.parent / (path.name + "." + str(os.getpid()) + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(record, handle)
        os.replace(tmp, path)
        return True
    except (OSError, ValueError, TypeError):
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return False


def from_session_work(payload: dict) -> dict:
    """The marker shape, built from a ``GET /v1/sessions/{id}/work`` body.

    Keeps only what the segment can render: the project this session touched
    and whether a run of its is live. The response is another service's schema
    and is treated as untrusted — every field is checked, and a shape we do not
    recognise degrades to "tracked nothing" rather than raising on a render path.

    WHICH PROJECT, when a session touched several: the LAST one. That is only a
    GUESS: the list is ordered by each link's first sighting, which is the
    SESSION's for every project it touched, so it ties and falls to uuid order.
    `read` puts the daemon's own answer (`<session>.scope`) in its place when
    there is one.
    """
    project = None
    titles: dict = {}
    projects = payload.get("projects")
    if isinstance(projects, list):
        for row in projects:
            if not isinstance(row, dict):
                continue
            slug = row.get("slug") or row.get("name")
            if isinstance(slug, str) and slug:
                project = slug
                name = row.get("name")
                titles.pop(slug, None)  # re-insert: the dict keeps response order, newest last
                if is_printable_title(name):
                    titles[slug] = name
    titles = dict(list(titles.items())[-MAX_TITLE_ROWS:])

    # The work read carries no run STATUS, only identity. The ids are kept so the
    # renderer can intersect them with the run locks this box holds — the local
    # fast path in `is_live`, which is what makes "running" mean THIS session's
    # run rather than any run on the machine.
    run_ids = []
    runs = payload.get("runs")
    if isinstance(runs, list):
        for row in runs:
            if not isinstance(row, dict):
                continue
            entity_id = row.get("entity_id")
            if isinstance(entity_id, str) and entity_id:
                run_ids.append(entity_id)

    return {"project": project, "run_ids": run_ids, "project_titles": titles, "titles_at": time.time()}


def from_active_runs(payload: object) -> list[str]:
    """Active run ids, from a ``GET /v1/runs?...&active=true`` body.

    The server's own liveness verdict: stored status is `running` AND the newest
    substantive update or heartbeat is inside the liveness window. Machine-
    independent, which is the whole reason it is worth a second request — a run
    executing on a cluster holds its lock on THAT box and is invisible to the
    local scan.
    """
    if not isinstance(payload, list):
        return []
    ids = []
    for row in payload:
        if not isinstance(row, dict):
            continue
        run_id = row.get("id")
        if isinstance(run_id, str) and run_id:
            ids.append(run_id)
    return ids


