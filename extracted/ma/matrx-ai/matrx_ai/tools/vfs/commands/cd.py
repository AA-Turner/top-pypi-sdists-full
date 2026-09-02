from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import cd_no_dir, cd_not_dir
from matrx_ai.tools.vfs.paths import normalize
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _expand_tilde(path: str, home: str) -> str:
    if path == "~":
        return home
    if path.startswith("~/"):
        return home + path[1:]
    return path


@register("cd")
async def cmd_cd(ctx: CommandContext) -> CommandResult:
    args = [a for a in ctx.args if a != "--"]
    home = ctx.env.get("HOME", "/home/user")

    if not args:
        target = home
        echo = False
    elif args[0] == "-":
        oldpwd = ctx.env.get("OLDPWD")
        if not oldpwd:
            return fail(1, encode("bash: cd: OLDPWD not set\n"))
        target = oldpwd
        echo = True
    else:
        raw = _expand_tilde(args[0], home)
        target = raw if raw.startswith("/") else resolve_cwd(ctx.env, raw)
        target = normalize(target)
        echo = False

    target = normalize(target)

    exists = await ctx.vfs._exists(target)
    if not exists:
        return fail(1, encode(cd_no_dir(args[0] if args else target)))

    is_dir = await ctx.vfs._isdir(target)
    if not is_dir:
        return fail(1, encode(cd_not_dir(args[0] if args else target)))

    ctx.env.cd(target)

    if echo:
        return ok(encode(target + "\n"))
    return ok()
