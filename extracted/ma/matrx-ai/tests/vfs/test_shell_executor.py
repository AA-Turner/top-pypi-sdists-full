from __future__ import annotations

from collections.abc import Awaitable, Callable

import pytest

from matrx_ai.tools.vfs.shell.env import ShellEnv
from matrx_ai.tools.vfs.shell.executor import execute
from matrx_ai.tools.vfs.shell.parser import parse
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
        self.run_log: list[tuple[list[str], bytes]] = []

    async def run(self, argv, env, stdin, cwd) -> CommandResult:
        self.run_log.append((argv, stdin))
        cmd = argv[0]
        if cmd in self.commands:
            return await self.commands[cmd](argv, env, stdin, cwd)
        return CommandResult(b"", b"", 127)

    async def glob(
        self, pattern: str, cwd: str, *, globstar: bool = True, nullglob: bool = False
    ) -> list[str]:
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


async def _echo(argv, env, stdin, cwd):
    text = " ".join(argv[1:]) + "\n"
    return CommandResult(text.encode(), b"", 0)


async def _cat(argv, env, stdin, cwd):
    if len(argv) > 1:
        return CommandResult(b"", b"", 1)  # tests should use stdin
    return CommandResult(stdin, b"", 0)


async def _true(argv, env, stdin, cwd):
    return CommandResult(b"", b"", 0)


async def _false(argv, env, stdin, cwd):
    return CommandResult(b"", b"", 1)


async def _printvar(argv, env, stdin, cwd):
    name = argv[1]
    val = env.get(name, "<unset>")
    return CommandResult(val.encode() + b"\n", b"", 0)


def _basic_runner(**extra) -> DictRunner:
    cmds: dict[str, Callable] = {
        "echo": _echo,
        "cat": _cat,
        "true": _true,
        "false": _false,
        "printvar": _printvar,
    }
    cmds.update(extra)
    return DictRunner(commands=cmds)


@pytest.mark.asyncio
async def test_simple_echo_pipeline_capture() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("echo hi")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"hi\n"
    assert res.exit_code == 0


@pytest.mark.asyncio
async def test_pipeline_pipes_stdout_to_stdin() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("echo hi | cat")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"hi\n"
    assert res.exit_code == 0


@pytest.mark.asyncio
async def test_andand_short_circuits_on_failure() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("false && echo nope")
    res = await execute(cl, env, runner, capture=True)
    # echo never ran => stdout empty
    assert res.stdout == b""
    assert res.exit_code != 0
    # confirm echo never invoked
    assert not any(a[0] == "echo" for a, _ in runner.run_log)


@pytest.mark.asyncio
async def test_oror_short_circuits_on_success() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("true || echo skip")
    res = await execute(cl, env, runner, capture=True)
    assert res.exit_code == 0
    assert not any(a[0] == "echo" for a, _ in runner.run_log)


@pytest.mark.asyncio
async def test_oror_runs_when_first_fails() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("false || echo recovered")
    res = await execute(cl, env, runner, capture=True)
    assert res.exit_code == 0
    assert res.stdout == b"recovered\n"


@pytest.mark.asyncio
async def test_redirect_stdout_writes_via_runner() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("echo hi > /tmp/x.txt")
    res = await execute(cl, env, runner, capture=True)
    assert res.exit_code == 0
    assert runner.files["/tmp/x.txt"] == b"hi\n"


@pytest.mark.asyncio
async def test_redirect_append() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    runner.files["/tmp/log"] = b"existing\n"
    cl = parse("echo more >> /tmp/log")
    await execute(cl, env, runner, capture=True)
    assert runner.files["/tmp/log"] == b"existing\nmore\n"


@pytest.mark.asyncio
async def test_redirect_stdin_reads_via_runner() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    runner.files["/tmp/x.txt"] = b"hello\n"
    cl = parse("cat < /tmp/x.txt")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"hello\n"


@pytest.mark.asyncio
async def test_command_list_runs_all() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("echo a; echo b; echo c")
    res = await execute(cl, env, runner, capture=True)
    # capture mode collects the shell's full stdout stream
    assert res.stdout == b"a\nb\nc\n"
    invoked = [a[1] for a, _ in runner.run_log if a[0] == "echo"]
    assert invoked == ["a", "b", "c"]


@pytest.mark.asyncio
async def test_errexit_off_continues_after_failure() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("false; echo hi")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"hi\n"


@pytest.mark.asyncio
async def test_errexit_on_stops_after_failure() -> None:
    env = ShellEnv()
    env.shell_opts["errexit"] = True
    runner = _basic_runner()
    cl = parse("false; echo hi")
    res = await execute(cl, env, runner, capture=True)
    assert res.exit_code != 0
    # echo never ran
    assert not any(a[0] == "echo" for a, _ in runner.run_log)


@pytest.mark.asyncio
async def test_subshell_does_not_leak_env() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("(VAR=foo; printvar VAR); printvar VAR")
    res = await execute(cl, env, runner, capture=True)
    # subshell prints "foo", outer prints "<unset>" because VAR didn't leak
    assert res.stdout == b"foo\n<unset>\n"


@pytest.mark.asyncio
async def test_assignment_only_persists() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("FOO=bar; printvar FOO")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"bar\n"


@pytest.mark.asyncio
async def test_assignment_prefix_scoped_to_command() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("FOO=hello printvar FOO; printvar FOO")
    res = await execute(cl, env, runner, capture=True)
    # First command sees FOO=hello via prefix; second sees unset (prefix scoped)
    assert res.stdout == b"hello\n<unset>\n"


@pytest.mark.asyncio
async def test_command_not_found_message() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("nosuchcmd")
    res = await execute(cl, env, runner, capture=True)
    assert res.exit_code == 127
    assert b"command not found" in res.stderr


@pytest.mark.asyncio
async def test_negated_pipeline() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("! false")
    res = await execute(cl, env, runner)
    assert res.exit_code == 0


@pytest.mark.asyncio
async def test_heredoc_provides_stdin() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("cat <<EOF\nhello world\nEOF\n")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"hello world\n"


@pytest.mark.asyncio
async def test_heredoc_quoted_no_expansion() -> None:
    env = ShellEnv()
    env.set("X", "expanded")
    runner = _basic_runner()
    cl = parse("cat <<'EOF'\n$X stays\nEOF\n")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"$X stays\n"


@pytest.mark.asyncio
async def test_heredoc_unquoted_expands() -> None:
    env = ShellEnv()
    env.set("X", "expanded")
    runner = _basic_runner()
    cl = parse("cat <<EOF\n$X here\nEOF\n")
    res = await execute(cl, env, runner, capture=True)
    assert res.stdout == b"expanded here\n"


@pytest.mark.asyncio
async def test_pipefail_off_uses_last_exit() -> None:
    env = ShellEnv()
    runner = _basic_runner()
    cl = parse("false | true")
    res = await execute(cl, env, runner)
    assert res.exit_code == 0


@pytest.mark.asyncio
async def test_pipefail_on_uses_first_failure() -> None:
    env = ShellEnv()
    env.shell_opts["pipefail"] = True
    runner = _basic_runner()
    cl = parse("false | true")
    res = await execute(cl, env, runner)
    assert res.exit_code != 0
