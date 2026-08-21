"""The tool hook's handling of a call a person has to authorize.

This hook sits in front of every real tool call, so the cases that matter most
where nothing should change.
"""

import asyncio
import time

from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest

from xpander_sdk.modules.agents.models.agent import (
    AgentGraphItemHITLSettings,
    AgentGraphItemType,
    AgentToolApprovalApprovers,
)
from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.modules.tools_repository.models.mcp import MCPServerDetails
from xpander_sdk.modules.backend.frameworks.agno import (
    AWAITING_APPROVAL_MESSAGE,
    _approval_envelope,
    _awaiting_approval_message,
    _is_awaiting_approval,
    _mark_awaiting_approval,
)


class _Task:
    """The little a task has to answer for a tool build."""

    id = "task-1"
    user_tokens = None
    mcp_servers = None
    input = None


_TASK = _Task()

ENVELOPE = {
    "type": "approval_required",
    "request_id": "req-1",
    "message": "waiting on a person",
}


class TestRecognizingTheEnvelope:
    def test_it_recognizes_a_bare_envelope(self) -> None:
        assert _approval_envelope(ENVELOPE) == ENVELOPE

    def test_it_unwraps_a_tool_invocation_result(self) -> None:
        # A connector refusal arrives as a dict under ToolInvocationResult.result.
        wrapped = SimpleNamespace(result=ENVELOPE)
        assert _approval_envelope(wrapped) == ENVELOPE

    def test_it_unwraps_an_agno_content_result(self) -> None:
        assert _approval_envelope(SimpleNamespace(content=ENVELOPE)) == ENVELOPE

    def test_it_stops_before_walking_deeply_nested_payloads(self) -> None:
        deep = SimpleNamespace(
            result=SimpleNamespace(result=SimpleNamespace(result=ENVELOPE))
        )
        assert _approval_envelope(deep) is None

    def test_an_ordinary_dict_result_is_left_alone(self) -> None:
        assert _approval_envelope({"ok": True, "rows": []}) is None

    def test_a_plain_string_result_is_left_alone(self) -> None:
        assert _approval_envelope("sent the email") is None

    def test_none_is_left_alone(self) -> None:
        assert _approval_envelope(None) is None

    def test_a_differently_typed_envelope_is_left_alone(self) -> None:
        # The connector sign-in hold uses the same shape with a different type.
        assert (
            _approval_envelope({"type": "auth_required", "auth_url": "https://x"})
            is None
        )

    def test_a_wrapped_ordinary_result_is_left_alone(self) -> None:
        assert _approval_envelope(SimpleNamespace(result={"rows": []})) is None


class TestRunState:
    def test_a_run_is_not_awaiting_approval_by_default(self) -> None:
        assert not _is_awaiting_approval(SimpleNamespace())
        assert _awaiting_approval_message(SimpleNamespace()) is None

    def test_marking_one_call_blocks_the_run(self) -> None:
        task = SimpleNamespace()
        _mark_awaiting_approval(task, "gmail_send", "gmail is waiting")
        assert _is_awaiting_approval(task)

    def test_a_later_tool_reads_the_original_statement(self) -> None:
        # Naming the second tool would say Slack is waiting when Gmail is.
        task = SimpleNamespace()
        _mark_awaiting_approval(task, "gmail_send", "gmail is waiting")
        assert _awaiting_approval_message(task) == "gmail is waiting"

    def test_marking_is_cumulative_and_does_not_lose_earlier_calls(self) -> None:
        task = SimpleNamespace()
        _mark_awaiting_approval(task, "gmail_send", "gmail is waiting")
        _mark_awaiting_approval(task, "slack_post", "slack is waiting")
        assert set(task._xp_awaiting_approval) == {"gmail_send", "slack_post"}

    def test_bookkeeping_never_raises_on_a_task_that_cannot_hold_state(self) -> None:
        # A frozen or exotic task must not turn into a failed tool call.
        _mark_awaiting_approval(None, "gmail_send", "waiting")
        assert not _is_awaiting_approval(None)


