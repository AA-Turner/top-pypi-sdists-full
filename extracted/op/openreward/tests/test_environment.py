import pytest
import asyncio
import uvicorn
import aiohttp
from threading import Thread
from typing import Generator, Optional
from openreward import AsyncOpenReward
from openreward.environments import Environment, Server, tool, ToolOutput
from openreward.environments.types import Blocks, TextBlock, JSONObject, ToolSpec, ListToolsOutput


class Foo(Environment):
    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text=str(self.task_spec["foo"]))]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        assert split == "train"
        return [{"foo": "bar"}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="foo_result")], reward=1.0, finished=True)


class Bar(Environment):
    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text=str(self.task_spec["bar"]))]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["test"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        assert split == "test"
        return [{"bar": "baz"}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="bar_result")], reward=0.5, finished=True)


class AsyncBaz(Environment):
    """Environment with async list_tasks to test maybe_await in the server."""

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text=str(self.task_spec["baz"]))]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    async def list_tasks(cls, split: str) -> list[JSONObject]:
        assert split == "train"
        return [{"baz": "qux"}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="baz_result")], reward=0.75, finished=True)

class LargeEnv(Environment):
    """Environment that overrides num_tasks/get_task to avoid materializing all tasks."""

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text=f"task_{self.task_spec['id']}")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train", "test"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        raise NotImplementedError("LargeEnv doesn't support listing all tasks")

    @classmethod
    async def num_tasks(cls, split: str) -> int:
        """Return a fixed count without materializing tasks."""
        return {"train": 1000, "test": 200}[split]

    @classmethod
    async def get_task(cls, split: str, index: int) -> JSONObject:
        """Generate a task on-the-fly by index."""
        limit = {"train": 1000, "test": 200}[split]
        if index < 0 or index >= limit:
            raise IndexError(f"index {index} out of range for split {split}")
        return {"id": index, "split": split}

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(
            blocks=[TextBlock(text=f"result_{self.task_spec['id']}")],
            reward=self.task_spec["id"] / 1000,
            finished=True,
        )

class EnvWithTaskTools(Environment):
    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="task tools prompt")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{"id": "1", "tools": ["read_file", "write_file"]}]

    def list_task_tools(self) -> ListToolsOutput:
        tools = []
        for tool_name in self.task_spec.get("tools", []):
            tools.append(ToolSpec(name=tool_name, description=f"Task tool: {tool_name}", input_schema=None))
        return ListToolsOutput(tools=tools)

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="task_tools_result")], reward=1.0, finished=True)

    @tool(shared=False)
    async def non_shared_helper(self) -> ToolOutput:
        """A non-shared tool that should not appear in env.list_tools()"""
        return ToolOutput(blocks=[TextBlock(text="helper")], reward=0.0, finished=False)


class SlowSetupEnv(Environment):
    """Environment whose setup() takes a long time — used to verify that
    /task_tools returns before setup() completes."""

    def setup(self):
        return asyncio.sleep(30)

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="prompt-before-setup")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        assert split == "train"
        return [{}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="submitted")], reward=1.0, finished=True)


_BLOCKING_PROMPT_SETUP_DELAY = 1.0


class BlockingPromptEnv(Environment):
    """Env whose get_prompt() depends on setup() — verifies that /prompt
    waits for setup when requires_setup_for_prompt is True (the default)."""

    def __init__(self, task_spec: JSONObject = {}, secrets: dict[str, str] = {}) -> None:
        super().__init__(task_spec, secrets)
        self.prompt_text: Optional[str] = None

    async def setup(self):
        await asyncio.sleep(_BLOCKING_PROMPT_SETUP_DELAY)
        self.prompt_text = "prompt-after-setup"

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        assert self.prompt_text is not None, "get_prompt() ran before setup() completed"
        return [TextBlock(text=self.prompt_text)]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        assert split == "train"
        return [{}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="submitted")], reward=1.0, finished=True)


_BLOCKING_LIST_TASKS_DELAY = 1.5


class BlockingListTasksEnv(Environment):
    """Env whose sync list_tasks blocks for a while — used to verify that
    sync user callbacks don't freeze the event loop."""

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="blocking")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["slow"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        import time as _time
        _time.sleep(_BLOCKING_LIST_TASKS_DELAY)
        return [{}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="ok")], reward=1.0, finished=True)


_BLOCKING_TOOL_DELAY = 1.5


class BlockingToolEnv(Environment):
    """Env whose @tool body is sync and blocks — used to verify that
    in-flight tool calls don't freeze the event loop."""

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="blocking-tool")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{}]

    @tool
    def slow(self) -> ToolOutput:
        import time as _time
        _time.sleep(_BLOCKING_TOOL_DELAY)
        return ToolOutput(blocks=[TextBlock(text="slept")], reward=0.0, finished=True)


_BLOCKING_INIT_DELAY = 1.5


class BlockingInitEnv(Environment):
    """Env whose __init__ blocks — used to verify that a heavy env constructor
    (run by /create) doesn't freeze the event loop for other sessions."""

    def __init__(self, task_spec: JSONObject = {}, secrets: dict[str, str] = {}) -> None:
        import time as _time
        _time.sleep(_BLOCKING_INIT_DELAY)
        super().__init__(task_spec, secrets)

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_prompt(self) -> Blocks:
        return [TextBlock(text="blocking-init")]

    @classmethod
    def list_splits(cls) -> list[str]:
        return ["train"]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        return [{}]

    @tool
    async def submit(self) -> ToolOutput:
        return ToolOutput(blocks=[TextBlock(text="ok")], reward=1.0, finished=True)


async def wait_for_server(base_url: str, timeout: float = 5.0):
    """Wait for server to be ready using aiohttp."""
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
    """Start the server in a background thread and yield the base URL."""
    host = "localhost"
    port = 8080
    app = Server(environments=[Foo, Bar, AsyncBaz, LargeEnv, EnvWithTaskTools, SlowSetupEnv, BlockingPromptEnv, BlockingListTasksEnv, BlockingToolEnv, BlockingInitEnv]).app
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
    """Create an async client."""
    return AsyncOpenReward(api_key="test")


