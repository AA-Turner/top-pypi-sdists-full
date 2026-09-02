from __future__ import annotations

import re

from matrx_ai.tools.vfs.commands import registry
from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

_VALID_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _is_valid_identifier(name: str) -> bool:
    return _VALID_NAME.match(name) is not None


def _split_assign(tok: str) -> tuple[str, str] | None:
    if "=" not in tok:
        return None
    name, _, value = tok.partition("=")
    if not _is_valid_identifier(name):
        return None
    return name, value


@register("env")
async def cmd_env(ctx: CommandContext) -> CommandResult:
    args = list(ctx.args)
    clear_env = False
    unset_names: list[str] = []
    null_sep = False

    i = 0
    while i < len(args):
        a = args[i]
        if a == "-i" or a == "--ignore-environment":
            clear_env = True
            i += 1
            continue
        if a == "-0" or a == "--null":
            null_sep = True
            i += 1
            continue
        if a == "-u":
            if i + 1 >= len(args):
                return fail(
                    125,
                    encode("env: option requires an argument -- 'u'\n"),
                )
            unset_names.append(args[i + 1])
            i += 2
            continue
        if a.startswith("--unset="):
            unset_names.append(a[len("--unset=") :])
            i += 1
            continue
        if a == "--":
            i += 1
            break
        if a.startswith("-") and len(a) > 1 and not _split_assign(a):
            return fail(
                125,
                encode(f"env: invalid option -- '{a[1:]}'\n"),
            )
        break

    # Build the prospective new env (we will mutate ctx.env in place).
    if clear_env:
        ctx.env.vars.clear()
        ctx.env.exported.clear()

    for name in unset_names:
        ctx.env.unset(name)

    # Now process VAR=val assignments.
    while i < len(args):
        pair = _split_assign(args[i])
        if pair is None:
            break
        name, value = pair
        ctx.env.set(name, value, export=True)
        i += 1

    remaining = args[i:]

    if not remaining:
        sep = b"\0" if null_sep else b"\n"
        out = bytearray()
        for k, v in ctx.env.vars.items():
            out.extend(encode(f"{k}={v}"))
            out.extend(sep)
        return ok(bytes(out))

    cmd_name = remaining[0]
    cmd = registry.get(cmd_name)
    if cmd is None:
        return fail(
            127,
            encode(f"env: '{cmd_name}': No such file or directory\n"),
        )

    sub_ctx = CommandContext(
        argv=remaining,
        stdin=ctx.stdin,
        env=ctx.env,
        vfs=ctx.vfs,
        extra=ctx.extra,
    )
    return await cmd(sub_ctx)


@register("export")
async def cmd_export(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    if not args:
        names = sorted(ctx.env.exported)
        out = bytearray()
        for name in names:
            value = ctx.env.vars.get(name, "")
            out.extend(encode(f'declare -x {name}="{value}"\n'))
        return ok(bytes(out))

    err_out = bytearray()
    exit_code = 0

    for a in args:
        if "=" in a:
            name, _, value = a.partition("=")
            if not _is_valid_identifier(name):
                err_out.extend(encode(f"bash: export: '{a}': not a valid identifier\n"))
                exit_code = 1
                continue
            ctx.env.set(name, value, export=True)
        else:
            if not _is_valid_identifier(a):
                err_out.extend(encode(f"bash: export: '{a}': not a valid identifier\n"))
                exit_code = 1
                continue
            ctx.env.export(a)
            if a not in ctx.env.vars:
                ctx.env.vars[a] = ""

    return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)


@register("unset")
async def cmd_unset(ctx: CommandContext) -> CommandResult:
    args = list(ctx.args)
    if not args:
        return ok()

    mode = "v"
    i = 0
    if i < len(args) and args[i] in ("-v", "-f"):
        mode = args[i][1]
        i += 1

    err_out = bytearray()
    exit_code = 0

    while i < len(args):
        name = args[i]
        if not _is_valid_identifier(name):
            err_out.extend(encode(f"bash: unset: '{name}': not a valid identifier\n"))
            exit_code = 1
            i += 1
            continue
        if mode == "v":
            ctx.env.unset(name)
        # mode == "f": no functions in our model — silent success.
        i += 1

    return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)
