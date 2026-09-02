from __future__ import annotations

from dataclasses import dataclass, field

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


@dataclass(slots=True)
class _Opts:
    mode: str = ""  # "f" for fields, "c" for chars, "b" for bytes
    delim: str = "\t"
    output_delim: str | None = None
    ranges: list[tuple[int, int]] = field(default_factory=list)  # (start,end) 1-based, end=-1=open
    suppress_no_delim: bool = False
    complement: bool = False
    files: list[str] = field(default_factory=list)


def _bad_usage(msg: str) -> bytes:
    return encode(f"cut: {msg}\nTry 'cut --help' for more information.\n")


def _parse_ranges(spec: str) -> list[tuple[int, int]] | None:
    if not spec:
        return None
    result: list[tuple[int, int]] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            return None
        if "-" in part:
            a, _, b = part.partition("-")
            if a == "" and b == "":
                return None
            if a == "":
                # -N → 1..N
                if not b.isdigit():
                    return None
                start = 1
                end = int(b)
            elif b == "":
                # N- → N..open
                if not a.isdigit():
                    return None
                start = int(a)
                end = -1
            else:
                if not a.isdigit() or not b.isdigit():
                    return None
                start = int(a)
                end = int(b)
            if start < 1:
                return None
            if end != -1 and end < start:
                return None
        else:
            if not part.isdigit():
                return None
            n = int(part)
            if n < 1:
                return None
            start = n
            end = n
        result.append((start, end))
    return result


def _parse_args(args: list[str]) -> tuple[_Opts, CommandResult | None]:
    opts = _Opts()
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            opts.files.extend(args[i + 1 :])
            break
        if a == "-":
            opts.files.append(a)
            i += 1
            continue
        if a.startswith("--"):
            name, has_eq, value = a[2:].partition("=")
            if name == "delimiter":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_usage("option requires an argument -- 'd'"))
                    i += 1
                    value = args[i]
                if len(value) != 1:
                    return opts, fail(1, _bad_usage("the delimiter must be a single character"))
                opts.delim = value
            elif name == "fields":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_usage("option requires an argument -- 'f'"))
                    i += 1
                    value = args[i]
                rng = _parse_ranges(value)
                if rng is None:
                    return opts, fail(1, _bad_usage("invalid field range"))
                opts.mode = "f"
                opts.ranges = rng
            elif name == "characters":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_usage("option requires an argument -- 'c'"))
                    i += 1
                    value = args[i]
                rng = _parse_ranges(value)
                if rng is None:
                    return opts, fail(1, _bad_usage("invalid field range"))
                opts.mode = "c"
                opts.ranges = rng
            elif name == "bytes":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_usage("option requires an argument -- 'b'"))
                    i += 1
                    value = args[i]
                rng = _parse_ranges(value)
                if rng is None:
                    return opts, fail(1, _bad_usage("invalid field range"))
                opts.mode = "b"
                opts.ranges = rng
            elif name == "output-delimiter":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _bad_usage("option requires an argument"))
                    i += 1
                    value = args[i]
                opts.output_delim = value
            elif name == "only-delimited":
                opts.suppress_no_delim = True
            elif name == "complement":
                opts.complement = True
            else:
                return opts, fail(1, _bad_usage(f"unrecognized option '--{name}'"))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            j = 1
            consumed_arg = False
            while j < len(a):
                letter = a[j]
                if letter in ("d", "f", "c", "b"):
                    inline = a[j + 1 :]
                    if inline:
                        value = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(
                                1, _bad_usage(f"option requires an argument -- '{letter}'")
                            )
                        i += 1
                        value = args[i]
                        consumed_arg = True
                        j = len(a)
                    if letter == "d":
                        if len(value) != 1:
                            return opts, fail(
                                1, _bad_usage("the delimiter must be a single character")
                            )
                        opts.delim = value
                    else:
                        rng = _parse_ranges(value)
                        if rng is None:
                            return opts, fail(1, _bad_usage("invalid field range"))
                        opts.mode = letter
                        opts.ranges = rng
                    break
                if letter == "s":
                    opts.suppress_no_delim = True
                    j += 1
                    continue
                if letter == "n":
                    # POSIX: don't split multibyte chars. Ignored here.
                    j += 1
                    continue
                return opts, fail(1, _bad_usage(f"invalid option -- '{letter}'"))
            if not consumed_arg:
                i += 1
            else:
                i += 1
            continue
        opts.files.append(a)
        i += 1

    if not opts.mode:
        return opts, fail(1, _bad_usage("you must specify a list of bytes, characters, or fields"))
    return opts, None


