from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from .env import ShellEnv


@dataclass(slots=True)
class CommandResult:
    stdout: bytes = b""
    stderr: bytes = b""
    exit_code: int = 0
    extra: dict[str, object] = field(default_factory=dict)


@runtime_checkable
class CommandRunner(Protocol):
    async def run(
        self,
        argv: list[str],
        env: ShellEnv,
        stdin: bytes,
        cwd: str,
    ) -> CommandResult: ...

    async def glob(
        self,
        pattern: str,
        cwd: str,
        *,
        globstar: bool = True,
        nullglob: bool = False,
    ) -> list[str]: ...

    async def is_executable(self, name: str) -> bool: ...

    async def read_file(self, path: str, env: ShellEnv) -> bytes: ...

    async def write_file(
        self,
        path: str,
        data: bytes,
        env: ShellEnv,
        *,
        append: bool = False,
    ) -> None: ...
