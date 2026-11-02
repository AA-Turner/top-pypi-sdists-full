"""The Runtime API's service logs: its wire models, one page read, and making their text safe to print.

`logs` (for `agents logs`) and `deploy_logs` (for a failed `agents deploy`) both read a managed worker's
runtime logs through this module, so the request and the response shape live in one place.
"""

from __future__ import annotations

import re
from datetime import datetime
from http import HTTPMethod
from typing import Literal
from urllib.parse import quote

import httpx
from pydantic import BaseModel, ConfigDict

from mistralai.vibe_agents._http import _InternalHTTPClient

# The output is printed to the user's terminal, so no escape sequence may reach it: colors, but also OSC
# (e.g. OSC 52 writes the clipboard), DCS/PM/APC strings and cursor movement. Strings run to BEL or ST.
_TERMINAL_ESCAPE = re.compile(
    r"\x1b(?:"
    r"\[[0-?]*[ -/]*[@-~]"  # CSI, including private parameters
    r"|[\]PX^_][^\x07\x1b]*(?:\x07|\x1b\\)?"  # OSC, DCS, SOS, PM, APC
    r"|[ -/]*[0-~]"  # any other escape
    r")?"
    r"|\x9b[0-?]*[ -/]*[@-~]"  # 8-bit CSI
    r"|[\x9d\x90\x98\x9e\x9f][^\x07\x1b\x9c]*(?:\x07|\x1b\\|\x9c)?"  # 8-bit OSC, DCS, SOS, PM, APC
)
# Remaining C0/C1 controls (carriage return, backspace, ...) could overwrite what was already printed.
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0a-\x1f\x7f-\x9f]")
# The same, keeping line feeds: multi-line text such as an agent's reply.
_CONTROL_CHARACTERS_BUT_NEWLINE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]")


# The two orders the Runtime API reads in.
type LogOrder = Literal["asc", "desc"]


class _LogLabels(BaseModel):
    model_config = ConfigDict(extra="ignore")

    stream: str | None = None


class LogEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    msg: str
    created_at: datetime | None = None
    labels: _LogLabels | None = None

    @property
    def stream(self) -> str | None:
        return self.labels.stream if self.labels is not None else None


class LogsResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    logs: list[LogEntry]
    has_more: bool | None = None
    # The cursor for the next page, already shifted past this page's last entry so it repeats none of them.
    # Null when the read reached the end of the window.
    next_start: str | None = None


def client(
    *,
    logs_url: str,
    api_key: str,
    timeout_seconds: float,
    transport: httpx.AsyncBaseTransport | None = None,
) -> _InternalHTTPClient:
    return _InternalHTTPClient(
        base_url=logs_url,
        api_key=api_key,
        timeout_seconds=timeout_seconds,
        transport=transport,
    )


async def read_page(
    http: _InternalHTTPClient,
    service_id: str,
    *,
    order: LogOrder,
    limit: int,
    start: str | None = None,
    retries: int | None = None,
) -> LogsResponse:
    """One page of a service's runtime logs. Raises httpx errors and ValidationError for the caller to word."""
    params: dict[str, str | int] = {"log_type": "runtime", "order": order, "limit": limit}
    if start is not None:
        params["start"] = start
    response = await http.make_request(HTTPMethod.GET, f"/{quote(service_id, safe='')}", params=params, retries=retries)
    response.raise_for_status()
    return LogsResponse.model_validate_json(response.content)


def logs_command(logs_url: str, service_id: str) -> str:
    """The equivalent request, for a user to run when the CLI could not."""
    return (
        f'curl -s "{logs_url.rstrip("/")}/{service_id}?log_type=runtime&order=asc&limit=1000" '
        '-H "Authorization: Bearer $MISTRAL_API_KEY"'
    )


def terminal_safe(text: str, *, keep_newlines: bool = False) -> str:
    """Drop every escape sequence and control character from text read off the network."""
    controls = _CONTROL_CHARACTERS_BUT_NEWLINE if keep_newlines else _CONTROL_CHARACTERS
    return controls.sub("", _TERMINAL_ESCAPE.sub("", text))
