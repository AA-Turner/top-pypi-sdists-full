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

    Exclusive by construction, not by check-then-write: the content goes to a
    UNIQUE temp file (pid AND a nanosecond stamp, O_EXCL, so two threads never
    share it) and is PUBLISHED with os.link, which fails with EEXIST rather than
    replacing. A researcher's `off` landing mid-seed keeps their `off`, and a
    crash cannot strand a half-written state. The legacy spellings are re-checked
    after publishing: an old client writing `<sid>.off` between the read and the
    publish must not be overridden by automation. Every seed reaches this through
    `seed_state` (Probe's hooks started the chat) or `seed_inline` (they did not).
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


#: How to fix each capture reason (`probe.cli.capture.state.REASONS`) and each daemon reason (`DAEMON_REASON_WORDS`):
#: one source for `probe statusline show`, the notice and doctor. Kept here because the plugin hooks load this file
#: with no `probe` package; `tests/test_statusline_fixes.py` pins the keys to both vocabularies.
CAPTURE_REASON_FIXES = {
    "running": "",
    "not started": "start a new chat; capture starts with the chat",
    "not installed": INSTALL_HINT,
    "not paired": INSTALL_HINT,
    "killswitch": "turn transcripts back on: probe capture on",
    "disabled path": "see probe doctor",
    "no session file": "see probe doctor",
    "interpreter too old": REPAIR_HINT,
    "halted": "see probe doctor",
    "turned off": "turn transcripts back on: probe capture on",
    "awaiting install": INSTALL_HINT,
    "not recording": "the Probe service is retrying; see probe doctor",
    "Probe is off": "turn Probe on: /probe on",
}
DAEMON_REASON_FIXES = {
    "not-started": "see probe doctor",
    "expired": "see probe doctor",
    "stopped": "see probe doctor",
    "gateway": "check the network, then see probe doctor",
    "budget": "see probe doctor",
    "unauthorized": DAEMON_HINT,
    "error": "see probe doctor",
    "disk_full": "free some disk space",
}


def get_capture_fix(reason: str) -> str:
    """How to fix a capture reason; a reason this copy does not know points at doctor."""
    return CAPTURE_REASON_FIXES.get(reason, "see probe doctor")


def get_daemon_fix(reason: "str | None") -> str:
    """How to fix a daemon reason; an unknown one points at doctor."""
    return DAEMON_REASON_FIXES.get(reason or "", "see probe doctor")


def _get_notice_words(session_state: "str | None", *, is_manual: bool = False) -> str:
    """The notice's state words: `on (daemon)` for a stored `daemon`, else `on (inline)` (its caller knows no more),
    tagged `manual` as the status line tags them (`is_manual`: the person sets this chat's switch)."""
    state = STATE_FULL if session_state not in (STATE_DAEMON, STATE_FULL) else session_state
    return get_state_words(state, Reader.DAEMON if state == STATE_DAEMON else Reader.INLINE, is_manual=is_manual)


def state_key(
    state: dict | None, *, live: bool = False, session_state: "str | None" = None, is_manual: bool = False
) -> str:
    """What "changed" means for the notice: exactly what it would show (words, title, note and reason), so a capture
    failure is heard and a run starting or stopping is not. `live` is accepted for older callers and ignored."""
    title = _get_line_title(state)
    reason = _capture_reason(state)
    return "|".join((_get_notice_words(session_state, is_manual=is_manual), title or "-", reason or "-"))


def message(
    state: dict | None, *, live: bool = False, tracking: bool = True, session_state: "str | None" = None,
    is_manual: bool = False,
) -> str:
    """One line for an agent with no status line, read by the person: `<words> | <title> | <note>`, the
    status line's own words with no glyph and no width cap (the one place a capture reason and its fix fit).

    `tracking` defaults to True: `statusline_notify.py` reaches here only for a recording chat. `live` is accepted for
    older callers and ignored. `is_manual`: the person sets this chat's switch (not `is_auto_chat`).
    """
    words = _get_notice_words(session_state, is_manual=is_manual)
    title = _get_line_title(state)
    fields = [words, title or NOTE_NOTHING_FILED]
    reason = _capture_reason(state) if tracking else ""
    if reason == _CHOSEN_OFF_REASON:
        fields.append(NOTE_TRANSCRIPTS_OFF)
    elif reason:
        fields.append(f"{NOTE_TRANSCRIPT_NOT_RECORDED}: {reason}; fix: {get_capture_fix(reason)}")
    return STATUS_DIVIDER.join(fields)


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




# ---------------------------------------------------------------------------
# WHAT RECORDS LESS NOW, AND WHO LOWERED IT (fixes-1107b T2, PR B)
# ---------------------------------------------------------------------------
#
#     <state>/probe/recording-lowered.json    {"lowered": [ENTRY, ...]}
#     ENTRY = {"scope", "state", "by", "since", "at", "session", "until", "told", "offered"}
#
# The agent's CLI adds an entry when it lowers a machine setting for the person (new chats
# read/off, Runs only, sign out: `record_lowering`). Whether it is lowered NOW is read from the
# setting itself (`_is_in_effect`), so the person's own move back (the app, the wizard, a
# typed command, an older client) ends it with no call here. A closed entry is the stretch
# the missed-chats offer covers (`take_missed_offers`). This chat's switch is `load_agent_move`.

LOWERED_FILENAME = "recording-lowered.json"
SCOPE_CHAT = "chat"
SCOPE_DEFAULT = "default"
SCOPE_PROFILE = "profile"
SCOPE_SIGN_IN = "sign_in"
MACHINE_SCOPES = (SCOPE_DEFAULT, SCOPE_PROFILE, SCOPE_SIGN_IN)
#: The lowered `state` of Runs only and of a sign-out (a default's is its stored state).
LOWERED_RUNS_ONLY = "runs"
LOWERED_SIGNED_OUT = "signed_out"
#: Where each entry was told: the chat that made the change (its Stop hook), a session's start.
TOLD_IN_CHAT = "chat"
TOLD_AT_START = "start"
#: Entries kept at most, and how long a closed one stays (Claude Code deletes chats after 30 days).
MAX_LOWERED = 20
LOWERED_KEEP_S = 45 * 86400
#: settings.json, beside the config file (`probe.foundation.settings_file.FILE_NAME`).
SETTINGS_FILENAME = "settings.json"

#: The person's lines: start with "Probe:", never "me", end with the undo (design review).
NOTICE_CHAT = {
    STATE_OFF: 'Probe: off for this chat. Say "turn Probe back on" or type `/probe on`.',
    STATE_READ_ONLY: 'Probe: read-only for this chat. Say "turn Probe back on" or type `/probe on`.',
}
NOTICE_CHAT_ON = "Probe: on for this chat; your agent turned it on."
NOTICE_CHAT_INLINE = "Probe: your agent now reads and writes Probe itself in this chat. Type `/probe on` to undo."
NOTICE_DEFAULT = {
    STATE_OFF: 'Probe: new chats start off. This chat is unchanged. Say "turn new chats back on".',
    STATE_READ_ONLY: 'Probe: new chats start read-only. This chat is unchanged. Say "turn new chats back on".',
}
NOTICE_RUNS_ONLY = 'Probe: chats are no longer recorded on this computer; runs still are. Say "record my chats again".'
NOTICE_SIGNED_OUT = ('Probe: signed out here; nothing is recorded until you sign in again. '
                     'Say "sign me back in to Probe".')
NOTICE_AGENT_REMOVED = 'Probe: removed from {agent}; its chats are no longer recorded. Say "add Probe back to {agent}".'
NOTICE_UNINSTALLED = "Probe: removed from this computer."
#: The current state, for a status line, pi's footer and `probe status` (never who or when).
STATUS_WORDS = {
    (SCOPE_CHAT, STATE_OFF): "Probe: off (this chat)",
    (SCOPE_CHAT, STATE_READ_ONLY): "Probe: read (this chat)",
    (SCOPE_DEFAULT, STATE_OFF): "Probe: new chats off",
    (SCOPE_DEFAULT, STATE_READ_ONLY): "Probe: new chats read",
    (SCOPE_PROFILE, LOWERED_RUNS_ONLY): "Probe: runs only",
    (SCOPE_SIGN_IN, LOWERED_SIGNED_OUT): "Probe: signed out",
}
STATUS_PREFIX = "Probe: "


def get_lowered_notice(scope: str, state: str) -> "str | None":
    """The person's line for `scope` lowered to `state`, or None."""
    if scope == SCOPE_CHAT:
        return NOTICE_CHAT.get(state)
    if scope == SCOPE_DEFAULT:
        return NOTICE_DEFAULT.get(state)
    return {SCOPE_PROFILE: NOTICE_RUNS_ONLY, SCOPE_SIGN_IN: NOTICE_SIGNED_OUT}.get(scope)


def get_agent_move_notice(state: str) -> "str | None":
    """The person's line for the agent's move of this chat to `state` (`load_agent_move`)."""
    if state == MOVED_TO_INLINE:
        return NOTICE_CHAT_INLINE
    if state in RECORDING_STATES:
        return NOTICE_CHAT_ON
    return NOTICE_CHAT.get(state)


def get_lowered_path() -> Path:
    return state_dir() / LOWERED_FILENAME


def _make_lowered_lock() -> "_StateLock":
    return _StateLock("", get_lowered_path().with_name(LOWERED_FILENAME + ".lock"))


def _to_iso(at: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(at))


def _load_lowered() -> list:
    try:
        data = json.loads(get_lowered_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    entries = data.get("lowered") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict) and entry.get("scope") in MACHINE_SCOPES
            and isinstance(entry.get("state"), str) and _finite(entry.get("since")) is not None]


