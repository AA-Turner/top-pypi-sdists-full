from __future__ import annotations

from collections import deque
from typing import cast

from .ast import (
    AndOrList,
    ArithPart,
    CmdSubPart,
    CommandList,
    GlobPart,
    LiteralPart,
    Pipeline,
    Redirect,
    Separator,
    SimpleCommand,
    Subshell,
    TildePart,
    VarPart,
    Word,
    WordPart,
)
from .heredoc import HeredocSpec, preprocess
from .lexer import ShellSyntaxError, Token, tokenize


class ShellParseError(Exception):
    def __init__(self, message: str, position: int) -> None:
        super().__init__(message)
        self.message = message
        self.position = position


_REDIR_OPS = {">", ">>", "<", "2>", "2>>", "&>", "&>>", "<<<", "<<", "<<-"}

# Sentinel LiteralPart instances used as dq boundary markers. The expansion
# pass recognizes these by identity and emits paired _QUOTED_OPEN/_QUOTED_CLOSE
# markers around the spanned content.
_DQ_OPEN = LiteralPart(text="\x04DQ_OPEN\x04", quoted=True)
_DQ_CLOSE = LiteralPart(text="\x04DQ_CLOSE\x04", quoted=True)
_FD_REDIR_PREFIXES = ("0<", "1>", "1>>", "3>", "3>>", "4>", "4>>", "5>", "5>>")


def _is_redirect_op(op: str) -> bool:
    if op in _REDIR_OPS:
        return True
    # numeric fd redirects like 1>, 1>>, 3>foo, etc.
    j = 0
    while j < len(op) and op[j].isdigit():
        j += 1
    if j == 0:
        return False
    rest = op[j:]
    return rest in (">", ">>", "<", "<<")


def _parse_redirect_op(op: str) -> tuple[str, int | None]:
    # Returns (canonical_op, fd_override).
    if op in _REDIR_OPS:
        return op, None
    j = 0
    while j < len(op) and op[j].isdigit():
        j += 1
    fd = int(op[:j])
    rest = op[j:]
    return rest, fd


