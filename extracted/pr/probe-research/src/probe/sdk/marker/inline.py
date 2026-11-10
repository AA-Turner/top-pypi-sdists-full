# ---------------------------------------------------------------------------
# INLINE: the researcher hands Probe to the agent (Richard 2026-10-06)
# ---------------------------------------------------------------------------
#
# `/probe inline`, typed by the researcher in a daemon-profile session, turns
# the daemon off and lets the agent read and write Probe itself, recording by
# track-work as written. Reachable from any state; any other switch move ends
# it. The researcher moves it: a typed prompt, pi's `/probe` command or
# `probe session state inline` from a terminal -- never a tool call the agent
# can make (the guard ignores `inline` in a Skill call and refuses every switch
# command the agent types). The one automatic exception is a trusted daemon
# model response with HTTP 429/code budget_exhausted (`inline_on_budget`): full
# daemon becomes full inline, while read-only daemon stays read-only inline.
# Replaces the agent-initiated takeover of 10-05.
# In the agent profile `inline` is `on`: the agent already records there.
#
# STORED AS `full` PLUS A MARKER. Every gate already reads `full` as "the agent
# records", and an older copy of this module meeting an unknown state byte would
# read it as recording anyway, so no new byte. The marker `<sid>.inline` is what
# makes a `full` inline: a `full` without one (an older CLI's `track`) is NOT
# inline and opens nothing.
# The researcher's `/probe inline` (`switch_to_inline`) always stores `full`,
# from any state: typed in a read-only session it hands the agent writes too, by
# design (the researcher chose it). Only the budget handoff (`inline_on_budget`)
# keeps a read-only session read-only: it stores `read-only` with `mode` in the
# marker, so every write gate keeps refusing writes there.
#
#     <sid>.inline      {"from": "daemon" | "read-only" | "off", "since": <epoch s>}
#                       (+ "mode": "full" | "read-only", "reason": "budget_exhausted"
#                          for a confirmed quota handoff)
#                       (+ "until" once closed but not yet logged: see below)
#     <sid>.inline-log  one {"since", "until", "from"} line per interval that ended
#
# The daemon skips the events stamped inside those intervals (`inline_intervals`):
# the switch's own times, not the moment a worker noticed.
#
# ORDER, so a reader that takes no lock never sees an inline state that is not
# one: entry writes the marker, then the state; leaving logs the interval, then
# writes the state, then removes the marker. A leave whose log cannot be written
# keeps the marker, closed (`until`), so the stretch is never handed back to the
# daemon. Writers take `_StateLock`.

INLINE_WORD = "inline"
INLINE_SUFFIX = ".inline"
INLINE_LOG_SUFFIX = ".inline-log"
INLINE_SHOWN_SUFFIX = ".inline-shown"
#: The states `/probe inline` is typed from (any; `off` also for no state yet).
INLINE_FROM = (STATE_DAEMON, STATE_READ_ONLY, STATE_OFF)
#: The marker `reason` of a stretch a spent daemon allowance opened (`inline_on_budget`, `_publish_budget_marker`).
BUDGET_INLINE_REASON = "budget_exhausted"
INLINE_DISPLAY = INLINE_STATE_DISPLAY[STATE_FULL]
#: The skills an inline agent records by (the main agent's versions), shipped as
#: plain files in the lean plugin's `inline/` folder (`make sync-daemon-plugin`;
#: never under `skills/`, which would list them); pi names its own package's.
INLINE_SKILL_FILES = ("track-work/SKILL.md", "write-summary/SKILL.md", "edit-notes/SKILL.md")
#: What the agent is told when the researcher switches to inline, and again after
#: a compaction or resume (Richard's approved text, 2026-10-06). Short on purpose:
#: Claude Code saves hook context over ~2 KB to a file, so the skills go by path.
#: `{reads}` is its last sentence, by what this machine's `probe` CLI can do
#: (`inline_notice`).
INLINE_NOTICE = (
    "Probe is `on (inline)` for this conversation: the Probe daemon is off, and you read and "
    "write Probe yourself with the `probe` CLI, recording the work as it happens. Before "
    "recording, read the three skills you record by: {track_work}, {write_summary} and {edit_notes}. "
    "{reads}"
)
#: How an inline agent reads where the CLI has the read bridge (`probe mcp tools|call`,
#: CLI 0.220.0: the hooks' `version_check.INLINE_BRIDGE_MIN_CLI`).
INLINE_READS = (
    "This session has no Probe MCP tools: where a skill names one, run `probe mcp tools` to see "
    "them and `probe mcp call <tool> '<json args>'` to use one."
)
#: ...and where the CLI is older, or its version unknown: the plugin and the CLI
#: update on their own schedules, and naming commands the CLI lacks sends the
#: agent to `No such command`.
INLINE_READS_OLD_CLI = (
    "This session has no Probe MCP tools, and this machine's `probe` CLI is too old to read Probe "
    "here: update it (`npx -y probe-research update --json`)."
)


