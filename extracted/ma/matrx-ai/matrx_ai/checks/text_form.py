"""The one-line text form of a check (CONTRACT v2 §2.2): a read view parsed into the same JSON.

``parse_check_text(format_check(c)) == c`` for every check the form can express.
"""

from __future__ import annotations

import json
import re
from typing import Any

from matrx_ai.checks.models import Check, Expected, ReadSpec, Split

__all__ = ["CheckTextError", "format_check", "parse_check_text"]

_OPS_TEXT: list[tuple[str, str]] = [
    ("not contains", "not_contains"),
    ("not matches", "not_matches"),
    ("not leaks", "not_leaks"),
    ("matches_schema", "matches_schema"),
    ("routes_in", "routes_in"),
    ("contains", "contains"),
    ("matches", "matches"),
    ("conforms", "conforms"),
    ("exists", "exists"),
    ("empty", "empty"),
    ("count", "count"),
    ("==", "eq"),
    ("!=", "ne"),
    (">=", "gte"),
    ("<=", "lte"),
    ("in", "in"),
]
_OP_TO_TEXT = {v: k for k, v in _OPS_TEXT}
_COUNT_OPS = {"==": "eq", ">=": "gte", "<=": "lte"}
_COUNT_TO_TEXT = {v: k for k, v in _COUNT_OPS.items()}
_SINKS = {
    "reply", "output", "request", "preview", "stored", "conversation",
    "tool_calls", "rows", "usage", "outcome", "door",
}
_MODS = {"match", "trim", "lower", "split"}


class CheckTextError(ValueError):
    def __init__(self, message: str, position: int) -> None:
        super().__init__(f"{message} (at character {position})")
        self.position = position


class _P:
    def __init__(self, text: str) -> None:
        self.s = text
        self.i = 0

    def ws(self) -> None:
        while self.i < len(self.s) and self.s[self.i].isspace():
            self.i += 1

    def peek(self, token: str) -> bool:
        return self.s.startswith(token, self.i)

    def eat(self, token: str) -> bool:
        if self.peek(token):
            self.i += len(token)
            return True
        return False

    def need(self, token: str) -> None:
        if not self.eat(token):
            raise CheckTextError(f"expected {token!r}", self.i)

    def ident(self) -> str:
        m = re.compile(r"[A-Za-z_][A-Za-z0-9_\-]*").match(self.s, self.i)
        if not m:
            raise CheckTextError("expected a name", self.i)
        self.i = m.end()
        return m.group(0)

    def integer(self) -> int:
        m = re.compile(r"-?\d+").match(self.s, self.i)
        if not m:
            raise CheckTextError("expected a whole number", self.i)
        self.i = m.end()
        return int(m.group(0))

    def string(self) -> str:
        if not self.eat('"'):
            raise CheckTextError('expected a "string"', self.i)
        out: list[str] = []
        while self.i < len(self.s):
            ch = self.s[self.i]
            if ch == "\\" and self.i + 1 < len(self.s) and self.s[self.i + 1] == '"':
                out.append('"')
                self.i += 2
                continue
            if ch == '"':
                self.i += 1
                return "".join(out)
            out.append(ch)
            self.i += 1
        raise CheckTextError("unterminated string", self.i)

    def name_or_string(self) -> str:
        return self.string() if self.peek('"') else self.ident()

    def done(self) -> bool:
        self.ws()
        return self.i >= len(self.s)


def _q(text: str) -> str:
    return '"' + text.replace('"', '\\"') + '"'


# ── modifiers ────────────────────────────────────────────────────────────────


def _parse_mod(p: _P, name: str, target: dict[str, Any]) -> None:
    if name == "trim":
        target["trim"] = True
    elif name == "lower":
        target["lower"] = True
    elif name == "match":
        p.need("(")
        target["match"] = p.string()
        p.need(")")
    elif name == "split":
        p.need("(")
        sep = p.string()
        p.ws()
        p.need(",")
        p.ws()
        idx = p.integer()
        p.need(")")
        target["split"] = Split(sep=sep, index=idx)


def _fmt_mods(m: Any) -> str:
    out = ""
    if m.split is not None:
        out += f".split({_q(m.split.sep)}, {m.split.index})"
    if m.match is not None:
        out += f".match({_q(m.match)})"
    if m.trim:
        out += ".trim"
    if m.lower:
        out += ".lower"
    return out


# ── sink expression ──────────────────────────────────────────────────────────


