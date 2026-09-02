from __future__ import annotations

import re

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

_USAGE_ERROR = b"printf: usage: printf [-v var] format [arguments]\n"


def _interpret_format_escapes(text: str) -> tuple[bytes, bool]:
    # printf-style: format-string backslash escapes. Returns (bytes, end_marker)
    # where end_marker is True if \c was encountered (terminates output entirely).
    out = bytearray()
    i = 0
    while i < len(text):
        ch = text[i]
        if ch != "\\" or i + 1 >= len(text):
            out.extend(ch.encode("utf-8"))
            i += 1
            continue
        nxt = text[i + 1]
        if nxt == "\\":
            out.append(0x5C)
            i += 2
        elif nxt == "a":
            out.append(0x07)
            i += 2
        elif nxt == "b":
            out.append(0x08)
            i += 2
        elif nxt == "c":
            return bytes(out), True
        elif nxt == "e" or nxt == "E":
            out.append(0x1B)
            i += 2
        elif nxt == "f":
            out.append(0x0C)
            i += 2
        elif nxt == "n":
            out.append(0x0A)
            i += 2
        elif nxt == "r":
            out.append(0x0D)
            i += 2
        elif nxt == "t":
            out.append(0x09)
            i += 2
        elif nxt == "v":
            out.append(0x0B)
            i += 2
        elif nxt == "x":
            j = i + 2
            digits = ""
            while j < len(text) and len(digits) < 2 and text[j] in "0123456789abcdefABCDEF":
                digits += text[j]
                j += 1
            if digits:
                out.append(int(digits, 16) & 0xFF)
                i = j
            else:
                out.extend(b"\\x")
                i += 2
        elif nxt in "01234567":
            # printf format octal: \NNN (1-3 digits, no leading 0 required).
            j = i + 1
            digits = ""
            while j < len(text) and len(digits) < 3 and text[j] in "01234567":
                digits += text[j]
                j += 1
            out.append(int(digits, 8) & 0xFF)
            i = j
        else:
            out.append(0x5C)
            out.extend(nxt.encode("utf-8"))
            i += 2
    return bytes(out), False


def _interpret_b_arg(text: str) -> bytes:
    # %b: interpret echo-style backslash escapes in the arg, including \c.
    out = bytearray()
    i = 0
    while i < len(text):
        ch = text[i]
        if ch != "\\" or i + 1 >= len(text):
            out.extend(ch.encode("utf-8"))
            i += 1
            continue
        nxt = text[i + 1]
        if nxt == "\\":
            out.append(0x5C)
            i += 2
        elif nxt == "a":
            out.append(0x07)
            i += 2
        elif nxt == "b":
            out.append(0x08)
            i += 2
        elif nxt == "c":
            return bytes(out)
        elif nxt == "e" or nxt == "E":
            out.append(0x1B)
            i += 2
        elif nxt == "f":
            out.append(0x0C)
            i += 2
        elif nxt == "n":
            out.append(0x0A)
            i += 2
        elif nxt == "r":
            out.append(0x0D)
            i += 2
        elif nxt == "t":
            out.append(0x09)
            i += 2
        elif nxt == "v":
            out.append(0x0B)
            i += 2
        elif nxt == "0":
            j = i + 2
            digits = ""
            while j < len(text) and len(digits) < 3 and text[j] in "01234567":
                digits += text[j]
                j += 1
            if digits:
                out.append(int(digits, 8) & 0xFF)
            else:
                out.append(0)
            i = j
        elif nxt == "x":
            j = i + 2
            digits = ""
            while j < len(text) and len(digits) < 2 and text[j] in "0123456789abcdefABCDEF":
                digits += text[j]
                j += 1
            if digits:
                out.append(int(digits, 16) & 0xFF)
                i = j
            else:
                out.extend(b"\\x")
                i += 2
        else:
            out.append(0x5C)
            out.extend(nxt.encode("utf-8"))
            i += 2
    return bytes(out)


def _shell_quote(arg: str) -> str:
    # Bash %q: produce a shell-quoted string that, when read back, yields the
    # original. If the argument is "safe" alnum/dot/slash/-_, leave bare.
    if not arg:
        return "''"
    safe = re.compile(r"^[A-Za-z0-9_./:@%+,=-]+$")
    if safe.match(arg):
        return arg
    # Use $'...' form when there are control chars; otherwise single-quote.
    has_ctl = any(ord(c) < 0x20 or c in ("'", "\\") for c in arg)
    if has_ctl:
        out = ["$'"]
        for c in arg:
            o = ord(c)
            if c == "'":
                out.append("\\'")
            elif c == "\\":
                out.append("\\\\")
            elif o == 0x07:
                out.append("\\a")
            elif o == 0x08:
                out.append("\\b")
            elif o == 0x09:
                out.append("\\t")
            elif o == 0x0A:
                out.append("\\n")
            elif o == 0x0B:
                out.append("\\v")
            elif o == 0x0C:
                out.append("\\f")
            elif o == 0x0D:
                out.append("\\r")
            elif o < 0x20:
                out.append(f"\\x{o:02x}")
            else:
                out.append(c)
        out.append("'")
        return "".join(out)
    return "'" + arg + "'"


_SPEC_RE = re.compile(
    r"%(?P<flags>[-+ 0#']*)(?P<width>\*|\d+)?(?:\.(?P<prec>\*|\d+))?(?P<conv>[sdioxXcbq%])"
)