class TestWhatTheModelReads:
    def test_the_message_names_the_tool_and_ends_the_turn(self) -> None:
        message = AWAITING_APPROVAL_MESSAGE.format(tool="gmail_send")
        assert "gmail_send" in message
        assert "has not run" in message
        assert "Finish now" in message

    def test_the_message_carries_no_retry_bait(self) -> None:
        message = AWAITING_APPROVAL_MESSAGE.format(tool="gmail_send").lower()
        for word in ("error", "failed", "denied", "forbidden", "try again", "retry"):
            assert word not in message


class TestMirroredSettings:
    def test_approval_is_off_unless_switched_on(self) -> None:
        assert AgentGraphItemHITLSettings().enabled is False

    def test_named_people_and_groups_round_trip(self) -> None:
        settings = AgentGraphItemHITLSettings(
            enabled=True,
            approvers=AgentToolApprovalApprovers(user_ids=["u1"], group_ids=["g1"]),
        )
        assert settings.approvers.user_ids == ["u1"]
        assert settings.approvers.group_ids == ["g1"]

    def test_a_denied_call_lets_the_run_continue_by_default(self) -> None:
        assert AgentGraphItemHITLSettings().on_deny == "continue"


class TestASettledRefusalDoesNotStopTheRun:
    """on_deny defaults to continue: the run finishes and reports what it skipped."""

    def test_a_denied_envelope_is_still_recognized(self) -> None:
        denied = {**ENVELOPE, "denied": True, "message": "declined"}
        assert _approval_envelope(denied) == denied

    def test_a_denied_envelope_carries_the_flag_the_hook_branches_on(self) -> None:
        # Marking the run on a refusal would block every remaining ungated call
        # and tell the user something is pending when nothing is.
        assert {**ENVELOPE, "denied": True}.get("denied") is True
        assert ENVELOPE.get("denied") is None


class TestTheRefusalFeedsTheBreaker:
    def test_the_refusal_joins_the_no_progress_markers(self) -> None:
        from xpander_sdk.modules.backend.frameworks.agno import _NO_PROGRESS_MARKERS

        message = AWAITING_APPROVAL_MESSAGE.format(tool="gmail_send")
        assert any(marker in message for marker in _NO_PROGRESS_MARKERS)


class TestASuppressedAttemptIsNotAnEvent:
    """A held run must not read as an agent retrying against its own gate."""

    @staticmethod
    def _guard_block() -> str:
        """The awaiting-approval guard, up to the next guard that follows it."""
        source = Path(agno_module.__file__).read_text()
        start = source.index("_is_awaiting_approval(task)")
        end = source.index("_is_tool_disabled(task, eff_name)", start)
        return source[start:end]

    def test_the_approval_block_reports_nothing(self) -> None:
        """The guard writes no activity entry for a call it refused."""
        # A suppressed attempt logged as a failed call reads as a retry against the gate.
        assert "_report_blocked_call" not in self._guard_block()

    def test_the_guard_after_it_still_reports(self) -> None:
        """Only the approval case is quiet; every other guard still emits."""
        # Silence was the original bug there: a stuck run looked like nothing was happening.
        source = Path(agno_module.__file__).read_text()
        after = source[source.index("_is_tool_disabled(task, eff_name)") :]
        assert "_report_blocked_call" in after[:2000]


