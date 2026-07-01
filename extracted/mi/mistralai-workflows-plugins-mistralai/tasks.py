import logging
from typing import Any

from invoke.exceptions import Exit, Failure
from invoke.runners import Result, Runner
from invoke.tasks import task

logger = logging.getLogger(__name__)


def exec_command(c: Runner, command: str) -> int:
    res: Result | None = None
    try:
        res = c.run(command, pty=True, warn=True)
        return res.exited if res else 1
    except Failure:
        raise
    finally:
        msg = "\nExecuting done"
        msg += f" - Exit code: {res.exited}" if res else " - command never started"
        logger.debug(msg)


def exec_command_with_env(c: Runner, command: str, env: dict[str, str]) -> int:
    res: Result | None = None
    try:
        res = c.run(command, pty=True, warn=True, env=env)
        return res.exited if res else 1
    except Failure:
        raise
    finally:
        msg = "\nExecuting done"
        msg += f" - Exit code: {res.exited}" if res else " - command never started"
        logger.debug(msg)


def check_exit_codes(exit_codes: list[int | None]) -> None:
    for exit_code in exit_codes:
        if exit_code is not None and exit_code > 0:
            raise Exit(code=exit_code)


@task
def lint(c: Runner, fix: bool = False) -> None:
    format_command = "uv run ruff format ."
    check_command = "uv run ruff check ."
    if fix:
        check_command += " --fix"
    if not fix:
        format_command += " --check"
    exit_codes: list[int | None] = []
    exit_codes.append(exec_command(c, format_command))
    exit_codes.append(exec_command(c, check_command))
    check_exit_codes(exit_codes)


@task
def typecheck(c: Runner) -> None:
    command = "uv run mypy mistralai/workflows/"
    exit_code = exec_command(c, command)
    check_exit_codes([exit_code])


@task
def tests(
    c: Any,
    k: str | None = None,
    s: bool = False,
    v: bool = False,
    enforce_determinism: bool = True,
) -> None:
    test_command = "uv run pytest tests/"
    if s:
        test_command += " -s"
    if k:
        test_command += f" -k {k}"
    if v:
        test_command += " -v"
    env = {"DEFAULT_ENFORCE_DETERMINISM": "1" if enforce_determinism else "0"}
    try:
        result = exec_command_with_env(c, test_command, env)
        check_exit_codes([result])
    except Failure:
        raise
