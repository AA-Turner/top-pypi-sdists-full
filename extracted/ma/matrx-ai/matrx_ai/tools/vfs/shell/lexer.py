from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

TokenKind = Literal[
    "WORD",
    "ASSIGN_PREFIX",
    "OPERATOR",
    "NEWLINE",
    "EOF",
    "HEREDOC_BODY",
]


@dataclass(slots=True)
class Token:
    kind: TokenKind
    value: str
    pos: int
    quoted_segments: list[tuple[str, str]] | None = None
    # quoted_segments: optional list of (kind, text) where kind is one of
    # 'lit', 'sq', 'dq', 'esc' — used by the parser to know which parts of a
    # WORD came from quoted contexts. For most tokens this is None and the
    # parser falls back to scanning `value` directly.


class ShellSyntaxError(Exception):
    def __init__(self, message: str, position: int) -> None:
        super().__init__(message)
        self.message = message
        self.position = position


# Operators in priority order: longest first so multi-char ones win.
_OPERATORS = (
    "&&",
    "||",
    "<<<",
    "<<-",
    "<<",
    ">>",
    "&>>",
    "&>",
    "2>>",
    "2>",
    "|",
    "&",
    ";",
    "(",
    ")",
    "<",
    ">",
)

_NAME_FIRST = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
_NAME_REST = _NAME_FIRST + "0123456789"


def _is_name_start(ch: str) -> bool:
    return ch in _NAME_FIRST


def _is_name_rest(ch: str) -> bool:
    return ch in _NAME_REST


