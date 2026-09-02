from __future__ import annotations

import fnmatch
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import get as get_command
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import find_no_file
from matrx_ai.tools.vfs.paths import basename
from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "f": "file",
    "d": "directory",
    "l": "link",
    # Sockets, fifos, char/block devices have no VFS analogue; we accept the
    # letters and never match.
    "s": "__socket__",
    "p": "__fifo__",
    "c": "__char__",
    "b": "__block__",
}


def _to_epoch(value: object) -> float:
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _info_type(info: dict) -> str:
    return info.get("type", "file")


def _join(parent: str, child: str) -> str:
    if parent.endswith("/"):
        return parent + child
    return parent + "/" + child


# ---------------------------------------------------------------------------
# Predicate parsing
# ---------------------------------------------------------------------------


@dataclass
class _ParseError(Exception):
    message: str


@dataclass
class _Node:
    pass


@dataclass
class _Test(_Node):
    name: str
    arg: str | None = None


@dataclass
class _Action(_Node):
    name: str
    args: list[str] = field(default_factory=list)


@dataclass
class _Not(_Node):
    inner: _Node


@dataclass
class _And(_Node):
    left: _Node
    right: _Node


@dataclass
class _Or(_Node):
    left: _Node
    right: _Node


_TESTS_WITH_ARG = {
    "-name",
    "-iname",
    "-path",
    "-ipath",
    "-wholename",
    "-regex",
    "-iregex",
    "-type",
    "-maxdepth",
    "-mindepth",
    "-mtime",
    "-mmin",
    "-newer",
    "-size",
    "-perm",
    "-user",
    "-group",
    "-uid",
    "-gid",
    "-inum",
    "-links",
}

_TESTS_NO_ARG = {
    "-empty",
    "-true",
    "-false",
    "-readable",
    "-writable",
    "-executable",
}

_ACTIONS_NO_ARG = {
    "-print",
    "-print0",
    "-ls",
    "-delete",
    "-quit",
    "-prune",
}

_ACTIONS_WITH_ARGS = {
    "-exec",
    "-execdir",
    "-ok",
    "-okdir",
    "-fprint",
    "-fprint0",
}

_GLOBAL_OPTIONS = {
    "-maxdepth",
    "-mindepth",
    "-depth",
    "-mount",
    "-xdev",
    "-noleaf",
    "-follow",
}

_OPERATORS = {"-and", "-a", "-or", "-o", "-not", "!", "(", ")", ","}


def _is_predicate_token(tok: str) -> bool:
    if tok in _OPERATORS:
        return True
    if tok in _TESTS_WITH_ARG or tok in _TESTS_NO_ARG:
        return True
    if tok in _ACTIONS_NO_ARG or tok in _ACTIONS_WITH_ARGS:
        return True
    if tok.startswith("-"):
        return True
    return False


def _split_paths_and_expr(args: list[str]) -> tuple[list[str], list[str], str | None]:
    paths: list[str] = []
    i = 0
    # Paths come first: any token that is not a leading `-`, `(`, `)`, or `!` is
    # treated as a path. The bare `-` is also a valid path. Once we hit a token
    # that starts the expression, the rest of argv belongs to the expression
    # (including arguments to predicates that may not start with `-`).
    while i < len(args):
        a = args[i]
        if a in ("(", ")", "!"):
            break
        if a.startswith("-") and a != "-":
            break
        paths.append(a)
        i += 1
    expr_tokens = args[i:]
    return paths, expr_tokens, None


