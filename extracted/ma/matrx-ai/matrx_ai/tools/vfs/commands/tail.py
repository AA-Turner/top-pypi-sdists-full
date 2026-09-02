from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import tail_no_file
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _invalid_option(letter: str) -> bytes:
    return encode(
        f"tail: invalid option -- '{letter}'\nTry 'tail --help' for more information.\n"
    )


def _invalid_argument(flag: str, value: str) -> bytes:
    return encode(f"tail: invalid number of {flag}: '{value}'\n")


def _parse_size(raw: str) -> tuple[int, bool]:
    # Returns (n, from_start). Leading '+' means "from this line/byte to EOF".
    if not raw:
        raise ValueError(raw)
    from_start = False
    s = raw
    if s[0] == "+":
        from_start = True
        s = s[1:]
    elif s[0] == "-":
        s = s[1:]
    if not s:
        raise ValueError(raw)
    multipliers: dict[str, int] = {
        "b": 512,
        "K": 1024,
        "KB": 1000,
        "M": 1024 * 1024,
        "MB": 1000 * 1000,
        "G": 1024 ** 3,
        "GB": 1000 ** 3,
        "T": 1024 ** 4,
        "TB": 1000 ** 4,
    }
    multiplier = 1
    for suffix, mult in sorted(multipliers.items(), key=lambda kv: -len(kv[0])):
        if s.endswith(suffix) and len(s) > len(suffix):
            multiplier = mult
            s = s[: -len(suffix)]
            break
    if not s.isdigit():
        raise ValueError(raw)
    return int(s) * multiplier, from_start


class _Opts:
    __slots__ = ("count", "is_bytes", "from_start", "verbose", "quiet", "follow")

    def __init__(self) -> None:
        self.count: int = 10
        self.is_bytes = False
        self.from_start = False
        self.verbose = False
        self.quiet = False
        self.follow = False


def _parse_args(args: list[str]) -> tuple[_Opts, list[str], CommandResult | None]:
    opts = _Opts()
    files: list[str] = []
    i = 0
    end_of_opts = False
    while i < len(args):
        a = args[i]
        if end_of_opts:
            files.append(a)
            i += 1
            continue
        if a == "--":
            end_of_opts = True
            i += 1
            continue
        if a == "-":
            files.append(a)
            i += 1
            continue
        if a.startswith("--"):
            name, _, value = a[2:].partition("=")
            if name == "bytes":
                if not value and i + 1 < len(args):
                    i += 1
                    value = args[i]
                try:
                    n, fs = _parse_size(value)
                except ValueError:
                    return opts, files, fail(1, _invalid_argument("bytes", value))
                opts.is_bytes = True
                opts.count = n
                opts.from_start = fs
            elif name == "lines":
                if not value and i + 1 < len(args):
                    i += 1
                    value = args[i]
                try:
                    n, fs = _parse_size(value)
                except ValueError:
                    return opts, files, fail(1, _invalid_argument("lines", value))
                opts.is_bytes = False
                opts.count = n
                opts.from_start = fs
            elif name == "follow":
                opts.follow = True
            elif name == "quiet" or name == "silent":
                opts.quiet = True
            elif name == "verbose":
                opts.verbose = True
            else:
                return opts, files, fail(1, _invalid_option(name))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            rest = a[1:]
            if rest[0].isdigit():
                try:
                    n, fs = _parse_size(rest)
                except ValueError:
                    return opts, files, fail(1, _invalid_argument("lines", a))
                opts.is_bytes = False
                opts.count = n
                opts.from_start = fs
                i += 1
                continue
            j = 0
            while j < len(rest):
                letter = rest[j]
                if letter == "n" or letter == "c":
                    value = rest[j + 1 :]
                    if not value:
                        if i + 1 >= len(args):
                            return opts, files, fail(
                                1, _invalid_argument("lines" if letter == "n" else "bytes", "")
                            )
                        i += 1
                        value = args[i]
                    try:
                        n, fs = _parse_size(value)
                    except ValueError:
                        flag = "lines" if letter == "n" else "bytes"
                        return opts, files, fail(1, _invalid_argument(flag, value))
                    opts.is_bytes = letter == "c"
                    opts.count = n
                    opts.from_start = fs
                    j = len(rest)
                    break
                elif letter == "q":
                    opts.quiet = True
                    j += 1
                elif letter == "v":
                    opts.verbose = True
                    j += 1
                elif letter == "f" or letter == "F":
                    opts.follow = True
                    j += 1
                elif letter == "z":
                    j += 1
                else:
                    return opts, files, fail(1, _invalid_option(letter))
            i += 1
            continue
        files.append(a)
        i += 1
    return opts, files, None


def _take_last_lines(data: bytes, n: int) -> bytes:
    if n <= 0 or not data:
        return b""
    # Count newlines from the end.
    pos = len(data)
    if data.endswith(b"\n"):
        pos -= 1
    count = 0
    while pos > 0 and count < n:
        nl = data.rfind(b"\n", 0, pos)
        if nl == -1:
            return data
        count += 1
        if count == n:
            return data[nl + 1 :]
        pos = nl
    return data


def _take_from_line(data: bytes, n: int) -> bytes:
    # n is 1-based: +1 means whole file, +2 means from line 2 onward.
    if n <= 1 or not data:
        return data
    pos = 0
    skipped = 0
    target = n - 1
    while skipped < target:
        nl = data.find(b"\n", pos)
        if nl == -1:
            return b""
        pos = nl + 1
        skipped += 1
    return data[pos:]


def _take_last_bytes(data: bytes, n: int) -> bytes:
    if n <= 0:
        return b""
    if n >= len(data):
        return data
    return data[-n:]


def _take_from_byte(data: bytes, n: int) -> bytes:
    # n is 1-based; +1 means whole file.
    if n <= 1:
        return data
    return data[n - 1 :]


def _format_header(path: str) -> bytes:
    return f"==> {path} <==\n".encode()


@register("tail")
async def cmd_tail(ctx: CommandContext) -> CommandResult:
    opts, files, err = _parse_args(ctx.args)
    if err is not None:
        return err

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    def slice_data(data: bytes) -> bytes:
        if opts.is_bytes:
            return _take_from_byte(data, opts.count) if opts.from_start else _take_last_bytes(
                data, opts.count
            )
        return _take_from_line(data, opts.count) if opts.from_start else _take_last_lines(
            data, opts.count
        )

    if not files:
        out.extend(slice_data(ctx.stdin))
        return ok(bytes(out))

    show_headers = (len(files) > 1 or opts.verbose) and not opts.quiet
    first_emitted = False
    for path in files:
        if path == "-":
            data = ctx.stdin
        else:
            resolved = resolve_cwd(ctx.env, path)
            try:
                if await ctx.vfs._isdir(resolved):
                    err_out.extend(encode(tail_no_file(path)))
                    exit_code = 1
                    continue
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(tail_no_file(path)))
                exit_code = 1
                continue
            except OSError:
                err_out.extend(encode(tail_no_file(path)))
                exit_code = 1
                continue
        if show_headers:
            if first_emitted:
                out.extend(b"\n")
            out.extend(_format_header(path))
        out.extend(slice_data(data))
        first_emitted = True

    # Follow mode: emit current tail and return immediately. No blocking.
    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