class _Lexer:
    __slots__ = ("src", "pos", "tokens")

    def __init__(self, src: str) -> None:
        self.src = src
        self.pos = 0
        self.tokens: list[Token] = []

    # --------------- helpers ---------------
    def _peek(self, offset: int = 0) -> str:
        p = self.pos + offset
        return self.src[p] if p < len(self.src) else ""

    def _starts_with(self, s: str) -> bool:
        return self.src.startswith(s, self.pos)

    def _match_operator(self) -> str | None:
        for op in _OPERATORS:
            if self._starts_with(op):
                # Special-case: digit before > or >> is an fd redirect, but
                # we already match 2> / 2>> explicitly. Plain '<' / '>' should
                # not absorb following '<<' etc. — handled by ordering.
                return op
        return None

    # --------------- segment readers ---------------
    def _read_single_quoted(self) -> tuple[str, str]:
        # caller already at the opening quote
        start = self.pos
        assert self.src[self.pos] == "'"
        self.pos += 1
        buf: list[str] = []
        while self.pos < len(self.src):
            ch = self.src[self.pos]
            if ch == "'":
                self.pos += 1
                return "".join(buf), "sq"
            buf.append(ch)
            self.pos += 1
        raise ShellSyntaxError("unmatched single quote", start)

    def _read_double_quoted(self) -> tuple[str, str]:
        start = self.pos
        assert self.src[self.pos] == '"'
        self.pos += 1
        buf: list[str] = []
        while self.pos < len(self.src):
            ch = self.src[self.pos]
            if ch == '"':
                self.pos += 1
                return "".join(buf), "dq"
            if ch == "\\":
                nxt = self._peek(1)
                # Inside double quotes, backslash only escapes: $ ` " \ <newline>
                if nxt in ('"', "$", "`", "\\"):
                    buf.append(nxt)
                    self.pos += 2
                    continue
                if nxt == "\n":
                    self.pos += 2
                    continue
                # Otherwise literal backslash retained
                buf.append(ch)
                self.pos += 1
                continue
            if ch == "$":
                # We need to preserve $... constructs verbatim, the parser
                # will reparse this segment for VarPart/CmdSubPart/ArithPart.
                seg = self._read_dollar_segment()
                buf.append(seg)
                continue
            if ch == "`":
                seg = self._read_backtick()
                buf.append(seg)
                continue
            buf.append(ch)
            self.pos += 1
        raise ShellSyntaxError("unmatched double quote", start)

    def _read_dollar_segment(self) -> str:
        # at '$'
        start = self.pos
        if self._peek(1) == "(":
            if self._peek(2) == "(":
                # arithmetic $((...))
                return self._read_arith()
            return self._read_cmdsub_paren()
        if self._peek(1) == "{":
            return self._read_brace_var()
        if self._peek(1) == "'":
            # ANSI-C quoting $'...'
            return self._read_ansi_c()
        # Plain $NAME or $X (single special char)
        self.pos += 1
        if self.pos >= len(self.src):
            return "$"
        ch = self.src[self.pos]
        if _is_name_start(ch):
            n_start = self.pos
            self.pos += 1
            while self.pos < len(self.src) and _is_name_rest(self.src[self.pos]):
                self.pos += 1
            return "$" + self.src[n_start : self.pos]
        if ch in "?$!#@*-" or ch.isdigit():
            self.pos += 1
            return "$" + ch
        # bare $ — return literal
        return self.src[start : self.pos]

    def _read_brace_var(self) -> str:
        # at '${'
        start = self.pos
        self.pos += 2
        depth = 1
        buf: list[str] = ["${"]
        while self.pos < len(self.src) and depth:
            ch = self.src[self.pos]
            if ch == "{":
                depth += 1
                buf.append(ch)
                self.pos += 1
            elif ch == "}":
                depth -= 1
                buf.append(ch)
                self.pos += 1
            elif ch == "\\":
                buf.append(ch)
                if self._peek(1):
                    buf.append(self._peek(1))
                    self.pos += 2
                else:
                    self.pos += 1
            elif ch == "'":
                # literal-only inside braces
                q, _ = self._read_single_quoted()
                buf.append("'")
                buf.append(q)
                buf.append("'")
            elif ch == '"':
                q, _ = self._read_double_quoted()
                buf.append('"')
                buf.append(q)
                buf.append('"')
            elif ch == "$":
                buf.append(self._read_dollar_segment())
            else:
                buf.append(ch)
                self.pos += 1
        if depth:
            raise ShellSyntaxError("unmatched ${", start)
        return "".join(buf)

    def _read_cmdsub_paren(self) -> str:
        # at '$('
        start = self.pos
        self.pos += 2
        depth = 1
        buf: list[str] = ["$("]
        while self.pos < len(self.src) and depth:
            ch = self.src[self.pos]
            if ch == "(":
                depth += 1
                buf.append(ch)
                self.pos += 1
            elif ch == ")":
                depth -= 1
                buf.append(ch)
                self.pos += 1
                if depth == 0:
                    break
            elif ch == "'":
                q, _ = self._read_single_quoted()
                buf.append("'")
                buf.append(q)
                buf.append("'")
            elif ch == '"':
                q, _ = self._read_double_quoted()
                buf.append('"')
                buf.append(q)
                buf.append('"')
            elif ch == "\\":
                buf.append(ch)
                if self._peek(1):
                    buf.append(self._peek(1))
                    self.pos += 2
                else:
                    self.pos += 1
            elif ch == "`":
                buf.append(self._read_backtick())
            elif ch == "$":
                buf.append(self._read_dollar_segment())
            else:
                buf.append(ch)
                self.pos += 1
        if depth:
            raise ShellSyntaxError("unmatched $(", start)
        return "".join(buf)

    def _read_arith(self) -> str:
        # at '$(('
        start = self.pos
        self.pos += 3
        depth = 2  # two open parens
        buf: list[str] = ["$(("]
        while self.pos < len(self.src):
            ch = self.src[self.pos]
            if ch == "(":
                depth += 1
                buf.append(ch)
                self.pos += 1
            elif ch == ")":
                depth -= 1
                buf.append(ch)
                self.pos += 1
                if depth == 0:
                    return "".join(buf)
            elif ch == "\\":
                buf.append(ch)
                if self._peek(1):
                    buf.append(self._peek(1))
                    self.pos += 2
                else:
                    self.pos += 1
            elif ch == "$":
                buf.append(self._read_dollar_segment())
            else:
                buf.append(ch)
                self.pos += 1
        raise ShellSyntaxError("unmatched $((", start)

    def _read_backtick(self) -> str:
        # at '`'
        start = self.pos
        self.pos += 1
        buf: list[str] = ["`"]
        while self.pos < len(self.src):
            ch = self.src[self.pos]
            if ch == "`":
                self.pos += 1
                buf.append("`")
                return "".join(buf)
            if ch == "\\":
                nxt = self._peek(1)
                if nxt in ("`", "$", "\\"):
                    buf.append(nxt)
                    self.pos += 2
                    continue
                buf.append(ch)
                self.pos += 1
                continue
            buf.append(ch)
            self.pos += 1
        raise ShellSyntaxError("unmatched backtick", start)

    def _read_ansi_c(self) -> str:
        # at "$'"
        start = self.pos
        self.pos += 2
        buf: list[str] = ["$'"]
        while self.pos < len(self.src):
            ch = self.src[self.pos]
            if ch == "'":
                self.pos += 1
                buf.append("'")
                return "".join(buf)
            if ch == "\\":
                buf.append(ch)
                if self._peek(1):
                    buf.append(self._peek(1))
                    self.pos += 2
                else:
                    self.pos += 1
            else:
                buf.append(ch)
                self.pos += 1
        raise ShellSyntaxError("unmatched $'", start)

    def _read_paren_subshell_word(self) -> str:
        # Process substitution <(...) >(...) — we don't support these. Surface
        # the raw text and let the executor produce an EFAULT-style error.
        # The parser will treat this as a literal word part to keep tests
        # for unrelated syntax working.
        start = self.pos
        self.pos += 1  # skip '<' or '>'
        if self._peek() != "(":
            self.pos = start
            return ""
        self.pos += 1
        depth = 1
        buf: list[str] = []
        while self.pos < len(self.src) and depth:
            ch = self.src[self.pos]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    self.pos += 1
                    break
            buf.append(ch)
            self.pos += 1
        return self.src[start : self.pos]

    # --------------- main loop ---------------
    def tokenize(self) -> list[Token]:
        while self.pos < len(self.src):
            ch = self.src[self.pos]

            # whitespace (not newline)
            if ch in " \t":
                self.pos += 1
                continue

            # line continuation
            if ch == "\\" and self._peek(1) == "\n":
                self.pos += 2
                continue

            # comment
            if ch == "#":
                # Comments only start at the beginning of a token (i.e., after
                # whitespace or operator), not in the middle of a word.
                # If previous token was a WORD/ASSIGN_PREFIX with no
                # whitespace, the '#' is part of the word — but our flow
                # only enters here at top level (between tokens), so it's
                # always safe to treat as a comment.
                while self.pos < len(self.src) and self.src[self.pos] != "\n":
                    self.pos += 1
                continue

            # newline
            if ch == "\n":
                self.tokens.append(Token("NEWLINE", "\n", self.pos))
                self.pos += 1
                continue

            # operator?
            op = self._match_operator()
            if op is not None:
                self.tokens.append(Token("OPERATOR", op, self.pos))
                self.pos += len(op)
                continue

            # numeric fd prefix? (e.g., 2>foo handled above by _OPERATORS,
            # but `1>foo` `3>foo` aren't in operators — handle here)
            if ch.isdigit():
                save = self.pos
                # Look for digits followed immediately by > or >>
                p = self.pos
                while p < len(self.src) and self.src[p].isdigit():
                    p += 1
                if p < len(self.src) and self.src[p] in (">", "<"):
                    if self.src[p] == ">":
                        if p + 1 < len(self.src) and self.src[p + 1] == ">":
                            value = self.src[self.pos : p + 2]
                            self.tokens.append(Token("OPERATOR", value, self.pos))
                            self.pos = p + 2
                            continue
                        value = self.src[self.pos : p + 1]
                        self.tokens.append(Token("OPERATOR", value, self.pos))
                        self.pos = p + 1
                        continue
                    if self.src[p] == "<":
                        value = self.src[self.pos : p + 1]
                        self.tokens.append(Token("OPERATOR", value, self.pos))
                        self.pos = p + 1
                        continue
                self.pos = save  # fall through to word

            # word
            self._read_word()

        self.tokens.append(Token("EOF", "", self.pos))
        return self.tokens

    def _read_word(self) -> None:
        start = self.pos
        segments: list[tuple[str, str]] = []
        buf: list[str] = []

        def flush_lit() -> None:
            if buf:
                segments.append(("lit", "".join(buf)))
                buf.clear()

        # Scan a single word until whitespace, newline, or operator boundary.
        while self.pos < len(self.src):
            ch = self.src[self.pos]
            if ch in " \t\n":
                break
            if ch == "\\" and self._peek(1) == "\n":
                self.pos += 2
                continue
            if ch == "\\":
                nxt = self._peek(1)
                if nxt:
                    flush_lit()
                    segments.append(("esc", nxt))
                    self.pos += 2
                else:
                    self.pos += 1
                continue
            if ch == "'":
                flush_lit()
                text, _ = self._read_single_quoted()
                segments.append(("sq", text))
                continue
            if ch == '"':
                flush_lit()
                text, _ = self._read_double_quoted()
                segments.append(("dq", text))
                continue
            if ch == "$":
                flush_lit()
                seg = self._read_dollar_segment()
                segments.append(("dollar", seg))
                continue
            if ch == "`":
                flush_lit()
                seg = self._read_backtick()
                segments.append(("dollar", seg))
                continue
            # operator boundaries
            if self._match_operator() is not None:
                break
            # numeric fd? Only at start of a word
            if ch == "#" and self.pos == start:
                # comment — but we shouldn't reach here since '#' is handled
                # at the top level. If we got here mid-word it's a literal '#'.
                pass
            buf.append(ch)
            self.pos += 1

        flush_lit()
        value = self.src[start : self.pos]

        # Detect ASSIGN_PREFIX: NAME=... where NAME is unquoted at start.
        # The '=' must come from a literal segment (not from inside quotes).
        if segments and segments[0][0] == "lit":
            lit = segments[0][1]
            eq_idx = lit.find("=")
            if eq_idx > 0 and self._is_valid_name(lit[:eq_idx]):
                # ASSIGN_PREFIX takes the entire word; downstream parser
                # decides whether it stays a prefix or becomes plain WORD.
                self.tokens.append(Token("ASSIGN_PREFIX", value, start, quoted_segments=segments))
                return

        self.tokens.append(Token("WORD", value, start, quoted_segments=segments))

    @staticmethod
    def _is_valid_name(s: str) -> bool:
        if not s:
            return False
        if not _is_name_start(s[0]):
            return False
        return all(_is_name_rest(c) for c in s[1:])


def tokenize(src: str) -> list[Token]:
    return _Lexer(src).tokenize()
