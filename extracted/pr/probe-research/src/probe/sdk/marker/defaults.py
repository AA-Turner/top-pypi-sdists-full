#: Ships ON. Tracking is the default posture: a session is tracked unless
#: somebody said otherwise, which is what stops tracking from depending on
#: anyone remembering to ask for it.
DEFAULT_TRACKING = True

#: Where a researcher's own default lives in the config file. TOP LEVEL, never
#: inside a context: `sdk.config.clear_context` replaces a context wholesale
#: (`contexts[name] = {}`, a deliberate fail-closed wipe), so a preference
#: stored there would be erased by signing out and tracking would silently
#: come back on. It would also make the default follow whichever TENANT is
#: selected, which is not what "all my sessions" means.
DEFAULTS_KEY = "defaults"
TRACKING_DEFAULT_KEY = "session_tracking"

#: The THREE-VALUED default, in its own key beside the two-valued one.
#:
#: A separate key, not a widened vocabulary in the old one, and the reason is
#: the same collision the flip claim hit: `session_tracking: "off"` was written
#: when `off` meant "stop recording, keep searching". That is `read-only` now.
#: Reading the new hard `off` out of that key would silently take reads away
#: from every folder and machine already configured -- the exact migration
#: mistake `session_state` refuses to make for a session marker.
#:
#: So writers write BOTH: this key three-valued, the old one as the safe
#: two-valued projection for clients that only know it. Readers prefer this one
#: and fall back to the old one THROUGH the legacy mapping.
STATE_DEFAULT_KEY = "session_state"

#: The spellings `default_tracking` recognizes, exported so the ONE other
#: surface that reasons about the env override (the wizard's settings screen)
#: cannot drift from the parser: a value outside both sets is IGNORED, and a
#: screen that calls it an override anyway misdiagnoses a typo.
TRACKING_OFF_VALUES = ("off", "0", "false", "no", "disabled")
TRACKING_ON_VALUES = ("on", "1", "true", "yes", "enabled")

#: The third set, exported beside the other two so the wizard and the CLI cannot
#: drift from this parser. Five spellings for one state looks generous until you
#: remember the failure mode: an unrecognized value resolves to `full`, so a
#: researcher who typed `readonly` and got recorded anyway would have no way to
#: tell a typo from a bug. `read` leads because it is the word this version
#: PRINTS (STATE_LABELS); the hyphenated spellings are what it is stored as and
#: what earlier versions taught people to type, and both keep working.
TRACKING_READ_ONLY_VALUES = ("read", "read-only", "readonly", "read_only", "ro")

# Folder configs are repository-controlled settings, never data blobs. Their bound
# protects startup/status paths from devices and giant files before JSON parsing can
# fail soft. Machine configs remain size-unbounded for backwards compatibility.


