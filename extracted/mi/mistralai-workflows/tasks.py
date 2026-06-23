import logging
import os
from pathlib import Path
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
def lock(c: Runner) -> None:
    """Regenerate uv.lock for workflow_sdk and all packages that transitively depend on mistralai-workflows.

    Uses the reverse dependency graph (via [tool.uv.sources] path entries) to find all
    transitive dependents and re-locks them. Use this after editing pyproject.toml.
    """
    exit_codes = [
        exec_command(c, "uv lock"),
        exec_command(c, "uv run python ../scripts/renovate/cascade_uv_lock.py workflow_sdk"),
    ]
    check_exit_codes(exit_codes)


@task
def get_api_key(c: Runner) -> str | None:
    api_key_file = Path("../abraxas/.api_key")
    if api_key_file.exists():
        return api_key_file.read_text().strip()
    return None


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
def check_api_surface(c: Runner, base_ref: str = "origin/main") -> None:
    public_api_check = (
        f"uv --project workflow_sdk run python workflow_sdk/scripts/check_public_api.py --base-ref {base_ref}"
    )
    griffe_check = (
        f"uv --project workflow_sdk run griffe check mistralai.workflows -b HEAD -a {base_ref} "
        "-s workflow_sdk -s workflow_sdk/worker_client/src"
    )
    exit_codes: list[int | None] = []
    exit_codes.append(exec_command(c, f"cd .. && {public_api_check}"))
    exit_codes.append(exec_command(c, f"cd .. && {griffe_check}"))
    if any(code is not None and code > 0 for code in exit_codes):
        YELLOW = "\033[93m"
        BOLD = "\033[1m"
        RESET = "\033[0m"
        print(f"\n{YELLOW}{'━' * 70}{RESET}")  # noqa: T201
        print(f"{BOLD}To proceed:{RESET}")  # noqa: T201
        print("  1. Document breaking changes in PR description")  # noqa: T201
        print(f"  2. Add the {BOLD}'breaking-sdk'{RESET} label to your PR")  # noqa: T201
        print(f"{YELLOW}{'━' * 70}{RESET}\n")  # noqa: T201
    check_exit_codes(exit_codes)


@task
def tests(
    c: Any,
    k: str | None = None,
    s: bool = False,
    v: bool = False,
    splits: str | None = None,
    group: str | None = None,
    store_durations: bool = False,
    n: str | None = None,
    timeout: float | None = None,
    enforce_determinism: bool = True,
) -> None:
    test_command = "uv run pytest tests/ -m 'not integration'"
    if s:
        test_command += " -s"
    if k:
        test_command += f" -k {k}"
    if v:
        test_command += " -v"
    if splits:
        test_command += f" --splits {splits}"
    if group:
        test_command += f" --group {group}"
    if store_durations:
        test_command += " --store-durations"
    if n:
        test_command += f" -n {n}"
    else:
        test_command += " -n auto"
    if timeout is not None:
        test_command += f" --timeout={timeout}"
    env = {"DEFAULT_ENFORCE_DETERMINISM": "1" if enforce_determinism else "0"}
    try:
        result = exec_command_with_env(c, test_command, env)
        check_exit_codes([result])
    except Failure:
        raise


@task
def integration_tests(
    c: Any,
    k: str | None = None,
    s: bool = False,
    v: bool = False,
    n: str | None = None,
) -> None:
    """
    Integration tests have moved to workflow_sdk_tests/.
    This task now delegates to the new package. For webhook plugin integration tests,
    those remain at plugins/webhook/tests/integration.

    Prerequisites: Dev environment must be running in abraxas (../abraxas).
    The MISTRAL_API_KEY environment variable must be set or ../abraxas/.api_key file must exist.
    """
    api_key = get_api_key(c)
    if not api_key:
        api_key = os.environ.get("MISTRAL_API_KEY")

    if not api_key:
        logger.error("MISTRAL_API_KEY environment variable is not set and ../abraxas/.api_key file not found.")
        logger.error("Please start the dev environment with 'cd ../abraxas && make dev'.")
        raise Exit(code=1)

    env: dict[str, str] = {"MISTRAL_API_KEY": api_key}

    exit_codes: list[int | None] = []

    # Run the main integration tests from the new package
    sdk_tests_cmd = "uv run --directory ../workflow_sdk_tests invoke integration-tests"
    if s:
        sdk_tests_cmd += " -s"
    if k:
        sdk_tests_cmd += f" -k {k}"
    if v:
        sdk_tests_cmd += " -v"
    if n:
        sdk_tests_cmd += f" -n {n}"
    exit_codes.append(exec_command_with_env(c, sdk_tests_cmd, env))

    # Run webhook plugin integration tests (still in this repo)
    webhook_cmd = "uv run --extra webhook pytest plugins/webhook/tests/integration -m integration"
    if s:
        webhook_cmd += " -s"
    if k:
        webhook_cmd += f" -k {k}"
    if v:
        webhook_cmd += " -v"
    if n:
        webhook_cmd += f" -n {n}"
    else:
        webhook_cmd += " -n auto"
    exit_codes.append(exec_command_with_env(c, webhook_cmd, env))

    check_exit_codes(exit_codes)
