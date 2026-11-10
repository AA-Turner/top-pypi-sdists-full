# ---------------------------------------------------------------------------
# Rendering: `  ● <state words> | <title> | <note>` (Richard 2026-11-07; no `Probe |` prefix, 11-08). Off is
# `  ● off` alone with a red dot (11-08); a failure line is `  ● <failure>` with a red dot (the failure names Probe).
# One line, bounded by MAX_SEGMENT_CHARS terminal columns.
# ---------------------------------------------------------------------------


class Reader(enum.Enum):
    """Who reads and records for a chat right now: the daemon, or the agent itself (inline)."""

    DAEMON = "daemon"
    INLINE = "inline"


def _paint(text: str, code: str, should_paint: bool) -> str:
    """`text` in `code`, closed at once. The ONLY place the renderer emits an SGR."""
    return code + text + _RESET if should_paint else text


#: Characters that never start a cluster of their own: combining marks, ZWJ, the emoji variation selector and the
#: skin-tone modifiers attach to the character before them. ZWJ and VS16 are `_TITLE_ALLOWED_CF` (marker.py).
_JOINERS = _TITLE_ALLOWED_CF
_ZWJ = "\u200d"
_VS16 = "\ufe0f"


def _is_joined_to_previous(ch: str, previous: str) -> bool:
    if ch in _JOINERS or previous == _ZWJ or unicodedata.category(ch) in ("Mn", "Me"):
        return True
    return 0x1F3FB <= ord(ch) <= 0x1F3FF  # skin-tone modifier


def _is_regional(ch: str) -> bool:
    return 0x1F1E6 <= ord(ch) <= 0x1F1FF


def _split_clusters(text: str) -> "list[str]":
    """`text` cut into visible characters: a base and what joins it, or a flag's two regional indicators."""
    out: "list[str]" = []
    for ch in text:
        if out and (_is_joined_to_previous(ch, out[-1][-1])
                    or (_is_regional(ch) and len(out[-1]) == 1 and _is_regional(out[-1]))):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def _get_cluster_width(cluster: str) -> int:
    """Terminal columns for one visible character. When unsure it counts more, never fewer: a ZWJ sequence counts
    each emoji in it (terminals that do not join them draw them all)."""
    width = 0
    for ch in cluster:
        if ch in _JOINERS or unicodedata.category(ch) in ("Mn", "Me", "Cf") or 0x1F3FB <= ord(ch) <= 0x1F3FF:
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return max(width, 2) if _VS16 in cluster else width


def get_text_width(text: str) -> int:
    """Terminal columns `text` takes (status-line text: no control characters)."""
    return sum(_get_cluster_width(c) for c in _split_clusters(text))


def _elide(text: str, limit: int = MAX_TITLE_CHARS) -> str:
    """`text` cut to `limit` columns with an ellipsis, only between visible characters."""
    if get_text_width(text) <= limit:
        return text
    kept, width = "", 0
    for cluster in _split_clusters(text):
        step = _get_cluster_width(cluster)
        if width + step + 1 > limit:
            break
        kept, width = kept + cluster, width + step
    return kept + _ELLIPSIS


def get_state_words(session_state: "str | None", reader: Reader, *, is_manual: bool = False) -> str:
    """The state as the status line says it: `on (daemon)`, `on (inline)`, `read (daemon)`, `read (inline)`, or `off`.
    `is_manual` (the person sets this chat's switch, not the agent) puts the manual tag inside the parentheses
    (`on (daemon, manual)`, `off (manual)`); an auto chat has no tag (Richard, 2026-11-08). A word this copy does
    not know raises, so a newer CLI's state renders as `status unavailable`, never as a guess."""
    if session_state == STATE_OFF:
        return "off (manual)" if is_manual else "off"
    if session_state in (STATE_DAEMON, STATE_FULL):
        who = "daemon" if session_state == STATE_DAEMON and reader is Reader.DAEMON else "inline"
        level = "on"
    elif session_state == STATE_READ_ONLY:
        who, level = reader.value, "read"
    else:
        raise ValueError(f"unknown session_state {session_state!r}")
    return f"{level} ({who}, manual)" if is_manual else f"{level} ({who})"


def _get_reader(session_state: str, is_daemon: bool, is_inline: bool) -> Reader:
    if is_inline:
        return Reader.INLINE
    if session_state == STATE_DAEMON or (session_state == STATE_READ_ONLY and is_daemon):
        return Reader.DAEMON
    return Reader.INLINE


def _get_line_title(state: "dict | None") -> str:
    """The line's title: the project's title, else its slug, else nothing. A `|` is drawn as `/`."""
    if not isinstance(state, dict):
        return ""
    for key in ("project_title", "project"):
        value = state.get(key)
        if is_printable_title(value):
            return value.replace("|", "/")
    return ""


