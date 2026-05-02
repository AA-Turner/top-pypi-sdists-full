"""Comprehensive tests for sage/core/plugin_system.py - Plugin integration system."""

import json
from unittest.mock import MagicMock, patch

import pytest

from sage.core.plugin_system import (
    AIPluginPlanner,
    ImportedSkillAdapter,
    PluginCapability,
    PluginErrorType,
    PluginExecutor,
    PluginInvocation,
    PluginInvocationResult,
    PluginRegistry,
    _derive_workflow_steps,
    _parse_jsonish,
    _tokenize,
)


# =============================================================================
# Tests for PluginErrorType enum
# =============================================================================


class TestPluginErrorType:
    """Tests for PluginErrorType enum."""

    def test_validation_value(self):
        """VALIDATION has correct value."""
        assert PluginErrorType.VALIDATION.value == "validation"

    def test_auth_value(self):
        """AUTH has correct value."""
        assert PluginErrorType.AUTH.value == "auth"

    def test_timeout_value(self):
        """TIMEOUT has correct value."""
        assert PluginErrorType.TIMEOUT.value == "timeout"

    def test_dependency_value(self):
        """DEPENDENCY has correct value."""
        assert PluginErrorType.DEPENDENCY.value == "dependency"

    def test_not_found_value(self):
        """NOT_FOUND has correct value."""
        assert PluginErrorType.NOT_FOUND.value == "not_found"

    def test_internal_value(self):
        """INTERNAL has correct value."""
        assert PluginErrorType.INTERNAL.value == "internal"

    def test_all_types_present(self):
        """All expected error types exist."""
        expected = ["VALIDATION", "AUTH", "TIMEOUT", "DEPENDENCY", "NOT_FOUND", "INTERNAL"]
        for name in expected:
            assert hasattr(PluginErrorType, name)


# =============================================================================
# Tests for PluginCapability dataclass
# =============================================================================