def _parse_sink(p: _P) -> tuple[str, int | str | None, dict[str, Any]]:
    start = p.i
    sink = p.ident()
    if sink not in _SINKS:
        raise CheckTextError(f"unknown sink {sink!r}", start)
    turn: int | str | None = None
    read: dict[str, Any] = {}
    if p.eat("["):
        turn = "each" if p.eat("each") else p.integer()
        p.need("]")
    if sink == "tool_calls" and p.eat("("):
        read["tool"] = p.string()
        p.need(")")
    if sink == "rows":
        p.need("(")
        read["table"] = p.string()
        where: dict[str, Any] = {}
        p.ws()
        while p.eat(","):
            p.ws()
            col = p.ident()
            p.ws()
            p.need("=")
            p.ws()
            where[col] = _parse_expected(p)
            p.ws()
        p.need(")")
        if where:
            read["where"] = where
    path: list[str] = []
    while p.eat("."):
        seg_start = p.i
        if re.compile(r"\d").match(p.s, p.i):
            path.append(str(p.integer()))
            continue
        name = p.ident()
        if name == "field":
            p.need("(")
            read["field"] = p.string()
            p.need(")")
        elif name in ("line", "final", "limit"):
            p.need("(")
            read[name] = p.integer()
            p.need(")")
        elif name in _MODS:
            _parse_mod(p, name, read)
        elif read.get("field") or read.get("match") or read.get("split"):
            raise CheckTextError("a path segment cannot follow a read modifier", seg_start)
        else:
            path.append(name)
    if path:
        read["path"] = ".".join(path)
    return sink, turn, read


def _fmt_sink(sink: str, turn: Any, read: ReadSpec) -> str:
    out = sink
    if turn is not None:
        out += f"[{turn}]"
    if sink == "tool_calls" and read.tool is not None:
        out += f"({_q(read.tool)})"
    if sink == "rows":
        parts = [_q(read.table or "")]
        for col, val in (read.where or {}).items():
            exp = val if isinstance(val, Expected) else Expected.model_validate({"from": "literal", "value": val})
            parts.append(f"{col} = {_fmt_expected(exp)}")
        out += "(" + ", ".join(parts) + ")"
    if read.path:
        out += "." + read.path
    if read.field is not None:
        out += f".field({_q(read.field)})"
    if read.line is not None:
        out += f".line({read.line})"
    if read.final is not None:
        out += f".final({read.final})"
    if sink == "rows" and read.limit != 50:
        out += f".limit({read.limit})"
    return out + _fmt_mods(read)


# ── expected ─────────────────────────────────────────────────────────────────


def _parse_at(p: _P, d: dict[str, Any]) -> None:
    if p.eat("@"):
        at = p.ident()
        if at not in ("seeded", "edited"):
            raise CheckTextError("expected @seeded or @edited", p.i)
        d["at"] = at


def _trailing_mods(p: _P, d: dict[str, Any]) -> None:
    while p.peek("."):
        save = p.i
        p.i += 1
        m = re.compile(r"[A-Za-z_]+").match(p.s, p.i)
        if not m or m.group(0) not in _MODS:
            p.i = save
            return
        p.i = m.end()
        _parse_mod(p, m.group(0), d)


def _parse_expected(p: _P) -> Expected:
    d: dict[str, Any]
    start = p.i
    if p.peek('"'):
        d = {"from": "literal", "value": p.string()}
    elif p.peek("[") or p.peek("{"):
        try:
            value, end = json.JSONDecoder().raw_decode(p.s, p.i)
        except json.JSONDecodeError as exc:
            raise CheckTextError(f"bad JSON: {exc.msg}", p.i) from exc
        p.i = end
        d = {"from": "literal", "value": value}
    elif re.compile(r"-?\d").match(p.s, p.i):
        m = re.compile(r"-?\d+(\.\d+)?").match(p.s, p.i)
        assert m is not None
        p.i = m.end()
        d = {"from": "literal", "value": float(m.group(0)) if m.group(1) else int(m.group(0))}
    else:
        word = p.ident()
        if word in ("true", "false", "null"):
            d = {"from": "literal", "value": {"true": True, "false": False, "null": None}[word]}
        elif word == "input":
            segs: list[str] = []
            while p.peek("."):
                save = p.i
                p.i += 1
                m = re.compile(r"[A-Za-z_][A-Za-z0-9_\-]*|\d+").match(p.s, p.i)
                if not m:
                    raise CheckTextError("expected an input path segment", p.i)
                if m.group(0) in _MODS:
                    p.i = save
                    break
                p.i = m.end()
                if m.group(0) == "turn" and p.eat("("):
                    n = p.integer()
                    p.need(")")
                    segs.extend(["turn", str(n)])
                else:
                    segs.append(m.group(0))
            if not segs:
                raise CheckTextError("input needs a path", start)
            d = {"from": "input", "path": ".".join(segs)}
        elif word == "marker":
            p.need("(")
            d = {"from": "marker", "name": p.name_or_string()}
            p.need(")")
        elif word == "pick_list":
            p.need("(")
            var = p.name_or_string()
            p.need(")")
            p.need(".")
            d = {"from": "pick_list", "var": var, "part": p.ident()}
            _parse_at(p, d)
        elif word == "prompt_block":
            p.need("(")
            name = p.name_or_string()
            p.need(")")
            p.need(".")
            d = {"from": "prompt_block", "name": name, "part": p.ident()}
            _parse_at(p, d)
        elif word == "default":
            p.need("(")
            d = {"from": "default", "var": p.name_or_string()}
            p.need(")")
            _parse_at(p, d)
        elif word == "observed":
            p.need("(")
            sink, turn, read = _parse_sink(p)
            p.need(")")
            d = {"from": "observed", "sink": sink, "turn": turn if isinstance(turn, int) else None}
            if read:
                d["read"] = ReadSpec(**read)
        elif word == "run":
            p.need(".")
            d = {"from": "run", "field": p.ident()}
        else:
            raise CheckTextError(f"unknown expected value {word!r}", start)
    _trailing_mods(p, d)
    return Expected.model_validate(d)


