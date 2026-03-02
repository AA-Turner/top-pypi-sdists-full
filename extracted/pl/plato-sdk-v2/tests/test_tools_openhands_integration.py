"""Integration tests: save_tools → OpenHands custom tools.

Verifies that pickled plato tools can be loaded and registered as
OpenHands custom tools. Uses the OpenHands SDK directly.

Tests marked with @pytest.mark.e2e require ANTHROPIC_API_KEY and make real LLM calls.
"""

import json
import os
import tempfile
from collections.abc import Sequence
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from openhands.sdk import LLM, Action, Agent, Conversation, Observation, TextContent
from openhands.sdk import ToolDefinition as OHToolDefinition
from openhands.sdk.tool import Tool, ToolExecutor, register_tool
from openhands.sdk.tool.registry import resolve_tool
from pydantic import Field, SecretStr

from plato.tools import ToolDefinition, get_workspace, load_tools, save_tools, set_workspace

DEFAULT_TOOLS_FILE = ".plato/tools.pkl"

_TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _register_plato_tools(tmpdir: str):
    """Load pickled tools and register them as OpenHands custom tools."""
    tools_path = Path(tmpdir) / DEFAULT_TOOLS_FILE
    plato_tools = load_tools(tools_path, workspace=tmpdir)

    for td in plato_tools:
        props = td.input_schema.get("properties", {})
        required = set(td.input_schema.get("required", []))
        annotations = {}
        namespace = {}
        for prop_name, prop_schema in props.items():
            py_type = _TYPE_MAP.get(prop_schema.get("type", "string"), str)
            desc = prop_schema.get("description", "")
            if prop_name in required:
                annotations[prop_name] = py_type
                namespace[prop_name] = Field(description=desc)
            else:
                annotations[prop_name] = py_type | None
                namespace[prop_name] = Field(default=prop_schema.get("default"), description=desc)
        namespace["__annotations__"] = annotations

        # Override serializer to avoid recursion in DiscriminatedUnionMixin
        # (dynamic classes created via type() don't match Pydantic's handler repr check)
        def _serialize_action(self, handler, info):
            return handler(self)

        namespace["_serialize_by_kind"] = _serialize_action

        action_cls = type(f"{td.name}_Action", (Action,), namespace)

        def _make_obs_cls(name):
            class PlatoObs(Observation):
                result: str = Field(default="")

                @property
                def to_llm_content(self) -> Sequence[TextContent]:
                    return [TextContent(text=self.result)]

                def _serialize_by_kind(self, handler, info):
                    return handler(self)

            PlatoObs.__name__ = f"{name}_Observation"
            PlatoObs.__qualname__ = f"{name}_Observation"
            return PlatoObs

        obs_cls = _make_obs_cls(td.name)

        def _make_executor(handler, _obs_cls):
            class PlatoExecutor(ToolExecutor):
                def __call__(self, action, conversation=None):
                    input_data = action.model_dump(exclude_none=True)
                    result = handler(input_data)
                    if isinstance(result, dict):
                        text = json.dumps(result, default=str)
                    else:
                        text = str(result)
                    return _obs_cls(result=text)

            return PlatoExecutor()

        executor = _make_executor(td.handler, obs_cls)

        # Register as a factory callable (option 3 in register_tool)
        def _make_factory(a_cls, o_cls, exc, desc, tool_name):
            def factory(conv_state):
                # Create concrete subclass with create() implemented
                class PlatoTool(OHToolDefinition[a_cls, o_cls]):
                    name = tool_name

                    @classmethod
                    def create(cls, conv_state, **kwargs):
                        return [cls(description=desc, action_type=a_cls, observation_type=o_cls, executor=exc)]

                return PlatoTool.create(conv_state)

            return factory

        register_tool(td.name, _make_factory(action_cls, obs_cls, executor, td.description, td.name))


def _save(tools, workspace):
    save_tools(tools, Path(workspace) / DEFAULT_TOOLS_FILE)


