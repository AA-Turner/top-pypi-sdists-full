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
import re
from dataclasses import dataclass, field

from probe._compat import StrEnum
from probe.sdk.workspace_limit import TeamItems


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
    #: A read, not an action: one diagnostic report to the Probe team
    #: (`probe.core.report`), `{"sent", "id", "skipped", "path"}` back. The
    #: Probe service asks it when something it watches misbehaves.
    REPORT = "report"
    #: Not an action either: one desktop management request (the JSON object
    #: `probe desktop request --json` reads) in, its v1 envelope out (API v1
    #: `desktop.request`). `probe.cli.desktop` reads and checks the request
    #: itself, so it never goes through `parse`.
    DESKTOP = "desktop"
    #: Limit what Probe on this computer reads to one workspace, or lift the
    #: limit: `probe workspace limit` (`probe.cli.workspace_limit_cmd`).
    WORKSPACE_LIMIT = "workspace_limit"
    #: A read in form, though it approves: Probe's own hooks in Codex, as an
    #: update does (`probe.cli.codex_hooks.heal`), `{"outcome", "approved",
    #: "error"}` back. The Probe service's healer asks it when Codex rewrote
    #: its copies of Probe's plugins (`probe.service.codextrust`, #3617).
    CODEX_TRUST = "codex_trust"


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
class WorkspaceLimitRequest:
    """`probe workspace limit <workspace> [--team-items ...]`, or `--team` (workspace
    None). `workspace`: an id, `id:<uuid>`, a slug or a name. `team_items` goes with
    a workspace only; left out it keeps the current choice (show for a new limit)."""

    workspace: str | None
    team_items: TeamItems | None = None

    def __post_init__(self) -> None:
        if self.workspace is not None and (not isinstance(self.workspace, str) or not self.workspace.strip()):
            raise RequestError(f"workspace_limit: workspace must be a workspace id, slug or name, or null; "
                               f"got {_shown(self.workspace)}")
        if self.team_items is not None:
            object.__setattr__(self, "team_items", _word(TeamItems, "team_items", self.team_items))
            if self.workspace is None:
                raise RequestError("workspace_limit: team_items goes with a workspace; null shows the whole team")


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


#: `report`'s `family` and `reason`: the server's slug rule.
_SLUG = re.compile(r"^[a-z0-9_:.-]{1,64}$")
_SESSION_ID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
#: `report`'s `facts`, serialized, at most (the contract's cap).
REPORT_FACTS_MAX_BYTES = 64 * 1024


@dataclass(frozen=True)
class ReportRequest:
    """`report`: one diagnostic report to the Probe team (`probe.core.report`).

    `auto` false is a manual report (`probe doctor --send`): no consent gate, no
    dedupe. `sid` names the session a session-family report is about (null for
    a machine family). `env` is the consenting environment an automatic report
    is gated on (`report_policy`): the session's own variables, REQUIRED for an
    automatic session report (left out, `{}` would read as consent), or left
    out / `{}` for a machine family whose consent the service already decided.
    `facts` is what the service saw (counters, last exits, a traceback), at
    most 64 KiB."""

    family: str
    reason: str
    auto: bool = True
    sid: str | None = None
    env: dict | None = None
    facts: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("family", "reason"):
            value = getattr(self, name)
            if not isinstance(value, str) or not _SLUG.match(value):
                raise RequestError(f"report: {name} must match {_SLUG.pattern}, got {_shown(value)}")
        if type(self.auto) is not bool:
            raise RequestError("report: auto must be true or false")
        if self.sid is not None and (not isinstance(self.sid, str) or not _SESSION_ID.match(self.sid)):
            raise RequestError(f"report: sid must be a session UUID or null, got {_shown(self.sid)}")
        if self.env is None:
            if self.auto and self.sid is not None:
                raise RequestError("report: an automatic session report needs that session's env (its consent)")
            object.__setattr__(self, "env", {})
        if not isinstance(self.env, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in self.env.items()
        ):
            raise RequestError("report: env must be an object of strings")
        if not isinstance(self.facts, dict):
            raise RequestError("report: facts must be an object")
        try:
            size = len(json.dumps(self.facts, ensure_ascii=False).encode("utf-8"))
        except (TypeError, ValueError):
            raise RequestError("report: facts must be JSON") from None
        if size > REPORT_FACTS_MAX_BYTES:
            raise RequestError(f"report: facts is {size} bytes; at most {REPORT_FACTS_MAX_BYTES}")


@dataclass(frozen=True)
class EmptyRequest:
    """logout, uninstall and update take no parameters."""


Request = (
    ConfigureRequest | RecorderRequest | SessionDefaultRequest | StatusRequest | VersionRequest | ReportRequest
    | WorkspaceLimitRequest | EmptyRequest
)

#: A configure request's capabilities: each is true, false or left out.
CAPABILITIES = ("tracking", "capture", "auto_update", "agent_rules")

#: Each action's fields: name -> (JSON type(s), required). The API v1 `params`.
_FIELDS: dict[ActionName, dict[str, tuple[type | tuple[type, ...], bool]]] = {
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
    ActionName.REPORT: {
        "auto": (bool, False),
        "family": (str, True),
        "reason": (str, True),
        "sid": ((str, type(None)), False),
        "env": (dict, False),
        "facts": (dict, False),
    },
    ActionName.WORKSPACE_LIMIT: {"workspace": ((str, type(None)), True), "team_items": (str, False)},
    ActionName.LOGOUT: {},
    ActionName.UNINSTALL: {},
    ActionName.UPDATE: {},
    ActionName.CODEX_TRUST: {},
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
    if name not in _FIELDS:
        raise RequestError(f"{name}: its request is read by `probe.cli.desktop`, never parsed here")
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
        kinds = kind if isinstance(kind, tuple) else (kind,)
        if type(value) not in kinds:
            wanted = " or ".join(_json_type(each) for each in kinds)
            raise RequestError(f"{name}: {key} must be a JSON {wanted}, got {_shown(value)}")
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
    if name is ActionName.REPORT:
        return ReportRequest(
            family=payload["family"],
            reason=payload["reason"],
            auto=payload.get("auto", True),
            sid=payload.get("sid"),
            env=payload.get("env"),
            facts=payload.get("facts", {}),
        )
    if name is ActionName.WORKSPACE_LIMIT:
        return WorkspaceLimitRequest(workspace=payload["workspace"], team_items=payload.get("team_items"))
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
    return {bool: "boolean", str: "string", list: "array", dict: "object", type(None): "null"}[kind]
