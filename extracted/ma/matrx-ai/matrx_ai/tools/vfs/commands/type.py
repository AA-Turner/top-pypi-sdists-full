from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import is_registered, register
from matrx_ai.tools.vfs.shell.runner import CommandResult

# Shell builtins/keywords commonly recognized by `type` and `command -v` in bash.
SHELL_BUILTINS: frozenset[str] = frozenset(
    {
        "cd",
        "echo",
        "printf",
        "pwd",
        "type",
        "command",
        ":",
        "true",
        "false",
        "test",
        "[",
        "set",
        "unset",
        "export",
        "read",
        "eval",
        "exec",
        "exit",
        "return",
        "shift",
        "source",
        ".",
    }
)


class _TypeOpts:
    __slots__ = ("only_type", "only_path", "all_matches")

    def __init__(self) -> None:
        self.only_type = False
        self.only_path = False
        self.all_matches = False


def _parse_type_args(args: list[str]) -> tuple[_TypeOpts, list[str], CommandResult | None]:
    opts = _TypeOpts()
    names: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            names.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if a.startswith("-") and len(a) > 1 and not a.startswith("--"):
            for ch in a[1:]:
                if ch == "t":
                    opts.only_type = True
                elif ch == "p":
                    opts.only_path = True
                elif ch == "a":
                    opts.all_matches = True
                elif ch == "f" or ch == "P":
                    # ignore: search even functions / force PATH search
                    pass
                else:
                    return opts, names, fail(
                        2,
                        encode(
                            f"bash: type: -{ch}: invalid option\n"
                            "type: usage: type [-afptP] name [name ...]\n"
                        ),
                    )
            continue
        names.append(a)
    return opts, names, None


def _classify(name: str) -> tuple[str, str | None]:
    # Returns (kind, path_if_file_or_None).
    # kind is one of: "builtin", "file", "keyword" (we collapse keyword into builtin), or "missing".
    if name in SHELL_BUILTINS:
        return "builtin", None
    if is_registered(name):
        return "file", f"/usr/bin/{name}"
    return "missing", None


@register("type")
async def cmd_type(ctx: CommandContext) -> CommandResult:
    opts, names, err = _parse_type_args(ctx.args)
    if err is not None:
        return err

    if not names:
        return ok()

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    for name in names:
        kind, path = _classify(name)
        if kind == "missing":
            err_out.extend(encode(f"bash: type: {name}: not found\n"))
            exit_code = 1
            continue
        if opts.only_type:
            out.extend(encode(f"{kind}\n"))
            continue
        if opts.only_path:
            if kind == "file" and path is not None:
                out.extend(encode(f"{path}\n"))
            # builtins emit nothing for -p
            continue
        if kind == "builtin":
            out.extend(encode(f"{name} is a shell builtin\n"))
        elif kind == "file" and path is not None:
            out.extend(encode(f"{name} is {path}\n"))
            if opts.all_matches and name in SHELL_BUILTINS:
                out.extend(encode(f"{name} is a shell builtin\n"))

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)


@register("command")
async def cmd_command(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    only_v = False
    only_V = False
    rest: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            rest.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if a.startswith("-") and len(a) > 1 and not a.startswith("--"):
            for ch in a[1:]:
                if ch == "v":
                    only_v = True
                elif ch == "V":
                    only_V = True
                elif ch == "p":
                    pass
                else:
                    return fail(
                        2,
                        encode(
                            f"bash: command: -{ch}: invalid option\n"
                            "command: usage: command [-pVv] command [arg ...]\n"
                        ),
                    )
            continue
        rest.append(a)

    if not rest:
        return ok()

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    if only_v or only_V:
        for name in rest:
            kind, path = _classify(name)
            if kind == "missing":
                exit_code = 1
                continue
            if only_v:
                if kind == "builtin":
                    out.extend(encode(f"{name}\n"))
                elif path is not None:
                    out.extend(encode(f"{path}\n"))
            else:  # -V
                if kind == "builtin":
                    out.extend(encode(f"{name} is a shell builtin\n"))
                elif path is not None:
                    out.extend(encode(f"{name} is {path}\n"))
        return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)

    # Without -v/-V `command CMD ARGS` would actually invoke the command. We
    # don't dispatch from here — that's the runner's job. Emit nothing.
    return ok()
