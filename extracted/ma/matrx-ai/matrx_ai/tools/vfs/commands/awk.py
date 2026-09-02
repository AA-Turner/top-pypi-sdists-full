from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class AwkSyntaxError(Exception):
    pass


class AwkRuntimeError(Exception):
    pass


class _NextSignal(Exception):
    pass


class _ExitSignal(Exception):
    def __init__(self, code: int) -> None:
        self.code = code


def _syntax_error(msg: str) -> bytes:
    return encode(
        f"awk: cmd. line:1: {msg}\nawk: cmd. line:1: ^ syntax error\n"
    )


def _missing_file(path: str) -> bytes:
    return encode(f"awk: can't open file {path}\n source line number 0\n")


def _div_zero(filename: str, fnr: int) -> bytes:
    return encode(
        f"awk: cmd. line:1: (FILENAME={filename} FNR={fnr}) "
        "fatal: division by zero attempted\n"
    )


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------


# Token types.
T_NUMBER = "NUMBER"
T_STRING = "STRING"
T_REGEX = "REGEX"
T_IDENT = "IDENT"
T_FIELD = "FIELD"  # $N or $expr
T_OP = "OP"
T_LBRACE = "LBRACE"
T_RBRACE = "RBRACE"
T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"
T_LBRACK = "LBRACK"
T_RBRACK = "RBRACK"
T_COMMA = "COMMA"
T_SEMI = "SEMI"
T_NEWLINE = "NEWLINE"
T_KEYWORD = "KEYWORD"
T_EOF = "EOF"

_KEYWORDS = {
    "BEGIN",
    "END",
    "if",
    "else",
    "while",
    "for",
    "do",
    "next",
    "exit",
    "return",
    "function",
    "in",
    "print",
    "printf",
    "break",
    "continue",
    "getline",
    "delete",
}

# Multi-char operators (longest first when scanning).
_MULTI_OPS = (
    "==", "!=", "<=", ">=", "&&", "||", "++", "--",
    "+=", "-=", "*=", "/=", "%=", "^=", "**",
    "!~", "~",
)
_SINGLE_OPS = "+-*/%^=<>!?:"


@dataclass(slots=True)
class _Token:
    kind: str
    value: Any
    pos: int


def _tokenize(src: str) -> list[_Token]:
    tokens: list[_Token] = []
    i = 0
    n = len(src)
    # Track context for regex disambiguation.
    # A '/' starts a regex when the previous meaningful token is "operatorish":
    # start of program, after comma, semicolon, newline, "(", "{", "[", "=",
    # operators, or keywords like "if", "while", "return", "print", "printf",
    # "&&", "||", "!", "~", "!~", or "$".
    def _can_be_regex_start() -> bool:
        for tok in reversed(tokens):
            if tok.kind == T_NEWLINE:
                return True
            return tok.kind not in (
                T_NUMBER, T_STRING, T_IDENT, T_RPAREN, T_RBRACK
            ) or (tok.kind == T_IDENT and tok.value in (
                "if", "while", "return", "print", "printf", "do", "else", "for"
            ))
        return True

    while i < n:
        ch = src[i]
        if ch in " \t":
            i += 1
            continue
        if ch == "\\" and i + 1 < n and src[i + 1] == "\n":
            # Line continuation.
            i += 2
            continue
        if ch == "\n":
            tokens.append(_Token(T_NEWLINE, "\n", i))
            i += 1
            continue
        if ch == "#":
            while i < n and src[i] != "\n":
                i += 1
            continue
        if ch == "{":
            tokens.append(_Token(T_LBRACE, "{", i))
            i += 1
            continue
        if ch == "}":
            tokens.append(_Token(T_RBRACE, "}", i))
            i += 1
            continue
        if ch == "(":
            tokens.append(_Token(T_LPAREN, "(", i))
            i += 1
            continue
        if ch == ")":
            tokens.append(_Token(T_RPAREN, ")", i))
            i += 1
            continue
        if ch == "[":
            tokens.append(_Token(T_LBRACK, "[", i))
            i += 1
            continue
        if ch == "]":
            tokens.append(_Token(T_RBRACK, "]", i))
            i += 1
            continue
        if ch == ",":
            tokens.append(_Token(T_COMMA, ",", i))
            i += 1
            continue
        if ch == ";":
            tokens.append(_Token(T_SEMI, ";", i))
            i += 1
            continue
        if ch == "$":
            tokens.append(_Token(T_OP, "$", i))
            i += 1
            continue
        if ch == '"':
            j = i + 1
            buf: list[str] = []
            while j < n and src[j] != '"':
                if src[j] == "\\" and j + 1 < n:
                    nxt = src[j + 1]
                    esc = {
                        "n": "\n", "t": "\t", "r": "\r",
                        "\\": "\\", '"': '"', "/": "/",
                        "a": "\a", "b": "\b", "f": "\f", "v": "\v", "0": "\0",
                    }.get(nxt)
                    if esc is not None:
                        buf.append(esc)
                        j += 2
                        continue
                    buf.append(nxt)
                    j += 2
                    continue
                buf.append(src[j])
                j += 1
            if j >= n:
                raise AwkSyntaxError("unterminated string")
            tokens.append(_Token(T_STRING, "".join(buf), i))
            i = j + 1
            continue
        if ch == "/" and _can_be_regex_start():
            j = i + 1
            buf = []
            while j < n and src[j] != "/":
                if src[j] == "\\" and j + 1 < n:
                    buf.append(src[j])
                    buf.append(src[j + 1])
                    j += 2
                    continue
                if src[j] == "\n":
                    raise AwkSyntaxError("unterminated regex")
                buf.append(src[j])
                j += 1
            if j >= n:
                raise AwkSyntaxError("unterminated regex")
            tokens.append(_Token(T_REGEX, "".join(buf), i))
            i = j + 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < n and src[i + 1].isdigit()):
            j = i
            saw_dot = False
            saw_e = False
            while j < n:
                c = src[j]
                if c.isdigit():
                    j += 1
                elif c == "." and not saw_dot and not saw_e:
                    saw_dot = True
                    j += 1
                elif c in "eE" and not saw_e:
                    saw_e = True
                    j += 1
                    if j < n and src[j] in "+-":
                        j += 1
                else:
                    break
            tokens.append(_Token(T_NUMBER, float(src[i:j]), i))
            i = j
            continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            word = src[i:j]
            if word in _KEYWORDS:
                tokens.append(_Token(T_IDENT, word, i))
            else:
                tokens.append(_Token(T_IDENT, word, i))
            i = j
            continue
        # Multi-char ops.
        matched = False
        for op in _MULTI_OPS:
            if src.startswith(op, i):
                tokens.append(_Token(T_OP, op, i))
                i += len(op)
                matched = True
                break
        if matched:
            continue
        if ch in _SINGLE_OPS:
            tokens.append(_Token(T_OP, ch, i))
            i += 1
            continue
        raise AwkSyntaxError(f"unexpected character {ch!r}")

    tokens.append(_Token(T_EOF, None, n))
    return tokens


