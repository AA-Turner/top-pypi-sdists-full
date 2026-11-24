"""A caller-bounded process tool's dispatch deadline outlives the timeout the caller asked for.

Live (2026-11-18, tool_execution_failed): ``shell_execute`` called with
``timeout_seconds=120`` (and another with 300) was canceled by the tool executor at exactly
120s (300s) — the executor's deadline was ``max(ceiling, requested)``, equal to the command's
own limit, so it always beat the box's graceful timeout answer (exit code, output so far),
which the ``/exec`` HTTP call waits ``EXEC_HTTP_GRACE_SECONDS`` past the limit to receive.
The agent got "canceled, work abandoned" instead of the command's real result.
"""

from __future__ import annotations

from matrx_ai.tools import knobs as knobs_mod
from matrx_ai.tools.executor import _dispatch_timeout_seconds
from matrx_ai.tools.knobs import (
    exec_http_grace_seconds,
    process_tool_deadline_grace_seconds,
)
from matrx_ai.tools.models import ToolDefinition, ToolType


def _shell(name: str = "shell_execute") -> ToolDefinition:
    return ToolDefinition(name=name, description="Run a command.", tool_type=ToolType.LOCAL)


def test_the_live_requests_get_room_for_the_box_to_answer() -> None:
    knobs_mod.configure_tool_dispatch_knobs(lambda key: {"default_timeout_seconds": 120}.get(key))
    for requested in (120, 300):
        deadline = _dispatch_timeout_seconds(
            _shell(), {"timeout_seconds": requested}, is_delegated=False
        )
        # The box answers its own timeout up to EXEC_HTTP_GRACE_SECONDS late; we must still be waiting.
        assert deadline > requested + exec_http_grace_seconds(), (requested, deadline)


def test_the_grace_covers_the_transport_grace_for_every_process_tool() -> None:
    knobs_mod.configure_tool_dispatch_knobs(lambda key: {"default_timeout_seconds": 120}.get(key))
    assert process_tool_deadline_grace_seconds() > exec_http_grace_seconds()
    for name in ("shell_execute", "shell_python"):
        assert _dispatch_timeout_seconds(_shell(name), {"timeout_seconds": 200}, is_delegated=False) == (
            200 + process_tool_deadline_grace_seconds()
        )


def test_a_short_request_keeps_the_ceiling_and_other_tools_are_untouched() -> None:
    knobs_mod.configure_tool_dispatch_knobs(lambda key: {"default_timeout_seconds": 120}.get(key))
    assert _dispatch_timeout_seconds(_shell(), {"timeout_seconds": 30}, is_delegated=False) == 120.0
    assert _dispatch_timeout_seconds(_shell(), {}, is_delegated=False) == 120.0
    assert _dispatch_timeout_seconds(_shell("rulebook"), {"timeout_seconds": 300}, is_delegated=False) == 120.0


def test_the_knob_values_are_used_and_the_deadline_stays_above_the_transport() -> None:
    rows = {"default_timeout_seconds": 120, "process_tool_deadline_grace_seconds": 45, "exec_http_grace_seconds": 5}
    knobs_mod.configure_tool_dispatch_knobs(rows.get)
    assert exec_http_grace_seconds() == 5.0
    assert _dispatch_timeout_seconds(_shell(), {"timeout_seconds": 200}, is_delegated=False) == 245.0
    # A deadline grace set below the transport grace is lifted above it, never left racing it.
    rows.update(process_tool_deadline_grace_seconds=3, exec_http_grace_seconds=20)
    assert _dispatch_timeout_seconds(_shell(), {"timeout_seconds": 200}, is_delegated=False) == 221.0