# Tests for default environment (no variant specified, uses first env)

@pytest.mark.asyncio
async def test_default_variant_splits(client: AsyncOpenReward, server: str):
    """Test that default variant works - redirects to first environment."""
    environment = client.environments.get("foo", base_url=server)
    splits = await environment.list_splits()
    assert splits == ["train"]


@pytest.mark.asyncio
async def test_default_variant_tools(client: AsyncOpenReward, server: str):
    """Test listing tools with default variant."""
    environment = client.environments.get("foo", base_url=server)
    tools = await environment.list_tools()
    tool_names = [t.name for t in tools]
    assert "submit" in tool_names


@pytest.mark.asyncio
async def test_default_variant_list_tasks(client: AsyncOpenReward, server: str):
    """Test listing tasks with default variant."""
    environment = client.environments.get("foo", base_url=server)
    tasks = await environment.list_tasks(split="train")
    assert len(tasks) == 1
    assert tasks[0].task_spec == {"foo": "bar"}


@pytest.mark.asyncio
async def test_default_variant_call_tool(client: AsyncOpenReward, server: str):
    """Test calling tool with default variant."""
    environment = client.environments.get("foo", base_url=server)
    tasks = await environment.list_tasks(split="train")
    async with environment.session(tasks[0]) as session:
        res = await session.call_tool("submit")
        assert res.reward == 1.0
        assert res.finished is True
        assert len(res.blocks) == 1
        assert res.blocks[0].type == "text"
        assert res.blocks[0].text == "foo_result"


# Tests for explicit variants

@pytest.mark.asyncio
async def test_explicit_variant_foo_splits(client: AsyncOpenReward, server: str):
    """Test Foo environment with explicit variant."""
    environment = client.environments.get("foo", variant="foo", base_url=server)
    splits = await environment.list_splits()
    assert splits == ["train"]


@pytest.mark.asyncio
async def test_explicit_variant_bar_splits(client: AsyncOpenReward, server: str):
    """Test Bar environment with explicit variant."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    splits = await environment.list_splits()
    assert splits == ["test"]


@pytest.mark.asyncio
async def test_explicit_variant_bar_tools(client: AsyncOpenReward, server: str):
    """Test Bar environment tools with explicit variant."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    tools = await environment.list_tools()
    tool_names = [t.name for t in tools]
    assert "submit" in tool_names


@pytest.mark.asyncio
async def test_explicit_variant_bar_list_tasks(client: AsyncOpenReward, server: str):
    """Test Bar environment task listing with explicit variant."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    tasks = await environment.list_tasks(split="test")
    assert len(tasks) == 1
    assert tasks[0].task_spec == {"bar": "baz"}


@pytest.mark.asyncio
async def test_explicit_variant_bar_call_tool(client: AsyncOpenReward, server: str):
    """Test Bar environment tool call with explicit variant."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    tasks = await environment.list_tasks(split="test")
    async with environment.session(tasks[0]) as session:
        res = await session.call_tool("submit")
        assert res.reward == 0.5
        assert res.finished is True
        assert len(res.blocks) == 1
        assert res.blocks[0].type == "text"
        assert res.blocks[0].text == "bar_result"


# Tests for async list_tools

@pytest.mark.asyncio
async def test_async_list_tools_returns_correct_schema(client: AsyncOpenReward, server: str):
    """Test that async list_tools returns tool specs with correct structure."""
    environment = client.environments.get("foo", base_url=server)
    tools = await environment.list_tools()
    assert len(tools) >= 1
    submit_tool = next(t for t in tools if t.name == "submit")
    assert submit_tool.name == "submit"
    assert submit_tool.input_schema is None  # submit takes no input model


@pytest.mark.asyncio
async def test_async_list_tools_with_provider_format(client: AsyncOpenReward, server: str):
    """Test that async list_tools works with provider-specific formats."""
    environment = client.environments.get("foo", base_url=server)

    openai_tools = await environment.list_tools(format="openai")
    assert len(openai_tools) >= 1
    assert openai_tools[0]["type"] == "function"
    assert openai_tools[0]["name"] == "submit"

    anthropic_tools = await environment.list_tools(format="anthropic")
    assert len(anthropic_tools) >= 1
    assert anthropic_tools[0]["type"] == "custom"
    assert anthropic_tools[0]["name"] == "submit"
    assert anthropic_tools[0]["input_schema"] == {"type": "object", "properties": {}}

    google_tools = await environment.list_tools(format="google")
    assert len(google_tools) >= 1
    assert google_tools[0]["name"] == "submit"


@pytest.mark.asyncio
async def test_async_list_tools_on_session(client: AsyncOpenReward, server: str):
    """Test that list_tools works on an active async session."""
    environment = client.environments.get("foo", base_url=server)
    tasks = await environment.list_tasks(split="train")
    async with environment.session(tasks[0]) as session:
        tools = await session.list_tools()
        tool_names = [t.name for t in tools]
        assert "submit" in tool_names


