from __future__ import annotations

import pytest

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.commands import (
    CommandContext,
    VfsCommandRunner,
    all_names,
    clear,
    fail,
    get,
    is_registered,
    ok,
    register,
)
from matrx_ai.tools.vfs.core import MatrxAsyncFS
from matrx_ai.tools.vfs.shell.env import ShellEnv


@pytest.fixture
def fresh_registry():
    clear()
    yield
    clear()


@pytest.fixture
async def vfs():
    backend = MemoryBackend()
    workspace_id = "ws-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
    await fs._mkdir("/tmp", create_parents=False)
    return fs


def test_register_and_get(fresh_registry):
    @register("foo")
    async def foo_cmd(ctx: CommandContext):
        return ok(b"hello")

    assert is_registered("foo")
    assert get("foo") is foo_cmd
    assert "foo" in all_names()


def test_register_aliases(fresh_registry):
    @register("a", "b", "c")
    async def alias_cmd(ctx: CommandContext):
        return ok()

    assert is_registered("a")
    assert is_registered("b")
    assert is_registered("c")


@pytest.mark.asyncio
async def test_runner_dispatches_to_registered(fresh_registry, vfs):
    @register("greet")
    async def greet_cmd(ctx: CommandContext):
        return ok(f"hello {ctx.args[0] if ctx.args else 'world'}".encode())

    runner = VfsCommandRunner(vfs)
    env = ShellEnv()
    result = await runner.run(["greet", "matrx"], env, b"", env.cwd)
    assert result.exit_code == 0
    assert result.stdout == b"hello matrx"


@pytest.mark.asyncio
async def test_runner_command_not_found(fresh_registry, vfs):
    runner = VfsCommandRunner(vfs)
    env = ShellEnv()
    result = await runner.run(["nonexistent"], env, b"", env.cwd)
    assert result.exit_code == 127
    assert result.stderr == b"bash: nonexistent: command not found\n"


@pytest.mark.asyncio
async def test_runner_is_executable(fresh_registry, vfs):
    @register("real")
    async def real_cmd(ctx: CommandContext):
        return ok()

    runner = VfsCommandRunner(vfs)
    assert await runner.is_executable("real")
    assert not await runner.is_executable("ghost")


@pytest.mark.asyncio
async def test_runner_read_write_roundtrip(vfs):
    runner = VfsCommandRunner(vfs)
    env = ShellEnv()
    await runner.write_file("/tmp/x.txt", b"payload", env)
    assert await runner.read_file("/tmp/x.txt", env) == b"payload"


@pytest.mark.asyncio
async def test_runner_write_append(vfs):
    runner = VfsCommandRunner(vfs)
    env = ShellEnv()
    await runner.write_file("/tmp/log", b"line1\n", env)
    await runner.write_file("/tmp/log", b"line2\n", env, append=True)
    assert await runner.read_file("/tmp/log", env) == b"line1\nline2\n"


def test_helpers():
    r = ok(b"hi")
    assert r.exit_code == 0 and r.stdout == b"hi"
    f = fail(2, b"bad")
    assert f.exit_code == 2 and f.stderr == b"bad"
