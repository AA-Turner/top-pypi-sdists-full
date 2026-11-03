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
Two copies exist on purpose and must stay byte-identical:

    src/probe/sdk/session_marker.py                     (canonical — edit here)
    plugins/probe-research/hooks/_session_marker.py     (vendored — never edit)

`make sync-session-marker` refreshes the copy, and tests/test_session_marker_parity.py
fails CI whenever the two differ.

FAIL-SOFT THROUGHOUT. Nothing here may raise into a caller: the writer runs beside
a research write that must survive a full disk, and the reader runs on a render
path where an exception is a broken prompt.
"""

from __future__ import annotations

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
#: A bound on a project name this file stores or shows. Server slugs are
#: free-form TEXT; the segment elides a long one anyway, so this only keeps a
#: pathological value off the render path.
MAX_LABEL_CHARS = 1024
#: Unicode categories a label may not hold: controls (an escape sequence),
#: format characters (bidi overrides, zero-width), line and paragraph
#: separators, surrogates and private use. Not `Cn` (unassigned): the hook's
#: python can be older than the daemon's, and a newer emoji is unassigned there.
_UNPRINTABLE = frozenset({"Cc", "Cf", "Zl", "Zp", "Cs", "Co"})

#: The ONE way any message sends a person to set up, sign in, update or repair
#: this device: setup is wizard-only (Richard 2026-09-29), so no user-facing text
#: names a `probe <setup command>`. Lives here because this file is the one every
#: surface can reach (the SDK imports it, the plugin hooks vendor it); the tap and
#: the pi extension carry copies that tests/test_wizard_hint_sync.py pins to it.
WIZARD_HINT = "run the Probe wizard: probe wizard or npx probe-research"

_ELLIPSIS = "…"  # …
#: ONE glyph for both states, and it is FILLED in both. A hollow ring is faint
#: at terminal font sizes and reads as a rendering artefact rather than a mark.
#: Nothing is lost by using the same glyph twice: the state is carried by the
#: WORD ("untracked" / "tracked →"), which is why the dot could be spared the
#: job in the first place. Colour distinguishes them for a quick glance; the
#: word distinguishes them when colour is off, absent, or unseeable.
_DOT = "●"  # ●
_ARROW = "→"  # →
_SEPARATOR = "·"  # ·

_INDENT = "  "
_GLYPH_WIDTH = 2  # the dot plus its trailing space

#: The state is spelled OUT, not encoded in the glyph. `● folding` requires the
#: reader to already know that a filled dot means tracked; `tracked → folding`
#: does not, and a status line is read by people who did not install it.
_LABEL_TRACKED = "tracking " + _ARROW + " "
_LABEL_TRACKING_BARE = "tracking"
#: The `daemon` state's words: `on (daemon)`, the switch's `on` with who records
#: in parentheses (Richard 2026-09-29; `DAEMON_STATE_DISPLAY`).
_LABEL_DAEMON = "on (daemon) " + _ARROW + " "
_LABEL_DAEMON_BARE = "on (daemon)"
#: Still `on (daemon)`, but the daemon holds no live lease (no key, out of
#: budget, gateway down, not started yet). The mode stays on screen; `degraded`
#: says the daemon is not the one doing it.
_LABEL_DAEMON_DEGRADED = "on (daemon degraded) " + _ARROW + " "
_LABEL_DAEMON_DEGRADED_BARE = "on (daemon degraded)"
#: The researcher set Probe inline (`/probe inline`, `is_inline`, Richard 2026-10-06).
_LABEL_INLINE = "on (inline) " + _ARROW + " "
_LABEL_INLINE_BARE = "on (inline)"
#: Kept for readers that still resolve the switch to a BOOLEAN. `render` only
#: reaches it when no three-valued state was passed in, which is the shape a
#: pre-three-state caller has. New callers pass `session_state` and get one of
#: the two labels below instead.
_LABEL_NOT_TRACKING = "not tracking"

#: The two non-recording states are spelled by `_STATE_SEGMENT`, down in the
#: Rendering section beside the colour each one is painted. Both words are
#: SHORTER than `not tracking` (9 and 3 against 12), so MAX_SEGMENT_CHARS is
#: untouched.

#: A middle dot, NOT a second arrow. `tracked → folding ▸ running` puts two
#: arrow-shaped glyphs in one short segment, and the eye reads them as a
#: sequence of three things rather than as a name with a state hung off it.
_ACCENT_TEXT = " " + _SEPARATOR + " running"

#: The third state: tracking is ON and the work IS landing, but no
#: transcript-capture daemon is live for this conversation.
#:
#: A HALF-FILLED dot, not a hollow one. Hollow is faint at terminal font sizes
#: (see `_DOT`), and the reader must be able to tell this from `not tracking` at
#: a glance; the WORD carries the meaning for anyone whose terminal renders both
#: dots the same. The dot stays GREEN when painted, because green means
#: "landing" and the work still is — yellow already belongs to `not tracking`,
#: and reusing it would make a degraded session look like a switched-off one.
_DOT_DEGRADED = "◐"  # ◐
#: SPELLED OUT. An earlier `no capture:` named the mechanism, and read beside
#: `tracking` it was taken for its opposite -- "nothing is being recorded" --
#: when the work IS landing and only the conversation is not. Naming the
#: transcript says exactly which half is missing. The columns this costs are
#: paid by `MAX_SEGMENT_CHARS` below, never by the project name.
_LABEL_NO_CAPTURE = " " + _SEPARATOR + " not capturing session transcript: "

#: The capture reason for transcripts turned off on purpose (`capture_state.TURNED_OFF_REASON`):
#: a choice, so it renders as a plain note with the full dot, never as a fault.
_CHOSEN_OFF_REASON = "turned off"
_LABEL_TRANSCRIPTS_OFF = " " + _SEPARATOR + " transcripts off"

#: The longest word in `probe.cli.capture_state.REASONS` (`interpreter too old`).
#: A literal, because nothing of ours may be imported on the render path;
#: `test_every_reason_in_the_closed_vocabulary_renders_whole_on_the_bare_line`
#: pins it against the vocabulary, so a longer reason added there fails a test
#: here rather than rendering as `interp…` on somebody's status line.
_LONGEST_REASON_CHARS = 19

#: Below this many columns an elided project name identifies nothing — `a-rea…`
#: is not a name, it is noise wearing one. When the reason is long enough to
#: push the name under this floor, the name is dropped ENTIRELY and the segment
#: falls back to `_LABEL_TRACKING_BARE`, which this file already renders for
#: "tracking is on, nothing filed yet".
_MIN_SLUG_CHARS_DEGRADED = 8

#: Hard ceiling on the rendered segment, leading indent included, counted in
#: VISIBLE characters. The cap exists because the status line must not WRAP: a
#: wrapped line reflows every other segment sharing it, which is the one failure
#: that makes neighbouring output less readable rather than merely longer.
#:
#: DERIVED FROM THE WIDEST LINE THAT MUST RENDER WHOLE: the degraded bare form
#: carrying the longest reason in the closed vocabulary,
#: `  ◐ tracking · not capturing session transcript: interpreter too old` (68).
#: The reason is the one actionable thing on that line and is on screen nowhere
#: else, so it is the last thing cut (`_no_capture_clause`); a ceiling it cannot
#: fit under would elide the diagnosis on every degraded render.
#:
#: The previous ceiling, 51, was measured against the HEALTHY line instead: the
#: smallest number at which a 26-character name budget survived, 26 being what
#: this lab's project names need (median 18, longest 29). The capture suffix was
#: 15 columns then and fit beneath it; spelling the suffix out made the degraded
#: line the binding one. The name budget grows with the ceiling (see
#: `MAX_SLUG_CHARS`), so nothing that fit whole before fits worse now.
#:
#: THE LABEL IS PAID FOR BY THE CEILING, NEVER BY THE NAME. Spelling out
#: "tracking → " costs eleven columns; taking them from the name would elide the
#: project the segment exists to identify. When a label changes length, this
#: number moves with it by construction.
#: `test_this_labs_project_names_mostly_fit_whole` pins the name budget.
#:
#: The bare label is the WIDER of the two that can carry the capture suffix:
#: `on (daemon)` does too (see `_recording_labels`), and it is three columns
#: longer than `tracking`.
MAX_SEGMENT_CHARS = (
    len(_INDENT)
    + _GLYPH_WIDTH
    + max(len(_LABEL_TRACKING_BARE), len(_LABEL_DAEMON_BARE))
    + len(_LABEL_NO_CAPTURE)
    + _LONGEST_REASON_CHARS
)

#: What the name may occupy. DERIVED, and derived against the LIVE width even
#: when idle, so the name keeps one budget in both states: a name that shrank the
#: moment a run started -- and grew back when it ended -- would read as the status
#: line glitching rather than as the run changing.
#:
#: Wider than any name this lab has (43 against a longest of 29), so a healthy
#: line reaches the ceiling only in theory; the columns the ceiling grew by are
#: spent on the reason, and only when there is one.
MAX_SLUG_CHARS = (
    MAX_SEGMENT_CHARS - len(_INDENT) - _GLYPH_WIDTH - len(_LABEL_TRACKED) - len(_ACCENT_TEXT)
)

# Basic SGR codes, never 256-colour or truecolour: the status line is rendered
# inside the user's terminal theme, and a hardcoded hex that looks right on one
# background is unreadable on the other. These resolve against whatever palette
# they already chose. Claude Code additionally dims the whole line, so treat
# these as a hint of hue rather than as emphasis.
#
# Three, and each is a state someone can name: landing (green), not landing but
# still reading (yellow), and switched off entirely (red). A fourth colour would
# be a state nobody defined.
#
# RED IS THE ONE THAT STOPS A READER, and `off` is the one state that earns it:
# it is the only position of the switch under which an agent cannot find prior
# work AND cannot know what it missed. `read-only` still answers questions, so
# it keeps the yellow that means "look, but nothing is on fire".
_DIM = "\033[2m"
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
    scope = read_scope(session_id)
    if scope is not None:
        return {**state, "project": scope}
    if state.get("project") is not None and not _printable(state.get("project")):
        return {**state, "project": None}
    return state


def scope_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + SCOPE_SUFFIX)


def _printable(value: object) -> bool:
    """A project name the segment can print: one bounded line, nothing a terminal
    or a bidi renderer would act on. It comes from the server, where slugs are
    free-form, so it is checked, not trusted."""
    return (isinstance(value, str) and 0 < len(value) <= MAX_LABEL_CHARS
            and all(unicodedata.category(ch) not in _UNPRINTABLE for ch in value))


def write_scope(session_id: str, project: str, project_id: str | None = None) -> bool:
    """Record the project the daemon's latest write landed in (its slug, and its
    id so a delete by id can clear it). True when it landed.

    A file of its own, not a key in the marker: the refresh hook REPLACES the
    marker every few seconds from the server's answer, and a second writer's key
    would be gone at the next refresh.
    """
    if not valid_session_id(session_id) or not _printable(project):
        return False
    record = {"project": project, "project_id": project_id, "updated_at": time.time()}
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
    projects = payload.get("projects")
    if isinstance(projects, list):
        for row in projects:
            if not isinstance(row, dict):
                continue
            slug = row.get("slug") or row.get("name")
            if isinstance(slug, str) and slug:
                project = slug

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

    return {"project": project, "run_ids": run_ids}


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


