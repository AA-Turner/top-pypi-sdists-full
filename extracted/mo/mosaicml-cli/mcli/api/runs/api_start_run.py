""" Start a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList

__all__ = ['start_runs']

QUERY_FUNCTION = 'startRuns'
VARIABLE_DATA_NAME = 'getRunsData'
QUERY = f"""
mutation StartRuns(${VARIABLE_DATA_NAME}: GetRunsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
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
    runType
    isDeleted
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
def start_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> Run:
    ...


@overload
def start_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[Run]:
    ...


def start_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Start a run

    Start a run currently stopped in the MosaicML platform.

    Args:
        run (``Optional[str | ``:class:`~mcli.api.model.run.Run` ``]``): A run or run name to start
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`start_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if starting the requested runs failed
            A successfully started run will have the status ```RunStatus.PENDING```

    Returns:
        If future is False:
            Started :class:`~mcli.api.model.run.Run` object
        Otherwise:
            A :class:`~concurrent.futures.Future` for the object
    """
    runs = cast(Union[List[str], List[Run]], [run])

    if future:
        res = start_runs(runs=runs, timeout=None, future=True)
        return convert_plural_future_to_singleton(res)

    return start_runs(runs=runs, timeout=timeout, future=False)[0]


@overload
def start_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[Run]:
    ...


@overload
def start_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[Run]]:
    ...


def start_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Start a list of runs

    Start a list of runs currently stopped in the MosaicML platform.

    Args:
        runs (``Optional[List[str] | List[``:class:`~mcli.api.model.run.Run` ``]]``):
            A list of runs or run names to start
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`start_runs` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        MAPIException: Raised if starting any of the requested runs failed. All
            successfully started runs will have the status ```RunStatus.PENDING```. You can
            freely retry any started and started runs if this error is raised due to a
            connection issue.

    Returns:
        If future is False:
            A list of started :class:`~mcli.api.model.run.Run` objects
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list
    """
    # Extract run names
    run_names = [r.name if isinstance(r, Run) else r for r in runs]

    filters = {}
    if run_names:
        filters['name'] = {'in': run_names}

    variables = {VARIABLE_DATA_NAME: {'filters': filters}}

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME])

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
