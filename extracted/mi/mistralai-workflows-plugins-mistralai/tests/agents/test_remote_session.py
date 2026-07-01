"""Tests for RemoteSession pending-tool-call tracking.

A handoff is a hard boundary for outstanding function calls. The server abandons every
call emitted before the final handoff (answering one makes the next append fail with a
400 "Unexpected tool call id ... in tool results") and keeps every call emitted after
it (leaving one unanswered makes the append fail with "results are still missing"). So a
call is pending iff no handoff follows it in the batch.
"""

import pytest
from mistralai.client import models as mistralai_models

from mistralai.workflows.plugins.mistralai.session.remote_session import RemoteSession


def _function_call(
    tool_call_id: str, agent_id: str = "ag_bigquery", name: str = "generate_log"
) -> mistralai_models.FunctionCallEntry:
    return mistralai_models.FunctionCallEntry(tool_call_id=tool_call_id, name=name, arguments="{}", agent_id=agent_id)


def _handoff(
    previous_agent_id: str = "ag_bigquery", next_agent_id: str = "ag_insight"
) -> mistralai_models.AgentHandoffEntry:
    return mistralai_models.AgentHandoffEntry(
        previous_agent_id=previous_agent_id,
        previous_agent_name="bigquery_runner_agent",
        next_agent_id=next_agent_id,
        next_agent_name="insight_agent",
    )


def _message_output() -> mistralai_models.MessageOutputEntry:
    return mistralai_models.MessageOutputEntry(content="Here is the answer.")


class TestOpenFunctionCallIds:
    def test_call_before_handoff_is_dropped(self) -> None:
        outputs = [_function_call("zB2ak8krq"), _handoff(), _message_output()]
        assert RemoteSession._open_function_call_ids(outputs) == set()

    def test_call_after_handoff_stays_open(self) -> None:
        outputs = [_handoff(), _message_output(), _function_call("EO3HrBkD3")]
        assert RemoteSession._open_function_call_ids(outputs) == {"EO3HrBkD3"}

    def test_calls_without_handoff_are_open(self) -> None:
        outputs = [_function_call("call-1"), _function_call("call-2")]
        assert RemoteSession._open_function_call_ids(outputs) == {"call-1", "call-2"}

    def test_only_calls_after_the_last_handoff_stay_open(self) -> None:
        outputs = [
            _function_call("call-1"),
            _handoff("ag_bigquery", "ag_insight"),
            _function_call("call-2"),
            _handoff("ag_insight", "ag_final"),
            _function_call("call-3"),
        ]
        assert RemoteSession._open_function_call_ids(outputs) == {"call-3"}


class TestProcessOutput:
    @pytest.mark.asyncio
    async def test_dropped_call_is_not_executed(self) -> None:
        session = RemoteSession()
        outputs = [_function_call("zB2ak8krq"), _handoff(), _message_output()]
        session._pending_tool_call_ids = RemoteSession._open_function_call_ids(outputs)

        # The abandoned function call must yield no follow-up tool result, so the
        # runner stops instead of appending a result the server would reject.
        result = await session.process_output(outputs[0])
        assert result == []

    @pytest.mark.asyncio
    async def test_dropped_call_is_not_remembered_as_pending(self) -> None:
        session = RemoteSession()
        outputs = [_function_call("zB2ak8krq"), _handoff(), _message_output()]
        session._pending_tool_call_ids = RemoteSession._open_function_call_ids(outputs)

        # Avoids a bogus "interrupted" FunctionResultEntry on the next append.
        assert session._build_missing_tool_result_inputs([]) == []

    @pytest.mark.asyncio
    async def test_open_call_is_remembered_as_pending(self) -> None:
        session = RemoteSession()
        outputs = [_handoff(), _message_output(), _function_call("EO3HrBkD3")]
        session._pending_tool_call_ids = RemoteSession._open_function_call_ids(outputs)

        assert session._pending_tool_call_ids == {"EO3HrBkD3"}
