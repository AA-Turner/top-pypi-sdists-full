from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING

import httpx
import jsonschema_rs
import mcp_types as types
import structlog
from mcp.shared.exceptions import MCPError
from starlette.exceptions import HTTPException

from langgraph_api.api.mcp._constants import (
    BREAKPOINT_MESSAGE,
    FINISHED_CALL_TTL_MINUTES,
    PAUSED_CALL_TTL_MINUTES,
)
from langgraph_api.api.mcp._outcome import Failed, Paused, RunOutcome, parse_outcome
from langgraph_api.api.mcp._request_state import Binding, InvalidRequestState
from langgraph_api.config import THREAD_TTL
from langgraph_api.models.run import create_valid_run
from langgraph_api.validation import RunCreateStateful, sanitize_and_validate
from langgraph_runtime.database import connect
from langgraph_runtime.retry import retry_db

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator, Mapping
    from uuid import UUID

    from langgraph_sdk.client import LangGraphClient
    from langgraph_sdk.schema import Thread
    from pydantic import JsonValue

    from langgraph_api.api.mcp._calls import ToolCallParams
    from langgraph_api.api.mcp._request_state import RequestState
    from langgraph_api.schema import Interrupt

logger = structlog.stdlib.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class CallThread:
    client: LangGraphClient
    headers: Mapping[str, str]
    assistant_id: str
    thread_id: str

    @classmethod
    async def create(
        cls, client: LangGraphClient, headers: Mapping[str, str], assistant_id: str
    ) -> CallThread:
        thread = await client.threads.create(
            ttl=_within_operator_ttl(PAUSED_CALL_TTL_MINUTES), headers=headers
        )
        return cls(client, headers, assistant_id, thread["thread_id"])

    async def get(self) -> Thread:
        with _invalid_state_if_missing():
            return await self.client.threads.get(self.thread_id, headers=self.headers)

    async def pending(self, thread: Thread) -> list[Interrupt]:
        if thread["status"] != "interrupted":
            return []
        with _invalid_state_if_missing():
            state = await self.client.threads.get_state(
                self.thread_id, headers=self.headers
            )
        return [
            interrupt for task in state["tasks"] for interrupt in task["interrupts"]
        ]

    async def bind(self, binding: Binding, replacing: Binding | None) -> None:
        if binding == replacing:
            return
        if replacing is not None and await self._bound() not in (replacing, binding):
            return
        await self.client.threads.update(
            self.thread_id,
            metadata=binding.metadata,
            ttl=_within_operator_ttl(PAUSED_CALL_TTL_MINUTES),
            headers=self.headers,
        )

    async def run(self, params: ToolCallParams) -> RunOutcome:
        value = await self.client.runs.wait(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            input=params.input,
            context=params.context,
            durability="exit",
            headers=self.headers,
            raise_error=False,
        )
        return await self._outcome(value)

    async def resume(
        self,
        value: JsonValue,
        state: RequestState,
        context: Mapping[str, JsonValue] | None,
    ) -> RunOutcome:
        try:
            await self._create_run(self._resume_payload(value, context), state.run_id)
        except HTTPException as error:
            if error.status_code == HTTPStatus.NOT_FOUND:
                raise InvalidRequestState from None
            if error.status_code != HTTPStatus.CONFLICT:
                raise
            return await self.join(state)
        return await self._wait_for(state)

    async def join(self, state: RequestState) -> RunOutcome:
        if not await self.resumed_with(state):
            raise InvalidRequestState
        return await self._wait_for(state)

    async def resumed_with(self, state: RequestState) -> bool:
        try:
            await self.client.runs.get(
                self.thread_id, str(state.run_id), headers=self.headers
            )
        except httpx.HTTPStatusError as error:
            if error.response.status_code != HTTPStatus.NOT_FOUND:
                raise
            return False
        return True

    async def delete(self) -> None:
        async with self._best_effort("Could not delete a finished MCP call's thread"):
            await self.client.threads.delete(self.thread_id, headers=self.headers)

    async def expire_soon(self) -> None:
        async with self._best_effort("Could not shorten a finished MCP call's TTL"):
            await self.client.threads.update(
                self.thread_id,
                metadata={},
                ttl=_within_operator_ttl(FINISHED_CALL_TTL_MINUTES),
                headers=self.headers,
            )

    async def _bound(self) -> Binding | None:
        return Binding.stored((await self.get())["metadata"])

    @asynccontextmanager
    async def _best_effort(self, failure: str) -> AsyncIterator[None]:
        try:
            yield
        except httpx.HTTPStatusError as error:
            if error.response.status_code != HTTPStatus.NOT_FOUND:
                await logger.awarning(
                    failure,
                    thread_id=self.thread_id,
                    status_code=error.response.status_code,
                )

    @retry_db
    async def _create_run(self, payload: dict[str, JsonValue], run_id: UUID) -> None:
        async with connect() as conn:
            await create_valid_run(
                conn, self.thread_id, payload, self.headers, run_id=run_id
            )

    async def _wait_for(self, state: RequestState) -> RunOutcome:
        with _invalid_state_if_missing():
            value = await self.client.runs.join(
                self.thread_id, str(state.run_id), headers=self.headers
            )
        return await self._outcome(value)

    async def _outcome(self, value: JsonValue) -> RunOutcome:
        outcome = parse_outcome(value)
        if isinstance(outcome, Failed):
            return outcome
        thread = await self.get()
        match thread["status"]:
            case "busy":
                raise InvalidRequestState
            case "interrupted":
                return await self._paused_or_stopped(thread)
            case _:
                return outcome

    async def _paused_or_stopped(self, thread: Thread) -> Paused | Failed:
        if interrupts := await self.pending(thread):
            return Paused(tuple(interrupts))
        return Failed(BREAKPOINT_MESSAGE)

    def _resume_payload(
        self, value: JsonValue, context: Mapping[str, JsonValue] | None
    ) -> dict[str, JsonValue]:
        payload: dict[str, JsonValue] = {
            "assistant_id": self.assistant_id,
            "command": {"resume": value},
            "multitask_strategy": "reject",
            "durability": "exit",
        }
        if context is not None:
            payload["context"] = dict(context)
        try:
            sanitize_and_validate(payload, RunCreateStateful)
        except jsonschema_rs.ValidationError:
            raise MCPError(types.INVALID_PARAMS, "Invalid tool call context") from None
        return payload


def _within_operator_ttl(minutes: float) -> float:
    operator_ttl = THREAD_TTL.get("default_ttl") if THREAD_TTL else None
    return minutes if operator_ttl is None else min(minutes, operator_ttl)


@contextmanager
def _invalid_state_if_missing() -> Iterator[None]:
    try:
        yield
    except httpx.HTTPStatusError as error:
        if error.response.status_code != HTTPStatus.NOT_FOUND:
            raise
        raise InvalidRequestState from None