class _Parser:
    __slots__ = ("tokens", "pos", "heredocs", "_hd_idx")

    def __init__(self, tokens: list[Token], heredocs: list[HeredocSpec]) -> None:
        self.tokens = tokens
        self.pos = 0
        self.heredocs: deque[HeredocSpec] = deque(heredocs)
        self._hd_idx = 0

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[idx]

    def _consume(self) -> Token:
        tok = self.tokens[self.pos]
        if tok.kind != "EOF":
            self.pos += 1
        return tok

    def _eat_newlines(self) -> None:
        while self._peek().kind == "NEWLINE":
            self.pos += 1

    def _at_eof(self) -> bool:
        return self._peek().kind == "EOF"

    # ---------- entry ----------
    def parse(self) -> CommandList:
        self._eat_newlines()
        if self._at_eof():
            return CommandList(items=[], separators=[])
        cl = self._parse_command_list(stop_ops=())
        self._eat_newlines()
        if not self._at_eof():
            tok = self._peek()
            raise ShellParseError(f"unexpected token '{tok.value}'", tok.pos)
        return cl

    # ---------- grammar ----------
    def _parse_command_list(self, stop_ops: tuple[str, ...]) -> CommandList:
        items: list[AndOrList] = []
        seps: list[Separator] = []
        first = self._parse_andor()
        items.append(first)
        while True:
            tok = self._peek()
            if tok.kind == "OPERATOR" and tok.value in (";", "&"):
                self._consume()
                seps.append(cast(Separator, tok.value))
            elif tok.kind == "NEWLINE":
                self._consume()
                seps.append(cast(Separator, "\n"))
            else:
                break
            # allow trailing separators
            self._eat_newlines()
            if self._at_eof() or (
                self._peek().kind == "OPERATOR" and self._peek().value in stop_ops
            ):
                break
            nxt = self._parse_andor()
            items.append(nxt)
        return CommandList(items=items, separators=seps)

    def _parse_andor(self) -> AndOrList:
        first = self._parse_pipeline()
        pipelines = [first]
        ops: list[str] = []
        while True:
            tok = self._peek()
            if tok.kind == "OPERATOR" and tok.value in ("&&", "||"):
                self._consume()
                self._eat_newlines()
                nxt = self._parse_pipeline()
                pipelines.append(nxt)
                ops.append(tok.value)
            else:
                break
        return AndOrList(pipelines=pipelines, operators=cast(list, ops))

    def _parse_pipeline(self) -> Pipeline:
        negated = False
        tok = self._peek()
        if tok.kind == "WORD" and tok.value == "!":
            self._consume()
            negated = True
            self._eat_newlines()
        first = self._parse_command()
        commands: list[SimpleCommand | Subshell] = [first]
        while True:
            tok = self._peek()
            if tok.kind == "OPERATOR" and tok.value == "|":
                self._consume()
                self._eat_newlines()
                nxt = self._parse_command()
                commands.append(nxt)
            else:
                break
        return Pipeline(commands=commands, negated=negated)

    def _parse_command(self) -> SimpleCommand | Subshell:
        tok = self._peek()
        if tok.kind == "OPERATOR" and tok.value == "(":
            return self._parse_subshell()
        return self._parse_simple_command()

    def _parse_subshell(self) -> Subshell:
        open_tok = self._consume()
        if open_tok.value != "(":
            raise ShellParseError("expected '('", open_tok.pos)
        self._eat_newlines()
        body = self._parse_command_list(stop_ops=(")",))
        self._eat_newlines()
        close = self._peek()
        if close.kind != "OPERATOR" or close.value != ")":
            raise ShellParseError(f"expected ')', got '{close.value}'", close.pos)
        self._consume()
        # optional redirects after subshell
        redirects = self._collect_redirects()
        return Subshell(body=body, redirects=redirects)

    def _parse_simple_command(self) -> SimpleCommand:
        assignments: list[tuple[str, Word]] = []
        argv: list[Word] = []
        redirects: list[Redirect] = []

        # Phase 1: optional ASSIGN_PREFIX tokens before any WORD/argv.
        while True:
            tok = self._peek()
            if tok.kind == "ASSIGN_PREFIX":
                self._consume()
                name, value_word = self._split_assignment(tok)
                assignments.append((name, value_word))
                continue
            break

        # Phase 2: collect WORDs, redirects, and bare ASSIGN_PREFIXes
        # interleaved. After we see a WORD, ASSIGN_PREFIXes become regular
        # words.
        seen_word = False
        while True:
            tok = self._peek()
            if tok.kind == "WORD":
                self._consume()
                argv.append(self._token_to_word(tok))
                seen_word = True
                continue
            if tok.kind == "ASSIGN_PREFIX":
                if not seen_word:
                    self._consume()
                    name, value_word = self._split_assignment(tok)
                    assignments.append((name, value_word))
                    continue
                self._consume()
                argv.append(self._token_to_word(tok))
                continue
            if tok.kind == "OPERATOR" and _is_redirect_op(tok.value):
                redirects.append(self._parse_redirect())
                continue
            break

        if not argv and not assignments and not redirects:
            tok = self._peek()
            raise ShellParseError(f"unexpected token '{tok.value}'", tok.pos)

        return SimpleCommand(assignments=assignments, argv=argv, redirects=redirects)

    def _collect_redirects(self) -> list[Redirect]:
        out: list[Redirect] = []
        while True:
            tok = self._peek()
            if tok.kind == "OPERATOR" and _is_redirect_op(tok.value):
                out.append(self._parse_redirect())
                continue
            break
        return out

    def _parse_redirect(self) -> Redirect:
        op_tok = self._consume()
        op_str, fd = _parse_redirect_op(op_tok.value)
        # set defaults
        if op_str in (">", ">>") and fd is None:
            fd = 1
        if op_str == "<" and fd is None:
            fd = 0
        if op_str in ("2>", "2>>"):
            fd = 2
        if op_str in ("&>", "&>>"):
            fd = None  # both stdout+stderr
        if op_str in ("<<", "<<-"):
            fd = 0
        if op_str == "<<<":
            fd = 0

        target_tok = self._peek()
        if target_tok.kind not in ("WORD", "ASSIGN_PREFIX"):
            raise ShellParseError(
                f"expected filename after '{op_tok.value}', got '{target_tok.value}'",
                target_tok.pos,
            )
        self._consume()
        target_word = self._token_to_word(target_tok)

        if op_str in ("<<", "<<-"):
            if not self.heredocs:
                raise ShellParseError("heredoc body missing", op_tok.pos)
            spec = self.heredocs.popleft()
            return Redirect(
                op=op_str,
                fd=fd,
                target=target_word,
                heredoc_body=spec.body,
                heredoc_quoted=spec.quoted,
                heredoc_strip_tabs=(op_str == "<<-"),
                heredoc_expand=not spec.quoted,
            )

        return Redirect(op=cast(str, op_str), fd=fd, target=target_word)

    # ---------- word construction ----------
    def _split_assignment(self, tok: Token) -> tuple[str, Word]:
        # tok.value looks like NAME=...
        segs = tok.quoted_segments or [("lit", tok.value)]
        first_kind, first_text = segs[0]
        eq = first_text.find("=")
        if first_kind != "lit" or eq < 0:
            raise ShellParseError(f"malformed assignment '{tok.value}'", tok.pos)
        name = first_text[:eq]
        rest_first = first_text[eq + 1 :]
        new_segs: list[tuple[str, str]] = []
        if rest_first:
            new_segs.append(("lit", rest_first))
        new_segs.extend(segs[1:])
        word = self._segments_to_word(new_segs, original_pos=tok.pos)
        return name, word

    def _token_to_word(self, tok: Token) -> Word:
        segs = tok.quoted_segments or [("lit", tok.value)]
        return self._segments_to_word(segs, original_pos=tok.pos)

    def _segments_to_word(self, segments: list[tuple[str, str]], *, original_pos: int) -> Word:
        parts: list[WordPart] = []
        first = True
        for kind, text in segments:
            if kind == "sq":
                parts.append(LiteralPart(text=text, quoted=True))
            elif kind == "esc":
                parts.append(LiteralPart(text=text, quoted=True))
            elif kind == "dq":
                # Mark dq boundaries via sentinel parts so expansion can
                # suppress word-splitting/globbing across the run AND still
                # produce one empty field for an empty quoted expansion.
                parts.append(_DQ_OPEN)
                parts.extend(self._parse_dq_content(text, pos=original_pos))
                parts.append(_DQ_CLOSE)
            elif kind == "lit":
                parts.extend(self._parse_lit_content(text, leading=first, pos=original_pos))
            elif kind == "dollar":
                parts.append(self._parse_dollar(text, pos=original_pos, quoted=False))
            else:
                parts.append(LiteralPart(text=text))
            first = False
        return Word(parts=parts)

    def _parse_lit_content(self, text: str, *, leading: bool, pos: int) -> list[WordPart]:
        # Literal text from outside quotes: handle ~ at start, glob chars,
        # and merge as LiteralPart otherwise.
        out: list[WordPart] = []
        i = 0
        n = len(text)
        if leading and n > 0 and text[0] == "~":
            # ~ or ~user/...
            j = 1
            while j < n and text[j] not in ("/", ":"):
                j += 1
            user = text[1:j] or None
            out.append(TildePart(user=user))
            i = j

        # Detect glob chars in the remaining literal — if we find any, the
        # WHOLE remaining literal becomes a GlobPart so wcmatch sees it
        # intact. Otherwise plain LiteralPart.
        rest = text[i:]
        if not rest:
            return out
        if any(c in "*?[" for c in rest):
            out.append(GlobPart(pattern=rest))
        else:
            out.append(LiteralPart(text=rest, quoted=False))
        return out

    def _parse_dq_content(self, text: str, *, pos: int) -> list[WordPart]:
        # Inside double-quotes: $... and `...` expand; glob doesn't.
        out: list[WordPart] = []
        i = 0
        n = len(text)
        buf: list[str] = []

        def flush() -> None:
            if buf:
                out.append(LiteralPart(text="".join(buf), quoted=True))
                buf.clear()

        while i < n:
            ch = text[i]
            if ch == "$":
                # find end of dollar segment
                seg, end = self._extract_dollar_segment(text, i)
                if seg is None:
                    buf.append(ch)
                    i += 1
                    continue
                flush()
                out.append(self._parse_dollar(seg, pos=pos, quoted=True))
                i = end
                continue
            if ch == "`":
                # find matching backtick
                end = i + 1
                while end < n:
                    if text[end] == "\\" and end + 1 < n:
                        end += 2
                        continue
                    if text[end] == "`":
                        break
                    end += 1
                if end >= n:
                    buf.append(ch)
                    i += 1
                    continue
                inner = text[i + 1 : end]
                flush()
                # parse inner as command
                inner_cl = parse(inner)
                out.append(CmdSubPart(command=inner_cl))
                i = end + 1
                continue
            buf.append(ch)
            i += 1
        flush()
        return out

    def _extract_dollar_segment(self, text: str, start: int) -> tuple[str | None, int]:
        # Mirror lexer._read_dollar_segment but operating on a string slice.
        n = len(text)
        if start + 1 >= n:
            return None, start + 1
        nxt = text[start + 1]
        if nxt == "(":
            if start + 2 < n and text[start + 2] == "(":
                # arithmetic
                depth = 2
                i = start + 3
                while i < n and depth:
                    c = text[i]
                    if c == "(":
                        depth += 1
                    elif c == ")":
                        depth -= 1
                        if depth == 0:
                            return text[start : i + 1], i + 1
                    elif c == "\\" and i + 1 < n:
                        i += 2
                        continue
                    i += 1
                return None, n
            depth = 1
            i = start + 2
            while i < n and depth:
                c = text[i]
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        return text[start : i + 1], i + 1
                elif c == "\\" and i + 1 < n:
                    i += 2
                    continue
                elif c == "'":
                    i += 1
                    while i < n and text[i] != "'":
                        i += 1
                    i = min(i + 1, n)
                    continue
                elif c == '"':
                    i += 1
                    while i < n:
                        if text[i] == "\\" and i + 1 < n:
                            i += 2
                            continue
                        if text[i] == '"':
                            break
                        i += 1
                    i = min(i + 1, n)
                    continue
                i += 1
            return None, n
        if nxt == "{":
            depth = 1
            i = start + 2
            while i < n and depth:
                c = text[i]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start : i + 1], i + 1
                elif c == "\\" and i + 1 < n:
                    i += 2
                    continue
                i += 1
            return None, n
        if nxt.isalpha() or nxt == "_":
            i = start + 2
            while i < n and (text[i].isalnum() or text[i] == "_"):
                i += 1
            return text[start:i], i
        if nxt.isdigit() or nxt in "?$!#@*-":
            return text[start : start + 2], start + 2
        return None, start + 1

    def _parse_dollar(self, seg: str, *, pos: int, quoted: bool) -> WordPart:
        # seg starts with $ or `. Returns one WordPart.
        if not seg:
            return LiteralPart(text="", quoted=quoted)
        if seg.startswith("`") and seg.endswith("`"):
            inner = seg[1:-1]
            return CmdSubPart(command=parse(inner))
        if seg.startswith("$((") and seg.endswith("))"):
            return ArithPart(expression=seg[3:-2])
        if seg.startswith("$(") and seg.endswith(")"):
            return CmdSubPart(command=parse(seg[2:-1]))
        if seg.startswith("${") and seg.endswith("}"):
            return _parse_brace_var(seg[2:-1])
        if seg.startswith("$") and len(seg) >= 2:
            return VarPart(name=seg[1:], mode="plain")
        return LiteralPart(text=seg, quoted=quoted)


