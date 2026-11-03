# ---------------------------------------------------------------------------
# WHAT THE SESSION OWES (notes parity N3)
# ---------------------------------------------------------------------------
#
# The CLI keeps it (`probe.cli.owed`); the end-of-turn hooks read only whether
# the agent's own items are there before asking the CLI (`probe session owed
# --send-back`). Only a CLI that has that command writes the file.

OWED_DIRNAME = "owed"
#: How many times an inline agent is sent back for one item, per session (`owed.MAX_ASKS`).
OWED_MAX_ASKS = 2
#: Where a summary checkout or push leaves the team's summaries mode
#: (`summary_cli.MODE_FILE`, `{"mode", "at", "server"}`), and how long it stands.
SUMMARIES_MODE_FILE = ("summaries", "mode.json")
SUMMARIES_MODE_TTL_S = 24 * 3600


def owed_path(session_id: str) -> Path:
    return state_dir() / OWED_DIRNAME / f"{session_id}.json"


def seen_recorder_mode() -> bool:
    """Did this machine last see the team's summaries in recorder mode, within
    the TTL? (Any server: `summary_cli.seen_mode` also matches the server.)"""
    try:
        seen = json.loads(state_dir().joinpath(*SUMMARIES_MODE_FILE).read_text(encoding="utf-8"))
        return (isinstance(seen, dict) and seen.get("mode") == "recorder"
                and time.time() - float(seen.get("at") or 0) < SUMMARIES_MODE_TTL_S)
    except (OSError, ValueError, TypeError):
        return False


def agent_owes(session_id: str) -> bool:
    """Could `probe session owed --send-back` say anything now? An item of the
    agent's own (not the daemon's) asked about fewer than OWED_MAX_ASKS times,
    a summary only while recorder mode was seen: an exhausted ledger starts no
    CLI at the end of every turn."""
    if not valid_session_id(session_id):
        return False
    try:
        data = json.loads(owed_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    items = data.get("items") if isinstance(data, dict) else None
    asks = data.get("asks") if isinstance(data, dict) and isinstance(data.get("asks"), dict) else {}
    if not isinstance(items, list):
        return False
    recorder = None
    for item in items:
        if not (isinstance(item, dict) and item.get("by") == "agent"):
            continue
        count = asks.get(f"{item.get('why')} {item.get('kind')} {item.get('ref')}", 0)
        if isinstance(count, int) and count >= OWED_MAX_ASKS:
            continue
        if item.get("why") == "summary":
            recorder = seen_recorder_mode() if recorder is None else recorder
            if not recorder:
                continue
        return True
    return False


def set_session_state_if_absent(
    session_id: str, state: str, *, source: "str | None" = None
) -> bool:
    """Seed the STARTING state, only when nobody has decided. True when we did.

    `source`: who decided the default (`SOURCE_DEFAULT` for the machine's or the
    shipped one, `SOURCE_EXPLICIT` for the environment's or a folder's,
    `default_is_explicit`). None writes no source file, which reads explicit:
    a caller that does not know never labels the session's state a default. A
    `default` is claimed BEFORE the state is published and dropped again when
    the seed loses, so an explicit write never ends up labelled a default.

    Exclusive by construction, exactly as `set_tracking_if_absent` is and for the
    same reasons -- see that docstring for why `os.link` rather than a
    check-then-write, and why the temp name carries pid AND a nanosecond stamp.
    The legacy spellings are re-checked after publishing for the same reason too:
    an old client writing `<sid>.off` between the read and the publish must not
    be overridden by automation.
    """
    if not valid_session_id(session_id) or state not in STATES:
        return False
    if session_state(session_id) is not None:
        return False
    claimed = source == SOURCE_DEFAULT and _claim_default_source(session_id)
    seeded = _seed_state_unlocked(session_id, state)
    if seeded and source == SOURCE_EXPLICIT:
        _publish_atomically(state_source_path(session_id), SOURCE_EXPLICIT + "\n")
    elif claimed and not seeded:
        _drop_source(session_id)
    return seeded


def _seed_state_unlocked(session_id: str, state: str) -> bool:
    """`set_session_state_if_absent`'s exclusive publish (its docstring)."""
    path = state_path(session_id)
    tmp_path = "%s.tmp-%d-%d" % (str(path), os.getpid(), time.time_ns())
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle = os.open(tmp_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0), 0o600)
    except OSError:
        return False
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as fh:
            fh.write(state + "\n")
        try:
            os.link(tmp_path, path)
        except OSError:
            return False  # EEXIST: someone decided between the read and the publish
        # BOTH LEGACY SPELLINGS ARE RE-CHECKED AFTER PUBLISHING, and the second
        # one is new with this file. `os.link` arbitrates `<sid>.state` only, so
        # a decision that landed in either older spelling between our read and
        # our publish would otherwise be overwritten by the compat write below --
        # automation silently overriding an explicit opt-out, which is the one
        # thing this must never do. Losing that race is repaired by removing what
        # we just published, not by keeping it.
        try:
            published = path.read_text(encoding="utf-8").strip().lower()
        except OSError:
            published = ""
        if published != state:
            # A NEWER WRITER took the canonical file. `os.link` refuses to
            # replace, but `set_session_state` publishes with `os.replace`,
            # which does, so what is on disk is now somebody's explicit
            # decision. Leave it and report that we did not decide. Deleting
            # here is how a seed erased an explicit `off` that had landed a
            # microsecond earlier, leaving only its compat file to migrate back
            # to read-only and silently reopen reads the researcher had closed.
            return False
        legacy = _legacy_tracking_value(session_id)
        expected = "on" if state in RECORDING_STATES else "off"
        if _legacy_off_path(session_id).is_file() or (
            legacy is not None and legacy != expected
        ):
            # An OLDER CLIENT wrote a legacy opt-out while we were publishing.
            # Only a value that DISAGREES counts: the one we are about to write
            # ourselves agrees by construction.
            path.unlink(missing_ok=True)
            return False
        _write_compat_tracking(session_id, state)
        return True
    except OSError:
        return False
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def notify_flag_path() -> Path:
    """Opt-in marker for the change NOTICE, the Codex-shaped half of this feature.

    Codex has no surface a computed segment can render into — its status line is a
    picker over built-in items — so the same information is delivered as a message
    when it CHANGES instead of as a line that is always there. Enabling that is
    still opt-in, and this file is the opt-in, exactly as the install directory is
    for the status line.

    In the probe state dir rather than under either agent's config: one flag, read
    by a hook that both agents load, and it outlives a reinstall of either.
    """
    return state_dir() / "statusline-notify"