def _save_lowered(entries: list, now: float) -> None:
    kept = [entry for entry in entries
            if entry.get("until") is None or now - (_finite(entry.get("until")) or 0) < LOWERED_KEEP_S]
    _publish_atomically(get_lowered_path(), json.dumps({"lowered": kept[-MAX_LOWERED:]}) + "\n")


def _load_setting_value(key: str) -> object:
    """A setting's newest `value` in settings.json (beside the config), or None."""
    try:
        data = json.loads((config_path().parent / SETTINGS_FILENAME).read_text(encoding="utf-8"))
        return data["settings"][key]["value"]
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _load_live_value(scope: str, config: dict) -> "str | None":
    """`scope`'s setting as it is now (a stored state, `runs`/`full`, `signed_out`/`signed_in`);
    None when it cannot be read (no config, an unreadable settings.json): never a guess."""
    if scope == SCOPE_DEFAULT:
        return (_stored_state(config.get(DEFAULTS_KEY)) or DEFAULT_STATE) if config else None
    if scope == SCOPE_PROFILE:
        value = _load_setting_value(SCOPE_PROFILE)
        return value if isinstance(value, str) else None
    if scope == SCOPE_SIGN_IN:
        return "signed_in" if configured(config, environ={}) else LOWERED_SIGNED_OUT
    return None


