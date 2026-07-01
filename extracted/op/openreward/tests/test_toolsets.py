"""Tests for toolset composition system."""

from typing import Any

import pytest
from pydantic import BaseModel, Field

from openreward.environments import Environment, Toolset, tool, ToolOutput, TextBlock
from openreward.environments.types import Blocks, JSONObject
from openreward.api.sandboxes.types import RunResult


# ===== Test Toolsets =====

class SimpleParams(BaseModel):
    message: str = Field(..., description="Test message")


class SimpleToolset:
    """Simple toolset without sandbox requirement"""

    @tool
    async def simple_tool(self, params: SimpleParams) -> ToolOutput:
        """A simple test tool"""
        return ToolOutput(
            blocks=[TextBlock(text=f"Simple: {params.message}")],
            reward=0.0,
            finished=False,
        )


class MockSandbox:
    """Mock sandbox for testing"""
    async def run(self, cmd: str, **kwargs) -> RunResult:
        return RunResult(output=f"Executed: {cmd}", return_code=0)


class SandboxToolset(Toolset):
    """Toolset that requires sandbox"""

    @tool
    async def sandbox_tool(self, params: SimpleParams) -> ToolOutput:
        """Tool that uses sandbox"""
        output, code = await self.sandbox.run("test command")
        return ToolOutput(
            blocks=[TextBlock(text=f"Sandbox: {params.message}, output={output}")],
            reward=0.0,
            finished=False,
        )


class AnotherToolset:
    """Another simple toolset for testing multiple toolsets"""

    @tool
    async def another_tool(self) -> ToolOutput:
        """Another test tool without parameters"""
        return ToolOutput(
            blocks=[TextBlock(text="Another toolset")],
            reward=0.5,
            finished=False,
        )


# ===== Test Environments =====

class EnvWithSimpleToolset(Environment):
    """Environment with a simple toolset"""
    toolsets = [SimpleToolset]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="Test prompt")]

    @tool
    async def env_tool(self) -> ToolOutput:
        """Tool defined on environment itself"""
        return ToolOutput(
            blocks=[TextBlock(text="From environment")],
            reward=1.0,
            finished=True,
        )


class EnvWithSandboxToolset(Environment):
    """Environment with sandbox toolset"""
    toolsets = [SandboxToolset]

    def __init__(self, task_spec: JSONObject = {}, secrets: dict[str, str] = {}):
        super().__init__(task_spec, secrets)
        self.sandbox = MockSandbox()

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="Test prompt with sandbox")]


class EnvWithMultipleToolsets(Environment):
    """Environment with multiple toolsets"""
    toolsets = [SimpleToolset, AnotherToolset]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="Test prompt")]


class EnvWithCustomSandboxAttr(Environment):
    """Environment with custom sandbox attribute name"""

    class CustomSandboxToolset(Toolset):
        def __init__(self, env: Any, sandbox_attr: str = "custom_sandbox"):
            super().__init__(env, sandbox_attr)

        @tool
        async def custom_sandbox_tool(self) -> ToolOutput:
            """Tool that uses custom sandbox attribute"""
            output, code = await self.sandbox.run("custom command")
            return ToolOutput(
                blocks=[TextBlock(text=f"Custom sandbox: {output}")],
                reward=0.0,
                finished=False,
            )

    toolsets = [CustomSandboxToolset]

    def __init__(self, task_spec: JSONObject = {}, secrets: dict[str, str] = {}):
        super().__init__(task_spec, secrets)
        self.custom_sandbox = MockSandbox()

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="Test prompt")]


# ===== Tests =====

@pytest.mark.asyncio
async def test_list_tools_discovers_toolset_tools():
    """Test that list_tools() discovers tools from class-level toolsets"""
    tools_output = EnvWithSimpleToolset.list_tools()
    tool_names = [t.name for t in tools_output.tools]

    # Should have both environment tool and toolset tool
    assert "env_tool" in tool_names
    assert "simple_tool" in tool_names


@pytest.mark.asyncio
async def test_list_tools_with_multiple_toolsets():
    """Test that list_tools() discovers tools from multiple toolsets"""
    tools_output = EnvWithMultipleToolsets.list_tools()
    tool_names = [t.name for t in tools_output.tools]

    assert "simple_tool" in tool_names
    assert "another_tool" in tool_names