def inline_path(session_id: str) -> Path:
    return state_path(session_id).with_suffix(INLINE_SUFFIX)


def inline_log_path(session_id: str) -> Path:
    return state_path(session_id).with_suffix(INLINE_LOG_SUFFIX)


def _state_lock_path(session_id: str) -> Path:
    return state_path(session_id).with_suffix(".lock")


class _StateLock:
    """One per-session lock around every state move: a switch re-reads the
    state inside it, so two moves landing the same instant apply one after the
    other. It waits: a move made unlocked after a timeout could be overwritten
    by the very move it waited for. Any process of the same user can still
    write the files directly; this orders Probe's own writers. No flock
    provider (`_fcntl`) or no lock file: unlocked, as every move was before."""

    def __init__(self, session_id: str, path: "Path | None" = None) -> None:
        self.session_id = session_id
        #: Another file to lock instead (one small record of the session's own).
        self.path = path
        self.fd: "int | None" = None

    def __enter__(self) -> "_StateLock":
        module = _fcntl()
        if module is None:
            return self
        try:
            path = self.path or _state_lock_path(self.session_id)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.fd = os.open(str(path), os.O_CREAT | os.O_RDWR, 0o600)
            module.flock(self.fd, module.LOCK_EX)
        except OSError:
            self._close()
        return self

    def __exit__(self, *exc: object) -> None:
        self._close()

    def _close(self) -> None:
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = None