def _parse_brace_var(inner: str) -> WordPart:
    # ${VAR}  ${VAR:-d}  ${VAR:=d}  ${VAR:?m}  ${VAR:+d}
    # ${#VAR}  ${VAR#pat} ${VAR##pat} ${VAR%pat} ${VAR%%pat}
    # ${VAR/pat/repl} ${VAR//pat/repl}
    if not inner:
        return LiteralPart(text="${}")
    if inner.startswith("#"):
        return VarPart(name=inner[1:], mode="length")
    # find first non-name char
    i = 0
    if inner[0] == "_" or inner[0].isalpha():
        i = 1
        while i < len(inner) and (inner[i].isalnum() or inner[i] == "_"):
            i += 1
    elif inner[0] in "?$!#@*-" or inner[0].isdigit():
        i = 1
    else:
        return LiteralPart(text="${" + inner + "}")
    name = inner[:i]
    rest = inner[i:]
    if not rest:
        return VarPart(name=name, mode="plain")
    if rest.startswith(":-"):
        return VarPart(name=name, default=rest[2:], mode="default")
    if rest.startswith("-"):
        return VarPart(name=name, default=rest[1:], mode="use_default")
    if rest.startswith(":="):
        return VarPart(name=name, default=rest[2:], mode="assign")
    if rest.startswith(":?"):
        return VarPart(name=name, default=rest[2:], mode="error")
    if rest.startswith(":+"):
        return VarPart(name=name, default=rest[2:], mode="alt")
    if rest.startswith("##"):
        return VarPart(name=name, default=rest[2:], mode="prefix_long")
    if rest.startswith("#"):
        return VarPart(name=name, default=rest[1:], mode="prefix")
    if rest.startswith("%%"):
        return VarPart(name=name, default=rest[2:], mode="suffix_long")
    if rest.startswith("%"):
        return VarPart(name=name, default=rest[1:], mode="suffix")
    if rest.startswith("//"):
        return VarPart(name=name, default=rest[2:], mode="replace_all")
    if rest.startswith("/"):
        return VarPart(name=name, default=rest[1:], mode="replace")
    return VarPart(name=name, default=rest, mode="plain")


