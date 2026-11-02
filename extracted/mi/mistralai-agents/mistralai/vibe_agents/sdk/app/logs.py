"""A deployed agent's runtime logs, for `agents logs`.

The Runtime API serves a managed worker's stdout and stderr by its Mistral Cloud service id. A user knows
the agent's name, so the name is resolved to the agent, and the agent to its service, first. A served
agent has no service: its logs are in the terminal that runs `agents serve`.
"""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import AsyncIterator
from datetime import datetime, timedelta
from enum import IntEnum

import httpx
from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError

from mistralai.vibe_agents._http import _InternalHTTPClient
from mistralai.vibe_agents.agents_client import AgentsClient

from . import config, runtime_logs
from .runtime_logs import LogEntry, LogOrder, LogsResponse, terminal_safe

# The Runtime API's largest page.
MAX_LINES = 1000
_FOLLOW_INTERVAL_SECONDS = 2.0


class LogsError(Exception):
    pass


class LogRetentionError(LogsError):
    """The agent's logs start before the organization's log retention window, so the Runtime API refuses to read them.

    The Runtime API reads from the service's creation by default, and refuses the whole read when that is
    older than the retention window, instead of returning the lines it still keeps.
    """


class Level(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class LogLine(BaseModel):
    """One log line, with what could be read from its own format.

    A worker logs in several formats at once: the Workflows SDK as JSON, structlog to a console, the
    Temporal core as Rust `tracing` lines, and Python itself as plain warnings and tracebacks. A line
    whose format is not recognised keeps its whole text as ``message`` and has no level.
    """

    model_config = ConfigDict(frozen=True)

    created_at: datetime | None
    stream: str | None
    text: str
    level: Level | None = None
    logger: str | None = None
    message: str = ""
    fields: dict[str, JsonValue] = {}
    detail: str | None = None

    @property
    def is_platform(self) -> bool:
        """A line the platform logged about the instance, not one the worker printed."""
        return self.stream == "koyeb"

    def to_record(self) -> dict[str, JsonValue]:
        return {
            "time": self.created_at.isoformat() if self.created_at else None,
            "stream": self.stream,
            "level": self.level.name.lower() if self.level else None,
            "logger": self.logger,
            "message": self.message,
            "fields": self.fields,
            "detail": self.detail,
        }

    @property
    def is_continuation(self) -> bool:
        """An indented line, such as a traceback frame: it belongs to the line before it."""
        return self.level is None and self.text[:1].isspace()


def parse_level(name: str) -> Level | None:
    return _LEVEL_NAMES.get(name.strip().lower())


_LEVEL_NAMES = {
    "trace": Level.DEBUG,
    "debug": Level.DEBUG,
    "info": Level.INFO,
    "warn": Level.WARNING,
    "warning": Level.WARNING,
    "error": Level.ERROR,
    "exception": Level.ERROR,
    "critical": Level.CRITICAL,
    "fatal": Level.CRITICAL,
}
# Rust `tracing`, as the Temporal core prints it: `2026-10-21T12:00:24.513600Z ERROR target::path: message`.
_TRACING_LINE = re.compile(
    r"^\d{4}-\d\d-\d\dT[\d:.]+Z?\s+(?P<level>TRACE|DEBUG|INFO|WARN|ERROR)\s+(?P<logger>[\w:.-]+):\s?(?P<message>.*)$"
)
# structlog's console renderer: `2026-10-19 12:51:57 [warning  ] message key=value`.
_CONSOLE_LINE = re.compile(r"^\d{4}-\d\d-\d\d[ T][\d:.]+\s+\[(?P<level>[a-z]+)\s*\]\s+(?P<message>.*)$")
# What Python prints itself: `path.py:5: SomeWarning: text`, `ValueError: text`, a traceback's first line.
_PYTHON_PROBLEM = re.compile(r"^(?:\S+:\d+: )?(?P<kind>[A-Z]\w*(?:Warning|Error|Exception)): ")
_TRACEBACK_START = "Traceback (most recent call last)"
# A JSON record's multi-line detail, printed under its line rather than squeezed into it.
_DETAIL_KEYS = ("exception", "exc_info", "stack", "stack_info", "traceback")
# Keys a JSON record spends on where it came from, or that the line already shows elsewhere.
_JSON_META_KEYS = frozenset(
    {"event", "message", "msg", "level", "levelname", "logger", "logger_name", "name", "timestamp", "time"}
    | {"lineno", "pathname", "filename", "func_name", "funcName", "module", "process", "thread", "thread_name"}
)


class LogSource(BaseModel):
    """Where an agent's logs are read from."""

    model_config = ConfigDict(frozen=True)

    agent_name: str
    service_id: str
    # Kept out of repr: a traceback or a debug print of the source must not show the key.
    api_key: str = Field(repr=False)
    logs_url: str


async def resolve(agent_name: str) -> LogSource:
    """Find the managed deployment behind the named agent, with the environment's control plane and API key."""
    try:
        settings = config.load_deploy_settings()
    except config.SettingsError as exc:
        raise LogsError(str(exc)) from exc
    return await resolve_source(
        agent_name=agent_name,
        api_key=settings.api_key,
        server_url=settings.deploy_control_plane_url,
        logs_url=settings.deploy_runtime_logs_url,
    )


async def resolve_source(
    *,
    agent_name: str,
    api_key: str,
    server_url: str,
    logs_url: str,
    transport: httpx.AsyncBaseTransport | None = None,
) -> LogSource:
    async with AgentsClient(base_url=server_url, api_key=api_key, transport=transport) as client:
        try:
            agent = await client.get_agent_by_name(agent_name)
            # Decided on the by-name answer: the detail route below does not return `source`, and a built-in
            # outside this workspace is not found there at all.
            if agent.source == "builtin":
                raise LogsError(f"Agent {agent_name} is a built-in agent; its logs are not available.")
            if agent.managed:
                # Only the detail route by id carries the service; the by-name lookup does not.
                agent = await client.get_agent(agent.agent_id)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == httpx.codes.NOT_FOUND:
                raise LogsError(f"No agent named {agent_name} in this workspace.") from exc
            # The body is the server's: strip escapes and newlines so it cannot drive the terminal or fake CLI lines.
            detail = terminal_safe(exc.response.text).strip()
            message = f"Failed to look up agent {agent_name} (HTTP {exc.response.status_code})"
            raise LogsError(f"{message}: {detail}" if detail else message) from exc
        # A 200 whose body is not JSON raises JSONDecodeError, a ValueError, from response.json().
        except (httpx.HTTPError, ValidationError, json.JSONDecodeError) as exc:
            raise LogsError(f"Failed to look up agent {agent_name}: {terminal_safe(str(exc))}") from exc

    if not agent.managed:
        raise LogsError(
            f"Agent {agent_name} is served, not deployed: its logs are in the terminal that runs `agents serve`."
        )
    if agent.service_id is None:
        raise LogsError(f"Agent {agent_name} has no managed deployment yet. Check `agents list`.")
    return LogSource(agent_name=agent.agent_name, service_id=agent.service_id, api_key=api_key, logs_url=logs_url)


async def read(source: LogSource, *, lines: int, transport: httpx.AsyncBaseTransport | None = None) -> list[LogLine]:
    """The last ``lines`` lines, oldest first."""
    async with _client(source, transport) as client:
        newest_first = await _page(client, source, order="desc", limit=min(lines, MAX_LINES))
    return [_line(entry) for entry in reversed(newest_first.logs)]


async def follow(
    source: LogSource,
    *,
    lines: int,
    interval_seconds: float = _FOLLOW_INTERVAL_SECONDS,
    transport: httpx.AsyncBaseTransport | None = None,
) -> AsyncIterator[LogLine]:
    """The last ``lines`` lines, then every new line as it is written, until cancelled.

    Each poll reads forward from the Runtime API's own ``next_start`` cursor, which it shifts past the last
    entry it returned, so no entry is read twice and entries sharing a timestamp are not skipped.
    """
    async with _client(source, transport) as client:
        newest_first = await _page(client, source, order="desc", limit=min(lines, MAX_LINES))
        entries = list(reversed(newest_first.logs))
        for entry in entries:
            yield _line(entry)
        start = _after_last(entries)
        while True:
            await asyncio.sleep(interval_seconds)
            while True:
                page = await _page(client, source, order="asc", limit=MAX_LINES, start=start)
                for entry in page.logs:
                    yield _line(entry)
                if page.next_start is not None:
                    start = page.next_start
                elif page.logs:
                    start = _after_last(page.logs) or start
                # A page with more behind it is read at once; otherwise wait for new lines.
                if not page.has_more:
                    break


def _after_last(oldest_first: list[LogEntry]) -> str | None:
    """Where to read on after the initial lines, which came newest first and carry no forward cursor.

    One microsecond past the newest one, as the Runtime API shifts its own cursors, so that line is not
    read again. None when no line has a time, which reads the window from the start.
    """
    stamps = [entry.created_at for entry in oldest_first if entry.created_at is not None]
    if not stamps:
        return None
    return (max(stamps) + timedelta(microseconds=1)).isoformat()


def logs_command(source: LogSource) -> str:
    """The equivalent request, for when the CLI could not make it."""
    return runtime_logs.logs_command(source.logs_url, source.service_id)


def _line(entry: LogEntry) -> LogLine:
    return parse_line(text=terminal_safe(entry.msg).rstrip(), created_at=entry.created_at, stream=entry.stream)


def _terminal_safe_json(value: JsonValue) -> JsonValue:
    # Newlines go too: a message or field printed on one line must not be able to forge a line under it.
    if isinstance(value, str):
        return terminal_safe(value)
    if isinstance(value, list):
        return [_terminal_safe_json(item) for item in value]
    if isinstance(value, dict):
        return {terminal_safe(key): _terminal_safe_json(item) for key, item in value.items()}
    return value


def parse_line(*, text: str, created_at: datetime | None, stream: str | None) -> LogLine:
    """Read the level, logger, message and fields out of one line, whichever format it is in."""
    plain = LogLine(created_at=created_at, stream=stream, text=text, message=text)
    if text.startswith("{"):
        try:
            record = json.loads(text)
        except ValueError:
            return plain
        if not isinstance(record, dict):
            return plain
        # The line was made terminal-safe as text, but JSON can spell an escape as `\u001b`, which decoding
        # turns back into a real one. Clean every decoded string, keys and nested values included.
        # Only a traceback keeps its newlines: it is printed as a block under the line, which is its place.
        record = {
            terminal_safe(key): (
                terminal_safe(value, keep_newlines=True)
                if key in _DETAIL_KEYS and isinstance(value, str)
                else _terminal_safe_json(value)
            )
            for key, value in record.items()
        }
        message = record.get("event", record.get("message", record.get("msg")))
        level = record.get("level", record.get("levelname"))
        logger = record.get("logger", record.get("logger_name", record.get("name")))
        details = [record[key] for key in _DETAIL_KEYS if isinstance(record.get(key), str) and record[key].strip()]
        return plain.model_copy(
            update={
                "message": message if isinstance(message, str) else text,
                "level": parse_level(level) if isinstance(level, str) else None,
                "logger": logger if isinstance(logger, str) else None,
                "fields": {
                    key: value
                    for key, value in record.items()
                    if key not in _JSON_META_KEYS and not (key in _DETAIL_KEYS and isinstance(value, str))
                },
                # Already terminal-safe: the record was cleaned above, its traceback keys with their newlines.
                "detail": "\n".join(details).rstrip() if details else None,
            }
        )
    if match := _TRACING_LINE.match(text):
        return plain.model_copy(
            update={
                "level": parse_level(match["level"]),
                "logger": match["logger"],
                "message": match["message"],
            }
        )
    if match := _CONSOLE_LINE.match(text):
        level = parse_level(match["level"])
        if level is not None:
            return plain.model_copy(update={"level": level, "message": match["message"]})
    if text.startswith(_TRACEBACK_START):
        return plain.model_copy(update={"level": Level.ERROR})
    if match := _PYTHON_PROBLEM.match(text):
        return plain.model_copy(update={"level": Level.WARNING if match["kind"].endswith("Warning") else Level.ERROR})
    return plain


def _client(source: LogSource, transport: httpx.AsyncBaseTransport | None) -> _InternalHTTPClient:
    return runtime_logs.client(
        logs_url=source.logs_url, api_key=source.api_key, timeout_seconds=30.0, transport=transport
    )


async def _page(
    client: _InternalHTTPClient,
    source: LogSource,
    *,
    order: LogOrder,
    limit: int,
    start: str | None = None,
) -> LogsResponse:
    try:
        return await runtime_logs.read_page(client, source.service_id, order=order, limit=limit, start=start)
    except httpx.HTTPStatusError as exc:
        detail = terminal_safe(exc.response.text).strip()
        # Matched case-insensitively: the wording is Koyeb's, relayed through the Runtime API.
        if exc.response.status_code == httpx.codes.FAILED_DEPENDENCY and "retention" in detail.lower():
            raise LogRetentionError(
                f"Cannot read the logs of {source.agent_name}: it was deployed before the start of your "
                "organization's log retention window, and the Runtime API refuses to read logs that start "
                "outside it, even the recent ones. Deploy it again with `agents deploy` to start a new log "
                "stream inside the window."
            ) from exc
        message = f"Failed to read the logs of {source.agent_name} (HTTP {exc.response.status_code})"
        raise LogsError(f"{message}: {detail}" if detail else message) from exc
    # InvalidURL is not an HTTPError: a malformed AGENTS_SDK_DEPLOY_RUNTIME_LOGS_URL lands there.
    except (httpx.HTTPError, httpx.InvalidURL, ValidationError) as exc:
        raise LogsError(f"Failed to read the logs of {source.agent_name}: {terminal_safe(str(exc))}") from exc