class TestHoldingASelfApproveCallOpen:
    """Nobody was asked but the person watching, so the call waits instead of the run parking."""

    def _agent(self) -> SimpleNamespace:
        """The minimum an agent needs to be polled against: an id and a configuration."""
        return SimpleNamespace(id="agent-1", configuration=SimpleNamespace())

    @pytest.mark.asyncio
    async def test_it_returns_the_decision_once_the_person_answers(
        self, monkeypatch: Any
    ) -> None:
        answers = [{"settled": False}, {"settled": True, "approved": True}]

        class _Client:
            """A platform that answers pending, then settled."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Return the next scripted status."""
                return answers.pop(0)

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        out = await agno_module._await_self_approval(self._agent(), "req-1", 30)
        assert out == {"settled": True, "approved": True}

    @pytest.mark.asyncio
    async def test_it_gives_up_at_the_window_rather_than_holding_forever(
        self, monkeypatch: Any
    ) -> None:
        class _Client:
            """A platform where nobody ever answers."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Never settle."""
                return {"settled": False}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        # None is not a failure: the caller falls through and parks exactly as it always did.
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", 0.05) is None
        )

    @pytest.mark.asyncio
    async def test_a_platform_blip_costs_the_poll_and_not_the_hold(
        self, monkeypatch: Any
    ) -> None:
        calls = {"n": 0}

        class _Client:
            def __init__(self, **_kw):
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Fail once, then settle."""
                calls["n"] += 1
                if calls["n"] == 1:
                    raise RuntimeError("connection reset")
                return {"settled": True, "approved": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        out = await agno_module._await_self_approval(self._agent(), "req-1", 30)
        assert out and out["approved"] is True

    @pytest.mark.asyncio
    async def test_no_window_means_no_hold_at_all(self, monkeypatch: Any) -> None:
        # An envelope with no wait_seconds is the old shape and must behave like the old shape.
        called = {"n": 0}

        class _Client:
            """Records that it was constructed at all, which it must not be."""

            def __init__(self, **_kw) -> None:
                called["n"] += 1

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Would settle, if it were ever reached."""
                return {"settled": True, "approved": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", None) is None
        )
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", "nonsense")
            is None
        )
        assert called["n"] == 0

    @pytest.mark.asyncio
    async def test_it_never_holds_longer_than_its_own_ceiling(
        self, monkeypatch: Any
    ) -> None:
        # The window comes off the wire, so an absurd value must not strand a worker.
        waited = []

        class _Client:
            """A platform that never settles, to prove the ceiling ends the hold."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Never settle."""
                waited.append(1)
                return {"settled": False}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_MAX_WAIT_SECONDS", 0.05)
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", 10_000)
            is None
        )

    @pytest.mark.asyncio
    async def test_one_slow_poll_cannot_outlive_the_window(
        self, monkeypatch: Any
    ) -> None:
        """A hung request must end with the hold, not with the client's own long timeout."""

        class _Client:
            """A platform that accepts the request and never answers it."""

            def __init__(self, **_kw) -> None:
                pass

            async def make_request(self, **_kw) -> Dict[str, Any]:
                """Hang for far longer than any hold window."""
                await asyncio.sleep(60)
                return {"settled": True, "approved": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        monkeypatch.setattr(agno_module, "SELF_APPROVE_POLL_SECONDS", 0)
        started = time.monotonic()
        assert (
            await agno_module._await_self_approval(self._agent(), "req-1", 0.2) is None
        )
        assert time.monotonic() - started < 5


class TestWhatTheModelReadsWhenSomeoneSaysNo:
    """A decline is a settled fact with a next step, never an error to retry against."""

    def test_it_names_the_decider_and_offers_a_way_on(self) -> None:
        message = agno_module._declined_message(
            {"decided_by_name": "Dana Cohen"}, "gmail_send"
        )
        assert "Dana Cohen declined" in message
        assert "gmail_send" in message
        assert "answer now" in message

    def test_it_carries_the_reason_when_one_was_given(self) -> None:
        message = agno_module._declined_message(
            {"decided_by_name": "Dana", "decision_note": "wrong recipient list"},
            "gmail_send",
        )
        assert 'They said: "wrong recipient list"' in message

    def test_it_reads_fine_when_nobody_is_named(self) -> None:
        message = agno_module._declined_message({}, "gmail_send")
        assert message.startswith("The person who was asked declined")


class TestWhichMcpServersCarryARule:
    """Only a server with an enabled rule is gated, because gating costs a connect."""

    def _agent(self, *items: Any) -> Any:
        """An agent whose graph is exactly the items given."""
        return SimpleNamespace(graph=SimpleNamespace(items=list(items)))

    def _item(self, item_id: str, name: str, url: str, hitl: Any) -> Any:
        """One MCP server node, gated or not according to the rule passed in."""
        return SimpleNamespace(
            item_id=item_id,
            name=name,
            type=AgentGraphItemType.MCP,
            settings=SimpleNamespace(
                hitl_options=hitl, mcp_settings=SimpleNamespace(url=url)
            ),
        )

    def test_an_enabled_rule_makes_the_server_gated(self) -> None:
        agent = self._agent(
            self._item(
                "srv-1",
                "Linear",
                "https://mcp.linear.app",
                AgentGraphItemHITLSettings(enabled=True),
            )
        )
        gated = agno_module._mcp_gated_servers(agent)
        assert len(gated) == 1
        item_id, keys, _scoped = gated[0]
        assert item_id == "srv-1"
        # Every name the server can be known by: the toolkit is built from mcp_settings while
        # the node carries its own display name, and the two are not required to agree.
        assert keys.count("https://mcp.linear.app") == 1
        assert keys.count("linear") == 1

    def test_a_rule_that_is_off_gates_nothing(self) -> None:
        agent = self._agent(
            self._item(
                "srv-1",
                "Linear",
                "https://mcp.linear.app",
                AgentGraphItemHITLSettings(enabled=False),
            )
        )
        assert agno_module._mcp_gated_servers(agent) == []

    def test_a_server_with_no_settings_gates_nothing(self) -> None:
        agent = self._agent(self._item("srv-1", "Linear", "", None))
        assert agno_module._mcp_gated_servers(agent) == []

    def test_a_connector_node_is_never_read_as_an_mcp_server(self) -> None:
        item = self._item("op-1", "Gmail", "", AgentGraphItemHITLSettings(enabled=True))
        item.type = AgentGraphItemType.TOOL
        assert agno_module._mcp_gated_servers(self._agent(item)) == []

    def test_an_agent_with_no_graph_gates_nothing(self) -> None:
        assert agno_module._mcp_gated_servers(SimpleNamespace()) == []


class TestTheToolNameOnTheCard:
    def test_the_shared_prefix_is_stripped(self) -> None:
        # Every MCP toolkit prefixes identically, so the prefix says nothing to a person.
        assert (
            agno_module._unprefixed_mcp_tool("mcp_tool_delete_issue") == "delete_issue"
        )

    def test_a_name_without_the_prefix_is_left_alone(self) -> None:
        assert agno_module._unprefixed_mcp_tool("delete_issue") == "delete_issue"


class TestAskingThePlatformBeforeDispatch:
    """The check itself: what it sends, and what it does when it cannot be sent."""

    def _agent(self) -> Any:
        """The little the check reads off an agent."""
        return SimpleNamespace(id="agent-1", configuration=SimpleNamespace())

    def test_it_sends_the_server_the_tool_and_the_arguments(
        self, monkeypatch: Any
    ) -> None:
        sent: Dict[str, Any] = {}

        class _Client:
            def __init__(self, configuration: Any = None) -> None:
                pass

            async def make_request(
                self, path: str, method: str, payload: Any = None, **kw: Any
            ) -> Dict[str, Any]:
                sent["path"] = path
                sent["method"] = method
                sent["payload"] = payload
                return {"allowed": True}

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        result = asyncio.run(
            agno_module._check_mcp_approval(
                self._agent(),
                SimpleNamespace(id="task-1"),
                "srv-1",
                "delete_issue",
                {"id": "ENG-1"},
            )
        )
        assert result is None
        assert sent["path"] == "/agents/agent-1/tool-approvals/check"
        assert sent["method"] == "POST"
        # The arguments travel because the approval binds to them.
        assert sent["payload"] == {
            "execution_id": "task-1",
            "operation_id": "srv-1",
            "tool_name": "delete_issue",
            "payload": {"id": "ENG-1"},
        }

    def test_a_held_call_comes_back_as_the_envelope(self, monkeypatch: Any) -> None:
        class _Client:
            def __init__(self, configuration: Any = None) -> None:
                pass

            async def make_request(self, **kw: Any) -> Dict[str, Any]:
                return ENVELOPE

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        result = asyncio.run(
            agno_module._check_mcp_approval(
                self._agent(), SimpleNamespace(id="task-1"), "srv-1", "delete_issue", {}
            )
        )
        assert result == ENVELOPE

    def test_an_unreachable_check_refuses_the_call(self, monkeypatch: Any) -> None:
        # Fails closed: letting it through performs the very action a person was to authorize.
        class _Client:
            def __init__(self, configuration: Any = None) -> None:
                pass

            async def make_request(self, **kw: Any) -> Dict[str, Any]:
                raise RuntimeError("connection reset")

        monkeypatch.setattr(agno_module, "APIClient", _Client)
        result = asyncio.run(
            agno_module._check_mcp_approval(
                self._agent(), SimpleNamespace(id="task-1"), "srv-1", "delete_issue", {}
            )
        )
        assert result is not None
        assert result["denied"] is True
        assert "delete_issue" in result["message"]

    def test_the_refusal_never_reads_as_an_error(self) -> None:
        # A failure tone here buys a retry flail on what is usually a brief platform blip.
        message = agno_module.MCP_APPROVAL_UNAVAILABLE_MESSAGE.format(
            tool="delete_issue"
        )
        assert "error" not in message.lower()
        assert "failed" not in message.lower()
        # It has to end somewhere the model can actually go.
        assert "finish now" in message.lower()


class TestAnAgentWithNoRulesPaysNothing:
    """The hook runs on every tool call on the platform; the ungated path must not change."""

    def test_no_gated_server_means_the_check_is_never_reached(self) -> None:
        source = Path(agno_module.__file__).read_text()
        block = source[
            source.index("if _mcp_gate_map:") : source.index(
                "_check_mcp_approval(", source.index("if _mcp_gate_map:")
            )
        ]
        # An empty map short-circuits before anything else: no lookup, no name work, no call.
        assert block.index("if _mcp_gate_map:") < block.index(
            "_mcp_gate_map.get(eff_name)"
        )

    def test_an_agent_with_no_gated_server_builds_an_empty_map(self) -> None:
        agent = SimpleNamespace(
            graph=SimpleNamespace(
                items=[
                    SimpleNamespace(
                        item_id="srv-1",
                        name="Linear",
                        type=AgentGraphItemType.MCP,
                        settings=SimpleNamespace(
                            hitl_options=None,
                            mcp_settings=SimpleNamespace(url="https://mcp.linear.app"),
                        ),
                    )
                ]
            )
        )
        assert agno_module._mcp_gated_servers(agent) == []

    def test_a_local_server_is_recognised_by_its_command(self) -> None:
        # A stdio server has no url, and the toolkit is named by mcp.name or mcp.command.
        agent = SimpleNamespace(
            graph=SimpleNamespace(
                items=[
                    SimpleNamespace(
                        item_id="srv-2",
                        name="Files",
                        type=AgentGraphItemType.MCP,
                        settings=SimpleNamespace(
                            hitl_options=AgentGraphItemHITLSettings(enabled=True),
                            mcp_settings=SimpleNamespace(
                                url=None, name=None, command="uvx mcp-server-files"
                            ),
                        ),
                    )
                ]
            )
        )
        _, keys, _scoped = agno_module._mcp_gated_servers(agent)[0]
        assert "uvx mcp-server-files" in keys
        assert "files" in keys

    def test_settings_that_arrive_as_a_dict_are_read_the_same_way(self) -> None:
        agent = SimpleNamespace(
            graph=SimpleNamespace(
                items=[
                    SimpleNamespace(
                        item_id="srv-3",
                        name="Linear",
                        type=AgentGraphItemType.MCP,
                        settings=SimpleNamespace(
                            hitl_options=AgentGraphItemHITLSettings(enabled=True),
                            mcp_settings={"url": "https://mcp.linear.app"},
                        ),
                    )
                ]
            )
        )
        _, keys, _scoped = agno_module._mcp_gated_servers(agent)[0]
        assert keys.count("https://mcp.linear.app") == 1


class TestAGatedServerThatCannotBeListed:
    """A tool nothing can recognise is a tool that would run without ever being held."""

    @staticmethod
    def _agent(hitl: Any) -> Any:
        """An agent with one remote MCP server, gated or not according to its rule."""
        return SimpleNamespace(
            id="agent-1",
            mcp_servers=[MCPServerDetails(url="https://mcp.linear.app", name="Linear")],
            tools=SimpleNamespace(functions=[]),
            graph=SimpleNamespace(
                items=[
                    SimpleNamespace(
                        item_id="srv-1",
                        name="Linear",
                        type=AgentGraphItemType.MCP,
                        settings=SimpleNamespace(
                            hitl_options=hitl,
                            mcp_settings=SimpleNamespace(
                                url="https://mcp.linear.app",
                                name="Linear",
                                command=None,
                            ),
                        ),
                    )
                ]
            ),
            pre_auth_audiences=None,
            oidc_pre_auth_token_mcp_audience=None,
        )

    @staticmethod
    def _unlistable_toolkit(closed: List[bool]) -> Any:
        """An MCPTools stand-in whose session refuses to open."""

        class _Toolkit:
            initialized = False
            functions: Dict[str, Any] = {}

            def __init__(self, **kwargs: Any) -> None:
                pass

            async def connect(self) -> None:
                raise RuntimeError("connection reset")

            async def close(self) -> None:
                closed.append(True)

        return _Toolkit

    def test_a_gated_server_is_withheld_rather_than_run_ungated(
        self, monkeypatch: Any
    ) -> None:
        closed: List[bool] = []

        async def _healthy(
            url: str, headers: Any = None, transport: str = "streamable-http"
        ) -> None:
            return None

        monkeypatch.setattr(agno_module, "probe_mcp_server", _healthy)
        monkeypatch.setattr("agno.tools.mcp.MCPTools", self._unlistable_toolkit(closed))

        notes: List[str] = []
        tools = asyncio.run(
            agno_module._resolve_agent_tools(
                agent=self._agent(AgentGraphItemHITLSettings(enabled=True)),
                skipped_notes=notes,
                mcp_gate_map={},
            )
        )
        assert tools == []
        assert closed == [True]
        assert any("Linear" in note and "approval" in note for note in notes)
        # The note has to end somewhere the model can go, not describe an absence and stop.
        assert any("answer now" in note for note in notes)

    def test_an_ungated_server_is_left_exactly_as_it_was(
        self, monkeypatch: Any
    ) -> None:
        closed: List[bool] = []

        async def _healthy(
            url: str, headers: Any = None, transport: str = "streamable-http"
        ) -> None:
            return None

        monkeypatch.setattr(agno_module, "probe_mcp_server", _healthy)
        monkeypatch.setattr("agno.tools.mcp.MCPTools", self._unlistable_toolkit(closed))

        gate_map: Dict[str, str] = {}
        tools = asyncio.run(
            agno_module._resolve_agent_tools(
                agent=self._agent(AgentGraphItemHITLSettings(enabled=False)),
                skipped_notes=[],
                mcp_gate_map=gate_map,
            )
        )
        # Never connected, never closed, handed to agno as before: the ungated path is untouched.
        assert len(tools) == 1
        assert closed == []
        assert gate_map == {}


class TestWhichServerAToolBelongsTo:
    """Getting this wrong asks the wrong people, or asks nobody at all."""

    @staticmethod
    def _listable_toolkit(by_server: Dict[str, List[str]], built: List[Any]) -> Any:
        """An MCPTools stand-in exposing a different tool per server, keyed by its params."""

        class _Toolkit:
            def __init__(self, **kwargs: Any) -> None:
                params = kwargs.get("server_params")
                key = str(
                    getattr(params, "url", None) or getattr(params, "command", "")
                )
                self.initialized = False
                self.functions = {name: object() for name in by_server.get(key, [])}
                built.append(self)

            async def connect(self) -> None:
                self.initialized = True

            async def close(self) -> None:
                self.initialized = False

        return _Toolkit

    @staticmethod
    def _agent(*servers: Any) -> Any:
        """An agent whose graph items and live servers are given pairwise."""
        return SimpleNamespace(
            id="agent-1",
            mcp_servers=[live for _item, live in servers],
            tools=SimpleNamespace(functions=[]),
            graph=SimpleNamespace(items=[item for item, _live in servers]),
            pre_auth_audiences=None,
            oidc_pre_auth_token_mcp_audience=None,
        )

    @staticmethod
    def _node(item_id: str, name: str, url: Optional[str], enabled: bool) -> Any:
        """One MCP server node in the graph."""
        return SimpleNamespace(
            item_id=item_id,
            id=item_id,
            name=name,
            type=AgentGraphItemType.MCP,
            settings=SimpleNamespace(
                hitl_options=AgentGraphItemHITLSettings(enabled=enabled),
                mcp_settings=SimpleNamespace(url=url, name=name, command=None),
            ),
        )

    def _resolve(
        self,
        agent: Any,
        by_server: Dict[str, List[str]],
        monkeypatch: Any,
        built: Optional[List[Any]] = None,
    ) -> Dict[str, str]:
        async def _healthy(
            url: str, headers: Any = None, transport: str = "streamable-http"
        ) -> None:
            return None

        monkeypatch.setattr(agno_module, "probe_mcp_server", _healthy)
        monkeypatch.setattr(
            "agno.tools.mcp.MCPTools",
            self._listable_toolkit(by_server, built if built is not None else []),
        )
        gate_map: Dict[str, str] = {}
        asyncio.run(
            agno_module._resolve_agent_tools(
                agent=agent, task=_TASK, skipped_notes=[], mcp_gate_map=gate_map
            )
        )
        return gate_map

    def test_an_ungated_server_sharing_a_name_does_not_inherit_the_rule(
        self, monkeypatch: Any
    ) -> None:
        # Two servers share a display name and differ by url. Only the first is gated, so
        # falling back to the name for the second would hand it another server's rule.
        agent = self._agent(
            (
                self._node("srv-1", "Tools", "https://gated.example/mcp", True),
                MCPServerDetails(url="https://gated.example/mcp", name="Tools"),
            ),
            (
                self._node("srv-2", "Tools", "https://other.example/mcp", False),
                MCPServerDetails(url="https://other.example/mcp", name="Tools"),
            ),
        )
        gate_map = self._resolve(
            agent,
            {
                "https://gated.example/mcp": ["mcp_tool_gated"],
                "https://other.example/mcp": ["mcp_tool_free"],
            },
            monkeypatch,
        )
        assert gate_map == {"mcp_tool_gated": "srv-1"}

    def test_two_gated_servers_sharing_a_tool_name_keep_the_first_claim(
        self, monkeypatch: Any
    ) -> None:
        agent = self._agent(
            (
                self._node("srv-1", "First", "https://first.example/mcp", True),
                MCPServerDetails(url="https://first.example/mcp", name="First"),
            ),
            (
                self._node("srv-2", "Second", "https://second.example/mcp", True),
                MCPServerDetails(url="https://second.example/mcp", name="Second"),
            ),
        )
        gate_map = self._resolve(
            agent,
            {
                "https://first.example/mcp": ["mcp_tool_run"],
                "https://second.example/mcp": ["mcp_tool_run"],
            },
            monkeypatch,
        )
        # Both are gated, so either way a person is asked; the ambiguity is logged, not silent.
        assert gate_map == {"mcp_tool_run": "srv-1"}

    def test_enumeration_does_not_hand_agno_a_connected_toolkit(
        self, monkeypatch: Any
    ) -> None:
        # agno closes only sessions it opened itself, so a pre-connected toolkit leaks its
        # session every run. Enumeration opens one, reads the names, and releases it.
        agent = self._agent(
            (
                self._node("srv-1", "Linear", "https://mcp.linear.app", True),
                MCPServerDetails(url="https://mcp.linear.app", name="Linear"),
            )
        )
        built: List[Any] = []
        gate_map = self._resolve(
            agent, {"https://mcp.linear.app": ["mcp_tool_run"]}, monkeypatch, built
        )
        assert gate_map == {"mcp_tool_run": "srv-1"}
        assert built and all(not toolkit.initialized for toolkit in built)


class TestTheCallIsLinkedToItsApproval:
    """The activity row can only carry the decision if the result event names the request."""

    def test_the_result_model_carries_the_link(self) -> None:
        """The optional field exists and round-trips."""
        from xpander_sdk.models.events import ToolCallResult

        event = ToolCallResult(
            request_id="act-1",
            operation_id="op-1",
            result="waiting",
            approval_request_id="req-9",
        )
        assert event.approval_request_id == "req-9"

    def test_an_ordinary_result_carries_nothing(self) -> None:
        """An envelope-less result stays exactly as it was."""
        from xpander_sdk.models.events import ToolCallResult

        event = ToolCallResult(request_id="act-1", operation_id="op-1", result="ok")
        assert event.approval_request_id is None

    @pytest.mark.asyncio
    async def test_report_threads_it_through(self, monkeypatch: Any) -> None:
        """report_tool_call_result passes the link onto the pushed event."""
        from xpander_sdk.modules.backend.utils import tool_call_events as mod

        pushed: Dict[str, Any] = {}

        async def _capture(task: Any, event_type: Any, data: Any) -> None:
            """Record what would have been pushed."""
            pushed["data"] = data

        monkeypatch.setattr(mod, "_push_event", _capture)
        monkeypatch.setattr(mod, "TOOL_CALL_SUMMARY_PREWARM_ENABLED", False)
        await mod.report_tool_call_result(
            task=SimpleNamespace(id="t1"),
            request_id="act-1",
            operation_id="op-1",
            result="The action needs a person to approve it.",
            approval_request_id="req-9",
        )
        assert pushed["data"].approval_request_id == "req-9"

    @pytest.mark.asyncio
    async def test_report_defaults_to_no_link(self, monkeypatch: Any) -> None:
        """Without the argument the event carries nothing new."""
        from xpander_sdk.modules.backend.utils import tool_call_events as mod

        pushed: Dict[str, Any] = {}

        async def _capture(task: Any, event_type: Any, data: Any) -> None:
            """Record what would have been pushed."""
            pushed["data"] = data

        monkeypatch.setattr(mod, "_push_event", _capture)
        monkeypatch.setattr(mod, "TOOL_CALL_SUMMARY_PREWARM_ENABLED", False)
        await mod.report_tool_call_result(
            task=SimpleNamespace(id="t1"),
            request_id="act-1",
            operation_id="op-1",
            result={"ok": True},
        )
        assert pushed["data"].approval_request_id is None


class TestARuleScopedToNamedTools:
    """tool_names on the rule maps only those tools; the rest stay off the map entirely."""

    @staticmethod
    def _agent(tool_names: Optional[List[str]]) -> Any:
        """One gated remote server whose rule is scoped to the given names."""
        return SimpleNamespace(
            id="agent-1",
            mcp_servers=[MCPServerDetails(url="https://mcp.linear.app", name="Linear")],
            tools=SimpleNamespace(functions=[]),
            graph=SimpleNamespace(
                items=[
                    SimpleNamespace(
                        item_id="srv-1",
                        name="Linear",
                        type=AgentGraphItemType.MCP,
                        settings=SimpleNamespace(
                            hitl_options=AgentGraphItemHITLSettings(
                                enabled=True, tool_names=tool_names
                            ),
                            mcp_settings=SimpleNamespace(
                                url="https://mcp.linear.app",
                                name="Linear",
                                command=None,
                            ),
                        ),
                    )
                ]
            ),
            pre_auth_audiences=None,
            oidc_pre_auth_token_mcp_audience=None,
        )

    def _gate_map(
        self, tool_names: Optional[List[str]], monkeypatch: Any
    ) -> Dict[str, str]:
        """The map the resolver builds for one scoped server exposing two tools."""

        async def _healthy(
            url: str, headers: Any = None, transport: str = "streamable-http"
        ) -> None:
            """A probe that always answers healthy."""
            return None

        class _Toolkit:
            """An MCPTools stand-in exposing two fixed tools."""

            def __init__(self, **kwargs: Any) -> None:
                self.initialized = False
                self.functions = {
                    "mcp_tool_create_issue": object(),
                    "mcp_tool_delete_issue": object(),
                }

            async def connect(self) -> None:
                self.initialized = True

            async def close(self) -> None:
                self.initialized = False

        monkeypatch.setattr(agno_module, "probe_mcp_server", _healthy)
        monkeypatch.setattr("agno.tools.mcp.MCPTools", _Toolkit)
        gate_map: Dict[str, str] = {}
        asyncio.run(
            agno_module._resolve_agent_tools(
                agent=self._agent(tool_names),
                task=_TASK,
                skipped_notes=[],
                mcp_gate_map=gate_map,
            )
        )
        return gate_map

    def test_only_the_listed_tool_is_mapped(self, monkeypatch: Any) -> None:
        # No entry means no check and no round-trip: an unlisted tool costs what an ungated
        # one costs, which is the whole point of scoping.
        gate_map = self._gate_map(["delete_issue"], monkeypatch)
        assert gate_map == {"mcp_tool_delete_issue": "srv-1"}

    def test_an_empty_list_maps_every_tool(self, monkeypatch: Any) -> None:
        for tool_names in (None, [], [" "]):
            gate_map = self._gate_map(tool_names, monkeypatch)
            assert set(gate_map) == {
                "mcp_tool_create_issue",
                "mcp_tool_delete_issue",
            }, f"tool_names={tool_names!r} should map everything"
