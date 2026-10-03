"""The agent's reasoning summaries, for the daemon to read (Claude Code and Codex).

Both coding agents write their reasoning to the chat log only as a SUMMARY,
and only when a setting asks for it:

* Claude Code saves each thinking block as an empty string plus an encrypted
  signature unless `showThinkingSummaries` is true in its `settings.json`.
* Codex saves each reasoning item with an empty `summary` unless
  `model_reasoning_summary` in `config.toml` asks for one: on this box its
  default wrote none (2,676 of 2,676 items empty) and `"detailed"` wrote text.

The daemon reads non-empty ones (`daemon/adapters/claude_code.py`, `codex.py`),
so without them it sees what the agent did and said, never why. On a replay
bench whose reasons lived only in thinking, the daemon recorded them in 5 of 7
runs with summaries and 0 of 7 without (2026-09-29).

They are SETTINGS, not plugin fields (see `statusline.py`), so the wizard writes
the one key into each agent's own config with that config's care: Claude's
through the status line's helpers (symlinks followed, one-time backup, atomic
replace keeping the mode), Codex's through `codex_config.write_top_level`
(parsed before and after, mode kept). A file that does not parse is never
rewritten: that would lose everything else in it.

Turning the daemon on for an agent turns its summaries on only where the user
never chose, and remembers the file and the value it replaced in a claim;
leaving the daemon or uninstalling puts back exactly that, in that file, and
only if Probe's value is still there. An explicit choice -- in the agent's own
config or on the wizard's row -- is the user's: the row drops Probe's claim
BEFORE it writes, so the choice survives both.

Headless `claude -p` ignores its setting (it needs `--thinking-display
summarized`), and a session already running keeps what it started with.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from probe._compat import StrEnum
from probe.cli import codex_config, statusline
from probe.sdk import homedir

CLAUDE_CODE = "claude_code"
CODEX = "codex"
def _covered():
    from probe.harness import get_registry

    return tuple(h for h in get_registry().all() if h.reasoning_setting)


#: The coding agents this covers: the registry rows with a reasoning setting
#: (Claude Code's settings.json key, Codex's config.toml key). The readers and
#: writers below know exactly those two files; `_check` refuses anything else.
SOURCES: tuple[str, ...] = tuple(h.id for h in _covered())
LABELS: dict[str, str] = {h.id: h.label for h in _covered()}


def _check(source: str) -> str:
    """A source this module can read and write, or ValueError: never Codex's
    config.toml on another harness's behalf."""
    if source not in (CLAUDE_CODE, CODEX) or source not in SOURCES:
        raise ValueError(f"no reasoning-summaries setting for coding agent {source!r}")
    return source

CLAUDE_KEY = "showThinkingSummaries"
CODEX_KEY = "model_reasoning_summary"
#: What Probe writes for Codex. `concise` also writes text; `detailed` gives
#: the daemon the most reasoning to record.
CODEX_ON = "detailed"
CODEX_OFF = "none"
#: Codex values that write summary text; `auto` (its default) wrote none here.
CODEX_SUMMARIES = frozenset({"concise", "detailed"})
#: Codex's default spelled out: nobody chose, same as the key being absent.
CODEX_DEFAULT = "auto"

HOW_TO_CHANGE = "probe wizard › Defaults › Who records (daemon, enter) › Daemon sees the agent's reasoning"

#: The two write failures an agent's config can raise.
_WRITE_ERRORS = (OSError, codex_config.ConfigError)


class State(StrEnum):
    ON = "on"
    OFF = "off"  # the user chose: off, or a value Probe does not know
    UNSET = "unset"  # the agent's default: no summaries written
    UNREADABLE = "unreadable"  # the file exists but does not parse


class Unparseable(OSError):
    """The settings file exists but does not parse: never rewritten."""


# ---------------------------------------------------------------------------
# Per agent: where the key lives, how it reads, how it is written.
# ---------------------------------------------------------------------------


