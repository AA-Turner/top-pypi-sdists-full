from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .ast import (
    ArithPart,
    CmdSubPart,
    GlobPart,
    LiteralPart,
    TildePart,
    VarPart,
    Word,
)

if TYPE_CHECKING:
    from .env import ShellEnv
    from .runner import CommandRunner


class ShellExpansionError(Exception):
    pass


# Sentinel chars to mark "kept-quoted" boundaries during word splitting.
# We embed segments that should never be split or globbed using a private
# marker. Word splitting treats characters between these markers as a single
# atom; pathname expansion treats any word containing these marks as
# non-glob (or strips them if no glob chars remain).
_QUOTED_OPEN = "\x01"
_QUOTED_CLOSE = "\x02"
_FIELD_SEP = "\x03"


async def expand_word(
    word: Word,
    env: ShellEnv,
    runner: CommandRunner,
    *,
    for_assignment: bool = False,
    for_redirect: bool = False,
) -> list[str]:
    # Returns 0..N strings for one Word, applying full bash expansion order.
    # Brace expansion happens upstream (in the executor pre-pass), so by the
    # time we reach here, the word is already a single brace-resolved unit.
    raw = await _build_raw_string(word, env, runner)
    if for_assignment or for_redirect:
        # Skip word splitting and glob; just collapse markers.
        return [_strip_markers(raw)]
    fields = _word_split(raw, env.ifs)
    out: list[str] = []
    for f in fields:
        if _has_glob(f):
            stripped_pattern = _strip_markers_for_glob(f)
            matches = await runner.glob(
                stripped_pattern,
                env.cwd,
                globstar=env.shell_opts.get("globstar", True),
                nullglob=env.shell_opts.get("nullglob", False),
            )
            if matches:
                out.extend(sorted(matches))
            else:
                if env.shell_opts.get("nullglob", False):
                    continue
                out.append(_strip_markers(f))
        else:
            out.append(_strip_markers(f))
    return out


_DQ_OPEN_TEXT = "\x04DQ_OPEN\x04"
_DQ_CLOSE_TEXT = "\x04DQ_CLOSE\x04"


async def _build_raw_string(word: Word, env: ShellEnv, runner: CommandRunner) -> str:
    parts: list[str] = []
    first = True
    for part in word.parts:
        if isinstance(part, LiteralPart):
            if part.text == _DQ_OPEN_TEXT:
                parts.append(_QUOTED_OPEN)
                continue
            if part.text == _DQ_CLOSE_TEXT:
                parts.append(_QUOTED_CLOSE)
                continue
            if part.quoted:
                parts.append(_QUOTED_OPEN + part.text + _QUOTED_CLOSE)
            else:
                parts.append(part.text)
        elif isinstance(part, TildePart):
            if first:
                if part.user is None:
                    home = env.get("HOME", "/")
                else:
                    home = f"/home/{part.user}"
                parts.append(home)
            else:
                parts.append("~" + (part.user or ""))
        elif isinstance(part, VarPart):
            text = _expand_var(part, env)
            parts.append(text)
        elif isinstance(part, ArithPart):
            parts.append(str(_eval_arith(part.expression, env)))
        elif isinstance(part, CmdSubPart):
            text = await _run_cmdsub(part, env, runner)
            parts.append(text)
        elif isinstance(part, GlobPart):
            parts.append(part.pattern)
        first = False
    return "".join(parts)


def _expand_var(part: VarPart, env: ShellEnv) -> str:
    name = part.name
    # Special vars
    if name == "?":
        return str(env.last_exit)
    if name == "$":
        return str(env.pid)
    if name == "!":
        return str(env.last_bg_pid)
    if name == "#":
        return str(len(env.positional))
    if name == "@" or name == "*":
        return " ".join(env.positional)
    if name == "0":
        return env.script_name
    if name.isdigit():
        idx = int(name) - 1
        if 0 <= idx < len(env.positional):
            return env.positional[idx]
        return ""

    set_ = env.is_set(name)
    val = env.get(name, "")
    nonempty = set_ and val != ""

    mode = part.mode
    if mode == "plain":
        return val
    if mode == "default":
        return val if nonempty else (part.default or "")
    if mode == "use_default":
        return val if set_ else (part.default or "")
    if mode == "assign":
        if not nonempty:
            env.set(name, part.default or "")
            return part.default or ""
        return val
    if mode == "error":
        if not nonempty:
            raise ShellExpansionError(part.default or f"{name}: parameter null or not set")
        return val
    if mode == "alt":
        return (part.default or "") if nonempty else ""
    if mode == "length":
        return str(len(val))
    if mode == "prefix":
        return _strip_prefix(val, part.default or "", greedy=False)
    if mode == "prefix_long":
        return _strip_prefix(val, part.default or "", greedy=True)
    if mode == "suffix":
        return _strip_suffix(val, part.default or "", greedy=False)
    if mode == "suffix_long":
        return _strip_suffix(val, part.default or "", greedy=True)
    if mode == "replace":
        return _replace(val, part.default or "", once=True)
    if mode == "replace_all":
        return _replace(val, part.default or "", once=False)
    return val


def _glob_to_re(pat: str) -> re.Pattern[str]:
    # Translate a shell-style pattern (only * ? [ ]) to a regex.
    out: list[str] = []
    i = 0
    n = len(pat)
    while i < n:
        c = pat[i]
        if c == "*":
            out.append(".*")
        elif c == "?":
            out.append(".")
        elif c == "[":
            j = i + 1
            if j < n and pat[j] == "!":
                pat_class = "^"
                j += 1
            else:
                pat_class = ""
            while j < n and pat[j] != "]":
                pat_class += re.escape(pat[j])
                j += 1
            if j < n:
                out.append(f"[{pat_class}]")
                i = j
            else:
                out.append(re.escape(c))
        elif c == "\\" and i + 1 < n:
            out.append(re.escape(pat[i + 1]))
            i += 1
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("".join(out))


