from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import head_no_file
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _invalid_option(letter: str) -> bytes:
    return encode(
        f"head: invalid option -- '{letter}'\nTry 'head --help' for more information.\n"
    )


def _invalid_argument(flag: str, value: str) -> bytes:
    return encode(f"head: invalid number of {flag}: '{value}'\n")


def _parse_size(raw: str) -> tuple[int, bool]:
    # Returns (n, leading_minus). Allows leading '+' (treated as positive),
    # leading '-' meaning "all but last N", and suffixes K, KB, M, MB, G, GB, T, TB.
    if not raw:
        raise ValueError(raw)
    leading_minus = False
    s = raw
    if s[0] == "+":
        s = s[1:]
    elif s[0] == "-":
        leading_minus = True
        s = s[1:]
    if not s:
        raise ValueError(raw)

    # Find suffix.
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
    return int(s) * multiplier, leading_minus


class _Opts:
    __slots__ = ("count", "is_bytes", "all_but_last", "verbose", "quiet")

    def __init__(self) -> None:
        self.count: int = 10
        self.is_bytes = False
        self.all_but_last = False
        self.verbose = False
        self.quiet = False


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
                    n, neg = _parse_size(value)
                except ValueError:
                    return opts, files, fail(1, _invalid_argument("bytes", value))
                opts.is_bytes = True
                opts.count = n
                opts.all_but_last = neg
            elif name == "lines":
                if not value and i + 1 < len(args):
                    i += 1
                    value = args[i]
                try:
                    n, neg = _parse_size(value)
                except ValueError:
                    return opts, files, fail(1, _invalid_argument("lines", value))
                opts.is_bytes = False
                opts.count = n
                opts.all_but_last = neg
            elif name == "quiet" or name == "silent":
                opts.quiet = True
            elif name == "verbose":
                opts.verbose = True
            else:
                return opts, files, fail(1, _invalid_option(name))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            # Could be a numeric shortcut like -5 (legacy obsolete syntax).
            rest = a[1:]
            if rest[0].isdigit():
                try:
                    n, _ = _parse_size(rest)
                except ValueError:
                    return opts, files, fail(1, _invalid_argument("lines", a))
                opts.is_bytes = False
                opts.count = n
                opts.all_but_last = False
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
                        n, neg = _parse_size(value)
                    except ValueError:
                        flag = "lines" if letter == "n" else "bytes"
                        return opts, files, fail(1, _invalid_argument(flag, value))
                    opts.is_bytes = letter == "c"
                    opts.count = n
                    opts.all_but_last = neg
                    j = len(rest)
                    break
                elif letter == "q":
                    opts.quiet = True
                    j += 1
                elif letter == "v":
                    opts.verbose = True
                    j += 1
                elif letter == "z":
                    # Zero-terminated lines; treat as default for VFS purposes.
                    j += 1
                else:
                    return opts, files, fail(1, _invalid_option(letter))
            i += 1
            continue
        files.append(a)
        i += 1
    return opts, files, None


def _take_lines(data: bytes, n: int, all_but_last: bool) -> bytes:
    if not data:
        return b""
    if all_but_last:
        # Drop last n lines.
        # Number of lines = number of '\n' + (1 if data does not end with \n).
        if n <= 0:
            return data
        offsets: list[int] = []
        pos = 0
        while True:
            nl = data.find(b"\n", pos)
            if nl == -1:
                break
            offsets.append(nl)
            pos = nl + 1
        ends_in_nl = data.endswith(b"\n")
        total = len(offsets) + (0 if ends_in_nl else 1)
        keep = total - n
        if keep <= 0:
            return b""
        # Keep first `keep` lines.
        if keep <= len(offsets):
            return data[: offsets[keep - 1] + 1]
        return data
    if n <= 0:
        return b""
    pos = 0
    count = 0
    while count < n:
        nl = data.find(b"\n", pos)
        if nl == -1:
            return data
        count += 1
        pos = nl + 1
    return data[:pos]


def _take_bytes(data: bytes, n: int, all_but_last: bool) -> bytes:
    if all_but_last:
        if n <= 0:
            return data
        if n >= len(data):
            return b""
        return data[: len(data) - n]
    if n <= 0:
        return b""
    return data[:n]


def _format_header(path: str) -> bytes:
    return f"==> {path} <==\n".encode()


@register("head")
async def cmd_head(ctx: CommandContext) -> CommandResult:
    opts, files, err = _parse_args(ctx.args)
    if err is not None:
        return err

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    if not files:
        data = ctx.stdin
        chunk = (
            _take_bytes(data, opts.count, opts.all_but_last)
            if opts.is_bytes
            else _take_lines(data, opts.count, opts.all_but_last)
        )
        out.extend(chunk)
        return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)

    show_headers = (len(files) > 1 or opts.verbose) and not opts.quiet

    first_emitted = False
    for path in files:
        if path == "-":
            data = ctx.stdin
        else:
            resolved = resolve_cwd(ctx.env, path)
            try:
                if await ctx.vfs._isdir(resolved):
                    err_out.extend(encode(head_no_file(path)))
                    exit_code = 1
                    continue
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(head_no_file(path)))
                exit_code = 1
                continue
            except OSError:
                err_out.extend(encode(head_no_file(path)))
                exit_code = 1
                continue
        if show_headers:
            if first_emitted:
                out.extend(b"\n")
            out.extend(_format_header(path))
        chunk = (
            _take_bytes(data, opts.count, opts.all_but_last)
            if opts.is_bytes
            else _take_lines(data, opts.count, opts.all_but_last)
        )
        out.extend(chunk)
        first_emitted = True

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
