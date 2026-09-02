from __future__ import annotations

import asyncio
from collections.abc import Iterator
from uuid import uuid4

import pytest

from matrx_ai.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
)
from matrx_connect.emitters.console_emitter import ConsoleEmitter
from matrx_ai.tools.implementations.vfs_filesystem import (
    fs_edit,
    fs_list,
    fs_mkdir,
    fs_read,
    fs_search,
    fs_write,
)
from matrx_ai.tools.implementations.vfs_shell import shell_execute
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.vfs.commands import CommandContext, load_all, ok, register
from matrx_ai.tools.vfs.commands.registry import is_registered
from matrx_ai.tools.vfs.shell.runner import CommandResult
from matrx_ai.tools.vfs.workspace import clear_workspace_cache


def _ensure_commands_loaded() -> None:
    # Other test modules (e.g. tests/vfs/test_command_base.py) clear() the
    # global command registry. The @register decorators only run on first
    # import, so a plain load_all() after clear() is a no-op. Force-reload the
    # command modules to re-execute their top-level @register decorators.
    import importlib
    import sys

    load_all()
    if not is_registered("echo"):
        for mod_name in list(sys.modules):
            if mod_name.startswith("matrx_ai.tools.vfs.commands.") and mod_name not in (
                "matrx_ai.tools.vfs.commands.base",
                "matrx_ai.tools.vfs.commands.registry",
                "matrx_ai.tools.vfs.commands.runner",
            ):
                importlib.reload(sys.modules[mod_name])

    if not is_registered("sleep"):

        @register("sleep")
        async def _sleep(ctx: CommandContext) -> CommandResult:
            try:
                seconds = float(ctx.args[0]) if ctx.args else 0.0
            except ValueError:
                return CommandResult(stderr=b"sleep: invalid time interval\n", exit_code=1)
            await asyncio.sleep(seconds)
            return ok()


def _make_app_context(user_id: str) -> AppContext:
    return AppContext(
        emitter=ConsoleEmitter(label="vfs-adapter-test"),
        user_id=user_id,
        email=None,
        auth_type="anonymous",
        is_authenticated=True,
        request_id=str(uuid4()),
        conversation_id=str(uuid4()),
    )


@pytest.fixture(autouse=True)
def fresh_workspace() -> Iterator[None]:
    clear_workspace_cache()
    _ensure_commands_loaded()
    yield
    clear_workspace_cache()


@pytest.fixture
def app_ctx_token() -> Iterator[None]:
    token = set_app_context(_make_app_context(user_id=f"user-{uuid4().hex[:8]}"))
    try:
        yield
    finally:
        clear_app_context(token)


@pytest.fixture
def ctx(app_ctx_token: None) -> ToolContext:
    _ = app_ctx_token
    return ToolContext(call_id=f"call-{uuid4().hex[:8]}", tool_name="fs", iteration=0)


# ---------------------------------------------------------------------------
# fs_read / fs_write
# ---------------------------------------------------------------------------


async def test_fs_write_then_read_roundtrip(ctx: ToolContext) -> None:
    write_result = await fs_write({"path": "hello.txt", "content": "hi"}, ctx)
    assert write_result.success is True
    assert write_result.output["bytes_written"] == 2
    assert write_result.output["mode"] == "write"

    read_result = await fs_read({"path": "hello.txt"}, ctx)
    assert read_result.success is True
    assert read_result.output["content"] == "hi"
    assert read_result.output["size"] == 2
    assert read_result.output["truncated"] is False