@pytest.mark.asyncio
async def test_async_list_tools_session_with_provider_format(client: AsyncOpenReward, server: str):
    """Test that session list_tools works with provider-specific formats."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    tasks = await environment.list_tasks(split="test")
    async with environment.session(tasks[0]) as session:
        openai_tools = await session.list_tools(format="openai")
        assert len(openai_tools) >= 1
        assert openai_tools[0]["type"] == "function"


# Tests for environment with async classmethods

@pytest.mark.asyncio
async def test_async_env_list_tools(client: AsyncOpenReward, server: str):
    """Test that list_tools works on an environment with async list_tasks."""
    environment = client.environments.get("asyncbaz", variant="asyncbaz", base_url=server)
    tools = await environment.list_tools()
    tool_names = [t.name for t in tools]
    assert "submit" in tool_names


@pytest.mark.asyncio
async def test_async_env_list_splits(client: AsyncOpenReward, server: str):
    """Test that list_splits works on an env with async list_tasks."""
    environment = client.environments.get("asyncbaz", variant="asyncbaz", base_url=server)
    splits = await environment.list_splits()
    assert splits == ["train"]


@pytest.mark.asyncio
async def test_async_env_list_tasks(client: AsyncOpenReward, server: str):
    """Test that async list_tasks is handled correctly."""
    environment = client.environments.get("asyncbaz", variant="asyncbaz", base_url=server)
    tasks = await environment.list_tasks(split="train")
    assert len(tasks) == 1
    assert tasks[0].task_spec == {"baz": "qux"}


@pytest.mark.asyncio
async def test_async_env_call_tool(client: AsyncOpenReward, server: str):
    """Test full session flow on an environment with async classmethods."""
    environment = client.environments.get("asyncbaz", variant="asyncbaz", base_url=server)
    tasks = await environment.list_tasks(split="train")
    async with environment.session(tasks[0]) as session:
        res = await session.call_tool("submit")
        assert res.reward == 0.75
        assert res.finished is True
        assert res.blocks[0].text == "baz_result"


# Tests for multiple variants interaction

@pytest.mark.asyncio
async def test_multiple_variants_different_splits(client: AsyncOpenReward, server: str):
    """Test that different variants return different splits."""
    foo_env = client.environments.get("foo", variant="foo", base_url=server)
    bar_env = client.environments.get("bar", variant="bar", base_url=server)

    foo_splits = await foo_env.list_splits()
    bar_splits = await bar_env.list_splits()

    assert foo_splits == ["train"]
    assert bar_splits == ["test"]
    assert foo_splits != bar_splits


@pytest.mark.asyncio
async def test_multiple_variants_different_tasks(client: AsyncOpenReward, server: str):
    """Test that different variants return different tasks."""
    foo_env = client.environments.get("foo", variant="foo", base_url=server)
    bar_env = client.environments.get("bar", variant="bar", base_url=server)

    foo_tasks = await foo_env.list_tasks(split="train")
    bar_tasks = await bar_env.list_tasks(split="test")

    assert foo_tasks[0].task_spec == {"foo": "bar"}
    assert bar_tasks[0].task_spec == {"bar": "baz"}


@pytest.mark.asyncio
async def test_multiple_variants_concurrent_sessions(client: AsyncOpenReward, server: str):
    """Test running sessions on multiple variants concurrently."""
    foo_env = client.environments.get("foo", variant="foo", base_url=server)
    bar_env = client.environments.get("bar", variant="bar", base_url=server)

    foo_tasks = await foo_env.list_tasks(split="train")
    bar_tasks = await bar_env.list_tasks(split="test")

    async with foo_env.session(foo_tasks[0]) as foo_session:
        async with bar_env.session(bar_tasks[0]) as bar_session:
            foo_res = await foo_session.call_tool("submit")
            bar_res = await bar_session.call_tool("submit")

            assert foo_res.reward == 1.0
            assert foo_res.blocks[0].text == "foo_result"

            assert bar_res.reward == 0.5
            assert bar_res.blocks[0].text == "bar_result"


@pytest.mark.asyncio
async def test_multiple_variants_prompt_isolation(client: AsyncOpenReward, server: str):
    """Test that prompts are correctly isolated between variants."""
    foo_env = client.environments.get("foo", variant="foo", base_url=server)
    bar_env = client.environments.get("bar", variant="bar", base_url=server)

    foo_tasks = await foo_env.list_tasks(split="train")
    bar_tasks = await bar_env.list_tasks(split="test")

    async with foo_env.session(foo_tasks[0]) as foo_session:
        foo_prompt = await foo_session.get_prompt()
        assert foo_prompt[0].text == "bar"  # from {"foo": "bar"}

    async with bar_env.session(bar_tasks[0]) as bar_session:
        bar_prompt = await bar_session.get_prompt()
        assert bar_prompt[0].text == "baz"  # from {"bar": "baz"}

# Tests for index-based API (num_tasks, get_task)

@pytest.mark.asyncio
async def test_num_tasks_foo(server: str):
    """Test num_tasks returns correct count for Foo."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/foo/num_tasks",
            json={"split": "train"},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["num_tasks"] == 1


@pytest.mark.asyncio
async def test_num_tasks_bar(server: str):
    """Test num_tasks returns correct count for Bar."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/bar/num_tasks",
            json={"split": "test"},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["num_tasks"] == 1


@pytest.mark.asyncio
async def test_num_tasks_invalid_split(server: str):
    """Test num_tasks rejects an invalid split."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/foo/num_tasks",
            json={"split": "nonexistent"},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_num_tasks_async_env(server: str):
    """Test num_tasks works for an environment with async list_tasks."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/asyncbaz/num_tasks",
            json={"split": "train"},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["num_tasks"] == 1


@pytest.mark.asyncio
async def test_get_task_foo(server: str):
    """Test get_task returns the correct task by index."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/foo/task",
            json={"split": "train", "index": 0},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["task"] == {"foo": "bar"}


@pytest.mark.asyncio
async def test_get_task_bar(server: str):
    """Test get_task on Bar environment."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/bar/task",
            json={"split": "test", "index": 0},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["task"] == {"bar": "baz"}


@pytest.mark.asyncio
async def test_get_task_invalid_split(server: str):
    """Test get_task rejects an invalid split."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/foo/task",
            json={"split": "nonexistent", "index": 0},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_get_task_index_out_of_bounds(server: str):
    """Test get_task returns 400 for an out-of-bounds index."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/foo/task",
            json={"split": "train", "index": 999},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_get_task_async_env(server: str):
    """Test get_task works for an environment with async list_tasks."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/asyncbaz/task",
            json={"split": "train", "index": 0},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["task"] == {"baz": "qux"}


@pytest.mark.asyncio
async def test_get_task_unknown_env(server: str):
    """Test get_task returns 404 for a nonexistent environment."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/doesnotexist/task",
            json={"split": "train", "index": 0},
        ) as resp:
            assert resp.status == 404


# Tests for LargeEnv (overridden num_tasks / get_task)

@pytest.mark.asyncio
async def test_large_env_list_tasks_returns_400(server: str):
    """Test that list_tasks returns 400 when env raises NotImplementedError."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/tasks",
            json={"split": "train"},
        ) as resp:
            assert resp.status == 400
            body = await resp.json()
            assert "index-based API" in body["detail"]