def _to_int(arg: str, err_out: bytearray) -> tuple[int, bool]:
    s = arg.strip()
    if not s:
        return 0, False
    base = 10
    if s.startswith(("0x", "0X")):
        base = 16
        body = s[2:]
        try:
            return int(body, 16), True
        except ValueError:
            err_out.extend(encode(f"printf: {arg}: invalid number\n"))
            return 0, False
    if s.startswith("'") or s.startswith('"'):
        # printf '%d' "'A" emits the codepoint of A.
        if len(s) >= 2:
            return ord(s[1]), True
        return 0, True
    try:
        if s.startswith("-0x") or s.startswith("-0X"):
            return -int(s[3:], 16), True
        if s.startswith("-"):
            return -int(s[1:], base), True
        return int(s, base), True
    except ValueError:
        err_out.extend(encode(f"printf: {arg}: invalid number\n"))
        return 0, False


def _format_one(
    spec: re.Match[str],
    consume: list[str],
    err_out: bytearray,
) -> tuple[bytes, bool]:
    # Returns (rendered_bytes, success).
    flags = spec.group("flags") or ""
    width_s = spec.group("width")
    prec_s = spec.group("prec")
    conv = spec.group("conv")

    width: int | None = None
    if width_s == "*":
        if consume:
            arg = consume.pop(0)
            n, _ = _to_int(arg, err_out)
            width = n
    elif width_s:
        width = int(width_s)

    precision: int | None = None
    if prec_s == "*":
        if consume:
            arg = consume.pop(0)
            n, _ = _to_int(arg, err_out)
            precision = n
    elif prec_s is not None:
        precision = int(prec_s)

    if conv == "%":
        return b"%", True

    if conv == "s":
        if not consume:
            arg = ""
        else:
            arg = consume.pop(0)
        if precision is not None:
            arg = arg[:precision]
        if width is not None:
            if "-" in flags:
                arg = arg.ljust(width)
            else:
                arg = arg.rjust(width)
        return arg.encode("utf-8"), True

    if conv == "b":
        if not consume:
            arg = ""
        else:
            arg = consume.pop(0)
        rendered = _interpret_b_arg(arg)
        return rendered, True

    if conv == "q":
        if not consume:
            arg = ""
        else:
            arg = consume.pop(0)
        return _shell_quote(arg).encode("utf-8"), True

    if conv == "c":
        if not consume:
            return b"", True
        arg = consume.pop(0)
        if not arg:
            return b"", True
        return arg[0].encode("utf-8"), True

    if conv in ("d", "i", "o", "x", "X"):
        if not consume:
            n = 0
        else:
            arg = consume.pop(0)
            n, _ = _to_int(arg, err_out)
        if conv in ("d", "i"):
            body = str(abs(n))
            sign = "-" if n < 0 else ("+" if "+" in flags else (" " if " " in flags else ""))
        elif conv == "o":
            body = format(abs(n), "o")
            sign = "-" if n < 0 else ""
        elif conv == "x":
            body = format(abs(n), "x")
            sign = "-" if n < 0 else ""
        else:  # "X"
            body = format(abs(n), "X")
            sign = "-" if n < 0 else ""

        if precision is not None and len(body) < precision:
            body = body.zfill(precision)
        text = sign + body
        if width is not None and len(text) < width:
            if "-" in flags:
                text = text.ljust(width)
            elif "0" in flags and precision is None:
                pad = "0" * (width - len(text))
                if sign and not body.startswith("0" * 9999):  # always
                    text = sign + pad + body
                else:
                    text = pad + text
            else:
                text = text.rjust(width)
        return text.encode("ascii"), True

    return b"", True


def _expand_format(fmt_bytes: bytes, args: list[str], err_out: bytearray) -> tuple[bytes, int]:
    # Apply format once, consuming as many args as needed. Return rendered bytes
    # and the number of placeholders the format had (used for reuse logic).
    text = fmt_bytes.decode("utf-8", errors="surrogateescape")
    out = bytearray()
    placeholders = 0
    i = 0
    consume = args
    while i < len(text):
        ch = text[i]
        if ch != "%":
            out.append(ord(ch) if ord(ch) < 128 else 0)
            if ord(ch) >= 128:
                out.pop()
                out.extend(ch.encode("utf-8"))
            i += 1
            continue
        m = _SPEC_RE.match(text, i)
        if m is None:
            # Stray %: emit literally.
            out.extend(b"%")
            i += 1
            continue
        if m.group("conv") != "%":
            placeholders += 1
        rendered, _ok = _format_one(m, consume, err_out)
        out.extend(rendered)
        i = m.end()
    return bytes(out), placeholders


@register("printf")
async def cmd_printf(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    if not args:
        return fail(2, _USAGE_ERROR)

    # Strip a leading '--' separator if present.
    if args[0] == "--":
        args = args[1:]
        if not args:
            return fail(2, _USAGE_ERROR)

    fmt_arg = args[0]
    rest = list(args[1:])

    fmt_bytes, terminated = _interpret_format_escapes(fmt_arg)
    if terminated:
        return CommandResult(stdout=fmt_bytes, stderr=b"", exit_code=0)

    err_out = bytearray()
    out = bytearray()

    if not rest:
        rendered, _placeholders = _expand_format(fmt_bytes, [], err_out)
        out.extend(rendered)
    else:
        consume = rest
        # First pass: always render once.
        first_render, placeholders = _expand_format(fmt_bytes, consume, err_out)
        out.extend(first_render)
        # Reuse format while args remain AND format had at least one placeholder.
        if placeholders > 0:
            while consume:
                err_for_pass = bytearray()
                rendered, _p = _expand_format(fmt_bytes, consume, err_for_pass)
                out.extend(rendered)
                err_out.extend(err_for_pass)

    exit_code = 1 if err_out else 0
    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
