from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS
    from matrx_ai.tools.vfs.shell.env import ShellEnv


@dataclass(slots=True)
class CommandContext:
    argv: list[str]
    stdin: bytes
    env: ShellEnv
    vfs: MatrxAsyncFS
    extra: dict[str, object] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.argv[0] if self.argv else ""

    @property
    def args(self) -> list[str]:
        return self.argv[1:] if len(self.argv) > 1 else []


class Command(Protocol):
    async def __call__(self, ctx: CommandContext) -> CommandResult: ...


def ok(stdout: bytes = b"", stderr: bytes = b"") -> CommandResult:
    return CommandResult(stdout=stdout, stderr=stderr, exit_code=0)


def fail(exit_code: int, stderr: bytes = b"", stdout: bytes = b"") -> CommandResult:
    return CommandResult(stdout=stdout, stderr=stderr, exit_code=exit_code)


def encode(value: str | bytes) -> bytes:
    return value.encode("utf-8", errors="surrogateescape") if isinstance(value, str) else value


def resolve_cwd(env: ShellEnv, path: str) -> str:
    from matrx_ai.tools.vfs.paths import join, normalize

    if path.startswith("/"):
        return normalize(path)
    return normalize(join(env.cwd, path))
