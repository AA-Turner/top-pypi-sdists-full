"""DataIntegration Task Runner.

This Module can run data-integration tasks, HTTP/RESTful calls
(or even any arbitrary python function),
received parametriced tasks and return the results.

Task Runner receives different command-line arguments:

--variables: override variables passed between components/processes.
--attributes: override root-level attributes of components.
--conditions: override values in components with conditions.
--params: any value in params ins passed as kwargs
--args: list of arguments to be used by some functions (like replacement of values)

* For Calling a task:
 --program=program_name --task=task_name --params
* For calling Python Functions:
 --function=path.to.python.import --params
* System Command:
 --command=path.to.command --params
* or even Calling a URL:
 --url=URI --params
"""
from typing import Any
import uuid
import random
import asyncio
import signal
from navconfig.logging import logging

# Worker: lazy-loaded to avoid importing aiogram/telegram (~18s) at startup.
# from qw.wrappers import TaskWrapper  # deferred to dispatch_to_worker()
# from qw.client import QClient  # deferred to __init__

# FlowTask
from .utils.stats import TaskMonitor
from .parsers.argparser import ConfigParser
from .exceptions import (
    TaskError,
    NotSupported,
)


def my_handler():
    # TODO: Copying Signal-handler from Notify Worker.
    print("Stopping")
    for task in asyncio.all_tasks():
        task.cancel()


def resolve_runner_route(
    cli_executor: str | None,
    no_worker: bool,
    wait_for_result: bool,
    default_executor: str | None,
) -> tuple[str, str]:
    """Decide the executor name and execution mode for a console task.

    The Runner mirrors the scheduler's priority-driven router
    (``flowtask/scheduler/functions.py``): here the *CLI flags* — not a
    priority string — pick whether a task runs in-process or is handed to the
    QWorker queue.  ``"local"`` is the router sentinel, NOT a force-in-process
    selector.

    Resolution (highest precedence first):

    * ``cli_executor`` (``--executor=<name>``) → that executor, as-is
      (``qworker``, ``docker``, ``k8s``, ``publish``, ``local``…).
    * ``no_worker`` (``--no-worker``) → ``"local"`` (run in-process).
    * otherwise → the QWorker, unless ``default_executor`` names a non-local
      global backend (e.g. ``docker``/``k8s``), which is honoured instead.

    Mode for the QWorker:

    * default → ``"dispatch"`` (fire-and-forget, ``QClient.queue()``).
    * ``wait_for_result`` (``--run``) → ``"run"`` (``QClient.run()``, waits).

    Every non-QWorker executor (local/docker/k8s/…) always runs and waits, so
    its mode is ``"run"``.

    Args:
        cli_executor: Value of the ``--executor`` flag, or ``None``.
        no_worker: Whether ``--no-worker`` was passed.
        wait_for_result: Whether ``--run`` was passed.
        default_executor: The global ``DEFAULT_EXECUTOR`` conf value.

    Returns:
        A ``(executor_name, mode)`` tuple where ``mode`` is ``"run"`` or
        ``"dispatch"``.
    """
    if cli_executor:
        executor_name = cli_executor
    elif no_worker:
        executor_name = "local"
    else:
        global_default = default_executor or "local"
        executor_name = "qworker" if global_default == "local" else global_default

    if executor_name == "qworker":
        mode = "run" if wait_for_result else "dispatch"
    else:
        mode = "run"

    return executor_name, mode

class TaskRunner:
    """
    TaskRunner.

        Execution of DataIntegration Tasks.
    """

    logger: logging.Logger = None

    def __init__(self, loop: asyncio.AbstractEventLoop = None, worker=None, **kwargs):
        """Init Method for Task Runner."""
        self._task = None
        self._command: str = None
        self._fn: str = None
        self._url: str = None
        self._taskname = ""
        self.task_type: str = "task"
        self.stat: TaskMonitor = None
        # arguments passed by command line:
        self._conditions = {}
        self._attrs = {}
        self.ignore_steps = []
        self.run_only = []
        self._stepattrs = {}
        self._kwargs = {}
        self._variables = {}
        self._result: Any = None
        if loop:
            self._loop = loop
            self.inner_evt = False
        else:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self.inner_evt = True
        self._loop.add_signal_handler(signal.SIGINT, my_handler)
        # Task ID:
        self.task_id = uuid.uuid1(node=random.getrandbits(48) | 0x010000000000)
        # argument Parser
        if "new_args" in kwargs:
            new_args = kwargs["new_args"]
            del kwargs["new_args"]
        else:
            new_args = []
        parser = ConfigParser()
        parser.parse(new_args)
        self._argparser = parser
        self._options = parser.options
        # program definition
        self._program = self._options.program
        try:
            self._program = kwargs["program"]
            del kwargs["program"]
        except KeyError:
            pass
        if not self._program:
            self._program = "navigator"
        # DEBUG
        try:
            self._debug = kwargs["debug"]
            del kwargs["debug"]
        except KeyError:
            self._debug = self._options.debug
        # logger
        self.logger = logging.getLogger("FlowTask.Runner")
        if self._debug:
            self.logger.setLevel(logging.DEBUG)
        self.logger.notice(f"Program is: > {self._program}")
        # about Worker Information:
        self.worker = worker
        ## Task Storage:
        self._taskstorage = self._options.storage
        try:
            self.no_worker = self._options.no_worker
        except (ValueError, TypeError):
            self.no_worker = False
        try:
            self.no_events = self._options.no_events
        except (ValueError, TypeError):
            self.no_events = False
        try:
            self.no_notify = self._options.no_notify
        except (ValueError, TypeError):
            self.no_notify = False
        if kwargs:
            # remain args go to kwargs:
            self._kwargs = {**kwargs}

    @property
    def stats(self) -> TaskMonitor:
        """stats.
        Return a TaskMonitor object with all collected stats.
        Returns:
            TaskMonitor: stat object.
        """
        return self.stat

    def options(self) -> dict:
        return self._options

    async def __aenter__(self) -> "TaskRunner":
        """Magic Context Methods"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Magic Context Methods"""
        # clean up anything you need to clean up
        await self.close()

    @property
    def result(self):
        return self._result

    async def start(self):
        # define the type of task:
        if self._options.command:
            self._command = self._options.command
            self.task_type = "command"
            self._taskname = f"{self._command!s}"
        elif self._options.function:
            self._fn = self._options.function
            self.task_type = "function"
            self._taskname = f"{self._fn!s}"
        elif self._options.task:
            self._taskname = self._options.task
            self.task_type = "task"
        else:
            raise NotSupported("Task Runner: Unknown or missing Task type.")
        # initialize the Task Monitor
        try:
            self.stat = TaskMonitor(
                name=self._taskname, program=self._program, task_id=self.task_id
            )
            await self.stat.start()
        except Exception as err:
            raise TaskError(f"Task Runner: Error on TaskMonitor: {err}") from err
        # NOTE: do NOT instantiate or start a Task/Command here.  Since the
        # executor-framework refactor (TASK-073), run() resolves an executor
        # and that executor owns the entire task lifecycle (it builds its own
        # Task and calls start()+run()).  Creating + start()ing a Task here as
        # well caused the task to be parsed/started twice — duplicate
        # "Starting Task" events, a duplicate local execution alongside the
        # intended executor, and a leaked TaskMonitor sampler.  start() is now
        # only responsible for resolving the task type and the monitor; run()
        # performs the execution.
        logging.debug(
            f"::: FlowTask: Prepared {self.task_type}: {self._taskname} with id: {self.task_id}"
        )
        return True

    async def run(self):
        from flowtask.executors.resolver import resolve_executor
        from flowtask.conf import DEFAULT_EXECUTOR
        try:
            # ── Flag-driven executor router ──────────────────────────────────
            # The Runner mirrors the scheduler's priority-driven router
            # (flowtask/scheduler/functions.py): here the *CLI flags* — not a
            # priority string — decide whether a console task runs in-process
            # or is handed to the QWorker queue.  "local" is the router
            # sentinel, NOT a force-in-process flag.
            #
            #   --no-worker            → local    (run in-process, wait)
            #   --executor=<name>      → <name>   (explicit override: qworker,
            #                                       docker, k8s, publish, local…)
            #   (no flag)              → qworker  (default dispatch)
            #
            # DEFAULT_EXECUTOR only switches the *global* backend (e.g. a
            # deployment that runs everything on docker/k8s).  When it is the
            # plain "local" sentinel, normal CLI dispatch routes to the worker;
            # an explicit non-local DEFAULT_EXECUTOR is honoured as the default
            # backend.
            executor_name, mode = resolve_runner_route(
                cli_executor=getattr(self._options, "executor", None),
                no_worker=self.no_worker,
                wait_for_result=getattr(self._options, "run", False),
                default_executor=DEFAULT_EXECUTOR,
            )

            # Resolve via the executor name we just decided.  Setting it on the
            # options object (instead of relying on the legacy --no-worker /
            # --queued handling inside resolve_executor) makes the choice
            # explicit and suppresses the deprecation warnings, exactly like
            # the scheduler does.
            self._options.executor = executor_name
            task_def = {"executor": executor_name}
            executor = resolve_executor(task_def, self._options)
            # The executor builds a fresh Task WITHOUT the CLI parser, so options
            # that the Task only reads from the parser (run_only, ignore,
            # override_attributes, variables, conditions) would be silently lost
            # — breaking flags like --run_only.  Forward them as serialisable
            # kwargs (NOT the parser object, which remote executors can't
            # serialise) so the Task picks them up via its kwargs fallbacks.
            for _opt_attr, _kw_name in (
                ("run_only", "run_only"),
                ("ignore", "ignore_steps"),
                ("override_attributes", "override_attributes"),
                ("variables", "variables"),
                ("conditions", "conditions"),
                ("masks", "masks"),
                ("args", "args"),
                ("arguments", "arguments"),
                # The executor builds a fresh Task that re-resolves its storage
                # from kwargs; without forwarding the selected task/file storage
                # the new Task silently falls back to "default" (TASK_PATH),
                # breaking --storage=<name> (e.g. private).
                ("storage", "storage"),
                ("filestore", "filestore"),
            ):
                _val = getattr(self._options, _opt_attr, None)
                if _val:
                    self._kwargs.setdefault(_kw_name, _val)
            if mode == "dispatch":
                handle = await executor.dispatch(
                    self._program,
                    self._taskname,
                    str(self.task_id),
                    debug=self._debug,
                    no_events=self.no_events,
                    **self._kwargs,
                )
                self._result = {"handle": handle.execution_id}
            else:
                task_result = await executor.run(
                    self._program,
                    self._taskname,
                    str(self.task_id),
                    debug=self._debug,
                    no_events=self.no_events,
                    **self._kwargs,
                )
                # Propagate the executor task's full TaskMonitor (with per-step
                # stats) so ``runner.stats`` reflects the real execution instead
                # of the runner's placeholder monitor.  Do this BEFORE raising on
                # failure so a FAILED task still surfaces the steps that ran
                # before the error (not just on success).  Local (in-process)
                # runs return the live TaskMonitor; remote executors return a
                # serialised dict, which we leave on self.stat untouched.
                if isinstance(task_result.stats, TaskMonitor):
                    try:
                        await self.stat.stop()  # stop placeholder's sampler
                    except Exception:  # pylint: disable=W0718
                        pass
                    self.stat = task_result.stats
                if task_result.status == "failed":
                    from flowtask.exceptions import TaskFailed
                    raise TaskFailed(task_result.error or "Task execution failed")
                self._result = task_result.result
        except Exception as err:
            logging.error(err)
            raise
        return True

    async def close(self):
        if self._debug:
            logging.debug(f"ENDING TASK {self._taskname}")
        try:
            await self.stat.stop()
        except Exception as err:  # pylint: disable=W0718
            logging.exception(err)
        finally:
            if self.inner_evt is True:
                self._loop.close()