def _parse_tracking_value(value: object) -> bool | None:
    """A recognized stored/env tracking value, or None when it is unknown."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in TRACKING_OFF_VALUES:
            return False
        if normalized in TRACKING_ON_VALUES:
            return True
    return None


def _read_config_text(
    path: Path,
    *,
    require_regular: bool = False,
    max_bytes: int | None = None,
) -> str:
    """Read a machine config normally or a folder config through a validated fd."""
    if not require_regular:
        return path.read_text(encoding="utf-8")

    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_BINARY", 0)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"{path} is not a regular file")
        if max_bytes is not None and info.st_size > max_bytes:
            raise ValueError(f"{path} exceeds the {max_bytes}-byte size limit")
        chunks: list[bytes] = []
        remaining = None if max_bytes is None else max_bytes + 1
        while remaining is None or remaining:
            chunk = os.read(fd, 16 * 1024 if remaining is None else min(16 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            if remaining is not None:
                remaining -= len(chunk)
        raw = b"".join(chunks)
        if max_bytes is not None and len(raw) > max_bytes:
            raise ValueError(f"{path} exceeds the {max_bytes}-byte size limit")
        return raw.decode("utf-8")
    finally:
        os.close(fd)


def _read_config() -> dict:
    """The config file as a dict, or `{}`. ONE parse, two answers.

    `configured()` and `default_tracking()` both need this file, and it is read
    on every status-line render, so parsing it twice would double the only I/O
    on that path. Small enough that the cost is the interpreter, not the file:
    measured at ~0.018ms to open and parse a realistic config.
    """
    try:
        data = json.loads(_read_config_text(config_path()))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def tracking_env_override() -> bool | None:
    """The RECOGNIZED `PROBE_SESSION_TRACKING` value, or None.

    None covers both "unset" and "unrecognized" -- a typo is ignored, never
    read as `off` (see `default_tracking`). Split out so a writer can ask
    "is the env holding this setting down?" without re-implementing the
    parse: while a recognized override is active, toggling the STORED default
    from the effective value writes `not env` into the file invisibly, and
    the stored value can never be set equal to the env's -- the wizard hides
    its toggle row on this answer instead.
    """
    # BOTH VARIABLES, PROJECTED. The three-valued reader has its own
    # `state_env_override`, but half this codebase still asks the boolean
    # question -- the status-line refresh, the capture check, the wizard's
    # settings screen. If `PROBE_SESSION_STATE=off` were invisible here, those
    # surfaces would keep behaving as though the session were recording while
    # the guard refused every write: one setting, two answers, nothing saying
    # which is winning. That is the exact failure this pair of functions exists
    # to prevent, so the projection happens once, here.
    explicit = normalize_state(os.environ.get("PROBE_SESSION_STATE"))
    if explicit is not None:
        return explicit in RECORDING_STATES
    return _parse_tracking_value(os.environ.get("PROBE_SESSION_TRACKING"))


def _tracking_value(data: dict) -> bool | None:
    """The stored default as a BOOLEAN, from whichever key carries it.

    Writers put both keys down, so the old one is normally enough. This reads
    the new one as a fallback for the config somebody edited BY HAND -- setting
    `session_state` alone is the obvious thing to do once it is documented, and
    without this fallback that edit would move the guard and leave the status
    line, the capture check and the wizard reading the shipped default.
    """
    defaults = data.get(DEFAULTS_KEY)
    if not isinstance(defaults, dict):
        return None
    value = _parse_tracking_value(defaults.get(TRACKING_DEFAULT_KEY))
    if value is not None:
        return value
    state = normalize_state(defaults.get(STATE_DEFAULT_KEY))
    return None if state is None else state in RECORDING_STATES


def default_tracking(config: dict | None = None) -> bool:
    """This machine's default for sessions nobody has decided about.

    `PROBE_SESSION_TRACKING` wins, matching the env-beats-file rule the rest of
    the client follows -- but it is an OVERRIDE and never the home for this
    setting. A dock-launched Claude Code sources no shell profile, so a default
    exported from a shell rc applies in a terminal session and not in a
    dock-launched one: the same setting, two answers, which is worse than having
    no setting at all.

    Anything unrecognised reads as the shipped default rather than as `off`. A
    typo in a config file must not silently stop recording someone's research.
    """
    override = tracking_env_override()
    if override is not None:
        return override
    data = _read_config() if config is None else config
    value = _tracking_value(data)
    return DEFAULT_TRACKING if value is None else value


def state_env_override(environ: "dict[str, str] | None" = None) -> "str | None":
    """The RECOGNIZED `PROBE_SESSION_TRACKING` value as a state, or None.

    Same variable as the boolean override, widened. Keeping one variable matters
    more than the tidiness of a second: a machine that exported the old name and
    a machine that exported a new one would disagree about the same setting, and
    nothing would say which was winning.

    `environ`: another environment to read (`harness_launch_environ`), else this
    process's own.
    """
    env = os.environ if environ is None else environ
    explicit = normalize_state(env.get("PROBE_SESSION_STATE"))
    if explicit is not None:
        return explicit
    # The old variable, read as what it meant when it was the only one.
    return _legacy_state_from_tracking(env.get("PROBE_SESSION_TRACKING"))


def _legacy_state_from_tracking(value: object) -> "str | None":
    """A two-valued stored default, read as what it MEANT: on -> full, off -> read-only."""
    parsed = _parse_tracking_value(value)
    if parsed is None:
        return None
    return STATE_FULL if parsed else STATE_READ_ONLY


def _stored_state(defaults: object) -> "str | None":
    """The state a `defaults` block carries, new key first, else the legacy one."""
    if not isinstance(defaults, dict):
        return None
    value = normalize_state(defaults.get(STATE_DEFAULT_KEY))
    if value is not None:
        return value
    return _legacy_state_from_tracking(defaults.get(TRACKING_DEFAULT_KEY))


def default_session_state(config: dict | None = None) -> str:
    """This machine's default state for sessions nobody has decided about.

    Env beats file, matching the rest of the client. Anything UNRECOGNIZED reads
    as DEFAULT_STATE rather than as a quieter state -- the rule `default_tracking`
    already states for recording ("a typo in a config file must not silently stop
    recording someone's research") applied to reads as well, which is where it
    now also bites.
    """
    override = state_env_override()
    if override is not None:
        return override
    data = _read_config() if config is None else config
    value = _stored_state(data.get(DEFAULTS_KEY))
    return DEFAULT_STATE if value is None else value


def _append_config_error(errors: list[str] | None, message: str) -> None:
    if errors is not None and message not in errors:
        errors.append(message)


def resolve_tracking_default(
    cwd: str | os.PathLike[str] | None,
    config: dict | None = None,
    *,
    errors: list[str] | None = None,
) -> tuple[bool, str]:
    """The effective new-session default and its diagnostic source: the
    environment, then the machine file, then shipped. `cwd` is unused since
    folder defaults retired; it stays for the callers that pass it."""
    override = tracking_env_override()
    if override is not None:
        return override, "environment"
    data = _read_config() if config is None else config
    value = default_tracking(data)
    if _tracking_value(data) is None:
        return value, "shipped"
    machine_path = Path(os.path.abspath(os.fspath(config_path())))
    return value, str(machine_path)


def resolve_state_default(
    cwd: str | os.PathLike[str] | None,
    config: dict | None = None,
    *,
    errors: list[str] | None = None,
    environ: "dict[str, str] | None" = None,
) -> tuple[str, str]:
    """The effective new-session STATE and its diagnostic source: the
    environment, then the machine file, then shipped -- the same ladder as
    `resolve_tracking_default`. `cwd` is unused since folder defaults retired.
    `environ`: the environment to read instead of this process's
    (`state_env_override`)."""
    override = state_env_override(environ)
    if override is not None:
        return override, "environment"
    data = _read_config() if config is None else config
    stored = _stored_state(data.get(DEFAULTS_KEY))
    if stored is None:
        return DEFAULT_STATE, "shipped"
    return stored, str(Path(os.path.abspath(os.fspath(config_path()))))


def write_default_tracking(on: bool) -> Path:
    """Persist this machine's session-tracking default; returns the config path.

    TOP LEVEL, never inside a context -- see DEFAULTS_KEY. Written through the
    config module's own primitives, and each one guards a real loss:

    * `_config_lock` -- `save_file` alone is atomic but not isolated, so this
      write racing a sign-in would restore its stale snapshot over the
      fresh token and report success doing it.
    * `load_file(strict=True)` -- the raw file may be a v1 flat blob. A raw
      read-modify-write leaves `defaults` beside the v1 keys, and the NEXT
      canonical write migrates every one of those keys into the context --
      burying the preference where `default_tracking` never looks, so capture
      silently comes back on. The migrating loader lands the file in v2 shape
      with `defaults` at the top level, where it stays. Strict also means an
      unparseable or non-object file RAISES (`ConfigUnreadable`) instead of
      being replaced by just this preference.
    * The empty-file seed matches `save_context`'s, so a fresh config is born
      v2 rather than being mistaken for v1 on its next read.

    Imported lazily: this module renders on the status-line hot path, and
    vendored copies may not ship the writer at all -- reading the default must
    keep working there even though setting it cannot.
    """
    from probe.sdk.config import (  # restructure-guard-ok: released hooks run this copy against older CLIs
        CONFIG_VERSION,
        DEFAULT_CONTEXT,
        _config_lock,
        _load_json_file,
        _save_json_file,
        _write_target,
    )

    path = config_path()
    target = _write_target(path)
    with _config_lock(target, _resolved=True):
        data = _load_json_file(target, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "current_context": DEFAULT_CONTEXT,
            "contexts": {},
        }
        defaults = data.get(DEFAULTS_KEY)
        data[DEFAULTS_KEY] = defaults if isinstance(defaults, dict) else {}
        data[DEFAULTS_KEY][TRACKING_DEFAULT_KEY] = "on" if on else "off"
        # BOTH KEYS, OR THIS WRITE IS A NO-OP. Readers prefer `session_state`,
        # so leaving a stale `full` there while this sets `session_tracking: off`
        # means the wizard reports tracking off and every new session keeps
        # recording. False maps to read-only -- what this boolean has always
        # meant: stop recording, keep searching.
        data[DEFAULTS_KEY][STATE_DEFAULT_KEY] = STATE_FULL if on else STATE_READ_ONLY
        # A change made here is the person's own: it no longer reads as staff's.
        data[DEFAULTS_KEY].pop(DEFAULT_SET_BY_KEY, None)
        _save_json_file(target, data, private=True, _resolved=True)
    return path


def write_default_state(state: str) -> Path:
    """Persist this machine's default STATE; returns the config path.

    The same key, the same file, the same locking as `write_default_tracking` --
    only the vocabulary is wider. One key, because it is one setting: a second
    key would let a machine hold two answers to "what does a new session start
    at" with nothing to say which won.

    An older client reading `read-only` here sees an unrecognized value and falls
    back to the SHIPPED default rather than to off, which is the documented rule
    (`default_tracking`) and the safe direction: a machine whose default is
    read-only records nothing under a new client, and records under an old one.
    That is visible on the dashboard. The reverse -- an old client reading it as
    a hard stop -- would silently lose work.
    """
    if state not in STATES:
        raise ValueError(f"expected one of {STATES}, got {state!r}")
    from probe.sdk.config import (  # restructure-guard-ok: released hooks run this copy against older CLIs
        CONFIG_VERSION,
        DEFAULT_CONTEXT,
        _config_lock,
        _load_json_file,
        _save_json_file,
        _write_target,
    )

    path = config_path()
    target = _write_target(path)
    with _config_lock(target, _resolved=True):
        data = _load_json_file(target, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "current_context": DEFAULT_CONTEXT,
            "contexts": {},
        }
        defaults = data.get(DEFAULTS_KEY)
        data[DEFAULTS_KEY] = defaults if isinstance(defaults, dict) else {}
        data[DEFAULTS_KEY][STATE_DEFAULT_KEY] = state
        # The compat projection, for clients that only know the old key.
        data[DEFAULTS_KEY][TRACKING_DEFAULT_KEY] = "on" if state in RECORDING_STATES else "off"
        # A change made here is the person's own: it no longer reads as staff's.
        data[DEFAULTS_KEY].pop(DEFAULT_SET_BY_KEY, None)
        _save_json_file(target, data, private=True, _resolved=True)
    return path


# ---------------------------------------------------------------------------
# A DEFAULT PROBE STAFF SET (research-os control/074, `probe.cli.remote_settings`)
# ---------------------------------------------------------------------------
#
# Staff may move this machine's default, once, and only toward quieter. The same
# locked write records who did it, beside the default:
#
#     defaults.session_state_set_by = {"by": "probe-staff", "at": "<iso>"}
#
# so `probe session default`, `probe doctor` and the wizard can say so even when
# the command that applied it ran in the background with nobody watching. Any
# local default change (`write_default_state`, `write_default_tracking`) drops it.

DEFAULT_SET_BY_KEY = "session_state_set_by"
SET_BY_STAFF = "probe-staff"

#: Quietness, quietest first: `off` stops capture and Probe calls, `read` stops
#: recording, `on` (stored `full` or `daemon`) records.
_LOUDNESS = {STATE_OFF: 0, STATE_READ_ONLY: 1, STATE_FULL: 2, STATE_DAEMON: 2}


def louder(state: "str | None", than: str) -> bool:
    """Is `state` louder than `than`? An unknown or missing state is not."""
    return state in _LOUDNESS and _LOUDNESS[state] > _LOUDNESS[than]


def lower_default_state(state: str, *, by: str, at: str) -> "tuple[str, bool]":
    """Move this machine's STORED default to `state` only where that is quieter
    than what is stored (nothing stored reads as DEFAULT_STATE), recording `by`
    and `at` beside it; one locked read-then-write, so a change the person makes
    meanwhile is compared against, never overwritten by a louder one. Returns the
    stored state before, and whether it moved. Raises like `write_default_state`
    (an unreadable config file is reported, never replaced)."""
    if state not in (STATE_OFF, STATE_READ_ONLY):
        raise ValueError(f"only off or read-only can be set this way, got {state!r}")
    from probe.sdk.config import (  # restructure-guard-ok: released hooks run this copy against older CLIs
        CONFIG_VERSION,
        DEFAULT_CONTEXT,
        _config_lock,
        _load_json_file,
        _save_json_file,
        _write_target,
    )

    target = _write_target(config_path())
    with _config_lock(target, _resolved=True):
        data = _load_json_file(target, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "current_context": DEFAULT_CONTEXT,
            "contexts": {},
        }
        defaults = data.get(DEFAULTS_KEY)
        before = _stored_state(defaults) or DEFAULT_STATE
        if not louder(before, state):
            return before, False
        data[DEFAULTS_KEY] = defaults if isinstance(defaults, dict) else {}
        data[DEFAULTS_KEY][STATE_DEFAULT_KEY] = state
        data[DEFAULTS_KEY][TRACKING_DEFAULT_KEY] = "off"
        data[DEFAULTS_KEY][DEFAULT_SET_BY_KEY] = {"by": by, "at": at, "value": state}
        _save_json_file(target, data, private=True, _resolved=True)
    return before, True


def default_set_by(config: "dict | None" = None) -> "dict | None":
    """`{"by", "at", "value"}` while the stored default is still the value Probe
    staff set, else None (a writer that does not know this key, an older CLI,
    may have changed the default and left it). Never raises."""
    data = _read_config() if config is None else config
    defaults = data.get(DEFAULTS_KEY) if isinstance(data, dict) else None
    marked = defaults.get(DEFAULT_SET_BY_KEY) if isinstance(defaults, dict) else None
    if not isinstance(marked, dict) or marked.get("by") != SET_BY_STAFF or not isinstance(marked.get("at"), str):
        return None
    if marked.get("value") != _stored_state(defaults):
        return None
    return {"by": marked["by"], "at": marked["at"], "value": marked["value"]}


def set_by_note(config: "dict | None" = None) -> "str | None":
    """`set by Probe staff on <date>` for a default staff set that is the one in
    effect, else None: an environment variable overriding the file is not
    staff's value, so it is never credited to them."""
    if state_env_override() is not None:
        return None
    marked = default_set_by(config)
    return None if marked is None else f"set by Probe staff on {marked['at'][:10]}"


#: The files a session's switch is read from (`session_state`): the canonical one
#: and the two legacy spellings it still migrates.
_STATE_SUFFIXES = (".state", ".tracking", ".off")


def decided_sessions() -> "list[str]":
    """Every session on this machine with a switch decision on disk, newest
    file first. Never raises (an unreadable folder is no sessions)."""
    found: dict[str, float] = {}
    try:
        with os.scandir(sessions_dir()) as listing:
            for entry in listing:
                suffix = next((s for s in _STATE_SUFFIXES if entry.name.endswith(s)), None)
                if suffix is None:
                    continue
                sid = entry.name[: -len(suffix)]
                if not valid_session_id(sid):
                    continue
                try:
                    found[sid] = max(found.get(sid, 0.0), entry.stat().st_mtime)
                except OSError:
                    continue
    except OSError:
        return []
    return sorted(found, key=lambda sid: found[sid], reverse=True)


RECORDERS_KEY = "recorders"
RECORDER_AGENT = "agent"
RECORDER_DAEMON = "daemon"
RECORDERS = (RECORDER_AGENT, RECORDER_DAEMON)


def recorder(source: "str | None", config: "dict | None" = None) -> str:
    """Who records for coding agent `source` (`claude_code`, `codex`, `pi`) on this
    machine: `daemon` only when the config says so, else `agent`. Fail-soft: an
    unreadable or odd config reads as `agent`, today's behaviour."""
    data = _read_config() if config is None else config
    defaults = data.get(DEFAULTS_KEY) if isinstance(data, dict) else None
    table = defaults.get(RECORDERS_KEY) if isinstance(defaults, dict) else None
    value = table.get(source) if isinstance(table, dict) and isinstance(source, str) else None
    return RECORDER_DAEMON if value == RECORDER_DAEMON else RECORDER_AGENT


def write_recorder(source: str, value: str) -> Path:
    """Persist who records for `source`; returns the config path. Same file, lock
    and loader as `write_default_state`. `agent` removes the entry (absent is
    `agent`), so a machine that never chose `daemon` keeps no trace of the key."""
    if value not in RECORDERS:
        raise ValueError(f"expected one of {RECORDERS}, got {value!r}")
    if not isinstance(source, str) or not source:
        raise ValueError("expected a coding agent name")
    from probe.sdk.config import (  # restructure-guard-ok: released hooks run this copy against older CLIs
        CONFIG_VERSION,
        DEFAULT_CONTEXT,
        _config_lock,
        _load_json_file,
        _save_json_file,
        _write_target,
    )

    path = config_path()
    target = _write_target(path)
    with _config_lock(target, _resolved=True):
        data = _load_json_file(target, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "current_context": DEFAULT_CONTEXT,
            "contexts": {},
        }
        defaults = data.get(DEFAULTS_KEY)
        data[DEFAULTS_KEY] = defaults if isinstance(defaults, dict) else {}
        table = data[DEFAULTS_KEY].get(RECORDERS_KEY)
        table = dict(table) if isinstance(table, dict) else {}
        if value == RECORDER_DAEMON:
            table[source] = value
        else:
            table.pop(source, None)
        if table:
            data[DEFAULTS_KEY][RECORDERS_KEY] = table
        else:
            data[DEFAULTS_KEY].pop(RECORDERS_KEY, None)
        _save_json_file(target, data, private=True, _resolved=True)
    return path


#: Images pasted into a prompt upload with the captured session (2026-10-12):
#: on unless this machine turned it off. The capture tap reads the same key
#: (`tap/config.py` `pasted_images_on`) before it uploads one.
PASTED_IMAGES_KEY = "pasted_images"


def pasted_images_on(config: "dict | None" = None) -> bool:
    """True unless this machine turned pasted-image upload off."""
    data = _read_config() if config is None else config
    defaults = data.get(DEFAULTS_KEY) if isinstance(data, dict) else None
    return not (isinstance(defaults, dict) and defaults.get(PASTED_IMAGES_KEY) is False)


def write_pasted_images(on: bool) -> Path:
    """Persist the pasted-image setting; returns the config path. Same file,
    lock and loader as `write_recorder`; on removes the key (absent is on)."""
    from probe.sdk.config import (  # restructure-guard-ok: released hooks run this copy against older CLIs
        CONFIG_VERSION,
        DEFAULT_CONTEXT,
        _config_lock,
        _load_json_file,
        _save_json_file,
        _write_target,
    )

    path = config_path()
    target = _write_target(path)
    with _config_lock(target, _resolved=True):
        data = _load_json_file(target, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "current_context": DEFAULT_CONTEXT,
            "contexts": {},
        }
        defaults = data.get(DEFAULTS_KEY)
        data[DEFAULTS_KEY] = defaults if isinstance(defaults, dict) else {}
        if on:
            data[DEFAULTS_KEY].pop(PASTED_IMAGES_KEY, None)
        else:
            data[DEFAULTS_KEY][PASTED_IMAGES_KEY] = False
        _save_json_file(target, data, private=True, _resolved=True)
    return path


def configured(config: dict | None = None, environ=None) -> bool:
    """Whether this machine has a credential for Probe. Cheap, and fail-soft.

    `_telemetry_core` answers the same question and is vendored alongside this
    file, so loading it would have been the obvious reuse -- and it was, until it
    was measured. It imports `urllib.request` for its own sending, which costs
    ~23ms of interpreter startup, on a path whose entire budget is one status-line
    render. So the question is re-answered here with `json` and `os` and nothing
    else. Reuse is the rule; a hot path is the exception that earns a duplicate,
    and this one is thirteen lines that mirror an interface, not logic.

    Both config shapes, for the reason the core documents: reading only the flat
    v1 shape silently missed every install the wizard had produced.

    `environ`: whose environment holds a token (this process's when None; the Probe service passes
    its caller's, which travels with the request, never its own).
    """
    environ = os.environ if environ is None else environ
    if environ.get("PROBE_TOKEN") or environ.get("PROBE_MCP_TOKEN"):
        return True
    data = _read_config() if config is None else config
    if not data:
        return False
    contexts = data.get("contexts")
    if isinstance(contexts, dict):
        active = contexts.get(data.get("current_context") or "default")
        data = active if isinstance(active, dict) else {}
    return bool(data.get("token") or data.get("mcp_token"))


