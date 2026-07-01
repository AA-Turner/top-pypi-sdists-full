""" Delete a run. """
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, cast, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList

__all__ = ['delete_runs', 'delete_run']

QUERY_FUNCTION = 'deleteRuns'
VARIABLE_DATA_NAME = 'getRunsData'
QUERY = f"""
mutation DeleteRuns(${VARIABLE_DATA_NAME}: GetRunsInput!) {{
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
        estimatedEndTime
    }}
  }}
}}"""


@overload
def delete_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> Run:
    ...


@overload
def delete_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[Run]:
    ...


def delete_run(
    run: Union[str, Run],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Delete a run in the MosaicML platform

    If a run is currently running, it will first be stopped.

    Args:
        run: A run to delete
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `delete_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A :type Run: for the run that was deleted
    """
    runs = cast(Union[List[str], List[Run]], [run])

    if future:
        res = delete_runs(runs=runs, timeout=None, future=True)
        return convert_plural_future_to_singleton(res)

    return delete_runs(runs=runs, timeout=timeout, future=False)[0]


@overload
def delete_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[Run]:
    ...


@overload
def delete_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[Run]]:
    ...


def delete_runs(
    runs: Union[List[str], List[Run], ObjectList[Run]],
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Delete a list of runs in the MosaicML platform

    Any runs that are currently running will first be stopped.

    Args:
        runs: A list of runs or run names to delete
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `delete_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A list of :type Run: for the runs that were deleted
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