@pytest.mark.asyncio
async def test_large_env_num_tasks_train(server: str):
    """Test overridden num_tasks returns custom count for train."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/num_tasks",
            json={"split": "train"},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["num_tasks"] == 1000


@pytest.mark.asyncio
async def test_large_env_num_tasks_test(server: str):
    """Test overridden num_tasks returns custom count for test."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/num_tasks",
            json={"split": "test"},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["num_tasks"] == 200


@pytest.mark.asyncio
async def test_large_env_get_task_first(server: str):
    """Test overridden get_task returns correct task at index 0."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task",
            json={"split": "train", "index": 0},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["task"] == {"id": 0, "split": "train"}


@pytest.mark.asyncio
async def test_large_env_get_task_mid(server: str):
    """Test overridden get_task returns correct task at an arbitrary index."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task",
            json={"split": "train", "index": 500},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["task"] == {"id": 500, "split": "train"}


@pytest.mark.asyncio
async def test_large_env_get_task_last(server: str):
    """Test overridden get_task at the last valid index."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task",
            json={"split": "test", "index": 199},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["task"] == {"id": 199, "split": "test"}


@pytest.mark.asyncio
async def test_large_env_get_task_out_of_bounds(server: str):
    """Test overridden get_task rejects out-of-bounds index."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task",
            json={"split": "train", "index": 1000},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_large_env_get_task_invalid_split(server: str):
    """Test overridden get_task rejects invalid split."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/num_tasks",
            json={"split": "nonexistent"},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_large_env_session_from_get_task(server: str):
    """Test full session flow using split/index to create session."""
    sid = str(__import__("uuid").uuid4())
    headers = {"X-Session-ID": sid}
    async with aiohttp.ClientSession() as http:
        # Create session with split/index instead of task_spec
        async with http.post(
            f"{server}/create",
            json={"env_name": "largeenv", "split": "train", "index": 42},
            headers=headers,
        ) as resp:
            assert resp.status == 200

        # Call tool — server resolved task_spec internally
        async with http.post(
            f"{server}/largeenv/call",
            json={"name": "submit", "input": {}},
            headers=headers,
        ) as resp:
            assert resp.status == 200
            body = await resp.text()
            assert "result_42" in body

        # Cleanup
        async with http.post(f"{server}/delete", headers=headers) as resp:
            assert resp.status == 200


@pytest.mark.asyncio
async def test_create_session_rejects_both_spec_and_index(server: str):
    """Test that providing both task_spec and split/index is rejected."""
    sid = str(__import__("uuid").uuid4())
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "foo", "task_spec": {"foo": "bar"}, "split": "train", "index": 0},
            headers={"X-Session-ID": sid},
        ) as resp:
            assert resp.status == 422


@pytest.mark.asyncio
async def test_create_session_rejects_neither_spec_nor_index(server: str):
    """Test that providing neither task_spec nor split/index is rejected."""
    sid = str(__import__("uuid").uuid4())
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "foo"},
            headers={"X-Session-ID": sid},
        ) as resp:
            assert resp.status == 422


@pytest.mark.asyncio
async def test_create_session_rejects_split_without_index(server: str):
    """Test that providing split alone is rejected."""
    sid = str(__import__("uuid").uuid4())
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "foo", "split": "train"},
            headers={"X-Session-ID": sid},
        ) as resp:
            assert resp.status == 422


@pytest.mark.asyncio
async def test_create_session_invalid_split(server: str):
    """Test that an invalid split in create is rejected."""
    sid = str(__import__("uuid").uuid4())
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "foo", "split": "nonexistent", "index": 0},
            headers={"X-Session-ID": sid},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_create_session_index_out_of_bounds(server: str):
    """Test that an out-of-bounds index in create is rejected."""
    sid = str(__import__("uuid").uuid4())
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "largeenv", "split": "train", "index": 9999},
            headers={"X-Session-ID": sid},
        ) as resp:
            assert resp.status == 400


# Tests for index-based API via AsyncOpenReward client

@pytest.mark.asyncio
async def test_client_num_tasks_foo(client: AsyncOpenReward, server: str):
    """Test num_tasks via the client SDK."""
    environment = client.environments.get("foo", base_url=server)
    count = await environment.num_tasks("train")
    assert count == 1


@pytest.mark.asyncio
async def test_client_num_tasks_bar(client: AsyncOpenReward, server: str):
    """Test num_tasks on Bar via the client SDK."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    count = await environment.num_tasks("test")
    assert count == 1


@pytest.mark.asyncio
async def test_client_get_task_foo(client: AsyncOpenReward, server: str):
    """Test get_task via the client SDK."""
    environment = client.environments.get("foo", base_url=server)
    task = await environment.get_task("train", 0)
    assert task.task_spec == {"foo": "bar"}