@pytest.mark.asyncio
async def test_call_toolset_tool():
    """Test calling a tool from a toolset"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    result = await env._call_tool("simple_tool", {"message": "Hello"})

    assert result.root.ok is True
    assert len(result.root.output.blocks) == 1
    assert result.root.output.blocks[0].text == "Simple: Hello"


@pytest.mark.asyncio
async def test_call_environment_tool():
    """Test calling a tool defined on environment itself"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    result = await env._call_tool("env_tool", {})

    assert result.root.ok is True
    assert len(result.root.output.blocks) == 1
    assert result.root.output.blocks[0].text == "From environment"
    assert result.root.output.reward == 1.0
    assert result.root.output.finished is True


@pytest.mark.asyncio
async def test_lazy_instantiation():
    """Test that toolsets are lazily instantiated on first tool call"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    # Before any tool call, toolset instances should be empty
    assert len(env._toolset_instances) == 0

    # Call a toolset tool
    await env._call_tool("simple_tool", {"message": "Test"})

    # Now toolset should be instantiated and cached
    assert len(env._toolset_instances) == 1
    assert SimpleToolset in env._toolset_instances


@pytest.mark.asyncio
async def test_toolset_caching():
    """Test that toolset instances are cached and reused"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    # First call instantiates
    await env._call_tool("simple_tool", {"message": "First"})
    first_instance = env._toolset_instances[SimpleToolset]

    # Second call reuses same instance
    await env._call_tool("simple_tool", {"message": "Second"})
    second_instance = env._toolset_instances[SimpleToolset]

    assert first_instance is second_instance


@pytest.mark.asyncio
async def test_toolset_with_sandbox():
    """Test toolset that requires sandbox access"""
    env = EnvWithSandboxToolset(task_spec={"id": "1"})

    result = await env._call_tool("sandbox_tool", {"message": "Test"})

    assert result.root.ok is True
    assert "Sandbox: Test" in result.root.output.blocks[0].text
    assert "Executed: test command" in result.root.output.blocks[0].text


@pytest.mark.asyncio
async def test_custom_sandbox_attribute():
    """Test toolset with custom sandbox attribute name"""
    env = EnvWithCustomSandboxAttr(task_spec={"id": "1"})

    result = await env._call_tool("custom_sandbox_tool", {})

    assert result.root.ok is True
    assert "Custom sandbox" in result.root.output.blocks[0].text


@pytest.mark.asyncio
async def test_tool_not_found():
    """Test calling a non-existent tool"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    result = await env._call_tool("nonexistent_tool", {})

    assert result.root.ok is False
    assert "not a valid tool" in result.root.error


@pytest.mark.asyncio
async def test_multiple_toolsets_tool_calls():
    """Test calling tools from different toolsets"""
    env = EnvWithMultipleToolsets(task_spec={"id": "1"})

    # Call tool from first toolset
    result1 = await env._call_tool("simple_tool", {"message": "Test1"})
    assert result1.root.ok is True
    assert "Simple: Test1" in result1.root.output.blocks[0].text

    # Call tool from second toolset
    result2 = await env._call_tool("another_tool", {})
    assert result2.root.ok is True
    assert "Another toolset" in result2.root.output.blocks[0].text


@pytest.mark.asyncio
async def test_tool_validation_error():
    """Test that tool parameter validation works"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    # Call tool with missing required parameter
    result = await env._call_tool("simple_tool", {})

    assert result.root.ok is False
    assert "validation error" in result.root.error.lower()


@pytest.mark.asyncio
async def test_toolset_tool_schema():
    """Test that toolset tools have proper schema in list_tools()"""
    tools_output = EnvWithSimpleToolset.list_tools()

    simple_tool = next((t for t in tools_output.tools if t.name == "simple_tool"), None)

    assert simple_tool is not None
    assert simple_tool.description == "A simple test tool"
    assert simple_tool.input_schema is not None
    assert "message" in simple_tool.input_schema["properties"]


@pytest.mark.asyncio
async def test_toolset_without_sandbox():
    """Test that simple toolsets work without sandbox"""
    env = EnvWithSimpleToolset(task_spec={"id": "1"})

    # Should not have sandbox attribute
    assert not hasattr(env, 'sandbox')

    # But toolset tools should still work
    result = await env._call_tool("simple_tool", {"message": "No sandbox"})

    assert result.root.ok is True
    assert "Simple: No sandbox" in result.root.output.blocks[0].text


