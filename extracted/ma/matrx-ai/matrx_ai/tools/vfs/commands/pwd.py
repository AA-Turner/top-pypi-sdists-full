from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


@register("pwd")
async def cmd_pwd(ctx: CommandContext) -> CommandResult:
    # GNU `pwd` accepts -L (logical, default) and -P (physical). In the VFS,
    # cwd is maintained logically and there are no symlink-resolved variants of
    # the cwd path, so both flags emit the stored cwd.
    for arg in ctx.args:
        if arg in ("-L", "-P"):
            continue
        if arg == "--":
            break
        if arg.startswith("-") and arg != "-":
            return fail(
                2,
                encode(
                    f"pwd: invalid option -- '{arg.lstrip('-')[:1]}'\n"
                    "Try 'pwd --help' for more information.\n"
                ),
            )

    cwd = ctx.env.cwd
    if not await ctx.vfs._isdir(cwd):
        return fail(
            1,
            encode(
                "pwd: error retrieving current directory: "
                "getcwd: cannot access parent directories: "
                "No such file or directory\n"
            ),
        )
    return ok(encode(cwd + "\n"))