@pytest.mark.asyncio
async def test_client_get_task_bar(client: AsyncOpenReward, server: str):
    """Test get_task on Bar via the client SDK."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    task = await environment.get_task("test", 0)
    assert task.task_spec == {"bar": "baz"}


@pytest.mark.asyncio
async def test_client_get_task_async_env(client: AsyncOpenReward, server: str):
    """Test get_task on an environment with async list_tasks."""
    environment = client.environments.get("asyncbaz", variant="asyncbaz", base_url=server)
    task = await environment.get_task("train", 0)
    assert task.task_spec == {"baz": "qux"}


@pytest.mark.asyncio
async def test_client_session_with_split_index(client: AsyncOpenReward, server: str):
    """Test creating a session via split/index instead of a Task object."""
    environment = client.environments.get("foo", base_url=server)
    async with environment.session(split="train", index=0) as session:
        res = await session.call_tool("submit")
        assert res.reward == 1.0
        assert res.finished is True
        assert res.blocks[0].text == "foo_result"


@pytest.mark.asyncio
async def test_client_session_with_split_index_bar(client: AsyncOpenReward, server: str):
    """Test split/index session on Bar."""
    environment = client.environments.get("bar", variant="bar", base_url=server)
    async with environment.session(split="test", index=0) as session:
        res = await session.call_tool("submit")
        assert res.reward == 0.5
        assert res.blocks[0].text == "bar_result"


@pytest.mark.asyncio
async def test_client_session_with_split_index_prompt(client: AsyncOpenReward, server: str):
    """Test that get_prompt works on a split/index session."""
    environment = client.environments.get("foo", base_url=server)
    async with environment.session(split="train", index=0) as session:
        prompt = await session.get_prompt()
        assert prompt[0].text == "bar"


@pytest.mark.asyncio
async def test_client_session_with_split_index_list_tools(client: AsyncOpenReward, server: str):
    """Test that list_tools works on a split/index session."""
    environment = client.environments.get("foo", base_url=server)
    async with environment.session(split="train", index=0) as session:
        tools = await session.list_tools()
        assert any(t.name == "submit" for t in tools)


@pytest.mark.asyncio
async def test_client_session_rejects_both_task_and_index(client: AsyncOpenReward, server: str):
    """Test that providing both task and split/index raises ValueError."""
    environment = client.environments.get("foo", base_url=server)
    task = await environment.get_task("train", 0)
    with pytest.raises(ValueError, match="either task or both split and index"):
        environment.session(task=task, split="train", index=0)


@pytest.mark.asyncio
async def test_client_session_rejects_neither_task_nor_index(client: AsyncOpenReward, server: str):
    """Test that providing neither task nor split/index raises ValueError."""
    environment = client.environments.get("foo", base_url=server)
    with pytest.raises(ValueError, match="either task or both split and index"):
        environment.session()


@pytest.mark.asyncio
async def test_client_session_rejects_split_without_index(client: AsyncOpenReward, server: str):
    """Test that providing split alone raises ValueError."""
    environment = client.environments.get("foo", base_url=server)
    with pytest.raises(ValueError, match="either task or both split and index"):
        environment.session(split="train")

# Tests for LargeEnv via the client SDK

@pytest.mark.asyncio
async def test_client_large_env_num_tasks(client: AsyncOpenReward, server: str):
    """Test num_tasks on LargeEnv via the client."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    assert await environment.num_tasks("train") == 1000
    assert await environment.num_tasks("test") == 200


@pytest.mark.asyncio
async def test_client_large_env_get_task(client: AsyncOpenReward, server: str):
    """Test get_task on LargeEnv via the client."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    task = await environment.get_task("train", 42)
    assert task.task_spec == {"id": 42, "split": "train"}


@pytest.mark.asyncio
async def test_client_large_env_session_with_task(client: AsyncOpenReward, server: str):
    """Test LargeEnv session created from a get_task result."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    task = await environment.get_task("train", 42)
    async with environment.session(task=task) as session:
        res = await session.call_tool("submit")
        assert "result_42" in res.blocks[0].text


@pytest.mark.asyncio
async def test_client_large_env_session_with_task_different_name(client: AsyncOpenReward, server: str):
    """Test that get_task -> session(task) works when server name differs from variant."""
    environment = client.environments.get("someserver", variant="largeenv", base_url=server)
    task = await environment.get_task("train", 42)
    async with environment.session(task=task) as session:
        res = await session.call_tool("submit")
        assert "result_42" in res.blocks[0].text


# Tests for task_tools endpoint

@pytest.mark.asyncio
async def test_session_list_tools_returns_task_tools(client: AsyncOpenReward, server: str):
    """Test that session.list_tools() returns task-specific tools from list_task_tools()."""
    environment = client.environments.get("envwithtasktools", variant="envwithtasktools", base_url=server)
    tasks = await environment.list_tasks(split="train")
    async with environment.session(tasks[0]) as session:
        tools = await session.list_tools()
        tool_names = [t.name for t in tools]
        assert "read_file" in tool_names
        assert "write_file" in tool_names
        # shared tool (submit) + 2 task-specific tools
        assert "submit" in tool_names
        assert len(tools) == 3


@pytest.mark.asyncio
async def test_env_list_tools_returns_shared_tools(client: AsyncOpenReward, server: str):
    """Test that environment.list_tools() returns shared tools (not task tools)."""
    environment = client.environments.get("envwithtasktools", variant="envwithtasktools", base_url=server)
    tools = await environment.list_tools()
    tool_names = [t.name for t in tools]
    # submit is a shared @tool, task tools (read_file, write_file) and non-shared tools should not appear
    assert "submit" in tool_names
    assert "read_file" not in tool_names
    assert "write_file" not in tool_names
    assert "non_shared_helper" not in tool_names
    assert len(tools) == 1


@pytest.mark.asyncio
async def test_client_large_env_session_with_split_index(client: AsyncOpenReward, server: str):
    """Test LargeEnv session created directly from split/index."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    async with environment.session(split="train", index=99) as session:
        res = await session.call_tool("submit")
        assert "result_99" in res.blocks[0].text


@pytest.mark.asyncio
async def test_client_large_env_concurrent_index_sessions(client: AsyncOpenReward, server: str):
    """Test multiple concurrent split/index sessions on LargeEnv."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    async with environment.session(split="train", index=0) as s1:
        async with environment.session(split="train", index=500) as s2:
            r1 = await s1.call_tool("submit")
            r2 = await s2.call_tool("submit")
            assert "result_0" in r1.blocks[0].text
            assert "result_500" in r2.blocks[0].text

# Tests for optional env_name (server defaults to first environment)

