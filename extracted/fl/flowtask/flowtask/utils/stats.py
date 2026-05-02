"""TaskMonitor.

Collect and saves stats for execution of tasks.
"""
import os
import sys
from typing import Any, Union
import random
import contextlib
import asyncio
import logging
from datetime import datetime
import time
from statistics import mean
from contextlib import suppress
from psutil import virtual_memory, cpu_percent, Process


class StepMonitor:
    def __init__(self, name, parent=None) -> None:
        self.name = name
        self.executed_at: datetime = datetime.now()
        self.stats: dict = {}
        self.traceback: str = ""
        self._parent: Any = parent

    def add_metric(self, key, value) -> None:
        self.stats[key] = value

    def stacktrace(self, trace: str) -> None:
        self.traceback = trace

    def parent(self):
        return self._parent

    def __str__(self) -> str:
        trace = ""
        if self.traceback:
            trace = f"StackTrace: <{self.traceback!s}>\n"
        stat = (
            f"{self.name}:\n"
            f"Executed At: {self.executed_at}:\n"
            f"<{self.stats!r}>\n"
            f"{trace!s}\n"
        )
        return stat


class TaskMonitor:
    def __init__(
        self, name: str, program: str, task_id: str, userid: Union[int, str] = None
    ) -> None:
        self.task_name = name
        self.task_id = task_id
        self._started: bool = False
        self.traceback = None
        self.stats: dict = {}
        self.user: Union[int, str] = None
        self.steps: list[StepMonitor] = []
        self.executed_at: datetime = datetime.now()
        self.start_time: float = 0
        self.finish_time: float = 0
        self.duration: float = 0
        self._sampling_task: asyncio.Task
        self.program: str = program
        # CPU and RAM stats:
        self.baseline_cpu: float = 0
        self.baseline_ram: float = 0
        self._cpu_usage_data: list = []
        self._ram_usage_data: list = []
        self._memory_info: list = []
        # returned values of Stats
        self.max_cpu_used: float = 0
        self.avg_cpu_used: float = 0
        self.max_ram_used: float = 0
        self.avg_ram_used: float = 0
        self.memory_usage: float = 0
        # self.cpu_percent = partial(cpu_percent, interval=0)
        ## Memory usage:
        self._pid = os.getpid()
        self._process = Process(self._pid)
        self._memory_before = self._process.memory_info().rss
        ## TODO: passing User information:
        if sys.stdin and sys.stdin.isatty():
            self.exec_type = "console"
            try:
                self.user = os.environ.get("USER")
            except Exception:
                self.user = os.environ.get("USERNAME")
        else:
            # was dispatched from code
            try:
                if "qw" in sys.argv[0]:
                    self.exec_type = "worker"
                else:
                    self.exec_type = "task"
            except IndexError:
                self.exec_type = "code"
                self.user = os.getlogin()
        if not self.user:
            self.user = userid
        print(f"Execution Mode: {self.exec_type} by User: {self.user}")

    def __str__(self) -> str:
        steps = "\n".join([f"{step!s}" for step in self.steps])
        if steps:
            steps = f"Steps: \n{steps!s}\n"
        stat = (
            f"Task: {self.task_name}\n"
            f"ID: {self.task_id}\n"
            f"< {self.stats!r} >\n"
            f"{steps!s}"
        )
        return stat

    def to_json(self) -> dict:
        steps = {}
        for step in self.steps:
            steps[step.name] = {"executed_at": step.executed_at, **step.stats}
        stat = {
            "Task": self.task_name,
            "program": self.program,
            "task_name": f"{self.program}.{self.task_name}",
            "ID": self.task_id,
            **self.stats,
            "steps": {**steps},
        }
        return stat

    def add_step(self, step: StepMonitor) -> None:
        self.steps.append(step)

    def start_timing(self):
        self.start_time = time.time()

    def end_timing(self):
        self.finish_time = time.time()
        self.duration = self.finish_time - self.start_time

    def stacktrace(self, trace: str) -> None:
        self.traceback = trace

    def is_started(self) -> bool:
        return self._started

    def _get_virtual_memory(self):
        return virtual_memory().percent

    async def get_virtual_memory(self):
        return virtual_memory().percent

    async def get_memory_info(self):
        try:
            # Use a context manager to ensure file handles are closed
            with contextlib.suppress(OSError):
                proc = Process(self._pid)
                return proc.memory_info().rss / 1048576
        except OSError as e:
            logging.warning(f"Error getting Memory Info: {e}")
            return 0
        except Exception as e:
            logging.warning(f"Unexpected error getting Memory Info: {e}")
            return 0

    # Improve the cpu_percent method to ensure handles are closed
    async def cpu_percent(self, *args, **kwargs):
        try:
            # psutil's cpu_percent can leak file handles on Linux
            # Make a quick call with a safe wrapper
            return cpu_percent(*args, **kwargs)
        except OSError as e:
            if e.errno == 24:  # Too many open files
                logging.warning(f"Too many files open in cpu_percent: {e}")
            return 0.0

    async def _get_current_state(self, interval: float = 1.0):
        """_get_current_state.
            Get the Current state of System, will be collected async every tick.
            Implements backoff when errors occur.
        Args:
            interval (float, optional): initial interval of collecting information. Defaults to 0.3.
        """
        current_interval = interval
        max_interval = 5.0  # Maximum interval in seconds
        consecutive_errors = 0

        while True:
            try:
                if not self._started:  # Stop if _started is False.
                    break

                # Get resource usage metrics
                try:
                    memory = await self.get_memory_info()
                    cpu = await self.cpu_percent()
                    ram = await self.get_virtual_memory()

                    # If we got here without errors, add the data and reset backoff
                    self._cpu_usage_data.append(cpu)
                    self._ram_usage_data.append(ram)
                    self._memory_info.append(memory)

                    # Reset backoff if successful
                    if consecutive_errors > 0:
                        consecutive_errors = 0
                        current_interval = interval  # Reset to original interval
                        logging.info("Resource monitoring recovered, resetting interval to normal")

                except OSError as e:
                    # Handle "too many open files" error with backoff
                    if e.errno == 24:  # "Too many open files" error
                        consecutive_errors += 1

                        # Apply exponential backoff with jitter
                        backoff_factor = min(2 ** consecutive_errors, 10)  # Cap the backoff factor
                        jitter = 0.1 * backoff_factor * (random.random() * 0.5 + 0.75)  # Add 25%-75% jitter
                        current_interval = min(interval * backoff_factor * jitter, max_interval)

                        logging.warning(
                            f"Too many open files error, backing off. New interval: {current_interval:.2f}s "
                            f"(consecutive errors: {consecutive_errors})"
                        )
                    else:
                        # For other OSErrors, just log and continue
                        logging.warning(f"OS Error during monitoring: {e}")

                await asyncio.sleep(current_interval)

            except asyncio.CancelledError:
                break  # Exit cleanly on task cancellation
            except Exception as err:
                logging.exception(f"Can't collect CPU/RAM metrics due to error: {err}")
                # Still apply backoff for other errors
                consecutive_errors += 1
                current_interval = min(interval * (1.5 ** consecutive_errors), max_interval)
                await asyncio.sleep(current_interval)

    async def start(self, interval: float = 0.5):
        try:
            # check if not started:
            if not self._started:
                self._started = True
                self.start_timing()
                # Start task to call func periodically:
                self._sampling_task = asyncio.create_task(
                    self._get_current_state(interval)
                )
            # is started
        except Exception as err:
            logging.exception(
                f"Task Monitor Failed to Start, error: {err}"
            )

    def _calculate_stats(self):
        if self._cpu_usage_data:
            self.max_cpu_used = max(self._cpu_usage_data)
            self.avg_cpu_used = mean(self._cpu_usage_data)
            self.max_ram_used = max(self._ram_usage_data)
            self.avg_ram_used = mean(self._ram_usage_data)
            self.memory_usage = mean(self._memory_info)

    async def stop(self) -> dict:
        try:
            # Check is sampling is happening
            if self._started:
                # Stopping Monitor.
                self._started = False

                # Stop task and await it stopped:
                if hasattr(self, '_sampling_task') and self._sampling_task:
                    with contextlib.suppress(asyncio.CancelledError):
                        self._sampling_task.cancel()
                        await self._sampling_task

                # Stop the clock, making calculations
                self.end_timing()
                self._calculate_stats()

                # Calculate memory usage more safely
                memory_after = 0
                rss_in_bytes = 0
                try:
                    with contextlib.suppress(OSError):
                        proc = Process(self._pid)
                        memory_after = proc.memory_info().rss
                        rss_in_bytes = memory_after - self._memory_before
                except Exception as err:
                    logging.exception(f"Unable to get Memory Info: {err}")

                self.stats.update({
                    "executed_at": f"{self.executed_at:%Y-%m-%d %H:%M}",
                    "duration": f"{self.duration:.5f}",
                    "pid": self._pid,
                    "max_cpu": round(float(self.max_cpu_used) if self._cpu_usage_data else 0, 2),
                    "avg_cpu": round(float(self.avg_cpu_used) if self._cpu_usage_data else 0, 2),
                    "max_ram": round(float(self.max_ram_used) if self._ram_usage_data else 0, 2),
                    "avg_ram": round(float(self.avg_ram_used) if self._ram_usage_data else 0, 2),
                    "memory_usage": self.memory_usage,
                    "thread_memory": round(rss_in_bytes / (1024 * 1024), 4),
                    "exec_type": self.exec_type,
                    "user": self.user,
                })
                return self.stats
            else:
                return {}
        except Exception as err:
            logging.exception(f"Task Monitor Failed to Stop, due to: {err}")
            raise