@pytest.mark.asyncio
async def test_tool_name_collision_detected_in_list_tools():
    """Test that list_tools() detects and raises error on tool name collisions"""

    class ToolsetWithSubmit:
        @tool
        async def submit(self) -> ToolOutput:
            return ToolOutput(
                blocks=[TextBlock(text="From toolset")],
                reward=0.0,
                finished=False,
            )

    class EnvWithConflictingTool(Environment):
        toolsets = [ToolsetWithSubmit]

        @classmethod
        def list_splits(cls) -> list[str]:
            return ["train"]

        @classmethod
        def list_tasks(cls, split: str) -> list[JSONObject]:
            return [{"id": "1"}]

        def get_prompt(self) -> Blocks:
            return [TextBlock(text="Test")]

        @tool
        async def submit(self) -> ToolOutput:
            return ToolOutput(
                blocks=[TextBlock(text="From environment")],
                reward=1.0,
                finished=True,
            )

    # list_tools() should raise ValueError on collision
    with pytest.raises(ValueError) as excinfo:
        EnvWithConflictingTool.list_tools()

    assert "Tool name collision" in str(excinfo.value)
    assert "'submit'" in str(excinfo.value)
    assert "ToolsetWithSubmit" in str(excinfo.value)


@pytest.mark.asyncio
async def test_tool_name_collision_detected_in_call_tool():
    """Test that _call_tool() detects and returns error on tool name collisions"""

    class ToolsetWithCollision:
        @tool
        async def my_tool(self) -> ToolOutput:
            return ToolOutput(
                blocks=[TextBlock(text="From toolset")],
                reward=0.0,
                finished=False,
            )

    class EnvWithCollision(Environment):
        toolsets = [ToolsetWithCollision]

        @classmethod
        def list_splits(cls) -> list[str]:
            return ["train"]

        @classmethod
        def list_tasks(cls, split: str) -> list[JSONObject]:
            return [{"id": "1"}]

        def get_prompt(self) -> Blocks:
            return [TextBlock(text="Test")]

        @tool
        async def my_tool(self) -> ToolOutput:
            return ToolOutput(
                blocks=[TextBlock(text="From environment")],
                reward=1.0,
                finished=True,
            )

    # Calling the tool should return an error about collision
    env = EnvWithCollision(task_spec={"id": "1"})
    result = await env._call_tool("my_tool", {})

    assert result.root.ok is False
    assert "Tool name collision" in result.root.error
    assert "'my_tool'" in result.root.error
    assert "ToolsetWithCollision" in result.root.error


# ===== Tests for @tool(shared=False) and list_task_tools =====


class EnvWithNonSharedTool(Environment):
    """Environment with both shared and non-shared tools"""

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="Test prompt")]

    @tool
    async def shared_tool(self) -> ToolOutput:
        """A shared tool"""
        return ToolOutput(
            blocks=[TextBlock(text="shared")],
            reward=0.0,
            finished=False,
        )

    @tool(shared=False)
    async def non_shared_tool(self, params: SimpleParams) -> ToolOutput:
        """A non-shared tool"""
        return ToolOutput(
            blocks=[TextBlock(text=f"non-shared: {params.message}")],
            reward=0.0,
            finished=False,
        )


def test_non_shared_tool_excluded_from_list_tools():
    """@tool(shared=False) methods should not appear in list_tools()"""
    tools_output = EnvWithNonSharedTool.list_tools()
    tool_names = [t.name for t in tools_output.tools]

    assert "shared_tool" in tool_names
    assert "non_shared_tool" not in tool_names


def test_default_tool_is_shared():
    """@tool (no args) methods should appear in list_tools()"""
    tools_output = EnvWithNonSharedTool.list_tools()
    tool_names = [t.name for t in tools_output.tools]

    assert "shared_tool" in tool_names


@pytest.mark.asyncio
async def test_non_shared_tool_still_callable():
    """Non-shared @tool methods should still be callable via _call_tool"""
    env = EnvWithNonSharedTool(task_spec={"id": "1"})

    result = await env._call_tool("non_shared_tool", {"message": "hello"})

    assert result.root.ok is True
    assert result.root.output.blocks[0].text == "non-shared: hello"