@pytest.mark.asyncio
async def test_create_session_defaults_env_name(server: str):
    """Test that omitting env_name defaults to the first registered environment (Foo)."""
    sid = str(__import__("uuid").uuid4())
    headers = {"X-Session-ID": sid}
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"split": "train", "index": 0},
            headers=headers,
        ) as resp:
            assert resp.status == 200

        # Foo is the first env, so prompt should come from {"foo": "bar"}
        async with http.get(
            f"{server}/foo/prompt",
            headers=headers,
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data[0]["text"] == "bar"

        async with http.post(f"{server}/delete", headers=headers) as resp:
            assert resp.status == 200


@pytest.mark.asyncio
async def test_create_session_rejects_no_task_source_without_env_name(server: str):
    """Test that omitting everything (no env_name, no task_spec, no split/index) is rejected."""
    sid = str(__import__("uuid").uuid4())
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={},
            headers={"X-Session-ID": sid},
        ) as resp:
            assert resp.status == 422


@pytest.mark.asyncio
async def test_create_session_without_env_name_with_split_index(server: str):
    """Test split/index without env_name — server defaults to first env and resolves task."""
    sid = str(__import__("uuid").uuid4())
    headers = {"X-Session-ID": sid}
    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"split": "train", "index": 0},
            headers=headers,
        ) as resp:
            assert resp.status == 200

        # Call submit on the default (Foo) environment
        async with http.post(
            f"{server}/foo/call",
            json={"name": "submit", "input": {}},
            headers=headers,
        ) as resp:
            assert resp.status == 200
            body = await resp.text()
            assert "foo_result" in body

        async with http.post(f"{server}/delete", headers=headers) as resp:
            assert resp.status == 200


# Tests for get_task_range server endpoint

@pytest.mark.asyncio
async def test_get_task_range_basic(server: str):
    """Test get_task_range returns tasks for a basic range."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "train", "start": 0, "stop": 3},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert len(data["tasks"]) == 3
            assert data["tasks"][0] == {"id": 0, "split": "train"}
            assert data["tasks"][2] == {"id": 2, "split": "train"}


@pytest.mark.asyncio
async def test_get_task_range_none_start(server: str):
    """Test get_task_range with None start defaults to 0."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "test", "stop": 2},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert len(data["tasks"]) == 2
            assert data["tasks"][0] == {"id": 0, "split": "test"}


@pytest.mark.asyncio
async def test_get_task_range_none_stop(server: str):
    """Test get_task_range with None stop defaults to num_tasks."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "test", "start": 198},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert len(data["tasks"]) == 2
            assert data["tasks"][0] == {"id": 198, "split": "test"}
            assert data["tasks"][1] == {"id": 199, "split": "test"}


@pytest.mark.asyncio
async def test_get_task_range_negative_start(server: str):
    """Test get_task_range with negative start (relative to end)."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "test", "start": -3},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert len(data["tasks"]) == 3
            assert data["tasks"][0] == {"id": 197, "split": "test"}
            assert data["tasks"][2] == {"id": 199, "split": "test"}


@pytest.mark.asyncio
async def test_get_task_range_negative_stop(server: str):
    """Test get_task_range with negative stop."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "test", "start": 0, "stop": -198},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert len(data["tasks"]) == 2
            assert data["tasks"][0] == {"id": 0, "split": "test"}
            assert data["tasks"][1] == {"id": 1, "split": "test"}


@pytest.mark.asyncio
async def test_get_task_range_empty(server: str):
    """Test get_task_range returns empty list when start >= stop."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "test", "start": 5, "stop": 5},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data["tasks"] == []


@pytest.mark.asyncio
async def test_get_task_range_invalid_split(server: str):
    """Test get_task_range rejects invalid split."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/largeenv/task_range",
            json={"split": "nonexistent", "start": 0, "stop": 1},
        ) as resp:
            assert resp.status == 400


@pytest.mark.asyncio
async def test_get_task_range_foo(server: str):
    """Test get_task_range on a small environment."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{server}/foo/task_range",
            json={"split": "train", "start": 0, "stop": 1},
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert len(data["tasks"]) == 1
            assert data["tasks"][0] == {"foo": "bar"}


# Tests for get_task_range via AsyncOpenReward client

@pytest.mark.asyncio
async def test_client_get_task_range_basic(client: AsyncOpenReward, server: str):
    """Test get_task_range via the client SDK."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    tasks = await environment.get_task_range("train", 0, 3)
    assert len(tasks) == 3
    assert tasks[0].task_spec == {"id": 0, "split": "train"}
    assert tasks[2].task_spec == {"id": 2, "split": "train"}


@pytest.mark.asyncio
async def test_client_get_task_range_defaults(client: AsyncOpenReward, server: str):
    """Test get_task_range with default start/stop via client."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    tasks = await environment.get_task_range("test")
    assert len(tasks) == 200


@pytest.mark.asyncio
async def test_client_get_task_range_negative(client: AsyncOpenReward, server: str):
    """Test get_task_range with negative indices via client."""
    environment = client.environments.get("largeenv", variant="largeenv", base_url=server)
    tasks = await environment.get_task_range("test", -2)
    assert len(tasks) == 2
    assert tasks[0].task_spec == {"id": 198, "split": "test"}
    assert tasks[1].task_spec == {"id": 199, "split": "test"}


@pytest.mark.asyncio
async def test_task_tools_does_not_wait_for_setup(server: str):
    """Regression: /task_tools must return immediately after /create, even
    while a slow setup() is still in flight."""
    import time
    import uuid
    sid = str(uuid.uuid4())
    headers = {"X-Session-ID": sid}

    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "slowsetupenv", "split": "train", "index": 0},
            headers=headers,
        ) as resp:
            assert resp.status == 200

        # setup() sleeps for 30s; /task_tools should return well before that.
        tools_start = time.monotonic()
        async with http.get(
            f"{server}/slowsetupenv/task_tools",
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=3),
        ) as resp:
            assert resp.status == 200
        tools_elapsed = time.monotonic() - tools_start
        assert tools_elapsed < 2.0, f"/task_tools took {tools_elapsed:.2f}s; expected < 2s"

        # /delete cancels the in-flight setup task.
        async with http.post(f"{server}/delete", headers=headers) as resp:
            assert resp.status == 200