class _Parser:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.pos = 0
        # Pre-extract global options (consumed without affecting the tree).
        self.maxdepth: int | None = None
        self.mindepth: int | None = None
        self.depth_first: bool = False
        self.has_action: bool = False

    def _peek(self) -> str | None:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def _consume(self) -> str:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self) -> _Node | None:
        if not self.tokens:
            return None
        node = self._parse_or()
        if self.pos < len(self.tokens):
            raise _ParseError(f"find: paths must precede expression: '{self.tokens[self.pos]}'\n")
        return node

    def _parse_or(self) -> _Node:
        left = self._parse_and()
        while self._peek() in ("-or", "-o", ","):
            op = self._consume()
            right = self._parse_and()
            if op == ",":
                # Comma operator: evaluate both, take right's truth value.
                # We treat it as "and" in terms of side-effects but never short-
                # circuits. For our 80% scope we collapse to OR semantics —
                # comma is rare; punt to OR which still evaluates both sides
                # under our action-emission model. If exactness mattered we
                # would add a dedicated _Comma node.
                left = _Or(left=left, right=right)
            else:
                left = _Or(left=left, right=right)
        return left

    def _parse_and(self) -> _Node:
        left = self._parse_factor()
        while True:
            nxt = self._peek()
            if nxt is None:
                break
            if nxt in ("-or", "-o", ")", ","):
                break
            if nxt in ("-and", "-a"):
                self._consume()
            right = self._parse_factor()
            left = _And(left=left, right=right)
        return left

    def _parse_factor(self) -> _Node:
        tok = self._peek()
        if tok is None:
            raise _ParseError("find: missing expression\n")
        if tok == "!" or tok == "-not":
            self._consume()
            inner = self._parse_factor()
            return _Not(inner=inner)
        if tok == "(":
            self._consume()
            inner = self._parse_or()
            close = self._peek()
            if close != ")":
                raise _ParseError("find: invalid expression: expected ')'\n")
            self._consume()
            return inner
        # A bare token that isn't `-`-prefixed and isn't a grouping marker is
        # a misplaced path argument.
        if not tok.startswith("-") and tok != ",":
            raise _ParseError(f"find: paths must precede expression: '{tok}'\n")
        return self._parse_predicate()

    def _parse_predicate(self) -> _Node:
        tok = self._consume()
        if tok in _TESTS_WITH_ARG:
            arg = self._peek()
            if arg is None:
                raise _ParseError(f"find: missing argument to '{tok}'\n")
            self._consume()
            if tok in ("-maxdepth", "-mindepth"):
                # Global option — resolve to integer and absorb into parser
                # state; emit a constant "true" predicate.
                try:
                    n = int(arg)
                except ValueError:
                    raise _ParseError(f"find: invalid argument '{arg}' to '{tok}'\n") from None
                if n < 0:
                    raise _ParseError(f"find: invalid argument '{arg}' to '{tok}'\n")
                if tok == "-maxdepth":
                    self.maxdepth = n
                else:
                    self.mindepth = n
                return _Test(name="-true")
            return _Test(name=tok, arg=arg)
        if tok in _TESTS_NO_ARG:
            return _Test(name=tok)
        if tok == "-depth":
            self.depth_first = True
            return _Test(name="-true")
        if tok in ("-mount", "-xdev", "-noleaf", "-follow"):
            return _Test(name="-true")
        if tok in _ACTIONS_NO_ARG:
            self.has_action = True
            return _Action(name=tok)
        if tok in ("-exec", "-execdir"):
            self.has_action = True
            cmd_args: list[str] = []
            terminator: str | None = None
            while True:
                nxt = self._peek()
                if nxt is None:
                    raise _ParseError(f"find: missing argument to '{tok}'\n")
                if nxt == ";" or nxt == "+":
                    terminator = nxt
                    self._consume()
                    break
                cmd_args.append(self._consume())
            if not cmd_args:
                raise _ParseError(f"find: missing argument to '{tok}'\n")
            return _Action(name=tok, args=cmd_args + [terminator])
        if tok == ")" or tok == "(":
            raise _ParseError(f"find: invalid expression: unexpected '{tok}'\n")
        # Unknown predicate.
        raise _ParseError(f"find: unknown predicate '{tok}'\n")


# ---------------------------------------------------------------------------
# Evaluation context
# ---------------------------------------------------------------------------


@dataclass
class _Match:
    """Single visited path in the traversal."""

    path: str  # display path (with original prefix)
    abs_path: str  # absolute resolved path
    info: dict
    depth: int


@dataclass
class _EvalState:
    stdout: bytearray
    stderr: bytearray
    exit_code: int
    quit: bool
    pruned: bool
    deleted_paths: set[str]


# ---------------------------------------------------------------------------
# Predicate matching (boolean logic only)
# ---------------------------------------------------------------------------


def _parse_size_for_match(arg: str) -> tuple[int, int, str]:
    sign = 0
    if arg.startswith("+"):
        sign = 1
        arg = arg[1:]
    elif arg.startswith("-"):
        sign = -1
        arg = arg[1:]
    if not arg:
        raise ValueError("empty size")
    suffix = arg[-1]
    if suffix in "cwbkMG":
        n = int(arg[:-1])
        return sign, n, suffix
    return sign, int(arg), "b"


