from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Protocol, assert_never

import anyio
import mcp_types as types
from langgraph_sdk.errors import PermissionDeniedError
from mcp.shared.exceptions import MCPError
from mcp_types.version import MODERN_PROTOCOL_VERSIONS

from langgraph_api.api.mcp._constants import (
    ELICITATION_REQUIRED_MESSAGE,
    PAUSED_TOOL_MESSAGE,
    UNRESUMABLE_PAUSE_MESSAGE,
)
from langgraph_api.api.mcp._elicitation import (
    EndCall,
    Mode,
    Resume,
    Round,
    UnaskableInterrupt,
)
from langgraph_api.api.mcp._outcome import (
    Completed,
    Failed,
    Finished,
    Paused,
    RunOutcome,
)
from langgraph_api.api.mcp._request_state import (
    Binding,
    InvalidRequestState,
    RequestState,
)
from langgraph_api.config import RUNS_ENABLED, THREADS_ENABLED

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from langgraph_sdk.schema import Thread
    from mcp.server.context import ServerRequestContext

    from langgraph_api.api.mcp._call_thread import CallThread
    from langgraph_api.api.mcp._calls import ToolCallParams
    from langgraph_api.api.mcp._tools import AssistantTool

ToolResult = types.CallToolResult | types.InputRequiredResult
FORM_ONLY: frozenset[Mode] = frozenset({"form"})


class ElicitationRequired(MCPError):
    def __init__(self, modes: frozenset[Mode]) -> None:
        elicitation = types.ElicitationCapability(
            form=types.FormElicitationCapability() if "form" in modes else None,
            url=types.UrlElicitationCapability() if "url" in modes else None,
        )
        super().__init__(
            types.MISSING_REQUIRED_CLIENT_CAPABILITY,
            ELICITATION_REQUIRED_MESSAGE.format(modes=" and ".join(sorted(modes))),
            types.MissingRequiredClientCapabilityErrorData(
                required_capabilities=types.ClientCapabilities(elicitation=elicitation)
            ).model_dump(by_alias=True, mode="json", exclude_none=True),
        )


@dataclass(frozen=True, slots=True)
class ElicitationModes:
    declared: frozenset[Mode]

    @classmethod
    def of(cls, capabilities: types.ClientCapabilities | None) -> ElicitationModes:
        elicitation = capabilities.elicitation if capabilities else None
        if elicitation is None:
            return cls(frozenset())
        declared: set[Mode] = set()
        if elicitation.form is not None:
            declared.add("form")
        if elicitation.url is not None:
            declared.add("url")
        return cls(frozenset(declared) or FORM_ONLY)

    def require(self, needed: frozenset[Mode]) -> None:
        if not needed <= self.declared:
            raise ElicitationRequired(needed)


class PausePolicy(Protocol):
    async def call(self, tool: AssistantTool, params: ToolCallParams) -> ToolResult: ...


@dataclass(frozen=True, slots=True)
class ReportPause:
    notice: str

    async def call(
        self, tool: AssistantTool, params: ToolCallParams
    ) -> types.CallToolResult:
        if params.request_state is not None:
            raise InvalidRequestState
        outcome = await tool.run_once(params)
        match outcome:
            case Paused():
                return outcome.notice(self.notice)
            case Completed() | Failed():
                return outcome.tool_result()
            case _:
                assert_never(outcome)


@dataclass(frozen=True, slots=True)
class RequireElicitation:
    async def call(self, tool: AssistantTool, params: ToolCallParams) -> ToolResult:
        if params.request_state is not None:
            return await ElicitAnswers(ElicitationModes(frozenset())).call(tool, params)
        outcome = await tool.run_once(params)
        match outcome:
            case Paused(interrupts=interrupts):
                try:
                    needed = Round.of(interrupts).modes
                except UnaskableInterrupt as error:
                    return error.outcome.tool_result()
                raise ElicitationRequired(needed)
            case Completed() | Failed():
                return outcome.tool_result()
            case _:
                assert_never(outcome)


