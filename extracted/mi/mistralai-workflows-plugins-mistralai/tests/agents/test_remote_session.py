"""Tests for RemoteSession pending-tool-call tracking.

A handoff is a hard boundary for outstanding function calls. The server abandons every
call emitted before the final handoff (answering one makes the next append fail with a
400 "Unexpected tool call id ... in tool results") and keeps every call emitted after
it (leaving one unanswered makes the append fail with "results are still missing"). So a
call is pending iff no handoff follows it in the batch.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mistralai.client import models as mistralai_models

from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.plugins.mistralai.agent import Agent
from mistralai.workflows.plugins.mistralai.connectors import connector
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs
from mistralai.workflows.plugins.mistralai.session import remote_session
from mistralai.workflows.plugins.mistralai.session.remote_session import RemoteSession

from .conftest import make_context


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


class TestAgentConnectorRunAsValidation:
    def test_mixed_run_as_on_agent_raises(self) -> None:
        agent = Agent(name="run-as-agent", connectors=[connector("github")])
        # Reassign post-construction to bypass the Agent validator and exercise
        # the session-level check directly.
        agent.connectors = [connector("github", run_as="auto"), connector("slack", run_as="deployment")]

        with pytest.raises(ValueError, match="mixes connector run_as"):
            RemoteSession._resolve_conversation_run_as(agent)

    def test_omitted_run_as_does_not_conflict_without_bindings(self) -> None:
        """An omitted slot has nothing to inherit, so it takes the resolved identity.

        Mirrors the Agent validator, which also judges explicit values only.
        """
        agent = Agent(
            name="mixed",
            connectors=[connector("github"), connector("slack", run_as="deployment")],
        )
        assert RemoteSession._resolve_conversation_run_as(agent) == ConnectorRunAs.DEPLOYMENT

    def test_uniform_run_as_on_agent_is_allowed(self) -> None:
        agent = Agent(
            name="deployment",
            connectors=[
                connector("github", run_as="deployment"),
                connector("slack", run_as="deployment"),
            ],
        )
        # Binding resolution is skipped outside a workflow context.
        RemoteSession._resolve_conversation_run_as(agent)


class TestResolveConversationRunAs:
    def test_no_connectors_defaults_to_auto(self) -> None:
        agent = Agent(name="plain")
        assert RemoteSession._resolve_conversation_run_as(agent) == ConnectorRunAs.AUTO

    def test_uniform_deployment_returns_deployment(self) -> None:
        agent = Agent(name="dep", connectors=[connector("github", run_as="deployment")])
        assert RemoteSession._resolve_conversation_run_as(agent) == ConnectorRunAs.DEPLOYMENT

    def test_connector_on_handoff_child_is_considered(self) -> None:
        child = Agent(name="child", connectors=[connector("github", run_as="deployment")])
        root = Agent(name="root", handoffs=[child])
        assert RemoteSession._resolve_conversation_run_as(root) == ConnectorRunAs.DEPLOYMENT

    def test_mixed_run_as_across_handoff_graph_raises(self) -> None:
        child = Agent(name="child", connectors=[connector("slack", run_as="deployment")])
        root = Agent(name="root", connectors=[connector("github", run_as="auto")], handoffs=[child])
        with pytest.raises(ValueError, match="mixes connector run_as"):
            RemoteSession._resolve_conversation_run_as(root)


class TestInitializeConversationForwardsRunAs:
    @pytest.mark.asyncio
    async def test_deployment_run_as_forwarded_to_create_and_start(self) -> None:
        agent = Agent(name="dep", connectors=[connector("github", run_as="deployment")])
        session = RemoteSession()
        created = MagicMock()
        created.id = "ag_1"
        with (
            patch.object(remote_session, "mistralai_create_agent", AsyncMock(return_value=created)) as create,
            patch.object(remote_session, "mistralai_update_agent", AsyncMock(return_value=created)) as update,
            patch.object(
                remote_session,
                "mistralai_start_conversation",
                AsyncMock(return_value=MagicMock(conversation_id="c", outputs=[])),
            ) as start,
        ):
            await session.initialize_conversation(agent, ["hi"])

        assert create.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT
        assert update.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT
        assert start.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT

    @pytest.mark.asyncio
    async def test_default_connector_uses_binding_run_as_for_create_and_start(self) -> None:
        agent = Agent(name="dep", connectors=[connector("github")])
        session = RemoteSession()
        created = MagicMock()
        created.id = "ag_1"
        ctx = make_context(
            bindings=[
                {
                    "connector_name": "github",
                    "connector_id": "conn-gh",
                    "run_as": "deployment",
                    "status": "ready",
                }
            ]
        )
        with (
            define_context(ctx),
            patch.object(remote_session, "mistralai_create_agent", AsyncMock(return_value=created)) as create,
            patch.object(remote_session, "mistralai_update_agent", AsyncMock(return_value=created)) as update,
            patch.object(
                remote_session,
                "mistralai_start_conversation",
                AsyncMock(return_value=MagicMock(conversation_id="c", outputs=[])),
            ) as start,
        ):
            await session.initialize_conversation(agent, ["hi"])

        assert create.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT
        assert update.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT
        assert start.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT

    @pytest.mark.asyncio
    async def test_no_connectors_forwards_auto(self) -> None:
        agent = Agent(name="plain")
        session = RemoteSession()
        created = MagicMock()
        created.id = "ag_1"
        with (
            patch.object(remote_session, "mistralai_create_agent", AsyncMock(return_value=created)),
            patch.object(
                remote_session,
                "mistralai_start_conversation",
                AsyncMock(return_value=MagicMock(conversation_id="c", outputs=[])),
            ) as start,
        ):
            await session.initialize_conversation(agent, ["hi"])

        assert start.await_args.kwargs["run_as"] == ConnectorRunAs.AUTO

    @pytest.mark.asyncio
    async def test_append_forwards_resolved_run_as(self) -> None:
        session = RemoteSession()
        session._conversation_id = "c"
        session._run_as = ConnectorRunAs.DEPLOYMENT
        with patch.object(
            remote_session,
            "mistralai_append_conversation",
            AsyncMock(return_value=MagicMock(outputs=[])),
        ) as append:
            await session.append_messages(["more"])

        assert append.await_args.kwargs["run_as"] == ConnectorRunAs.DEPLOYMENT


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