def test_list_task_tools_default_empty():
    """list_task_tools() should return empty by default"""
    env = EnvWithNonSharedTool(task_spec={"id": "1"})
    task_tools = env.list_task_tools()

    assert task_tools.tools == []


class EnvWithTaskTools(Environment):
    """Environment that overrides list_task_tools"""

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1", "tools": ["read_file"]}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="Test prompt")]

    def list_task_tools(self):
        from openreward.environments.types import ListToolsOutput, ToolSpec
        tools = []
        for tool_name in self.task_spec.get("tools", []):
            tools.append(ToolSpec(name=tool_name, description=f"Task tool: {tool_name}", input_schema=None))
        return ListToolsOutput(tools=tools)


def test_list_task_tools_override():
    """Subclass overriding list_task_tools should return task-specific tools"""
    env = EnvWithTaskTools(task_spec={"id": "1", "tools": ["read_file", "write_file"]})
    task_tools = env.list_task_tools()

    tool_names = [t.name for t in task_tools.tools]
    assert "read_file" in tool_names
    assert "write_file" in tool_names
    assert len(task_tools.tools) == 2


# ===== CLIToolset tests =====
#
# These exercise the shared sandbox-tool implementations in
# openreward.environments._sandbox_tools via the new CLIToolset wrapper.
# A FakeFsSandbox in-memory file dict is enough — none of the tools talk
# to a real container.

import base64
import re

from openreward.toolsets import CLIToolset
from openreward.toolsets.cli import (
    BashParams as CliBashParams,
    EditParams as CliEditParams,
    GlobParams as CliGlobParams,
    GrepParams as CliGrepParams,
    LSParams as CliLSParams,
    MultiEditParams as CliMultiEditParams,
    ReadParams as CliReadParams,
    TodoWriteParams as CliTodoWriteParams,
    WriteParams as CliWriteParams,
)


class FakeFsSandbox:
    """In-memory sandbox stand-in.

    Supports the three calls the SDK helpers make:
      * ``await sandbox.download(path)`` -> bytes (from ``self.files``)
      * ``await sandbox.check_run(cmd)`` -> recognises the base64 upload
        pattern emitted by ``upload_text`` and updates ``self.files``;
        otherwise echoes the command.
      * ``await sandbox.run(cmd)`` -> echoes ``(cmd, return_code)`` with a
        configurable default return code.

    Tests can pre-populate ``self.files`` and pre-program ``self.run_responses``
    (dict mapping a regex pattern -> ``(output, return_code)``) to simulate
    bash/grep/ls behaviour.
    """

    def __init__(self, files=None, default_return_code: int = 0):
        self.files = dict(files or {})
        self.default_return_code = default_return_code
        self.run_responses: list[tuple[str, tuple[str, int]]] = []
        self.run_log: list[str] = []
        self.check_run_log: list[str] = []

    def program(self, pattern: str, output: str, return_code: int = 0):
        self.run_responses.append((pattern, (output, return_code)))

    async def download(self, path: str) -> bytes:
        if path not in self.files:
            raise FileNotFoundError(path)
        return self.files[path]

    async def check_run(self, cmd: str):
        self.check_run_log.append(cmd)
        m = re.fullmatch(r"echo '([A-Za-z0-9+/=]+)' \| base64 -d > (.+)", cmd)
        if m:
            payload = base64.b64decode(m.group(1).encode("ascii"))
            self.files[m.group(2)] = payload
            return ("", 0)
        return ("", 0)

    async def run(self, cmd: str, **kwargs):
        self.run_log.append(cmd)
        for pat, (output, code) in self.run_responses:
            if re.search(pat, cmd):
                return (output, code)
        return (cmd, self.default_return_code)


class _FakeEnv:
    """Bare env stand-in carrying a ``sandbox`` attribute for Toolset binding."""

    def __init__(self, sandbox: FakeFsSandbox):
        self.sandbox = sandbox


def _read_text(sandbox: FakeFsSandbox, path: str) -> str:
    return sandbox.files[path].decode("utf-8")


@pytest.mark.asyncio
async def test_cli_toolset_rejects_env_without_sandbox():
    """Toolset.__init__ should raise if env.sandbox is missing or None."""
    class NoSandboxEnv:
        sandbox = None

    with pytest.raises(ValueError, match="requires `env.sandbox`"):
        CLIToolset(NoSandboxEnv())