# ---------------------------------------------------------------------------
# AST
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _Rule:
    pattern: Any  # None | "BEGIN" | "END" | ("regex", str) | ast expression
    action: list[Any]  # list of statement nodes; None means default {print}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


class _Parser:
    def __init__(self, tokens: list[_Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self, offset: int = 0) -> _Token:
        return self.tokens[self.pos + offset]

    def _advance(self) -> _Token:
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def _check(self, kind: str, value: Any = None) -> bool:
        t = self.tokens[self.pos]
        if t.kind != kind:
            return False
        if value is not None and t.value != value:
            return False
        return True

    def _match(self, kind: str, value: Any = None) -> bool:
        if self._check(kind, value):
            self._advance()
            return True
        return False

    def _skip_terminators(self) -> None:
        while self._check(T_NEWLINE) or self._check(T_SEMI):
            self._advance()

    def parse_program(self) -> list[_Rule]:
        rules: list[_Rule] = []
        self._skip_terminators()
        while not self._check(T_EOF):
            rule = self._parse_rule()
            rules.append(rule)
            self._skip_terminators()
        return rules

    def _parse_rule(self) -> _Rule:
        # Pattern can be: BEGIN, END, /regex/, expression, or empty.
        pattern: Any = None
        if self._check(T_IDENT, "BEGIN"):
            self._advance()
            pattern = "BEGIN"
        elif self._check(T_IDENT, "END"):
            self._advance()
            pattern = "END"
        elif self._check(T_LBRACE):
            pattern = None
        else:
            # An expression pattern (possibly a regex literal).
            pattern = ("expr", self._parse_expression())

        # Action.
        action: list[Any]
        if self._check(T_LBRACE):
            self._advance()
            action = self._parse_statements_until_rbrace()
        else:
            # No action: default is { print }
            action = [("print", [("field", ("number", 0.0))], None)]
        return _Rule(pattern=pattern, action=action)

    def _parse_statements_until_rbrace(self) -> list[Any]:
        stmts: list[Any] = []
        self._skip_terminators()
        while not self._check(T_RBRACE) and not self._check(T_EOF):
            stmt = self._parse_statement()
            if stmt is not None:
                stmts.append(stmt)
            self._skip_terminators()
        if not self._match(T_RBRACE):
            raise AwkSyntaxError("expected '}'")
        return stmts

    def _parse_statement(self) -> Any:
        t = self._peek()
        if t.kind == T_IDENT:
            if t.value == "if":
                return self._parse_if()
            if t.value == "while":
                return self._parse_while()
            if t.value == "for":
                return self._parse_for()
            if t.value == "next":
                self._advance()
                return ("next",)
            if t.value == "exit":
                self._advance()
                expr = None
                if not self._is_statement_terminator():
                    expr = self._parse_expression()
                return ("exit", expr)
            if t.value == "break":
                self._advance()
                return ("break",)
            if t.value == "continue":
                self._advance()
                return ("continue",)
            if t.value == "print":
                return self._parse_print()
            if t.value == "printf":
                return self._parse_printf()
            if t.value == "delete":
                self._advance()
                # delete arr[idx] — we ignore (not in subset).
                self._parse_expression()
                return ("noop",)
        if t.kind == T_LBRACE:
            self._advance()
            stmts = self._parse_statements_until_rbrace()
            return ("block", stmts)
        if t.kind == T_SEMI or t.kind == T_NEWLINE:
            return None
        # Expression statement.
        expr = self._parse_expression()
        return ("expr_stmt", expr)

    def _is_statement_terminator(self) -> bool:
        return self._check(T_SEMI) or self._check(T_NEWLINE) or self._check(T_RBRACE) or self._check(T_EOF)

    def _parse_if(self) -> Any:
        self._advance()  # if
        if not self._match(T_LPAREN):
            raise AwkSyntaxError("expected '(' after 'if'")
        cond = self._parse_expression()
        if not self._match(T_RPAREN):
            raise AwkSyntaxError("expected ')'")
        self._skip_terminators()
        then_stmt = self._parse_statement()
        self._skip_terminators()
        else_stmt = None
        if self._check(T_IDENT, "else"):
            self._advance()
            self._skip_terminators()
            else_stmt = self._parse_statement()
        return ("if", cond, then_stmt, else_stmt)

    def _parse_while(self) -> Any:
        self._advance()
        if not self._match(T_LPAREN):
            raise AwkSyntaxError("expected '(' after 'while'")
        cond = self._parse_expression()
        if not self._match(T_RPAREN):
            raise AwkSyntaxError("expected ')'")
        self._skip_terminators()
        body = self._parse_statement()
        return ("while", cond, body)

    def _parse_for(self) -> Any:
        self._advance()
        if not self._match(T_LPAREN):
            raise AwkSyntaxError("expected '(' after 'for'")
        # C-style for: (init; cond; step) body
        init = None
        if not self._check(T_SEMI):
            init = self._parse_statement()
        if not self._match(T_SEMI):
            raise AwkSyntaxError("expected ';' in for")
        cond = None
        if not self._check(T_SEMI):
            cond = self._parse_expression()
        if not self._match(T_SEMI):
            raise AwkSyntaxError("expected ';' in for")
        step = None
        if not self._check(T_RPAREN):
            step = self._parse_statement()
        if not self._match(T_RPAREN):
            raise AwkSyntaxError("expected ')'")
        self._skip_terminators()
        body = self._parse_statement()
        return ("for", init, cond, step, body)

    def _parse_print(self) -> Any:
        self._advance()
        # No-arg print = print $0.
        if self._is_statement_terminator():
            return ("print", [("field", ("number", 0.0))], None)
        args = self._parse_expr_list()
        # Optional > "file" — we don't support file redirection, but parse defensively.
        return ("print", args, None)

    def _parse_printf(self) -> Any:
        self._advance()
        if self._is_statement_terminator():
            raise AwkSyntaxError("printf requires format string")
        args = self._parse_expr_list()
        if not args:
            raise AwkSyntaxError("printf requires format string")
        return ("printf", args[0], args[1:])

    def _parse_expr_list(self) -> list[Any]:
        exprs = [self._parse_expression()]
        while self._match(T_COMMA):
            exprs.append(self._parse_expression())
        return exprs

    # ----- expression parser (recursive descent) -----

    def _parse_expression(self) -> Any:
        return self._parse_assignment()

    def _parse_assignment(self) -> Any:
        left = self._parse_ternary()
        if self._check(T_OP) and self._peek().value in (
            "=", "+=", "-=", "*=", "/=", "%=", "^="
        ):
            op = self._advance().value
            right = self._parse_assignment()
            return ("assign", op, left, right)
        return left

    def _parse_ternary(self) -> Any:
        cond = self._parse_logical_or()
        if self._check(T_OP, "?"):
            self._advance()
            then_e = self._parse_assignment()
            if not self._match(T_OP, ":"):
                raise AwkSyntaxError("expected ':' in ternary")
            else_e = self._parse_assignment()
            return ("ternary", cond, then_e, else_e)
        return cond

    def _parse_logical_or(self) -> Any:
        left = self._parse_logical_and()
        while self._check(T_OP, "||"):
            self._advance()
            right = self._parse_logical_and()
            left = ("logical", "||", left, right)
        return left

    def _parse_logical_and(self) -> Any:
        left = self._parse_in_match()
        while self._check(T_OP, "&&"):
            self._advance()
            right = self._parse_in_match()
            left = ("logical", "&&", left, right)
        return left

    def _parse_in_match(self) -> Any:
        left = self._parse_relational()
        while self._check(T_OP) and self._peek().value in ("~", "!~"):
            op = self._advance().value
            right = self._parse_relational()
            left = ("match", op, left, right)
        return left

    def _parse_relational(self) -> Any:
        left = self._parse_concat()
        while self._check(T_OP) and self._peek().value in (
            "<", ">", "<=", ">=", "==", "!="
        ):
            op = self._advance().value
            right = self._parse_concat()
            left = ("rel", op, left, right)
        return left

    def _parse_concat(self) -> Any:
        # In awk, two adjacent expressions implicitly concatenate.
        # Detection: next token can start an expression and isn't an operator/comma.
        left = self._parse_addition()
        while self._can_start_expression():
            right = self._parse_addition()
            left = ("concat", left, right)
        return left

    def _can_start_expression(self) -> bool:
        t = self._peek()
        if t.kind in (T_NUMBER, T_STRING):
            return True
        if t.kind == T_IDENT:
            # Avoid keywords that aren't expression starters.
            if t.value in (
                "BEGIN", "END", "if", "else", "while", "for", "do", "next",
                "exit", "return", "function", "in", "break", "continue",
                "delete", "print", "printf",
            ):
                return False
            return True
        if t.kind == T_LPAREN:
            return True
        if t.kind == T_OP and t.value in ("$", "!", "-", "+"):
            return True
        if t.kind == T_REGEX:
            return True
        return False

    def _parse_addition(self) -> Any:
        left = self._parse_multiplication()
        while self._check(T_OP) and self._peek().value in ("+", "-"):
            op = self._advance().value
            right = self._parse_multiplication()
            left = ("binop", op, left, right)
        return left

    def _parse_multiplication(self) -> Any:
        left = self._parse_exponent()
        while self._check(T_OP) and self._peek().value in ("*", "/", "%"):
            op = self._advance().value
            right = self._parse_exponent()
            left = ("binop", op, left, right)
        return left

    def _parse_exponent(self) -> Any:
        left = self._parse_unary()
        if self._check(T_OP) and self._peek().value in ("^", "**"):
            self._advance()
            right = self._parse_exponent()
            return ("binop", "^", left, right)
        return left

    def _parse_unary(self) -> Any:
        if self._check(T_OP, "!"):
            self._advance()
            return ("unary", "!", self._parse_unary())
        if self._check(T_OP, "-"):
            self._advance()
            return ("unary", "-", self._parse_unary())
        if self._check(T_OP, "+"):
            self._advance()
            return ("unary", "+", self._parse_unary())
        return self._parse_postfix()

    def _parse_postfix(self) -> Any:
        node = self._parse_field()
        while self._check(T_OP) and self._peek().value in ("++", "--"):
            op = self._advance().value
            node = ("postfix", op, node)
        return node

    def _parse_field(self) -> Any:
        if self._check(T_OP, "$"):
            self._advance()
            inner = self._parse_field()
            return ("field", inner)
        return self._parse_primary()

    def _parse_primary(self) -> Any:
        t = self._peek()
        if t.kind == T_NUMBER:
            self._advance()
            return ("number", t.value)
        if t.kind == T_STRING:
            self._advance()
            return ("string", t.value)
        if t.kind == T_REGEX:
            self._advance()
            return ("regex_lit", t.value)
        if t.kind == T_LPAREN:
            self._advance()
            expr = self._parse_expression()
            if not self._match(T_RPAREN):
                raise AwkSyntaxError("expected ')'")
            return ("group", expr)
        if t.kind == T_IDENT:
            name = t.value
            self._advance()
            # Function call?
            if self._check(T_LPAREN):
                self._advance()
                args: list[Any] = []
                if not self._check(T_RPAREN):
                    args.append(self._parse_expression())
                    while self._match(T_COMMA):
                        args.append(self._parse_expression())
                if not self._match(T_RPAREN):
                    raise AwkSyntaxError("expected ')'")
                return ("call", name, args)
            # Array indexing?
            if self._check(T_LBRACK):
                self._advance()
                idx = [self._parse_expression()]
                while self._match(T_COMMA):
                    idx.append(self._parse_expression())
                if not self._match(T_RBRACK):
                    raise AwkSyntaxError("expected ']'")
                return ("index", name, idx)
            return ("var", name)
        raise AwkSyntaxError(f"unexpected token {t.kind} {t.value!r}")


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _AwkState:
    variables: dict[str, Any] = field(default_factory=dict)
    arrays: dict[str, dict[str, Any]] = field(default_factory=dict)
    fields: list[str] = field(default_factory=list)
    nr: int = 0
    nf: int = 0
    fnr: int = 0
    filename: str = ""
    out: bytearray = field(default_factory=bytearray)
    err: bytearray = field(default_factory=bytearray)


def _to_number(v: Any) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return 0.0
    s = str(v).strip()
    if not s:
        return 0.0
    # Awk converts leading numeric portion only.
    m = re.match(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?", s)
    if m:
        try:
            return float(m.group(0))
        except ValueError:
            return 0.0
    return 0.0


def _to_string(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e16:
            return str(int(v))
        # gawk default OFMT is "%.6g".
        return f"{v:.6g}"
    return str(v)


def _is_truthy(v: Any) -> bool:
    if isinstance(v, (int, float)):
        return v != 0
    if isinstance(v, str):
        # Numeric string treatment: try numeric.
        s = v.strip()
        if s == "":
            return False
        try:
            return float(s) != 0
        except ValueError:
            return True
    return bool(v)


_DEFAULT_VARS: dict[str, Any] = {
    "FS": " ",
    "OFS": " ",
    "ORS": "\n",
    "RS": "\n",
    "NR": 0.0,
    "NF": 0.0,
    "FNR": 0.0,
    "FILENAME": "",
    "SUBSEP": "\x1c",
}


def _split_fields(line: str, fs: str) -> list[str]:
    if fs == " ":
        # Default: whitespace runs, leading/trailing trimmed.
        return line.split()
    if len(fs) == 1:
        return line.split(fs)
    # Regex separator.
    try:
        return re.split(fs, line)
    except re.error:
        return [line]


class _Interpreter:
    def __init__(self, rules: list[_Rule], state: _AwkState) -> None:
        self.rules = rules
        self.state = state

    def run_begin(self) -> None:
        for rule in self.rules:
            if rule.pattern == "BEGIN":
                try:
                    self._exec_block(rule.action)
                except _NextSignal:
                    pass

    def run_end(self) -> None:
        for rule in self.rules:
            if rule.pattern == "END":
                try:
                    self._exec_block(rule.action)
                except _NextSignal:
                    pass

    def run_line(self, line: str) -> None:
        self.state.nr += 1
        self.state.fnr += 1
        self._set_record(line)
        try:
            for rule in self.rules:
                if rule.pattern == "BEGIN" or rule.pattern == "END":
                    continue
                if self._pattern_matches(rule.pattern):
                    self._exec_block(rule.action)
        except _NextSignal:
            return

    def _set_record(self, line: str) -> None:
        self.state.fields = [line]
        fs = _to_string(self.state.variables.get("FS", " "))
        parts = _split_fields(line, fs)
        self.state.fields.extend(parts)
        self.state.nf = len(parts)
        self.state.variables["NF"] = float(self.state.nf)
        self.state.variables["NR"] = float(self.state.nr)
        self.state.variables["FNR"] = float(self.state.fnr)

    def _rebuild_record(self) -> None:
        ofs = _to_string(self.state.variables.get("OFS", " "))
        if self.state.fields:
            self.state.fields[0] = ofs.join(self.state.fields[1:])

    def _pattern_matches(self, pattern: Any) -> bool:
        if pattern is None:
            return True
        if isinstance(pattern, tuple) and pattern[0] == "expr":
            val = self._eval(pattern[1])
            # Bare regex literal pattern matches against $0.
            if isinstance(pattern[1], tuple) and pattern[1][0] == "regex_lit":
                rx = pattern[1][1]
                try:
                    return re.search(rx, self.state.fields[0]) is not None
                except re.error:
                    return False
            return _is_truthy(val)
        return False

    # ------- statements -------

    def _exec_block(self, stmts: list[Any]) -> None:
        for stmt in stmts:
            self._exec(stmt)

    def _exec(self, stmt: Any) -> None:
        if stmt is None:
            return
        kind = stmt[0]
        if kind == "noop":
            return
        if kind == "block":
            self._exec_block(stmt[1])
            return
        if kind == "expr_stmt":
            self._eval(stmt[1])
            return
        if kind == "if":
            cond, then_s, else_s = stmt[1], stmt[2], stmt[3]
            if _is_truthy(self._eval(cond)):
                self._exec(then_s)
            elif else_s is not None:
                self._exec(else_s)
            return
        if kind == "while":
            cond, body = stmt[1], stmt[2]
            while _is_truthy(self._eval(cond)):
                try:
                    self._exec(body)
                except _BreakSignal:
                    break
                except _ContinueSignal:
                    continue
            return
        if kind == "for":
            init, cond, step, body = stmt[1], stmt[2], stmt[3], stmt[4]
            if init is not None:
                self._exec(init)
            while cond is None or _is_truthy(self._eval(cond)):
                try:
                    self._exec(body)
                except _BreakSignal:
                    break
                except _ContinueSignal:
                    pass
                if step is not None:
                    self._exec(step)
            return
        if kind == "next":
            raise _NextSignal()
        if kind == "exit":
            code = 0
            if stmt[1] is not None:
                code = int(_to_number(self._eval(stmt[1])))
            raise _ExitSignal(code)
        if kind == "break":
            raise _BreakSignal()
        if kind == "continue":
            raise _ContinueSignal()
        if kind == "print":
            args, _redir = stmt[1], stmt[2]
            ofs = _to_string(self.state.variables.get("OFS", " "))
            ors_ = _to_string(self.state.variables.get("ORS", "\n"))
            pieces = [_to_string(self._eval(a)) for a in args]
            self.state.out.extend((ofs.join(pieces) + ors_).encode(
                "utf-8", errors="surrogateescape"
            ))
            return
        if kind == "printf":
            fmt_node, args_node = stmt[1], stmt[2]
            fmt = _to_string(self._eval(fmt_node))
            args = [self._eval(a) for a in args_node]
            self.state.out.extend(_sprintf(fmt, args).encode(
                "utf-8", errors="surrogateescape"
            ))
            return
        raise AwkRuntimeError(f"unknown statement kind {kind}")

    # ------- expressions -------

    def _eval(self, node: Any) -> Any:
        kind = node[0]
        if kind == "number":
            return float(node[1])
        if kind == "string":
            return node[1]
        if kind == "regex_lit":
            # When used in expression context, becomes match against $0.
            try:
                return 1.0 if re.search(node[1], self.state.fields[0]) else 0.0
            except re.error:
                return 0.0
        if kind == "var":
            return self._get_var(node[1])
        if kind == "group":
            return self._eval(node[1])
        if kind == "field":
            idx = int(_to_number(self._eval(node[1])))
            if idx < 0:
                raise AwkRuntimeError("negative field")
            if idx >= len(self.state.fields):
                return ""
            return self.state.fields[idx]
        if kind == "binop":
            op = node[1]
            lhs = self._eval(node[2])
            rhs = self._eval(node[3])
            return self._binop(op, lhs, rhs)
        if kind == "concat":
            lhs = self._eval(node[1])
            rhs = self._eval(node[2])
            return _to_string(lhs) + _to_string(rhs)
        if kind == "rel":
            op = node[1]
            lhs = self._eval(node[2])
            rhs = self._eval(node[3])
            return self._compare(op, lhs, rhs)
        if kind == "match":
            op = node[1]
            target = self._eval(node[2])
            pat_node = node[3]
            if isinstance(pat_node, tuple) and pat_node[0] == "regex_lit":
                rx = pat_node[1]
            else:
                rx = _to_string(self._eval(pat_node))
            try:
                found = re.search(rx, _to_string(target)) is not None
            except re.error:
                found = False
            if op == "~":
                return 1.0 if found else 0.0
            return 0.0 if found else 1.0
        if kind == "logical":
            op = node[1]
            if op == "&&":
                if not _is_truthy(self._eval(node[2])):
                    return 0.0
                return 1.0 if _is_truthy(self._eval(node[3])) else 0.0
            # ||
            if _is_truthy(self._eval(node[2])):
                return 1.0
            return 1.0 if _is_truthy(self._eval(node[3])) else 0.0
        if kind == "ternary":
            if _is_truthy(self._eval(node[1])):
                return self._eval(node[2])
            return self._eval(node[3])
        if kind == "unary":
            op = node[1]
            v = self._eval(node[2])
            if op == "!":
                return 0.0 if _is_truthy(v) else 1.0
            if op == "-":
                return -_to_number(v)
            if op == "+":
                return _to_number(v)
        if kind == "postfix":
            op = node[1]
            target = node[2]
            cur = _to_number(self._eval(target))
            new = cur + (1 if op == "++" else -1)
            self._assign_target(target, new)
            return cur
        if kind == "assign":
            op = node[1]
            target = node[2]
            rhs = self._eval(node[3])
            if op == "=":
                value = rhs
            else:
                cur = self._eval(target)
                value = self._binop(op[:-1], cur, rhs)
            self._assign_target(target, value)
            return value
        if kind == "call":
            return self._call(node[1], node[2])
        if kind == "index":
            name = node[1]
            idx_nodes = node[2]
            subsep = _to_string(self.state.variables.get("SUBSEP", "\x1c"))
            key = subsep.join(_to_string(self._eval(n)) for n in idx_nodes)
            arr = self.state.arrays.setdefault(name, {})
            return arr.get(key, "")
        raise AwkRuntimeError(f"unknown expression kind {kind}")

    def _binop(self, op: str, lhs: Any, rhs: Any) -> Any:
        a = _to_number(lhs)
        b = _to_number(rhs)
        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            if b == 0:
                raise AwkRuntimeError("division by zero")
            return a / b
        if op == "%":
            if b == 0:
                raise AwkRuntimeError("division by zero")
            # awk's % is C-style fmod.
            import math
            return math.fmod(a, b)
        if op == "^":
            return a ** b
        raise AwkRuntimeError(f"bad operator {op}")

    def _compare(self, op: str, lhs: Any, rhs: Any) -> float:
        # If both look numeric or one is number and the other is a numeric string,
        # compare as numbers.
        def _num_or_none(x: Any) -> float | None:
            if isinstance(x, (int, float)):
                return float(x)
            if isinstance(x, str):
                s = x.strip()
                if not s:
                    return None
                try:
                    return float(s)
                except ValueError:
                    return None
            return None

        ln = _num_or_none(lhs)
        rn = _num_or_none(rhs)
        # Both are numeric (one is a real number, or both look numeric).
        if isinstance(lhs, (int, float)) and isinstance(rhs, (int, float)):
            cmp_l: Any = float(lhs)
            cmp_r: Any = float(rhs)
        elif (isinstance(lhs, (int, float)) and rn is not None) or (
            isinstance(rhs, (int, float)) and ln is not None
        ):
            cmp_l = (
                float(lhs) if isinstance(lhs, (int, float))
                else (ln if ln is not None else 0.0)
            )
            cmp_r = (
                float(rhs) if isinstance(rhs, (int, float))
                else (rn if rn is not None else 0.0)
            )
        elif ln is not None and rn is not None:
            cmp_l = ln
            cmp_r = rn
        else:
            cmp_l = _to_string(lhs)
            cmp_r = _to_string(rhs)
        if op == "==":
            return 1.0 if cmp_l == cmp_r else 0.0
        if op == "!=":
            return 1.0 if cmp_l != cmp_r else 0.0
        if op == "<":
            return 1.0 if cmp_l < cmp_r else 0.0
        if op == ">":
            return 1.0 if cmp_l > cmp_r else 0.0
        if op == "<=":
            return 1.0 if cmp_l <= cmp_r else 0.0
        if op == ">=":
            return 1.0 if cmp_l >= cmp_r else 0.0
        return 0.0

    def _get_var(self, name: str) -> Any:
        if name in self.state.variables:
            return self.state.variables[name]
        return ""

    def _assign_target(self, target: Any, value: Any) -> None:
        if not isinstance(target, tuple):
            raise AwkRuntimeError("bad assignment target")
        kind = target[0]
        if kind == "var":
            self.state.variables[target[1]] = value
            if target[1] in ("NF", "FS", "OFS", "ORS", "RS"):
                # If NF assigned, conceptually we'd reshape fields; not supported.
                pass
            return
        if kind == "field":
            idx = int(_to_number(self._eval(target[1])))
            if idx < 0:
                raise AwkRuntimeError("negative field")
            sval = _to_string(value)
            while idx >= len(self.state.fields):
                self.state.fields.append("")
            self.state.fields[idx] = sval
            self.state.nf = max(self.state.nf, len(self.state.fields) - 1)
            self.state.variables["NF"] = float(self.state.nf)
            if idx > 0:
                self._rebuild_record()
            else:
                # Reassigning $0 reparses fields.
                fs = _to_string(self.state.variables.get("FS", " "))
                parts = _split_fields(sval, fs)
                self.state.fields = [sval] + parts
                self.state.nf = len(parts)
                self.state.variables["NF"] = float(self.state.nf)
            return
        if kind == "index":
            name = target[1]
            idx_nodes = target[2]
            subsep = _to_string(self.state.variables.get("SUBSEP", "\x1c"))
            key = subsep.join(_to_string(self._eval(n)) for n in idx_nodes)
            arr = self.state.arrays.setdefault(name, {})
            arr[key] = value
            return
        raise AwkRuntimeError("bad assignment target")

    def _call(self, name: str, arg_nodes: list[Any]) -> Any:
        # Lazy-eval args (most builtins are eager).
        if name == "length":
            if not arg_nodes:
                return float(len(_to_string(self.state.fields[0])))
            v = self._eval(arg_nodes[0])
            if isinstance(v, dict):
                return float(len(v))
            return float(len(_to_string(v)))
        if name == "substr":
            s = _to_string(self._eval(arg_nodes[0]))
            m = int(_to_number(self._eval(arg_nodes[1])))
            # awk is 1-indexed.
            if len(arg_nodes) >= 3:
                length = int(_to_number(self._eval(arg_nodes[2])))
            else:
                length = None
            # Compute in awk semantics.
            if m < 1:
                if length is not None:
                    length = length + m - 1
                m = 1
            if length is None:
                return s[m - 1 :]
            if length < 0:
                return ""
            return s[m - 1 : m - 1 + length]
        if name == "tolower":
            return _to_string(self._eval(arg_nodes[0])).lower()
        if name == "toupper":
            return _to_string(self._eval(arg_nodes[0])).upper()
        if name == "split":
            s = _to_string(self._eval(arg_nodes[0]))
            arr_name_node = arg_nodes[1]
            if not (isinstance(arr_name_node, tuple) and arr_name_node[0] == "var"):
                raise AwkRuntimeError("split: second arg must be array")
            arr_name = arr_name_node[1]
            if len(arg_nodes) >= 3:
                sep_node = arg_nodes[2]
                if isinstance(sep_node, tuple) and sep_node[0] == "regex_lit":
                    sep = sep_node[1]
                else:
                    sep = _to_string(self._eval(sep_node))
            else:
                sep = _to_string(self.state.variables.get("FS", " "))
            parts = _split_fields(s, sep)
            arr = {}
            for i, p in enumerate(parts, start=1):
                arr[str(i)] = p
            self.state.arrays[arr_name] = arr
            return float(len(parts))
        if name == "gsub":
            return self._gsub(arg_nodes, replace_all=True)
        if name == "sub":
            return self._gsub(arg_nodes, replace_all=False)
        if name == "match":
            s = _to_string(self._eval(arg_nodes[0]))
            pat_node = arg_nodes[1]
            if isinstance(pat_node, tuple) and pat_node[0] == "regex_lit":
                rx = pat_node[1]
            else:
                rx = _to_string(self._eval(pat_node))
            try:
                m = re.search(rx, s)
            except re.error:
                m = None
            if m is None:
                self.state.variables["RSTART"] = 0.0
                self.state.variables["RLENGTH"] = -1.0
                return 0.0
            self.state.variables["RSTART"] = float(m.start() + 1)
            self.state.variables["RLENGTH"] = float(m.end() - m.start())
            return float(m.start() + 1)
        if name == "index":
            s = _to_string(self._eval(arg_nodes[0]))
            t = _to_string(self._eval(arg_nodes[1]))
            if t == "":
                return 0.0
            i = s.find(t)
            return float(0 if i < 0 else i + 1)
        if name == "sprintf":
            fmt = _to_string(self._eval(arg_nodes[0]))
            args = [self._eval(a) for a in arg_nodes[1:]]
            return _sprintf(fmt, args)
        if name == "int":
            return float(int(_to_number(self._eval(arg_nodes[0]))))
        raise AwkRuntimeError(f"unknown function {name}")

    def _gsub(self, arg_nodes: list[Any], replace_all: bool) -> Any:
        pat_node = arg_nodes[0]
        if isinstance(pat_node, tuple) and pat_node[0] == "regex_lit":
            rx = pat_node[1]
        else:
            rx = _to_string(self._eval(pat_node))
        repl = _to_string(self._eval(arg_nodes[1]))
        # Determine target. Default is $0.
        if len(arg_nodes) >= 3:
            target = arg_nodes[2]
        else:
            target = ("field", ("number", 0.0))
        s = _to_string(self._eval(target))
        # Awk replacement: '&' refers to whole match; '\&' is literal '&'.
        try:
            compiled = re.compile(rx)
        except re.error:
            return 0.0

        count = 0

        def _rep_func(m: re.Match[str]) -> str:
            nonlocal count
            count += 1
            out = []
            i = 0
            while i < len(repl):
                c = repl[i]
                if c == "\\" and i + 1 < len(repl):
                    nxt = repl[i + 1]
                    if nxt == "&":
                        out.append("&")
                    elif nxt == "\\":
                        out.append("\\")
                    else:
                        out.append("\\")
                        out.append(nxt)
                    i += 2
                    continue
                if c == "&":
                    out.append(m.group(0))
                    i += 1
                    continue
                out.append(c)
                i += 1
            return "".join(out)

        if replace_all:
            new_s = compiled.sub(_rep_func, s)
        else:
            new_s = compiled.sub(_rep_func, s, count=1)
        self._assign_target(target, new_s)
        return float(count)


class _BreakSignal(Exception):
    pass


class _ContinueSignal(Exception):
    pass


# ---------------------------------------------------------------------------
# printf-style formatting (for printf and sprintf)
# ---------------------------------------------------------------------------

_PRINTF_RE = re.compile(
    r"%(?P<flags>[-+ 0#]*)(?P<width>\d+)?(?:\.(?P<prec>\d+))?(?P<conv>[sdiouxXeEfgGc%])"
)


def _sprintf(fmt: str, args: list[Any]) -> str:
    out: list[str] = []
    i = 0
    ai = 0
    while i < len(fmt):
        ch = fmt[i]
        if ch == "\\" and i + 1 < len(fmt):
            nxt = fmt[i + 1]
            esc = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\"}.get(nxt)
            if esc is not None:
                out.append(esc)
                i += 2
                continue
        if ch != "%":
            out.append(ch)
            i += 1
            continue
        m = _PRINTF_RE.match(fmt, i)
        if m is None:
            out.append(ch)
            i += 1
            continue
        conv = m.group("conv")
        if conv == "%":
            out.append("%")
            i = m.end()
            continue
        flags = m.group("flags") or ""
        width = m.group("width")
        prec = m.group("prec")
        spec = "%" + flags + (width or "") + (("." + prec) if prec is not None else "") + conv
        # Get arg.
        if ai < len(args):
            arg = args[ai]
            ai += 1
        else:
            arg = ""
        try:
            if conv == "s":
                rendered = spec % _to_string(arg)
            elif conv == "c":
                # awk %c: numeric -> chr; else first char.
                if isinstance(arg, (int, float)) and not (
                    isinstance(arg, str)
                ):
                    rendered = chr(int(arg))
                else:
                    s = _to_string(arg)
                    rendered = s[0] if s else ""
            elif conv in ("d", "i", "o", "x", "X", "u"):
                py_conv = "d" if conv == "i" else conv
                py_spec = "%" + flags + (width or "") + (
                    ("." + prec) if prec is not None else ""
                ) + py_conv
                rendered = py_spec % int(_to_number(arg))
            else:
                rendered = spec % _to_number(arg)
        except (TypeError, ValueError):
            rendered = ""
        out.append(rendered)
        i = m.end()
    return "".join(out)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _AwkOpts:
    fs: str | None = None
    program: str = ""
    program_files: list[str] = field(default_factory=list)
    var_inits: list[tuple[str, str]] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


def _parse_var_assignment(s: str) -> tuple[str, str] | None:
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", s)
    if not m:
        return None
    return m.group(1), m.group(2)


def _parse_args(args: list[str]) -> tuple[_AwkOpts, CommandResult | None]:
    opts = _AwkOpts()
    i = 0
    have_program = False
    end_of_opts = False
    while i < len(args):
        a = args[i]
        if end_of_opts:
            opts.files.append(a)
            i += 1
            continue
        if a == "--":
            end_of_opts = True
            i += 1
            continue
        if a.startswith("-F"):
            value = a[2:]
            if not value:
                if i + 1 >= len(args):
                    return opts, fail(2, _syntax_error("missing argument for -F"))
                i += 1
                value = args[i]
            opts.fs = value
            i += 1
            continue
        if a.startswith("-v"):
            value = a[2:]
            if not value:
                if i + 1 >= len(args):
                    return opts, fail(2, _syntax_error("missing argument for -v"))
                i += 1
                value = args[i]
            parsed = _parse_var_assignment(value)
            if parsed is None:
                return opts, fail(2, _syntax_error(f"invalid -v assignment: {value}"))
            opts.var_inits.append(parsed)
            i += 1
            continue
        if a.startswith("-f"):
            value = a[2:]
            if not value:
                if i + 1 >= len(args):
                    return opts, fail(2, _syntax_error("missing argument for -f"))
                i += 1
                value = args[i]
            opts.program_files.append(value)
            have_program = True
            i += 1
            continue
        if a == "-" or not a.startswith("-"):
            if not have_program:
                opts.program = a
                have_program = True
                i += 1
                continue
            # Late "var=val" file is a var assignment that takes effect between files;
            # we don't model that — treat as a regular file path or var assignment for END.
            parsed = _parse_var_assignment(a)
            if parsed is not None:
                opts.var_inits.append(parsed)
                i += 1
                continue
            opts.files.append(a)
            i += 1
            continue
        return opts, fail(2, _syntax_error(f"unknown option {a!r}"))
    if not have_program:
        return opts, fail(2, _syntax_error("missing program"))
    return opts, None


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


@register("awk", "gawk")
async def cmd_awk(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.args)
    if err is not None:
        return err

    # Resolve program text.
    program_parts: list[str] = []
    for pf in opts.program_files:
        resolved = resolve_cwd(ctx.env, pf)
        try:
            data = await ctx.vfs._cat_file(resolved)
        except (FileNotFoundError, IsADirectoryError, OSError):
            return fail(2, _missing_file(pf))
        program_parts.append(data.decode("utf-8", errors="surrogateescape"))
    if opts.program:
        program_parts.append(opts.program)
    program_text = "\n".join(program_parts)

    try:
        tokens = _tokenize(program_text)
        rules = _Parser(tokens).parse_program()
    except AwkSyntaxError as exc:
        return fail(2, _syntax_error(str(exc)))

    state = _AwkState()
    state.variables.update(_DEFAULT_VARS)
    if opts.fs is not None:
        state.variables["FS"] = opts.fs
    for k, v in opts.var_inits:
        state.variables[k] = v

    interp = _Interpreter(rules, state)

    exit_code = 0

    try:
        interp.run_begin()
    except _ExitSignal as e:
        return _finish(state, e.code)
    except AwkRuntimeError as e:
        msg = str(e)
        if "division by zero" in msg:
            state.err.extend(_div_zero(state.filename or "-", state.fnr))
            return CommandResult(
                stdout=bytes(state.out),
                stderr=bytes(state.err),
                exit_code=2,
            )
        state.err.extend(encode(f"awk: {msg}\n"))
        return CommandResult(
            stdout=bytes(state.out),
            stderr=bytes(state.err),
            exit_code=2,
        )

    # Build input source list.
    input_sources: list[tuple[str, bytes]] = []
    if not opts.files:
        input_sources.append(("-", ctx.stdin))
    else:
        for fn in opts.files:
            if fn == "-":
                input_sources.append(("-", ctx.stdin))
                continue
            resolved = resolve_cwd(ctx.env, fn)
            try:
                data = await ctx.vfs._cat_file(resolved)
            except (FileNotFoundError, IsADirectoryError, OSError):
                state.err.extend(_missing_file(fn))
                exit_code = 2
                continue
            input_sources.append((fn, data))

    # Process inputs.
    try:
        for fn, data in input_sources:
            state.filename = fn
            state.fnr = 0
            state.variables["FILENAME"] = fn
            text = data.decode("utf-8", errors="surrogateescape")
            rs = _to_string(state.variables.get("RS", "\n"))
            if rs == "\n":
                lines = text.split("\n")
                if lines and lines[-1] == "":
                    lines.pop()
            elif len(rs) == 1:
                lines = text.split(rs)
                if lines and lines[-1] == "":
                    lines.pop()
            else:
                lines = re.split(rs, text)
                if lines and lines[-1] == "":
                    lines.pop()
            for line in lines:
                try:
                    interp.run_line(line)
                except AwkRuntimeError as e:
                    msg = str(e)
                    if "division by zero" in msg:
                        state.err.extend(_div_zero(fn, state.fnr))
                        return CommandResult(
                            stdout=bytes(state.out),
                            stderr=bytes(state.err),
                            exit_code=2,
                        )
                    state.err.extend(encode(f"awk: {msg}\n"))
                    return CommandResult(
                        stdout=bytes(state.out),
                        stderr=bytes(state.err),
                        exit_code=2,
                    )

        interp.run_end()
    except _ExitSignal as e:
        try:
            interp.run_end()
        except _ExitSignal as e2:
            return _finish(state, e2.code)
        except (AwkRuntimeError, _NextSignal):
            pass
        return _finish(state, e.code)
    except AwkRuntimeError as e:
        msg = str(e)
        if "division by zero" in msg:
            state.err.extend(_div_zero(state.filename or "-", state.fnr))
            return CommandResult(
                stdout=bytes(state.out),
                stderr=bytes(state.err),
                exit_code=2,
            )
        state.err.extend(encode(f"awk: {msg}\n"))
        return CommandResult(
            stdout=bytes(state.out),
            stderr=bytes(state.err),
            exit_code=2,
        )

    return CommandResult(
        stdout=bytes(state.out),
        stderr=bytes(state.err),
        exit_code=exit_code,
    )


def _finish(state: _AwkState, code: int) -> CommandResult:
    return CommandResult(
        stdout=bytes(state.out),
        stderr=bytes(state.err),
        exit_code=code,
    )
