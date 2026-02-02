import asyncio
import codecs
import os
import platform
import shutil
import signal
from collections.abc import AsyncGenerator, Callable
from typing import Any

from exponent.core.remote_execution.default_env import get_process_env
from exponent.core.remote_execution.languages.types import (
    ShellExecutionResult,
    StreamedOutputPiece,
)

STDOUT_FD = 1
STDERR_FD = 2
MAX_TIMEOUT = 300
# Timeout for draining remaining output after process exits
# This handles cases where background processes inherit pipes
DRAIN_TIMEOUT = 0.1
# Interval for polling process exit status
PROCESS_POLL_INTERVAL = 0.05


def get_rc_file_source_command(shell_path: str) -> str:
    """
    Returns a command to source the user's shell rc file
    Login profiles are already sourced via the -l flag
    """
    # On Windows, shell behavior is different
    if platform.system() == "Windows":
        return ""  # Windows shells don't typically use rc files in the same way

    shell_name = os.path.basename(shell_path)
    home_dir = os.path.expanduser("~")

    if shell_name == "zsh":
        zshrc = os.path.join(home_dir, ".zshrc")
        if os.path.exists(zshrc):
            return f"source {zshrc} 2>/dev/null || true; "
    elif shell_name == "bash":
        bashrc = os.path.join(home_dir, ".bashrc")
        if os.path.exists(bashrc):
            return f"source {bashrc} 2>/dev/null || true; "

    return ""  # No rc file found or unsupported shell


async def read_stream_chunk(
    stream: asyncio.StreamReader,
    fd: int,
    output: list[tuple[int, str]],
    decoder: codecs.IncrementalDecoder,
) -> StreamedOutputPiece | None:
    """
    Read a single chunk from the stream.
    Returns a StreamedOutputPiece if data was read, None if EOF.
    """
    try:
        data = await stream.read(50_000)
        if not data:
            # EOF - flush any remaining bytes in decoder
            chunk = decoder.decode(b"", final=True)
            if chunk:
                output.append((fd, chunk))
                return StreamedOutputPiece(content=chunk)
            return None
        chunk = decoder.decode(data, final=False)
        if chunk:
            output.append((fd, chunk))
            return StreamedOutputPiece(content=chunk)
        # Empty chunk after decode (partial multi-byte sequence), return empty piece
        return StreamedOutputPiece(content="")
    except asyncio.CancelledError:
        raise
    except Exception:
        return None


