import unittest
import asyncio
import json
from unittest.mock import MagicMock, AsyncMock
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage


class FakeAgent:
    """Minimal stand-in for LangGraphAgent to test _emit_new_subgraph_messages."""

    def __init__(self):
        self.active_run = {
            "id": "run-1",
            "emitted_message_ids": set(),
            "streamed_messages": [],
        }
        self.emitted_events = []

    def _dispatch_event(self, event):
        serialized = json.dumps({"type": event.type.value if hasattr(event.type, 'value') else event.type})
        self.emitted_events.append(event)
        return serialized

    # Bind the real method under test
    from ag_ui_langgraph.agent import LangGraphAgent
    _emit_new_subgraph_messages = LangGraphAgent._emit_new_subgraph_messages


def collect(gen):
    """Consume a sync generator and return the list of yielded values."""
    return list(gen)


class TestEmitNewSubgraphMessages(unittest.TestCase):

    def setUp(self):
        self.agent = FakeAgent()

    def test_emits_three_events_for_new_ai_message(self):
        msg = AIMessage(content="Hello from subgraph", id="msg-1")
        results = collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertEqual(len(results), 3)
        types = [e.type for e in self.agent.emitted_events]
        from ag_ui.core import EventType
        self.assertIn(EventType.TEXT_MESSAGE_START, types)
        self.assertIn(EventType.TEXT_MESSAGE_CONTENT, types)
        self.assertIn(EventType.TEXT_MESSAGE_END, types)

    def test_skips_already_emitted_id(self):
        self.agent.active_run["emitted_message_ids"].add("msg-already")
        msg = AIMessage(content="Should not emit", id="msg-already")
        results = collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertEqual(len(results), 0)

    def test_skips_non_ai_messages(self):
        msgs = [
            HumanMessage(content="user", id="h1"),
            ToolMessage(content="tool result", tool_call_id="tc1", id="t1"),
            SystemMessage(content="system", id="s1"),
        ]
        results = collect(self.agent._emit_new_subgraph_messages(msgs))
        self.assertEqual(len(results), 0)

    def test_skips_ai_message_with_empty_content(self):
        msg = AIMessage(content="", id="tc-msg")
        results = collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertEqual(len(results), 0)

    def test_skips_message_with_no_id(self):
        msg = AIMessage(content="No ID")
        msg.id = None
        results = collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertEqual(len(results), 0)

    def test_registers_emitted_id(self):
        msg = AIMessage(content="New message", id="msg-2")
        collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertIn("msg-2", self.agent.active_run["emitted_message_ids"])

    def test_appends_to_streamed_messages(self):
        msg = AIMessage(content="Streamed", id="msg-3")
        collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertIn(msg, self.agent.active_run["streamed_messages"])

    def test_processes_multiple_skipping_old(self):
        self.agent.active_run["emitted_message_ids"].add("old-1")
        msgs = [
            AIMessage(content="Already seen", id="old-1"),
            AIMessage(content="First new", id="new-1"),
            AIMessage(content="Second new", id="new-2"),
        ]
        collect(self.agent._emit_new_subgraph_messages(msgs))
        from ag_ui.core import EventType
        starts = [e for e in self.agent.emitted_events if e.type == EventType.TEXT_MESSAGE_START]
        self.assertEqual(len(starts), 2)
        self.assertEqual(starts[0].message_id, "new-1")
        self.assertEqual(starts[1].message_id, "new-2")

    def test_does_nothing_when_active_run_is_none(self):
        self.agent.active_run = None
        msg = AIMessage(content="Should not emit", id="msg-x")
        results = collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertEqual(len(results), 0)

    def test_does_not_re_emit_id_pre_registered(self):
        """Simulates OnChatModelEnd having registered the ID."""
        self.agent.active_run["emitted_message_ids"].add("llm-msg-1")
        msg = AIMessage(content="Already streamed via LLM", id="llm-msg-1")
        results = collect(self.agent._emit_new_subgraph_messages([msg]))
        self.assertEqual(len(results), 0)


