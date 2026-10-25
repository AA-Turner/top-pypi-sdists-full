"""Probe off means the session is not captured (the owner's decision, 2026-10-24).

The session's switch (`probe session state`, `/probe`) is stored in
`<state>/sessions/<sid>.state`; a session nobody has decided about yet takes
the machine's default (`defaults.session_state`, `PROBE_SESSION_STATE`). While
it reads `off`, the Probe service records nothing of the session's transcript
written in that time, and moving it back resumes capture FROM THE MOVE: what
was written while it was off is never sent later (the `probe` skill: "Moving
the switch never deletes anything and never backfills anything"). Before this
the switch gated only the daemon and the agent's Probe calls, and the tap
uploaded the whole transcript of an `off` session.

The Probe service enforces it for every session it records, with the tap it
loaded (the service always runs the newest installed CLI, so a session already
open when this lands is covered from the service's next start, with no restart
of the agent). From tap 0.10.19 the tap gates its own drains in every process
(`tap/capture_gate.py`, `NATIVE`): with such a tap loaded this service installs
none of the wraps below; it adds its in-memory gaps to the tap's (`host`) and
settles through the tap's own `settling`. Taps 0.10.0-0.10.18 are wrapped:

    the gaps        a session's off stretches, as transcript byte ranges
                    `[from, to)`: `from` is the transcript's complete-line size
                    when the switch was seen `off`, `to` its size when it was
                    seen on again (None while still off; at the session's end
                    an open gap runs to the end). A session first seen already
                    off gets `from` 0 (when it turned off is not known). Kept
                    in the session's `recorders.json` record (GAPS_KEY) and in
                    its GAP FILE (below), so neither a restart, nor the session
                    leaving `recorders.json`, nor a pruned `.state` forgets one.
                    The service looks at a running session's switch every
                    POLL_S (a stat of its files; a read only when one changed),
                    a held one's every HELD_POLL_S, and at once when the CLI or
                    the typed `/probe` hook that moved it asks `session.recording`
    held            while a gap is open the session's own recorder does not run
                    (its loop leaves at its next check: `controls.pause`) and
                    nothing of it is staged
    every drain     a recorder stages every session in its journal (the tap's
                    shared drain) and adopts transcripts it has a log for and
                    no journal row (its gap sweep). In this process neither
                    touches a session that has a gap not yet settled (in memory
                    or in its gap file), or whose switch reads `off`
                    (`install`): `Journal.stage` gives such a session only the
                    batch it staged before the switch moved (it may still
                    flush; nothing is deleted), and `reconcile.find_gaps`
                    leaves it out
    settling        once the switch is on again (or the session ends) the
                    session's own recorder thread stages and delivers it from
                    its cursor with every line that STARTS inside a gap read
                    past and sent as nothing (`settle`): the tap's own batch,
                    with no event for those lines, so the server's cursor moves
                    past them and no recorder can ever send them. Lines outside
                    the gaps go as they always did. A session that ends while
                    off is settled to its end and finalized (retried by later
                    services while the server cannot be reached; dropped, its
                    gap file kept, when refused for good: no login here, or
                    the Probe gateway's own 401/403/404/422, REFUSED);
                    one that never uploaded anything sends nothing at all, and
                    its gap file stays, so a later capture of it skips the
                    stretch too

THE GAP FILE (for every reader, the tap's own included): `<state>/sessions/
<sid>.gaps`, beside the session's `.state`, 0600, replaced whole (written to a
temporary file, flushed to disk, renamed) under the session's lock file
(`<sid>.gaps.lock`, `locked`), which every writer takes for its whole
read-modify-write: this service, and from tap 0.10.19 a `tap watch` recording
its own session's off stretches (the two coexist for a moment at a hand-over).
What another writer put there since this service last wrote or read the file
is merged into its record before it writes (`RecorderHost._flush_gap_file`),
never written over:

    {"v": 1, "sid": "<sid>", "transcript": "<absolute path>" | null,
     "gaps": [[from, to | null], ...], "updated_at": <epoch seconds>}

A transcript line whose start byte offset lies in a gap (`from <= offset < to`,
`to` null: to the end) was written while Probe was off and is never to be
uploaded; a reader that cannot tell where a line starts uploads nothing of the
session, and neither does one that cannot read the file (truncated, another
version, or an error reading it now): it covers the whole session
(`read_gap_file`). A recorder never takes such a failure into the session's
record: it holds the session and reads the file again at its next look. No file: no gaps. The
service removes it once its cursor on the server is past every gap; for a
session this process records, its record decides, not the file (`live`).
`session_marker.prune` keeps the gap file and the `.state` while the file
holds gaps and its transcript still exists (one naming no transcript, or not
readable: 90 days from its last write), and removes it once that transcript
is gone. The service writes it off its loop and off the lock every session's
gate takes (`RecorderHost._flush_gap_file`).

How a skipped line is skipped (a tap from 0.10.19 does it in its own `stage`,
on the thread `settle` marks with its `settling`; before it): `settle` runs on
its own thread with the session in a thread-local (`_LOCAL.catchup`), and the
loaded tap's `_sanitizer` and
`_title_reader` are wrapped once (`install`) so that, on that thread only, a
line whose start offset (`stage`'s own `end`, read from its frame) lies in one
of the session's gaps (as they are at that moment: a gap opened during the
settle counts) reads as one the sanitizer dropped: no event, no title. Every
other thread gets the tap's own functions. A tap whose `stage` keeps no `end`
(none since 0.10.0, when the service started hosting) has every line of the
settling pass dropped: a few lines written while it ran may be lost, never sent.

What this does not reach (tap 0.10.19 reads the switch and the gap file in
its own drains and closes it for every process running that tap or newer):
    - a `tap watch` process of a tap before 0.10.19 (outside this process)
      stages every session of its journal, off ones included, and its own
      session until it hands that to the service (`tap/handback.py`, every
      minute; plan C0 for older taps), until it is replaced
    - a Claude Code resume that copies earlier history into a new session id
      (not checked)
Accepted here:
    - with a tap before 0.10.19, a line over the tap's MAX_SOURCE_LINE inside
      a gap is still sent as its size-only placeholder (`[transcript line not
      sent: N bytes]`); 0.10.19 skips it (outside a CLI 0.307-0.310 service,
      which wraps every tap and stands the tap's own gate down)
    - a compaction summary written after the flip back on (Claude Code's
      `isCompactSummary`, Codex `compacted`, pi's compaction entry) can carry
      what was said while off: it is a line written while on
    - the flip itself: lines written between the move and the service seeing
      it (none when the CLI or the hook asked it; at most POLL_S, or
      HELD_POLL_S for a held session, when nothing did) fall on the off side
      when it moved off (they may go) and on the on side when it moved back
      (they are skipped: lost, never leaked). Moved on while no service runs
      and nothing asked: the stretch until a service starts (the keeper,
      within a minute) is skipped
    - a crash or power loss in the moment a gap is written: the gap file is
      flushed to disk before it replaces the old one, `recorders.json` is not
    - a Codex session switched on while its sessions folder is not there (or
      cannot be looked in) stays held until it can be: the lines its rollout
      gets before the next look (POLL_S) are skipped

Stdlib only at import (the service's start path); the tap is passed in.
"""