async def execute_shell_streaming(
    code: str,
    working_directory: str,
    timeout: int,
    should_halt: Callable[[], bool] | None = None,
    env: dict[str, str] | None = None,
) -> AsyncGenerator[StreamedOutputPiece | ShellExecutionResult, None]:
    timeout_seconds = min(timeout, MAX_TIMEOUT)

    shell_path = os.environ.get("SHELL") or shutil.which("bash") or shutil.which("sh")

    # Track whether we created a process group (for proper cleanup)
    uses_process_group = False

    if not shell_path:
        process = await asyncio.create_subprocess_shell(
            code,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
            env=get_process_env(env),
        )
    else:
        # Add rc file sourcing to the command
        rc_source_cmd = get_rc_file_source_command(shell_path)
        full_command = f"{rc_source_cmd}{code}"

        process = await asyncio.create_subprocess_exec(
            shell_path,
            "-l",
            "-c",
            full_command,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_directory,
            env=get_process_env(env),
            start_new_session=True if platform.system() != "Windows" else False,
        )
        uses_process_group = platform.system() != "Windows"

    exit_code = None
    output: list[tuple[int, str]] = []
    halted = False
    timed_out = False
    process_exited = False  # Shared flag to signal process exit to halt monitor
    assert process.stdout
    assert process.stderr

    async def monitor_halt() -> None:
        nonlocal halted

        while True:
            if should_halt and should_halt():
                # Set halted flag BEFORE killing so main loop sees it
                halted = True
                # Send signal to process group for proper interrupt propagation
                try:
                    if uses_process_group:
                        # Send SIGTERM to the process group
                        try:
                            os.killpg(process.pid, signal.SIGTERM)
                        except OSError:
                            # Fallback if not a process group leader
                            process.terminate()
                        # Wait briefly for process to terminate
                        for _ in range(20):  # 2 seconds max
                            if process.returncode is not None or process_exited:
                                break
                            await asyncio.sleep(0.1)
                        else:
                            # Fall back to SIGKILL
                            try:
                                os.killpg(process.pid, signal.SIGKILL)
                            except OSError:
                                process.kill()
                    else:
                        # No process group - use regular terminate/kill
                        process.terminate()
                        for _ in range(20):  # 2 seconds max
                            if process.returncode is not None or process_exited:
                                break
                            await asyncio.sleep(0.1)
                        else:
                            process.kill()
                except ProcessLookupError:
                    # Process already terminated
                    pass
                break
            if process.returncode is not None or process_exited:
                break
            await asyncio.sleep(0.1)

    def on_timeout() -> None:
        nonlocal timed_out
        timed_out = True
        try:
            if uses_process_group:
                # Kill the entire process group, not just the shell process
                # This is critical because the shell was started with start_new_session=True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    # Fallback to killing just the process if killpg fails
                    # (e.g., if process is not actually a group leader)
                    process.kill()
            else:
                process.kill()
        except ProcessLookupError:
            pass

    try:
        halt_task = asyncio.create_task(monitor_halt()) if should_halt else None
        timeout_handle = asyncio.get_running_loop().call_later(
            timeout_seconds, on_timeout
        )

        # Create decoders for each stream
        stdout_decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
        stderr_decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

        # Create initial read tasks
        stdout_task: asyncio.Task[StreamedOutputPiece | None] | None = (
            asyncio.create_task(
                read_stream_chunk(process.stdout, STDOUT_FD, output, stdout_decoder)
            )
        )
        stderr_task: asyncio.Task[StreamedOutputPiece | None] | None = (
            asyncio.create_task(
                read_stream_chunk(process.stderr, STDERR_FD, output, stderr_decoder)
            )
        )

        # Helper to check if process has exited using os.waitpid with WNOHANG
        # This is needed because asyncio's process.wait() waits for BOTH process
        # exit AND pipe EOF, which blocks when background processes inherit pipes
        def check_process_exited() -> int | None:
            """Check if process exited without blocking. Returns exit code or None."""
            if process.returncode is not None:
                return process.returncode
            if platform.system() == "Windows":
                # On Windows, we can't use waitpid, fall back to polling returncode
                return process.returncode
            try:
                pid, status = os.waitpid(process.pid, os.WNOHANG)
                if pid != 0:
                    # Process has exited - extract exit code
                    if os.WIFEXITED(status):
                        return os.WEXITSTATUS(status)
                    elif os.WIFSIGNALED(status):
                        return -os.WTERMSIG(status)
                    return -1
            except ChildProcessError:
                # Process already reaped
                return process.returncode if process.returncode is not None else 0
            return None

        # Stream output until the process exits
        # We poll for process exit using os.waitpid(WNOHANG) because asyncio's
        # process.wait() waits for pipes to close, which blocks when background
        # processes inherit the pipes
        while True:
            # Check if halted by monitor_halt task
            if halted:
                break

            # Check if process has exited
            proc_exit_code = check_process_exited()
            if proc_exit_code is not None:
                exit_code = proc_exit_code
                process_exited = True
                # Give halt monitor a chance to set halted flag if it killed the process
                # This handles the race where we detect exit before halted is set
                await asyncio.sleep(0)
                break

            # Build set of pending read tasks
            pending: set[asyncio.Task[Any]] = set()
            if stdout_task is not None:
                pending.add(stdout_task)
            if stderr_task is not None:
                pending.add(stderr_task)

            if not pending:
                # No read tasks, just poll for process exit
                await asyncio.sleep(PROCESS_POLL_INTERVAL)
                continue

            # Wait for output with a short timeout so we can check process exit
            done, _ = await asyncio.wait(
                pending,
                timeout=PROCESS_POLL_INTERVAL,
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Process any completed output tasks
            for task in done:
                try:
                    piece = await task
                    if piece is not None and piece.content:
                        yield piece

                    # Schedule next read from the same stream if not EOF
                    if task is stdout_task:
                        if piece is None or process.stdout.at_eof():
                            stdout_task = None
                        else:
                            stdout_task = asyncio.create_task(
                                read_stream_chunk(
                                    process.stdout, STDOUT_FD, output, stdout_decoder
                                )
                            )
                    elif task is stderr_task:
                        if piece is None or process.stderr.at_eof():
                            stderr_task = None
                        else:
                            stderr_task = asyncio.create_task(
                                read_stream_chunk(
                                    process.stderr, STDERR_FD, output, stderr_decoder
                                )
                            )
                except Exception:
                    # On any error, stop reading from that stream
                    if task is stdout_task:
                        stdout_task = None
                    elif task is stderr_task:
                        stderr_task = None

        # Process has exited - drain any remaining buffered output with a short timeout
        # This ensures we capture output that was written before the process exited,
        # but don't block indefinitely on background processes that inherited the pipes
        remaining_tasks: set[asyncio.Task[Any]] = set()
        if stdout_task is not None:
            remaining_tasks.add(stdout_task)
        if stderr_task is not None:
            remaining_tasks.add(stderr_task)

        if remaining_tasks:
            done, not_done = await asyncio.wait(
                remaining_tasks,
                timeout=DRAIN_TIMEOUT,
                return_when=asyncio.ALL_COMPLETED,
            )
            for task in done:
                try:
                    piece = await task
                    if piece is not None and piece.content:
                        yield piece
                except Exception:
                    pass
            # Cancel any tasks that didn't complete in time
            for task in not_done:
                task.cancel()
                try:
                    await task
                except (asyncio.CancelledError, Exception):
                    pass

        timeout_handle.cancel()

    except asyncio.CancelledError:
        # Kill the entire process group when cancelled
        try:
            if uses_process_group:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except OSError:
                    # Fallback to killing just the process if killpg fails
                    process.kill()
            else:
                process.kill()
        except ProcessLookupError:
            pass
        raise
    finally:
        # Explicitly kill the process if it's still running
        if process and process.returncode is None:
            try:
                if uses_process_group:
                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except OSError:
                        # Fallback if not a process group leader
                        process.terminate()
                else:
                    process.terminate()
            except ProcessLookupError:
                pass

        # Wait for the process to fully terminate to avoid subprocess transport warnings
        try:
            await process.wait()
        except Exception:
            pass

        # Explicitly close the subprocess transport to prevent warnings when the
        # event loop closes before garbage collection runs on the transport.
        # Note: _transport is a private API but there's no public way to close it.
        if hasattr(process, "_transport") and process._transport:
            process._transport.close()  # type: ignore[union-attr]

        # Cancel any remaining tasks
        tasks_to_cancel: list[asyncio.Task[Any]] = []
        if stdout_task is not None:
            tasks_to_cancel.append(stdout_task)
        if stderr_task is not None:
            tasks_to_cancel.append(stderr_task)
        if halt_task:
            tasks_to_cancel.append(halt_task)

        for task in tasks_to_cancel:
            task.cancel()
        await asyncio.gather(*tasks_to_cancel, return_exceptions=True)

    formatted_output = "".join([chunk for (_, chunk) in output]).strip() + "\n\n"

    yield ShellExecutionResult(
        output=formatted_output,
        cancelled_for_timeout=timed_out,
        exit_code=None if timed_out else exit_code,
        halted=halted,
    )