def notify_enabled() -> bool:
    return notify_flag_path().is_file()


def state_key(state: dict | None, *, live: bool) -> str:
    """What "changed" MEANS, as one comparable string.

    Only the two things the notice actually reports. `updated_at` moves on every
    refresh and `run_ids` churns as runs come and go, so comparing whole markers
    would fire a notice several times a minute while nothing a reader cares about
    had changed.
    """
    project = state.get("project") if isinstance(state, dict) else None
    if not (isinstance(project, str) and project):
        return "untracked"
    return f"{project}|{'running' if live else 'idle'}"


def _capture_reason(state: dict | None) -> str:
    """Why no transcript daemon is watching this session, or `""` for silence.

    The marker's `capture` object is written by the background refresh hook, and
    the reason is one of the closed vocabulary in `probe.cli.capture_state`.
    SILENCE IS THE DEFAULT, and deliberately so: a marker written by an older
    refresh hook carries no `capture` key at all, and every shape this function
    does not recognise — a missing key, a null, a non-string reason, a `running`
    that is not exactly `False` — means nobody measured anything. Rendering a
    guess there would put a fabricated diagnosis on somebody's status line.

    A multi-line reason is refused rather than flattened: the one thing the
    segment may never do is emit a newline, and a reason that needs two lines is
    not a reason this vocabulary produced.

    Shared by `render` and `message` so the two surfaces cannot come to disagree
    about when capture is missing.
    """
    capture = state.get("capture") if isinstance(state, dict) else None
    if not isinstance(capture, dict) or capture.get("running") is not False:
        return ""
    reason = capture.get("reason")
    if not (isinstance(reason, str) and reason) or "\n" in reason or "\r" in reason:
        return ""
    return reason


def message(state: dict | None, *, live: bool = False, tracking: bool = True) -> str:
    """One line for an agent with no status line to hang a segment on.

    Built from the same labels the segment uses, so the two surfaces cannot drift
    into describing the same state differently. No colour and no glyph: this is a
    sentence in a transcript, not a mark on a line.

    `tracking` defaults to True because that is the only state this notice has
    ever been emitted in — `statusline_notify.py` reaches here having already
    resolved the switch. It is a parameter rather than an assumption so a caller
    that has NOT resolved it cannot accidentally claim a capture failure matters
    to a session that is recording nothing.

    NO WIDTH CAP HERE, unlike `render`. This is a sentence in a transcript, which
    wraps harmlessly; the segment shares one line with strangers, which does not.
    """
    project = state.get("project") if isinstance(state, dict) else None
    if not (isinstance(project, str) and project):
        return "Probe: this session is not tracked yet."
    text = "Probe: " + _LABEL_TRACKED + project
    if live:
        text += _ACCENT_TEXT
    reason = _capture_reason(state) if tracking else ""
    if reason == _CHOSEN_OFF_REASON:
        text += "; session transcripts are turned off"
    elif reason:
        text += ", but not capturing session transcript: " + reason
    return text


def read_notified(session_id: str) -> str | None:
    """The state key this session was last told about, or None."""
    if not valid_session_id(session_id):
        return None
    try:
        return (sessions_dir() / (session_id + ".notified")).read_text(encoding="utf-8").strip()
    except OSError:
        return None


def write_notified(session_id: str, key: str) -> None:
    """Record what we just said. Never raises.

    Written AFTER the message is emitted rather than before: a crash between the
    two costs a repeated notice, which is a great deal better than a silent one
    the reader never sees.
    """
    if not valid_session_id(session_id):
        return
    path = sessions_dir() / (session_id + ".notified")
    tmp = path.parent / (path.name + "." + str(os.getpid()) + ".tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(key, encoding="utf-8")
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass


