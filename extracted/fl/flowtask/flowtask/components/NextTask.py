"""FEAT-555 — the reserved NextTask continuation step."""
from typing import Any

from ..exceptions import ComponentError  # verified: flowtask/exceptions.py:104
from ..interfaces.flow import FlowComponent  # verified: flowtask/interfaces/flow.py:38


class NextTask(FlowComponent):
    """
    NextTask

        Overview

            Declares a *continuation*: another task that runs as a fresh,
            top-level task once this task finishes, receiving this task's final
            result, its end-of-run variables and the chain metadata.

            A NextTask step never executes as an ordinary component. It is
            removed from the DAG at build time and reserved; the continuation
            fires from Task.close(), so it runs whichever launcher ran the
            origin — runner, local executor, scheduler or a remote qw worker.

            Unlike SubTask, the hop does NOT run inside this task: it gets its
            own task_id, its own events and its own execution row, and this
            task's own result is what the launcher reports. Unlike the RunTask
            event, the hop receives the finished task's result and variables.

        :widths: auto

            | Name      | Required | Summary                                                                   |
            |-----------|----------|---------------------------------------------------------------------------|
            | task      |   Yes    | Name of the task to run as a continuation.                                |
            | program   |   No     | Program the target task belongs to. Default: the current program.         |
            | executor  |   No     | "inline" (default), a registered executor name, or a full executor dict.  |
            | priority  |   No     | Queue priority, forwarded to the qworker executor.                        |
            | on        |   No     | success (default) | nodata | warning | failure | always.                  |
            | variables |   No     | Extra variables merged last, over the origin's own variables.             |
            | result    |   No     | False suppresses the result hand-off. Default: True.                      |
            | storage   |   No     | Task storage name for the hop. Default: inherited from this task.         |
            | filestore |   No     | File storage name for the hop. Default: inherited from this task.         |

        Example:

        ```yaml
          - NextTask:
              task: load_orders
              program: warehouse
              on: success
              variables:
                channel: "#ops"
          - NextTask:
              task: notify_failure
              executor: qworker
              priority: high
              on: failure
              result: false
        ```

        Returns

            Nothing. This step produces no output and is never present in the
            executed pile; executing it is an error.
    """

    _version: str = "1.0.0"

    # YAML keys — FlowComponent.__init__ setattr()s leftovers (flow.py:155-160).
    task: str
    program: str | None = None
    executor: str | dict = "inline"
    priority: str | None = None
    on: str = "success"
    variables: dict = {}  # noqa: RUF012
    result: bool = True
    storage: str | None = None
    filestore: str | None = None

    _REFUSAL: str = (
        "NextTask must not be executed as a step; it is reserved by TaskPile "
        "and fired from Task.close(). Reaching this point means the task pile "
        "was built through a path that skips continuation reservation."
    )

    async def start(self, **kwargs: Any) -> bool:
        """Always fails: a reserved step must never be started.

        Raises:
            ComponentError: Unconditionally.
        """
        task_name = getattr(self, "TaskName", "Unknown")
        self.logger.error(f"[{task_name}] Refusing to start NextTask component: {self._REFUSAL}")
        raise ComponentError(self._REFUSAL)

    async def run(self) -> Any:
        """Always fails: a reserved step must never be run.

        Raises:
            ComponentError: Unconditionally.
        """
        raise ComponentError(self._REFUSAL)

    async def close(self) -> bool:
        """No-op: the stub holds no resources."""
        return True
