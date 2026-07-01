""" Stop a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import Any, Dict, List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList

__all__ = ['stop_runs', 'stop_run']

QUERY_FUNCTION = 'stopRuns'
VARIABLE_DATA_NAME = 'getRunsData'
OPTIONAL_DATA_NAME = 'stopRunsData'
QUERY = f"""
mutation StopRuns(${VARIABLE_DATA_NAME}: GetRunsInput!, ${OPTIONAL_DATA_NAME}: StopRunsInput) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}, {OPTIONAL_DATA_NAME}: ${OPTIONAL_DATA_NAME}) {{
    id
    name
    createdByEmail
    status
    createdAt
    updatedAt
    reason
    priority
    maxRetries
    preemptible
    retryOnSystemFailure
    isDeleted
    runType
    resumptions {{
        clusterName
        cpus
        gpuType
        gpus
        nodes
        executionIndex
        startTime
        endTime
        status
    }}
  }}
}}"""


@overload
def stop_run(
    run: Union[str, Run],
    *,
    reason: Optional[str] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> Run:
    ...


@overload
def stop_run(
    run: Union[str, Run],
    *,
    reason: Optional[str] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[Run]:
    ...


def stop_run(
    run: Union[str, Run],
    *,
    reason: Optional[str] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Stop a run

    Stop a run currently running in the MosaicML platform.

    Args:
        run (``Optional[str | ``:class:`~mcli.api.model.run.Run` ``]``):
            A run or run name to stop. Using :class:`~mcli.api.model.run.Run` objects is most
            efficient. See the note below.
        reason (``Optional[str]``): A reason for stopping the run
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`stop_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if stopping the requested runs failed
            A successfully stopped run will have the status ```RunStatus.STOPPED```

    Returns:
        If future is False:
            Stopped :class:`~mcli.api.model.run.Run` object
        Otherwise:
            A :class:`~concurrent.futures.Future` for the object
    """
    runs = cast(Union[List[str], List[Run]], [run])

    if future:
        res = stop_runs(runs=runs, reason=reason, timeout=None, future=True)
        return convert_plural_future_to_singleton(res)

    return stop_runs(runs=runs, reason=reason, timeout=timeout, future=False)[0]


@overload
def stop_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    reason: Optional[str] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[Run]:
    ...


@overload
def stop_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    reason: Optional[str] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[Run]]:
    ...


def stop_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    reason: Optional[str] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Stop a list of runs

    Stop a list of runs currently running in the MosaicML platform.

    Args:
        runs (``Optional[List[str] | List[``:class:`~mcli.api.model.run.Run` ``]]``):
            A list of runs or run names to stop. Using :class:`~mcli.api.model.run.Run`
            objects is most efficient. See the note below.
        reason (``Optional[str]``): A reason for stopping the run
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`stop_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if stopping any of the requested runs failed. All
            successfully stopped runs will have the status ```RunStatus.STOPPED```. You can
            freely retry any stopped and unstopped runs if this error is raised due to a
            connection issue.

    Returns:
        If future is False:
            A list of stopped :class:`~mcli.api.model.run.Run` objects
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list
    """
    # Extract run names
    run_names = [r.name if isinstance(r, Run) else r for r in runs]

    filters = {}
    if run_names:
        filters['name'] = {'in': run_names}

    variables: Dict[str, Dict[str, Any]] = {VARIABLE_DATA_NAME: {'filters': filters}}

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME])

    if reason:
        variables[OPTIONAL_DATA_NAME] = {'reason': reason}

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