@dataclass(frozen=True, slots=True)
class ElicitAnswers:
    modes: ElicitationModes

    async def call(self, tool: AssistantTool, params: ToolCallParams) -> ToolResult:
        if params.request_state is None:
            return await self._start(tool, params)
        state = RequestState.parse(params.request_state)
        thread = tool.thread(str(state.thread_id))
        call = ElicitingCall(
            thread,
            params,
            state,
            modes=self.modes,
            answers=params.answers,
            release=thread.expire_soon,
        )
        return await call.retry()

    async def _start(self, tool: AssistantTool, params: ToolCallParams) -> ToolResult:
        try:
            thread = await tool.new_thread()
        except PermissionDeniedError:
            return await ReportPause(UNRESUMABLE_PAUSE_MESSAGE).call(tool, params)
        state = RequestState.new(thread.thread_id)
        call = ElicitingCall(
            thread,
            params,
            state,
            modes=self.modes,
            answers=params.answers,
            release=thread.delete,
        )
        return await call.first()


def pause_policy(ctx: ServerRequestContext) -> PausePolicy:
    if not (THREADS_ENABLED and RUNS_ENABLED):
        return ReportPause(UNRESUMABLE_PAUSE_MESSAGE)
    if ctx.protocol_version not in MODERN_PROTOCOL_VERSIONS:
        return ReportPause(PAUSED_TOOL_MESSAGE)
    modes = ElicitationModes.of(ctx.session.client_capabilities)
    if not modes.declared:
        return RequireElicitation()
    return ElicitAnswers(modes)


@dataclass(frozen=True, slots=True)
class ElicitingCall:
    thread: CallThread
    params: ToolCallParams
    state: RequestState
    modes: ElicitationModes
    answers: types.InputResponses
    release: Callable[[], Awaitable[None]]
    verified: Binding | None = None

    async def first(self) -> ToolResult:
        try:
            return await self._settle(await self.thread.run(self.params))
        except UnaskableInterrupt as error:
            return await self._unaskable(error)
        except BaseException:
            with anyio.CancelScope(shield=True):
                await self.release()
            raise

    async def retry(self) -> ToolResult:
        snapshot = await self.thread.get()
        binding = Binding.verified(snapshot["metadata"], self._call_digest, self.state)
        if binding.ended is not None:
            return EndCall(binding.ended).outcome.tool_result()
        call = replace(self, verified=binding)
        try:
            if binding.admits(self._call_digest, self.state):
                return await call._continue(snapshot, binding)
            return await call._next()._continue(snapshot, binding)
        except ElicitationRequired:
            await self.release()
            raise

    async def _continue(self, snapshot: Thread, binding: Binding) -> ToolResult:
        try:
            if interrupts := await self.thread.pending(snapshot):
                pending = Round.of(interrupts)
                if pending.digest == binding.asked:
                    return await self._answer(pending)
                if not await self.thread.resumed_with(self.state):
                    return await replace(self, answers={})._answer(pending)
            outcome = await self.thread.join(self.state)
            return await self._next()._settle(outcome)
        except UnaskableInterrupt as error:
            return await self._unaskable(error)

    async def _settle(self, outcome: RunOutcome) -> ToolResult:
        match outcome:
            case Paused(interrupts=interrupts):
                return await self._answer(Round.of(interrupts))
            case Completed() | Failed():
                return await self._finish(outcome)
            case _:
                assert_never(outcome)

    async def _answer(self, pending: Round) -> ToolResult:
        self.modes.require(pending.modes)
        if not pending.answered_by(self.answers):
            return await self._ask(pending)
        reply = pending.reply(self.answers)
        match reply:
            case EndCall() as ended:
                ending = Binding.of(
                    self._call_digest, self.state, pending, ended.refusal
                )
                await self.thread.bind(ending, self.verified)
                return await self._finish(ended.outcome)
            case Resume(value=value):
                outcome = await self.thread.resume(
                    value, self.state, self.params.context
                )
                return await self._next()._settle(outcome)
            case _:
                assert_never(reply)

    async def _ask(self, pending: Round) -> ToolResult:
        try:
            await self.thread.bind(
                Binding.of(self._call_digest, self.state, pending), self.verified
            )
        except PermissionDeniedError:
            return await self._finish(Failed(UNRESUMABLE_PAUSE_MESSAGE))
        return types.InputRequiredResult(
            input_requests=pending.input_requests, request_state=str(self.state)
        )

    async def _finish(self, outcome: Finished) -> types.CallToolResult:
        await self.release()
        return outcome.tool_result()

    async def _unaskable(self, error: UnaskableInterrupt) -> types.CallToolResult:
        return await self._finish(error.outcome)

    @property
    def _call_digest(self) -> str:
        return self.params.digest(self.thread.assistant_id)

    def _next(self) -> ElicitingCall:
        return replace(self, state=self.state.next(), answers={})
