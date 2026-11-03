def session_state(session_id: str) -> "str | None":
    """This conversation's state, or None when nobody has decided yet.

    MIGRATION LIVES HERE, and it is the most consequential rule in the switch.
    A legacy `off` marker was written by somebody who meant "stop recording,
    keep searching" -- the switch has never gated reads. That is the new
    `read-only` exactly. Mapping it to the new `off` would retroactively take
    away reads they never gave up, so it maps to `read-only` and the hard `off`
    is reachable only from an explicit new-format write.

        .state = full | daemon | read-only | off  ->  that
        .tracking = "on"                  ->  full
        .tracking = "off"                 ->  read-only
        <sid>.off present                 ->  read-only
        nothing                           ->  None (undecided)
    """
    if not valid_session_id(session_id):
        return None
    try:
        raw = state_path(session_id).read_text(encoding="utf-8").strip().lower()
        if raw in STATES:
            return raw
    except OSError:
        pass
    # No canonical file: fall back to the legacy spellings and MIGRATE them.
    # Read those directly rather than through `tracking_signal`, which now
    # consults `.state` first and would re-walk a file we just missed.
    legacy = _legacy_tracking_value(session_id)
    if legacy == "on":
        return STATE_FULL
    if legacy == "off":
        return STATE_READ_ONLY
    return STATE_READ_ONLY if _legacy_off_path(session_id).is_file() else None


def _publish_atomically(path: Path, content: str) -> bool:
    """Write `content` to `path` so no reader can ever see it half-written.

    A plain `write_text` truncates first, so a concurrent reader -- and there is
    always one, the status line renders on every turn -- can observe an EMPTY
    marker and resolve it as "no decision". Write to a unique temp and
    `os.replace`, which is atomic on POSIX and on Windows.

    `os.replace`, not `os.link`: this is a LAST-WRITER-WINS file, unlike the
    exclusive publish in `set_session_state_if_absent`, which must fail rather
    than overwrite.
    """
    tmp = "%s.tmp-%d-%d" % (str(path), os.getpid(), time.time_ns())
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0), 0o600)
    except OSError:
        return False
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp, path)
        return True
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return False


def _write_compat_tracking(session_id: str, state: str) -> None:
    """Leave older clients a value they cannot misread. Best effort.

    `full` -> on; `read-only` and `off` -> off. Both non-recording states project
    to `off` because that is the strongest thing a two-valued reader can be told,
    and it is TRUE of both: neither records. Failure here is not fatal -- the
    canonical file already landed -- but it is the difference between an old CLI
    reading an opt-out and an old CLI inventing consent.
    """
    if _publish_atomically(
        tracking_signal_path(session_id), "on\n" if state in RECORDING_STATES else "off\n"
    ):
        try:
            _legacy_off_path(session_id).unlink(missing_ok=True)
        except OSError:
            pass


def _legacy_tracking_value(session_id: str) -> "str | None":
    """The two-valued file's raw decision, or None. Never consults `.state`."""
    try:
        value = tracking_signal_path(session_id).read_text(encoding="utf-8").strip().lower()
    except OSError:
        return None
    return value if value in ("on", "off") else None


def set_session_state(
    session_id: str, state: str, now: "float | None" = None, *, explicit: bool = True
) -> bool:
    """Record the decision. True when the canonical file now reads `state`.

    Every switch move goes through here, so this is also where an inline stretch
    (`switch_to_inline`) ends, at `now` (default: the clock): its interval is
    logged BEFORE the state reopens recording, and a failed log keeps the
    marker, closed, rather than handing the stretch back to the daemon. When
    neither can be written the move does not happen (False).

    `explicit` (every caller but automation): the researcher chose it, so the
    source becomes `explicit`. Automation that only follows a default
    (`explicit=False`, an `on` session following its profile) keeps a
    `default` source a default."""
    if not valid_session_id(session_id) or state not in STATES:
        return False
    with _StateLock(session_id):
        return _set_session_state_locked(session_id, state, now, explicit=explicit)


