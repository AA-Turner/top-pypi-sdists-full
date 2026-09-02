from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import (
    cat_is_dir,
    cat_no_file,
    format_cat_minus_a,
    format_cat_n_with_offset,
    from_oserror,
)
from matrx_ai.tools.vfs.shell.runner import CommandResult

_LONG_OPTS: dict[str, str] = {
    "--show-all": "A",
    "--number-nonblank": "b",
    "--show-ends": "E",
    "--number": "n",
    "--squeeze-blank": "s",
    "--show-tabs": "T",
    "--show-nonprinting": "v",
}


class _Flags:
    __slots__ = ("show_all", "number_nonblank", "show_ends", "number", "squeeze", "show_tabs")

    def __init__(self) -> None:
        self.show_all = False
        self.number_nonblank = False
        self.show_ends = False
        self.number = False
        self.squeeze = False
        self.show_tabs = False


def _invalid_option(letter: str) -> bytes:
    return encode(
        f"cat: invalid option -- '{letter}'\nTry 'cat --help' for more information.\n"
    )


def _parse_args(args: list[str]) -> tuple[_Flags, list[str], CommandResult | None]:
    flags = _Flags()
    files: list[str] = []
    i = 0
    end_of_opts = False
    while i < len(args):
        a = args[i]
        if end_of_opts:
            files.append(a)
        elif a == "--":
            end_of_opts = True
        elif a == "-":
            files.append(a)
        elif a.startswith("--"):
            letter = _LONG_OPTS.get(a)
            if letter is None:
                name = a[2:].split("=", 1)[0]
                return flags, files, fail(1, _invalid_option(name))
            _apply_letter(flags, letter)
            if letter == "A":
                flags.show_ends = True
                flags.show_tabs = True
        elif a.startswith("-") and len(a) > 1:
            for letter in a[1:]:
                if letter == "A":
                    flags.show_all = True
                    flags.show_ends = True
                    flags.show_tabs = True
                elif letter in ("b", "E", "n", "s", "T", "v", "e", "t", "u"):
                    _apply_letter(flags, letter)
                else:
                    return flags, files, fail(1, _invalid_option(letter))
        else:
            files.append(a)
        i += 1
    return flags, files, None


def _apply_letter(flags: _Flags, letter: str) -> None:
    if letter == "A":
        flags.show_all = True
        flags.show_ends = True
        flags.show_tabs = True
    elif letter == "b":
        flags.number_nonblank = True
    elif letter == "E":
        flags.show_ends = True
    elif letter == "e":
        flags.show_ends = True
        flags.show_all = True
    elif letter == "n":
        flags.number = True
    elif letter == "s":
        flags.squeeze = True
    elif letter == "T":
        flags.show_tabs = True
    elif letter == "t":
        flags.show_tabs = True
        flags.show_all = True
    elif letter == "v":
        flags.show_all = True
    # 'u' is a no-op (unbuffered); accept silently.


def _apply_show_all(content: bytes) -> bytes:
    text = content.decode("latin-1")
    return format_cat_minus_a(text).encode("latin-1")


def _apply_show_tabs(content: bytes) -> bytes:
    return content.replace(b"\t", b"^I")


def _apply_show_ends(content: bytes) -> bytes:
    return content.replace(b"\n", b"$\n")


def _apply_squeeze(content: bytes) -> bytes:
    if not content:
        return content
    # Squeeze runs of more than one empty line to a single empty line.
    out = bytearray()
    last_was_empty = False
    in_first = True
    # Split keeping each line plus its newline.
    lines: list[bytes] = []
    start = 0
    for i, b in enumerate(content):
        if b == 0x0A:
            lines.append(content[start : i + 1])
            start = i + 1
    if start < len(content):
        lines.append(content[start:])

    blank_run = 0
    for line in lines:
        is_empty = line == b"\n" or line == b""
        if is_empty and line == b"\n":
            blank_run += 1
            if blank_run > 1:
                continue
            out.extend(line)
        else:
            blank_run = 0
            out.extend(line)
        in_first = False
        last_was_empty = is_empty
    _ = (in_first, last_was_empty)
    return bytes(out)


def _apply_numbering(content: bytes, number_nonblank: bool, start: int) -> tuple[bytes, int]:
    # Decode latin-1 to preserve bytes 1:1; format_cat_n_with_offset is text-based,
    # but we operate on bytes and emit identical bytes back.
    if not content:
        return b"", start
    out = bytearray()
    counter = start
    # Iterate over lines (each line's terminator preserved; a trailing unterminated
    # line is also numbered with a synthetic newline added — matches GNU cat -n).
    pos = 0
    while pos < len(content):
        nl = content.find(b"\n", pos)
        if nl == -1:
            line = content[pos:]
            terminator = b""
            pos = len(content)
        else:
            line = content[pos:nl]
            terminator = b"\n"
            pos = nl + 1

        is_blank = len(line) == 0
        if number_nonblank and is_blank:
            out.extend(line)
            out.extend(terminator)
        else:
            label = f"{counter:>6d}\t".encode()
            out.extend(label)
            out.extend(line)
            out.extend(terminator)
            counter += 1
    return bytes(out), counter


def _transform(
    content: bytes,
    flags: _Flags,
    line_counter: int,
) -> tuple[bytes, int]:
    data = content
    if flags.squeeze:
        data = _apply_squeeze(data)
    # show_all subsumes show_tabs and show_ends.
    if flags.show_all:
        data = _apply_show_all(data)
    else:
        if flags.show_tabs:
            data = _apply_show_tabs(data)
        if flags.show_ends:
            data = _apply_show_ends(data)
    if flags.number or flags.number_nonblank:
        data, line_counter = _apply_numbering(data, flags.number_nonblank, line_counter)
    _ = format_cat_n_with_offset  # keep import live for potential future use.
    return data, line_counter


@register("cat")
async def cmd_cat(ctx: CommandContext) -> CommandResult:
    flags, files, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not files:
        # No files: copy stdin to stdout.
        data = ctx.stdin
        out, _ = _transform(data, flags, 1)
        return ok(out)

    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    line_counter = 1

    for path in files:
        if path == "-":
            data = ctx.stdin
        else:
            resolved = resolve_cwd(ctx.env, path)
            try:
                if await ctx.vfs._isdir(resolved):
                    err_out.extend(encode(cat_is_dir(path)))
                    exit_code = 1
                    continue
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(cat_no_file(path)))
                exit_code = 1
                continue
            except IsADirectoryError:
                err_out.extend(encode(cat_is_dir(path)))
                exit_code = 1
                continue
            except OSError as e:
                err_out.extend(encode(from_oserror("cat", path, e)))
                exit_code = 1
                continue

        chunk, line_counter = _transform(data, flags, line_counter)
        out.extend(chunk)

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
