from __future__ import annotations

from collections.abc import Awaitable, Callable

import pytest

from matrx_ai.tools.vfs.shell.env import ShellEnv
from matrx_ai.tools.vfs.shell.expansion import expand_word
from matrx_ai.tools.vfs.shell.parser import expand_braces, parse
from matrx_ai.tools.vfs.shell.runner import CommandResult, CommandRunner


class DictRunner(CommandRunner):
    def __init__(
        self,
        commands: dict[str, Callable[..., Awaitable[CommandResult]]] | None = None,
        files: dict[str, bytes] | None = None,
        glob_results: dict[str, list[str]] | None = None,
    ) -> None:
        self.commands = commands or {}
        self.files = files or {}
        self.glob_results = glob_results or {}
        self.glob_calls: list[tuple[str, str]] = []

    async def run(self, argv, env, stdin, cwd) -> CommandResult:
        cmd = argv[0]
        if cmd in self.commands:
            return await self.commands[cmd](argv, env, stdin, cwd)
        return CommandResult(b"", b"", 127)

    async def glob(
        self, pattern: str, cwd: str, *, globstar: bool = True, nullglob: bool = False
    ) -> list[str]:
        self.glob_calls.append((pattern, cwd))
        return list(self.glob_results.get(pattern, []))

    async def is_executable(self, name: str) -> bool:
        return name in self.commands

    async def read_file(self, path: str, env) -> bytes:
        if path in self.files:
            return self.files[path]
        raise FileNotFoundError(2, "no such file or directory", path)

    async def write_file(self, path: str, data: bytes, env, *, append: bool = False) -> None:
        if append and path in self.files:
            self.files[path] = self.files[path] + data
        else:
            self.files[path] = data


def _word(src: str):
    cl = parse(src)
    cmd = cl.items[0].pipelines[0].commands[0]
    return cmd.argv[0]


@pytest.fixture
def env() -> ShellEnv:
    e = ShellEnv()
    e.set("FOO", "bar")
    e.set("EMPTY", "")
    return e


@pytest.fixture
def runner() -> DictRunner:
    return DictRunner()