def parse(source: str) -> CommandList:
    pre = preprocess(source)
    try:
        tokens = tokenize(pre.cleaned_source)
    except ShellSyntaxError as e:
        raise ShellParseError(e.message, e.position) from e
    parser = _Parser(tokens, pre.heredocs)
    return parser.parse()


def expand_braces(text: str) -> list[str]:
    # Brace expansion for a flat literal string. Supports {a,b,c} and {x..y}
    # and {x..y..step}. Operates pre-variable-expansion. If the input has no
    # unquoted braces, returns [text].
    return _brace_expand(text)


def _brace_expand(text: str) -> list[str]:
    # Find first unescaped, top-level '{...}' that contains either a comma at
    # top level OR a valid sequence ('..').
    n = len(text)
    i = 0
    while i < n:
        if text[i] == "\\" and i + 1 < n:
            i += 2
            continue
        if text[i] == "{":
            close = _find_brace_close(text, i)
            if close < 0:
                i += 1
                continue
            inner = text[i + 1 : close]
            parts = _brace_split(inner)
            if parts is None:
                # not a real brace expansion
                i = close + 1
                continue
            prefix = text[:i]
            suffix = text[close + 1 :]
            results: list[str] = []
            for part in parts:
                # recurse on each combined string
                for expanded in _brace_expand(prefix + part + suffix):
                    results.append(expanded)
            return results
        i += 1
    return [text]


