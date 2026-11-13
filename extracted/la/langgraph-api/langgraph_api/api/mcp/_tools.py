from __future__ import annotations

import asyncio
import contextlib
import functools
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
import mcp_types as types
import structlog
from langgraph_sdk.client import LangGraphClient, get_client
from mcp.shared.exceptions import MCPError
from starlette.exceptions import HTTPException
from starlette.requests import Request

from langgraph_api.api.mcp import _sanitizers
from langgraph_api.api.mcp._call_thread import CallThread
from langgraph_api.api.mcp._constants import (
    DEFAULT_PAGE_SIZE,
    INTERNAL_ERROR_MESSAGE,
    INVALID_CURSOR_MESSAGE,
    MAX_ASSISTANTS,
    MAX_CURSOR_LENGTH,
    MAX_PAGE_OFFSET,
)
from langgraph_api.api.mcp._outcome import RunOutcome, parse_outcome
from langgraph_api.api.mcp._pauses import PausePolicy, pause_policy

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterable, Mapping

    from langgraph_sdk.schema import Assistant
    from mcp.server.context import ServerRequestContext

    from langgraph_api.api.mcp._calls import ToolCallParams
    from langgraph_api.api.mcp._pauses import ToolResult

logger = structlog.stdlib.get_logger(__name__)

_CURSOR_DIGITS = re.compile(rf"[0-9]{{1,{MAX_CURSOR_LENGTH}}}")
_ANNOTATIONS = types.ToolAnnotations(
    read_only_hint=False,
    destructive_hint=False,
    idempotent_hint=False,
    open_world_hint=True,
)


@functools.lru_cache(maxsize=1)
def _client() -> LangGraphClient:
    return get_client(url=None)


@contextlib.asynccontextmanager
async def _failures_as_mcp_errors() -> AsyncIterator[None]:
    try:
        yield
    except MCPError:
        raise
    except Exception as error:
        mcp_error = _mcp_error(error)
        if mcp_error.code == types.INTERNAL_ERROR:
            await logger.aexception("MCP tool request failed")
        raise mcp_error from error


def _mcp_error(error: Exception) -> MCPError:
    match error:
        case httpx.HTTPStatusError(response=response) if response.is_client_error:
            return MCPError(types.INVALID_PARAMS, _detail(response))
        case HTTPException(status_code=status, detail=detail) if (
            httpx.codes.is_client_error(status)
        ):
            return MCPError(types.INVALID_PARAMS, detail)
        case _:
            return MCPError(types.INTERNAL_ERROR, INTERNAL_ERROR_MESSAGE)


def _detail(response: httpx.Response) -> str:
    with contextlib.suppress(ValueError):
        match response.json():
            case {"detail": str() as detail} if detail:
                return detail
    return response.reason_phrase


@dataclass(frozen=True, slots=True)
class AssistantTools:
    client: LangGraphClient
    headers: Mapping[str, str]
    pauses: PausePolicy

    @classmethod
    def of(cls, ctx: ServerRequestContext) -> AssistantTools:
        if not isinstance(ctx.request, Request):
            raise TypeError("Assistant tools are served over HTTP only")
        return cls(_client(), ctx.request.headers, pause_policy(ctx))

    @_failures_as_mcp_errors()
    async def list(self, cursor: str | None) -> types.ListToolsResult:
        offset = _page_offset(cursor)
        assistants = await self.client.assistants.search(
            offset=offset, limit=DEFAULT_PAGE_SIZE, headers=self.headers
        )
        named = await _first_per_name(assistants)
        tools = await asyncio.gather(
            *(self._tool(assistant, name) for name, assistant in named.items())
        )
        return types.ListToolsResult(
            tools=[tool for tool in tools if tool is not None],
            next_cursor=str(offset + DEFAULT_PAGE_SIZE)
            if len(assistants) == DEFAULT_PAGE_SIZE
            else None,
        )

    @_failures_as_mcp_errors()
    async def call(self, params: ToolCallParams) -> ToolResult:
        assistant_id = await self._assistant_serving(params.name)
        return await self.pauses.call(
            AssistantTool(self.client, self.headers, assistant_id), params
        )

    async def _tool(self, assistant: Assistant, name: str) -> types.Tool | None:
        try:
            schemas = await self.client.assistants.get_schemas(
                assistant["assistant_id"], headers=self.headers
            )
            input_schema = schemas.get("input_schema", {})
            if input_schema is None:
                raise ValueError("Input schema generation failed")
            if input_schema:
                _sanitizers.simplify_mcp_schema_inplace(input_schema)
                _sanitizers.drop_mcp_param_headers_inplace(input_schema)
            input_schema.setdefault("type", "object")
            return types.Tool(
                name=name,
                title=assistant["name"],
                description=assistant.get("description")
                or f"Tool based on the {assistant['name']} assistant",
                input_schema=input_schema,
                annotations=_ANNOTATIONS,
            )
        except Exception as e:
            await logger.awarning(
                "Failed to get schema for assistant, skipping from MCP tools list",
                assistant_id=assistant["assistant_id"],
                assistant_name=assistant["name"],
                error=str(e),
            )
            return None

    async def _assistant_serving(self, tool_name: str) -> str:
        assistants = await self.client.assistants.search(
            limit=MAX_ASSISTANTS, headers=self.headers
        )
        match [
            assistant["assistant_id"]
            for assistant in assistants
            if _sanitizers.normalize_name(assistant["name"]) == tool_name
        ]:
            case [assistant_id]:
                return assistant_id
            case []:
                raise MCPError(types.INVALID_PARAMS, f"Unknown tool: {tool_name}")
            case _:
                raise MCPError(
                    types.INVALID_PARAMS, "Multiple tools found with the same name."
                )


@dataclass(frozen=True, slots=True)
class AssistantTool:
    client: LangGraphClient
    headers: Mapping[str, str]
    assistant_id: str

    async def run_once(self, params: ToolCallParams) -> RunOutcome:
        value = await self.client.runs.wait(
            thread_id=None,
            assistant_id=self.assistant_id,
            input=params.input,
            context=params.context,
            headers=self.headers,
            raise_error=False,
        )
        return parse_outcome(value)

    async def new_thread(self) -> CallThread:
        return await CallThread.create(self.client, self.headers, self.assistant_id)

    def thread(self, thread_id: str) -> CallThread:
        return CallThread(self.client, self.headers, self.assistant_id, thread_id)


async def _first_per_name(assistants: Iterable[Assistant]) -> dict[str, Assistant]:
    named: dict[str, Assistant] = {}
    for assistant in assistants:
        name = _sanitizers.normalize_name(assistant["name"])
        if name in named:
            await logger.awarning(
                f"Duplicate assistant name found {assistant['name']}",
                name=assistant["name"],
                normalized=name,
            )
        else:
            named[name] = assistant
    return named


def _page_offset(cursor: str | None) -> int:
    if cursor is None:
        return 0
    if not _CURSOR_DIGITS.fullmatch(cursor) or int(cursor) > MAX_PAGE_OFFSET:
        raise MCPError(types.INVALID_PARAMS, INVALID_CURSOR_MESSAGE)
    return int(cursor)
