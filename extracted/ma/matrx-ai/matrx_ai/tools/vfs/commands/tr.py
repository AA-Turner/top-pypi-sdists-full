from __future__ import annotations

import string

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


_CHAR_CLASSES: dict[str, str] = {
    "alpha": string.ascii_letters,
    "digit": string.digits,
    "upper": string.ascii_uppercase,
    "lower": string.ascii_lowercase,
    "alnum": string.ascii_letters + string.digits,
    "space": " \t\n\r\v\f",
    "blank": " \t",
    "punct": string.punctuation,
    "cntrl": "".join(chr(i) for i in range(32)) + chr(127),
    "print": "".join(chr(i) for i in range(32, 127)),
    "graph": "".join(chr(i) for i in range(33, 127)),
    "xdigit": string.hexdigits,
}


def _missing_operand() -> bytes:
    return encode("tr: missing operand\nTry 'tr --help' for more information.\n")


def _extra_operand(arg: str) -> bytes:
    return encode(f"tr: extra operand '{arg}'\nTry 'tr --help' for more information.\n")


def _parse_set(spec: str) -> str:
    out: list[str] = []
    i = 0
    chars: list[str] = []
    while i < len(spec):
        ch = spec[i]
        if ch == "\\" and i + 1 < len(spec):
            nxt = spec[i + 1]
            if nxt == "n":
                chars.append("\n")
                i += 2
                continue
            if nxt == "t":
                chars.append("\t")
                i += 2
                continue
            if nxt == "r":
                chars.append("\r")
                i += 2
                continue
            if nxt == "\\":
                chars.append("\\")
                i += 2
                continue
            if nxt == "0":
                chars.append("\x00")
                i += 2
                continue
            if nxt.isdigit():
                # Octal up to 3 digits.
                j = i + 1
                end = min(i + 4, len(spec))
                while j < end and spec[j].isdigit() and spec[j] in "01234567":
                    j += 1
                chars.append(chr(int(spec[i + 1 : j], 8)))
                i = j
                continue
            chars.append(nxt)
            i += 2
            continue
        if ch == "[" and i + 1 < len(spec) and spec[i + 1] == ":":
            # [:class:]
            close = spec.find(":]", i + 2)
            if close != -1:
                cls_name = spec[i + 2 : close]
                if cls_name in _CHAR_CLASSES:
                    chars.extend(_CHAR_CLASSES[cls_name])
                    i = close + 2
                    continue
        chars.append(ch)
        i += 1

    # Expand ranges (a-b) on the parsed character list.
    j = 0
    while j < len(chars):
        if j + 2 < len(chars) and chars[j + 1] == "-":
            start = chars[j]
            end = chars[j + 2]
            if ord(start) <= ord(end):
                out.extend(chr(c) for c in range(ord(start), ord(end) + 1))
                j += 3
                continue
        out.append(chars[j])
        j += 1
    return "".join(out)


def _complement(set_chars: str) -> str:
    in_set = set(set_chars)
    return "".join(chr(c) for c in range(256) if chr(c) not in in_set)


@register("tr")
async def cmd_tr(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    delete = False
    squeeze = False
    complement = False
    truncate = False
    positional: list[str] = []

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            positional.extend(args[i + 1 :])
            break
        if a == "--delete":
            delete = True
            i += 1
            continue
        if a == "--squeeze-repeats":
            squeeze = True
            i += 1
            continue
        if a == "--complement":
            complement = True
            i += 1
            continue
        if a == "--truncate-set1":
            truncate = True
            i += 1
            continue
        if a.startswith("-") and len(a) > 1 and not a[1:].lstrip("-").isdigit() and a != "-":
            # Short flags - but allow "-" as positional placeholder if needed.
            for letter in a[1:]:
                if letter == "d":
                    delete = True
                elif letter == "s":
                    squeeze = True
                elif letter == "c" or letter == "C":
                    complement = True
                elif letter == "t":
                    truncate = True
                else:
                    return fail(
                        1,
                        encode(
                            f"tr: invalid option -- '{letter}'\n"
                            "Try 'tr --help' for more information.\n"
                        ),
                    )
            i += 1
            continue
        positional.append(a)
        i += 1

    if not positional:
        return fail(1, _missing_operand())

    set1 = _parse_set(positional[0])
    set2 = _parse_set(positional[1]) if len(positional) >= 2 else ""

    if delete:
        if len(positional) > 2:
            return fail(1, _extra_operand(positional[2]))
        if not squeeze and len(positional) >= 2:
            # tr -d SET1 SET2 only valid with -s
            return fail(1, _extra_operand(positional[1]))
    else:
        if len(positional) < 2 and not squeeze:
            return fail(
                1,
                encode(
                    "tr: missing operand after '"
                    + positional[0]
                    + "'\nTwo strings must be given when translating.\n"
                ),
            )
        if len(positional) > 2:
            return fail(1, _extra_operand(positional[2]))

    if complement:
        set1 = _complement(set1)

    data = ctx.stdin
    text = data.decode("latin-1")

    if delete:
        del_set = set(set1)
        text = "".join(c for c in text if c not in del_set)
        if squeeze and len(positional) >= 2:
            sq_set = set(set2)
            text = _squeeze(text, sq_set)
    else:
        if len(positional) >= 2:
            # Build mapping from set1 -> set2. Pad set2 (with last char) unless
            # truncate is set, in which case set1 is truncated to len(set2).
            if truncate and len(set1) > len(set2):
                set1 = set1[: len(set2)]
            mapping: dict[str, str] = {}
            if set2:
                for idx, c in enumerate(set1):
                    if idx < len(set2):
                        mapping[c] = set2[idx]
                    else:
                        mapping[c] = set2[-1]
            text = "".join(mapping.get(c, c) for c in text)
            if squeeze:
                sq_set = set(set2)
                text = _squeeze(text, sq_set)
        elif squeeze:
            sq_set = set(set1)
            text = _squeeze(text, sq_set)

    return ok(text.encode("latin-1"))


def _squeeze(text: str, chars: set[str]) -> str:
    if not chars:
        return text
    out: list[str] = []
    prev: str | None = None
    for c in text:
        if c in chars and prev == c:
            continue
        out.append(c)
        prev = c
    return "".join(out)
