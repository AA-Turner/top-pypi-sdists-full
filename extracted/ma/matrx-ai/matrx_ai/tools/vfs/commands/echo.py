from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _is_flag(arg: str) -> bool:
    if not arg.startswith("-") or len(arg) < 2:
        return False
    for ch in arg[1:]:
        if ch not in ("n", "e", "E"):
            return False
    return True


def _interpret(text: str) -> tuple[bytes, bool]:
    # Returns (bytes, terminated_early). Terminated early when \c is seen.
    out = bytearray()
    i = 0
    while i < len(text):
        ch = text[i]
        if ch != "\\" or i + 1 >= len(text):
            out.append(ord(ch) if ord(ch) < 128 else 0)
            if ord(ch) >= 128:
                # encode multi-byte
                out.pop()
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
        elif nxt == "0":
            # \0NNN: up to 3 octal digits after the 0.
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
    return bytes(out), False


@register("echo")
async def cmd_echo(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    suppress_newline = False
    interpret_escapes = False

    i = 0
    while i < len(args) and _is_flag(args[i]):
        for ch in args[i][1:]:
            if ch == "n":
                suppress_newline = True
            elif ch == "e":
                interpret_escapes = True
            elif ch == "E":
                interpret_escapes = False
        i += 1

    payload_args = args[i:]

    out = bytearray()
    terminated_early = False
    for j, a in enumerate(payload_args):
        if interpret_escapes:
            chunk, term = _interpret(a)
            out.extend(chunk)
            if term:
                terminated_early = True
                break
        else:
            out.extend(a.encode("utf-8"))
        if j < len(payload_args) - 1:
            out.append(0x20)

    if not suppress_newline and not terminated_early:
        out.append(0x0A)

    return ok(bytes(out))