def _select_indices(length: int, ranges: list[tuple[int, int]]) -> list[int]:
    selected: set[int] = set()
    for start, end in ranges:
        actual_end = length if end == -1 else min(end, length)
        for k in range(start - 1, actual_end):
            if 0 <= k < length:
                selected.add(k)
    return sorted(selected)


def _apply_to_chars(line: str, ranges: list[tuple[int, int]], complement: bool) -> str:
    indices = _select_indices(len(line), ranges)
    if complement:
        idx_set = set(indices)
        out = "".join(line[i] for i in range(len(line)) if i not in idx_set)
    else:
        out = "".join(line[i] for i in indices)
    return out


def _apply_to_fields(
    line: str,
    delim: str,
    out_delim: str,
    ranges: list[tuple[int, int]],
    suppress: bool,
    complement: bool,
) -> str | None:
    if delim not in line:
        if suppress:
            return None
        return line
    fields = line.split(delim)
    indices = _select_indices(len(fields), ranges)
    if complement:
        idx_set = set(indices)
        keep = [i for i in range(len(fields)) if i not in idx_set]
    else:
        keep = indices
    return out_delim.join(fields[i] for i in keep)


@register("cut")
async def cmd_cut(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.args)
    if err is not None:
        return err

    out_delim = opts.output_delim if opts.output_delim is not None else opts.delim

    sources: list[tuple[str, bytes | None]] = []
    err_out = bytearray()
    exit_code = 0
    if not opts.files:
        sources.append(("-", None))
    else:
        for path in opts.files:
            sources.append((path, None))

    out = bytearray()
    for path, _ in sources:
        if path == "-":
            data = ctx.stdin
        else:
            resolved = resolve_cwd(ctx.env, path)
            try:
                if await ctx.vfs._isdir(resolved):
                    err_out.extend(encode(f"cut: {path}: Is a directory\n"))
                    exit_code = 1
                    continue
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(f"cut: {path}: No such file or directory\n"))
                exit_code = 1
                continue
            except OSError as exc:
                err_out.extend(encode(f"cut: {path}: {exc.strerror or 'I/O error'}\n"))
                exit_code = 1
                continue
        text = data.decode("latin-1")
        if not text:
            continue
        ends_in_newline = text.endswith("\n")
        if ends_in_newline:
            text = text[:-1]
        for line in text.split("\n"):
            if opts.mode == "f":
                result = _apply_to_fields(
                    line, opts.delim, out_delim, opts.ranges, opts.suppress_no_delim, opts.complement
                )
                if result is None:
                    continue
                out.extend(result.encode("latin-1"))
                out.append(0x0A)
            elif opts.mode == "c":
                result = _apply_to_chars(line, opts.ranges, opts.complement)
                out.extend(result.encode("latin-1"))
                out.append(0x0A)
            else:  # "b" — same as chars when input is byte-treated
                # Use bytes directly.
                line_b = line.encode("latin-1")
                indices = _select_indices(len(line_b), opts.ranges)
                if opts.complement:
                    idx_set = set(indices)
                    res_b = bytes(line_b[i] for i in range(len(line_b)) if i not in idx_set)
                else:
                    res_b = bytes(line_b[i] for i in indices)
                out.extend(res_b)
                out.append(0x0A)

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
