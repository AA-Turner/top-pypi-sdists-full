# ---------------------------------------------------------------------------
# Is Probe configured on this machine at all
# ---------------------------------------------------------------------------


def config_path() -> Path:
    """Mirrors `probe.sdk.settings.settings` and `_telemetry_core._config_path`."""
    override = os.environ.get("PROBE_CONFIG_PATH")
    if override:
        return Path(override)
    base = os.environ.get("XDG_CONFIG_HOME") or (_home() / ".config")
    return Path(base) / "probe" / "config.json"


def tracking_signal_path(session_id: str) -> Path:
    """Where THE DECISION lives: is this conversation being tracked.

    One file, three readable values -- `on`, `off`, and absent. Absent is not a
    third STATE, it is the absence of a decision, and `is_tracking` resolves it
    from what the session has actually recorded. Two states reach the reader;
    the undecided case just has to pick one of them honestly.

    Per session, beside the marker, because the answer is about THIS
    conversation. A machine-wide switch would decide the next one too.
    """
    return sessions_dir() / (session_id + ".tracking")


def _legacy_off_path(session_id: str) -> Path:
    """The 0.27-0.29 spelling: presence of `<sid>.off` meant "not tracking".

    Read, never written. A researcher who turned tracking off before upgrading
    must not silently come back ON because the file was renamed underneath them
    -- that is precisely the decision the file exists to remember.
    """
    return sessions_dir() / (session_id + ".off")


def tracking_signal(session_id: str) -> str | None:
    """`"on"`, `"off"`, or None when nobody has decided yet.

    THE CANONICAL FILE ANSWERS FIRST, and that is what stops the two files from
    ever disagreeing inside this codebase. `set_session_state` publishes twice --
    `.state`, then the compat `.tracking` -- and two writers interleaving those
    four writes can leave `.state=off` beside `.tracking=on`. Reading `.tracking`
    directly, half the surfaces here (the status-line refresh, the capture check,
    the wizard) would keep recording while the guard refused every write: one
    setting, two answers, and nothing saying which is winning.

    So `.tracking` is a file we WRITE for old clients and do not READ while the
    canonical one exists. A torn pair is then eventually consistent rather than
    contradictory -- the next write repairs it, and until then everything here
    agrees.
    """
    if not valid_session_id(session_id):
        return None
    try:
        raw = state_path(session_id).read_text(encoding="utf-8").strip().lower()
        if raw in STATES:
            return "on" if raw in RECORDING_STATES else "off"
    except OSError:
        pass
    try:
        value = tracking_signal_path(session_id).read_text(encoding="utf-8").strip().lower()
        if value in ("on", "off"):
            return value
    except OSError:
        pass
    return "off" if _legacy_off_path(session_id).is_file() else None


def set_tracking(session_id: str, on: bool) -> bool:
    """Record a BOOLEAN decision. True when it landed.

    THE FALSE BRANCH IS `read-only`, NOT `off`. Every caller of this function
    predates the third state, and what they have always meant by False is what
    `probe session untrack` has always documented: "records nothing further".
    That is `read-only` precisely -- the switch has never gated reads. Routing
    them to the new `off` would take reads away from people who asked only to
    stop recording, which is the same mistake `session_state` refuses to make
    when it migrates a stored marker.

    The hard `off` is reachable only by naming it: `set_session_state(sid,
    STATE_OFF)`, which is what the new switch calls.
    """
    return set_session_state(
        session_id, STATE_FULL if on else STATE_READ_ONLY
    )


