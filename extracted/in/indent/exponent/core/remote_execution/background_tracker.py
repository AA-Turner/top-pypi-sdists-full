"""Background process tracking for bash commands."""

import asyncio
import logging
import os
import time
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

MAX_OUTPUT_SIZE = 50000


@dataclass
class TrackedProcess:
    """Information about a tracked background process."""

    pid: int
    output_file: str
    command: str
    correlation_id: str
    start_time: float = field(default_factory=time.time)


class BackgroundProcessTracker:
    """Tracks background bash processes and notifies when they complete.

    When a background process is spawned, it can be registered with this tracker.
    The tracker will monitor the process and call the on_complete callback when
    the process exits, providing the exit code and captured output.
    """

    def __init__(
        self,
        on_complete: Callable[
            [TrackedProcess, int, str, bool, int], Coroutine[Any, Any, None]
        ],
    ):
        """Initialize the tracker.

        Args:
            on_complete: Async callback called when a process completes.
                Arguments are (tracked_process, exit_code, output, truncated, duration_ms).
        """
        self._processes: dict[int, TrackedProcess] = {}
        self._monitor_tasks: dict[int, asyncio.Task[None]] = {}
        self._on_complete = on_complete

    def track(
        self,
        process: asyncio.subprocess.Process,
        output_file: str,
        command: str,
        correlation_id: str,
    ) -> None:
        """Start tracking a background process.

        Args:
            process: The subprocess to track.
            output_file: Path to the file where stdout/stderr are being written.
            command: The original command that was executed.
            correlation_id: The request ID that spawned this process.
        """
        if process.pid is None:
            logger.warning("Cannot track process with no PID")
            return

        tracked = TrackedProcess(
            pid=process.pid,
            output_file=output_file,
            command=command,
            correlation_id=correlation_id,
        )
        self._processes[process.pid] = tracked
        self._monitor_tasks[process.pid] = asyncio.create_task(
            self._monitor_process(process, tracked)
        )
        logger.info(
            "Tracking background process pid=%d command=%s correlation_id=%s",
            process.pid,
            command[:100],
            correlation_id,
        )

    async def _monitor_process(
        self,
        process: asyncio.subprocess.Process,
        tracked: TrackedProcess,
    ) -> None:
        """Wait for process to complete and trigger callback."""
        try:
            exit_code = await process.wait()

            output = ""
            truncated = False
            if os.path.exists(tracked.output_file):
                try:
                    with open(tracked.output_file, errors="replace") as f:
                        output = f.read(MAX_OUTPUT_SIZE + 1)
                        if len(output) > MAX_OUTPUT_SIZE:
                            output = output[:MAX_OUTPUT_SIZE]
                            truncated = True
                except Exception as e:
                    logger.warning(
                        "Failed to read background process output pid=%d output_file=%s error=%s",
                        tracked.pid,
                        tracked.output_file,
                        e,
                    )
                    output = f"[Error reading output: {e}]"

            duration_ms = int((time.time() - tracked.start_time) * 1000)

            logger.info(
                "Background process completed pid=%d exit_code=%d output_size=%d truncated=%s duration_ms=%d",
                tracked.pid,
                exit_code,
                len(output),
                truncated,
                duration_ms,
            )

            await self._on_complete(tracked, exit_code, output, truncated, duration_ms)

        except asyncio.CancelledError:
            logger.info("Background process monitoring cancelled pid=%d", tracked.pid)
            raise
        except Exception:
            logger.exception(
                "Error monitoring background process pid=%d",
                tracked.pid,
            )
        finally:
            self._processes.pop(tracked.pid, None)
            self._monitor_tasks.pop(tracked.pid, None)

    @property
    def active_count(self) -> int:
        """Return the number of actively tracked processes."""
        return len(self._processes)

    async def stop_all(self) -> None:
        """Cancel all monitoring tasks.

        This does NOT kill the background processes - they will continue running.
        It just stops the CLI from monitoring them.
        """
        if not self._monitor_tasks:
            return

        logger.info(
            "Stopping background process tracking count=%d",
            len(self._monitor_tasks),
        )

        for task in self._monitor_tasks.values():
            task.cancel()

        await asyncio.gather(*self._monitor_tasks.values(), return_exceptions=True)
        self._monitor_tasks.clear()
        self._processes.clear()
