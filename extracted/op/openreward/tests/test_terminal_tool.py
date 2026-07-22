"""Tests for the @terminal decorator and the terminal-tool plumbing.

A terminal tool is hidden from the tool list the model sees; instead the
harness treats a plain assistant message as the end of the rollout and routes
its text into the tool via call_terminal_tool().
"""

import asyncio
from threading import Thread
from typing import Generator

import aiohttp
import pytest
import uvicorn
from pydantic import BaseModel

from openreward import AsyncOpenReward
from openreward.environments import (Environment, Server, TerminalToolSpec,
                                     Toolset, terminal, tool)
from openreward.environments.session import call_session_tool, list_session_tools
from openreward.environments.types import Blocks, JSONObject, TextBlock, ToolOutput


class Answer(BaseModel):
    answer: str


class TwoFields(BaseModel):
    answer: str
    confidence: float


class _Base(Environment):
    def get_prompt(self) -> Blocks:
        return [TextBlock(text="what is 2+2?")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"expected": "4"}]


class TerminalEnv(_Base):
    """Environment whose final assistant message is the answer."""

    @tool
    async def think(self) -> ToolOutput:
        """A visible scratchpad tool."""
        return ToolOutput(blocks=[TextBlock(text="ok")])

    @terminal
    @tool
    async def submit_answer(self, args: Answer) -> ToolOutput:
        """Grade the assistant's final message."""
        correct = args.answer.strip() == self.task_spec["expected"]
        return ToolOutput(
            blocks=[TextBlock(text="graded")],
            reward=1.0 if correct else 0.0,
            finished=True,
        )


class PlainEnv(_Base):
    """Environment with no terminal tool."""

    @tool
    async def submit(self, args: Answer) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="done")], reward=1.0, finished=True)


# --- environment-side discovery -------------------------------------------------


def test_terminal_tool_is_discovered():
    term = TerminalEnv.list_tools().terminal_tool
    assert term == TerminalToolSpec(
        name="submit_answer",
        arg="answer",
        description="Grade the assistant's final message.",
    )


def test_terminal_tool_hidden_from_list_tools():
    names = [t.name for t in TerminalEnv.list_tools().tools]
    assert names == ["think"]


def test_is_assistant_message_final():
    assert TerminalEnv.is_assistant_message_final() is True
    assert PlainEnv.is_assistant_message_final() is False
    assert PlainEnv.list_tools().terminal_tool is None


@pytest.mark.asyncio
async def test_call_terminal_tool_routes_message():
    env = TerminalEnv(task_spec={"expected": "4"})
    res = await env.call_terminal_tool("4")
    assert res.root.ok is True
    assert res.root.output.reward == 1.0

    wrong = await env.call_terminal_tool("5")
    assert wrong.root.output.reward == 0.0


@pytest.mark.asyncio
async def test_call_terminal_tool_without_terminal_tool_raises():
    env = PlainEnv(task_spec={"expected": "4"})
    with pytest.raises(ValueError, match="no @terminal tool"):
        await env.call_terminal_tool("4")


@pytest.mark.asyncio
async def test_terminal_tool_still_callable_by_name():
    """Hiding it from list_tools must not break dispatch."""
    env = TerminalEnv(task_spec={"expected": "4"})
    res = await env._call_tool("submit_answer", {"answer": "4"})
    assert res.root.ok is True


# --- validation errors ----------------------------------------------------------


