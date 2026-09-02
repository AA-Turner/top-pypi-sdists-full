from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

# POSIX whitespace bytes for word-splitting.
_WHITESPACE = b" \t\n\v\f\r"
_WHITESPACE_SET = set(_WHITESPACE)


def _invalid_option(letter: str) -> bytes:
    return encode(
        f"wc: invalid option -- '{letter}'\nTry 'wc --help' for more information.\n"
    )


def _wc_no_file(path: str) -> str:
    return f"wc: {path}: No such file or directory\n"


def _wc_is_dir(path: str) -> str:
    return f"wc: {path}: Is a directory\n"


class _Opts:
    __slots__ = ("lines", "words", "bytes", "chars", "max_line", "any_set")

    def __init__(self) -> None:
        self.lines = False
        self.words = False
        self.bytes = False
        self.chars = False
        self.max_line = False
        self.any_set = False


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
            name = a[2:]
            if name == "lines":
                opts.lines = True
                opts.any_set = True
            elif name == "words":
                opts.words = True
                opts.any_set = True
            elif name == "bytes":
                opts.bytes = True
                opts.any_set = True
            elif name == "chars":
                opts.chars = True
                opts.any_set = True
            elif name == "max-line-length":
                opts.max_line = True
                opts.any_set = True
            else:
                return opts, files, fail(1, _invalid_option(name))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            for letter in a[1:]:
                if letter == "l":
                    opts.lines = True
                    opts.any_set = True
                elif letter == "w":
                    opts.words = True
                    opts.any_set = True
                elif letter == "c":
                    opts.bytes = True
                    opts.any_set = True
                elif letter == "m":
                    opts.chars = True
                    opts.any_set = True
                elif letter == "L":
                    opts.max_line = True
                    opts.any_set = True
                else:
                    return opts, files, fail(1, _invalid_option(letter))
            i += 1
            continue
        files.append(a)
        i += 1

    if not opts.any_set:
        opts.lines = True
        opts.words = True
        opts.bytes = True
    return opts, files, None


def _count(data: bytes) -> tuple[int, int, int, int, int]:
    # lines, words, bytes, chars, max_line_length
    lines = data.count(b"\n")
    byte_len = len(data)
    word_count = 0
    in_word = False
    for b in data:
        if b in _WHITESPACE_SET:
            in_word = False
        else:
            if not in_word:
                word_count += 1
                in_word = True
    try:
        chars = len(data.decode("utf-8"))
    except UnicodeDecodeError:
        chars = byte_len

    # Longest line length (excluding newline). For wc -L, GNU expands tabs to
    # next multiple of 8; we approximate by counting raw chars in the line.
    max_line = 0
    cur = 0
    for b in data:
        if b == 0x0A:
            if cur > max_line:
                max_line = cur
            cur = 0
        elif b == 0x09:
            cur = (cur // 8 + 1) * 8
        else:
            cur += 1
    if cur > max_line:
        max_line = cur
    return lines, word_count, byte_len, chars, max_line


def _selected_columns(opts: _Opts, counts: tuple[int, int, int, int, int]) -> list[int]:
    lines, words, byte_len, chars, max_line = counts
    cols: list[int] = []
    if opts.lines:
        cols.append(lines)
    if opts.words:
        cols.append(words)
    if opts.bytes:
        cols.append(byte_len)
    if opts.chars:
        cols.append(chars)
    if opts.max_line:
        cols.append(max_line)
    return cols


@register("wc")
async def cmd_wc(ctx: CommandContext) -> CommandResult:
    opts, files, err = _parse_args(ctx.args)
    if err is not None:
        return err

    err_out = bytearray()
    exit_code = 0

    rows: list[tuple[list[int], str | None]] = []  # (cols, label-or-None)

    if not files:
        counts = _count(ctx.stdin)
        rows.append((_selected_columns(opts, counts), None))
    else:
        totals = [0] * 5  # lines, words, bytes, chars, max_line (max for max_line)
        any_ok = False
        for path in files:
            if path == "-":
                data = ctx.stdin
                counts = _count(data)
                rows.append((_selected_columns(opts, counts), path))
                for k in range(4):
                    totals[k] += counts[k]
                if counts[4] > totals[4]:
                    totals[4] = counts[4]
                any_ok = True
                continue
            resolved = resolve_cwd(ctx.env, path)
            try:
                if await ctx.vfs._isdir(resolved):
                    err_out.extend(encode(_wc_is_dir(path)))
                    exit_code = 1
                    rows.append((_selected_columns(opts, (0, 0, 0, 0, 0)), path))
                    continue
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(_wc_no_file(path)))
                exit_code = 1
                continue
            except OSError:
                err_out.extend(encode(_wc_no_file(path)))
                exit_code = 1
                continue
            counts = _count(data)
            rows.append((_selected_columns(opts, counts), path))
            for k in range(4):
                totals[k] += counts[k]
            if counts[4] > totals[4]:
                totals[4] = counts[4]
            any_ok = True

        # Multiple successful files → totals row.
        successful = [r for r in rows if r[1] is not None and not _zero_cols(r[0])]
        if len([p for p in files if True]) > 1 and any_ok:
            total_counts = (totals[0], totals[1], totals[2], totals[3], totals[4])
            rows.append((_selected_columns(opts, total_counts), "total"))
        _ = successful  # silence unused.

    # Build output with right-aligned padding to max column width.
    if not rows:
        return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)
    num_cols = len(rows[0][0])
    if num_cols == 0:
        return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)
    widths = [0] * num_cols
    for cols, _label in rows:
        for j, v in enumerate(cols):
            w = len(str(v))
            if w > widths[j]:
                widths[j] = w

    out = bytearray()
    for cols, label in rows:
        parts = [f"{cols[j]:>{widths[j]}d}" for j in range(num_cols)]
        line = " ".join(parts)
        if label is not None:
            line = f"{line} {label}"
        out.extend(encode(line + "\n"))

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)


def _zero_cols(cols: list[int]) -> bool:
    return all(c == 0 for c in cols)
