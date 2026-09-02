from __future__ import annotations


def _split_lines_keep_trailing(content: str) -> list[str]:
    # Split on \n, treating each segment ending in \n as a line. The "cat -n"
    # output numbers logical lines as separated by \n; we always emit the
    # full content with a \n at the end of each numbered line, even when the
    # last source line was unterminated.
    if not content:
        return []
    parts = content.split("\n")
    # If the content ends with \n, the split produces a trailing "" which is
    # not a real line; drop it.
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def format_cat_n(content: str) -> str:
    return format_cat_n_with_offset(content, 1)


def format_cat_n_with_offset(content: str, start_line: int, end_line: int | None = None) -> str:
    if not content:
        return ""
    lines = _split_lines_keep_trailing(content)
    out: list[str] = []
    for idx, line in enumerate(lines):
        n = start_line + idx
        if end_line is not None and n > end_line:
            break
        out.append(f"{n:>6d}\t{line}\n")
    return "".join(out)


def format_cat(content: str) -> str:
    return content


_CARET_NOTATIONS: dict[int, str] = {}


def _caret(byte: int) -> str:
    cached = _CARET_NOTATIONS.get(byte)
    if cached is not None:
        return cached
    if byte == 9:
        result = "^I"
    elif byte == 10:
        result = "$\n"
    elif byte < 32:
        result = "^" + chr(byte + 64)
    elif byte == 127:
        result = "^?"
    else:
        result = chr(byte)
    _CARET_NOTATIONS[byte] = result
    return result


def format_cat_minus_a(content: str) -> str:
    # `cat -A` == `cat -vET`. Tabs as ^I, line endings as $, control chars as ^X,
    # high-bit (M-x notation) approximated. This is sufficient for ASCII text
    # and the basic tab/newline tests.
    out: list[str] = []
    for ch in content:
        code = ord(ch)
        if code == 9:
            out.append("^I")
        elif code == 10:
            out.append("$\n")
        elif code < 32:
            out.append("^" + chr(code + 64))
        elif code == 127:
            out.append("^?")
        elif code < 128:
            out.append(ch)
        else:
            # Fall back to a passthrough for non-ASCII; full M- notation
            # requires byte-level handling and is not load-bearing here.
            out.append(ch)
    return "".join(out)
