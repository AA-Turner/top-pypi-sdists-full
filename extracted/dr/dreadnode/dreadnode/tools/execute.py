import asyncio
import contextlib
import os
import signal

from loguru import logger

from dreadnode.agents.tools import tool
from dreadnode.app.env import resolve_python_executable

# How long to wait after SIGTERM before escalating to SIGKILL.
_SIGKILL_ESCALATION_TIMEOUT = 5.0


async def _kill_process_group(proc: asyncio.subprocess.Process) -> None:
    """Terminate *proc* and its entire process group.

    Uses ``start_new_session=True`` at subprocess creation so the process
    is the leader of its own session/group.  Sends ``SIGTERM`` to the
    group first.  If the process is still alive after
    :data:`_SIGKILL_ESCALATION_TIMEOUT` seconds, ``SIGKILL`` is sent.
    """
    if proc.returncode is not None:
        return  # already exited

    pid = proc.pid
    if pid is None:
        return

    try:
        pgid = os.getpgid(pid)
    except (OSError, ProcessLookupError):
        return  # process already gone

    # --- SIGTERM --------------------------------------------------------
    with contextlib.suppress(OSError, ProcessLookupError):
        os.killpg(pgid, signal.SIGTERM)

    try:
        await asyncio.wait_for(proc.wait(), timeout=_SIGKILL_ESCALATION_TIMEOUT)
    except TimeoutError:
        # --- SIGKILL (escalation) --------------------------------------
        with contextlib.suppress(OSError, ProcessLookupError):
            os.killpg(pgid, signal.SIGKILL)

        with contextlib.suppress(ProcessLookupError):
            await proc.wait()


@tool
async def execute(
    cmd: list[str],
    *,
    timeout: int = 120,  # noqa: ASYNC109
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    input: str | None = None,
) -> str:
    """
    Execute a command without shell interpretation (safer).

    Arguments are passed directly to the executable without shell expansion.
    Use this when you have a specific command with known arguments.

    Args:
        cmd: Command and arguments as a list of strings.
        timeout: Maximum execution time in seconds.
        cwd: Working directory for the command.
        env: Additional environment variables.
        input: Text to send to stdin.

    Returns:
        Command output.
    """
    command_str = " ".join(cmd)
    logger.debug(f"Executing '{command_str}'")

    process_env = os.environ.copy()
    if env:
        process_env.update(env)

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        stdin=asyncio.subprocess.PIPE if input is not None else None,
        env=process_env,
        cwd=cwd,
        start_new_session=True,
    )

    output = ""

    async def read_stdout() -> None:
        nonlocal output

        if not proc.stdout:
            return

        while True:
            chunk = await proc.stdout.read(1024)
            if not chunk:
                break
            output += chunk.decode(errors="replace")

    async def write_and_close_stdin() -> None:
        if proc.stdin and input:
            proc.stdin.write(input.encode())
            await proc.stdin.drain()
            proc.stdin.close()

    try:
        await asyncio.wait_for(
            asyncio.gather(read_stdout(), write_and_close_stdin()), timeout=timeout
        )
        await proc.wait()

    except TimeoutError as e:
        error_message = f"Command '{command_str}' timed out after {timeout} seconds."
        if output:
            error_message += f"\n\nPartial Output:\n{output}"
        logger.warning(error_message)

        await _kill_process_group(proc)

        raise TimeoutError(error_message) from e

    if proc.returncode != 0:
        logger.error(
            f"Command '{command_str}' failed with return code {proc.returncode}:\n{output}"
        )
        raise RuntimeError(f"Command failed ({proc.returncode}):\n{output}")

    logger.debug(f"Command '{command_str}' completed:\n{output}")
    return output


@tool
async def bash(
    cmd: str,
    *,
    timeout: int = 120,  # noqa: ASYNC109
    cwd: str | None = None,
    env: dict[str, str] | None = None,
    input: str | None = None,
) -> str:
    """
    Execute a bash command in a subprocess.

    Use for shell commands, scripts, or operations requiring shell features.

    Args:
        cmd: Bash command to execute.
        timeout: Maximum execution time in seconds.
        cwd: Working directory for the command.
        env: Additional environment variables.
        input: Text to send to stdin.

    Returns:
        Command output.
    """
    return await execute(
        ["bash", "-c", cmd],
        timeout=timeout,
        cwd=cwd,
        env=env,
        input=input,
    )


@tool
async def python(
    code: str,
    *,
    timeout: int = 120,  # noqa: ASYNC109
    cwd: str | None = None,
    env: dict[str, str] | None = None,
) -> str:
    """
    Execute Python code in a subprocess.

    Use for custom logic, data processing, or operations not covered by other tools.
    Results must be printed to stdout to be captured.

    Args:
        code: Python code to execute.
        timeout: Maximum execution time in seconds.
        cwd: Working directory for the command.
        env: Additional environment variables.

    Returns:
        Python process output.
    """
    return await execute(
        [resolve_python_executable(), "-"],
        timeout=timeout,
        input=code,
        cwd=cwd,
        env=env,
    )
