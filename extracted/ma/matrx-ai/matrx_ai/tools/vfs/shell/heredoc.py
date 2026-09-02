from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class HeredocSpec:
    op: str  # "<<" or "<<-"
    terminator_raw: str  # terminator as it appeared (may include quotes)
    terminator: str  # cleaned (quotes removed)
    quoted: bool  # True if terminator was quoted/escaped => no expansion
    body: str  # collected body text (with trailing newline preserved)


@dataclass(slots=True)
class HeredocPreprocessResult:
    cleaned_source: str
    heredocs: list[HeredocSpec]


def _strip_terminator_quotes(raw: str) -> tuple[str, bool]:
    s = raw.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1], True
    if "\\" in s:
        return s.replace("\\", ""), True
    return s, False


def _scan_quotes(line: str, start: int) -> int:
    # given line[start] is a quote/dollar opener, return position after the
    # matching close. Handles: ' " $( ` only enough to skip << inside them.
    i = start
    n = len(line)
    if i >= n:
        return i
    ch = line[i]
    if ch == "'":
        i += 1
        while i < n and line[i] != "'":
            i += 1
        return min(i + 1, n)
    if ch == '"':
        i += 1
        while i < n:
            if line[i] == "\\" and i + 1 < n:
                i += 2
                continue
            if line[i] == '"':
                return i + 1
            i += 1
        return n
    if ch == "$" and i + 1 < n and line[i + 1] == "(":
        depth = 1
        i += 2
        while i < n and depth:
            c = line[i]
            if c == "\\" and i + 1 < n:
                i += 2
                continue
            if c == "'" or c == '"' or (c == "$" and i + 1 < n and line[i + 1] == "("):
                i = _scan_quotes(line, i)
                continue
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            i += 1
        return i
    if ch == "`":
        i += 1
        while i < n:
            if line[i] == "\\" and i + 1 < n:
                i += 2
                continue
            if line[i] == "`":
                return i + 1
            i += 1
        return n
    return i + 1


def _find_heredoc_ops_in_line(line: str) -> list[tuple[int, str, str, int]]:
    # Returns list of (op_start, op, raw_terminator, end_pos_after_terminator).
    out: list[tuple[int, str, str, int]] = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch in ("'", '"', "`"):
            i = _scan_quotes(line, i)
            continue
        if ch == "$" and i + 1 < n and line[i + 1] == "(":
            i = _scan_quotes(line, i)
            continue
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break  # rest is comment
        if ch == "<" and i + 1 < n and line[i + 1] == "<":
            # not <<<
            if i + 2 < n and line[i + 2] == "<":
                i += 3
                continue
            op = "<<"
            j = i + 2
            if j < n and line[j] == "-":
                op = "<<-"
                j += 1
            while j < n and line[j] in " \t":
                j += 1
            term_start = j
            term_end = j
            while term_end < n:
                c = line[term_end]
                if c in " \t;|&()<>":
                    break
                if c in ("'", '"'):
                    term_end = _scan_quotes(line, term_end)
                    continue
                if c == "\\" and term_end + 1 < n:
                    term_end += 2
                    continue
                term_end += 1
            if term_end == term_start:
                # malformed — skip
                i = j
                continue
            out.append((i, op, line[term_start:term_end], term_end))
            i = term_end
            continue
        i += 1
    return out


def preprocess(source: str) -> HeredocPreprocessResult:
    lines = source.split("\n")
    out_lines: list[str] = []
    heredocs: list[HeredocSpec] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        ops = _find_heredoc_ops_in_line(line)
        out_lines.append(line)
        i += 1
        for _op_start, op, raw_term, _end in ops:
            terminator, quoted = _strip_terminator_quotes(raw_term)
            body_lines: list[str] = []
            while i < len(lines):
                bl = lines[i]
                check = bl.lstrip("\t") if op == "<<-" else bl
                if check == terminator:
                    i += 1
                    break
                body_lines.append(bl.lstrip("\t") if op == "<<-" else bl)
                i += 1
            body = "\n".join(body_lines)
            if body_lines:
                body += "\n"
            heredocs.append(
                HeredocSpec(
                    op=op,
                    terminator_raw=raw_term,
                    terminator=terminator,
                    quoted=quoted,
                    body=body,
                )
            )

    cleaned = "\n".join(out_lines)
    return HeredocPreprocessResult(cleaned_source=cleaned, heredocs=heredocs)