from __future__ import annotations

import contextlib
import functools
import json
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable

#: The switch's stored word for off (`session_marker.STATE_OFF`).
OFF = "off"
#: How often the service looks at a running session's switch: a stat of its
#: files, a read only when one changed (`read_switch`).
POLL_S = 0.2
#: How often a held session looks again by itself; the CLI and the hook that
#: moved the switch wake it at once (`session.recording`).
HELD_POLL_S = 1.0
#: The session's gaps in its `recorders.json` record (`RecorderHost._valid` keeps it).
GAPS_KEY = "capture_gaps"
#: The gap file beside a session's state (see the module docstring).
GAP_FILE_SUFFIX = ".gaps"
GAP_FILE_VERSION = 1
#: At most this many gaps per session are kept: past it the oldest closed ones
#: merge (a switch flipped thousands of times must not grow the record forever).
MAX_GAPS = 64
#: Batches one `settle` call stages at most (each reads at most 4 MiB of the
#: transcript, the tap's own bound): past it, the next call goes on.
MAX_SETTLE_BATCHES = 256
#: Switch and gap-file readings kept (`read_switch`, `read_gap_file`).
_CACHE_MAX = 4096

#: `settle`'s answers.
DONE = "done"  # the server's cursor is past every gap (or there was nothing to cover)
KEPT = "kept"  # nothing was or will be sent now: the gaps stay recorded
RETRY = "retry"  # try again later (no network, any other refusal, the claim held elsewhere, superseded)
REFUSED = "refused"  # refused for good: no login here, or the Probe gateway's own 401/403/404/422
DELETED = "deleted"  # the server deleted the session at its team's request
#: What the Probe gateway answers when it refuses a session for good: the
#: device is not (or no longer) allowed to send it (`_refused_for_good`).
REFUSED_STATUSES = (401, 403, 404, 422)
#: What a gap file that is there and does not read covers: the whole session
#: (a reader that cannot tell where a line starts uploads nothing of it).
WHOLE = [[0, None]]

_LOCAL = threading.local()
#: Sessions with a gap not yet settled, for the drains' wrappers on every
#: thread of this process: `{sid: gaps}`.
_UNSETTLED: dict[str, list] = {}
_LOCK = threading.Lock()
#: Sessions this process records now: for them the in-memory gaps
#: (`_UNSETTLED`) decide, never a gap file a failed removal left behind.
_LIVE: set[str] = set()
_CACHE_LOCK = threading.Lock()
_SWITCHES: dict[tuple, tuple] = {}
_GAP_FILES: dict[str, tuple] = {}


