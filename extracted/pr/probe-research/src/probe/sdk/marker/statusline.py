# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _paint(text: str, code: str, color: bool) -> str:
    """`text` in `code`, closed immediately. The ONLY place an SGR is emitted.

    One function, so "every code opened is closed" is a property of this file
    rather than a habit at four call sites: an unterminated run bleeds into
    whatever the neighbouring status-line segment prints next.
    """
    return code + text + _RESET if color else text


def _elide(slug: str, limit: int = MAX_SLUG_CHARS) -> str:
    if len(slug) <= limit:
        return slug
    return slug[: limit - 1] + _ELLIPSIS


def _name_room(label: str) -> int:
    """Columns left for the project name after `label` and the running accent.

    `MAX_SLUG_CHARS` for the tracking label; a longer label (the daemon's) takes
    its extra columns from the name, never from the ceiling.
    """
    return MAX_SEGMENT_CHARS - len(_INDENT) - _GLYPH_WIDTH - len(label) - len(_ACCENT_TEXT)


def _recording_labels(
    session_state: "str | None", daemon_live: bool, capture_reason: str, inline: bool = False
) -> tuple[str, str]:
    """`(label before a project name, bare label)` for a session that records.

    In the `daemon` state the capture suffix already explains a daemon that is
    not running (the worker is a child of capture), so that line keeps the
    shorter `on (daemon)` and its columns go to the reason. An inline session
    (the researcher's `/probe inline`) reads `on (inline)`.
    """
    if inline and session_state == STATE_FULL:
        return _LABEL_INLINE, _LABEL_INLINE_BARE
    if session_state != STATE_DAEMON:
        return _LABEL_TRACKED, _LABEL_TRACKING_BARE
    if daemon_live or capture_reason:
        return _LABEL_DAEMON, _LABEL_DAEMON_BARE
    return _LABEL_DAEMON_DEGRADED, _LABEL_DAEMON_DEGRADED_BARE


def _no_capture_clause(reason: str, label_bare: str = _LABEL_TRACKING_BARE) -> str:
    """The `· not capturing session transcript: …` suffix, as it hangs off
    `label_bare`.

    THE LAST STOP FOR THE WIDTH CAP. With no project name left to give up, the
    reason itself is elided. The vocabulary in `probe.cli.capture_state` is short
    enough that this never fires today, but this renderer reads whatever a
    refresh hook of ANY vintage wrote into the marker, and an unbounded field on
    a status line wraps the whole line — which reflows every other segment on it.
    """
    if not reason:
        return ""
    room = (
        MAX_SEGMENT_CHARS
        - len(_INDENT)
        - _GLYPH_WIDTH
        - len(label_bare)
        - len(_LABEL_NO_CAPTURE)
    )
    return _LABEL_NO_CAPTURE + _elide(reason, room)