class TestSubgraphOnChainEndHook(unittest.IsolatedAsyncioTestCase):
    """Integration tests for the on_chain_end → _emit_new_subgraph_messages hook."""

    def _make_agent(self):
        """Return a LangGraphAgent with minimal mocking."""
        from ag_ui_langgraph.agent import LangGraphAgent
        from unittest.mock import MagicMock, AsyncMock, patch

        agent = LangGraphAgent.__new__(LangGraphAgent)
        agent.active_run = {
            "id": "run-1",
            "thread_id": "thread-1",
            "node_name": None,
            "prev_node_name": None,
            "has_function_streaming": False,
            "model_made_tool_call": False,
            "state_reliable": True,
            "streamed_messages": [],
            "emitted_message_ids": set(),
            "manually_emitted_state": None,
            "reasoning_process": None,
            "schema_keys": None,
        }
        agent.messages_in_process = {}
        agent.config = {}
        return agent

    async def _collect_events(self, agent, stream_chunks, stream_subgraphs=True):
        """Drive _handle_stream_events with a fake stream and collect yielded event strings."""
        import json

        # Minimal RunAgentInput mock
        run_input = MagicMock()
        run_input.run_id = "run-1"
        run_input.thread_id = "thread-1"
        run_input.messages = []
        run_input.forwarded_props = {"stream_subgraphs": stream_subgraphs} if stream_subgraphs else {}

        # Stub prepare_stream to return our fake chunks
        async def fake_prepare(*args, **kwargs):
            # Replicate what the real prepare_stream does: set schema_keys on active_run
            agent.active_run["schema_keys"] = {
                "input": ["messages"],
                "output": ["messages"],
                "config": [],
            }
            async def gen():
                for c in stream_chunks:
                    yield c
            return {
                "stream": gen(),
                "state": {"messages": []},
                "config": {"configurable": {"thread_id": "thread-1"}},
            }

        # Stub aget_state (called after stream ends)
        from langchain_core.messages import AIMessage
        final_state = MagicMock()
        final_state.values = {"messages": [AIMessage(content="x", id="msg-sub-1")]}
        final_state.tasks = []
        final_state.next = []
        final_state.metadata = {"writes": {}}

        agent.graph = AsyncMock()
        agent.graph.aget_state = AsyncMock(return_value=final_state)
        agent.prepare_stream = fake_prepare

        collected = []
        async for ev_str in agent._handle_stream_events(run_input):
            collected.append(ev_str)
        return collected

    async def test_emits_text_messages_for_ai_on_chain_end_when_subgraphs_enabled(self):
        from langchain_core.messages import AIMessage
        agent = self._make_agent()

        msg = AIMessage(content="Subgraph message", id="msg-sub-1")
        chunks = [
            {
                "event": "on_chain_end",
                "name": "flights_agent_chat_node",
                "data": {"output": {"messages": [msg]}},
                "metadata": {"langgraph_node": "flights_agent_chat_node"},
                "run_id": "run-1",
            }
        ]

        events = await self._collect_events(agent, chunks, stream_subgraphs=True)
        event_types = []
        for ev in events:
            # _dispatch_event returns event objects directly; extract type string
            if hasattr(ev, "type"):
                t = ev.type
                event_types.append(t.value if hasattr(t, "value") else str(t))
            else:
                try:
                    obj = json.loads(ev)
                    event_types.append(obj.get("type"))
                except Exception:
                    pass

        self.assertIn("TEXT_MESSAGE_START", event_types)
        self.assertIn("TEXT_MESSAGE_CONTENT", event_types)
        self.assertIn("TEXT_MESSAGE_END", event_types)

    async def test_no_text_messages_when_subgraphs_not_enabled(self):
        from langchain_core.messages import AIMessage
        agent = self._make_agent()

        msg = AIMessage(content="Subgraph message", id="msg-sub-2")
        chunks = [
            {
                "event": "on_chain_end",
                "name": "flights_agent_chat_node",
                "data": {"output": {"messages": [msg]}},
                "metadata": {"langgraph_node": "flights_agent_chat_node"},
                "run_id": "run-1",
            }
        ]

        events = await self._collect_events(agent, chunks, stream_subgraphs=False)
        event_types = []
        for ev in events:
            # _dispatch_event returns event objects directly; extract type string
            if hasattr(ev, "type"):
                t = ev.type
                event_types.append(t.value if hasattr(t, "value") else str(t))
            else:
                try:
                    obj = json.loads(ev)
                    event_types.append(obj.get("type"))
                except Exception:
                    pass

        self.assertNotIn("TEXT_MESSAGE_START", event_types)


if __name__ == "__main__":
    unittest.main()
