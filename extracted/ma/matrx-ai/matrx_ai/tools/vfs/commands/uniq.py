from __future__ import annotations

from dataclasses import dataclass

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


@dataclass(slots=True)
class _Opts:
    count: bool = False
    repeated: bool = False
    unique_only: bool = False
    ignore_case: bool = False
    skip_fields: int = 0
    skip_chars: int = 0
    input_file: str | None = None
    output_file: str | None = None


def _bad_arg(msg: str) -> bytes:
    return encode(f"uniq: {msg}\nTry 'uniq --help' for more information.\n")


def _parse_int(s: str) -> int | None:
    if s.isdigit():
        return int(s)
    return None


def _parse_args(args: list[str]) -> tuple[_Opts, CommandResult | None]:
    opts = _Opts()
    positional: list[str] = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            positional.extend(args[i + 1 :])
            break
        if a == "-":
            positional.append(a)
            i += 1
            continue
        if a.startswith("--"):
            name, has_eq, value = a[2:].partition("=")
            if name == "count":
                opts.count = True
            elif name == "repeated":
                opts.repeated = True
            elif name == "unique":
                opts.unique_only = True
            elif name == "ignore-case":
                opts.ignore_case = True
            elif name == "skip-fields":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_arg("option requires an argument"))
                    i += 1
                    value = args[i]
                n = _parse_int(value)
                if n is None:
                    return opts, fail(1, _bad_arg(f"invalid number of fields to skip: '{value}'"))
                opts.skip_fields = n
            elif name == "skip-chars":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_arg("option requires an argument"))
                    i += 1
                    value = args[i]
                n = _parse_int(value)
                if n is None:
                    return opts, fail(1, _bad_arg(f"invalid number of bytes to skip: '{value}'"))
                opts.skip_chars = n
            else:
                return opts, fail(1, _bad_arg(f"unrecognized option '--{name}'"))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1 and not a[1:].isdigit():
            j = 1
            while j < len(a):
                letter = a[j]
                if letter == "c":
                    opts.count = True
                    j += 1
                elif letter == "d":
                    opts.repeated = True
                    j += 1
                elif letter == "u":
                    opts.unique_only = True
                    j += 1
                elif letter == "i":
                    opts.ignore_case = True
                    j += 1
                elif letter == "f":
                    inline = a[j + 1 :]
                    if inline:
                        value = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(1, _bad_arg("option requires an argument -- 'f'"))
                        i += 1
                        value = args[i]
                        j = len(a)
                    n = _parse_int(value)
                    if n is None:
                        return opts, fail(
                            1, _bad_arg(f"invalid number of fields to skip: '{value}'")
                        )
                    opts.skip_fields = n
                elif letter == "s":
                    inline = a[j + 1 :]
                    if inline:
                        value = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(1, _bad_arg("option requires an argument -- 's'"))
                        i += 1
                        value = args[i]
                        j = len(a)
                    n = _parse_int(value)
                    if n is None:
                        return opts, fail(
                            1, _bad_arg(f"invalid number of bytes to skip: '{value}'")
                        )
                    opts.skip_chars = n
                else:
                    return opts, fail(1, _bad_arg(f"invalid option -- '{letter}'"))
            i += 1
            continue
        positional.append(a)
        i += 1

    if len(positional) >= 1:
        opts.input_file = positional[0]
    if len(positional) >= 2:
        opts.output_file = positional[1]
    if len(positional) >= 3:
        return opts, fail(1, _bad_arg(f"extra operand '{positional[2]}'"))
    return opts, None


def _key(line: str, opts: _Opts) -> str:
    s = line
    if opts.skip_fields > 0:
        # Skip leading whitespace, then N field-and-trailing-whitespace blocks.
        idx = 0
        n = opts.skip_fields
        while n > 0 and idx < len(s):
            while idx < len(s) and s[idx] in (" ", "\t"):
                idx += 1
            while idx < len(s) and s[idx] not in (" ", "\t"):
                idx += 1
            n -= 1
        s = s[idx:]
    if opts.skip_chars > 0:
        s = s[opts.skip_chars :] if opts.skip_chars < len(s) else ""
    if opts.ignore_case:
        s = s.lower()
    return s


@register("uniq")
async def cmd_uniq(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if opts.input_file and opts.input_file != "-":
        resolved = resolve_cwd(ctx.env, opts.input_file)
        try:
            data = await ctx.vfs._cat_file(resolved)
        except FileNotFoundError:
            return fail(
                1, encode(f"uniq: {opts.input_file}: No such file or directory\n")
            )
        except OSError as exc:
            return fail(
                1, encode(f"uniq: {opts.input_file}: {exc.strerror or 'I/O error'}\n")
            )
    else:
        data = ctx.stdin

    text = data.decode("latin-1")
    ends_with_nl = text.endswith("\n")
    body = text[:-1] if ends_with_nl else text
    lines = body.split("\n") if body else ([] if not ends_with_nl else [""])

    out = bytearray()
    if not lines:
        return ok(b"")

    # Collect runs.
    runs: list[tuple[str, int]] = []  # (representative_line, count)
    cur_line = lines[0]
    cur_key = _key(cur_line, opts)
    cur_count = 1
    for line in lines[1:]:
        k = _key(line, opts)
        if k == cur_key:
            cur_count += 1
        else:
            runs.append((cur_line, cur_count))
            cur_line = line
            cur_key = k
            cur_count = 1
    runs.append((cur_line, cur_count))

    for line, count in runs:
        if opts.repeated and count < 2:
            continue
        if opts.unique_only and count != 1:
            continue
        if opts.count:
            out.extend(encode(f"{count:>7d} {line}\n"))
        else:
            out.extend(line.encode("latin-1"))
            out.append(0x0A)

    if opts.output_file:
        resolved = resolve_cwd(ctx.env, opts.output_file)
        await ctx.vfs._pipe_file(resolved, bytes(out))
        return ok(b"")
    return ok(bytes(out))