def _is_in_effect(entry: dict, config: dict) -> "bool | None":
    """Is `entry`'s setting still where the agent put it (its notice stands)? None: cannot tell."""
    value = _load_live_value(entry.get("scope"), config)
    return None if value is None else value == entry.get("state")


def _is_back_up(entry: dict, config: dict) -> "bool | None":
    """Does `entry`'s setting record again (its stretch ends)? Moved elsewhere but still down (the
    person turned new chats from read to off) is not back up. None: cannot tell."""
    value = _load_live_value(entry.get("scope"), config)
    if value is None:
        return None
    if entry.get("scope") == SCOPE_DEFAULT:
        return value in RECORDING_STATES
    return value != entry.get("state")


def _to_public(entry: dict) -> dict:
    """An entry as `probe status --json` shows it (`recording_lowered`)."""
    scope, state = entry["scope"], entry["state"]
    return {"scope": scope, "state": STATE_LABELS.get(state, state), "by": entry.get("by") or MOVED_BY_AGENT,
            "at": _to_iso(_finite(entry.get("at")) or entry["since"]),
            "notice": get_lowered_notice(scope, state), "status": STATUS_WORDS.get((scope, state))}


def get_this_chat_lowered(session_id: str) -> "dict | None":
    """This chat's switch, lowered by its agent and still there (`recording_lowered`'s chat entry)."""
    move = load_agent_move(session_id)
    if move is None or move["state"] not in NOTICE_CHAT:
        return None
    return {"scope": SCOPE_CHAT, "state": STATE_LABELS[move["state"]], "by": MOVED_BY_AGENT,
            "at": _to_iso(move["at"]), "notice": NOTICE_CHAT[move["state"]],
            "status": STATUS_WORDS[(SCOPE_CHAT, move["state"])]}


