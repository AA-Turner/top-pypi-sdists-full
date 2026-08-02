"""Builtin bash tool for the Vibe SDK.

Runs a shell command via ``asyncio.create_subprocess_shell`` and returns its
captured stdout / stderr / returncode. No approval / sandbox layer — every
command the agent picks is executed.
"""

import asyncio
import contextlib
import os
from typing import Any

import structlog
from pydantic import BaseModel, Field

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.utils import is_windows

logger = structlog.get_logger()


# Hardcoded — not exposed to the agent. Tune in source if needed.
DEFAULT_TIMEOUT_SECONDS = 300
MAX_OUTPUT_BYTES = 16_000

# TEMPORARY (workflow team escape hatch).
#
# When set to "1", bash discards subprocess stdout/stderr at the OS level
# (passes ``DEVNULL`` instead of ``PIPE``). The returned ``BashResult`` then
# has empty ``stdout`` / ``stderr`` strings; only ``returncode`` is meaningful.
#
# This mirrors what the workflow team currently achieves by monkey-patching
# ``asyncio.create_subprocess_shell`` in their stack to default both streams
# to ``DEVNULL``. Giving them an env-driven option here lets them drop the
# global monkey-patch and use the SDK's bash builtin unchanged.
#
# Remove once the workflow team no longer relies on this.
DISCARD_SUBPROCESS_OUTPUT_ENV_VAR = "VIBE_SDK_DISCARD_SUBPROCESS_OUTPUT"


class BashArgs(BaseModel):
    command: str = Field(description="Shell command to execute.")
    timeout_seconds: int = Field(
        default=DEFAULT_TIMEOUT_SECONDS,
        gt=0,
        description="Maximum time to wait for the command to finish.",
    )


class BashResult(BaseModel):
    command: str
    stdout: str
    stderr: str
    returncode: int


@tool(
    name="bash",
    description="Run a shell command and capture its stdout, stderr, and return code.",
    input_schema=BashArgs,
    result_schema=BashResult,
)
async def bash(args: BashArgs) -> BashResult:
    proc: asyncio.subprocess.Process | None = None
    try:
        kwargs: dict[str, Any] = {} if is_windows() else {"start_new_session": True}
        stdout_target, stderr_target = _subprocess_output_targets()
        proc = await asyncio.create_subprocess_shell(
            args.command,
            stdout=stdout_target,
            stderr=stderr_target,
            stdin=asyncio.subprocess.DEVNULL,
            env=_base_env(),
            executable=_shell_executable(),
            **kwargs,
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(),
                timeout=args.timeout_seconds,
            )
        except TimeoutError as exc:
            await _kill(proc)
            raise ValueError(
                f"Command timed out after {args.timeout_seconds}s: {args.command!r}"
            ) from exc

        encoding = _subprocess_encoding()
        # Slice raw bytes BEFORE decoding so MAX_OUTPUT_BYTES is a true byte cap
        # (slicing after decode counts characters, which is up to 4× larger).
        stdout = (
            stdout_bytes[:MAX_OUTPUT_BYTES].decode(encoding, errors="replace")
            if stdout_bytes
            else ""
        )
        stderr = (
            stderr_bytes[:MAX_OUTPUT_BYTES].decode(encoding, errors="replace")
            if stderr_bytes
            else ""
        )
        returncode = proc.returncode or 0

        if returncode != 0:
            error_lines = [
                f"Command failed: {args.command!r}",
                f"Return code: {returncode}",
            ]
            if stderr:
                error_lines.append(f"Stderr: {stderr}")
            if stdout:
                error_lines.append(f"Stdout: {stdout}")
            raise ValueError("\n".join(error_lines))

        return BashResult(
            command=args.command,
            stdout=stdout,
            stderr=stderr,
            returncode=returncode,
        )
    except asyncio.CancelledError:
        if proc is not None:
            await _kill(proc)
        raise
    except ValueError:
        # Already a clean tool-side error; let it propagate.
        raise
    except Exception as exc:
        logger.exception("bash.execution_failed", command=args.command)
        raise ValueError(f"Error running {args.command!r}: {exc}") from exc
    finally:
        if proc is not None:
            await _kill(proc)


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------


def _subprocess_output_targets() -> tuple[int, int]:
    """Return the ``(stdout, stderr)`` file descriptor targets for the subprocess.

    See ``DISCARD_SUBPROCESS_OUTPUT_ENV_VAR`` — temporary workflow-team escape hatch.
    """
    if os.environ.get(DISCARD_SUBPROCESS_OUTPUT_ENV_VAR) == "1":
        return asyncio.subprocess.DEVNULL, asyncio.subprocess.DEVNULL
    return asyncio.subprocess.PIPE, asyncio.subprocess.PIPE


def _subprocess_encoding() -> str:
    if is_windows():
        import ctypes

        return f"cp{ctypes.windll.kernel32.GetOEMCP()}"  # type: ignore[attr-defined]
    return "utf-8"


def _shell_executable() -> str | None:
    if is_windows():
        return None
    return os.environ.get("SHELL")


def _base_env() -> dict[str, str]:
    env = {**os.environ, "CI": "true", "NONINTERACTIVE": "1", "NO_TTY": "1"}
    if is_windows():
        env["GIT_PAGER"] = "more"
        env["PAGER"] = "more"
    else:
        env["TERM"] = "dumb"
        env["DEBIAN_FRONTEND"] = "noninteractive"
        env["GIT_PAGER"] = "cat"
        env["PAGER"] = "cat"
        env["LESS"] = "-FX"
        env["LC_ALL"] = "en_US.UTF-8"
    return env


async def _kill(proc: asyncio.subprocess.Process) -> None:
    """Force-terminate a subprocess and its process group, then wait."""
    if proc.returncode is not None:
        return
    try:
        if is_windows():
            try:
                killer = await asyncio.create_subprocess_exec(
                    "taskkill",
                    "/F",
                    "/T",
                    "/PID",
                    str(proc.pid),
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                await killer.wait()
            except (FileNotFoundError, OSError):
                proc.terminate()
        else:
            import signal

            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        await proc.wait()
    except (ProcessLookupError, PermissionError, OSError):
        pass
