from dataclasses import dataclass

import mcp_types as types
from pydantic import JsonValue

from langgraph_api.api.mcp._constants import RUN_FAILED_MESSAGE
from langgraph_api.schema import Interrupt
from langgraph_api.serde import json_dumpb
from langgraph_api.state import patch_interrupt


@dataclass(frozen=True, slots=True)
class Completed:
    output: JsonValue

    def tool_result(self) -> types.CallToolResult:
        return types.CallToolResult(content=[_text(json_dumpb(self.output).decode())])


@dataclass(frozen=True, slots=True)
class Failed:
    message: str

    def tool_result(self) -> types.CallToolResult:
        return types.CallToolResult(content=[_text(self.message)], is_error=True)


@dataclass(frozen=True, slots=True)
class Paused:
    interrupts: tuple[Interrupt, ...]

    def notice(self, message: str) -> types.CallToolResult:
        return types.CallToolResult(
            content=[_text(message), _text(json_dumpb(self.interrupts).decode())],
            is_error=True,
        )


Finished = Completed | Failed
RunOutcome = Completed | Failed | Paused


def parse_outcome(value: JsonValue) -> RunOutcome:
    match value:
        case {"__error__": error, **rest} if not rest:
            return Failed(_error_message(error))
        case {"__interrupt__": [_, *_] as interrupts}:
            return Paused(tuple(map(patch_interrupt, interrupts)))
        case _:
            return Completed(value)


def _error_message(error: JsonValue) -> str:
    match error:
        case {"error": str() as name, "message": str() as message} if message:
            return f"{name}: {message}"
        case {"error": str() as name}:
            return name
        case _:
            return RUN_FAILED_MESSAGE


def _text(text: str) -> types.TextContent:
    return types.TextContent(type="text", text=text)
