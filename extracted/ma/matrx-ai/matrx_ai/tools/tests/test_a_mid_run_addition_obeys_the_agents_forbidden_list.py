"""A mid-run addition never brings back a tool the agent forbids (TOOL-SOURCES.md rule U).

A bundle lister, ``find_tools`` or ``load_tools`` queues tools through
``ctx.queue_tool_changes``; ``drain_tool_mutations`` merges them between loop steps. The
agent's forbidden list (``config.agent_excluded_tools``, stamped on turn 1) must hold there
too, or a forbidden tool returns one step after the funnel removed it (real test F-Q16-2).
"""

from __future__ import annotations

import pytest

from matrx_ai.config.message_config import MessageList
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools.dynamic_drain import drain_tool_mutations
from matrx_ai.tools.models import _PENDING_TOOL_MUTATIONS_KEY

pytestmark = pytest.mark.asyncio


class _Emitter:
    async def send_resource_changed(self, **_kw) -> None: ...
    async def send_warning(self, *_a, **_kw): ...
    async def send_info(self, *_a, **_kw): ...


def _queued(*names: str):
    from matrx_connect import AppContext

    return AppContext(
        emitter=_Emitter(),
        conversation_id="conv-1",
        request_id="req-1",
        metadata={
            _PENDING_TOOL_MUTATIONS_KEY: [
                {
                    "action": "add",
                    "specs": [{"kind": "registered", "name": n} for n in names],
                    "by": "bundle__list_x",
                }
            ]
        },
    )


async def test_a_forbidden_tool_queued_mid_run_is_not_added() -> None:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[]), tools=["web"])
    config.agent_excluded_tools = ["memory"]
    await drain_tool_mutations(config, _queued("memory", "dom_query"))
    assert "memory" not in config.tools, f"a mid-run addition brought back a forbidden tool: {config.tools}"
    assert "dom_query" in config.tools, f"the forbidden list blocked more than it names: {config.tools}"


async def test_with_no_forbidden_list_the_addition_lands() -> None:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=[]), tools=["web"])
    await drain_tool_mutations(config, _queued("memory"))
    assert "memory" in config.tools, config.tools
