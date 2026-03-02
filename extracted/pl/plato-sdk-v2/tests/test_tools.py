"""Tests for plato.tools — ToolDefinition, serialization, and get_workspace."""

import tempfile
from pathlib import Path

import pytest

from plato.tools import ToolDefinition, get_workspace, load_tools, save_tools, set_workspace

DEFAULT_TOOLS_FILE = ".plato/tools.pkl"


def _save(tools, workspace):
    """Save tools to <workspace>/.plato/tools.pkl."""
    return save_tools(tools, Path(workspace) / DEFAULT_TOOLS_FILE)


def _load(workspace):
    """Load tools from <workspace>/.plato/tools.pkl."""
    return load_tools(Path(workspace) / DEFAULT_TOOLS_FILE, workspace=workspace)


def _echo_handler(input_data: dict) -> dict:
    return {"echo": input_data}


def _greet_handler(input_data: dict) -> str:
    name = input_data.get("name", "world")
    return f"Hello, {name}!"


TOOLS = [
    ToolDefinition(
        name="echo",
        description="Echoes input back",
        input_schema={"type": "object", "properties": {"msg": {"type": "string"}}},
        handler=_echo_handler,
    ),
    ToolDefinition(
        name="greet",
        description="Greets by name",
        input_schema={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
        handler=_greet_handler,
    ),
]


# =============================================================================
# Serialization tests
# =============================================================================


def test_save_and_load_tools():
    """Tools can be pickled and unpickled with working handlers."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _save(TOOLS, tmpdir)

        # Verify file exists
        assert (Path(tmpdir) / ".plato" / "tools.pkl").exists()

        # Load and verify
        loaded = _load(tmpdir)
        assert len(loaded) == 2
        assert {t.name for t in loaded} == {"echo", "greet"}

        # Verify handlers still work
        echo = next(t for t in loaded if t.name == "echo")
        assert echo.handler({"msg": "test"}) == {"echo": {"msg": "test"}}

        greet = next(t for t in loaded if t.name == "greet")
        assert greet.handler({"name": "World"}) == "Hello, World!"


def test_save_tools_with_closure():
    """Handlers that close over variables survive pickling."""
    captured_data = {"key": "value", "items": [1, 2, 3]}

    def closure_handler(input_data: dict) -> dict:
        return {"data": captured_data, "input": input_data}

    tools = [
        ToolDefinition(
            name="closure_tool",
            description="Tool with closure",
            input_schema={"type": "object", "properties": {}},
            handler=closure_handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        result = loaded[0].handler({"arg": 1})
        assert result["data"] == captured_data
        assert result["input"] == {"arg": 1}


def test_save_tools_with_lambda():
    """Lambda handlers survive pickling via cloudpickle."""
    tools = [
        ToolDefinition(
            name="lambda_tool",
            description="Tool with lambda",
            input_schema={"type": "object", "properties": {}},
            handler=lambda input_data: f"got: {input_data}",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        result = loaded[0].handler({"x": 1})
        assert result == "got: {'x': 1}"


def test_load_tools_missing_file():
    """Loading from a dir without tools raises FileNotFoundError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError):
            _load(tmpdir)


def test_save_tools_creates_directory():
    """save_tools creates the .plato directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir) / "nested" / "workspace"
        workspace.mkdir(parents=True)
        _save(TOOLS, workspace)
        assert (workspace / ".plato" / "tools.pkl").exists()


# =============================================================================
# get_workspace tests
# =============================================================================


def test_get_workspace_default():
    """get_workspace returns /workspace by default."""
    # Reset to default
    set_workspace("/workspace")
    assert get_workspace() == Path("/workspace")


def test_set_and_get_workspace():
    """set_workspace / get_workspace round-trip."""
    set_workspace("/tmp/my-workspace")
    assert get_workspace() == Path("/tmp/my-workspace")
    # Reset
    set_workspace("/workspace")


def test_load_tools_sets_workspace():
    """load_tools automatically sets the workspace path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _save(TOOLS, tmpdir)
        _load(tmpdir)
        assert get_workspace() == Path(tmpdir)
    # Reset
    set_workspace("/workspace")