def _strip_prefix(val: str, pat: str, *, greedy: bool) -> str:
    if not pat:
        return val
    rx = _glob_to_re(pat)
    if greedy:
        # longest match at start
        for end in range(len(val), -1, -1):
            if rx.fullmatch(val[:end]):
                return val[end:]
    else:
        for end in range(0, len(val) + 1):
            if rx.fullmatch(val[:end]):
                return val[end:]
    return val


def _strip_suffix(val: str, pat: str, *, greedy: bool) -> str:
    if not pat:
        return val
    rx = _glob_to_re(pat)
    if greedy:
        for start in range(0, len(val) + 1):
            if rx.fullmatch(val[start:]):
                return val[:start]
    else:
        for start in range(len(val), -1, -1):
            if rx.fullmatch(val[start:]):
                return val[:start]
    return val


def _replace(val: str, spec: str, *, once: bool) -> str:
    # spec is "pat/repl" or "pat" (replace with "")
    if "/" in spec:
        pat, repl = spec.split("/", 1)
    else:
        pat, repl = spec, ""
    rx = _glob_to_re(pat)
    if once:
        m = rx.search(val)
        if not m:
            return val
        return val[: m.start()] + repl + val[m.end() :]
    return rx.sub(repl, val)


def _eval_arith(expr: str, env: ShellEnv) -> int:
    # Substitute bare names with their values (default 0) then eval as a
    # constrained int expression. Operators allowed: + - * / % ** ( ) and
    # unary -/+. We use ast for safety.
    import ast as _ast

    def _resolve_names(s: str) -> str:
        def repl(m: re.Match[str]) -> str:
            name = m.group(0)
            if name in {"True", "False", "None"}:
                return name
            v = env.get(name, "0")
            try:
                int(v)
            except ValueError:
                return "0"
            return v

        return re.sub(r"\$?[A-Za-z_][A-Za-z0-9_]*", repl, s)

    src = _resolve_names(expr)

    try:
        tree = _ast.parse(src, mode="eval")
    except SyntaxError:
        return 0

    def _eval(node: object) -> int:
        if isinstance(node, _ast.Expression):
            return _eval(node.body)
        if isinstance(node, _ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, _ast.UnaryOp):
            v = _eval(node.operand)
            if isinstance(node.op, _ast.USub):
                return -v
            if isinstance(node.op, _ast.UAdd):
                return v
            return 0
        if isinstance(node, _ast.BinOp):
            lhs = _eval(node.left)
            rhs = _eval(node.right)
            op = node.op
            if isinstance(op, _ast.Add):
                return lhs + rhs
            if isinstance(op, _ast.Sub):
                return lhs - rhs
            if isinstance(op, _ast.Mult):
                return lhs * rhs
            if isinstance(op, _ast.Div):
                return lhs // rhs if rhs else 0
            if isinstance(op, _ast.FloorDiv):
                return lhs // rhs if rhs else 0
            if isinstance(op, _ast.Mod):
                return lhs % rhs if rhs else 0
            if isinstance(op, _ast.Pow):
                return lhs**rhs
            return 0
        return 0

    try:
        return _eval(tree)
    except Exception:
        return 0


async def _run_cmdsub(part: CmdSubPart, env: ShellEnv, runner: CommandRunner) -> str:
    # Avoid circular import: defer.
    from .executor import execute  # noqa: PLC0415

    result = await execute(part.command, env, runner, capture=True)
    out = result.stdout.decode("utf-8", errors="replace")
    # POSIX: strip trailing newlines.
    return out.rstrip("\n")


def _word_split(raw: str, ifs: str) -> list[str]:
    # Split outside _QUOTED_OPEN/_QUOTED_CLOSE markers on any IFS char.
    # POSIX nuance: a quoted empty section yields one empty field — we track
    # whether the buffer touched a quoted region so a `""` produces [""] not [].
    if not ifs:
        return [raw] if raw else []
    out: list[str] = []
    buf: list[str] = []
    inside = 0
    saw_quoted = False
    for ch in raw:
        if ch == _QUOTED_OPEN:
            inside += 1
            saw_quoted = True
            buf.append(ch)
            continue
        if ch == _QUOTED_CLOSE:
            inside = max(0, inside - 1)
            buf.append(ch)
            continue
        if inside == 0 and ch in ifs:
            if buf:
                out.append("".join(buf))
                buf.clear()
                saw_quoted = False
            continue
        buf.append(ch)
    if buf:
        out.append("".join(buf))
    elif saw_quoted:
        out.append("")
    return out


def _strip_markers(s: str) -> str:
    return s.replace(_QUOTED_OPEN, "").replace(_QUOTED_CLOSE, "")


def _strip_markers_for_glob(s: str) -> str:
    # When globbing, characters inside markers are literal: escape metacharacters.
    out: list[str] = []
    inside = 0
    for ch in s:
        if ch == _QUOTED_OPEN:
            inside += 1
            continue
        if ch == _QUOTED_CLOSE:
            inside = max(0, inside - 1)
            continue
        if inside > 0 and ch in "*?[]":
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def _has_glob(s: str) -> bool:
    inside = 0
    for ch in s:
        if ch == _QUOTED_OPEN:
            inside += 1
            continue
        if ch == _QUOTED_CLOSE:
            inside = max(0, inside - 1)
            continue
        if inside == 0 and ch in "*?[":
            return True
    return False