def _size_matches(file_size: int, sign: int, n: int, unit: str) -> bool:
    multipliers = {"c": 1, "w": 2, "b": 512, "k": 1024, "M": 1024 * 1024, "G": 1024 * 1024 * 1024}
    mult = multipliers[unit]
    # GNU find: file_size is rounded up to next unit.
    rounded = (file_size + mult - 1) // mult if file_size > 0 else 0
    if sign == 0:
        return rounded == n
    if sign > 0:
        return rounded > n
    return rounded < n


def _time_matches(delta_seconds: float, sign: int, n: int, unit_seconds: int) -> bool:
    # GNU find: rounds delta toward zero in unit, then compares.
    days = int(delta_seconds // unit_seconds)
    if sign == 0:
        return days == n
    if sign > 0:
        return days > n
    return days < n


async def _eval_test(
    node: _Test,
    match: _Match,
    ctx: CommandContext,
    state: _EvalState,
    newer_cache: dict[str, float],
) -> bool:
    name = node.name
    arg = node.arg
    if name == "-true":
        return True
    if name == "-false":
        return False
    if name == "-name":
        return fnmatch.fnmatchcase(basename(match.path) or match.path, arg or "")
    if name == "-iname":
        bn = basename(match.path) or match.path
        return fnmatch.fnmatchcase(bn.lower(), (arg or "").lower())
    if name in ("-path", "-wholename"):
        return fnmatch.fnmatchcase(match.path, arg or "")
    if name == "-ipath":
        return fnmatch.fnmatchcase(match.path.lower(), (arg or "").lower())
    if name == "-regex":
        try:
            return re.fullmatch(arg or "", match.path) is not None
        except re.error:
            return False
    if name == "-iregex":
        try:
            return re.fullmatch(arg or "", match.path, re.IGNORECASE) is not None
        except re.error:
            return False
    if name == "-type":
        if not arg:
            return False
        wanted = _TYPE_MAP.get(arg)
        if wanted is None:
            return False
        return _info_type(match.info) == wanted
    if name == "-empty":
        t = _info_type(match.info)
        if t == "directory":
            children = await ctx.vfs._ls(match.abs_path, detail=False)
            return len(children) == 0
        if t == "file":
            return int(match.info.get("size", 0) or 0) == 0
        return False
    if name == "-size":
        if _info_type(match.info) != "file":
            return False
        try:
            sign, n, unit = _parse_size_for_match(arg or "")
        except ValueError:
            return False
        return _size_matches(int(match.info.get("size", 0) or 0), sign, n, unit)
    if name == "-mtime":
        try:
            sign, n = _parse_signed_int(arg or "")
        except ValueError:
            return False
        delta = time.time() - _to_epoch(match.info.get("mtime"))
        return _time_matches(delta, sign, n, 86400)
    if name == "-mmin":
        try:
            sign, n = _parse_signed_int(arg or "")
        except ValueError:
            return False
        delta = time.time() - _to_epoch(match.info.get("mtime"))
        return _time_matches(delta, sign, n, 60)
    if name == "-newer":
        if not arg:
            return False
        if arg not in newer_cache:
            try:
                ref_info = await ctx.vfs._info(resolve_cwd(ctx.env, arg))
                newer_cache[arg] = _to_epoch(ref_info.get("mtime"))
            except (FileNotFoundError, OSError):
                newer_cache[arg] = float("inf")
        return _to_epoch(match.info.get("mtime")) > newer_cache[arg]
    if name in ("-readable", "-writable", "-executable"):
        # All paths are accessible in the VFS.
        return True
    # Unknown test: should have been caught at parse time.
    return False


def _parse_signed_int(arg: str) -> tuple[int, int]:
    if arg.startswith("+"):
        return 1, int(arg[1:])
    if arg.startswith("-"):
        return -1, int(arg[1:])
    return 0, int(arg)


# ---------------------------------------------------------------------------
# Action execution
# ---------------------------------------------------------------------------


def _ls_dils_line(match: _Match) -> str:
    info = match.info
    t = _info_type(info)
    mode = int(info.get("mode") or (0o755 if t == "directory" else 0o644))
    size = int(info.get("size", 0) or 0)
    nlink = int(info.get("nlink") or (2 if t == "directory" else 1))
    if t == "directory":
        prefix = "d"
    elif t == "link":
        prefix = "l"
    else:
        prefix = "-"
    bits = ""
    for shift in (6, 3, 0):
        chunk = (mode >> shift) & 0o7
        bits += "r" if chunk & 0o4 else "-"
        bits += "w" if chunk & 0o2 else "-"
        bits += "x" if chunk & 0o1 else "-"
    perms = prefix + bits
    blocks = (size + 1023) // 1024
    mtime = _to_epoch(info.get("mtime"))
    if mtime:
        date_str = datetime.fromtimestamp(mtime).strftime("%b %d %H:%M")
    else:
        date_str = "Jan  1  1970"
    return f"       1 {blocks:>4} {perms} {nlink:>3} user user {size:>8} {date_str} {match.path}"


async def _delete_match(match: _Match, ctx: CommandContext, state: _EvalState) -> None:
    t = _info_type(match.info)
    try:
        if t == "directory":
            await ctx.vfs._rmdir(match.abs_path)
        else:
            await ctx.vfs._rm_file(match.abs_path)
        state.deleted_paths.add(match.abs_path)
    except OSError as e:
        state.stderr.extend(
            encode(
                f"find: cannot delete '{match.path}': {e.strerror or 'Operation not permitted'}\n"
            )
        )
        state.exit_code = 1


async def _run_exec(
    action: _Action,
    match: _Match,
    ctx: CommandContext,
    state: _EvalState,
) -> bool:
    # action.args = [arg1, arg2, ..., terminator]
    template = action.args[:-1]
    terminator = action.args[-1]
    if terminator == "+":
        # Aggregate form: in our model we still execute once per match for
        # simplicity. The semantic difference is invisible when the underlying
        # command produces deterministic per-arg output.
        substituted = [a.replace("{}", match.abs_path) for a in template]
    else:
        substituted = [a.replace("{}", match.abs_path) for a in template]
    if not substituted:
        return True
    cmd_name = substituted[0]
    cmd = get_command(cmd_name)
    if cmd is None:
        state.stderr.extend(encode(f"find: '{cmd_name}': No such file or directory\n"))
        state.exit_code = 1
        # Per GNU find, -exec failure stops emitting output for this match
        # but does not abort the traversal.
        return False
    new_ctx = CommandContext(
        argv=substituted,
        stdin=b"",
        env=ctx.env,
        vfs=ctx.vfs,
    )
    try:
        result = await cmd(new_ctx)
    except Exception as e:  # noqa: BLE001 - guard against any cmd raising
        state.stderr.extend(encode(f"find: {cmd_name}: {e}\n"))
        state.exit_code = 1
        return False
    if result.stdout:
        state.stdout.extend(result.stdout)
    if result.stderr:
        state.stderr.extend(result.stderr)
    return result.exit_code == 0


async def _exec_action(
    node: _Action,
    match: _Match,
    ctx: CommandContext,
    state: _EvalState,
) -> bool:
    name = node.name
    if name == "-print":
        state.stdout.extend(encode(match.path + "\n"))
        return True
    if name == "-print0":
        state.stdout.extend(encode(match.path))
        state.stdout.append(0)
        return True
    if name == "-ls":
        state.stdout.extend(encode(_ls_dils_line(match) + "\n"))
        return True
    if name == "-delete":
        await _delete_match(match, ctx, state)
        return True
    if name == "-quit":
        state.quit = True
        return True
    if name == "-prune":
        state.pruned = True
        return True
    if name in ("-exec", "-execdir"):
        return await _run_exec(node, match, ctx, state)
    return True


# ---------------------------------------------------------------------------
# Tree evaluation: returns truth value, may emit via actions.
# ---------------------------------------------------------------------------


async def _eval(
    node: _Node,
    match: _Match,
    ctx: CommandContext,
    state: _EvalState,
    newer_cache: dict[str, float],
) -> bool:
    if isinstance(node, _Test):
        return await _eval_test(node, match, ctx, state, newer_cache)
    if isinstance(node, _Action):
        return await _exec_action(node, match, ctx, state)
    if isinstance(node, _Not):
        return not await _eval(node.inner, match, ctx, state, newer_cache)
    if isinstance(node, _And):
        left = await _eval(node.left, match, ctx, state, newer_cache)
        if not left:
            return False
        return await _eval(node.right, match, ctx, state, newer_cache)
    if isinstance(node, _Or):
        left = await _eval(node.left, match, ctx, state, newer_cache)
        if left:
            return True
        return await _eval(node.right, match, ctx, state, newer_cache)
    return False


# ---------------------------------------------------------------------------
# Traversal
# ---------------------------------------------------------------------------


async def _gather_children(
    vfs: MatrxAsyncFS,
    abs_path: str,
) -> list[dict] | None:
    try:
        return await vfs._ls(abs_path, detail=True)
    except (FileNotFoundError, OSError):
        return None


async def _traverse(
    display: str,
    abs_path: str,
    info: dict,
    depth: int,
    parser: _Parser,
    expr: _Node | None,
    default_action: _Node | None,
    ctx: CommandContext,
    state: _EvalState,
    newer_cache: dict[str, float],
) -> None:
    if state.quit:
        return

    match = _Match(path=display, abs_path=abs_path, info=info, depth=depth)

    pre_visit = not parser.depth_first
    state.pruned = False
    matched = True

    async def visit() -> None:
        nonlocal matched
        if parser.mindepth is not None and depth < parser.mindepth:
            matched = False
            return
        # Reset pruned flag for each visit
        # (state.pruned is mutated by -prune action)
        if expr is not None:
            matched = await _eval(expr, match, ctx, state, newer_cache)
        else:
            matched = True
        # If the user did not specify any "real" action that emits, run
        # the default.
        if matched and default_action is not None:
            await _exec_action(_Action(name=default_action.name, args=[]), match, ctx, state)  # type: ignore[arg-type]

    if pre_visit:
        await visit()

    descend = True
    if state.pruned:
        descend = False
    if state.quit:
        return
    if abs_path in state.deleted_paths:
        descend = False
    if parser.maxdepth is not None and depth >= parser.maxdepth:
        descend = False

    if _info_type(info) == "directory" and descend:
        children = await _gather_children(ctx.vfs, abs_path)
        if children is None:
            state.stderr.extend(encode(f"find: '{display}': Permission denied\n"))
            state.exit_code = 1
        else:
            children_sorted = sorted(children, key=lambda c: basename(c["name"]))
            for child in children_sorted:
                child_name = basename(child["name"])
                child_abs = _join(abs_path, child_name)
                child_display = _join(display, child_name)
                await _traverse(
                    child_display,
                    child_abs,
                    child,
                    depth + 1,
                    parser,
                    expr,
                    default_action,
                    ctx,
                    state,
                    newer_cache,
                )
                if state.quit:
                    return

    if not pre_visit:
        # depth-first / -depth flag: visit after children.
        await visit()


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------


@register("find")
async def cmd_find(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    paths, expr_tokens, split_err = _split_paths_and_expr(args)
    if split_err is not None:
        return fail(1, encode(split_err))

    parser = _Parser(expr_tokens)
    try:
        expr = parser.parse()
    except _ParseError as e:
        return fail(1, encode(e.message))

    if not paths:
        paths = ["."]

    # GNU find: implicit -print runs unless an "output-emitting" action exists
    # in the expression. -prune and -quit are side-effect-only and do not
    # suppress the default -print. -delete suppresses default -print.
    default_action: _Node | None
    if expr is not None and _expr_has_output_action(expr):
        default_action = None
    else:
        default_action = _Action(name="-print")

    state = _EvalState(
        stdout=bytearray(),
        stderr=bytearray(),
        exit_code=0,
        quit=False,
        pruned=False,
        deleted_paths=set(),
    )
    newer_cache: dict[str, float] = {}

    for raw_path in paths:
        abs_path = raw_path if raw_path.startswith("/") else resolve_cwd(ctx.env, raw_path)
        try:
            info = await ctx.vfs._info(abs_path)
        except FileNotFoundError:
            state.stderr.extend(encode(find_no_file(raw_path)))
            state.exit_code = 1
            continue
        except OSError as e:
            state.stderr.extend(encode(f"find: '{raw_path}': {e.strerror or 'I/O error'}\n"))
            state.exit_code = 1
            continue
        await _traverse(
            display=raw_path,
            abs_path=abs_path,
            info=info,
            depth=0,
            parser=parser,
            expr=expr,
            default_action=default_action,
            ctx=ctx,
            state=state,
            newer_cache=newer_cache,
        )
        if state.quit:
            break

    return CommandResult(
        stdout=bytes(state.stdout),
        stderr=bytes(state.stderr),
        exit_code=state.exit_code,
    )


def _expr_has_output_action(node: _Node) -> bool:
    if isinstance(node, _Action):
        return node.name in ("-print", "-print0", "-ls", "-delete", "-exec", "-execdir")
    if isinstance(node, _Not):
        return _expr_has_output_action(node.inner)
    if isinstance(node, (_And, _Or)):
        return _expr_has_output_action(node.left) or _expr_has_output_action(node.right)
    return False
