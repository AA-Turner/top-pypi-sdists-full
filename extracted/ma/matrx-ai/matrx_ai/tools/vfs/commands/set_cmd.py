from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

# Mapping of -X short flags to their long option name in shell_opts.
_SHORT_TO_OPT: dict[str, str] = {
    "e": "errexit",
    "u": "nounset",
    "x": "xtrace",
    "f": "noglob",
}

# All recognized long option names (set -o NAME).
_LONG_OPTS: tuple[str, ...] = (
    "errexit",
    "nounset",
    "xtrace",
    "noglob",
    "pipefail",
    "nullglob",
    "globstar",
)


def _quote_single(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def _set_no_args(ctx: CommandContext) -> CommandResult:
    out = bytearray()
    for name in sorted(ctx.env.vars.keys()):
        out.extend(encode(f"{name}={_quote_single(ctx.env.vars[name])}\n"))
    return ok(bytes(out))


def _set_o_print(ctx: CommandContext) -> CommandResult:
    out = bytearray()
    for opt in _LONG_OPTS:
        state = "on" if ctx.env.shell_opts.get(opt, False) else "off"
        out.extend(encode(f"{opt}\t{state}\n"))
    return ok(bytes(out))


@register("set")
async def cmd_set(ctx: CommandContext) -> CommandResult:
    args = list(ctx.args)
    if not args:
        return _set_no_args(ctx)

    i = 0
    n = len(args)

    # Process flag tokens: -X / +X / -o NAME / +o NAME / -- / --
    while i < n:
        a = args[i]
        if a == "--":
            i += 1
            ctx.env.positional = list(args[i:])
            return ok()
        if a == "-":
            # `set -` clears -x and -v in bash; we treat as a no-op past flag parsing.
            i += 1
            continue
        if not (a.startswith("-") or a.startswith("+")) or len(a) < 2:
            # First non-option arg without `--` ⇒ treat remaining as positional.
            ctx.env.positional = list(args[i:])
            return ok()

        sign = a[0]
        body = a[1:]
        enable = sign == "-"

        if body == "o" or body == "+o":
            if i + 1 >= n:
                if enable:
                    return _set_o_print(ctx)
                # `+o` without arg also prints — match a stable form.
                return _set_o_print(ctx)
            name = args[i + 1]
            if name not in _LONG_OPTS:
                return fail(
                    2,
                    encode(f"bash: set: {name}: invalid option name\n"),
                )
            ctx.env.shell_opts[name] = enable
            i += 2
            continue

        # Cluster of short flags.
        for ch in body:
            if ch == "o":
                # Already handled above unless mixed: edge case—treat as start of -o.
                continue
            opt = _SHORT_TO_OPT.get(ch)
            if opt is None:
                return fail(
                    2,
                    encode(f"bash: set: -{ch}: invalid option\n"),
                )
            ctx.env.shell_opts[opt] = enable
        i += 1

    return ok()


@register("true")
async def cmd_true(ctx: CommandContext) -> CommandResult:
    return ok()


@register("false")
async def cmd_false(ctx: CommandContext) -> CommandResult:
    return fail(1)


@register(":")
async def cmd_colon(ctx: CommandContext) -> CommandResult:
    return ok()


# `exit` returns a result with the requested exit_code. The executor itself does
# not terminate — the surrounding shell driver is responsible for treating an
# `exit` builtin as a signal to stop interpreting further commands.
@register("exit")
async def cmd_exit(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    if not args:
        code = ctx.env.last_exit
    else:
        try:
            code = int(args[0])
        except ValueError:
            return fail(
                2,
                encode(f"bash: exit: {args[0]}: numeric argument required\n"),
            )
    # Mask to 0..255 like POSIX shells.
    code = code & 0xFF
    return CommandResult(stdout=b"", stderr=b"", exit_code=code, extra={"exit_shell": True})
