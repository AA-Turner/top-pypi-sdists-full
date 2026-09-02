from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

_UNARY_FILE_OPS = {"-e", "-f", "-d", "-L", "-h", "-r", "-w", "-x", "-s"}
_UNARY_STR_OPS = {"-z", "-n"}
_UNARY_OPS = _UNARY_FILE_OPS | _UNARY_STR_OPS

_BINARY_STR_OPS = {"=", "==", "!=", "<", ">"}
_BINARY_NUM_OPS = {"-eq", "-ne", "-lt", "-le", "-gt", "-ge"}
_BINARY_OPS = _BINARY_STR_OPS | _BINARY_NUM_OPS


class _TestError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _to_int(s: str) -> int:
    try:
        return int(s)
    except ValueError as e:
        raise _TestError(f"{s}: integer expression expected") from e


async def _file_op(op: str, path: str, vfs: object) -> bool:
    # Use VFS predicates and info — `_info` returns mode in octal int.
    if op == "-e":
        return bool(await vfs._exists(path))  # type: ignore[attr-defined]
    if op == "-f":
        return bool(await vfs._isfile(path))  # type: ignore[attr-defined]
    if op == "-d":
        return bool(await vfs._isdir(path))  # type: ignore[attr-defined]
    if op in ("-L", "-h"):
        try:
            info = await vfs._info(path)  # type: ignore[attr-defined]
        except FileNotFoundError:
            return False
        except Exception:
            return False
        return info.get("type") == "link"
    if op == "-r" or op == "-w":
        # In our VFS we don't truly enforce read/write permissions — exists ⇒ readable/writable.
        return bool(await vfs._exists(path))  # type: ignore[attr-defined]
    if op == "-x":
        try:
            info = await vfs._info(path)  # type: ignore[attr-defined]
        except FileNotFoundError:
            return False
        except Exception:
            return False
        if info.get("type") != "file":
            return False
        mode = int(info.get("mode") or 0)
        return (mode & 0o111) != 0
    if op == "-s":
        try:
            info = await vfs._info(path)  # type: ignore[attr-defined]
        except FileNotFoundError:
            return False
        except Exception:
            return False
        if info.get("type") == "directory":
            return False
        return int(info.get("size") or 0) > 0
    raise _TestError(f"{op}: unary operator expected")


async def _eval_unary(op: str, arg: str, vfs: object) -> bool:
    if op == "-z":
        return len(arg) == 0
    if op == "-n":
        return len(arg) > 0
    if op in _UNARY_FILE_OPS:
        return await _file_op(op, arg, vfs)
    raise _TestError(f"{op}: unary operator expected")


def _eval_binary(left: str, op: str, right: str) -> bool:
    if op in ("=", "=="):
        return left == right
    if op == "!=":
        return left != right
    if op == "<":
        return left < right
    if op == ">":
        return left > right
    if op == "-eq":
        return _to_int(left) == _to_int(right)
    if op == "-ne":
        return _to_int(left) != _to_int(right)
    if op == "-lt":
        return _to_int(left) < _to_int(right)
    if op == "-le":
        return _to_int(left) <= _to_int(right)
    if op == "-gt":
        return _to_int(left) > _to_int(right)
    if op == "-ge":
        return _to_int(left) >= _to_int(right)
    raise _TestError(f"{op}: binary operator expected")


# --------------------------------------------------------------------------
# Recursive-descent parser/evaluator for test expressions.
#
# Grammar (POSIX-flavored):
#   expr   ::= or
#   or     ::= and ( '-o' and )*
#   and    ::= not ( '-a' not )*
#   not    ::= '!' not | primary
#   primary::= '(' expr ')' | unary | binary | string
# --------------------------------------------------------------------------


class _Parser:
    __slots__ = ("toks", "pos", "vfs")

    def __init__(self, toks: list[str], vfs: object) -> None:
        self.toks = toks
        self.pos = 0
        self.vfs = vfs

    def _peek(self) -> str | None:
        if self.pos >= len(self.toks):
            return None
        return self.toks[self.pos]

    def _advance(self) -> str:
        t = self.toks[self.pos]
        self.pos += 1
        return t

    async def parse(self) -> bool:
        result = await self._or()
        if self.pos != len(self.toks):
            raise _TestError(f"{self.toks[self.pos]}: unexpected argument")
        return result

    async def _or(self) -> bool:
        left = await self._and()
        while self._peek() == "-o":
            self._advance()
            right = await self._and()
            left = left or right
        return left

    async def _and(self) -> bool:
        left = await self._not()
        while self._peek() == "-a":
            self._advance()
            right = await self._not()
            left = left and right
        return left

    async def _not(self) -> bool:
        if self._peek() == "!":
            self._advance()
            return not await self._not()
        return await self._primary()

    async def _primary(self) -> bool:
        tok = self._peek()
        if tok is None:
            raise _TestError("argument expected")

        if tok == "(":
            self._advance()
            value = await self._or()
            close = self._peek()
            if close != ")":
                raise _TestError("')' expected")
            self._advance()
            return value

        remaining = len(self.toks) - self.pos

        # Try a 3-token binary form first, since some operators (-eq, =, etc.)
        # take precedence over a treat-as-string fallback.
        if remaining >= 3:
            mid = self.toks[self.pos + 1]
            if mid in _BINARY_OPS:
                left = self._advance()
                op = self._advance()
                right = self._advance()
                return _eval_binary(left, op, right)

        # Unary operator (2 tokens).
        if remaining >= 2 and tok in _UNARY_OPS:
            self._advance()
            arg = self._advance()
            return await _eval_unary(tok, arg, self.vfs)

        # Single token: truthy iff non-empty (matches `test STRING`).
        if tok in _UNARY_OPS:
            # Trailing unary with no operand → treat as the token itself
            # (POSIX: `test -e` is true since "-e" is non-empty). But in
            # bash this errors. We follow bash for unary file ops.
            raise _TestError(f"{tok}: argument expected")

        self._advance()
        return len(tok) > 0


async def _evaluate(toks: list[str], vfs: object) -> bool:
    if not toks:
        return False
    if len(toks) == 1:
        return len(toks[0]) > 0
    parser = _Parser(toks, vfs)
    return await parser.parse()


@register("test")
async def cmd_test(ctx: CommandContext) -> CommandResult:
    try:
        result = await _evaluate(list(ctx.args), ctx.vfs)
    except _TestError as e:
        return fail(2, encode(f"bash: test: {e.message}\n"))
    return ok() if result else fail(1)


@register("[")
async def cmd_lbracket(ctx: CommandContext) -> CommandResult:
    args = list(ctx.args)
    if not args or args[-1] != "]":
        return fail(2, encode("bash: [: missing ']'\n"))
    inner = args[:-1]
    try:
        result = await _evaluate(inner, ctx.vfs)
    except _TestError as e:
        return fail(2, encode(f"bash: [: {e.message}\n"))
    return ok() if result else fail(1)