@pytest.mark.asyncio
async def test_prompt_blocks_on_setup(server: str):
    """/prompt waits for setup() to finish before invoking get_prompt()."""
    import time
    import uuid
    sid = str(uuid.uuid4())
    headers = {"X-Session-ID": sid}

    async with aiohttp.ClientSession() as http:
        async with http.post(
            f"{server}/create",
            json={"env_name": "blockingpromptenv", "split": "train", "index": 0},
            headers=headers,
        ) as resp:
            assert resp.status == 200

        prompt_start = time.monotonic()
        async with http.get(
            f"{server}/blockingpromptenv/prompt",
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=_BLOCKING_PROMPT_SETUP_DELAY + 3),
        ) as resp:
            assert resp.status == 200
            data = await resp.json()
            assert data[0]["text"] == "prompt-after-setup"
        prompt_elapsed = time.monotonic() - prompt_start
        assert prompt_elapsed >= _BLOCKING_PROMPT_SETUP_DELAY * 0.8, (
            f"/prompt returned in {prompt_elapsed:.2f}s; expected to wait for setup "
            f"(~{_BLOCKING_PROMPT_SETUP_DELAY}s)"
        )

        async with http.post(f"{server}/delete", headers=headers) as resp:
            assert resp.status == 200


# ── Event-loop responsiveness under sync user code ──


@pytest.mark.asyncio
async def test_sync_list_tasks_does_not_block_loop(server: str):
    """A sync list_tasks that does blocking I/O must not freeze the loop —
    /health on a sibling env should answer while the slow call is in flight."""
    import time
    async with aiohttp.ClientSession() as http:
        slow = asyncio.create_task(
            http.post(
                f"{server}/blockinglisttasksenv/num_tasks",
                json={"split": "slow"},
                timeout=aiohttp.ClientTimeout(total=10),
            )
        )
        # Give the slow request a moment to land on the server.
        await asyncio.sleep(0.2)

        # Health should respond promptly even while the slow handler is
        # parked inside a sync user callback.
        health_start = time.monotonic()
        async with http.get(
            f"{server}/health",
            timeout=aiohttp.ClientTimeout(total=2),
        ) as health_resp:
            assert health_resp.status == 200
        health_elapsed = time.monotonic() - health_start
        assert health_elapsed < 0.5, (
            f"/health took {health_elapsed:.2f}s while a sync list_tasks "
            f"was in flight; expected < 0.5s"
        )

        slow_resp = await slow
        async with slow_resp:
            assert slow_resp.status == 200
            body = await slow_resp.json()
            assert body == {"num_tasks": 1}


@pytest.mark.asyncio
async def test_sync_tool_does_not_block_loop(server: str):
    """A sync @tool that blocks must not freeze the loop — /health and
    /prompt on a sibling session should answer concurrently."""
    import time
    import uuid

    tool_sid = str(uuid.uuid4())
    sibling_sid = str(uuid.uuid4())

    async with aiohttp.ClientSession() as http:
        # Spin up two sessions.
        async with http.post(
            f"{server}/create",
            json={"env_name": "blockingtoolenv", "split": "train", "index": 0},
            headers={"X-Session-ID": tool_sid},
        ) as resp:
            assert resp.status == 200
        async with http.post(
            f"{server}/create",
            json={"env_name": "foo", "split": "train", "index": 0},
            headers={"X-Session-ID": sibling_sid},
        ) as resp:
            assert resp.status == 200

        # Fire the slow tool call in the background.
        slow = asyncio.create_task(
            http.post(
                f"{server}/blockingtoolenv/call",
                json={"name": "slow", "input": {}},
                headers={"X-Session-ID": tool_sid},
                timeout=aiohttp.ClientTimeout(total=10),
            )
        )
        await asyncio.sleep(0.2)

        # Sibling session reads its prompt while the slow tool is mid-call.
        prompt_start = time.monotonic()
        async with http.get(
            f"{server}/foo/prompt",
            headers={"X-Session-ID": sibling_sid},
            timeout=aiohttp.ClientTimeout(total=2),
        ) as resp:
            assert resp.status == 200
        prompt_elapsed = time.monotonic() - prompt_start
        assert prompt_elapsed < 0.5, (
            f"/prompt on a sibling session took {prompt_elapsed:.2f}s while "
            f"a sync tool was in flight; expected < 0.5s"
        )

        slow_resp = await slow
        async with slow_resp:
            assert slow_resp.status == 200

        # Cleanup.
        async with http.post(
            f"{server}/delete",
            headers={"X-Session-ID": tool_sid},
        ) as resp:
            assert resp.status == 200
        async with http.post(
            f"{server}/delete",
            headers={"X-Session-ID": sibling_sid},
        ) as resp:
            assert resp.status == 200


@pytest.mark.asyncio
async def test_blocking_init_does_not_block_loop(server: str):
    """A slow env __init__ (run by /create) must not freeze the loop — /health
    should answer promptly while the constructor is parked in a thread."""
    import time
    import uuid

    create_sid = str(uuid.uuid4())
    async with aiohttp.ClientSession() as http:
        # Fire a /create whose constructor blocks for _BLOCKING_INIT_DELAY.
        slow = asyncio.create_task(
            http.post(
                f"{server}/create",
                json={"env_name": "blockinginitenv", "split": "train", "index": 0},
                headers={"X-Session-ID": create_sid},
                timeout=aiohttp.ClientTimeout(total=10),
            )
        )
        # Let the create request land and enter the constructor.
        await asyncio.sleep(0.2)

        # Health must respond promptly even while the constructor is in flight.
        health_start = time.monotonic()
        async with http.get(
            f"{server}/health",
            timeout=aiohttp.ClientTimeout(total=2),
        ) as health_resp:
            assert health_resp.status == 200
        health_elapsed = time.monotonic() - health_start
        assert health_elapsed < 0.5, (
            f"/health took {health_elapsed:.2f}s while a blocking env __init__ "
            f"was in flight; expected < 0.5s"
        )

        slow_resp = await slow
        async with slow_resp:
            assert slow_resp.status == 200

        # Cleanup.
        async with http.post(
            f"{server}/delete",
            headers={"X-Session-ID": create_sid},
        ) as resp:
            assert resp.status == 200