def _fmt_literal(value: Any) -> str:
    if isinstance(value, str):
        return _q(value)
    return json.dumps(value)


def _fmt_expected(e: Expected) -> str:
    src = e.from_
    at = "" if e.at == "seeded" else f"@{e.at}"
    if src == "literal":
        out = _fmt_literal(e.value)
    elif src == "input":
        out = "input." + re.sub(r"(^|\.)turn\.(\d+)", r"\1turn(\2)", e.path or "")
    elif src == "marker":
        out = f"marker({_q(e.name or '')})"
    elif src == "pick_list":
        out = f"pick_list({e.var}).{e.part or 'label'}{at}"
    elif src == "prompt_block":
        out = f"prompt_block({_q(e.name or '')}).{e.part or 'content'}{at}"
    elif src == "default":
        out = f"default({e.var}){at}"
    elif src == "observed":
        out = f"observed({_fmt_sink(e.sink or 'reply', e.turn, e.read or ReadSpec())})"
    else:
        out = f"run.{e.field}"
    return out + _fmt_mods(e)


# ── public ───────────────────────────────────────────────────────────────────


def parse_check_text(line: str, *, id: str = "", title: str = "", required: bool = True) -> Check:  # noqa: A002
    p = _P(line.strip())
    p.need("expect")
    p.ws()
    data: dict[str, Any] = {"id": id or "check", "title": title, "required": required}
    if p.eat("same_across_doors("):
        p.ws()
        sink, turn, read = _parse_sink(p)
        p.ws()
        ignore: list[str] = []
        if p.eat(","):
            p.ws()
            p.need("ignore:")
            p.ws()
            ignore.append(p.name_or_string())
            p.ws()
            while p.eat(","):
                p.ws()
                ignore.append(p.name_or_string())
                p.ws()
        p.need(")")
        data.update(sink=sink, turn=turn, read=ReadSpec(**read), op="same_across_doors", ignore=ignore)
    else:
        sink, turn, read = _parse_sink(p)
        p.ws()
        op = None
        for text, name in _OPS_TEXT:
            if p.peek(text) and (not text[-1].isalpha() or not p.s[p.i + len(text): p.i + len(text) + 1].isalnum()):
                p.i += len(text)
                op = name
                break
        if op is None:
            raise CheckTextError("expected an operator", p.i)
        data.update(sink=sink, turn=turn, read=ReadSpec(**read), op=op)
        p.ws()
        if op == "count":
            for text, cop in _COUNT_OPS.items():
                if p.eat(text):
                    data["count_op"] = cop
                    break
            else:
                raise CheckTextError("count needs ==, >= or <=", p.i)
            p.ws()
            data["expected"] = Expected.model_validate({"from": "literal", "value": p.integer()})
        elif op not in ("exists", "empty"):
            data["expected"] = _parse_expected(p)
    if not p.done():
        raise CheckTextError("unexpected text after the check", p.i)
    return Check(**data)


def format_check(check: Check) -> str:
    sink = _fmt_sink(check.sink, check.turn, check.read)
    if check.op == "same_across_doors":
        ignore = ""
        if check.ignore:
            ignore = ", ignore: " + ", ".join(
                i if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_\-]*", i) else _q(i) for i in check.ignore
            )
        return f"expect same_across_doors({sink}{ignore})"
    if check.op == "count":
        n = check.expected.value if check.expected is not None else 0
        return f"expect {sink} count {_COUNT_TO_TEXT[check.count_op or 'eq']} {n}"
    out = f"expect {sink} {_OP_TO_TEXT[check.op]}"
    if check.expected is not None:
        out += " " + _fmt_expected(check.expected)
    return out
