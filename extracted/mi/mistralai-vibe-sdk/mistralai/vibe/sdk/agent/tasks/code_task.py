"""ToolAsCodeTask — wraps the programmatic tool calling engine as a Task.

Follows the same pattern as ToolTask (ModuleTask + StateModule):

    Initialize → [RunCode effect] → CodeComplete → CompletedOutput/FailedOutput

The RunCode effect handler calls orchestrate() to run the full
pause/resume loop. The module/task infrastructure handles channels,
downstream events, and lifecycle automatically via LocalChannel.

The code-task engine itself (orchestrate, ToolResolver, ToolDefinition, …)
lives in ``mistralai.vibe.sdk.experimental.code_task``; this module is the
agent-layer task runtime wrapper that drives it.
"""

from typing import Any

import structlog
from pydantic import BaseModel

from mistralai.vibe.sdk.agent.execution.loop import EffectRegistry, StateModule, StateSink
from mistralai.vibe.sdk.agent.tasks.core import Card, TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import ModuleTask, TaskConfigBase
from mistralai.vibe.sdk.execution_record.state import CompletedOutput, FailedOutput, TaskState
from mistralai.vibe.sdk.experimental.code_task.orchestrator import ToolResolver, orchestrate
from mistralai.vibe.sdk.experimental.code_task.types import ToolDefinition

logger = structlog.get_logger()


# ---------------------------------------------------------------------------
# Actions and effects
# ---------------------------------------------------------------------------


class ToolAsCodeInitialize(BaseModel):
    """Seed action — starts code execution."""


class RunCode(BaseModel):
    """Effect: run the code orchestration loop."""

    state: TaskState
    tools: list[ToolDefinition]


class CodeComplete(BaseModel):
    """Action: code execution finished."""

    output_state: TaskState


# ---------------------------------------------------------------------------
# Effect handler registry
# ---------------------------------------------------------------------------

_code_task_registry = EffectRegistry()


@_code_task_registry.handles(RunCode)
async def _handle_run_code(
    effect: RunCode,
    sink: StateSink,
    resolve_tool: ToolResolver | None = None,
) -> list[CodeComplete]:
    """Run the orchestration loop and return CodeComplete."""
    if resolve_tool is None:
        msg = "resolve_tool must be provided"
        raise ValueError(msg)

    state = effect.state
    code = state.input.get("code", "") if isinstance(state.input, dict) else ""
    input_data = state.input.get("input", {}) if isinstance(state.input, dict) else {}

    try:
        result = await orchestrate(
            code=code,
            tools=effect.tools,
            resolve_tool=resolve_tool,
            input=input_data,
        )

        if result.type == "code_result" and result.result and result.result.type == "success":
            output = CompletedOutput(value=result.result.value)
        elif result.type == "code_result" and result.result and result.result.type == "error":
            output = FailedOutput(error=str(result.result.error))
        else:
            output = FailedOutput(error=result.error or "Unknown error")
    except Exception as e:
        logger.exception("tool_as_code.execution_failed")
        output = FailedOutput(error=str(e))

    new_state = state.model_copy(update={"output": output})
    return [CodeComplete(output_state=new_state)]


# ---------------------------------------------------------------------------
# ToolAsCodeModule — one-step StateModule
# ---------------------------------------------------------------------------


class ToolAsCodeModule(StateModule):
    """StateModule for tool-as-code execution.

    One-step lifecycle: Initialize -> RunCode -> CodeComplete -> done.
    Same shape as ToolModule but delegates to the orchestration engine.
    """

    effect_handlers = _code_task_registry
    initial_action_type = ToolAsCodeInitialize

    def __init__(self, tools: list[ToolDefinition], resolve_tool: ToolResolver) -> None:
        self._tools = tools
        self._resolve_tool = resolve_tool

    def reduce(self, state: TaskState, action: Any) -> tuple[TaskState, list[Any]]:
        match action:
            case ToolAsCodeInitialize():
                return (state, [RunCode(state=state, tools=self._tools)])
            case CodeComplete(output_state=output_state):
                return (output_state, [])
        return (state, [])

    async def handle_effect(self, effect: Any, sink: StateSink) -> list[Any]:
        handler = self.effect_handlers.get(type(effect))
        if handler is None:
            return []
        if isinstance(effect, RunCode):
            return await handler(effect, sink, resolve_tool=self._resolve_tool)
        return await handler(effect, sink)


# ---------------------------------------------------------------------------
# ToolAsCodeTask — ModuleTask wrapping the engine
# ---------------------------------------------------------------------------


class ToolAsCodeTask(ModuleTask[TaskConfigBase]):
    """Execute LLM-generated Python code with tool access.

    Follows the standard ModuleTask pattern. Inherits run() which
    returns a LocalChannel, and execute() for workflow integration.

    Usage::

        task = ToolAsCodeTask(
            name="run_python",
            tools=[ToolDefinition(function=FunctionDef(name="web_search"))],
            resolve_tool=my_resolver,
        )
        channel = await task.run(state)
        async for event in channel:
            ...
    """

    # -- input schema advertised on the card ----------------------------------
    INPUT_SCHEMA: dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python source with an `async def main()` entry point.",
            },
            "input": {
                "type": "object",
                "description": "Keyword arguments forwarded to main().",
            },
        },
        "required": ["code"],
    }

    def __init__(
        self,
        *,
        name: str = "tool_as_code",
        description: str = "Execute Python code with tool access",
        tools: list[ToolDefinition] | None = None,
        resolve_tool: ToolResolver,
    ) -> None:
        tools_list = tools or []
        callbacks = self._build_callbacks(tools_list)
        super().__init__(
            name=name,
            description=description,
            input_schema=self.INPUT_SCHEMA,
            callbacks=callbacks,
        )
        self._tools = tools_list
        self._resolve_tool = resolve_tool

    # -- helpers --------------------------------------------------------------

    @staticmethod
    def _build_callbacks(tools: list[ToolDefinition]) -> list[TaskCallback]:
        """Convert tool definitions into TaskCallback declarations.

        Each tool the code may call is surfaced as a callback so that a
        parent orchestrator can see the task's dependencies.
        """
        return [
            TaskCallback(
                card=Card(
                    name=t.function.name,
                    description=t.function.description or "",
                    input_schema=t.function.input_schema or None,
                    output_schema=t.function.output_schema or None,
                ),
            )
            for t in tools
        ]

    def create_module(self) -> ToolAsCodeModule:
        return ToolAsCodeModule(tools=self._tools, resolve_tool=self._resolve_tool)

    @classmethod
    def from_config(cls, config: Any, **kwargs: Any) -> "ToolAsCodeTask":
        msg = "ToolAsCodeTask does not support config-based reconstruction yet"
        raise NotImplementedError(msg)