def set_tracking_if_absent(session_id: str, on: bool) -> bool:
    """Record the session's STARTING value, ONLY when nobody has decided yet.
    True when THIS call decided.

    The seed half of the toggle. A session starts at the effective default for
    its INITIAL cwd (`resolve_tracking_default(initial_cwd)`) and the file exists
    from SessionStart onward, so "undecided" is not a state any reader has to
    resolve for itself: one setting, one file, always present.

    THE VALUE IS A PARAMETER, never a literal `on`. Seeding `on` on a machine
    whose initial-cwd default is `off` would let automation author a declaration the
    researcher did not make -- the default IS the researcher saying which value
    a new session starts at, and it is the same setting the toggle flips, not a
    weaker kind of preference. A DECISION is never touched either: an existing
    file in either direction, and the legacy `<sid>.off` spelling, all block
    the seed.

    Exclusive by construction, not by check-then-write. The content is written
    to a UNIQUE temp file and PUBLISHED with os.link, which fails with EEXIST
    rather than replacing. A researcher typing the toggle to `off` while the
    first write is in flight keeps their `off`, and a crash between create and
    publish cannot strand a half-written signal: the target either does not
    exist or carries complete content.

    The temp name carries pid AND a nanosecond stamp, and is created O_EXCL.
    Naming it by pid alone lets two THREADS of one process share it, and the
    loser then truncates a file the winner has already published — a reader
    sees an empty marker. `tempfile.mkstemp` would say this in one call and
    costs ~17ms of import (it pulls in shutil/lzma); this module is imported on
    every status-line render, where that is the whole budget. Hence os.open.

    THE LEGACY SPELLING IS RE-CHECKED AFTER PUBLISHING. `os.link` arbitrates
    `<sid>.tracking` only, so an old client writing `<sid>.off` between the read
    and the publish would leave both files on disk with `on` winning the read —
    automation silently overriding an explicit opt-out, which is the one thing
    this must never do. Losing that race is repaired by removing what we just
    published, not by keeping it.
    """
    return set_session_state_if_absent(
        session_id, STATE_FULL if on else STATE_READ_ONLY
    )


def is_tracking(signal: str | None, *, default: bool | None = None) -> bool:
    """The one boolean the whole surface renders. TWO STATES, never three.

    An explicit per-session decision wins in BOTH directions -- that is what
    makes the toggle a toggle, and it is why a researcher who turns tracking off
    stays off no matter what any default says.

    With no decision, this machine's default answers. Since SessionStart seeds
    the signal from that default, a missing file now means only that the seed
    never ran -- a session started before this shipped, or a hook that could
    not write -- so resolving it against the same default is what keeps those
    sessions reading the value the researcher chose rather than a third
    behaviour nobody selected.

    `default=None` reads the machine's setting. Callers that already parsed the
    config pass it in so the render path parses the file once.
    """
    if signal == "off":
        return False
    if signal == "on":
        return True
    return default_tracking() if default is None else default


# ---------------------------------------------------------------------------
# THE THREE-VALUED SWITCH.
#
#   full        reads and writes. What "tracking on" has always meant.
#   read-only   reads allowed, records nothing new. What "tracking off" has
#               always meant -- the switch never gated reads.
#   off         no Probe calls at all, and no session-start injections; and
#               nothing captures the transcript (`probe.service.capture_gate`,
#               and from tap 0.10.19 every `tap watch`: `tap/capture_gate.py`;
#               a `tap watch` still running an older tap uploads it until it
#               ends).
#
#                 /probe
#          full <----------> read-only        off ----------> read-only
#                 /probe                            /probe
#
#   THE BARE SWITCH NEVER LANDS ON `off`. It is thrown without reading
#   anything, and `off` is the one state that costs something invisible: no
#   Probe calls at all, so an agent under it cannot find prior work and cannot
#   know what it missed. Nobody should get there by one press too many. `off`
#   is reached by TYPING it, and one press leaves it for `read-only` -- the
#   smallest change that gives back what it took away. See `_NEXT_STATE`.
#
# TWO FILES, ONE DECISION. `<sid>.state` is canonical and three-valued.
# `<sid>.tracking` keeps being WRITTEN with the two-valued projection and is
# never read by new code. That is not bookkeeping: `tracking_signal` above
# returns its value only when it is exactly "on" or "off", and ANY other answer
# -- an unknown word, or a missing file -- falls through to `default_tracking()`
# -> DEFAULT_TRACKING -> True. So an older client that met a three-valued file,
# or met no file at all after a clean cutover, would resolve an opt-out to
# TRACKING ON and silently record work the researcher declined. The compat write
# is what makes that unsayable, and it is the same trick `<sid>.off` already
# plays in the other direction.
# ---------------------------------------------------------------------------

