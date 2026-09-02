from __future__ import annotations

from dataclasses import dataclass, field

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail
from matrx_ai.tools.vfs.commands.registry import get as get_command
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


@dataclass(slots=True)
class _Opts:
    null_separator: bool = False
    no_run_if_empty: bool = False
    trace: bool = False
    replace_str: str | None = None
    max_args: int | None = None
    parallel: int | None = None
    cmd_argv: list[str] = field(default_factory=list)


def _bad(msg: str) -> bytes:
    return encode(f"xargs: {msg}\n")


def _parse_args(args: list[str]) -> tuple[_Opts, CommandResult | None]:
    opts = _Opts()
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            opts.cmd_argv.extend(args[i + 1 :])
            break
        if a.startswith("--"):
            name, has_eq, value = a[2:].partition("=")
            if name == "null":
                opts.null_separator = True
                i += 1
                continue
            if name == "no-run-if-empty":
                opts.no_run_if_empty = True
                i += 1
                continue
            if name == "verbose":
                opts.trace = True
                i += 1
                continue
            if name == "replace":
                opts.replace_str = value if has_eq else "{}"
                i += 1
                continue
            if name == "max-args":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad("option requires an argument"))
                    i += 1
                    value = args[i]
                if not value.isdigit():
                    return opts, fail(1, _bad(f"invalid number for --max-args: '{value}'"))
                opts.max_args = int(value)
                i += 1
                continue
            if name == "max-procs":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad("option requires an argument"))
                    i += 1
                    value = args[i]
                if not value.isdigit():
                    return opts, fail(1, _bad(f"invalid number for --max-procs: '{value}'"))
                opts.parallel = int(value)
                i += 1
                continue
            return opts, fail(1, _bad(f"unrecognized option '--{name}'"))
        if a.startswith("-") and len(a) > 1:
            j = 1
            consumed = False
            while j < len(a):
                letter = a[j]
                if letter == "0":
                    opts.null_separator = True
                    j += 1
                elif letter == "r":
                    opts.no_run_if_empty = True
                    j += 1
                elif letter == "t":
                    opts.trace = True
                    j += 1
                elif letter == "I":
                    inline = a[j + 1 :]
                    if inline:
                        opts.replace_str = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(1, _bad("option requires an argument -- 'I'"))
                        i += 1
                        opts.replace_str = args[i]
                        consumed = True
                        j = len(a)
                elif letter == "n":
                    inline = a[j + 1 :]
                    if inline:
                        v = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(1, _bad("option requires an argument -- 'n'"))
                        i += 1
                        v = args[i]
                        consumed = True
                        j = len(a)
                    if not v.isdigit():
                        return opts, fail(1, _bad(f"invalid number for -n: '{v}'"))
                    opts.max_args = int(v)
                elif letter == "P":
                    inline = a[j + 1 :]
                    if inline:
                        v = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(1, _bad("option requires an argument -- 'P'"))
                        i += 1
                        v = args[i]
                        consumed = True
                        j = len(a)
                    if not v.isdigit():
                        return opts, fail(1, _bad(f"invalid number for -P: '{v}'"))
                    opts.parallel = int(v)
                else:
                    return opts, fail(1, _bad(f"invalid option -- '{letter}'"))
            i += 1
            _ = consumed
            continue
        # First positional: this and the rest are CMD ARGS...
        opts.cmd_argv.extend(args[i:])
        break
    return opts, None


def _split_input(data: bytes, null: bool) -> list[str]:
    if not data:
        return []
    text = data.decode("latin-1")
    if null:
        parts = text.split("\x00")
        return [p for p in parts if p]
    # default: split on whitespace runs and newlines
    return text.split()


def _split_lines(data: bytes, null: bool) -> list[str]:
    if not data:
        return []
    text = data.decode("latin-1")
    if null:
        parts = text.split("\x00")
        return [p for p in parts if p]
    # By line.
    return [ln for ln in text.split("\n") if ln != ""]


def _trace_line(argv: list[str]) -> bytes:
    return encode(" ".join(argv) + "\n")


@register("xargs")
async def cmd_xargs(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not opts.cmd_argv:
        opts.cmd_argv = ["echo"]

    cmd_name = opts.cmd_argv[0]
    base_args = opts.cmd_argv[1:]

    cmd_fn = get_command(cmd_name)
    if cmd_fn is None:
        return fail(127, encode(f"xargs: {cmd_name}: command not found\n"))

    out = bytearray()
    err_out = bytearray()
    worst_exit = 0

    def _track_exit(code: int) -> None:
        nonlocal worst_exit
        if code == 0:
            return
        if 1 <= code <= 125:
            worst_exit = max(worst_exit, 123)
        elif code == 126:
            worst_exit = max(worst_exit, 126)
        elif code == 127:
            worst_exit = max(worst_exit, 127)
        else:
            worst_exit = max(worst_exit, code)

    if opts.replace_str is not None:
        # One invocation per line of input.
        lines = _split_lines(ctx.stdin, opts.null_separator)
        if not lines:
            if opts.no_run_if_empty:
                return CommandResult(stdout=b"", stderr=b"", exit_code=0)
            # GNU xargs -I never runs on empty input.
            return CommandResult(stdout=b"", stderr=b"", exit_code=0)
        for line in lines:
            new_args = [a.replace(opts.replace_str, line) for a in base_args]
            argv = [cmd_name] + new_args
            if opts.trace:
                err_out.extend(_trace_line(argv))
            sub_ctx = CommandContext(argv=argv, stdin=b"", env=ctx.env, vfs=ctx.vfs)
            res = await cmd_fn(sub_ctx)
            out.extend(res.stdout)
            err_out.extend(res.stderr)
            _track_exit(res.exit_code)
        return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=worst_exit)

    # Word-mode.
    words = _split_input(ctx.stdin, opts.null_separator)
    if not words:
        if opts.no_run_if_empty:
            return CommandResult(stdout=b"", stderr=b"", exit_code=0)
        # Default GNU: still run once with no extra args.
        argv = [cmd_name] + base_args
        if opts.trace:
            err_out.extend(_trace_line(argv))
        sub_ctx = CommandContext(argv=argv, stdin=b"", env=ctx.env, vfs=ctx.vfs)
        res = await cmd_fn(sub_ctx)
        out.extend(res.stdout)
        err_out.extend(res.stderr)
        _track_exit(res.exit_code)
        return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=worst_exit)

    if opts.max_args is not None and opts.max_args > 0:
        batches: list[list[str]] = []
        for k in range(0, len(words), opts.max_args):
            batches.append(words[k : k + opts.max_args])
    else:
        batches = [words]

    for batch in batches:
        argv = [cmd_name] + base_args + batch
        if opts.trace:
            err_out.extend(_trace_line(argv))
        sub_ctx = CommandContext(argv=argv, stdin=b"", env=ctx.env, vfs=ctx.vfs)
        res = await cmd_fn(sub_ctx)
        out.extend(res.stdout)
        err_out.extend(res.stderr)
        _track_exit(res.exit_code)

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=worst_exit)
