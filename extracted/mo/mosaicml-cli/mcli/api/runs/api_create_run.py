""" Create a Run """
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.run import Run
from mcli.models.run_config import FinalRunConfig, RunConfig

__all__ = ['create_run']

QUERY_FUNCTION = 'createRun'
VARIABLE_DATA_NAME = 'createRunData'
QUERY = f"""
mutation CreateRun(${VARIABLE_DATA_NAME}: CreateRunInput!) {{
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
    details {{
        originalRunInput
        metadata
        lastExecutionId
    }}
  }}
}}"""


@overload
def create_run(run: Union[RunConfig, FinalRunConfig],
               *,
               timeout: Optional[float] = 10,
               future: Literal[False] = False) -> Run:
    ...


@overload
def create_run(run: Union[RunConfig, FinalRunConfig],
               *,
               timeout: Optional[float] = None,
               future: Literal[True] = True) -> Future[Run]:
    ...


def create_run(run: Union[RunConfig, FinalRunConfig],
               *,
               timeout: Optional[float] = 10,
               future: bool = False) -> Union[Run, Future[Run]]:
    """Launch a run in the MosaicML platform

    The provided :class:`run <mcli.models.run_config.RunConfig>` must contain
    enough information to fully detail the run

    Args:
        run: A fully-configured run to launch. The run will be queued and persisted
            in the run database.
        timeout: Time, in seconds, in which the call should complete. If the run creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `create_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type Run: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A Run that includes the launched run details and the run status
    """

    if isinstance(run, RunConfig):
        run = FinalRunConfig.finalize_config(run)

    variables = {
        VARIABLE_DATA_NAME: run.to_create_run_api_input(),
    }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
