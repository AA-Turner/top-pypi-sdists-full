"""Observe agent runs; on AgentEnd with failures, spawn a reflector subagent."""

import asyncio
import sys
from collections import defaultdict
from contextvars import ContextVar
from pathlib import Path
from uuid import UUID

from loguru import logger

from dreadnode.agents.events import (
    AgentEnd,
    AgentStart,
    GenerationError,
    ToolError,
)
from dreadnode.core.hook import hook

_CAPABILITY_ROOT = Path(__file__).resolve().parents[1]
if str(_CAPABILITY_ROOT) not in sys.path:
    sys.path.insert(0, str(_CAPABILITY_ROOT))

from self_improvement_lib.classifier import (  # noqa: E402
    ClassifiedFailure,
    classify_generation_error,
    classify_tool_error,
)
from self_improvement_lib.reflector_goal import build_reflection_goal  # noqa: E402
from self_improvement_lib.skill_io import update_skill, write_skill  # noqa: E402

_PROPOSED_DIR = _CAPABILITY_ROOT / "skills-proposed"

# ContextVar propagates to asyncio tasks, so the reflector's own hook
# invocations see _is_reflector=True and short-circuit.
_is_reflector: ContextVar[bool] = ContextVar("_dn_is_reflector", default=False)

_runs: dict[UUID, list[ClassifiedFailure]] = defaultdict(list)


@hook(AgentStart)
async def _capture_start(event: AgentStart) -> None:
    if _is_reflector.get():
        return
    _runs[event.agent_id]


@hook(ToolError)
async def _observe_tool_error(event: ToolError) -> None:
    if _is_reflector.get() or event.agent_id not in _runs:
        return
    failure = classify_tool_error(event)
    if failure.worth_learning_from:
        _runs[event.agent_id].append(failure)


@hook(GenerationError)
async def _observe_generation_error(event: GenerationError) -> None:
    if _is_reflector.get() or event.agent_id not in _runs:
        return
    failure = classify_generation_error(event)
    if failure.worth_learning_from:
        _runs[event.agent_id].append(failure)


@hook(AgentEnd)
async def _maybe_reflect(event: AgentEnd) -> None:
    failures = _runs.pop(event.agent_id, None)
    if not failures or _is_reflector.get():
        return
    task = asyncio.create_task(_reflect(failures, event))
    task.add_done_callback(_log_reflector_failure)


def _log_reflector_failure(task: asyncio.Task) -> None:
    exc = task.exception()
    if exc is not None:
        logger.warning("self-improvement reflector failed: {}", exc)


async def _reflect(failures: list[ClassifiedFailure], end_event: AgentEnd) -> None:
    token = _is_reflector.set(True)
    try:
        from dreadnode.app.server.app import create_agent

        goal = build_reflection_goal(failures, end_event, _PROPOSED_DIR)
        reflector = create_agent(
            model="anthropic/claude-sonnet-4-5-20250929",
            extra_tools=[write_skill, update_skill],
        )
        await reflector.run(goal)
    finally:
        _is_reflector.reset(token)