def test_register_simple_tool():
    """A simple tool gets registered and can be instantiated via OpenHands SDK."""
    tools = [
        ToolDefinition(
            name="add_numbers",
            description="Add two numbers",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First number"},
                    "b": {"type": "integer", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            handler=lambda x: {"sum": x["a"] + x["b"]},
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        _register_plato_tools(tmpdir)

        conv_state = MagicMock()
        tool_defs = resolve_tool(Tool(name="add_numbers"), conv_state)
        assert len(tool_defs) == 1
        assert tool_defs[0].description == "Add two numbers"

    set_workspace("/workspace")


def test_registered_tool_executor_works():
    """The executor actually calls the pickled handler and returns correct results."""
    inventory = {"banana": 0.75, "apple": 1.50}

    def lookup(input_data: dict) -> dict:
        item = input_data["item"]
        return {"item": item, "price": inventory.get(item, "unknown")}

    tools = [
        ToolDefinition(
            name="lookup_price",
            description="Look up item price",
            input_schema={
                "type": "object",
                "properties": {"item": {"type": "string", "description": "Item name"}},
                "required": ["item"],
            },
            handler=lookup,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        _register_plato_tools(tmpdir)

        conv_state = MagicMock()
        td = resolve_tool(Tool(name="lookup_price"), conv_state)[0]

        action = td.action_type(item="banana")
        observation = td.executor(action)
        assert "0.75" in observation.result

    set_workspace("/workspace")


def test_registered_tool_with_closure():
    """Tools with closures over data survive pickling and work via OpenHands."""
    data = {f"key_{i}": f"value_{i}" for i in range(100)}

    def handler(input_data: dict) -> str:
        return data.get(input_data["key"], "not found")

    tools = [
        ToolDefinition(
            name="data_lookup",
            description="Look up data by key",
            input_schema={
                "type": "object",
                "properties": {"key": {"type": "string"}},
                "required": ["key"],
            },
            handler=handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        _register_plato_tools(tmpdir)

        conv_state = MagicMock()
        td = resolve_tool(Tool(name="data_lookup"), conv_state)[0]

        action = td.action_type(key="key_42")
        observation = td.executor(action)
        assert observation.result == "value_42"

    set_workspace("/workspace")


def test_registered_tool_with_workspace():
    """Tools using get_workspace() resolve correctly via OpenHands bridge."""

    def handler(input_data: dict) -> str:
        ws = get_workspace()
        return str(ws / "output.txt")

    tools = [
        ToolDefinition(
            name="ws_tool",
            description="Uses workspace",
            input_schema={"type": "object", "properties": {}},
            handler=handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        _register_plato_tools(tmpdir)

        conv_state = MagicMock()
        td = resolve_tool(Tool(name="ws_tool"), conv_state)[0]

        action = td.action_type()
        observation = td.executor(action)
        assert observation.result == str(Path(tmpdir) / "output.txt")

    set_workspace("/workspace")


def test_observation_to_llm_content():
    """Observations have proper to_llm_content for LLM consumption."""
    tools = [
        ToolDefinition(
            name="content_tool",
            description="Returns content",
            input_schema={"type": "object", "properties": {}},
            handler=lambda d: "hello from tool",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        _register_plato_tools(tmpdir)

        conv_state = MagicMock()
        td = resolve_tool(Tool(name="content_tool"), conv_state)[0]
        obs = td.executor(td.action_type())

        llm_content = obs.to_llm_content
        assert len(llm_content) == 1
        assert isinstance(llm_content[0], TextContent)
        assert llm_content[0].text == "hello from tool"

    set_workspace("/workspace")


# =============================================================================
# End-to-end tests: actual OpenHands agent conversation with custom tools
# =============================================================================

ANTHROPIC_API_KEY = os.environ.get(
    "ANTHROPIC_API_KEY",
    "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",
)


@pytest.mark.e2e
def test_e2e_agent_uses_custom_tool():
    """An actual OpenHands agent conversation that calls a custom plato tool."""
    call_log = []

    def add_handler(input_data: dict) -> dict:
        call_log.append(input_data)
        return {"sum": input_data["a"] + input_data["b"]}

    tools = [
        ToolDefinition(
            name="add_numbers_e2e",
            description="Add two numbers together. Returns a JSON object with the sum.",
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First number"},
                    "b": {"type": "integer", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
            handler=add_handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        _register_plato_tools(tmpdir)

        llm = LLM(
            model="anthropic/claude-haiku-4-5-20251001",
            api_key=SecretStr(ANTHROPIC_API_KEY),
        )

        agent = Agent(
            llm=llm,
            tools=[Tool(name="add_numbers_e2e")],
        )

        conversation = Conversation(agent=agent, workspace=tmpdir)
        conversation.send_message("Use the add_numbers_e2e tool to add 17 and 25. Report the result from the tool.")
        conversation.run()

        # Verify the agent called the tool and got correct results
        action_events = [e for e in conversation.state.events if hasattr(e, "action")]
        obs_events = [e for e in conversation.state.events if hasattr(e, "observation")]

        # Agent should have called add_numbers_e2e
        tool_actions = [e for e in action_events if "add_numbers_e2e" in type(e.action).__name__]
        assert len(tool_actions) >= 1, (
            f"Tool was never called. Actions: {[type(e.action).__name__ for e in action_events]}"
        )
        assert tool_actions[0].action.a == 17
        assert tool_actions[0].action.b == 25

        # Observation should contain the sum
        tool_obs = [e for e in obs_events if hasattr(e.observation, "result") and "42" in str(e.observation.result)]
        assert len(tool_obs) >= 1, "Tool result not found in observations"

    set_workspace("/workspace")