@pytest.mark.asyncio
async def test_call_user_helpers():
    """Unit-test call_user: async, sync, sync-returning-awaitable, contextvars."""
    import contextvars
    from openreward.environments.utils import run_user_callable

    async def async_fn(x):
        return x + 1

    def sync_fn(x):
        return x * 2

    async def coro(x):
        return x + 10

    def sync_returning_coro(x):
        return coro(x)

    assert await run_user_callable(async_fn, 2) == 3
    assert await run_user_callable(sync_fn, 5) == 10
    assert await run_user_callable(sync_returning_coro, 7) == 17

    # contextvars propagate into the thread.
    var: contextvars.ContextVar[str] = contextvars.ContextVar("test_var")
    var.set("ctx-value")

    def read_ctx():
        return var.get()

    assert await run_user_callable(read_ctx) == "ctx-value"


class _FakeJSONResponse:
    """Minimal async-context-manager response for the platform-API client."""

    def __init__(self, payload: dict, status: int = 200):
        self._payload = payload
        self.status = status
        self.ok = status < 400
        self.headers = {}
        self.request_info = None
        self.history = ()

    async def text(self) -> str:
        import json
        return json.dumps(self._payload)

    async def json(self) -> dict:
        return self._payload

    async def __aenter__(self) -> "_FakeJSONResponse":
        return self

    async def __aexit__(self, *exc) -> bool:
        return False


class _RecordingAPIClient:
    """Stands in for the platform-API aiohttp ClientSession; records GET calls."""

    def __init__(self, payload: dict):
        self._payload = payload
        self.calls: list[dict] = []

    def get(self, path, headers=None, params=None):
        self.calls.append({"path": path, "headers": headers or {}, "params": params or {}})
        return _FakeJSONResponse(self._payload)


def _make_env(api_client, *, namespace="thomas", name="arc-agi-1-harbor-test", variant=None, api_key="or_test_key"):
    from unittest.mock import MagicMock
    from openreward.api.environments.client import AsyncEnvironment
    return AsyncEnvironment(
        namespace=namespace,
        name=name,
        variant=variant,
        client=MagicMock(),  # env-server client; unused by get_task_difficulty
        api_key=api_key,
        api_client=api_client,
    )


@pytest.mark.asyncio
async def test_get_task_difficulty_request_and_parse():
    """Path, X-API-Key header, query-param building, and response parsing."""
    from openreward.api.environments.types import ResponseChars, TaskDifficulty

    rc0 = {"mean": 820.0, "p1": 100.0, "p10": 250.0, "p25": 400.0,
           "p50": 800.0, "p75": 1200.0, "p90": 1500.0, "p99": 1900.0}
    rc1 = {"mean": 300.0, "p1": 50.0, "p10": 120.0, "p25": 200.0,
           "p50": 300.0, "p75": 400.0, "p90": 480.0, "p99": 600.0}
    payload = {"tasks": [
        {"split": "test", "variant": None, "task_index": 0,
         "avg_reward": 0.5, "min_reward": 0.0, "max_reward": 1.0, "num_rollouts": 3,
         "response_chars": rc0},
        {"split": "test", "variant": None, "task_index": 1,
         "avg_reward": 1.0, "min_reward": 1.0, "max_reward": 1.0, "num_rollouts": 2,
         "response_chars": rc1},
    ]}
    api_client = _RecordingAPIClient(payload)
    env = _make_env(api_client)

    result = await env.get_task_difficulty(
        split="test", model_name="m", min_model_params=1_000,
        max_model_params=9_000, training_stage="rl",
    )

    assert len(api_client.calls) == 1
    call = api_client.calls[0]
    assert call["path"] == "/v1/environments/thomas/arc-agi-1-harbor-test/task-difficulty"
    assert call["headers"]["X-API-Key"] == "or_test_key"
    # No variant on an unscoped env; numeric filters are stringified for the query.
    assert call["params"] == {
        "split": "test",
        "model_name": "m",
        "min_model_params": "1000",
        "max_model_params": "9000",
        "training_stage": "rl",
    }

    assert result == [
        TaskDifficulty(task_index=0, avg_reward=0.5, min_reward=0.0, max_reward=1.0,
                       num_rollouts=3, response_chars=ResponseChars(**rc0),
                       split="test", variant=None),
        TaskDifficulty(task_index=1, avg_reward=1.0, min_reward=1.0, max_reward=1.0,
                       num_rollouts=2, response_chars=ResponseChars(**rc1),
                       split="test", variant=None),
    ]


@pytest.mark.asyncio
async def test_get_task_difficulty_scopes_to_variant():
    """A variant-scoped env filters by that variant without an explicit arg."""
    api_client = _RecordingAPIClient({"tasks": []})
    env = _make_env(api_client, variant="v1")

    await env.get_task_difficulty()

    assert api_client.calls[0]["params"] == {"variant": "v1"}


@pytest.mark.asyncio
async def test_get_task_difficulty_no_filters_no_params():
    """Unscoped env with no filters sends an empty query (all variants/splits)."""
    api_client = _RecordingAPIClient({"tasks": []})
    env = _make_env(api_client)

    await env.get_task_difficulty()

    assert api_client.calls[0]["params"] == {}


@pytest.mark.asyncio
async def test_get_task_difficulty_requires_api_client():
    """Without a platform-API base URL configured, raise a clear error."""
    env = _make_env(None)
    with pytest.raises(RuntimeError, match="API base URL not configured"):
        await env.get_task_difficulty()


@pytest.mark.asyncio
async def test_get_task_difficulty_requires_namespace():
    """A namespace-less env can't form an owner-keyed request — raise, don't
    silently build /v1/environments//task-difficulty."""
    api_client = _RecordingAPIClient({"tasks": []})
    env = _make_env(api_client, namespace=None)
    with pytest.raises(ValueError, match="has no namespace"):
        await env.get_task_difficulty()
    assert api_client.calls == []  # no request attempted