def _set_session_state_locked(session_id: str, state: str, now: "float | None", *, explicit: bool) -> bool:
    """`set_session_state`'s move, with the session's `_StateLock` already held."""
    keep = _close_inline(session_id, inline_marker(session_id), now)
    if keep is None:
        return False
    was_default = not explicit and state_source(session_id) == SOURCE_DEFAULT
    if not _set_state_unlocked(session_id, state):
        return False
    if not keep:
        _remove_inline_marker(session_id)
    if explicit:
        _publish_atomically(state_source_path(session_id), SOURCE_EXPLICIT + "\n")
    elif was_default:
        # Rewritten AFTER the state, so the source is not older than it.
        _publish_atomically(state_source_path(session_id), SOURCE_DEFAULT + "\n")
    return True


def lower_session_state(session_id: str, state: str) -> "bool | None":
    """Move `session_id` to `state` only when its switch is louder than that, read
    and written under the session's own lock, so a switch the person moves at the
    same moment is compared against, never overwritten by a louder value (an
    explicit choice, as `set_session_state`). True: it moved; None: it was not
    louder (nothing to do); False: the write failed."""
    if not valid_session_id(session_id) or state not in STATES:
        return False
    with _StateLock(session_id):
        if not louder(session_state(session_id), state):
            return None
        return _set_session_state_locked(session_id, state, None, explicit=True) and session_state(session_id) == state


def _set_state_unlocked(session_id: str, state: str) -> bool:
    if not _publish_atomically(state_path(session_id), state + "\n"):
        return False
    _write_compat_tracking(session_id, state)
    return True


def daemon_session(session_id: str, source: "str | None" = None) -> bool:
    """Does the Probe daemon record and read for this session (the wizard's "Who
    records")? The lean plugin's `<sid>.profile` mark decides when present; without
    one, the machine's setting for the coding agent (`recorder`) does."""
    marked = session_profile(session_id)
    if marked is not None:
        return marked == RECORDER_DAEMON
    return recorder(source) == RECORDER_DAEMON if source else False


def on_state(session_id: str, source: "str | None" = None) -> str:
    """What `on` is STORED as in this session: `daemon` where the daemon records
    (`daemon_session`), else `full`. The one place the switch's `on` meets the
    wizard's "Who records"."""
    return STATE_DAEMON if daemon_session(session_id, source) else STATE_FULL


def switch_target(session_id: str, state: str, source: "str | None" = None) -> "str | None":
    """The state a switch move to `state` STORES, or None for a move the switch
    does not make. `full` is `on` and resolves by `on_state`; `read-only` and
    `off` are themselves. `daemon` asked for BY NAME is the one refusal (None):
    the caller answers `DAEMON_SWITCH_REFUSAL`."""
    if state == STATE_FULL:
        return on_state(session_id, source)
    return state if state in SWITCH_STATES else None


def seed_state(session_id: str, default: str, source: "str | None" = None) -> str:
    """The state a NEW session starts at from `default`: `on` (and a `daemon`
    default stored before the switch lost that position) is stored by who records
    (`on_state`); `read-only` and `off` are themselves. Every seeding path uses it
    -- the session-start hook, and `probe session initialize` for pi."""
    if default in (STATE_FULL, STATE_DAEMON):
        return on_state(session_id, source)
    return default


def profile_path(session_id: str) -> Path:
    """`<sid>.profile`: `daemon` when the lean daemon-profile plugin started this
    session (daemon reads), so a command run OUTSIDE the agent -- `probe session
    track --session <sid>` from a terminal -- still knows its `on` is `daemon`."""
    return state_path(session_id).with_suffix(".profile")


def session_profile(session_id: str) -> "str | None":
    if not valid_session_id(session_id):
        return None
    try:
        return profile_path(session_id).read_text(encoding="utf-8").strip() or None
    except OSError:
        return None