@pytest.mark.asyncio
async def test_cli_toolset_bash_propagates_exit_code():
    sandbox = FakeFsSandbox()
    sandbox.program(r"false", "", return_code=1)
    toolset = CLIToolset(_FakeEnv(sandbox))

    result = await toolset.bash(CliBashParams(command="false"))

    assert result.metadata["exit_code"] == 1
    assert "(exit 1)" in result.blocks[0].text


@pytest.mark.asyncio
async def test_cli_toolset_edit_not_found_errors_without_writing():
    sandbox = FakeFsSandbox(files={"/foo.txt": b"hello world\n"})
    toolset = CLIToolset(_FakeEnv(sandbox))
    EditParams = CliEditParams

    result = await toolset.edit(EditParams(
        file_path="/foo.txt", old_string="goodbye", new_string="bye",
    ))

    assert "not found" in result.blocks[0].text.lower()
    assert "not found" in result.metadata["error"].lower()
    # File untouched, and no check_run upload was issued.
    assert sandbox.files["/foo.txt"] == b"hello world\n"
    assert sandbox.check_run_log == []


@pytest.mark.asyncio
async def test_cli_toolset_edit_strict_uniqueness_blocks_ambiguous_replace():
    """Non-unique old_string without replace_all should error, not replace first."""
    sandbox = FakeFsSandbox(files={"/foo.txt": b"x\nx\nx\n"})
    toolset = CLIToolset(_FakeEnv(sandbox))
    EditParams = CliEditParams

    result = await toolset.edit(EditParams(
        file_path="/foo.txt", old_string="x", new_string="y", replace_all=False,
    ))

    assert "appears 3 times" in result.metadata["error"]
    # File untouched (the bug: legacy sed-based edit would have replaced first).
    assert sandbox.files["/foo.txt"] == b"x\nx\nx\n"
    assert sandbox.check_run_log == []


@pytest.mark.asyncio
async def test_cli_toolset_edit_replace_all_replaces_every_occurrence():
    sandbox = FakeFsSandbox(files={"/foo.txt": b"x\nx\nx\n"})
    toolset = CLIToolset(_FakeEnv(sandbox))
    EditParams = CliEditParams

    result = await toolset.edit(EditParams(
        file_path="/foo.txt", old_string="x", new_string="y", replace_all=True,
    ))

    assert result.metadata == {"output": "", "exit_code": 0}
    assert _read_text(sandbox, "/foo.txt") == "y\ny\ny\n"


@pytest.mark.asyncio
async def test_cli_toolset_edit_multiline_with_regex_metacharacters():
    """The exact failure mode the legacy sed-based edit silently no-op'd on."""
    src = (
        "fn parse(s: &str) -> Result<i64, String> {\n"
        "    let mut i = 0;\n"
        "    while i < s.len() {\n"
        "        // body with [*]./()|+? metachars\n"
        "    }\n"
        "    Ok(0)\n"
        "}\n"
    )
    sandbox = FakeFsSandbox(files={"/lib.rs": src.encode("utf-8")})
    toolset = CLIToolset(_FakeEnv(sandbox))
    EditParams = CliEditParams

    old = "    while i < s.len() {\n        // body with [*]./()|+? metachars\n    }\n"
    new = "    /* body removed */\n"
    result = await toolset.edit(EditParams(
        file_path="/lib.rs", old_string=old, new_string=new,
    ))

    assert "Successfully edited" in result.blocks[0].text
    assert "/* body removed */" in _read_text(sandbox, "/lib.rs")
    assert "metachars" not in _read_text(sandbox, "/lib.rs")


@pytest.mark.asyncio
async def test_cli_toolset_multi_edit_applies_sequentially():
    sandbox = FakeFsSandbox(files={"/foo.txt": b"alpha beta gamma\n"})
    toolset = CLIToolset(_FakeEnv(sandbox))
    MultiEditParams = CliMultiEditParams

    result = await toolset.multi_edit(MultiEditParams(
        file_path="/foo.txt",
        edits=[
            {"old_string": "alpha", "new_string": "A"},
            {"old_string": "beta", "new_string": "B"},
            {"old_string": "gamma", "new_string": "G"},
        ],
    ))

    assert result.metadata["total_replacements"] == 3
    assert result.metadata["edits_applied"] == 3
    assert _read_text(sandbox, "/foo.txt") == "A B G\n"