def _finite(value: object) -> "float | None":
    """A finite number, or None: a marker or log line is read as data, and an
    `Infinity` there would hand every event of the session to nobody."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(value) else None


def inline_marker(session_id: str) -> "dict | None":
    """The marker (`{"from", "since"}`, plus `"until"` when closed but not yet
    logged), or None. A malformed one is None."""
    if not valid_session_id(session_id):
        return None
    try:
        data = json.loads(inline_path(session_id).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("from") not in INLINE_FROM:
        return None
    since = _finite(data.get("since"))
    if since is None:
        return None
    marker: dict = {"from": data["from"], "since": since}
    if "mode" in data:
        if data["mode"] not in (STATE_FULL, STATE_READ_ONLY):
            return None
        marker["mode"] = data["mode"]
    if data.get("reason") == BUDGET_INLINE_REASON:
        marker["reason"] = BUDGET_INLINE_REASON
    if "until" in data:
        until = _finite(data.get("until"))
        if until is None or until < since:
            return None
        marker["until"] = until
    return marker


def _open_marker(session_id: str, state: "str | None" = None) -> "dict | None":
    """The marker of the stretch the session is in now, or None: the state is
    the marker's mode (`full` by default), the session is the daemon's or no plugin
    marked it (`seed_inline`'s chat), and the marker is open (no `until`). One read of
    each file; the guard asks before every call."""
    if state is None:
        state = session_state(session_id)
    if state not in (STATE_FULL, STATE_READ_ONLY) or session_profile(session_id) not in (RECORDER_DAEMON, None):
        return None
    marker = inline_marker(session_id)
    return marker if marker is not None and "until" not in marker and marker.get("mode", STATE_FULL) == state else None


def is_inline(session_id: str, state: "str | None" = None) -> bool:
    """Is manual or trusted confirmed-quota inline active? See `_open_marker`."""
    return _open_marker(session_id, state) is not None


def switch_to_inline(session_id: str, now: "float | None" = None, *, is_agent: bool = False,
                     is_directed: bool = False) -> bool:
    """`/probe inline`: the researcher's (a typed prompt, pi's command or a terminal), or with
    `is_agent` the agent's own (`session state inline`: when the person asked, `is_directed`, or the
    chat is in auto, read inside the lock). True when the session is inline (in the agent profile:
    `on`) afterwards. In a daemon-profile session: the marker (`from` the state before, `off` when
    there was none), then `full`; a session already inline stays, though the researcher's move still
    makes the switch theirs (`_hand_switch_to_researcher`). A stretch closed earlier whose log could not be
    written is logged first, or nothing moves: overwriting its marker would hand that stretch back to
    the daemon."""
    if not valid_session_id(session_id):
        return False
    if session_profile(session_id) != RECORDER_DAEMON:
        if is_agent:
            return set_state_by_agent(session_id, STATE_FULL, is_directed=is_directed)[0]
        return set_session_state(session_id, STATE_FULL, now)
    with _StateLock(session_id):
        is_auto = is_auto_chat(session_id)
        if is_agent and not (is_auto or is_directed):
            return False
        moved = _enter_inline_locked(session_id, now)
        if moved and is_agent:
            save_agent_move(session_id, MOVED_TO_INLINE, is_auto=is_auto)
        elif moved:
            _hand_switch_to_researcher(session_id)
    return moved


def _enter_inline_locked(session_id: str, now: "float | None") -> bool:
    """`switch_to_inline`'s move, with the session's `_StateLock` already held."""
    state = session_state(session_id)
    if is_inline(session_id, state) and state == STATE_FULL:
        return True
    stale = inline_marker(session_id)
    if stale is not None and "until" not in stale and is_inline(session_id, state):
        if _close_inline(session_id, stale, now) is not False:
            return False
    if stale is not None and "until" in stale and not _log_inline_interval(session_id, stale, stale["until"]):
        return False
    at = time.time() if now is None else now
    prior = state if state in INLINE_FROM else STATE_OFF
    if not _publish_atomically(inline_path(session_id), json.dumps({"from": prior, "since": at}) + "\n"):
        return False
    if not _set_state_unlocked(session_id, STATE_FULL):
        _remove_inline_marker(session_id)
        return False
    _save_kept_out(session_id, STATE_FULL)
    return True


def seed_inline(session_id: str, default: "str | None" = None, now: "float | None" = None) -> bool:
    """Seed the switch of a chat Probe's hooks never started (open before the install,
    or its hooks never ran) from `default` (the new-chat default when None). True when
    THIS call decided; a decision on disk is never touched.

    Its `on` is `on (inline)` (Richard 2026-11-06): no session-start hook attached a
    daemon worker or told its agent the daemon records, and neither Claude Code nor
    Codex loads a plugin into a chat already open. Stored as the marker, then `full`,
    and NO profile mark: nothing refuses the agent's own `probe` calls, `probe mcp` is
    its read path, and the stretch is logged if the chat ever moves to the daemon.
    `read-only` and `off` are themselves."""
    if not valid_session_id(session_id):
        return False
    if default is None:
        default, where = resolve_state_default(None)
        source = seed_source(where)
    else:
        source = SOURCE_DEFAULT
    if default not in (STATE_FULL, STATE_DAEMON):
        return set_session_state_if_absent(session_id, default, source=source)
    with _StateLock(session_id):
        if session_state(session_id) is not None:
            return False
        if session_profile(session_id) is not None:
            # A plugin did start it and its seed is still landing: the value that seed writes.
            return _seed_started_locked(session_id, seed_state(session_id, default), source)
        stale = inline_marker(session_id)
        if stale is not None and "until" in stale and not _log_inline_interval(session_id, stale, stale["until"]):
            return False  # overwriting it would hand that stretch back to the daemon
        at = time.time() if now is None else now
        if not _publish_atomically(inline_path(session_id), json.dumps({"from": STATE_OFF, "since": at}) + "\n"):
            return set_session_state_if_absent(session_id, STATE_FULL, source=source)
        if set_session_state_if_absent(session_id, STATE_FULL, source=source):
            return True
        _remove_inline_marker(session_id)
        return False


def inline_on_budget(session_id: str, expected_state: str, now: "float | None" = None) -> bool:
    """Trusted daemon handoff after a structured monthly-quota refusal.

    Never a CLI/agent switch door. The worker classifies the refusal first;
    this atomic compare-and-set preserves a concurrent explicit read/off move,
    the configured recorder and machine defaults. Read-only stays read-only.
    """
    if not valid_session_id(session_id) or expected_state not in (STATE_DAEMON, STATE_READ_ONLY):
        return False
    with _StateLock(session_id):
        if session_profile(session_id) != RECORDER_DAEMON or session_state(session_id) != expected_state:
            return False
        if is_inline(session_id, expected_state):
            return True
        stale = inline_marker(session_id)
        if stale is not None and "until" in stale and not _log_inline_interval(session_id, stale, stale["until"]):
            return False
        target = STATE_FULL if expected_state == STATE_DAEMON else STATE_READ_ONLY
        # The handoff is the daemon's, never the person's: an auto chat stays the agent's (`is_auto_chat`).
        was_default = state_source(session_id) == SOURCE_DEFAULT
        move = load_agent_move(session_id)
        if not _publish_budget_marker(session_id, expected_state, target, now):
            return False
        if was_default:  # claimed before the state, as the seed claims it, so no reader sees the move as the person's
            _publish_atomically(state_source_path(session_id), SOURCE_DEFAULT + "\n")
        if not _set_state_unlocked(session_id, target):
            _remove_inline_marker(session_id)
            return False
        if not was_default and move is not None and move["auto"]:
            # The agent's `read` stays its `read`; its daemon `on` is now its chat, inline.
            save_agent_move(session_id, move["state"] if target == expected_state else MOVED_TO_INLINE, is_auto=True)
        return True


def seed_started(session_id: str, default: str, where: str, agent: "str | None" = None) -> bool:
    """Seed a chat Probe's hooks started (the session-start hook, `probe session initialize`): its state from
    `default` by who records (`seed_state`), its source by where that default came from (`seed_source(where)`).
    While the team's daemon allowance is spent a daemon seed starts inline (`get_budget_inline_state`), marker
    first. True when this call seeded it."""
    state = seed_state(session_id, default, agent)
    source = seed_source(where)
    if get_budget_inline_state(session_id, state) is None:
        return set_session_state_if_absent(session_id, state, source=source)
    with _StateLock(session_id):
        return _seed_started_locked(session_id, state, source)


def _seed_started_locked(session_id: str, state: str, source: "str | None") -> bool:
    """`seed_started`'s seed of `state` (already resolved by `seed_state`), the chat's `_StateLock` held: inline
    with the budget marker while the allowance is spent, else as asked."""
    budget = get_budget_inline_state(session_id, state)
    if budget is None:
        return set_session_state_if_absent(session_id, state, source=source)
    if session_state(session_id) is not None:
        return False
    stale = inline_marker(session_id)
    if stale is not None and "until" in stale and not _log_inline_interval(session_id, stale, stale["until"]):
        return False  # overwriting it would hand that stretch back to the daemon
    if not _publish_budget_marker(session_id, state, budget, None):
        return set_session_state_if_absent(session_id, state, source=source)
    if set_session_state_if_absent(session_id, budget, source=source):
        return True
    _remove_inline_marker(session_id)
    return False


def _publish_budget_marker(session_id: str, from_state: str, mode: str, now: "float | None") -> bool:
    """The marker of a stretch the spent allowance opened: `from` the daemon state it replaces, `mode` stored."""
    at = time.time() if now is None else now
    marker = {"from": from_state, "since": at, "mode": mode, "reason": BUDGET_INLINE_REASON}
    return _publish_atomically(inline_path(session_id), json.dumps(marker) + "\n")


# ---------------------------------------------------------------------------
# A SPENT ALLOWANCE, remembered (Richard 2026-11-08)
# ---------------------------------------------------------------------------
# The free team's month refusal (`scope: team_month`, read by the worker's `_quota_inline`) is remembered on the
# machine for an hour, so every daemon move and seed of a daemon-profile chat lands inline at once
# (`get_budget_inline_state`) instead of rediscovering it with a refused call. It only lapses: an answer may come
# from a call admitted before the cap. Keyed by who is signed in (`_get_sign_in_key`: the context, its server and
# a hash of its token), so a refusal another team or another sign-in got steers nothing.
#
#     daemon-budget.json   {"sign_in": <key>, "at": <epoch s>, "until": <epoch s>}

DAEMON_BUDGET_FILENAME = "daemon-budget.json"
#: How long a spent month stays remembered; after it the next daemon move tries the daemon once.
DAEMON_BUDGET_LAPSE_S = 3600.0
#: The refusal scope that is the team's month (`TEAM_MONTH_SCOPE` in app/agents/companion/router.py).
TEAM_MONTH_SCOPE = "team_month"


def get_daemon_budget_path() -> Path:
    return state_dir() / DAEMON_BUDGET_FILENAME


def _get_sign_in_key() -> str:
    """Who is signed in, as the record keys it: the current context's name, server and a hash of its daemon
    credential (`companion_token`, the one a refusal answered; else its token). A new sign-in under the same
    name, or another team, is another key. Read from the config on every side, never the token itself."""
    import hashlib  # noqa: PLC0415 -- only when a record is written or exists, never on the status line's path

    data = _read_config()
    name = str(data.get("current_context") or "default")
    contexts = data.get("contexts")
    context = contexts.get(name) if isinstance(contexts, dict) else None
    context = context if isinstance(context, dict) else {}
    token = str(context.get("companion_token") or context.get("token") or "")
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]
    return f"{name}|{context.get('base_url') or ''}|{digest}"


def save_daemon_budget_spent(now: "float | None" = None) -> bool:
    """Remember the team's month refusal for `DAEMON_BUDGET_LAPSE_S`. True when written."""
    at = time.time() if now is None else now
    record = {"sign_in": _get_sign_in_key(), "at": at, "until": at + DAEMON_BUDGET_LAPSE_S}
    try:
        state_dir().mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    return _publish_atomically(get_daemon_budget_path(), json.dumps(record) + "\n")