def settings_path(source: str) -> Path:
    _check(source)
    return statusline.settings_path() if source == CLAUDE_CODE else codex_config.config_path()


def _read_claude(path: Path) -> tuple[State, object, dict | None]:
    """State, raw value and the parsed settings (parsed ONCE; the write reuses them)."""
    if not path.is_file():
        return State.UNSET, None, {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return State.UNREADABLE, None, None
    if not isinstance(parsed, dict):
        return State.UNREADABLE, None, None
    if CLAUDE_KEY not in parsed:
        return State.UNSET, None, parsed
    value = parsed[CLAUDE_KEY]
    # Anything but `true` is a value someone typed: theirs, like Codex's below.
    return (State.ON if value is True else State.OFF), value, parsed


def _read(source: str, path: Path) -> tuple[State, object]:
    _check(source)
    if source == CLAUDE_CODE:
        state, value, _parsed = _read_claude(path)
        return state, value
    readable, value = codex_config.read_top_level(CODEX_KEY, path=path)
    if not readable:
        return State.UNREADABLE, None
    if value is None or value == CODEX_DEFAULT:
        return State.UNSET, value  # `auto` is kept as the value to put back
    if isinstance(value, str) and value in CODEX_SUMMARIES:
        return State.ON, value
    # `none`, or a value Probe does not know (a list, a table): the user's.
    return State.OFF, value


def _write(source: str, path: Path, value: object) -> None:
    """Write the RAW value (None removes the key) into `path`."""
    _check(source)
    if source == CLAUDE_CODE:
        _state, _value, settings = _read_claude(path)
        if settings is None:
            raise Unparseable(f"left {path} alone: it is not a JSON object")
        statusline._backup(path)
        if value is None:
            settings.pop(CLAUDE_KEY, None)
        else:
            settings[CLAUDE_KEY] = value
        statusline._save(path, settings)
        return
    codex_config.write_top_level(CODEX_KEY, value, path=path)


def _on_value(source: str) -> object:
    _check(source)
    return True if source == CLAUDE_CODE else CODEX_ON


def _off_value(source: str) -> object:
    _check(source)
    return False if source == CLAUDE_CODE else CODEX_OFF


def _key(source: str) -> str:
    _check(source)
    return CLAUDE_KEY if source == CLAUDE_CODE else CODEX_KEY


# ---------------------------------------------------------------------------
# The claim: which file Probe turned summaries on in, and what it replaced.
# ---------------------------------------------------------------------------


def _claim_path() -> Path:
    return homedir.state_base() / "probe" / "reasoning-summaries.json"


def _claims() -> dict[str, dict]:
    """`{source: {"path": ..., "previous": ...}}` for each agent Probe turned on.

    A claim that does not parse claims nothing: guessing which agent it meant
    could take away a value the user set themselves, and the cost of the other
    guess is only summaries left on, which the row turns off.
    """
    try:
        data = json.loads(_claim_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    entries = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(entries, dict):
        return {}
    return {
        source: entry for source, entry in entries.items()
        if source in SOURCES and isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }


def _save_claims(claims: dict[str, dict]) -> None:
    path = _claim_path()
    if not claims:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".{os.getpid()}.tmp")
    temporary.write_text(json.dumps({"set_by": "probe", "sources": claims}, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _claim(source: str, path: Path, previous: object) -> None:
    claims = _claims()
    claims[source] = {"key": _key(source), "path": str(path), "previous": previous}
    _save_claims(claims)


def _unclaim(source: str) -> None:
    claims = _claims()
    if claims.pop(source, None) is not None:
        _save_claims(claims)


# ---------------------------------------------------------------------------
# What the wizard, the uninstall and `probe doctor` call.
# ---------------------------------------------------------------------------


def current(source: str) -> State:
    return _read(source, settings_path(source))[0]


def claimed(source: str) -> bool:
    return source in _claims()


def row_on(sources: tuple[str, ...] = SOURCES) -> bool:
    """The wizard row's box: on only when EVERY agent it covers writes summaries."""
    return bool(sources) and all(current(source) is State.ON for source in sources)


def on_for_daemon(source: str) -> list[str]:
    """The daemon now records for `source`: turn its summaries on where the
    user never chose. Returns the lines to show."""
    label = LABELS[source]
    try:
        path = settings_path(source)
        state, previous = _read(source, path)
        if state is State.ON:
            return []
        if state is State.OFF:
            return [
                f"{label}'s reasoning summaries are off in its config ({_key(source)} = {json.dumps(previous, default=str)}),",
                f"  so the daemon will not see why the agent chose what it did. Turn on: {HOW_TO_CHANGE}.",
            ]
        if state is State.UNREADABLE:
            raise Unparseable(f"left {path} alone: it does not parse")
        # The claim FIRST: a claim with no write undoes nothing, but a write with
        # no claim could never be undone.
        _claim(source, path, previous)
        try:
            _write(source, path, _on_value(source))
        except _WRITE_ERRORS:
            _unclaim(source)
            raise
    except _WRITE_ERRORS as exc:
        return [f"! could not turn on {label}'s reasoning summaries: {exc}"]
    return [
        f"{label}'s reasoning summaries → on, so the daemon sees why the agent chose what it did.",
        "  They also show in your terminal and are uploaded with the session. New sessions only;",
        f"  change it: {HOW_TO_CHANGE}.",
    ]


def undo_for_agent(source: str) -> list[str]:
    """The daemon no longer records for `source` (or Probe is uninstalled):
    put back what Probe replaced, only if Probe's value is still there, in the
    file it wrote it in."""
    label = LABELS[source]
    try:
        entry = _claims().get(source)
        if entry is None:
            return []
        path = Path(entry["path"])
        state, value = _read(source, path)
        if state is State.UNREADABLE:
            # Keep the claim: once the file is fixed, a later undo still finds it.
            return [f"! could not read {path}; left {label}'s reasoning summaries as they are."]
        # Only PROBE's value is undone: `concise`, typed by the user since, is theirs.
        ours = value == _on_value(source)
        if ours:
            _write(source, path, entry.get("previous"))
        _unclaim(source)
    except _WRITE_ERRORS as exc:
        return [f"! could not turn {label}'s reasoning summaries back off: {exc}"]
    return [f"{label}'s reasoning summaries → back to {label}'s default."] if ours else []


def set_explicit(on: bool, sources: tuple[str, ...] = SOURCES) -> list[str]:
    """The settings row: the user's own choice, for every agent it covers, kept
    by the daemon switch and by uninstall alike. Each claim goes FIRST, so a
    failed write can never leave a stale claim sitting on the user's choice."""
    lines: list[str] = []
    done: list[str] = []
    for source in sources:
        try:
            _unclaim(source)
            path = settings_path(source)
            # Already where the box says (`concise` is on; an unknown value is
            # off): the user's own spelling stays.
            if _read(source, path)[0] is not (State.ON if on else State.OFF):
                _write(source, path, _on_value(source) if on else _off_value(source))
        except _WRITE_ERRORS as exc:
            lines.append(f"! could not set {LABELS[source]}'s reasoning summaries: {exc}")
            continue
        done.append(LABELS[source])
    if done:
        word = "on" if on else "off"
        lines.insert(0, f"Daemon sees the agent's reasoning → {word} ({', '.join(done)}; new sessions)")
    return lines


def doctor_value(source: str) -> str:
    """The `probe doctor` row's value, where the daemon records for `source`."""
    state = current(source)
    if state is State.ON:
        return f"visible (reasoning summaries on{', set by Probe' if claimed(source) else ''})"
    if state is State.UNREADABLE:
        return f"unknown — {settings_path(source)} does not parse"
    why = f"off in your {LABELS[source]} config" if state is State.OFF else f"{LABELS[source]}'s default"
    return f"hidden — reasoning summaries off ({why}); {HOW_TO_CHANGE}"
