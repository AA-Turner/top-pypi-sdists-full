from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import is_registered, register
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[bool, list[str], CommandResult | None]:
    show_all = False
    names: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            names.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if a == "-a" or a == "--all":
            show_all = True
            continue
        if a.startswith("-") and len(a) > 1 and not a.startswith("--"):
            ok_letters = True
            for ch in a[1:]:
                if ch == "a":
                    show_all = True
                else:
                    ok_letters = False
                    break
            if not ok_letters:
                return show_all, names, fail(
                    2,
                    encode(
                        f"which: illegal option -- {a[1]}\n"
                        "Usage: which [-a] args\n"
                    ),
                )
            continue
        if a.startswith("--"):
            return show_all, names, fail(
                2,
                encode(
                    f"which: illegal option -- {a}\nUsage: which [-a] args\n"
                ),
            )
        names.append(a)
    return show_all, names, None


@register("which")
async def cmd_which(ctx: CommandContext) -> CommandResult:
    _show_all, names, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not names:
        return ok()

    out = bytearray()
    not_found = 0
    for name in names:
        if is_registered(name):
            out.extend(encode(f"/usr/bin/{name}\n"))
        else:
            not_found += 1

    return CommandResult(stdout=bytes(out), stderr=b"", exit_code=1 if not_found else 0)