# -- where a session's files are ----------------------------------------------------


def _home(env) -> Path:
    home = env.get("HOME")
    return Path(home) if home else Path(os.path.expanduser("~"))


def sessions_dir_for(env, state_dir: object = None) -> Path:
    """`session_marker.sessions_dir()` for `env`: `state_dir` when the
    registrant named it (`<XDG_STATE_HOME or ~/.local/state>/probe`)."""
    if isinstance(state_dir, str) and os.path.isabs(state_dir):
        return Path(state_dir) / "sessions"
    xdg = env.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else _home(env) / ".local" / "state"
    return base / "probe" / "sessions"


def config_path_for(env) -> Path:
    """`session_marker.config_path()` for `env`."""
    override = env.get("PROBE_CONFIG_PATH")
    if override:
        return Path(override)
    base = env.get("XDG_CONFIG_HOME")
    return (Path(base) if base else _home(env) / ".config") / "probe" / "config.json"


def _stat(path: Path) -> tuple | None:
    try:
        st = os.stat(path)
    except OSError:
        return None
    return (st.st_mtime_ns, st.st_size, st.st_ino)


# -- the switch ---------------------------------------------------------------


def _ladder(sid: str, sessions: Path, env, config: Path) -> str:
    """`session_marker.session_state` (with its migration of the legacy
    files), else `session_marker.resolve_state_default`, on these paths and
    this environment (`test_capture_gate.py` holds the two equal)."""
    from probe.sdk import session_marker as marker

    try:
        raw = (sessions / f"{sid}.state").read_text(encoding="utf-8").strip().lower()
        if raw in marker.STATES:
            return raw
    except OSError:
        pass
    try:
        legacy = (sessions / f"{sid}.tracking").read_text(encoding="utf-8").strip().lower()
    except OSError:
        legacy = None
    if legacy == "on":
        return marker.STATE_FULL
    if legacy == "off" or (sessions / f"{sid}.off").is_file():
        return marker.STATE_READ_ONLY
    explicit = marker.normalize_state(env.get("PROBE_SESSION_STATE"))
    if explicit is not None:
        return explicit
    legacy_env = marker._legacy_state_from_tracking(env.get("PROBE_SESSION_TRACKING"))  # noqa: SLF001
    if legacy_env is not None:
        return legacy_env
    try:
        data = json.loads(config.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    stored = marker._stored_state(data.get(marker.DEFAULTS_KEY)) if isinstance(data, dict) else None  # noqa: SLF001
    return marker.DEFAULT_STATE if stored is None else stored


def explicitly_off(sid: str, sessions: Path) -> bool:
    """Does the session's own `.state` say `off` (never a machine default or
    an environment variable: what `probe import` goes by)?"""
    try:
        return (sessions / f"{sid}.state").read_text(encoding="utf-8").strip().lower() == OFF
    except OSError:
        return False


def read_switch(sid: object, sessions: Path, env) -> str | None:
    """The session's switch in `env`, its files in `sessions`: read again only
    when one of them, or the machine's config, changed (a stat each), or an
    override in `env` did. None when it cannot be read (never `off` on a
    guess)."""
    try:
        from probe.sdk import session_marker as marker

        if not marker.valid_session_id(sid):
            return None
        config = config_path_for(env)
        signature = (
            _stat(sessions / f"{sid}.state"), _stat(sessions / f"{sid}.tracking"), _stat(sessions / f"{sid}.off"),
            _stat(config), env.get("PROBE_SESSION_STATE"), env.get("PROBE_SESSION_TRACKING"),
        )
        key = (str(sessions), sid, str(config))
        with _CACHE_LOCK:
            cached = _SWITCHES.get(key)
        if cached is not None and cached[0] == signature:
            return cached[1]
        state = _ladder(str(sid), sessions, env, config)
        with _CACHE_LOCK:
            if len(_SWITCHES) >= _CACHE_MAX:
                _SWITCHES.clear()
            _SWITCHES[key] = (signature, state)
        return state
    except Exception:  # noqa: BLE001 -- unreadable: the session records as before
        return None


def switch(params: dict) -> str | None:
    """The session's switch as its registrant keeps it: its state folder
    (`state_dir`) and its own environment (`env`)."""
    env = params.get("env") if isinstance(params.get("env"), dict) else {}
    return read_switch(params.get("sid"), sessions_dir_for(env, params.get("state_dir")), env)


def is_off(params: dict) -> bool:
    return switch(params) == OFF


def _read_switch(sid: object) -> str | None:
    """`sid`'s switch in this thread's environment (a recorder's: its session's)."""
    return read_switch(sid, sessions_dir_for(os.environ), os.environ)


# -- gaps -----------------------------------------------------------------------


def _valid_gaps(raw: object) -> list[list]:
    out: list[list] = []
    if not isinstance(raw, list):
        return out
    for gap in raw[-MAX_GAPS:]:
        if not (isinstance(gap, (list, tuple)) and len(gap) == 2):
            continue
        start, end = gap
        if not isinstance(start, int) or isinstance(start, bool) or start < 0:
            continue
        if end is not None and (not isinstance(end, int) or isinstance(end, bool) or end < start):
            continue
        out.append([start, end])
    return out


def gaps_of(params: dict) -> list[list]:
    """A session's gaps as `[[from, to|None], ...]`, whatever its record holds."""
    return _valid_gaps(params.get(GAPS_KEY))


def normalized(gaps: list) -> list[list]:
    """Gaps in order of where they start, each once; an open gap last (one
    covers everything after its start, so a gap starting past it adds nothing)."""
    unique = {(g[0], g[1]) for g in _valid_gaps(gaps)}
    out: list[list] = []
    for start, end in sorted(unique, key=lambda g: (g[0], float("inf") if g[1] is None else g[1])):
        if out and out[-1][1] is None:
            break
        out.append([start, end])
    return out


def is_open(gaps: list) -> bool:
    return bool(gaps) and gaps[-1][1] is None


def opened(gaps: list, mark: int) -> list:
    """`gaps` with one open from `mark` (unchanged when one is open already)."""
    if is_open(gaps):
        return gaps
    out = [list(g) for g in gaps] + [[mark, None]]
    while len(out) > MAX_GAPS:
        # Merge the two oldest: what lay between them is dropped too, never sent.
        first, second = out.pop(0), out.pop(0)
        out.insert(0, [first[0], second[1]])
    return out


def closed(gaps: list, mark: int) -> list:
    """`gaps` with the open one closed at `mark` (never before its own start)."""
    if not is_open(gaps):
        return gaps
    out = [list(g) for g in gaps]
    out[-1][1] = max(out[-1][0], mark)
    return out


def in_gap(gaps: list, offset: int) -> bool:
    return any(start <= offset and (end is None or offset < end) for start, end in gaps)


def unsettled(sid: str, gaps: list) -> None:
    """Publish `sid`'s gaps to the drains' wrappers. Never clears them: only a
    settle does (`settled`), so a first look at a session that reads on does
    not lift what an earlier recording of it left unsettled."""
    if gaps:
        with _LOCK:
            _UNSETTLED[sid] = [list(g) for g in gaps]


def settled(sid: str) -> None:
    with _LOCK:
        _UNSETTLED.pop(sid, None)


def live(sid: str, recorded: bool) -> None:
    """This process records `sid` now (or no longer)."""
    with _LOCK:
        if recorded:
            _LIVE.add(sid)
        else:
            _LIVE.discard(sid)


def _live_gaps(sid: str, snapshot: list) -> list:
    with _LOCK:
        current = list(_UNSETTLED.get(sid) or [])
    return snapshot + current


def blocked(sid: object) -> bool:
    """May no drain of this process stage `sid` now? True while it has a gap
    not yet settled (here, or in its gap file), but not on the thread
    settling it, or while its switch reads `off`, in the calling thread's
    environment."""
    if not isinstance(sid, str):
        return False
    context = getattr(_LOCAL, "catchup", None)
    if context is not None and context[0] == sid:
        return False
    with _LOCK:
        if sid in _UNSETTLED:
            return True
        recorded_here = sid in _LIVE
    if not recorded_here and read_gap_file(sessions_dir_for(os.environ), sid):
        return True
    return _read_switch(sid) == OFF


# -- the gap file --------------------------------------------------------------------


def gap_file(sessions: Path, sid: str) -> Path:
    return sessions / f"{sid}{GAP_FILE_SUFFIX}"


def read_gap_file(sessions: Path, sid: str) -> list[list]:
    """The gaps a session's gap file holds (none without one); read again only
    when the file changed. FAILS CLOSED: a file that is there and does not
    read (truncated, not JSON, another version, a gap in it that does not
    read), or that cannot be read now (an OSError), covers the whole session
    (WHOLE)."""
    gaps = read_gap_file_raw(sessions, sid)
    return [list(g) for g in WHOLE] if gaps is None else gaps


def read_gap_file_raw(sessions: Path, sid: str) -> list[list] | None:
    """As `read_gap_file`, but None when the file could not be read NOW (an
    OSError other than its absence: too many open files, permission denied, a
    Windows sharing violation). Only what a read said is cached (by the file's
    signature); a failed read is tried again at the next call. A recorder
    never merges such a failure into the session's record (`RecorderHost._gate`)."""
    path = gap_file(sessions, sid)
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return []
    except OSError:
        return None
    signature = (st.st_mtime_ns, st.st_size, st.st_ino)
    with _CACHE_LOCK:
        cached = _GAP_FILES.get(str(path))
    if cached is not None and cached[0] == signature:
        return [list(g) for g in cached[1]]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not (isinstance(data, dict) and data.get("v") == GAP_FILE_VERSION and isinstance(data.get("gaps"), list)):
            raise ValueError("not a gap file this reader knows")
        if len(_valid_gaps(data["gaps"])) != len(data["gaps"]):
            raise ValueError("a gap that does not read")
        gaps = normalized(data["gaps"])
    except FileNotFoundError:
        return []
    except ValueError:  # UnicodeDecodeError included: what the file says, so cached
        gaps = [list(g) for g in WHOLE]
    except OSError:
        return None
    with _CACHE_LOCK:
        if len(_GAP_FILES) >= _CACHE_MAX:
            _GAP_FILES.clear()
        _GAP_FILES[str(path)] = (signature, gaps)
    return [list(g) for g in gaps]


def file_signature(sessions: Path, sid: str) -> tuple | None:
    """The gap file's `(mtime_ns, size, inode)`, None without one: every write
    replaces it (a new inode), so a signature that changed means a write."""
    return _stat(gap_file(sessions, sid))


def locked(sessions: Path, sid: str):
    """The session's gap-file lock (`<sid>.gaps.lock`), every writer's: the
    tap's own protocol (`probe.tap_core.capture_gate.locked`, the copy of
    `tap/capture_gate.py`). OSError when it cannot be had now."""
    from probe.tap_core import capture_gate as tap_gate

    return tap_gate.locked(sid, sessions)


def write_gap_file(sessions: Path, sid: str, gaps: list, transcript_path: object = None) -> bool:
    """Replace the session's gap file with `gaps` (none: remove it). Written to
    a temporary file of this user's alone, flushed to disk, then renamed over
    the old one. False when it could not be written."""
    path = gap_file(sessions, sid)
    gaps = normalized(gaps)
    if not gaps:
        try:
            path.unlink()
        except FileNotFoundError:
            return True
        except OSError:
            return False
        return True
    record = {
        "v": GAP_FILE_VERSION, "sid": sid,
        "transcript": str(transcript_path) if isinstance(transcript_path, (str, Path)) and str(transcript_path) else None,
        "gaps": gaps, "updated_at": time.time(),
    }
    tmp = path.with_name(f".{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
    try:
        sessions.mkdir(parents=True, exist_ok=True)
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(record, handle, separators=(",", ":"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        return True
    except OSError:
        return False
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


# -- the transcript ---------------------------------------------------------------


def mark_now(tap: Any, path: Path | None) -> int | None:
    """Where a gap starts or ends now: the transcript's size up to its last
    complete line (a line still being written belongs to after the move). 0
    when there is no transcript yet: everything it will hold is after. None
    when it is there and cannot be read: the caller must not close a gap on
    that (an opening falls back to 0)."""
    if path is None:
        return 0
    try:
        size = path.stat().st_size
        return int(tap.session_journal.complete_line_end(path, size))
    except FileNotFoundError:
        return 0
    except (OSError, ValueError, AttributeError):
        return None


def transcript(tap: Any, params: dict) -> Path | None:
    """The session's transcript file: the one it named, else (Codex, which
    names a folder) the rollout the tap would find there. None when there is
    none yet, or it could not be looked for (`find_transcript` tells which)."""
    return find_transcript(tap, params)[0]


def find_transcript(tap: Any, params: dict) -> tuple[Path | None, bool]:
    """`(path, looked)`. `looked` False: the rollout could not be looked for
    (its folder is not there, or the look failed), so None says nothing about
    whether the session wrote any: a gap is never closed on that (it would
    close at 0 and send the stretch), and nothing is settled."""
    named = params.get("transcript")
    if isinstance(named, str) and named:
        return Path(named), True
    folder = params.get("transcript_dir")
    if not isinstance(folder, str) or not folder:
        return None, True
    try:
        if not Path(folder).is_dir():
            return None, False
        return tap.main._resolve_codex_transcript(Path(folder), str(params["sid"])), True
    except Exception:  # noqa: BLE001
        return None, False


# -- the tap's drains, in this process -------------------------------------------


def _frame_offset(depth: int) -> int | None:
    """`stage`'s `end` (the current line's start offset) from the frame that
    called the sanitizer or the title reader."""
    try:
        value = sys._getframe(depth).f_locals.get("end")  # noqa: SLF001 -- see the module docstring
    except (ValueError, AttributeError):
        return None
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _skipped() -> bool:
    """On the thread settling a session: does the line `stage` reads now start
    inside one of its gaps? True when that cannot be told (a skipped line is
    lost, an off line is never sent)."""
    context = getattr(_LOCAL, "catchup", None)
    if context is None:
        return False
    offset = _frame_offset(3)
    # The gaps as they are now: one opened while this settle runs counts too.
    return offset is None or in_gap(_live_gaps(context[0], context[1]), offset)


def native(tap: Any) -> Any:
    """The loaded tap's own gate (`tap/capture_gate.py`, tap 0.10.19), or None
    for a tap before it (wrapped here instead)."""
    module = getattr(tap, "capture_gate", None)
    try:
        return module if module is not None and int(getattr(module, "NATIVE", 0)) >= 1 else None
    except (TypeError, ValueError):
        return None


def _host_gaps(sid: str) -> list:
    """This process's gaps of `sid` not settled yet, for the tap's own gate:
    the recorders' record, a moment ahead of the gap file."""
    with _LOCK:
        gaps = _UNSETTLED.get(sid)
        return [list(g) for g in gaps] if gaps else []


def install(tap: Any, log: Callable[[str], None] = lambda _m: None) -> bool:
    """Wrap the loaded tap's drains once (see the module docstring). A tap that
    gates its own (`native`) is not wrapped: its gate gets this process's gaps
    (`host`), and the tap's own recorder of gap files stands down here (this
    service records them). False when this tap lacks what they wrap: then only
    its own recorder is held."""
    own = native(tap)
    if own is not None:
        own.host(_host_gaps)
        return True
    sj, reconcile = tap.session_journal, tap.reconcile
    if getattr(sj, "_probe_capture_gate", False):
        return True
    needed = (getattr(sj, "_sanitizer", None), getattr(sj, "_title_reader", None),
              getattr(getattr(sj, "Journal", None), "stage", None), getattr(reconcile, "find_gaps", None))
    if not all(callable(f) for f in needed):
        log("capture gate: this tap cannot be gated in its drains; only its own recorder is held while off")
        return False
    real_sanitizer, real_title, real_stage, real_gaps = needed

    def _sanitizer(source):
        real = real_sanitizer(source)
        if getattr(_LOCAL, "catchup", None) is None:
            return real

        def sanitize(line):
            return None if _skipped() else real(line)

        return sanitize

    def _title_reader(source):
        real = real_title(source)
        if real is None or getattr(_LOCAL, "catchup", None) is None:
            return real

        def read_title(line):
            return None if _skipped() else real(line)

        return read_title

    @functools.wraps(real_stage)  # its signature too: `settle` asks it what it takes
    def stage(self, session_id, *args, **kwargs):
        if blocked(session_id) and self.pending(session_id) is None:
            return None
        return real_stage(self, session_id, *args, **kwargs)

    def find_gaps(*args, **kwargs):
        return [gap for gap in real_gaps(*args, **kwargs) if not blocked(getattr(gap, "session_id", None))]

    sj._sanitizer, sj._title_reader, reconcile.find_gaps = _sanitizer, _title_reader, find_gaps
    sj.Journal.stage = stage
    sj._probe_capture_gate = True
    return True


# -- settling ---------------------------------------------------------------------


@contextlib.contextmanager
def _catchup(sid: str, gaps: list):
    previous = getattr(_LOCAL, "catchup", None)
    _LOCAL.catchup = (sid, [list(g) for g in gaps])
    try:
        yield
    finally:
        _LOCAL.catchup = previous


def settle(tap: Any, params: dict, gaps: list, *, finalize: bool, log: Callable[[str], None],
           current: Callable[[], bool] = lambda: True) -> str:
    """Stage and deliver the session from its cursor with every line that
    starts in a gap sent as nothing, until its cursor passes the last gap's
    end (`finalize`: to its end, then FINALIZE). On the session's recorder
    thread, under its environment. DONE (the server's cursor is past every
    gap, or there was nothing to cover), KEPT (nothing was or will be sent
    now, so the gaps stay recorded: this machine ships nothing for it, or it
    never sent anything), RETRY (try again later: no network, another
    recorder holds the session, or `current()` says a newer recording of the
    session took over), REFUSED (refused for good: no login on this machine,
    or the Probe gateway itself answering 401, 403, 404 or 422 in its own
    error shape; a proxy's answer, a 400, 413 or 407, an unknown protocol, a
    local error and an unreadable `.token` are RETRY: `_refused_for_good`), or
    DELETED (the server deleted the session at its team's request: nothing
    more to do). `current` is asked before each batch and before FINALIZE."""
    sid = str(params["sid"])
    sj, cfg = tap.session_journal, tap.config
    with tap.threadenv.install().session(params.get("env") or {}):
        if cfg.killswitch_active() or cfg.cwd_disabled(Path(params["cwd"])):
            return KEPT  # this machine ships nothing for it now
        if finalize and gaps and gaps[0][0] == 0 and not _journals_holding(sj, sid):
            # Off from its first line, and nothing of it was ever staged here:
            # it ends sending nothing, not even a question about it.
            return KEPT
        token = cfg.load_token()
        if not token:
            # Not signed in on this machine; a `.token` that is there and
            # could not be read now is tried again.
            return RETRY if _token_unreadable(cfg) else REFUSED
        journal = None
        requested = False
        answers: dict = {}
        try:
            wire = sj.Wire(cfg.api_base_url(), token, cfg.capture_source())
            _keep_answers(wire, answers)
            remote = wire.receipts(sid)
            journal = sj.Journal(wire.base_url, remote["customer_id"], wire.source)
            if not journal.claim_live(sid):
                return RETRY  # another recorder holds it; it hands over, or ends
            path, looked = find_transcript(tap, params)
            state = journal.get(sid)
            if state is None and not remote.get("stream"):
                if finalize and not (bool(gaps) and gaps[0][0] > 0):
                    return KEPT  # nothing was ever sent, and nothing will be
                if not looked:
                    return RETRY  # its rollout could not be looked for: later
                if path is None or not path.exists():
                    return DONE  # no transcript yet: no line of it was written while off
            if path is None:
                return RETRY
            provenance = None
            if state is None:
                provenance = tap.session_identity.validate_identity(path, wire.source, sid)
            if not current():
                return RETRY
            journal.ensure(sid, path, remote, historical=False, provenance=provenance, cwd=str(params["cwd"]))
            if finalize:
                journal.update(sid, finalize_requested=True)
                requested = True
            target = None if finalize else max((g[1] for g in gaps if g[1] is not None), default=0)
            extra = {}
            with contextlib.suppress(Exception):
                import inspect

                if "pasted_images" in inspect.signature(journal.stage).parameters:
                    extra["pasted_images"] = cfg.pasted_images_on()
            own = native(tap)
            # A tap that gates its own drains skips the lines of `gaps` (and
            # this process's live ones) on this thread itself; an older one is
            # wrapped (`_catchup`).
            with (own.settling(sid, gaps) if own is not None else _catchup(sid, gaps)):
                for _ in range(MAX_SETTLE_BATCHES):
                    if not current():
                        # A newer recording of the session took over (a resume
                        # after its end): it settles, and the session is live,
                        # so its row is not to be finalized.
                        if requested:
                            journal.update(sid, finalize_requested=False)
                        return RETRY
                    now = journal.get(sid) or {}
                    if target is not None and now.get("source_byte_end", 0) >= target and not journal.pending(sid):
                        return DONE
                    body = journal.stage(sid, cwd=str(params["cwd"]), finalize=finalize, **extra)
                    if body is None:
                        now = journal.get(sid) or {}
                        if target is None or now.get("source_byte_end", 0) >= target:
                            return DONE
                        return RETRY  # the transcript ends before the gap did (rewritten?): later
                    try:
                        journal.deliver(sid, wire)
                    except sj.ProtocolRestarted:
                        continue
                    except sj.ReconciliationRequired as exc:
                        if not sj.recoverable(exc) or journal.reconcile_pending(sid, wire) is None:
                            raise
                    if finalize and (journal.get(sid) or {}).get("finalized") and not journal.pending(sid):
                        return DONE
            return RETRY
        except sj.SessionDeleted:
            return DELETED
        except (sj.DeliveryPending, sj.ReconciliationRequired) as exc:
            refused = _refused_for_good(answers)
            log(f"capture gate: session {sid} not settled{'' if refused else ' yet'} "
                f"({type(exc).__name__}: {str(exc)[:200]})")
            return REFUSED if refused else RETRY
        except Exception as exc:  # noqa: BLE001 -- held: the next try goes on from what was delivered
            log(f"capture gate: session {sid} not settled yet ({type(exc).__name__}: {str(exc)[:200]})")
            return RETRY
        finally:
            if journal is not None:
                with contextlib.suppress(Exception):
                    journal.release_live(sid)
                with contextlib.suppress(Exception):
                    journal.close()


def _token_unreadable(cfg: Any) -> bool:
    """Is the paired `.token` there but unreadable now (not "not signed in")?"""
    try:
        path = cfg.token_file()
        if not path.is_file():
            return False
        path.read_text(encoding="utf-8")
        return False
    except OSError:
        return True
    except Exception:  # noqa: BLE001 -- a tap that cannot say: not signed in
        return False


def _keep_answers(wire: Any, answers: dict) -> None:
    """Keep the status and body of the last answer `wire` got (`Wire._request`,
    every tap the service hosts): what `_refused_for_good` reads."""
    request = getattr(wire, "_request", None)
    if not callable(request):
        return

    def kept(*args: Any, **kwargs: Any) -> Any:
        code, body = request(*args, **kwargs)
        answers["code"], answers["body"] = code, body
        return code, body

    with contextlib.suppress(Exception):
        wire._request = kept


def _refused_for_good(answers: dict) -> bool:
    """Did the Probe gateway itself refuse the session for good? Its last
    answer was a 401/403/404/422 in the gateway's own error shape (a JSON
    object whose `detail` is a string or a list: FastAPI's). A proxy's page
    (the tap reads it as `{"detail": "invalid error response"}`), any other
    status (400, 407, 413, ...), an answer that never came and a local error
    are not: tried again."""
    body = answers.get("body")
    detail = body.get("detail") if isinstance(body, dict) else None
    gateway = isinstance(detail, list) or (isinstance(detail, str) and detail != "invalid error response")
    return answers.get("code") in REFUSED_STATUSES and gateway


# -- holding the session's claim ---------------------------------------------------


class Claim:
    """The session's live claim (`Journal.claim_live`) held for a session that
    is off: a `tap watch` of it (an older tap's) offering it to the service
    sees the service's recorder hold it, and hands it over (exits without a
    last pass) instead of recording on; a fresh one finds it taken. Only a
    journal that already holds the session's row is used (found locally:
    nothing is asked of the server for an off session)."""

    def __init__(self, tap: Any, params: dict) -> None:
        self.tap, self.params = tap, params
        self.journal = None

    def take(self) -> str | None:
        """The journal folder whose claim is held now, else None."""
        if self.journal is not None:
            return str(self.journal.directory)
        sid = str(self.params["sid"])
        sj = self.tap.session_journal
        with self.tap.threadenv.install().session(self.params.get("env") or {}):
            for root, destination in _journals_holding(sj, sid):
                try:
                    journal = sj.Journal(destination["base_url"], destination["customer_id"], destination["source"],
                                         directory=root)
                except Exception:  # noqa: BLE001
                    continue
                try:
                    if journal.claim_live(sid):
                        self.journal = journal
                        return str(journal.directory)
                except Exception:  # noqa: BLE001
                    pass
                with contextlib.suppress(Exception):
                    journal.close()
        return None

    def release(self) -> None:
        journal, self.journal = self.journal, None
        if journal is None:
            return
        with contextlib.suppress(Exception):
            journal.release_live(str(self.params["sid"]))
        with contextlib.suppress(Exception):
            journal.close()


def _journals_holding(sj: Any, sid: str) -> list[tuple[Path, dict]]:
    """`(root, destination)` of each journal under this thread's journal root
    that holds a row for `sid` (read-only), as `probe.service.receipts` finds
    them. Only a folder named for its own destination (the tap's namespace
    hash): a `Journal` for any other would create a folder of its own."""
    import hashlib
    import json
    import sqlite3

    found = []
    root = sj.state_root()
    try:
        entries = sorted(entry.name for entry in os.scandir(root) if entry.is_dir(follow_symlinks=False))
    except OSError:
        return found
    for name in entries[:64]:
        folder = root / name
        db = folder / "state.sqlite3"
        if not db.is_file():
            continue
        try:
            # `DESTINATION_NAME` from tap 0.10.7; the same file name before it.
            name_of = getattr(sj, "DESTINATION_NAME", "destination.json")
            destination = json.loads((folder / name_of).read_text(encoding="utf-8"))
        except (OSError, ValueError, AttributeError):
            continue
        if not isinstance(destination, dict) or not all(
            isinstance(destination.get(k), str) and destination.get(k) for k in ("base_url", "customer_id", "source")
        ):
            continue
        named = json.dumps([destination["base_url"].rstrip("/"), destination["customer_id"], destination["source"]])
        if hashlib.sha256(named.encode()).hexdigest() != name:
            continue
        try:
            conn = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True, timeout=0.2)
        except (sqlite3.Error, ValueError):
            continue
        try:
            held = False
            for table in ("sessions", "fragment_sessions"):
                try:
                    if conn.execute(f"SELECT 1 FROM {table} WHERE session_id=?", (sid,)).fetchone():  # noqa: S608
                        held = True
                        break
                except sqlite3.Error:
                    continue
        finally:
            conn.close()
        if held:
            found.append((root, destination))
    return found


def marker_names(tap: Any, params: dict) -> str | None:
    """What the session's `.hosted` marker names now (None without one)."""
    with contextlib.suppress(Exception):
        with tap.threadenv.install().session(params.get("env") or {}):
            return tap.config.hosted_file(str(params["sid"])).read_text(encoding="utf-8").strip()
    return None


def write_marker(tap: Any, params: dict, pid: int | None) -> None:
    """The session's `.hosted` marker names `pid` (the session's own agent,
    while it is off and no service runs): the hooks of a tap that asks about
    a live marker only with `kill -0` (ensure-daemon.sh's fast path) then
    start no service and no `tap watch` for it every prompt. A reader that
    checks the marker names the service (`capture_state._hosted_pid`,
    `record_client.hosted_pid`, pi) reads it as not recorded by the service,
    which is true. None: the marker goes, when it names this process or `pid`'s
    owner."""
    sid = str(params["sid"])
    with contextlib.suppress(Exception):
        with tap.threadenv.install().session(params.get("env") or {}):
            if pid is not None:
                tap.record_client._write_hosted(sid, pid)
                return
            path = tap.config.hosted_file(sid)
            owner = params.get("owner") if isinstance(params.get("owner"), dict) else {}
            named = path.read_text(encoding="utf-8").strip()
            if named in (str(os.getpid()), str(owner.get("pid"))):
                path.unlink()