class TestPluginCapability:
    """Tests for PluginCapability dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        cap = PluginCapability(
            plugin_id="test", name="action", description="Test action"
        )
        assert cap.plugin_id == "test"
        assert cap.name == "action"
        assert cap.description == "Test action"
        assert cap.mutating is False
        assert cap.tags == ()

    def test_create_full(self):
        """Create with all fields."""
        cap = PluginCapability(
            plugin_id="test",
            name="action",
            description="Test action",
            mutating=True,
            tags=("read", "write"),
        )
        assert cap.mutating is True
        assert cap.tags == ("read", "write")

    def test_key_property(self):
        """Key property combines plugin_id and name."""
        cap = PluginCapability(plugin_id="my.plugin", name="do_thing", description="d")
        assert cap.key == "my.plugin.do_thing"

    def test_to_dict(self):
        """to_dict returns serializable representation."""
        cap = PluginCapability(
            plugin_id="test",
            name="action",
            description="Test action",
            mutating=True,
            tags=("tag1", "tag2"),
        )
        d = cap.to_dict()
        assert d["plugin_id"] == "test"
        assert d["name"] == "action"
        assert d["key"] == "test.action"
        assert d["description"] == "Test action"
        assert d["mutating"] is True
        assert d["tags"] == ["tag1", "tag2"]

    def test_frozen(self):
        """PluginCapability is frozen/immutable."""
        cap = PluginCapability(plugin_id="test", name="action", description="d")
        with pytest.raises(AttributeError):
            cap.plugin_id = "other"


# =============================================================================
# Tests for PluginInvocation dataclass
# =============================================================================


class TestPluginInvocation:
    """Tests for PluginInvocation dataclass."""

    def test_create_minimal(self):
        """Create with minimal fields."""
        inv = PluginInvocation(capability_key="test.action")
        assert inv.capability_key == "test.action"
        assert inv.args == {}
        assert inv.idempotency_key is None
        assert inv.timeout_seconds is None

    def test_create_full(self):
        """Create with all fields."""
        inv = PluginInvocation(
            capability_key="test.action",
            args={"param": "value"},
            idempotency_key="abc123",
            timeout_seconds=30.0,
        )
        assert inv.args == {"param": "value"}
        assert inv.idempotency_key == "abc123"
        assert inv.timeout_seconds == 30.0

    def test_to_dict(self):
        """to_dict returns serializable representation."""
        inv = PluginInvocation(
            capability_key="test.action",
            args={"x": 1},
            idempotency_key="key1",
            timeout_seconds=60.0,
        )
        d = inv.to_dict()
        assert d["capability_key"] == "test.action"
        assert d["args"] == {"x": 1}
        assert d["idempotency_key"] == "key1"
        assert d["timeout_seconds"] == 60.0


# =============================================================================
# Tests for PluginInvocationResult dataclass
# =============================================================================


class TestPluginInvocationResult:
    """Tests for PluginInvocationResult dataclass."""

    def test_create_success(self):
        """Create success result."""
        result = PluginInvocationResult(
            capability_key="test.action", success=True, data={"result": "ok"}
        )
        assert result.capability_key == "test.action"
        assert result.success is True
        assert result.data == {"result": "ok"}
        assert result.error_type is None
        assert result.error_message is None

    def test_create_failure(self):
        """Create failure result."""
        result = PluginInvocationResult(
            capability_key="test.action",
            success=False,
            error_type=PluginErrorType.VALIDATION,
            error_message="Invalid input",
        )
        assert result.success is False
        assert result.error_type == PluginErrorType.VALIDATION
        assert result.error_message == "Invalid input"

    def test_to_dict_success(self):
        """to_dict for success result."""
        result = PluginInvocationResult(
            capability_key="test.action", success=True, data={"x": 1}
        )
        d = result.to_dict()
        assert d["capability_key"] == "test.action"
        assert d["success"] is True
        assert d["data"] == {"x": 1}
        assert d["error_type"] is None
        assert d["error_message"] is None

    def test_to_dict_failure(self):
        """to_dict for failure result."""
        result = PluginInvocationResult(
            capability_key="test.action",
            success=False,
            error_type=PluginErrorType.TIMEOUT,
            error_message="Timed out",
        )
        d = result.to_dict()
        assert d["error_type"] == "timeout"
        assert d["error_message"] == "Timed out"


# =============================================================================
# Tests for _parse_jsonish function
# =============================================================================


class TestParseJsonish:
    """Tests for _parse_jsonish helper function."""

    def test_parse_none(self):
        """None returns empty dict."""
        assert _parse_jsonish(None) == {}

    def test_parse_dict(self):
        """Dict passes through."""
        d = {"key": "value"}
        assert _parse_jsonish(d) == d

    def test_parse_list(self):
        """List wraps in items/actions."""
        result = _parse_jsonish([1, 2, 3])
        assert result["items"] == [1, 2, 3]
        assert result["actions"] == [1, 2, 3]

    def test_parse_json_string(self):
        """JSON string is parsed."""
        result = _parse_jsonish('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_invalid_json_string(self):
        """Invalid JSON string returns raw_text."""
        result = _parse_jsonish("not json")
        assert result == {"raw_text": "not json"}

    def test_parse_empty_string(self):
        """Empty string returns empty dict."""
        assert _parse_jsonish("") == {}
        assert _parse_jsonish("   ") == {}

    def test_parse_wrapped_actions(self):
        """Handles wrapped actions key."""
        d = {"actions": '[{"capability_key": "test"}]'}
        result = _parse_jsonish(d)
        assert "actions" in result

    def test_parse_wrapped_result(self):
        """Handles wrapped result key."""
        d = {"result": '{"data": 123}'}
        result = _parse_jsonish(d)
        assert result.get("data") == 123

    def test_parse_other_type(self):
        """Other types return raw_value."""
        result = _parse_jsonish(123)
        assert result == {"raw_value": "123"}

    def test_parse_nested_json(self):
        """Nested JSON string in dict."""
        d = {"response": '{"nested": "value"}'}
        result = _parse_jsonish(d)
        assert result.get("nested") == "value"


# =============================================================================
# Tests for _tokenize function
# =============================================================================


class TestTokenize:
    """Tests for _tokenize helper function."""

    def test_tokenize_simple(self):
        """Tokenize simple text."""
        tokens = _tokenize("hello world")
        assert "hello" in tokens
        assert "world" in tokens

    def test_tokenize_lowercase(self):
        """Tokens are lowercase."""
        tokens = _tokenize("Hello WORLD")
        assert "hello" in tokens
        assert "world" in tokens

    def test_tokenize_min_length(self):
        """Tokens < 3 chars are filtered."""
        tokens = _tokenize("a bb ccc dddd")
        assert "a" not in tokens
        assert "bb" not in tokens
        assert "ccc" in tokens
        assert "dddd" in tokens

    def test_tokenize_special_chars(self):
        """Special chars (except underscore) are word boundaries."""
        # Underscore is part of token: [a-zA-Z0-9_]+
        tokens = _tokenize("foo-bar_baz.qux")
        assert "foo" in tokens
        assert "bar_baz" in tokens  # Underscore doesn't split
        assert "qux" in tokens

    def test_tokenize_numbers(self):
        """Numbers are included in tokens."""
        tokens = _tokenize("test123 456abc")
        assert "test123" in tokens
        assert "456abc" in tokens

    def test_tokenize_empty(self):
        """Empty string returns empty set."""
        assert _tokenize("") == set()


# =============================================================================
# Tests for _derive_workflow_steps function
# =============================================================================


class TestDeriveWorkflowSteps:
    """Tests for _derive_workflow_steps helper function."""

    def test_derive_from_list(self):
        """Derive from explicit list."""
        steps = _derive_workflow_steps(["Step 1", "Step 2"], "")
        assert steps == ["Step 1", "Step 2"]

    def test_derive_empty_list_fallback(self):
        """Empty list falls back to markdown parsing."""
        markdown = "1. First step\n2. Second step"
        steps = _derive_workflow_steps([], markdown)
        assert "First step" in steps
        assert "Second step" in steps

    def test_derive_from_numbered_markdown(self):
        """Parse numbered steps from markdown."""
        markdown = "1. Do this\n2. Do that\n3. Then this"
        steps = _derive_workflow_steps(None, markdown)
        assert len(steps) == 3

    def test_derive_from_bulleted_markdown(self):
        """Parse bullet points from markdown."""
        markdown = "- First item\n- Second item\n* Third item"
        steps = _derive_workflow_steps(None, markdown)
        assert len(steps) == 3

    def test_derive_limit(self):
        """Steps are limited to max count."""
        many_steps = [f"Step {i}" for i in range(50)]
        steps = _derive_workflow_steps(many_steps, "", limit=5)
        assert len(steps) == 5

    def test_derive_deduplicates(self):
        """Duplicate steps are removed."""
        markdown = "1. Same step\n2. Same step\n3. Different step"
        steps = _derive_workflow_steps(None, markdown)
        assert steps.count("Same step") == 1

    def test_derive_strips_whitespace(self):
        """Steps have whitespace stripped."""
        steps = _derive_workflow_steps(["  Step 1  ", "Step 2"], "")
        assert steps[0] == "Step 1"

    def test_derive_filters_empty(self):
        """Empty steps are filtered."""
        steps = _derive_workflow_steps(["Step 1", "", "  ", "Step 2"], "")
        assert len(steps) == 2

    def test_derive_empty_all(self):
        """Empty input returns empty list."""
        assert _derive_workflow_steps(None, "") == []
        assert _derive_workflow_steps([], "") == []


# =============================================================================
# Tests for PluginRegistry class
# =============================================================================


class MockAdapter:
    """Mock plugin adapter for testing."""

    def __init__(self, plugin_id: str, capabilities: list[PluginCapability]):
        self._plugin_id = plugin_id
        self._capabilities = capabilities

    @property
    def plugin_id(self) -> str:
        return self._plugin_id

    def capabilities(self) -> list[PluginCapability]:
        return self._capabilities

    def invoke(self, capability_name: str, args: dict) -> dict:
        return {"invoked": capability_name, "args": args}


class TestPluginRegistry:
    """Tests for PluginRegistry class."""

    def test_init(self):
        """Registry initializes empty."""
        registry = PluginRegistry()
        assert registry.list_capabilities() == []

    def test_register_adapter(self):
        """Register adapter adds capabilities."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test action")
        adapter = MockAdapter("test", [cap])
        registry.register(adapter)
        assert len(registry.list_capabilities()) == 1

    def test_register_multiple_capabilities(self):
        """Adapter with multiple capabilities."""
        registry = PluginRegistry()
        caps = [
            PluginCapability("test", "action1", "Action 1"),
            PluginCapability("test", "action2", "Action 2"),
        ]
        adapter = MockAdapter("test", caps)
        registry.register(adapter)
        assert len(registry.list_capabilities()) == 2

    def test_register_duplicate_raises(self):
        """Duplicate capability key raises ValueError."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")
        adapter1 = MockAdapter("test", [cap])
        adapter2 = MockAdapter("test", [cap])
        registry.register(adapter1)
        with pytest.raises(ValueError, match="Duplicate"):
            registry.register(adapter2)

    def test_list_capabilities_sorted(self):
        """Capabilities are sorted by key."""
        registry = PluginRegistry()
        caps = [
            PluginCapability("z", "last", "Last"),
            PluginCapability("a", "first", "First"),
            PluginCapability("m", "middle", "Middle"),
        ]
        for cap in caps:
            adapter = MockAdapter(cap.plugin_id, [cap])
            registry.register(adapter)
        listed = registry.list_capabilities()
        keys = [c.key for c in listed]
        assert keys == sorted(keys)

    def test_get_capability_exists(self):
        """Get existing capability."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")
        adapter = MockAdapter("test", [cap])
        registry.register(adapter)
        result = registry.get_capability("test.action")
        assert result is not None
        assert result.key == "test.action"

    def test_get_capability_not_exists(self):
        """Get non-existent capability returns None."""
        registry = PluginRegistry()
        assert registry.get_capability("nonexistent") is None

    def test_get_adapter_for_capability(self):
        """Get adapter for capability."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")
        adapter = MockAdapter("test", [cap])
        registry.register(adapter)
        result_adapter, name = registry.get_adapter_for_capability("test.action")
        assert result_adapter is adapter
        assert name == "action"

    def test_get_adapter_for_nonexistent(self):
        """Get adapter for non-existent capability."""
        registry = PluginRegistry()
        adapter, name = registry.get_adapter_for_capability("nonexistent")
        assert adapter is None
        assert name == ""


# =============================================================================
# Tests for PluginExecutor class
# =============================================================================


class TestPluginExecutor:
    """Tests for PluginExecutor class."""

    def test_execute_success(self):
        """Execute successful invocation."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")
        adapter = MockAdapter("test", [cap])
        registry.register(adapter)
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("test.action", args={"x": 1})
        result = executor.execute(invocation)
        assert result.success is True
        assert result.data["invoked"] == "action"

    def test_execute_not_found(self):
        """Execute returns NOT_FOUND for unknown capability."""
        registry = PluginRegistry()
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("unknown.action")
        result = executor.execute(invocation)
        assert result.success is False
        assert result.error_type == PluginErrorType.NOT_FOUND

    def test_execute_mutating_blocked(self):
        """Mutating capability blocked by default."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test", mutating=True)
        adapter = MockAdapter("test", [cap])
        registry.register(adapter)
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("test.action")
        result = executor.execute(invocation)
        assert result.success is False
        assert result.error_type == PluginErrorType.VALIDATION
        assert "Mutating" in result.error_message

    def test_execute_mutating_allowed(self):
        """Mutating capability allowed when explicitly permitted."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test", mutating=True)
        adapter = MockAdapter("test", [cap])
        registry.register(adapter)
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("test.action")
        result = executor.execute(invocation, allow_mutating=True)
        assert result.success is True

    def test_execute_timeout_error(self):
        """TimeoutError maps to TIMEOUT error type."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")

        class TimeoutAdapter(MockAdapter):
            def invoke(self, capability_name: str, args: dict) -> dict:
                raise TimeoutError("Operation timed out")

        adapter = TimeoutAdapter("test", [cap])
        registry.register(adapter)
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("test.action")
        result = executor.execute(invocation)
        assert result.success is False
        assert result.error_type == PluginErrorType.TIMEOUT

    def test_execute_permission_error(self):
        """PermissionError maps to AUTH error type."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")

        class AuthAdapter(MockAdapter):
            def invoke(self, capability_name: str, args: dict) -> dict:
                raise PermissionError("Not authorized")

        adapter = AuthAdapter("test", [cap])
        registry.register(adapter)
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("test.action")
        result = executor.execute(invocation)
        assert result.success is False
        assert result.error_type == PluginErrorType.AUTH

    def test_execute_wraps_non_dict_result(self):
        """Non-dict result is wrapped."""
        registry = PluginRegistry()
        cap = PluginCapability("test", "action", "Test")

        class StringAdapter(MockAdapter):
            def invoke(self, capability_name: str, args: dict) -> dict:
                return "string result"  # type: ignore

        adapter = StringAdapter("test", [cap])
        registry.register(adapter)
        executor = PluginExecutor(registry)
        invocation = PluginInvocation("test.action")
        result = executor.execute(invocation)
        assert result.success is True
        assert result.data["result"] == "string result"


