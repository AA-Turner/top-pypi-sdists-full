"""Adds run status watching for the MCloud API"""
from __future__ import annotations

import functools
import logging
from concurrent.futures import Future
from typing import Any, Dict, Generator, Optional, Union, overload

import gql
from typing_extensions import Literal

from mcli.api.engine.engine import MAPIConnection, get_return_response, run_in_threadpool
from mcli.api.model.run import Run
from mcli.api.runs.api_get_runs import get_run
from mcli.utils.utils_run_status import RunStatus
from mcli.utils.utils_spinner import progress

logger = logging.getLogger(__name__)

QUERY_FUNCTION = 'watchRunStatus'
VARIABLE_DATA_NAME = 'watchRunStatusInput'
QUERY = f"""
subscription Subscription(${VARIABLE_DATA_NAME}: WatchRunStatusInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME})
}}
"""


class RunStatusNotReached(Exception):

    def __init__(self, name: str, actual: RunStatus, expected: RunStatus):
        self.name = name
        self.actual = actual
        self.expected = expected
        super().__init__()

    def __str__(self):
        return f"""Run {self.name} never reached expected status:
Requested: {self.expected}
Reached: {self.actual}
"""


@overload
def wait_for_run_status(run: Union[str, Run],
                        status: Union[str, RunStatus],
                        timeout: Optional[float] = None,
                        future: Literal[False] = False) -> Run:
    ...


@overload
def wait_for_run_status(run: Union[str, Run],
                        status: Union[str, RunStatus],
                        timeout: Optional[float] = None,
                        future: Literal[True] = True) -> Future[Run]:
    ...


def wait_for_run_status(run: Union[Run, str],
                        status: Union[RunStatus, str],
                        timeout: Optional[float] = None,
                        future: bool = False) -> Union[Run, Future[Run]]:
    """Wait for a launched run to reach a specific status

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run whose status
            should be watched. This can be provided using the run's name or an existing
            :class:`~mcli.api.model.run.Run` object.
        status (:obj:`str` | :class:`~mcli.utils.utils_run_status.RunStatus`): Status to wait for.
            This can be any valid :class:`~mcli.utils.utils_run_status.RunStatus`
            value. If the status is short-lived, or the run terminates, it is possible the run
            will reach a LATER status than the one requested. If the run never reaches this state
            (e.g. it stops early or the wait times out), then an error will be raised.
            See exception details below.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`wait_for_run_status` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if the run does not exist or there is an issue connecting to the
            MAPI service.
        RunStatusNotReached: Raised in the event that the watch closes before the run reaches
            the desired status. If this happens, the connection to MAPI may have dropped, so
            try again.
        TimeoutError: Raised if the run did not reach the correct status in the specified time

    Returns:
         If future is False:
            A :class:`~mcli.api.model.run.Run` object once it has reached the requested status
        Otherwise:
            A :class:`~concurrent.futures.Future` for the run. This will not resolve until
            the run reaches the requested status
    """

    if not isinstance(status, RunStatus):
        status = RunStatus.from_string(status)

    response = run_in_threadpool(_threaded_wait_for_run_status, run=run, status=status)
    return get_return_response(response, future=future, timeout=timeout)


def _threaded_wait_for_run_status(run: Union[Run, str], status: RunStatus):
    # Convert to Run
    if not isinstance(run, Run):
        run = get_run(run, include_details=False)

    updated_run: Optional[Run] = None
    for updated_run in watch_run_status(run):
        if updated_run.status.after(status, inclusive=True):
            return updated_run

    if not updated_run:
        updated_run = run

    raise RunStatusNotReached(updated_run.name, updated_run.status, status)


@overload
def watch_run_status(
    run: Union[Run, str],
    timeout: Optional[float] = None,
    future: Literal[False] = False,
) -> Generator[Run, None, None]:
    ...


@overload
def watch_run_status(
    run: Union[Run, str],
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Generator[Future[Run], None, None]:
    ...


def watch_run_status(
    run: Union[Run, str],
    timeout: Optional[float] = None,
    future: bool = False,
) -> Union[Generator[Run, None, None], Generator[Future[Run], None, None]]:
    """Watch a launched run and retrieve a new Run object everytime its status updates

    Args:
        run (:obj:`str` | :class:`~mcli.api.model.run.Run`): The run whose status
            should be watched. This can be provided using the run's name or an existing
            :class:`~mcli.api.model.run.Run` object.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored. A run may
            take some time to change statuses (especially to go from RUNNING to COMPLETED), so
            you likely do not want to set a timeout.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`.
            If ``True``, each iteration will yield a :class:`~concurrent.futures.Future` for
            the next updated :class:`~mcli.api.model.run.Run` object. This takes precedence
            over the ``timeout`` argument. To get the :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument. With futures,
            you can easily watch multiple Runs in parallel. NOTE: If you set ``future==True``,
            you should wrap your ``return_value.result()`` in a ``try: ... except StopAsyncIteration``
            to catch the end of the iteration.

    Raises:
        MAPIException: Raised if the run could not be found or if there is an issue contacting the MAPI service
        TimeoutError: Raised if the run did not reach the correct status in the specified time

    Yields:
        If future is False:
            A :class:`~mcli.api.model.run.Run` object at each status update
        Otherwise:
            A :class:`~concurrent.futures.Future` for the run. This will not resolve until
            the run reaches a new status
    """

    # Convert to Run
    if not isinstance(run, Run):
        run = get_run(run, include_details=False)

    variables: Dict[str, Any] = {'name': run.name}

    variables = {VARIABLE_DATA_NAME: variables}
    query = gql.gql(QUERY)

    connection = MAPIConnection.get_current_connection()
    for run_future in connection.subscribe(query=query,
                                           variables=variables,
                                           callback=functools.partial(_convert_run_status, run=run),
                                           retry_callback=lambda x: x):
        if not future:
            try:
                yield run_future.result(timeout)
            except StopAsyncIteration:
                break
        else:
            yield run_future


def _convert_run_status(incoming: Dict[str, Any], run: Run) -> Run:
    logger.debug(f"Got message from subscription: {incoming}")
    run_status = RunStatus.from_string(incoming['watchRunStatus'])
    run.status = run_status

    return run


class EpilogSpinner:
    """A run spinner that follows a run's status

    This can be used as a context manager where the spinner(s) will be started and
    stopped automatically. Otherwise they can be manually started and stopped using
    ``epilog.progress.start()`` and ``spinner.progress.stop()``.

    Attributes:
        progress: The ``rich.progress`` progress bar that contains the spinners

    Example:

    with EpilogSpinner(run, RunStatus.RUNNING) as spinner:
        run = epilog.follow()
    """

    def __init__(self, run: Run, status: RunStatus):
        self.run = run
        self.status = status
        self.progress = progress()
        self._task = self.progress.add_task(description=f'One moment. Checking on run {run.name}...')

    def __enter__(self) -> EpilogSpinner:
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        self.progress.stop()
        return False

    @staticmethod
    def _get_description(state: RunStatus) -> str:
        if state == RunStatus.PENDING:
            return 'Waiting in run queue...'
        if state == RunStatus.QUEUED:
            return 'Waiting for resources to become available...'
        elif state == RunStatus.STARTING:
            return 'Pulling Docker image...'
        else:
            return state.value.title().replace('_', ' ') + '...'

    def follow(self) -> Run:
        run = self.run
        for run in watch_run_status(self.run):
            self.progress.update(self._task,
                                 description=f'Run [cyan]{run.name}[/]: {self._get_description(run.status)}')
            if run.status.after(self.status, inclusive=True):
                break

        return run