async def test_fs_read_missing_file(ctx: ToolContext) -> None:
    result = await fs_read({"path": "ghost.txt"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "not_found"
    assert "ghost.txt" in result.error.message


async def test_fs_read_directory_returns_filesystem_error(ctx: ToolContext) -> None:
    await fs_mkdir({"path": "adir"}, ctx)
    result = await fs_read({"path": "adir"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "filesystem"


async def test_fs_write_creates_parent_dirs(ctx: ToolContext) -> None:
    result = await fs_write(
        {"path": "deep/nested/dir/file.txt", "content": "x", "create_dirs": True}, ctx
    )
    assert result.success is True

    read_result = await fs_read({"path": "deep/nested/dir/file.txt"}, ctx)
    assert read_result.success is True
    assert read_result.output["content"] == "x"


async def test_fs_write_append(ctx: ToolContext) -> None:
    await fs_write({"path": "log.txt", "content": "one\n"}, ctx)
    append_result = await fs_write({"path": "log.txt", "content": "two\n", "append": True}, ctx)
    assert append_result.success is True
    assert append_result.output["mode"] == "append"

    read_result = await fs_read({"path": "log.txt"}, ctx)
    assert read_result.success is True
    assert read_result.output["content"] == "one\ntwo\n"


# ---------------------------------------------------------------------------
# fs_list
# ---------------------------------------------------------------------------


async def test_fs_list_pattern_filter(ctx: ToolContext) -> None:
    await fs_write({"path": "a.py", "content": "x"}, ctx)
    await fs_write({"path": "b.py", "content": "x"}, ctx)
    await fs_write({"path": "c.txt", "content": "x"}, ctx)

    result = await fs_list({"path": "/", "pattern": "*.py"}, ctx)
    assert result.success is True
    names = sorted(e["name"] for e in result.output["entries"])
    assert names == ["a.py", "b.py"]


async def test_fs_list_recursive(ctx: ToolContext) -> None:
    await fs_write({"path": "top.txt", "content": "x"}, ctx)
    await fs_write({"path": "sub/a.txt", "content": "y"}, ctx)
    await fs_write({"path": "sub/inner/b.txt", "content": "z"}, ctx)

    result = await fs_list({"path": "/", "recursive": True}, ctx)
    assert result.success is True
    names = {e["name"] for e in result.output["entries"]}
    assert {"top.txt", "a.txt", "b.txt"}.issubset(names)


async def test_fs_list_missing_directory(ctx: ToolContext) -> None:
    result = await fs_list({"path": "/no-such-dir"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "not_found"


# ---------------------------------------------------------------------------
# fs_search
# ---------------------------------------------------------------------------


async def test_fs_search_by_name(ctx: ToolContext) -> None:
    await fs_write({"path": "foo.py", "content": "x"}, ctx)
    await fs_write({"path": "sub/bar.py", "content": "y"}, ctx)
    await fs_write({"path": "sub/baz.txt", "content": "z"}, ctx)

    result = await fs_search({"pattern": "*.py", "path": "/"}, ctx)
    assert result.success is True
    paths = {r["path"] for r in result.output["results"]}
    assert "foo.py" in paths
    assert "sub/bar.py" in paths
    assert all(p.endswith(".py") for p in paths)


async def test_fs_search_by_content(ctx: ToolContext) -> None:
    await fs_write({"path": "a.txt", "content": "needle in haystack"}, ctx)
    await fs_write({"path": "b.txt", "content": "no match here"}, ctx)
    await fs_write({"path": "c.txt", "content": "another needle here"}, ctx)

    result = await fs_search({"pattern": "needle", "path": "/", "content_search": True}, ctx)
    assert result.success is True
    paths = {r["path"] for r in result.output["results"]}
    assert paths == {"a.txt", "c.txt"}


# ---------------------------------------------------------------------------
# fs_mkdir
# ---------------------------------------------------------------------------


async def test_fs_mkdir_with_parents(ctx: ToolContext) -> None:
    result = await fs_mkdir({"path": "x/y/z", "parents": True}, ctx)
    assert result.success is True

    list_result = await fs_list({"path": "x/y"}, ctx)
    assert list_result.success is True
    names = [e["name"] for e in list_result.output["entries"]]
    assert "z" in names


async def test_fs_mkdir_no_parents_missing_parent(ctx: ToolContext) -> None:
    result = await fs_mkdir({"path": "missing/inner", "parents": False}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "not_found"


async def test_fs_mkdir_existing_without_parents(ctx: ToolContext) -> None:
    await fs_mkdir({"path": "exists", "parents": False}, ctx)
    result = await fs_mkdir({"path": "exists", "parents": False}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "filesystem"


# ---------------------------------------------------------------------------
# fs_edit
# ---------------------------------------------------------------------------


async def test_fs_edit_single_match(ctx: ToolContext) -> None:
    await fs_write({"path": "doc.txt", "content": "hello world"}, ctx)
    result = await fs_edit({"path": "doc.txt", "old_str": "world", "new_str": "there"}, ctx)
    assert result.success is True
    assert result.output["old_str_count"] == 1
    assert result.output["replaced"] == 1

    read_result = await fs_read({"path": "doc.txt"}, ctx)
    assert read_result.output["content"] == "hello there"


async def test_fs_edit_no_match(ctx: ToolContext) -> None:
    await fs_write({"path": "doc.txt", "content": "hello"}, ctx)
    result = await fs_edit({"path": "doc.txt", "old_str": "nope", "new_str": "x"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert "String to replace not found in file." in result.error.message


async def test_fs_edit_multi_match_without_replace_all(ctx: ToolContext) -> None:
    await fs_write({"path": "doc.txt", "content": "ab ab ab"}, ctx)
    result = await fs_edit({"path": "doc.txt", "old_str": "ab", "new_str": "x"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert "Found 3 matches" in result.error.message


async def test_fs_edit_multi_match_with_replace_all(ctx: ToolContext) -> None:
    await fs_write({"path": "doc.txt", "content": "ab ab ab"}, ctx)
    result = await fs_edit(
        {
            "path": "doc.txt",
            "old_str": "ab",
            "new_str": "x",
            "replace_all": True,
        },
        ctx,
    )
    assert result.success is True
    assert result.output["old_str_count"] == 3
    assert result.output["replaced"] == 3

    read_result = await fs_read({"path": "doc.txt"}, ctx)
    assert read_result.output["content"] == "x x x"


async def test_fs_edit_missing_file(ctx: ToolContext) -> None:
    result = await fs_edit({"path": "ghost.txt", "old_str": "a", "new_str": "b"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "not_found"


# ---------------------------------------------------------------------------
# shell_execute
# ---------------------------------------------------------------------------


async def test_shell_execute_echo(ctx: ToolContext) -> None:
    result = await shell_execute({"command": "echo hi"}, ctx)
    assert result.success is True
    assert result.output["stdout"] == "hi\n"
    assert result.output["exit_code"] == 0


async def test_shell_execute_ls_root(ctx: ToolContext) -> None:
    await fs_write({"path": "a.txt", "content": "x"}, ctx)
    await fs_write({"path": "b.txt", "content": "y"}, ctx)

    result = await shell_execute({"command": "ls /"}, ctx)
    assert result.success is True
    assert "a.txt" in result.output["stdout"]
    assert "b.txt" in result.output["stdout"]


async def test_shell_execute_false_returns_exit_code_error(ctx: ToolContext) -> None:
    result = await shell_execute({"command": "false"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "exit_code"
    assert result.output["exit_code"] == 1


async def test_shell_execute_timeout(ctx: ToolContext) -> None:
    result = await shell_execute({"command": "sleep 5", "timeout_seconds": 1}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "timeout"
    assert result.error.is_retryable is True


async def test_shell_execute_syntax_error(ctx: ToolContext) -> None:
    result = await shell_execute({"command": "echo 'unterminated"}, ctx)
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "validation"
    assert "syntax error" in result.error.message


async def test_shell_execute_missing_command(ctx: ToolContext) -> None:
    result = await shell_execute({"command": "missing-cmd"}, ctx)
    assert result.success is False
    assert result.output["exit_code"] == 127
    assert "command not found" in result.output["stderr"]
    assert result.error is not None
    assert result.error.error_type == "exit_code"


# ---------------------------------------------------------------------------
# Workspace isolation
# ---------------------------------------------------------------------------


async def test_workspace_isolation_between_users() -> None:
    user_a = f"user-a-{uuid4().hex[:8]}"
    user_b = f"user-b-{uuid4().hex[:8]}"
    call_id_a = f"call-{uuid4().hex[:8]}"
    call_id_b = f"call-{uuid4().hex[:8]}"

    token_a = set_app_context(_make_app_context(user_id=user_a))
    try:
        ctx_a = ToolContext(call_id=call_id_a, tool_name="fs", iteration=0)
        await fs_write({"path": "shared.txt", "content": "from-a"}, ctx_a)
    finally:
        clear_app_context(token_a)

    token_b = set_app_context(_make_app_context(user_id=user_b))
    try:
        ctx_b = ToolContext(call_id=call_id_b, tool_name="fs", iteration=0)
        # User B sees their own empty workspace — same path, no clash
        read_b = await fs_read({"path": "shared.txt"}, ctx_b)
        assert read_b.success is False
        assert read_b.error is not None
        assert read_b.error.error_type == "not_found"

        await fs_write({"path": "shared.txt", "content": "from-b"}, ctx_b)
        own = await fs_read({"path": "shared.txt"}, ctx_b)
        assert own.success is True
        assert own.output["content"] == "from-b"
    finally:
        clear_app_context(token_b)

    token_a2 = set_app_context(_make_app_context(user_id=user_a))
    try:
        ctx_a2 = ToolContext(call_id=f"call-{uuid4().hex[:8]}", tool_name="fs", iteration=0)
        # New conversation_id ⇒ new workspace, even for the same user.
        # We confirm that user A's previous workspace stays untouched by user B
        # by re-running with the same conversation_id used in the first set.
        # A simpler assertion: the new conv lane is independent from B's lane.
        read_isolated = await fs_read({"path": "shared.txt"}, ctx_a2)
        assert read_isolated.success is False
    finally:
        clear_app_context(token_a2)