# =============================================================================
# Tests for AIPluginPlanner class
# =============================================================================


class TestAIPluginPlanner:
    """Tests for AIPluginPlanner class."""

    def test_plan_actions_with_valid_json(self):
        """Plan actions with valid JSON response."""

        def mock_send(prompt: str):
            return json.dumps(
                {"actions": [{"capability_key": "test.action", "args": {"x": 1}}]}
            )

        planner = AIPluginPlanner(mock_send)
        caps = [PluginCapability("test", "action", "Test action")]
        invocations = planner.plan_actions("Do test action", caps)
        assert len(invocations) == 1
        assert invocations[0].capability_key == "test.action"
        assert invocations[0].args == {"x": 1}

    def test_plan_actions_with_plugin_actions_key(self):
        """Plan actions with plugin_actions key."""

        def mock_send(prompt: str):
            return {"plugin_actions": [{"capability_key": "test.action"}]}

        planner = AIPluginPlanner(mock_send)
        caps = [PluginCapability("test", "action", "Test action")]
        invocations = planner.plan_actions("Do test action", caps)
        assert len(invocations) == 1

    def test_plan_actions_with_tool_calls_key(self):
        """Plan actions with tool_calls key."""

        def mock_send(prompt: str):
            return {"tool_calls": [{"capability_key": "test.action"}]}

        planner = AIPluginPlanner(mock_send)
        caps = [PluginCapability("test", "action", "Test action")]
        invocations = planner.plan_actions("Do test action", caps)
        assert len(invocations) == 1

    def test_plan_actions_filters_invalid_keys(self):
        """Invalid capability keys are filtered."""

        def mock_send(prompt: str):
            return {
                "actions": [
                    {"capability_key": "test.action"},
                    {"capability_key": "invalid.key"},
                ]
            }

        planner = AIPluginPlanner(mock_send)
        caps = [PluginCapability("test", "action", "Test action")]
        invocations = planner.plan_actions("Task", caps)
        assert len(invocations) == 1
        assert invocations[0].capability_key == "test.action"

    def test_plan_actions_fallback_on_no_actions(self):
        """Fallback when no valid actions returned."""

        def mock_send(prompt: str):
            return {}

        planner = AIPluginPlanner(mock_send)
        caps = [
            PluginCapability("test", "search_files", "Search for files"),
            PluginCapability("test", "read_data", "Read data from source"),
        ]
        invocations = planner.plan_actions("search files", caps)
        # Fallback should match based on token overlap
        assert any(inv.capability_key == "test.search_files" for inv in invocations)

    def test_plan_actions_fallback_skips_mutating(self):
        """Fallback skips mutating capabilities."""

        def mock_send(prompt: str):
            return {}

        planner = AIPluginPlanner(mock_send)
        caps = [
            PluginCapability("test", "delete_file", "Delete file", mutating=True),
            PluginCapability("test", "list_files", "List files"),
        ]
        invocations = planner.plan_actions("delete file", caps)
        # Should not include mutating capability in fallback
        assert not any(inv.capability_key == "test.delete_file" for inv in invocations)

    def test_plan_actions_empty_task(self):
        """Empty task returns empty invocations."""

        def mock_send(prompt: str):
            return {}

        planner = AIPluginPlanner(mock_send)
        caps = [PluginCapability("test", "action", "Test")]
        invocations = planner.plan_actions("", caps)
        # No tokens to match
        assert invocations == []

    def test_plan_actions_handles_non_dict_action(self):
        """Non-dict actions are filtered."""

        def mock_send(prompt: str):
            return {"actions": [{"capability_key": "test.action"}, "invalid", 123]}

        planner = AIPluginPlanner(mock_send)
        caps = [PluginCapability("test", "action", "Test")]
        invocations = planner.plan_actions("Task", caps)
        assert len(invocations) == 1