def _find_brace_close(text: str, start: int) -> int:
    depth = 0
    i = start
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _brace_split(inner: str) -> list[str] | None:
    # Split on top-level commas; if none, try sequence form A..B[..STEP].
    parts: list[str] = []
    depth = 0
    last = 0
    i = 0
    n = len(inner)
    has_comma = False
    while i < n:
        ch = inner[i]
        if ch == "\\" and i + 1 < n:
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(inner[last:i])
            last = i + 1
            has_comma = True
        i += 1
    parts.append(inner[last:])
    if has_comma:
        return parts
    # sequence form
    return _expand_sequence(inner)


def _expand_sequence(inner: str) -> list[str] | None:
    # A..B or A..B..STEP. A and B are integers or single chars.
    bits = inner.split("..")
    if len(bits) not in (2, 3):
        return None
    step = 1
    try:
        a = int(bits[0])
        b = int(bits[1])
        if len(bits) == 3:
            step = int(bits[2])
        if step == 0:
            step = 1
        if a <= b:
            step = abs(step)
            return [str(v) for v in range(a, b + 1, step)]
        step = -abs(step)
        return [str(v) for v in range(a, b - 1, step)]
    except ValueError:
        # char range — only single-char a/b
        if len(bits[0]) == 1 and len(bits[1]) == 1:
            a_ch = bits[0]
            b_ch = bits[1]
            ai, bi = ord(a_ch), ord(b_ch)
            if ai <= bi:
                return [chr(c) for c in range(ai, bi + 1)]
            return [chr(c) for c in range(ai, bi - 1, -1)]
        return None