#: WHAT EACH NON-RECORDING STATE IS CALLED HERE, and the colour it is painted.
#:
#: `read-only` is spelled OUT rather than taken from `state_label`. The switch's
#: own word is `read`, which names what the session may still do and not what it
#: may no longer do -- alone on a status line, with no neighbouring word to lean
#: on, `read` is taken for an activity in progress rather than for a restriction.
#: This is not a second vocabulary: `read-only` is the state's canonical STORED
#: name and an accepted spelling everywhere a state is typed, so `/probe read`
#: and this label still name one thing, and `normalize_state` takes either back.
#:
#: The colour is here rather than at the call site so that a state cannot be
#: given a word without also being given a hue -- the two are one decision, and
#: splitting them is how a fourth state ends up yellow by default.
_STATE_SEGMENT = {
    STATE_READ_ONLY: ("read-only", _YELLOW),
    STATE_OFF: ("off", _RED),
}


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
) -> str:
    """The status-line segment. One line, bounded, self-delimiting, or empty.

    In the `daemon` state the label is `on (daemon)` while the daemon holds a
    live lease (`daemon_live`), and `on (daemon degraded)` when it does not.
    `daemon` says the daemon records and reads for this session (`daemon_session`),
    so its `read-only` reads `read only (daemon)`.

    TWO STATES OF THE SWITCH: tracking, or not. The caller resolves which via
    `is_tracking`; this only renders it. An earlier version carried a third —
    "tracking off" as something distinct from "untracked" — and that was a
    mistake. A reader does not care WHY nothing is being recorded, only whether
    anything is, and the third state made them decode a distinction that changed
    nothing they would do.

    `tracked, not capturing session transcript` is a third state of a DIFFERENT
    question, and it earns its place by the same test the rejected one failed: it
    changes what the reader does. The work is landing — projects, runs, metrics,
    artifacts, all of it — and the CONVERSATION is not being recorded. Only the
    researcher can decide whether that matters for this session, and they cannot
    decide it without being told. It renders as a SUFFIX on the tracking segment,
    never as a replacement for it, because a line reading only "not capturing
    session transcript" says the opposite of what is true.

    THE SEGMENT MUST SURVIVE ANY NEIGHBOUR. It shares one line with whatever else
    is chained into `statusLine`, so four properties are load-bearing:

    * **No newline, ever.** Claude Code splits this command's stdout on newlines
      and renders each as its own status row.
    * **A two-space indent and a glyph in front.** Output is concatenated with the
      neighbour's; without the gap `…main● tracking` fuses into one token.
    * **Bounded width.** Overflow wraps the line, reflowing every segment on it —
      the one way this makes other output worse rather than merely longer.
    * **One coloured character, always closed, never counted.** Only the dot is
      painted (`_paint` is the single place an SGR is emitted), and layout is
      computed on PLAIN text — measuring a coloured string counts invisible bytes.

    Empty when Probe is not configured on this machine: someone who does not use
    it should not spend a column being told so.
    """
    if not configured:
        return ""

    if not tracking:
        # THE SWITCH NOW HAS THREE POSITIONS AND TWO OF THEM ARE NOT RECORDING,
        # and the difference is the one thing a reader can act on: under
        # `read-only` an agent will still find prior work, under `off` it will
        # not and will not know what it missed. That passes the same test the
        # rejected third state failed and `not capturing session transcript`
        # passed -- it changes what the reader does.
        #
        # `session_state=None` is a caller from before the third state. It gets
        # the two-state word -- and the two-state colour -- it has always got
        # rather than a guess: yellow, because the one state red is reserved for
        # is the one such a caller cannot tell us it is in.
        label, hue = _STATE_SEGMENT.get(session_state, (_LABEL_NOT_TRACKING, _YELLOW))
        if daemon and session_state == STATE_READ_ONLY:
            # The daemon still reads for this session; it records nothing.
            label = DAEMON_STATE_DISPLAY[STATE_READ_ONLY]
        if inline and session_state == STATE_READ_ONLY:
            label = "read only (inline)"
        return _INDENT + _paint(_DOT, hue, color) + " " + label

    # Read PAST the `not tracking` return above on purpose: capture is a fact
    # about a session that is recording, and naming it for one that is not would
    # be an answer to a question nobody asked.
    reason = _capture_reason(state)
    # Turned off on purpose: nothing is wrong, so the full dot and a plain note.
    chosen_off = reason == _CHOSEN_OFF_REASON
    if chosen_off:
        reason = ""
    head = _INDENT + _paint(_DOT_DEGRADED if reason else _DOT, _GREEN, color) + " "
    label_tracked, label_bare = _recording_labels(session_state, daemon_live, reason, inline)

    project = state.get("project") if isinstance(state, dict) else None
    if not (isinstance(project, str) and project):
        # Tracking is on, nothing filed yet. State it without inventing a name.
        if chosen_off:
            return head + label_bare + _LABEL_TRANSCRIPTS_OFF
        return head + label_bare + _no_capture_clause(reason, label_bare)

    if chosen_off:
        room = _name_room(label_tracked) + len(_ACCENT_TEXT) - len(_LABEL_TRANSCRIPTS_OFF)
        if room >= _MIN_SLUG_CHARS_DEGRADED:
            return head + label_tracked + _elide(project, room) + _LABEL_TRANSCRIPTS_OFF
        return head + label_bare + _LABEL_TRANSCRIPTS_OFF

    if not reason:
        # THE NAME YIELDS, THE LABEL AND ACCENT DO NOT: `MAX_SLUG_CHARS` reserves
        # both widths whether or not the accent shows, so truncation only ever
        # costs characters of the project name.
        accent = _ACCENT_TEXT if live else ""
        return head + label_tracked + _elide(project, _name_room(label_tracked)) + accent

    # DEGRADED — WHAT YIELDS FIRST, AND WHY.
    #
    # The name, and it yields all the way to nothing. The reason is the only
    # actionable thing on the line — it names what to fix — and it is on screen
    # nowhere else; the project name is on the dashboard, in `probe session
    # status`, and usually in the previous turn's own output. `not capturing
    # session transcript: interp…` names nothing to fix, so the reason is the
    # LAST thing cut, and only after the name has been given up entirely
    # (`_no_capture_clause`).
    #
    # The live-run accent goes with the name, and hands the reason back its ten
    # columns. One qualifier per segment stays legible; `· running · not
    # capturing session transcript: halted` reads as a list of unrelated facts,
    # and the accent returns the moment capture is healthy — which is also the
    # moment it is worth reading.
    room = (
        MAX_SEGMENT_CHARS
        - len(_INDENT)
        - _GLYPH_WIDTH
        - len(label_tracked)
        - len(_LABEL_NO_CAPTURE)
        - len(reason)
    )
    if room >= _MIN_SLUG_CHARS_DEGRADED:
        return head + label_tracked + _elide(project, room) + _LABEL_NO_CAPTURE + reason
    return head + label_bare + _no_capture_clause(reason, label_bare)


