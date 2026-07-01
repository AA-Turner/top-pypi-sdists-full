"""Tests for session-scoped toolsets passed via env.session(toolset=...).

These tests run a real Server bound to in-process environments that use a
mock sandbox, so the ClaudeCodeToolset / CodexToolset tools execute end-to-end
through the HTTP layer (POST /create, GET /task_tools, POST /call).
"""

import asyncio
import base64
from threading import Thread
from typing import Generator

import aiohttp
import pytest
import uvicorn

from openreward import AsyncOpenReward
from openreward.api.environments.types import ToolCallError
from openreward.api.sandboxes.types import RunResult
from openreward.environments import Environment, Server, ToolOutput, tool
from openreward.environments.types import Blocks, JSONObject, TextBlock
from openreward.toolsets import ClaudeCodeToolset


# ── Mock sandbox that records every call ──

class _MockSandbox:
    """Tracks calls to run/check_run/upload/download for assertions."""

    def __init__(self) -> None:
        self.commands: list[str] = []
        self.files: dict[str, bytes] = {}

    async def run(self, cmd: str, **kwargs) -> RunResult:
        self.commands.append(cmd)
        return RunResult(output=f"ran: {cmd}", return_code=0)

    async def check_run(self, cmd: str, **kwargs) -> str:
        self.commands.append(cmd)
        # Emulate "echo BASE64 | base64 -d > path" used by _upload_text.
        if " | base64 -d > " in cmd:
            encoded = cmd.split("'", 2)[1]
            path = cmd.split(" > ", 1)[1]
            self.files[path] = base64.b64decode(encoded)
        return ""

    async def download(self, path: str) -> bytes:
        return self.files.get(path, b"")

    async def upload(self, local_path, container_path: str) -> None:  # pragma: no cover
        with open(local_path, "rb") as f:
            self.files[container_path] = f.read()


# ── Test environments ──

class EnvWithSandbox(Environment):
    """Environment that exposes a mock sandbox and an own ``bash`` tool to
    verify that the session toolset overrides same-named env tools."""

    def __init__(self, task_spec: JSONObject = {}, secrets: dict[str, str] = {}) -> None:
        super().__init__(task_spec, secrets)
        self.sandbox = _MockSandbox()

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="prompt")]

    @tool
    async def bash(self) -> ToolOutput:
        """Env-defined bash that should be overridden by the toolset."""
        return ToolOutput(blocks=[TextBlock(text="ENV_BASH")], reward=0.0, finished=False)

    @tool
    async def submit(self) -> ToolOutput:
        """Env-defined submit tool."""
        return ToolOutput(blocks=[TextBlock(text="submitted")], reward=1.0, finished=True)


class EnvWithoutSandbox(Environment):
    """Environment with no ``self.sandbox`` — toolset binding must raise."""

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1"}]

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="prompt")]

    @tool
    async def submit(self) -> ToolOutput:
        """Env-defined submit tool."""
        return ToolOutput(blocks=[TextBlock(text="submitted")], reward=1.0, finished=True)


# ── Server fixture (separate port from test_environment.py) ──

async def _wait_for_server(base_url: str, timeout: float = 5.0) -> None:
    import time
    start = time.monotonic()
    async with aiohttp.ClientSession() as session:
        while time.monotonic() - start < timeout:
            try:
                async with session.get(
                    f"{base_url}/health",
                    timeout=aiohttp.ClientTimeout(total=0.5),
                ) as resp:
                    if resp.status == 200:
                        return
            except Exception:
                pass
            await asyncio.sleep(0.1)
    pytest.fail("Server failed to start")


@pytest.fixture(scope="module")
def server() -> Generator[str, None, None]:
    host = "localhost"
    port = 8082
    app = Server(environments=[EnvWithSandbox, EnvWithoutSandbox]).app
    config = uvicorn.Config(app, host=host, port=port, log_level="warning")
    instance = uvicorn.Server(config)

    thread = Thread(target=instance.run, daemon=True)
    thread.start()

    base_url = f"http://{host}:{port}"
    asyncio.run(_wait_for_server(base_url))
    yield base_url
    instance.should_exit = True


@pytest.fixture
def client() -> AsyncOpenReward:
    return AsyncOpenReward(api_key="test")


# ── list_tools merging ──

CLAUDE_CODE_TOOLS = {"bash", "glob", "grep", "read", "write", "edit", "todo_write"}


@pytest.mark.asyncio
async def test_session_with_toolset_lists_merged_tools(client: AsyncOpenReward, server: str):
    env = client.environments.get("envwithsandbox", variant="envwithsandbox", base_url=server)
    tasks = await env.list_tasks(split="train")
    async with env.session(tasks[0], toolset="claude-code") as session:
        tools = await session.list_tools()
        names = [t.name for t in tools]
        for name in CLAUDE_CODE_TOOLS:
            assert name in names, f"missing tool {name}"
        # Env's other non-overridden tool is preserved.
        assert "submit" in names
        # The env's `bash` is replaced by the toolset's `bash`. The firehorse
        # description starts with "Executes a given bash command".
        bash_spec = next(t for t in tools if t.name == "bash")
        assert bash_spec.description.startswith("Executes a given bash command")