def test_multiple_terminal_tools_raises():
    class TwoTerminals(_Base):
        @terminal
        @tool
        async def submit_a(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

        @terminal
        @tool
        async def submit_b(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

    with pytest.raises(ValueError, match="Multiple @terminal tools"):
        TwoTerminals.list_tools()


def test_terminal_tool_in_env_and_toolset_raises():
    class TerminalToolset(Toolset):
        def __init__(self, env=None):
            pass

        @terminal
        @tool
        async def finish(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

    class Clashing(_Base):
        toolsets = [TerminalToolset]

        @terminal
        @tool
        async def submit_answer(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

    with pytest.raises(ValueError, match="Multiple @terminal tools"):
        Clashing.list_tools()


def test_terminal_tool_with_multiple_fields_raises():
    class MultiField(_Base):
        @terminal
        @tool
        async def submit_answer(self, args: TwoFields) -> ToolOutput:
            return ToolOutput(blocks=[])

    with pytest.raises(ValueError, match="at most one argument"):
        MultiField.list_tools()


def test_terminal_without_tool_raises():
    """@terminal marks an existing tool; it does not declare one."""

    class Bare(_Base):
        @tool
        async def think(self) -> ToolOutput:
            return ToolOutput(blocks=[])

        @terminal
        async def submit_answer(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

    with pytest.raises(ValueError, match="missing @tool"):
        Bare.list_tools()


def test_terminal_decorator_order_is_irrelevant():
    """Docs put @terminal on top; @tool on top must behave identically."""

    class ToolOutermost(_Base):
        @tool
        @terminal
        async def submit_answer(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

    term = ToolOutermost.list_tools().terminal_tool
    assert term is not None and term.arg == "answer"
    assert ToolOutermost.list_tools().tools == []


def test_env_with_only_a_terminal_tool_is_valid():
    class OnlyTerminal(_Base):
        @terminal
        @tool
        async def submit_answer(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[])

    assert OnlyTerminal.list_tools().tools == []
    assert OnlyTerminal.list_tools().terminal_tool is not None
    Server(environments=[OnlyTerminal])


# --- terminal tools that take no arguments --------------------------------------


class NoArgTerminalEnv(_Base):
    """Grades from environment state; the final message just ends the rollout."""

    @terminal
    @tool
    async def finish(self) -> ToolOutput:
        """Score whatever the environment currently holds."""
        return ToolOutput(blocks=[TextBlock(text="scored")], reward=0.25, finished=True)


def test_no_arg_terminal_tool_has_no_arg():
    term = NoArgTerminalEnv.list_tools().terminal_tool
    assert term is not None
    assert term.name == "finish"
    assert term.arg is None
    assert NoArgTerminalEnv.is_assistant_message_final() is True
    assert NoArgTerminalEnv.list_tools().tools == []


@pytest.mark.asyncio
async def test_no_arg_terminal_tool_drops_the_message():
    env = NoArgTerminalEnv(task_spec={})
    res = await env.call_terminal_tool("this text is not passed on")
    assert res.root.ok is True
    assert res.root.output.reward == 0.25
    # Callable with no message at all.
    assert (await env.call_terminal_tool()).root.output.reward == 0.25


def test_terminal_tool_with_empty_model_takes_no_arg():
    class Empty(BaseModel):
        pass

    class EmptyModelEnv(_Base):
        @terminal
        @tool
        async def finish(self, args: Empty) -> ToolOutput:
            return ToolOutput(blocks=[])

    term = EmptyModelEnv.list_tools().terminal_tool
    assert term is not None and term.arg is None


# --- session merging ------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_session_tools_hides_terminal_tool():
    env = TerminalEnv(task_spec={"expected": "4"})
    listed = await list_session_tools(env, None)
    assert [t.name for t in listed.tools] == ["think"]
    assert listed.terminal_tool is not None
    assert listed.terminal_tool.name == "submit_answer"


@pytest.mark.asyncio
async def test_session_toolset_terminal_tool_wins():
    class OverridingToolset(Toolset):
        def __init__(self, env=None):
            pass

        @terminal
        @tool
        async def finish(self, args: Answer) -> ToolOutput:
            return ToolOutput(blocks=[TextBlock(text="toolset")], reward=0.5, finished=True)

    env = PlainEnv(task_spec={"expected": "4"})
    listed = await list_session_tools(env, OverridingToolset())
    assert listed.terminal_tool is not None
    assert listed.terminal_tool.name == "finish"
    assert "finish" not in [t.name for t in listed.tools]

    res = await call_session_tool(env, OverridingToolset(), "finish", {"answer": "4"})
    assert res.root.ok is True
    assert res.root.output.reward == 0.5


# --- end-to-end over the wire ---------------------------------------------------


async def wait_for_server(base_url: str, timeout: float = 5.0):
    import time
    start = time.monotonic()
    async with aiohttp.ClientSession() as session:
        while time.monotonic() - start < timeout:
            try:
                async with session.get(f"{base_url}/health", timeout=aiohttp.ClientTimeout(total=0.5)) as resp:
                    if resp.status == 200:
                        return
            except Exception:
                pass
            await asyncio.sleep(0.1)
    pytest.fail("Server failed to start")


@pytest.fixture(scope="module")
def server() -> Generator[str, None, None]:
    host, port = "localhost", 8087
    app = Server(environments=[TerminalEnv, PlainEnv]).app
    config = uvicorn.Config(app, host=host, port=port, log_level="warning")
    server_instance = uvicorn.Server(config)
    thread = Thread(target=server_instance.run, daemon=True)
    thread.start()
    base_url = f"http://{host}:{port}"
    asyncio.run(wait_for_server(base_url))
    yield base_url
    server_instance.should_exit = True


@pytest.fixture
def client() -> AsyncOpenReward:
    return AsyncOpenReward(api_key="test")


@pytest.mark.asyncio
async def test_env_level_terminal_tool_over_wire(client: AsyncOpenReward, server: str):
    environment = client.environments.get("terminalenv", variant="terminalenv", base_url=server)
    assert await environment.is_assistant_message_final() is True
    term = await environment.terminal_tool()
    assert term is not None and term.name == "submit_answer" and term.arg == "answer"
    assert [t.name for t in await environment.list_tools()] == ["think"]


@pytest.mark.asyncio
async def test_plain_env_reports_no_terminal_tool(client: AsyncOpenReward, server: str):
    environment = client.environments.get("plainenv", variant="plainenv", base_url=server)
    assert await environment.is_assistant_message_final() is False
    assert await environment.terminal_tool() is None


@pytest.mark.asyncio
async def test_session_call_terminal_tool(client: AsyncOpenReward, server: str):
    environment = client.environments.get("terminalenv", variant="terminalenv", base_url=server)
    tasks = await environment.list_tasks(split="train")
    async with environment.session(tasks[0]) as session:
        assert await session.is_assistant_message_final() is True
        assert "submit_answer" not in [t.name for t in await session.list_tools()]

        out = await session.call_terminal_tool("4")
        assert out.reward == 1.0
        assert out.finished is True


@pytest.mark.asyncio
async def test_session_call_terminal_tool_without_one(client: AsyncOpenReward, server: str):
    from openreward.api.errors import ToolCallError

    environment = client.environments.get("plainenv", variant="plainenv", base_url=server)
    tasks = await environment.list_tasks(split="train")
    async with environment.session(tasks[0]) as session:
        assert await session.is_assistant_message_final() is False
        with pytest.raises(ToolCallError):
            await session.call_terminal_tool("4")
