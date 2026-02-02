import abc
import time
from typing import Any

import numpy as np
import rich.progress
from rich.text import Text

from bec_lib.logger import bec_logger

logger = bec_logger.logger


class MoveTaskProgressColumn(rich.progress.TaskProgressColumn):
    """Custom progress column for the move device progress bar"""

    def render(self, task) -> Text:
        """Renders the text for the progress bar"""
        if task.total is None and self.show_speed:
            return self.render_speed(task.finished_speed or task.speed)
        if task.fields.get("fields"):
            _text = f"[progress.percentage]{task.fields['fields'].get('current_pos'):10.2f} / {task.fields['fields'].get('target_pos'):10.2f} / {task.percentage:>3.0f} %"
        else:
            _text = f"[progress.percentage]{task.percentage:>3.0f}%"
        if self.markup:
            text = Text.from_markup(_text, style=self.style, justify=self.justify)
        else:
            text = Text(_text, style=self.style, justify=self.justify)
        if self.highlighter:
            self.highlighter.highlight(text)
        return text


class ScanTaskProgressColumn(rich.progress.TaskProgressColumn):
    """Custom progress column for the scan progress bar"""

    def render(self, task) -> Text:
        """Renders the text for the progress bar"""
        if task.total is None and self.show_speed:
            return self.render_speed(task.finished_speed or task.speed)
        if task.fields.get("fields"):
            _text = f"[progress.percentage]{int(task.fields['fields'].get('current_scan_pos'))} / {task.percentage:>3.0f} %"
        else:
            _text = f"[progress.percentage]{task.percentage:>3.0f}%"
        if self.markup:
            text = Text.from_markup(_text, style=self.style, justify=self.justify)
        else:
            text = Text(_text, style=self.style, justify=self.justify)
        if self.highlighter:
            self.highlighter.highlight(text)
        return text


class ProgressBarBase(abc.ABC):
    NUM_STEPS = 1000
    UPDATE_FREQUENCY = 10

    def __init__(self, clear_on_exit: bool = False) -> None:
        """Base class for progress bars. Override _init_tasks and _update_task for a new progress bar implementation.
        Override columns for a customized bar style.

        Args:
            clear_on_exit (bool, optional): remove progress bar after completion. Defaults to False.

        """
        self.clear_on_exit = clear_on_exit
        self._progress = None
        self._tasks = []

    @property
    def columns(self) -> tuple[rich.progress.ProgressColumn, ...]:
        """Columns used for a new Progress instance:
           - a text column for the description (TextColumn)
           - the bar itself (BarColumn)
           - a text column showing completion percentage (TextColumn)
           - an estimated-time-remaining column (TimeRemainingColumn)

        Override in subclasses to customize the progress bar appearance.

        Returns:
            tuple[rich.progress.ProgressColumn, ...]: columns
        """
        return rich.progress.Progress.get_default_columns()

    def start(self) -> None:
        """Start the Progress handler and initialize the tasks."""
        self._progress = rich.progress.Progress(
            *self.columns, transient=self.clear_on_exit, auto_refresh=False
        )
        self._progress.start()
        self._init_tasks()
        self._progress.refresh()

    def sleep(self):
        """Sleep for a short time to avoid busy waiting."""
        time.sleep(1 / self.UPDATE_FREQUENCY)

    def stop(self) -> None:
        """Stop the Progress handler"""
        self._progress.stop()

    @abc.abstractmethod
    def _init_tasks(self) -> None:
        """Initialize tasks by appending new items to self._progress."""

    @property
    def finished(self) -> bool:
        """True if all tasks have been completed.

        Returns:
            bool: True if all tasks have been completed.
        """
        return self._progress.finished

    @abc.abstractmethod
    def _update_task(self, task: int, value: Any) -> None:
        """Update routine that is applied to each tasks during self.update calls.

        Args:
            task (int): task ID
            value (Any): updated value received from self.update

        """

    def update(self, values: list):
        """Update the progress bar with new values.

        Args:
            values (list): list of values to update the progress bar with.
        """
        if not isinstance(values, list):
            values = [values]
        for i, task in enumerate(self._tasks):
            self._update_task(task=task, value=values[i])

    def __enter__(self):
        """Start the progress bar when entering a context."""
        self.start()
        return self

    def __exit__(self, *args):
        """Stop the progress bar when exiting a context."""
        self.stop()


