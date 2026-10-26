"""The model and reasoning effort each folder-import agent runs at, per lane.

A folder import runs the researcher's OWN Claude Code or Codex, on their
subscription. Left alone, it runs at whatever that agent is configured for -- a
personal `model_reasoning_effort = "xhigh"` in `~/.codex/config.toml` included,
which is how one team's imports burned through their plan (2026-10-25). So the
server can say what each lane runs at, and this module decides it ONCE per
import process, field by field, first hit wins:

    env      PROBE_IMPORT_AGENT_SETTINGS              this machine; same JSON shape
    server   GET /v1/import-jobs/agent-settings       the team's map over the fleet's
    builtin  BUILTIN                                  today's values, nothing more

The shape is `{agent: {lane: {"model": ..., "effort": ...}}}`: an agent is a
`backfill.Agent` value with an `EFFORTS` list, a lane is `classify`, `import`,
`draft`, or `*` for every lane of that agent (a named lane wins over it, field
by field, within one source).

NO ANSWER IS TODAY'S ARGV, byte for byte. BUILTIN holds only what the lanes
already sent before this module existed (Claude drafts on sonnet), so a server
that times out, answers 404 (a self-hosted API without the route) or sends
nothing leaves every launch exactly as it was. The server is never required: a
failed read is the builtin answer, never a failed import.

EACH FIELD STANDS ALONE. A model that is not a `backfill.MODEL_NAME` or an
effort not on the agent's `backfill.EFFORTS` is dropped and counted
(`settings_dropped`); the rest of the map is kept. A bad value in the
researcher's own env var is also said in the import's report.

`Meter` counts what the lanes' agents cost (`launch_agent`) and goes out on
`backfill.summary` (the foreground import) and `import_job.finished` (each
background worker attempt) as per-lane properties. Metadata only: model and
effort names, counts and token sums, never a path or an error's text.
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass

from probe._compat import StrEnum

from .backfill import EFFORTS, MODEL_NAME, USAGE_FIELDS, Agent


class Lane(StrEnum):
    """Where in an import an agent runs. The settings and the meter are keyed by it."""

    #: Classification: the single-shot pass, the survey/name/assign slices of a
    #: large folder, and a reviewer's revision.
    CLASSIFY = "classify"
    #: One unit's notes over its files.
    IMPORT = "import"
    #: One project's reconstruction draft.
    DRAFT = "draft"


class Source(StrEnum):
    """Where a lane's settings came from: the highest source that set any field."""

    ENV = "env"
    SERVER = "server"
    BUILTIN = "builtin"


ENV_VAR = "PROBE_IMPORT_AGENT_SETTINGS"
ROUTE = "/v1/import-jobs/agent-settings"
#: The whole read, retries included. An import waits this long at most for its
#: settings, once, before falling back to the builtin answer.
READ_TIMEOUT_S = 5.0
#: The lane key that means "every lane of this agent".
EVERY_LANE = "*"
_FIELDS = ("model", "effort")

#: Today's values and nothing else -- see the module docstring. Cross-document
#: reconstruction needs more reasoning than the agent's default for a Claude
#: user on a small model (the acceptance fixture exposed reversed ordering and
#: lost qualifiers), so Claude drafts on sonnet. Classification and units send
#: no model: they run as the researcher configured their agent.
BUILTIN: dict[Agent, dict[Lane, dict[str, str]]] = {
    Agent.CLAUDE: {Lane.DRAFT: {"model": "sonnet"}},
}


@dataclass(frozen=True)
class LaneSettings:
    """What one lane's launches carry, and what they fall back to."""

    lane: Lane
    model: str | None = None
    effort: str | None = None
    source: Source = Source.BUILTIN
    #: The lane's BUILTIN values: what a launch runs with when the agent refuses
    #: an override (`backfill.launch_agent`).
    builtin_model: str | None = None
    builtin_effort: str | None = None

    def fallback(self) -> LaneSettings:
        return LaneSettings(
            self.lane, self.builtin_model, self.builtin_effort, Source.BUILTIN,
            self.builtin_model, self.builtin_effort,
        )