def _pick_note(*, recording: bool, reader: Reader, session_state: str, reason: str, daemon_live: bool,
               lowered: str) -> "tuple[str, str]":
    """`(note, its reason)`: the one note the line carries, most serious first. Read chats show only a lowering."""
    words = lowered[len(STATUS_PREFIX):] if lowered.startswith(STATUS_PREFIX) else lowered
    words = _elide(words.replace("\n", " "), _MAX_LOWERED_CHARS) if words else ""
    if not recording:
        return (words, "") if words else ("", "")
    chosen_off = reason == _CHOSEN_OFF_REASON
    if reason and not chosen_off:
        return NOTE_TRANSCRIPT_NOT_RECORDED, reason
    if session_state == STATE_DAEMON and reader is Reader.DAEMON and not daemon_live and not chosen_off:
        return NOTE_DAEMON_NOT_RECORDING, ""
    if words:
        return words, ""
    if chosen_off:
        return NOTE_TRANSCRIPTS_OFF, ""
    return "", ""


def _fit_fields(words: str, hue: str, title: str, note: str, reason: str, should_paint: bool, ceiling: int) -> str:
    """Lay the fields out under `ceiling` columns: the title yields first (cut, then dropped below
    `_MIN_TITLE_CHARS`), the note last. The capture reason rides on the note only when no title shows."""
    head = _INDENT + _paint(_DOT, hue, should_paint) + " " + words
    head_width = len(_INDENT) + _GLYPH_WIDTH + len(words)
    note_room = ceiling - head_width - len(STATUS_DIVIDER)
    if note:
        note = _elide(note, note_room)
    note_width = len(STATUS_DIVIDER) + get_text_width(note) if note else 0
    if title:
        room = min(ceiling - head_width - note_width - len(STATUS_DIVIDER), MAX_TITLE_CHARS)
        title = _elide(title, room) if room >= _MIN_TITLE_CHARS else ""
    if note and reason and not title:
        note = _elide(note + ": " + reason.replace("\n", " "), note_room)
    line = head + (STATUS_DIVIDER + title if title else "")
    return line + (STATUS_DIVIDER + _paint(note, _YELLOW, should_paint) if note else "")


def render(
    state: dict | None,
    *,
    configured: bool,
    tracking: bool,
    live: bool = False,
    color: bool = True,
    session_state: "str | None" = None,
    daemon_live: bool = False,
    daemon: bool = False,
    inline: bool = False,
    lowered: str = "",
    is_manual: bool = False,
) -> str:
    """The status-line segment, or `""` when Probe is not set up. An off chat draws `● off` alone with a red dot: no
    title and no note, not even the agent's lowering (Richard, 2026-11-08).

    `daemon_live`: the daemon holds a live lease or is still starting (the caller decides; `is_worker_starting`).
    `daemon`: the daemon reads for this chat now (`is_daemon_mode`); `inline` (`is_inline`) wins over it.
    `lowered`: a machine-wide lowering the agent made (`get_lowered_status_word`), shown as the note.
    `is_manual`: the person sets this chat's switch (not `is_auto_chat`), so the words say `manual`.
    `live` is accepted for older callers and ignored: a running run is not a problem, so it has no note.
    """
    if not configured:
        return ""
    if session_state is None:  # a caller from before the five states
        session_state = STATE_FULL if tracking else STATE_READ_ONLY
    if session_state == STATE_OFF:
        words = get_state_words(STATE_OFF, Reader.INLINE, is_manual=is_manual)
        return _fit_fields(words, _RED, "", "", "", color, MAX_SEGMENT_CHARS)
    recording = tracking and session_state != STATE_READ_ONLY
    shown = session_state if recording else STATE_READ_ONLY
    reader = _get_reader(shown, daemon, inline)
    words = get_state_words(shown, reader, is_manual=is_manual)
    note, reason = _pick_note(recording=recording, reader=reader, session_state=shown,
                              reason=_capture_reason(state), daemon_live=daemon_live, lowered=lowered)
    ceiling = MAX_SEGMENT_CHARS + (len(", manual") if is_manual else 0)
    return _fit_fields(words, _GREEN if recording else _YELLOW, _get_line_title(state), note, reason, color, ceiling)


def render_failure(note: str, *, should_paint: bool = True) -> str:
    """A line for Probe itself being broken: `  ● <note>` with a red dot, the status alone (the note names Probe)."""
    return (_INDENT + _paint(_DOT, _RED, should_paint) + " "
            + note.replace("\n", " "))


def render_signed_out(*, should_paint: bool = True) -> str:
    """The line where nothing is signed in because the agent signed the person out (PR B)."""
    return render_failure(NOTE_SIGNED_OUT, should_paint=should_paint)


def get_lowered_status_word(config: "dict | None" = None) -> str:
    """The newest machine-wide lowering's status words (`load_lowered_now`), else ""."""
    for entry in load_lowered_now(config):
        if entry["scope"] != SCOPE_SIGN_IN and entry.get("status"):
            return entry["status"]
    return ""