# =============================================================================
# Tests for ImportedSkillAdapter class
# =============================================================================


class TestImportedSkillAdapter:
    """Tests for ImportedSkillAdapter class."""

    def test_init_basic(self):
        """Basic initialization."""
        adapter = ImportedSkillAdapter(
            plugin_name="myPlugin",
            plugin_description="My plugin",
            skills=[{"skill": "doThing", "description": "Does thing"}],
        )
        assert adapter.plugin_id == "claude.myPlugin"

    def test_init_empty_name(self):
        """Empty name uses unknown."""
        adapter = ImportedSkillAdapter("", "desc", [])
        assert adapter.plugin_id == "claude.unknown"

    def test_capabilities_from_skills(self):
        """Capabilities from skills list."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[
                {"skill": "skill1", "description": "Skill 1"},
                {"skill": "skill2", "description": "Skill 2"},
            ],
        )
        caps = adapter.capabilities()
        assert len(caps) == 2
        assert any(c.name == "skill1" for c in caps)

    def test_capabilities_from_commands(self):
        """Capabilities from commands list."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[],
            commands=[{"command": "cmd1", "description": "Command 1"}],
        )
        caps = adapter.capabilities()
        assert len(caps) == 1
        assert caps[0].name == "command.cmd1"

    def test_capabilities_from_agents(self):
        """Capabilities from agents list."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[],
            agents=[{"agent": "agent1", "description": "Agent 1"}],
        )
        caps = adapter.capabilities()
        assert len(caps) == 1
        assert caps[0].name == "agent.agent1"

    def test_capabilities_from_mcp_servers(self):
        """Capabilities from MCP servers list."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[],
            mcp_servers=[{"server": "server1", "description": "Server 1"}],
        )
        caps = adapter.capabilities()
        assert len(caps) == 1
        assert caps[0].name == "mcp.server1"

    def test_capabilities_tags(self):
        """Capabilities have correct tags."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[{"skill": "s", "description": "d"}],
            commands=[{"command": "c", "description": "d"}],
        )
        caps = adapter.capabilities()
        skill_cap = next(c for c in caps if c.name == "s")
        cmd_cap = next(c for c in caps if c.name == "command.c")
        assert "procedural" in skill_cap.tags
        assert "command" in cmd_cap.tags

    def test_invoke_skill(self):
        """Invoke skill capability."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[
                {
                    "skill": "mySkill",
                    "description": "My skill",
                    "instruction_markdown": "Do things",
                    "default_prompt": "prompt",
                }
            ],
        )
        result = adapter.invoke("mySkill", {"param": "value"})
        assert result["skill"] == "mySkill"
        assert result["capability_type"] == "skill"
        assert "execution_prompt" in result

    def test_invoke_command(self):
        """Invoke command capability."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[],
            commands=[{"command": "myCmd", "description": "desc"}],
        )
        result = adapter.invoke("command.myCmd", {})
        assert result["command"] == "myCmd"
        assert result["capability_type"] == "command"

    def test_invoke_agent(self):
        """Invoke agent capability."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[],
            agents=[{"agent": "myAgent", "description": "desc"}],
        )
        result = adapter.invoke("agent.myAgent", {})
        assert result["agent"] == "myAgent"
        assert result["capability_type"] == "agent"

    def test_invoke_mcp(self):
        """Invoke MCP server capability."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[],
            mcp_servers=[
                {
                    "server": "myServer",
                    "description": "desc",
                    "transport": "http",
                    "url": "http://example.com",
                }
            ],
        )
        result = adapter.invoke("mcp.myServer", {})
        assert result["mcp_server"] == "myServer"
        assert result["capability_type"] == "mcp"
        assert result["transport"] == "http"

    def test_invoke_unknown_raises(self):
        """Invoke unknown capability raises ValueError."""
        adapter = ImportedSkillAdapter("plugin", "desc", skills=[])
        with pytest.raises(ValueError, match="Unsupported"):
            adapter.invoke("unknown", {})

    def test_invoke_workflow_steps_derived(self):
        """Workflow steps are derived from instruction markdown."""
        adapter = ImportedSkillAdapter(
            "plugin",
            "desc",
            skills=[
                {
                    "skill": "s",
                    "description": "d",
                    "instruction_markdown": "1. First step\n2. Second step",
                }
            ],
        )
        result = adapter.invoke("s", {})
        assert len(result["workflow_steps"]) == 2


# =============================================================================
# Integration tests
# =============================================================================


class TestPluginSystemIntegration:
    """Integration tests for plugin system."""

    def test_full_workflow(self):
        """Test full workflow: register, plan, execute."""
        # Create registry
        registry = PluginRegistry()

        # Create and register adapter
        caps = [
            PluginCapability("test", "read", "Read data"),
            PluginCapability("test", "write", "Write data", mutating=True),
        ]
        adapter = MockAdapter("test", caps)
        registry.register(adapter)

        # Create planner
        def mock_send(prompt: str):
            return {"actions": [{"capability_key": "test.read", "args": {"file": "x"}}]}

        planner = AIPluginPlanner(mock_send)

        # Plan actions
        invocations = planner.plan_actions("Read data", registry.list_capabilities())
        assert len(invocations) == 1

        # Execute
        executor = PluginExecutor(registry)
        result = executor.execute(invocations[0])
        assert result.success is True

    def test_imported_skill_workflow(self):
        """Test workflow with imported skill adapter."""
        adapter = ImportedSkillAdapter(
            "testPlugin",
            "Test plugin",
            skills=[{"skill": "analyze", "description": "Analyze code"}],
        )

        registry = PluginRegistry()
        registry.register(adapter)

        caps = registry.list_capabilities()
        assert len(caps) == 1
        assert caps[0].key == "claude.testPlugin.analyze"

        executor = PluginExecutor(registry)
        invocation = PluginInvocation("claude.testPlugin.analyze")
        result = executor.execute(invocation)
        assert result.success is True
        assert result.data["skill"] == "analyze"
