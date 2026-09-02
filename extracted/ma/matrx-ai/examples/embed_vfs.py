"""Standalone embedding example for the matrx-ai virtual filesystem.

Demonstrates using the VFS package without any other matrx-ai code: build a
workspace, run shell commands, and observe byte-exact GNU coreutils output.

Run with:
    uv run python examples/embed_vfs.py
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from matrx_ai.tools.vfs import (
    MatrxAsyncFS,
    MemoryBackend,
    ShellEnv,
    VfsCommandRunner,
    execute,
    load_all,
    make_vfs,
    parse,
)


@dataclass
class MyContext:
    user_id: str | None = "demo-user"
    conversation_id: str | None = "demo-session"


async def run_one(runner: VfsCommandRunner, env: ShellEnv, command: str) -> None:
    print(f"\n$ {command}")
    node = parse(command)
    result = await execute(node, env, runner, capture=True)
    if result.stdout:
        print(result.stdout.decode("utf-8", errors="replace"), end="")
    if result.stderr:
        print(f"[stderr] {result.stderr.decode('utf-8', errors='replace')}", end="")
    if result.exit_code != 0:
        print(f"[exit={result.exit_code}]")


async def main() -> None:
    load_all()

    fs = await make_vfs("demo-user:demo-session")

    await fs._pipe_file("/hello.txt", b"Hello, World!\n")
    await fs._pipe_file(
        "/notes.md",
        b"# Project notes\n- TODO: write tests\n- TODO: deploy\n- DONE: design\n",
    )
    await fs._makedirs("/src/components", exist_ok=True)
    await fs._pipe_file("/src/main.py", b"def main():\n    print('hi')\n")
    await fs._pipe_file(
        "/src/components/button.py",
        b"def render():\n    return '<button>'\n",
    )

    runner = VfsCommandRunner(fs)
    env = ShellEnv()
    env.cd("/")

    await run_one(runner, env, "ls -la")
    await run_one(runner, env, "cat /hello.txt | tr a-z A-Z")
    await run_one(runner, env, "grep -rn TODO /notes.md")
    await run_one(runner, env, "find /src -name '*.py'")
    await run_one(runner, env, "wc -l /src/main.py /src/components/button.py")
    await run_one(runner, env, "echo 'inserted line' >> /hello.txt && cat /hello.txt")
    await run_one(runner, env, "cat /no/such/file")
    await run_one(runner, env, "rm /sub")


if __name__ == "__main__":
    asyncio.run(main())