@pytest.mark.asyncio
async def test_session_without_toolset_unchanged(client: AsyncOpenReward, server: str):
    env = client.environments.get("envwithsandbox", variant="envwithsandbox", base_url=server)
    tasks = await env.list_tasks(split="train")
    async with env.session(tasks[0]) as session:
        tools = await session.list_tools()
        names = {t.name for t in tools}
        assert names == {"bash", "submit"}


# ── call_tool routing ──

@pytest.mark.asyncio
async def test_session_toolset_call_routes_to_toolset(client: AsyncOpenReward, server: str):
    env = client.environments.get("envwithsandbox", variant="envwithsandbox", base_url=server)
    tasks = await env.list_tasks(split="train")
    async with env.session(tasks[0], toolset="claude-code") as session:
        result = await session.call_tool("bash", {"command": "echo hi"})
        # Toolset bash uses sandbox.run and prefixes the output with "ran: ".
        assert "ran: echo hi" in result.blocks[0].text
        # The env-level bash returns "ENV_BASH" — confirm we did NOT hit it.
        assert "ENV_BASH" not in result.blocks[0].text


@pytest.mark.asyncio
async def test_session_toolset_write_then_read_roundtrip(client: AsyncOpenReward, server: str):
    env = client.environments.get("envwithsandbox", variant="envwithsandbox", base_url=server)
    tasks = await env.list_tasks(split="train")
    async with env.session(tasks[0], toolset="claude-code") as session:
        await session.call_tool("write", {"file_path": "/tmp/x.txt", "content": "hello"})
        result = await session.call_tool("read", {"file_path": "/tmp/x.txt"})
        # Read uses cat -n format on each line.
        assert "hello" in result.blocks[0].text


# ── No-sandbox env raises ──

@pytest.mark.asyncio
async def test_session_toolset_no_sandbox_raises(client: AsyncOpenReward, server: str):
    env = client.environments.get(
        "envwithoutsandbox", variant="envwithoutsandbox", base_url=server,
    )
    tasks = await env.list_tasks(split="train")
    # Server stores the ValueError in setup_errors and raises it on the next
    # request that hits require_existing_session (e.g. list_tools/call_tool).
    with pytest.raises(Exception) as exc_info:
        async with env.session(tasks[0], toolset="claude-code") as session:
            await session.list_tools()
    msg = str(exc_info.value)
    assert "sandbox" in msg.lower()


# ── Codex toolset ──

@pytest.mark.asyncio
async def test_codex_toolset_only_bash(client: AsyncOpenReward, server: str):
    env = client.environments.get("envwithsandbox", variant="envwithsandbox", base_url=server)
    tasks = await env.list_tasks(split="train")
    async with env.session(tasks[0], toolset="codex") as session:
        tools = await session.list_tools()
        toolset_names = {t.name for t in tools}
        # Codex toolset only contributes bash; env's submit + replaced bash.
        assert "bash" in toolset_names
        assert "submit" in toolset_names
        # Codex toolset has none of the read/write/etc.
        for name in ("read", "write", "edit", "grep", "glob", "todo_write"):
            assert name not in toolset_names
        bash_spec = next(t for t in tools if t.name == "bash")
        # Codex bash description is the upstream Codex shell_command line.
        assert bash_spec.description.startswith("Runs a shell command")


# ── Client-side rejection of unknown toolset ──

@pytest.mark.asyncio
async def test_unknown_toolset_name_rejected_clientside(client: AsyncOpenReward, server: str):
    env = client.environments.get("envwithsandbox", variant="envwithsandbox", base_url=server)
    with pytest.raises(ValueError, match="Unknown toolset"):
        env.session(split="train", index=0, toolset="nonexistent")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_session_toolset_warns_on_shadow(monkeypatch):
    """When the session toolset shadows an env tool of the same name, log a warning.

    Tests the session helpers directly (no HTTP) so we can monkey-patch the
    logger and observe warnings — ``structlog.testing.capture_logs`` won't
    cross the uvicorn worker thread boundary.
    """
    from openreward.environments import session as session_module
    from openreward.environments.session import call_session_tool, list_session_tools

    captured: list[tuple[str, dict]] = []

    def fake_warning(event, **kwargs):
        captured.append((event, kwargs))

    monkeypatch.setattr(session_module.logger, "warning", fake_warning)

    env = EnvWithSandbox(task_spec={"id": "1"})
    toolset = ClaudeCodeToolset(env)

    # Listing tools should fire a shadow warning for `bash`.
    await list_session_tools(env, toolset)
    list_warnings = [e for e in captured if e[0] == "session_toolset_shadows_env_tool"]
    assert len(list_warnings) >= 1
    assert any(e[1].get("tool") == "bash" for e in list_warnings)
    assert any(e[1].get("toolset") == "ClaudeCodeToolset" for e in list_warnings)

    # Calling the shadowed tool should fire another warning.
    captured.clear()
    await call_session_tool(env, toolset, "bash", {"command": "echo hi"})
    call_warnings = [e for e in captured if e[0] == "session_toolset_shadows_env_tool"]
    assert len(call_warnings) == 1
    assert call_warnings[0][1]["tool"] == "bash"