def is_daemon_budget_spent(now: "float | None" = None) -> bool:
    """Does a remembered month refusal stand: written for this sign-in, `at <= now < until`, never longer than
    `DAEMON_BUDGET_LAPSE_S`? A missing, unreadable or foreign record is no record (today's behaviour)."""
    try:
        data = json.loads(get_daemon_budget_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(data, dict):
        return False
    at, until = _finite(data.get("at")), _finite(data.get("until"))
    moment = time.time() if now is None else now
    return (at is not None and until is not None and at <= moment < min(until, at + DAEMON_BUDGET_LAPSE_S)
            and data.get("sign_in") == _get_sign_in_key())


def get_budget_inline_state(session_id: str, state: str) -> "str | None":
    """What a move or seed to `state` stores instead while the allowance is spent: `full` for the daemon's
    `on`, `read-only` (inline) for its read, in a daemon-profile chat (`inline_on_budget`'s rule). None: as asked."""
    if state not in (STATE_DAEMON, STATE_READ_ONLY) or session_profile(session_id) != RECORDER_DAEMON:
        return None
    if not is_daemon_budget_spent():
        return None
    return STATE_FULL if state == STATE_DAEMON else STATE_READ_ONLY


def is_budget_inline(session_id: str, state: str) -> bool:
    """Is the chat now inline where a spent allowance put `state` (`get_budget_inline_state`)? The read-back a
    caller checks a move by."""
    marker = inline_marker(session_id)
    return (marker is not None and marker.get("reason") == BUDGET_INLINE_REASON and "until" not in marker
            and marker.get("from") == state and session_state(session_id) == marker.get("mode"))


def _log_replaced_stretch(session_id: str, marker: "dict | None", now: "float | None") -> bool:
    """Before a budget stretch replaces `marker`: log the stretch it holds. True when there was nothing to log or
    its line landed; on False nothing on disk changed (unlike `_close_inline`), so the move can refuse cleanly."""
    if marker is None:
        return True
    if "until" in marker:
        return _log_inline_interval(session_id, marker, marker["until"])
    if session_state(session_id) != marker.get("mode", STATE_FULL):
        return True  # a crashed entry: the marker beside another state claims nothing
    return _log_inline_interval(session_id, marker, now)


def _load_inline_text(session_id: str) -> "str | None":
    """The marker file as written, to put back when a move that replaced it fails; None when there is none."""
    try:
        return inline_path(session_id).read_text(encoding="utf-8")
    except OSError:
        return None


def _restore_inline_text(session_id: str, text: "str | None") -> None:
    """Put back the marker `_load_inline_text` read (remove it when there was none)."""
    if text is None:
        _remove_inline_marker(session_id)
    else:
        _publish_atomically(inline_path(session_id), text)


def _close_inline(session_id: str, marker: "dict | None", now: "float | None") -> "bool | None":
    """Before a switch moves away: log the stretch the session is in, or retry
    one closed earlier. True when the marker must STAY (its interval could not be
    logged: an open one is rewritten closed, so the daemon still skips the
    stretch), False when it can go, None when neither the log nor the closed
    marker could be written (the move must not happen).

    Open means open whatever the profile says now: pi rewrites `<sid>.profile` on
    every start, and a stretch must not lose its log to that."""
    if marker is None:
        return False
    if "until" in marker:
        return not _log_inline_interval(session_id, marker, marker["until"])
    if session_state(session_id) != marker.get("mode", STATE_FULL):
        return False  # a crashed entry: the marker beside another state claims nothing
    if _log_inline_interval(session_id, marker, now):
        return False
    closed = {**marker, "until": time.time() if now is None else now}
    return True if _publish_atomically(inline_path(session_id), json.dumps(closed) + "\n") else None


def _log_inline_interval(session_id: str, marker: dict, now: "float | None") -> bool:
    """Append `{"since", "until", "from"}` to the interval log. True when the
    whole line landed."""
    until = time.time() if now is None else now
    # A leading newline too: a row torn by an earlier short write stays on a line
    # of its own (unreadable, skipped) instead of swallowing this one.
    data = ("\n" + json.dumps({"since": marker["since"], "until": until, "from": marker["from"]}) + "\n").encode("utf-8")
    try:
        fd = os.open(str(inline_log_path(session_id)), os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o600)
        try:
            return os.write(fd, data) == len(data)
        finally:
            os.close(fd)
    except OSError:
        return False


def _remove_inline_marker(session_id: str) -> None:
    try:
        inline_path(session_id).unlink()
    except OSError:
        pass


def inline_intervals(session_id: str) -> "list[tuple[float, float | None]]":
    """Every manual or trusted confirmed-quota inline stretch in this session,
    `(since, until)` in epoch seconds, the open one first with `until` None. The
    daemon leaves the events stamped inside them to the agent.

    The OPEN one is read FIRST: leaving logs the interval before it moves the
    state, so whichever side of a move this read lands on, the stretch is in one
    of the two answers. A marker kept closed (its log failed) counts too."""
    out: "list[tuple[float, float | None]]" = []
    if not valid_session_id(session_id):
        return out
    marker = inline_marker(session_id)
    if marker is not None and "until" not in marker:
        if is_inline(session_id):
            out.append((marker["since"], None))
        else:
            # Not inline (any more): a leave whose log failed closes the marker
            # before it moves the state, so read it again; a logged leave is in
            # the log, read below.
            marker = inline_marker(session_id)
            if marker is not None and "until" in marker:
                out.append((marker["since"], marker["until"]))
    elif marker is not None:
        out.append((marker["since"], marker["until"]))
    try:
        lines = inline_log_path(session_id).read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        since = _finite(row.get("since")) if isinstance(row, dict) else None
        until = _finite(row.get("until")) if isinstance(row, dict) else None
        if since is not None and until is not None and since <= until:
            out.append((since, until))
    return out


def inline_notice(
    track_work: "str | Path", write_summary: "str | Path", edit_notes: "str | Path", *, bridge: bool,
    read_only: bool = False, budget: bool = False,
) -> str:
    """`INLINE_NOTICE` naming the skill files the agent records by, in
    `INLINE_SKILL_FILES` order; `bridge`:
    this machine's CLI has `probe mcp tools|call` (`INLINE_READS`), else it is
    too old to read Probe inline (`INLINE_READS_OLD_CLI`)."""
    reads = INLINE_READS if bridge else INLINE_READS_OLD_CLI
    prefix = ALLOWANCE_SPENT + " Probe switched to inline automatically. " if budget else ""
    if read_only:
        return prefix + ("Probe is `read only (inline)` for this conversation: the daemon is off, and you read "
                         "Probe yourself. Record nothing new; the researcher's read-only choice stays in effect. " + reads)
    return prefix + INLINE_NOTICE.format(
        track_work=track_work, write_summary=write_summary, edit_notes=edit_notes, reads=reads
    )


def _inline_shown_path(session_id: str) -> Path:
    return state_path(session_id).with_suffix(INLINE_SHOWN_SUFFIX)


def inline_notice_due(session_id: str) -> "float | None":
    """The stretch's `since` when the session is inline and the agent has not
    been told about THIS stretch, else None. Once per stretch, so a researcher's
    switch from a terminal or pi reaches the agent at its next chance."""
    marker = _open_marker(session_id)
    if marker is None:
        return None
    try:
        shown = float(_inline_shown_path(session_id).read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        shown = None
    # Compared as numbers: pi's extension writes this file too, in its own spelling.
    return None if shown == marker["since"] else marker["since"]


def mark_inline_shown(session_id: str, since: float) -> None:
    """Best effort: the agent was told about the stretch that began at `since`."""
    _publish_atomically(_inline_shown_path(session_id), repr(since) + "\n")


def forget_inline_shown(session_id: str) -> None:
    """A compaction or resume took the notice, and the skills sent after it,
    out of the agent's context: the next chance tells it again."""
    for path in (_inline_shown_path(session_id), _inline_skills_path(session_id)):
        try:
            path.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# THE SKILLS, WHOLE (notes parity N1, 2026-10-28)
# ---------------------------------------------------------------------------
#
# The daemon's writer reads the three skills it records by whole in every run
# (`daemon/bite.py` SHARED_SKILLS); an inline agent was only told where they
# are, and one read track-work and never edit-notes. So an inline agent gets
# the same text the daemon's loader renders for a main agent
# (`bite.skills_text(SHARED_SKILLS, reader="main-agent")`), from the plugin's
# `inline/` copies. Claude Code saves hook context over 10,000 characters to a
# file and shows 2,000 of it, and Codex any over ~2,500 tokens, so it goes in
# parts of at most INLINE_SKILLS_PART_CHARS, one per hook event that reaches the
# model, from the inline notice on. `<sid>.inline-skills` holds
# `{"since": <the stretch's since>, "next": <part>, "of": <parts>}`; a new stretch, a
# compaction or a resume starts again at part 1 (`forget_inline_shown`).
# Never in `read only (inline)`: the skills are how to record.

INLINE_SKILLS_SUFFIX = ".inline-skills"
INLINE_SKILLS_PART_CHARS = 7_000
INLINE_SKILLS_PART = "Probe skills you record by (part {n} of {of}{more}):\n\n{text}"


def _inline_skills_path(session_id: str) -> Path:
    return state_path(session_id).with_suffix(INLINE_SKILLS_SUFFIX)


def _skill_body(text: str) -> str:
    """A SKILL.md without its front matter (`skill_versions.split_front_matter`)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            cut = text.find("\n", end + 1)
            text = text[cut + 1:] if cut >= 0 else ""
    return text.strip()


def inline_skills_text(root: "str | Path") -> str:
    """The skills in INLINE_SKILL_FILES under `root`, as the daemon's loader
    joins them (`bite.skills_text`); "" when none can be read."""
    out = []
    for name in INLINE_SKILL_FILES:
        try:
            text = (Path(root) / name).read_text(encoding="utf-8")
        except OSError:
            continue
        out.append(f"# Skill: {name.split('/', 1)[0]}\n\n{_skill_body(text)}")
    return "\n\n".join(out)


def split_parts(text: str, limit: int = INLINE_SKILLS_PART_CHARS) -> "list[str]":
    """`text` in pieces of at most `limit` characters that join back into it,
    cut before a heading where one fits, else at a blank line, else at a line."""
    parts: "list[str]" = []
    while len(text) > limit:
        window = text[: limit + 1]
        cut = max(window.rfind("\n#"), 0) or max(window.rfind("\n\n"), 0) or max(window.rfind("\n"), 0)
        if cut <= limit // 4:
            cut = max(window.rfind("\n\n"), window.rfind("\n"))
        cut = cut + 1 if cut > 0 else limit
        parts.append(text[:cut])
        text = text[cut:]
    if text:
        parts.append(text)
    return parts


def next_inline_skills_part(session_id: str, root: "str | Path") -> "str | None":
    """The next part of the skills for a full inline session (`is_inline`, not
    read-only), wrapped in INLINE_SKILLS_PART, and marked sent; None when every
    part went or there is none."""
    marker = _open_marker(session_id)
    if marker is None or marker.get("mode", STATE_FULL) != STATE_FULL:
        return None
    path = _inline_skills_path(session_id)
    # Locked: parallel tool calls each run this hook, and both reading part 2
    # as next would send it twice.
    with _StateLock(session_id, path.with_suffix(INLINE_SKILLS_SUFFIX + "-lock")):
        try:
            sent = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            sent = {}
        if not (isinstance(sent, dict) and sent.get("since") == marker["since"]):
            sent = {}
        index, total = sent.get("next"), sent.get("of")
        index = index if isinstance(index, int) and not isinstance(index, bool) and index >= 0 else 0
        if isinstance(total, int) and index >= total:
            return None  # all sent: the skill files are not read again
        parts = split_parts(inline_skills_text(root))
        if index >= len(parts):
            return None
        if not _publish_atomically(path, json.dumps({"since": marker["since"], "next": index + 1,
                                                     "of": len(parts)}) + "\n"):
            return None
    more = ", the rest comes with your next steps" if index + 1 < len(parts) else ""
    return INLINE_SKILLS_PART.format(n=index + 1, of=len(parts), more=more, text=parts[index].strip("\n"))