class ScanProgressBar(ProgressBarBase):
    def __init__(self, scan_number: int, clear_on_exit=False) -> None:
        """Progress bar for a scan.

        Args:
            scan_number (int): scan number
            clear_on_exit (bool, optional): remove progress bar after completion. Defaults to False.
        """
        super().__init__(clear_on_exit)
        self._max_points = None
        self.scan_number = scan_number

    @property
    def columns(self) -> tuple:
        """Columns used for a new Progress instance.

        Returns:
            tuple: columns
        """
        return (
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.BarColumn(),
            ScanTaskProgressColumn(),
            rich.progress.TimeRemainingColumn(),
            rich.progress.TimeElapsedColumn(),
        )

    def _init_tasks(self):
        """Initialize tasks by appending new items to self._progress."""
        self._tasks.append(
            self._progress.add_task(f"[green] Scan {self.scan_number}: ", total=self.max_points)
        )

    def _update_tasks_total(self, max_points: int) -> None:
        """Update the total number of steps for the progress bar.

        Args:
            max_points (int): total number of steps
        """
        self._progress.tasks[0].total = max_points

    @property
    def max_points(self) -> int:
        """Total number of steps for the progress bar.

        Returns: int: total number of steps
        """
        return self._max_points

    @max_points.setter
    def max_points(self, max_points: int) -> None:
        """Setter for the total number of steps for the progress bar.

        Args:
            max_points (int): total number of steps
        """
        self._max_points = max_points
        self._update_tasks_total(max_points)

    def _update_task(self, task: int, value):
        """Update routine that is applied to each tasks during self.update calls.

        Args:
            task (int): task ID
            value (Any): updated value received from self.update
        """
        if self.max_points:
            self._progress.update(
                self._tasks[task], completed=value, fields={"current_scan_pos": value}, refresh=True
            )
            self._progress.refresh()
        else:
            self._progress.update(
                self._tasks[task], fields={"current_scan_pos": value}, refresh=True
            )
            self._progress.refresh()


class DeviceProgressBar(ProgressBarBase):
    def __init__(
        self,
        devices: list[str],
        target_values: list[float],
        start_values: list[float] = None,
        clear_on_exit: bool = False,
    ) -> None:
        """Progress bar for moving devices.

        Args:
            devices (list[str]): list of device names
            target_values (list[float]): list of target values
            start_values (list[float], optional): list of start values. Defaults to None.
            clear_on_exit (bool, optional): remove progress bar after completion. Defaults to False.
        """
        self.target_values = target_values
        self.start_values = start_values
        self.devices = devices

        super().__init__(clear_on_exit)

        self._tasks = []

    @property
    def columns(self):
        """Columns used for a new Progress instance."""
        return (
            rich.progress.TextColumn("[progress.description]{task.description}"),
            rich.progress.BarColumn(),
            MoveTaskProgressColumn(),
            rich.progress.TimeRemainingColumn(),
            rich.progress.TimeElapsedColumn(),
        )

    def _init_tasks(self):
        """Initialize tasks by appending new items to self._progress."""
        for ii, dev in enumerate(self.devices):
            self._tasks.append(
                self._progress.add_task(
                    f"[green] {dev}:{self.start_values[ii]:10.2f}", total=self.NUM_STEPS
                )
            )

    def _update_task(self, task: Any, value: float) -> None:
        """Update routine that is applied to each tasks during self.update calls.

        Args:
            task (Any): task ID
            value (float): updated value received from self.update
        """
        if self._progress.tasks[task].finished:
            return

        movement_range = self.target_values[task] - self.start_values[task]
        if np.abs(movement_range) > 0:
            completed = np.abs((value - self.start_values[task]) / movement_range * self.NUM_STEPS)
        else:
            completed = self.NUM_STEPS
        self._progress.update(
            task,
            completed=completed,
            fields={"current_pos": value, "target_pos": self.target_values[task]},
            refresh=True,
        )
        self._progress.refresh()

    def set_finished(self, device):
        """Set a progressbar for a device as finished.

        Args:
            device (str): device name
        """
        device_index = self.devices.index(device)
        self._progress.advance(self._tasks[device_index], self.NUM_STEPS)


if __name__ == "__main__":
    pass
    # devices = ["samx", "samy"]
    # target_values = [25, 50]
    # start = [0, 5]
    # steps_sim = []
    # for ii, dev in enumerate(devices):
    #     steps_sim.append(np.linspace(start[ii], target_values[ii], 100 * (ii + 1)))
    # loop_index = 0

    # def get_device_values(index):
    #     values = [
    #         steps_sim[dev_index][min(index, len(steps_sim[dev_index]) - 1)]
    #         for dev_index, _ in enumerate(devices)
    #     ]
    #     return values

    # with DeviceProgressBar(
    #     devices=devices, start_values=start, target_values=target_values
    # ) as progress:
    #     while not progress.finished:
    #         values = get_device_values(loop_index)
    #         progress.update(values=values)
    #         time.sleep(0.001)
    #         # for ii, dev in enumerate(devices):
    #         #     if np.isclose(values[ii], target_values[ii], atol=0.05):
    #         #         progress.set_finished(dev)
    #         loop_index += 1