def record_lowering(scope: str, state: str, *, session: "str | None" = None, now: "float | None" = None) -> None:
    """The agent just lowered `scope` to `state` for the person: one open entry per scope, its
    stretch starting at the first lowering still open. Best effort."""
    if scope not in MACHINE_SCOPES:
        return
    at = time.time() if now is None else now
    with _make_lowered_lock():
        entries = _load_lowered()
        still = next((entry for entry in entries if entry["scope"] == scope and entry.get("until") is None), None)
        entries = [entry for entry in entries if entry is not still]
        entries.append({"scope": scope, "state": state, "by": MOVED_BY_AGENT,
                        "since": still["since"] if still else at, "at": at,
                        "session": session if valid_session_id(session or "") else None,
                        "until": None, "told": [], "offered": False})
        _save_lowered(entries, at)


def record_raise(scope: str, now: "float | None" = None) -> None:
    """`scope` is back where it was: its open entry closes now. Best effort."""
    at = time.time() if now is None else now
    with _make_lowered_lock():
        entries = _load_lowered()
        if any(entry["scope"] == scope and entry.get("until") is None for entry in entries):
            for entry in entries:
                if entry["scope"] == scope and entry.get("until") is None:
                    entry["until"] = at
            _save_lowered(entries, at)


def _settle(entries: list, config: dict, now: float) -> bool:
    """Close every open entry whose setting records again; True when one did."""
    has_moved = False
    for entry in entries:
        if entry.get("until") is None and _is_back_up(entry, config) is True:
            entry["until"] = now
            has_moved = True
    return has_moved


def load_lowered_now(config: "dict | None" = None) -> list:
    """What the agent lowered for the person and is lowered still, newest first (`_to_public`)."""
    data = _read_config() if config is None else config
    return [_to_public(entry) for entry in reversed(_load_lowered())
            if entry.get("until") is None and _is_in_effect(entry, data) is not False]


def take_untold(mark: str, *, session: "str | None" = None, config: "dict | None" = None) -> list:
    """The lowerings still in effect not yet told at `mark`, marked told now. TOLD_IN_CHAT: only
    the ones `session` made."""
    data = _read_config() if config is None else config
    now = time.time()
    with _make_lowered_lock():
        entries = _load_lowered()
        taken = []
        for entry in entries:
            told = entry.get("told") if isinstance(entry.get("told"), list) else []
            if entry.get("until") is not None or mark in told or _is_in_effect(entry, data) is False:
                continue
            if mark == TOLD_IN_CHAT and (not session or entry.get("session") != session):
                continue
            entry["told"] = told + [mark]
            taken.append(_to_public(entry))
        if taken or _settle(entries, data, now):
            _save_lowered(entries, now)
        return taken


def take_missed_offers(config: "dict | None" = None, now: "float | None" = None) -> list:
    """The stretches that ended since they were last offered (`{"scope", "state", "from", "to"}`,
    epoch seconds), each marked offered: a session start offers to bring their chats in."""
    data = _read_config() if config is None else config
    at = time.time() if now is None else now
    with _make_lowered_lock():
        entries = _load_lowered()
        has_moved = _settle(entries, data, at)
        offers = []
        for entry in entries:
            if entry.get("until") is None or entry.get("offered") is True:
                continue
            entry["offered"] = True
            offers.append({"scope": entry["scope"], "state": entry["state"], "from": entry["since"],
                           "to": _finite(entry["until"]) or at})
        if offers or has_moved:
            _save_lowered(entries, at)
        return offers


def load_missed_window(now: "float | None" = None) -> "tuple[float, float] | None":
    """(from, to): the stretch the lowered settings left chats unrecorded in, every entry kept
    (closed or still open) together; None when there is none."""
    at = time.time() if now is None else now
    entries = _load_lowered()
    if not entries:
        return None
    return (min(entry["since"] for entry in entries),
            max((_finite(entry.get("until")) or at) for entry in entries))