def mark_session_profile(session_id: str, profile: str) -> None:
    """Best effort: the lean plugin marks its sessions at SessionStart."""
    if not valid_session_id(session_id):
        return
    path = profile_path(session_id)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name("%s.tmp-%d" % (path.name, os.getpid()))
        tmp.write_text(profile, encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# WHO SET THE STATE
# ---------------------------------------------------------------------------
#
# Whether the session's state came from a DEFAULT or the researcher chose it
# (`state_source`; `probe session status` says which). One file beside
# `<sid>.state`, whose bytes never change:
#
#     <sid>.state-source   `explicit` | `default`
#
# EXPLICIT is a typed `/probe ...`, `probe session state ...` and the environment
# override. DEFAULT is the machine's (the
# wizard's) setting and the shipped one. A MISSING or unreadable source reads
# explicit: an older client wrote that state, and what we cannot prove was a
# default is never called one. A `default` older than the state it describes
# reads explicit too: a writer that does not know this file (an older plugin's
# guard) moved the state after the seed.
#
# An older CLI may have left a `<sid>.auto-pause` beside it (its ML gate's
# pause): nothing reads it, and `prune` takes it with the session's other files.

STATE_SOURCE_SUFFIX = ".state-source"
SOURCE_EXPLICIT = "explicit"
SOURCE_DEFAULT = "default"
#: How much newer `.state` may be than a `default` source and still be the seed's
#: own write (the seed claims the source a moment BEFORE it publishes the state).
_SOURCE_SLACK_S = 2.0


def state_source_path(session_id: str) -> Path:
    return sessions_dir() / (session_id + STATE_SOURCE_SUFFIX)


def default_is_explicit(source: str) -> bool:
    """Is a default `resolve_state_default` resolved (its diagnostic `source`)
    the researcher's own explicit setting? The environment override is; the
    machine file and the shipped value are not."""
    return source == "environment"


def seed_source(source: str) -> str:
    """The source a seed records for a default `resolve_state_default` resolved
    from `source` (its diagnostic second value)."""
    return SOURCE_EXPLICIT if default_is_explicit(source) else SOURCE_DEFAULT


#: `probe session status`'s word for a session with no source file (an older
#: client seeded it). It reads explicit everywhere else.
SOURCE_UNRECORDED = "unrecorded"


def state_source_label(session_id: str) -> str:
    """`state_source`, or `unrecorded` when no source file exists: what
    `probe session status` prints. Behaviour is unchanged (it counts as explicit)."""
    if not valid_session_id(session_id) or not state_source_path(session_id).exists():
        return SOURCE_UNRECORDED
    return state_source(session_id)


def state_source(session_id: str) -> str:
    """`default` when the session's state is provably a seeded default, else
    `explicit` (see the block above)."""
    if not valid_session_id(session_id):
        return SOURCE_EXPLICIT
    path = state_source_path(session_id)
    try:
        raw = path.read_text(encoding="utf-8").strip()
        claimed = path.stat().st_mtime
    except OSError:
        return SOURCE_EXPLICIT
    if raw != SOURCE_DEFAULT:
        return SOURCE_EXPLICIT
    try:
        moved = state_path(session_id).stat().st_mtime
    except OSError:
        return SOURCE_DEFAULT  # the seed claimed the source and is about to publish
    return SOURCE_EXPLICIT if moved > claimed + _SOURCE_SLACK_S else SOURCE_DEFAULT


def _claim_default_source(session_id: str) -> bool:
    """The seed claims `default` BEFORE it publishes the state, and only when no
    source exists yet: an explicit writer that got there first keeps its claim."""
    path = state_source_path(session_id)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0), 0o600)
    except OSError:
        return False
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as fh:
            fh.write(SOURCE_DEFAULT + "\n")
        return True
    except OSError:
        return False


def _drop_source(session_id: str) -> None:
    try:
        state_source_path(session_id).unlink()
    except OSError:
        pass