@pytest.mark.asyncio
async def test_var_substitution(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("$FOO")
    out = await expand_word(w, env, runner)
    assert out == ["bar"]


@pytest.mark.asyncio
async def test_var_default_when_unset(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("${UNSET:-defaultval}")
    out = await expand_word(w, env, runner)
    assert out == ["defaultval"]


@pytest.mark.asyncio
async def test_var_default_when_set(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("${FOO:-defaultval}")
    out = await expand_word(w, env, runner)
    assert out == ["bar"]


@pytest.mark.asyncio
async def test_var_alt_when_set(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("${FOO:+ALT}")
    out = await expand_word(w, env, runner)
    assert out == ["ALT"]


@pytest.mark.asyncio
async def test_var_alt_when_unset(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("${UNSET:+ALT}")
    out = await expand_word(w, env, runner)
    # bash: unquoted empty expansion produces no fields
    assert out == []


@pytest.mark.asyncio
async def test_var_alt_when_unset_quoted(env: ShellEnv, runner: DictRunner) -> None:
    w = _word('"${UNSET:+ALT}"')
    out = await expand_word(w, env, runner)
    assert out == [""]


@pytest.mark.asyncio
async def test_var_length(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("${#FOO}")
    out = await expand_word(w, env, runner)
    assert out == ["3"]


@pytest.mark.asyncio
async def test_special_question_mark(runner: DictRunner) -> None:
    e = ShellEnv()
    e.last_exit = 42
    w = _word("$?")
    out = await expand_word(w, e, runner)
    assert out == ["42"]


@pytest.mark.asyncio
async def test_tilde_expansion(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("~")
    out = await expand_word(w, env, runner)
    assert out == [env.get("HOME")]


@pytest.mark.asyncio
async def test_tilde_with_path(env: ShellEnv, runner: DictRunner) -> None:
    w = _word("~/foo/bar")
    out = await expand_word(w, env, runner)
    assert out == [env.get("HOME") + "/foo/bar"]


def test_brace_expansion_comma() -> None:
    assert expand_braces("a{x,y,z}b") == ["axb", "ayb", "azb"]


def test_brace_expansion_range() -> None:
    assert expand_braces("{1..5}") == ["1", "2", "3", "4", "5"]


def test_brace_expansion_char_range() -> None:
    assert expand_braces("{a..e}") == ["a", "b", "c", "d", "e"]


def test_brace_expansion_step() -> None:
    assert expand_braces("{1..10..2}") == ["1", "3", "5", "7", "9"]


def test_brace_no_braces() -> None:
    assert expand_braces("plain") == ["plain"]


@pytest.mark.asyncio
async def test_command_substitution_runs(env: ShellEnv) -> None:
    async def fake_echo(argv, env, stdin, cwd):
        return CommandResult(b" ".join(a.encode() for a in argv[1:]) + b"\n", b"", 0)

    runner = DictRunner(commands={"echo": fake_echo})
    w = _word("$(echo hi)")
    out = await expand_word(w, env, runner)
    assert out == ["hi"]


@pytest.mark.asyncio
async def test_command_substitution_strips_trailing_newlines(env: ShellEnv) -> None:
    async def fake(argv, env, stdin, cwd):
        return CommandResult(b"line1\nline2\n\n\n", b"", 0)

    runner = DictRunner(commands={"x": fake})
    w = _word("$(x)")
    out = await expand_word(w, env, runner)
    assert out == ["line1", "line2"]  # trailing newlines stripped, then split on IFS


@pytest.mark.asyncio
async def test_quoted_command_substitution_no_split(env: ShellEnv) -> None:
    async def fake(argv, env, stdin, cwd):
        return CommandResult(b"a b c\n", b"", 0)

    runner = DictRunner(commands={"x": fake})
    w = _word('"$(x)"')
    out = await expand_word(w, env, runner)
    assert out == ["a b c"]


@pytest.mark.asyncio
async def test_glob_expansion_matches(env: ShellEnv) -> None:
    runner = DictRunner(glob_results={"*.py": ["a.py", "b.py"]})
    w = _word("*.py")
    out = await expand_word(w, env, runner)
    assert out == ["a.py", "b.py"]


@pytest.mark.asyncio
async def test_glob_no_match_default(env: ShellEnv) -> None:
    runner = DictRunner()
    w = _word("*.nope")
    out = await expand_word(w, env, runner)
    # bash default: leave pattern in place
    assert out == ["*.nope"]


@pytest.mark.asyncio
async def test_glob_no_match_nullglob(env: ShellEnv) -> None:
    env.shell_opts["nullglob"] = True
    runner = DictRunner()
    w = _word("*.nope")
    out = await expand_word(w, env, runner)
    assert out == []


@pytest.mark.asyncio
async def test_word_splitting(env: ShellEnv) -> None:
    env.set("LIST", "a b c")
    runner = DictRunner()
    w = _word("$LIST")
    out = await expand_word(w, env, runner)
    assert out == ["a", "b", "c"]


@pytest.mark.asyncio
async def test_quoted_var_no_split(env: ShellEnv) -> None:
    env.set("LIST", "a b c")
    runner = DictRunner()
    w = _word('"$LIST"')
    out = await expand_word(w, env, runner)
    assert out == ["a b c"]


@pytest.mark.asyncio
async def test_arithmetic_expansion(env: ShellEnv) -> None:
    runner = DictRunner()
    w = _word("$((2 + 3))")
    out = await expand_word(w, env, runner)
    assert out == ["5"]


@pytest.mark.asyncio
async def test_arithmetic_with_var(env: ShellEnv) -> None:
    env.set("N", "10")
    runner = DictRunner()
    w = _word("$((N * 2))")
    out = await expand_word(w, env, runner)
    assert out == ["20"]