@dataclass(frozen=True)
class AgentSettings:
    """One import process's settings for its agent, every lane resolved, and the
    meter its launches count into."""

    agent: Agent
    lanes: dict[Lane, LaneSettings]
    meter: Meter
    #: The server map's version (`settings_version`), or None when it did not answer.
    version: str | None = None
    #: Lines for the import's report: the researcher's own env setting, ignored.
    notes: tuple[str, ...] = ()
    #: Fields dropped from this agent's env and server maps, every lane.
    dropped: int = 0

    def lane(self, lane: Lane) -> LaneSettings:
        return self.lanes[lane]

    def flags(self) -> tuple[str, ...]:
        """The optional flags these settings make some launch send, so
        `degraded_note` can say when this binary would drop one."""
        model = any(settings.model for settings in self.lanes.values())
        effort = any(settings.effort for settings in self.lanes.values())
        effort_flag = "--config" if self.agent is Agent.CODEX else "--effort"
        return (*(("--model",) if model else ()), *((effort_flag,) if effort else ()))


def lane_settings(agents: AgentSettings | None, agent: Agent, lane: Lane) -> LaneSettings:
    """`agents`' settings for `lane`, or the lane's BUILTIN ones without any."""
    if agents is not None:
        return agents.lane(lane)
    own = BUILTIN.get(agent, {}).get(lane, {})
    model, effort = own.get("model"), own.get("effort")
    return LaneSettings(lane, model, effort, Source.BUILTIN, model, effort)


def launch_kwargs(agents: AgentSettings | None, lane: Lane) -> dict:
    """`launch_agent`'s settings and meter for one lane, or nothing at all: a
    caller with no settings launches exactly as before they existed."""
    return {} if agents is None else {"settings": agents.lane(lane), "meter": agents.meter}


def cached(agents: AgentSettings | None, lane: Lane) -> None:
    """One pass answered from the prep cache, launching nothing."""
    if agents is not None:
        agents.meter.cached(lane)


class Meter:
    """What one import process's (or worker attempt's) agents cost, per lane.

    Thread-safe: units and classification slices launch from worker threads.
    A launch with no usage event (killed, timed out, refused) is counted in
    `usage_missing` and adds nothing to the token sums -- never a 0 that would
    make an aborted import read as free. The token sums are only reported for a
    lane where at least one launch reported usage.
    """

    _COUNTS = ("launches", "rejected", "cached", "usage_missing", "metered")

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counts = {lane: dict.fromkeys(self._COUNTS, 0) for lane in Lane}
        self._tokens = {lane: dict.fromkeys(USAGE_FIELDS, 0) for lane in Lane}
        #: Set by `resolve`, once: the settings these counts ran under.
        self.settings: AgentSettings | None = None

    def launched(self, lane: Lane, usage: dict | None) -> None:
        with self._lock:
            counts = self._counts[lane]
            counts["launches"] += 1
            if usage is None:
                counts["usage_missing"] += 1
                return
            counts["metered"] += 1
            for name in USAGE_FIELDS:
                self._tokens[lane][name] += int(usage.get(name) or 0)

    def rejected(self, lane: Lane) -> None:
        with self._lock:
            self._counts[lane]["rejected"] += 1

    def cached(self, lane: Lane) -> None:
        with self._lock:
            self._counts[lane]["cached"] += 1

    def properties(self) -> dict:
        """The per-lane telemetry properties; {} when nothing was resolved or run.

        `<lane>_model`, `<lane>_effort`, `<lane>_source` (the settings), then
        `<lane>_launches`, `<lane>_rejected`, `<lane>_cached`,
        `<lane>_usage_missing` and the five `<lane>_<USAGE_FIELDS>` sums, plus
        `backfill_agent`, `settings_version` and `settings_dropped`.
        """
        with self._lock:
            counts = {lane: dict(values) for lane, values in self._counts.items()}
            tokens = {lane: dict(values) for lane, values in self._tokens.items()}
        settings = self.settings
        if settings is None and not any(
            counts[lane]["launches"] or counts[lane]["cached"] for lane in Lane
        ):
            return {}
        props: dict = {}
        if settings is not None:
            props.update(
                backfill_agent=settings.agent.value,
                settings_version=settings.version,
                settings_dropped=settings.dropped,
            )
        for lane in Lane:
            if settings is not None:
                chosen = settings.lane(lane)
                props.update({
                    f"{lane}_model": chosen.model,
                    f"{lane}_effort": chosen.effort,
                    f"{lane}_source": chosen.source.value,
                })
            props.update({
                f"{lane}_{name}": counts[lane][name]
                for name in ("launches", "rejected", "cached", "usage_missing")
            })
            if counts[lane]["metered"]:
                props.update({f"{lane}_{name}": tokens[lane][name] for name in USAGE_FIELDS})
        return props


