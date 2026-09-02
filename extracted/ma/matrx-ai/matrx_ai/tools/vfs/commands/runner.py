from __future__ import annotations

from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.commands import registry
from matrx_ai.tools.vfs.commands.base import CommandContext
from matrx_ai.tools.vfs.mimicry.coreutils_errors import cmd_not_found
from matrx_ai.tools.vfs.paths import join, normalize
from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS
    from matrx_ai.tools.vfs.shell.env import ShellEnv


class VfsCommandRunner:
    def __init__(self, vfs: MatrxAsyncFS) -> None:
        self.vfs = vfs

    async def run(
        self,
        argv: list[str],
        env: ShellEnv,
        stdin: bytes,
        cwd: str,
    ) -> CommandResult:
        if not argv:
            return CommandResult(exit_code=0)

        name = argv[0]
        cmd = registry.get(name)
        if cmd is None:
            return CommandResult(stderr=cmd_not_found(name).encode(), exit_code=127)

        env.cd(cwd) if cwd != env.cwd else None
        ctx = CommandContext(argv=argv, stdin=stdin, env=env, vfs=self.vfs)
        return await cmd(ctx)

    async def glob(
        self,
        pattern: str,
        cwd: str,
        *,
        globstar: bool = True,
        nullglob: bool = False,
    ) -> list[str]:
        if not pattern.startswith("/"):
            pattern = normalize(join(cwd, pattern))
        try:
            matches = await self.vfs._glob(pattern)
        except Exception:
            matches = []
        if not matches and not nullglob:
            return [pattern]
        return sorted(matches)

    async def is_executable(self, name: str) -> bool:
        return registry.is_registered(name)

    async def read_file(self, path: str, env: ShellEnv) -> bytes:
        resolved = path if path.startswith("/") else normalize(join(env.cwd, path))
        return await self.vfs._cat_file(resolved)

    async def write_file(
        self,
        path: str,
        data: bytes,
        env: ShellEnv,
        *,
        append: bool = False,
    ) -> None:
        resolved = path if path.startswith("/") else normalize(join(env.cwd, path))
        if append:
            try:
                existing = await self.vfs._cat_file(resolved)
            except FileNotFoundError:
                existing = b""
            data = existing + data
        await self.vfs._pipe_file(resolved, data)