@pytest.mark.asyncio
async def test_cli_toolset_multi_edit_missing_string_aborts_atomically():
    """If any edit's old_string is missing, the whole multi_edit must fail and not write."""
    sandbox = FakeFsSandbox(files={"/foo.txt": b"alpha beta\n"})
    toolset = CLIToolset(_FakeEnv(sandbox))
    MultiEditParams = CliMultiEditParams

    result = await toolset.multi_edit(MultiEditParams(
        file_path="/foo.txt",
        edits=[
            {"old_string": "alpha", "new_string": "A"},
            {"old_string": "MISSING", "new_string": "X"},
        ],
    ))

    assert "'MISSING' not found" in result.metadata["error"]
    # File untouched: no check_run upload happened.
    assert sandbox.files["/foo.txt"] == b"alpha beta\n"
    assert sandbox.check_run_log == []


@pytest.mark.asyncio
async def test_cli_toolset_todo_write_stores_on_toolset_not_env():
    sandbox = FakeFsSandbox()
    env = _FakeEnv(sandbox)
    toolset = CLIToolset(env)
    TodoWriteParams = CliTodoWriteParams

    todos = [{"id": "1", "content": "do thing", "status": "pending", "priority": "high"}]
    result = toolset.todo_write(TodoWriteParams(todos=todos))

    assert result.metadata["count"] == 1
    assert toolset.todos == todos
    assert not hasattr(env, "todos")


@pytest.mark.asyncio
async def test_cli_toolset_write_creates_parent_dir_and_uploads():
    sandbox = FakeFsSandbox()
    toolset = CLIToolset(_FakeEnv(sandbox))
    WriteParams = CliWriteParams

    await toolset.write(WriteParams(file_path="/work/sub/out.txt", content="hello"))

    # Parent dir creation should have run mkdir -p.
    assert any("mkdir -p /work/sub" in c for c in sandbox.run_log)
    assert sandbox.files["/work/sub/out.txt"] == b"hello\n"


@pytest.mark.asyncio
async def test_cli_toolset_read_uses_download_when_no_offset_or_limit():
    sandbox = FakeFsSandbox(files={"/foo.txt": b"line1\nline2\nline3\n"})
    toolset = CLIToolset(_FakeEnv(sandbox))
    ReadParams = CliReadParams

    result = await toolset.read(ReadParams(file_path="/foo.txt"))

    # cat -n style numbering, no `sed`/`tail`/`head` ran.
    assert "1\tline1" in result.metadata["output"]
    assert "2\tline2" in result.metadata["output"]
    assert "3\tline3" in result.metadata["output"]
    assert sandbox.run_log == []  # download path only


@pytest.mark.asyncio
async def test_cli_toolset_grep_uses_include_field():
    sandbox = FakeFsSandbox()
    sandbox.program(r"find .* -name '\*\.py'", "match.txt\n", return_code=0)
    toolset = CLIToolset(_FakeEnv(sandbox))
    GrepParams = CliGrepParams

    result = await toolset.grep(GrepParams(pattern="foo", include="*.py"))

    # CLIToolset uses `include` (legacy env-local naming); ClaudeCodeToolset uses `glob`.
    assert any("find" in c and "-name '*.py'" in c for c in sandbox.run_log)
    assert result.metadata["exit_code"] == 0


@pytest.mark.asyncio
async def test_cli_toolset_ls_runs_ls_la():
    sandbox = FakeFsSandbox()
    toolset = CLIToolset(_FakeEnv(sandbox))
    LSParams = CliLSParams

    await toolset.ls(LSParams(path="/srv/data"))

    assert sandbox.run_log == ["ls -la /srv/data"]


@pytest.mark.asyncio
async def test_cli_toolset_glob_runs_find_sorted():
    sandbox = FakeFsSandbox()
    toolset = CLIToolset(_FakeEnv(sandbox))
    GlobParams = CliGlobParams

    await toolset.glob(GlobParams(pattern="*.rs", path="/workspace"))

    assert sandbox.run_log == ["find /workspace -name '*.rs' -type f | sort"]


@pytest.mark.asyncio
async def test_cli_toolset_registered_in_builtin_toolsets():
    """CLIToolset should be discoverable via the session toolset registry."""
    from openreward.toolsets import BUILTIN_TOOLSETS
    assert "cli" in BUILTIN_TOOLSETS
    assert BUILTIN_TOOLSETS["cli"] is CLIToolset