def _read_server(client) -> tuple[dict, str | None]:
    """The server's map and version, or `({}, None)` on ANY failure.

    Bounded by one deadline over every attempt (`deadline_scope`), so a slow or
    unreachable API costs an import at most `READ_TIMEOUT_S`. A 404 is a
    self-hosted API without the route; it raises like any other failure.
    """
    try:
        from ..sdk.transport import deadline_scope

        with deadline_scope(time.monotonic() + READ_TIMEOUT_S):
            body = client.transport.get(ROUTE)
    except Exception:
        return {}, None
    if not isinstance(body, dict) or not isinstance(body.get("settings"), dict):
        return {}, None
    version = body.get("version")
    return body["settings"], version if isinstance(version, str) else None


def _read_env(raw: str | None, notes: list[str]) -> dict:
    if not raw or not raw.strip():
        return {}
    try:
        value = json.loads(raw)
    except ValueError:
        value = None
    if not isinstance(value, dict):
        notes.append(f"{ENV_VAR} is not a JSON object, so this import ignores it.")
        return {}
    return value


def _valid(agent: Agent, name: str, value) -> bool:
    if name == "model":
        return isinstance(value, str) and MODEL_NAME.fullmatch(value) is not None
    return isinstance(value, str) and value in EFFORTS.get(agent, ())


def _lanes(raw, agent: Agent) -> tuple[dict[str, dict[str, str]], list[str]]:
    """One source's map for `agent`: `{lane or "*": {field: value}}` holding only
    what this agent can take, and the dotted names of everything dropped."""
    if raw is None:
        return {}, []
    if not isinstance(raw, dict):
        return {}, [agent.value]
    kept: dict[str, dict[str, str]] = {}
    dropped: list[str] = []
    lanes = {lane.value for lane in Lane} | {EVERY_LANE}
    for lane, fields in raw.items():
        if lane not in lanes or not isinstance(fields, dict):
            dropped.append(f"{agent.value}.{lane}")
            continue
        for name, value in fields.items():
            if name in _FIELDS and _valid(agent, name, value):
                kept.setdefault(lane, {})[name] = value
            else:
                dropped.append(f"{agent.value}.{lane}.{name}")
    return kept, dropped


def resolve(client, agent: Agent, *, meter: Meter | None = None, environ=None) -> AgentSettings:
    """`agent`'s settings for every lane: env over server over builtin, per field.

    Once per process: a `meter` that already holds settings for this agent (a
    background worker re-entering its job inside one attempt) answers again
    without another read. Never raises.
    """
    meter = meter if meter is not None else Meter()
    if meter.settings is not None and meter.settings.agent is agent:
        return meter.settings
    environ = os.environ if environ is None else environ
    notes: list[str] = []
    env_map = _read_env(environ.get(ENV_VAR), notes)
    server_map, version = _read_server(client)
    env, env_dropped = _lanes(env_map.get(agent.value), agent)
    server, server_dropped = _lanes(server_map.get(agent.value), agent)
    if env_dropped:
        notes.append(
            f"{ENV_VAR}: ignored {', '.join(env_dropped)} (an unknown lane or field, "
            "a model name an agent cannot take, or an effort this agent does not accept)."
        )
    builtin = {lane.value: fields for lane, fields in BUILTIN.get(agent, {}).items()}
    sources = ((Source.ENV, env), (Source.SERVER, server), (Source.BUILTIN, builtin))
    lanes: dict[Lane, LaneSettings] = {}
    for lane in Lane:
        picked: dict[str, tuple[str, Source]] = {}
        for source, layer in sources:
            for key in (lane.value, EVERY_LANE):
                for name, value in layer.get(key, {}).items():
                    picked.setdefault(name, (value, source))
        given = [source for _, source in picked.values()]
        own = builtin.get(lane.value, {})
        lanes[lane] = LaneSettings(
            lane,
            model=picked.get("model", (None,))[0],
            effort=picked.get("effort", (None,))[0],
            source=min(given, key=list(Source).index) if given else Source.BUILTIN,
            builtin_model=own.get("model"),
            builtin_effort=own.get("effort"),
        )
    settings = AgentSettings(
        agent, lanes, meter, version=version, notes=tuple(notes),
        dropped=len(env_dropped) + len(server_dropped),
    )
    meter.settings = settings
    return settings
