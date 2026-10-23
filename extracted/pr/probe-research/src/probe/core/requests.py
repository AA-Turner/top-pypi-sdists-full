"""What a caller asks `probe.core` to do: the Probe service API v1 action params.

One small type per action, built either in Python or from the JSON object a
`python -m probe.core.run <action>` child reads on stdin (`parse`). The words
are the ones the desktop app already sends (`src-tauri/src/wizard.rs`), and
each request maps to exactly the `probe wizard` flags the app passes today
(`probe.core.actions`), so the two paths cannot mean different things.

Parsing is strict: an unknown field, a repeated one, a wrong type or an
unknown word is a usage error, never ignored or guessed at. A misspelt
`"capture": false` that was dropped would turn session capture ON. A request
built in Python is checked the same way (`RequestError` either way).

Stdlib only: `import probe.core` stays light.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from probe._compat import StrEnum


class ActionName(StrEnum):
    """`python -m probe.core.run <action>` (and API v1 `action.run`'s `action`)."""

    CONFIGURE = "configure"
    RECORDER = "recorder"
    LOGOUT = "logout"
    UNINSTALL = "uninstall"
    UPDATE = "update"
    SESSION_DEFAULT = "session_default"
    #: A read, not an action: `probe status --json`'s object (API v1 `status.get`).
    STATUS = "status"
    #: A read, not an action: the installed CLI's version, as a fresh process
    #: imports it (`{"cli_version", "cli_latest"}`). The Probe service asks after
    #: an update, because its own `probe.__version__` is the one it started
    #: with, and (`latest`) before it stops daemon workers for one (D7).
    VERSION = "version"


def _agent_words() -> dict[str, str]:
    """The wizard's exact installable ids and aliases, from its shared registry.

    Keep the existing API v1 enum members (CLAUDE, CODEX, PI) while allowing
    clients to send the canonical ids that `probe status` reports. A new
    installable harness needs no second service-side list.
    """
    from probe.harness import get_registry

    return {
        word.upper(): word
        for harness in get_registry().installable()
        for word in dict.fromkeys((harness.cli_flag, *harness.names))
        if word
    }


Agent = StrEnum("Agent", _agent_words(), module=__name__)


class Recorder(StrEnum):
    """Who records on this machine: `probe wizard --who-records`."""

    AGENT = "agent"
    DAEMON = "daemon"


class SessionState(StrEnum):
    """A new session's default: `probe session default` (never `daemon`)."""

    ON = "on"
    READ = "read"
    OFF = "off"


class RequestError(ValueError):
    """The request was refused before anything ran: a usage error (exit 2)."""


@dataclass(frozen=True)
class ConfigureRequest:
    """Install and configure Probe for these agents, in one browser approval.

    A capability left out (None) is that flag left out of `probe wizard --yes`
    (`setup.resolve_selection`): on a fresh device the wizard's fresh defaults
    (`setup.FRESH_DEFAULTS`, all on), on a configured one what the device
    already has. So a request that does not name capture never turns on a
    capture someone turned off. The desktop app names all four.
    """

    agents: tuple[Agent, ...]
    tracking: bool | None = None
    capture: bool | None = None
    auto_update: bool | None = None
    agent_rules: bool | None = None
    reinstall: bool = False

    def __post_init__(self) -> None:
        agents = tuple(dict.fromkeys(_word(Agent, "agents", agent) for agent in self.agents))
        if not agents:
            raise RequestError("configure needs at least one agent")
        for name in CAPABILITIES:
            value = getattr(self, name)
            # A string is truthy: `"false"` would turn the capability ON.
            if value is not None and type(value) is not bool:
                raise RequestError(f"configure: {name} must be true, false or left out, got {_shown(value)}")
        object.__setattr__(self, "agents", agents)
        if type(self.reinstall) is not bool:
            raise RequestError("configure: reinstall must be true or false")
        if self.reinstall and any(getattr(self, name) is not None for name in CAPABILITIES):
            raise RequestError("configure: reinstall preserves existing settings; leave capability fields out")


@dataclass(frozen=True)
class RecorderRequest:
    """Switch who records, for every coding agent on this machine."""

    who_records: Recorder

    def __post_init__(self) -> None:
        object.__setattr__(self, "who_records", _word(Recorder, "who_records", self.who_records))


@dataclass(frozen=True)
class SessionDefaultRequest:
    """Set the machine's default state for new sessions."""

    state: SessionState

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", _word(SessionState, "state", self.state))


@dataclass(frozen=True)
class StatusRequest:
    """`probe status --json`; `refresh` is its `--refresh`."""

    refresh: bool = False


@dataclass(frozen=True)
class VersionRequest:
    """`version`; `latest`: also ask the release manifest (a network read) for
    the newest CLI, instead of the cached manifest's answer. `refresh`: first
    refresh the CLI's cached manifest as its own refresher does (the Probe
    service's `manifest.refresh`), and say how that went."""

    latest: bool = False
    refresh: bool = False


@dataclass(frozen=True)
class EmptyRequest:
    """logout, uninstall and update take no parameters."""


Request = ConfigureRequest | RecorderRequest | SessionDefaultRequest | StatusRequest | VersionRequest | EmptyRequest

#: A configure request's capabilities: each is true, false or left out.
CAPABILITIES = ("tracking", "capture", "auto_update", "agent_rules")

#: Each action's fields: name -> (JSON type, required). The API v1 `params`.
_FIELDS: dict[ActionName, dict[str, tuple[type, bool]]] = {
    ActionName.CONFIGURE: {
        "agents": (list, True),
        "tracking": (bool, False),
        "capture": (bool, False),
        "auto_update": (bool, False),
        "agent_rules": (bool, False),
        "reinstall": (bool, False),
    },
    ActionName.RECORDER: {"who_records": (str, True)},
    ActionName.SESSION_DEFAULT: {"state": (str, True)},
    ActionName.STATUS: {"refresh": (bool, False)},
    ActionName.VERSION: {"latest": (bool, False), "refresh": (bool, False)},
    ActionName.LOGOUT: {},
    ActionName.UNINSTALL: {},
    ActionName.UPDATE: {},
}


def _words(kind: type[StrEnum]) -> str:
    return ", ".join(member.value for member in kind)


#: How much of a refused value a refusal repeats: the message is an `error`
#: event, and a reader's line has a size limit.
_SHOWN_CHARS = 80


def _cut(text: str) -> str:
    return text if len(text) <= _SHOWN_CHARS else text[: _SHOWN_CHARS - 3] + "..."


def _shown(value: object) -> str:
    return _cut(repr(value) if isinstance(value, str) else json.dumps(value, default=repr))


def action_name(word: str) -> ActionName:
    try:
        return ActionName(word)
    except ValueError:
        raise RequestError(f"unknown action {word!r}; expected one of: {_words(ActionName)}") from None


def _word(kind: type[StrEnum], name: str, value: object) -> StrEnum:
    try:
        return kind(value)
    except ValueError:
        raise RequestError(f"{name} must be one of {_words(kind)}, got {_shown(value)}") from None


def parse(action: ActionName | str, payload: object) -> Request:
    """The request for `action` from its JSON params (an object, already
    decoded). Raises `RequestError` for anything it would have to guess at."""
    name = action_name(str(action))
    if not isinstance(payload, dict):
        raise RequestError(f"{name}: the request must be a JSON object, got {type(payload).__name__}")
    fields = _FIELDS[name]
    unknown = sorted(set(payload) - set(fields))
    if unknown:
        raise RequestError(
            f"{name}: unknown field(s) {_cut(', '.join(unknown))}; it takes: {', '.join(fields) or 'none'}"
        )
    for key, (kind, required) in fields.items():
        if key not in payload:
            if required:
                raise RequestError(f"{name}: {key} is required")
            continue
        value = payload[key]
        # `True` is an int in Python, and 1 is not a boolean in JSON: exact types only.
        if type(value) is not kind:
            raise RequestError(f"{name}: {key} must be a JSON {_json_type(kind)}, got {_shown(value)}")
    if name is ActionName.CONFIGURE:
        agents = payload["agents"]
        if not all(isinstance(agent, str) for agent in agents):
            raise RequestError(f"configure: agents must be words ({_words(Agent)})")
        return ConfigureRequest(
            agents=tuple(_word(Agent, "agents", agent) for agent in agents),
            reinstall=payload.get("reinstall", False),
            **{key: payload[key] for key in CAPABILITIES if key in payload},
        )
    if name is ActionName.RECORDER:
        return RecorderRequest(_word(Recorder, "who_records", payload["who_records"]))
    if name is ActionName.SESSION_DEFAULT:
        return SessionDefaultRequest(_word(SessionState, "state", payload["state"]))
    if name is ActionName.STATUS:
        return StatusRequest(refresh=payload.get("refresh", False))
    if name is ActionName.VERSION:
        return VersionRequest(latest=payload.get("latest", False), refresh=payload.get("refresh", False))
    return EmptyRequest()


def parse_json(action: ActionName | str, text: str) -> Request:
    """`parse` over the text a child read on stdin: empty means `{}`."""
    name = action_name(str(action))
    if not text.strip():
        return parse(name, {})
    try:
        payload = json.loads(text, object_pairs_hook=_object)
    except RequestError as exc:
        raise RequestError(f"{name}: {exc}") from None
    except RecursionError:
        raise RequestError(f"{name}: the request nests deeper than it can be read") from None
    except ValueError as exc:
        raise RequestError(f"{name}: the request is not JSON ({exc})") from None
    return parse(name, payload)


def _object(pairs: list[tuple[str, object]]) -> dict:
    """A JSON object, refusing a key it names twice: `json.loads` would keep the
    last, so `"capture": false, "capture": true` would turn capture on."""
    payload: dict = {}
    for key, value in pairs:
        if key in payload:
            raise RequestError(f"the request names {_shown(key)} twice")
        payload[key] = value
    return payload


def _json_type(kind: type) -> str:
    return {bool: "boolean", str: "string", list: "array"}[kind]