STATE_FULL = "full"
STATE_READ_ONLY = "read-only"
STATE_OFF = "off"
#: THE STORED FORM OF `on (daemon)`: the session is recorded by the Probe daemon
#: beside it rather than by the agent. The agent still launches runs; the `probe`
#: CLI refuses the rest while the daemon holds the write lease (see
#: `daemon_status`).
#:
#: NOT A SWITCH POSITION (Richard 2026-09-29: "the daemon should only be swappable
#: through the wizard"). Whether the daemon records is the wizard's "Who records"
#: setting (`recorder`); the switch is on / read / off, and `on` in a session the
#: daemon records for is WRITTEN as this value (`on_state`). No typed word reaches
#: it -- `/probe daemon`, `probe session state daemon` and `probe session default
#: daemon` are refused with `DAEMON_SWITCH_REFUSAL`. A stored `daemon` from before
#: (a session, a folder or machine default) still reads, never an error.
#:
#: OLDER CLIENTS READ IT AS `full`. They do not know this word, so they fall
#: through to the compat `<sid>.tracking` file, which projects `daemon` to `on`
#: (`_write_compat_tracking`). That is the safe direction: a half-upgraded
#: machine's agent records as it always has, and the worst case is a duplicate
#: the daemon's read-before-write drops -- never silence.
STATE_DAEMON = "daemon"

#: Every state, in the order any surface that has to OFFER all four lists them.
#: This is NOT the order the bare switch advances through -- see `_NEXT_STATE`,
#: which deliberately leaves `off` off the cycle.
STATES = (STATE_FULL, STATE_DAEMON, STATE_READ_ONLY, STATE_OFF)

#: The states in which this session's work IS recorded -- by the agent (`full`)
#: or by the daemon (`daemon`). Everything that asks "is this session being
#: tracked?" asks this, not "is it `full`?".
RECORDING_STATES = (STATE_FULL, STATE_DAEMON)

#: What a machine that has said nothing gets. `full`, for the same reason
#: DEFAULT_TRACKING is True: tracking must not depend on anyone remembering to
#: ask for it. Shipping `read-only` here would quietly stop recording for
#: everyone on upgrade -- a product change wearing a plumbing change's clothes.
DEFAULT_STATE = STATE_FULL

#: WHAT EACH STATE IS CALLED, which is deliberately not what it is STORED as.
#:
#: `<sid>.state` and `defaults.session_state` are a wire format shared with every
#: OTHER copy of this module on the machine -- a vendored hook, an older plugin,
#: the pi extension's own parser -- and `normalize_state` in those copies cannot
#: know a word this version invented. An unrecognised value there reads as
#: DEFAULT_STATE (see the block above this one), so renaming the stored value
#: would turn somebody's opt-out into recording on exactly the machines that are
#: half-upgraded. The WORDS are ours to change; the bytes are not.
#:
#: Both spellings are accepted on input, forever -- see `normalize_state`.
STATE_LABELS = {
    STATE_FULL: "on",
    STATE_DAEMON: "daemon",
    STATE_READ_ONLY: "read",
    STATE_OFF: "off",
}

#: THE SWITCH: the three positions a person can type or press. `daemon` is not one
#: of them -- see STATE_DAEMON.
SWITCH_STATES = (STATE_FULL, STATE_READ_ONLY, STATE_OFF)

#: The switch's words, for anything that has to offer them.
STATE_WORDS = tuple(STATE_LABELS[state] for state in SWITCH_STATES)

#: What a TYPED `daemon` gets back instead of a state change.
DAEMON_SWITCH_REFUSAL = (
    "Whether the Probe daemon records is set in `probe wizard` (Defaults › Who records), "
    "not by this switch, which is on / read / off. Nothing changed."
)

#: WHAT A PERSON READS for each state when the daemon is the one recording and
#: reading (Richard 2026-09-29). Display only: JSON keeps `state_label`'s words
#: (`daemon` included), because pi's `parseState` and older hooks read them.
DAEMON_STATE_DISPLAY = {
    STATE_DAEMON: "on (daemon)",
    STATE_READ_ONLY: "read only (daemon)",
    STATE_OFF: "off",
}


def state_display(state: "str | None", daemon: bool = False, inline: bool = False) -> str:
    """The state as a person reads it: `on` / `read` / `off`, and in a session the
    daemon records for (`daemon`, see `daemon_session`) `on (daemon)` /
    `read only (daemon)` / `off`. A stored `daemon` always reads `on (daemon)`;
    an inline session (`is_inline`) reads `on (inline)`."""
    if inline and state == STATE_FULL:
        return INLINE_DISPLAY
    if inline and state == STATE_READ_ONLY:
        return "read only (inline)"
    if state == STATE_DAEMON or (daemon and state in DAEMON_STATE_DISPLAY):
        return DAEMON_STATE_DISPLAY[state]
    return state_label(state)


