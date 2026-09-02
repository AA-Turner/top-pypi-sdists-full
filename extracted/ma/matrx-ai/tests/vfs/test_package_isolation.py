from __future__ import annotations

import ast
import subprocess
from pathlib import Path

import pytest

VFS_ROOT = Path("/home/user/matrx-ai/matrx_ai/tools/vfs")


def test_no_external_matrx_imports_in_vfs_source() -> None:
    result = subprocess.run(
        [
            "grep",
            "-rn",
            "--include=*.py",
            "from matrx_ai",
            str(VFS_ROOT),
        ],
        capture_output=True,
        text=True,
    )
    offending = [
        line
        for line in result.stdout.splitlines()
        if "matrx_ai.tools.vfs" not in line
    ]
    assert not offending, (
        "Found matrx_ai imports inside vfs/ that aren't from vfs itself:\n"
        + "\n".join(offending)
        + "\n\nThese would break a copy-paste extraction. Either re-route through "
        "the public vfs API or move the coupling to the adapter layer."
    )


def test_ast_level_cleanliness() -> None:
    bad: list[str] = []
    for py in VFS_ROOT.rglob("*.py"):
        try:
            tree = ast.parse(py.read_text())
        except SyntaxError as e:
            pytest.fail(f"Syntax error parsing {py}: {e}")
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("matrx_ai."):
                    if not node.module.startswith("matrx_ai.tools.vfs"):
                        bad.append(f"{py.relative_to(VFS_ROOT)}: from {node.module}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("matrx_ai.") and not alias.name.startswith(
                        "matrx_ai.tools.vfs"
                    ):
                        bad.append(f"{py.relative_to(VFS_ROOT)}: import {alias.name}")
    assert not bad, (
        "AST scan found matrx_ai imports leaking out of vfs:\n" + "\n".join(bad)
    )


def test_external_dependency_set_is_minimal() -> None:
    allowed_third_party = {
        "fsspec",
        "wcmatch",
        "pathspec",
        "pydantic",
    }
    third_party: set[str] = set()
    for py in VFS_ROOT.rglob("*.py"):
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            mod_name: str | None = None
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.level and node.level > 0:
                    continue
                mod_name = node.module
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top not in {"matrx_ai"} and not _is_stdlib(top):
                        third_party.add(top)
                continue
            if mod_name:
                top = mod_name.split(".")[0]
                if top not in {"matrx_ai"} and not _is_stdlib(top):
                    third_party.add(top)

    unexpected = third_party - allowed_third_party
    assert not unexpected, (
        f"vfs/ depends on third-party packages outside the documented set "
        f"{sorted(allowed_third_party)}: {sorted(unexpected)}. "
        "Either add to the allowlist (and document in README) or remove the dep."
    )


def _is_stdlib(module: str) -> bool:
    import sys

    return module in sys.stdlib_module_names


def _reload_all_commands() -> None:
    import importlib
    import sys

    from matrx_ai.tools.vfs.commands.registry import is_registered

    if is_registered("cat"):
        return
    for mod_name in list(sys.modules):
        if mod_name.startswith("matrx_ai.tools.vfs.commands.") and mod_name not in (
            "matrx_ai.tools.vfs.commands.base",
            "matrx_ai.tools.vfs.commands.registry",
            "matrx_ai.tools.vfs.commands.runner",
        ):
            importlib.reload(sys.modules[mod_name])


@pytest.mark.asyncio
async def test_minimal_embedded_usage() -> None:
    from matrx_ai.tools.vfs import (
        MatrxAsyncFS,
        MemoryBackend,
        ShellEnv,
        VfsCommandRunner,
        execute,
        load_all,
        parse,
    )

    load_all()
    _reload_all_commands()

    backend = MemoryBackend()
    workspace_id = "embedded-test"
    await backend.ensure_workspace_root(workspace_id)
    fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)

    await fs._pipe_file("/hello.txt", b"Hello, World!\n")

    runner = VfsCommandRunner(fs)
    env = ShellEnv()
    node = parse("cat /hello.txt | tr a-z A-Z")
    result = await execute(node, env, runner, capture=True)

    assert result.exit_code == 0
    assert result.stdout == b"HELLO, WORLD!\n"


@pytest.mark.asyncio
async def test_workspace_protocol_satisfaction() -> None:
    from dataclasses import dataclass

    from matrx_ai.tools.vfs import WorkspaceContext, workspace_id_for

    @dataclass
    class FakeCtx:
        user_id: str | None
        conversation_id: str | None

    ctx = FakeCtx(user_id="alice", conversation_id="session-1")
    assert isinstance(ctx, WorkspaceContext)
    assert workspace_id_for(ctx) == "alice:session-1"

    from matrx_ai.tools.vfs import WorkspaceIdentityMissingError

    anon = FakeCtx(user_id=None, conversation_id=None)
    with pytest.raises(WorkspaceIdentityMissingError) as exc:
        workspace_id_for(anon)
    assert "WorkspaceContext.user_id" in str(exc.value)


@pytest.mark.asyncio
async def test_make_vfs_helper_is_self_contained() -> None:
    from matrx_ai.tools.vfs import clear_workspace_cache, make_vfs

    clear_workspace_cache()
    fs = await make_vfs("solo-workspace")
    await fs._pipe_file("/x.txt", b"hi")
    assert await fs._cat_file("/x.txt") == b"hi"
    clear_workspace_cache()