def test_handler_using_get_workspace():
    """Handlers that use get_workspace() resolve to the correct path."""

    def workspace_handler(input_data: dict) -> str:
        ws = get_workspace()
        return str(ws / "output.txt")

    tools = [
        ToolDefinition(
            name="ws_tool",
            description="Uses workspace",
            input_schema={"type": "object", "properties": {}},
            handler=workspace_handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        result = loaded[0].handler({})
        assert result == str(Path(tmpdir) / "output.txt")

    # Reset
    set_workspace("/workspace")


# =============================================================================
# Pickling robustness tests
# =============================================================================


def test_pickle_closure_over_large_dict():
    """Handlers closing over large dicts (like recording JSON) survive pickling."""
    # Simulate a recording data dict with nested structure
    large_data = {
        f"/page/{i}--{1000000 + i}": {
            "url": f"https://example.com/page/{i}",
            "html": f"<html><body>Page {i} content {'x' * 500}</body></html>",
            "trigger": "after_navigation",
            "screenshot": f"data:image/png;base64,{'A' * 100}",
        }
        for i in range(50)
    }

    def handler(input_data: dict) -> str:
        keys = sorted(large_data.keys())
        return f"Found {len(keys)} snapshots, first: {keys[0]}"

    tools = [
        ToolDefinition(
            name="list_snapshots",
            description="List snapshots from recording data",
            input_schema={"type": "object", "properties": {}},
            handler=handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        result = loaded[0].handler({})
        assert "Found 50 snapshots" in result
        assert "/page/0--1000000" in result


def test_pickle_closure_with_get_workspace_and_data():
    """The real pattern: handler closes over data dict AND uses get_workspace() for paths."""
    recording_data = {
        "/--1000": {"url": "https://example.com/", "html": "<html>home</html>"},
        "/about--2000": {"url": "https://example.com/about", "html": "<html>about</html>"},
    }

    def list_handler(input_data: dict) -> str:
        return f"Snapshots: {list(recording_data.keys())}"

    def read_handler(input_data: dict) -> str:
        project_dir = get_workspace()
        key = input_data["key"]
        snap = recording_data.get(key)
        if not snap:
            return "Error: not found"
        return f"HTML from {project_dir}: {snap['html']}"

    tools = [
        ToolDefinition(
            name="list",
            description="List snapshots",
            input_schema={"type": "object", "properties": {}},
            handler=list_handler,
        ),
        ToolDefinition(
            name="read",
            description="Read snapshot",
            input_schema={"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]},
            handler=read_handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        # list handler works — data dict survived pickling
        result = loaded[0].handler({})
        assert "/--1000" in result
        assert "/about--2000" in result

        # read handler works — data dict AND get_workspace() both work
        result = loaded[1].handler({"key": "/about--2000"})
        assert "<html>about</html>" in result
        assert tmpdir in result  # workspace was set by load_tools

    set_workspace("/workspace")


def test_pickle_multiple_closures_sharing_data():
    """Multiple handlers closing over the same data object all get independent copies."""
    shared_data = {"counter": 0, "items": ["a", "b", "c"]}

    def handler_a(input_data: dict) -> str:
        return f"items={shared_data['items']}"

    def handler_b(input_data: dict) -> str:
        return f"counter={shared_data['counter']}"

    tools = [
        ToolDefinition(name="a", description="A", input_schema={"type": "object", "properties": {}}, handler=handler_a),
        ToolDefinition(name="b", description="B", input_schema={"type": "object", "properties": {}}, handler=handler_b),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        assert loaded[0].handler({}) == "items=['a', 'b', 'c']"
        assert loaded[1].handler({}) == "counter=0"


def test_pickle_handler_returning_complex_types():
    """Handlers returning dicts with nested structures survive pickling."""

    def handler(input_data: dict) -> dict:
        return {
            "type": "screenshot_result",
            "snapshot_key": input_data.get("key", ""),
            "image_b64": "iVBORw0KGgo=",
            "media_type": "image/png",
            "nested": {"list": [1, 2, 3], "none": None, "bool": True},
        }

    tools = [
        ToolDefinition(
            name="screenshot",
            description="Returns complex dict",
            input_schema={"type": "object", "properties": {"key": {"type": "string"}}},
            handler=handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        result = loaded[0].handler({"key": "/page--123"})
        assert result["type"] == "screenshot_result"
        assert result["snapshot_key"] == "/page--123"
        assert result["nested"]["list"] == [1, 2, 3]
        assert result["nested"]["none"] is None


def test_pickle_handler_with_imports():
    """Handlers that import modules at call time survive pickling."""
    import json as json_module  # close over the module

    def handler(input_data: dict) -> str:
        return json_module.dumps(input_data, sort_keys=True)

    tools = [
        ToolDefinition(
            name="jsonify",
            description="JSON encode",
            input_schema={"type": "object", "properties": {}},
            handler=handler,
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        result = loaded[0].handler({"b": 2, "a": 1})
        assert result == '{"a": 1, "b": 2}'


def test_pickle_handler_factory_pattern():
    """The _make_handler factory pattern used in flow_extraction survives pickling."""

    def make_handler(name: str, data: dict):
        """Mimics the real _make_handler pattern."""

        def handler(input_data: dict) -> str:
            ws = get_workspace()
            if name == "list":
                return f"keys: {list(data.keys())}"
            elif name == "read":
                key = input_data["key"]
                return f"data[{key}] from {ws}: {data.get(key, 'NOT FOUND')}"
            return f"unknown tool: {name}"

        return handler

    data = {"snapshot_1": "html_content_1", "snapshot_2": "html_content_2"}

    tools = [
        ToolDefinition(
            name="list",
            description="List",
            input_schema={"type": "object", "properties": {}},
            handler=make_handler("list", data),
        ),
        ToolDefinition(
            name="read",
            description="Read",
            input_schema={"type": "object", "properties": {"key": {"type": "string"}}},
            handler=make_handler("read", data),
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        assert "snapshot_1" in loaded[0].handler({})
        assert "snapshot_2" in loaded[0].handler({})

        result = loaded[1].handler({"key": "snapshot_1"})
        assert "html_content_1" in result
        assert tmpdir in result  # workspace resolved correctly

        result = loaded[1].handler({"key": "missing"})
        assert "NOT FOUND" in result

    set_workspace("/workspace")


def test_pickle_handler_with_path_objects_in_closure():
    """Path objects in closures are pickled but DON'T match the agent workspace.
    This test demonstrates WHY handlers should use get_workspace() instead."""
    original_path = Path("/world/vm/recordings/project_123")

    def bad_handler(input_data: dict) -> str:
        # BAD: closes over a world-side path
        return str(original_path / "flows")

    def good_handler(input_data: dict) -> str:
        # GOOD: uses get_workspace()
        return str(get_workspace() / "flows")

    tools = [
        ToolDefinition(
            name="bad", description="Bad", input_schema={"type": "object", "properties": {}}, handler=bad_handler
        ),
        ToolDefinition(
            name="good", description="Good", input_schema={"type": "object", "properties": {}}, handler=good_handler
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        # The bad handler still has the world-side path baked in
        assert loaded[0].handler({}) == "/world/vm/recordings/project_123/flows"

        # The good handler resolves to the agent-side workspace
        assert loaded[1].handler({}) == str(Path(tmpdir) / "flows")

    set_workspace("/workspace")


def test_pickle_roundtrip_preserves_schema():
    """Tool schemas (name, description, input_schema) survive pickling exactly."""
    schema = {
        "type": "object",
        "properties": {
            "snapshot_key": {"type": "string", "description": "The snapshot key"},
            "max_chars": {"type": "integer", "description": "Max chars to return"},
        },
        "required": ["snapshot_key"],
    }

    tools = [
        ToolDefinition(
            name="read_html",
            description="Read HTML content from a snapshot with optional truncation.",
            input_schema=schema,
            handler=lambda x: "ok",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        _save(tools, tmpdir)
        loaded = _load(tmpdir)

        t = loaded[0]
        assert t.name == "read_html"
        assert t.description == "Read HTML content from a snapshot with optional truncation."
        assert t.input_schema == schema
        assert t.input_schema["properties"]["snapshot_key"]["type"] == "string"
        assert t.input_schema["required"] == ["snapshot_key"]