def state_label(state: "str | None") -> str:
    """The word for a state -- what a person types, and what we print back.

    Unknown in, unknown out: a value this module does not recognise is shown as
    it is rather than dressed as a state, because the one thing worse than an
    odd-looking word on screen is a familiar one standing in for it.
    """
    return STATE_LABELS.get(state, str(state))


def state_for_label(word: object) -> "str | None":
    """A word back to the state it names, or None. `normalize_state`, narrowed
    to the vocabulary this version prints -- kept beside it so the two halves of
    the rename cannot drift apart."""
    if not isinstance(word, str):
        return None
    wanted = word.strip().lower()
    return next((state for state, label in STATE_LABELS.items() if label == wanted), None)


def state_path(session_id: str) -> Path:
    """Where the three-valued decision lives. Canonical; see the block above."""
    return sessions_dir() / (session_id + ".state")


def normalize_state(raw: object) -> "str | None":
    """A recognized state name, or None.

    Accepts the spellings a person actually types. `read-only` carries a hyphen,
    and a hyphen is the one character someone reliably gets wrong, so the three
    obvious near-misses resolve rather than reading as unrecognized -- which, per
    `default_session_state`, would mean falling back to `full` and recording work
    somebody tried to decline.
    """
    if not isinstance(raw, str):
        return None
    value = raw.strip().lower()
    # THE CANONICAL NAMES FIRST. They are not all in the legacy synonym tuples
    # -- `full` is in none of them -- and leaning on those alone meant the one
    # spelling this file documents everywhere was the one it rejected.
    if value in STATES:
        return value
    if value in TRACKING_READ_ONLY_VALUES:
        return STATE_READ_ONLY
    if value in TRACKING_OFF_VALUES:
        return STATE_OFF
    if value in TRACKING_ON_VALUES:
        return STATE_FULL
    return None


#: WHERE ONE BARE PRESS LANDS. Not a rotation through `STATES`: `off` is not on
#: the cycle at all, and that asymmetry is the point.
#:
#: The bare switch is the FAST path -- it is pressed without reading anything,
#: often to quiet a session mid-thought. `off` is the expensive state: under it
#: an agent makes no Probe calls, so it cannot find prior work AND cannot know
#: what it missed, and every later answer is silently poorer with no signal that
#: it is. Reaching that by one press too many is a cost the presser never
#: consented to and has no way to notice. A state that damaging has to be
#: TYPED: `/probe off`, and nothing else, puts the switch there.
#:
#: So the cycle oscillates between the two states that both keep reads alive:
#:
#:     on  <-->  read-only          off  -->  read-only  (one way out)
#:
#: `off` still ANSWERS a press, rather than sticking. Someone pressing a switch
#: they have set to off is asking for something to change, and `read-only` is
#: the smallest change that gives them back what off took away. From there the
#: oscillation is ordinary, and returning to `off` means typing it again.
_NEXT_STATE = {
    STATE_FULL: STATE_READ_ONLY,
    STATE_READ_ONLY: STATE_FULL,
    STATE_OFF: STATE_READ_ONLY,
    # `daemon` is off the cycle like `off`: it is reached by typing it, and one
    # press leaves it for `read-only`, the same smallest-change rule.
    STATE_DAEMON: STATE_READ_ONLY,
}


def next_state(state: str) -> str:
    """The state one press of the bare switch lands on.

    An UNRECOGNISED state lands on `full`, which is what every other ambiguity
    in this file resolves to: a corrupted marker must not be a quiet way to stop
    recording somebody's research.
    """
    return _NEXT_STATE.get(state, STATE_FULL)


def state_allows_writes(state: "str | None") -> bool:
    """Is this session's work recorded at all? `full` and `daemon`.

    WHO may write is a second question, answered by the `probe` CLI's write gate
    (`probe.cli.write_gate`): under `daemon` with a live lease the agent's own
    ambient writes are refused and the daemon makes them. Every caller of this
    function asks the first question -- whether to show "tracking", whether to
    inject the read-only notice, whether capture's work counts -- so `daemon`
    answers True here.
    """
    return state in RECORDING_STATES


def state_allows_reads(state: "str | None") -> bool:
    """`full` and `read-only` may look things up. Only `off` may not.

    An UNKNOWN state reads as allowed, deliberately. Everywhere else in this
    file ambiguity resolves toward the shipped posture, and a corrupted marker
    that silently stopped an agent finding prior work would be invisible: it
    looks exactly like the work not existing.
    """
    return state != STATE_OFF


