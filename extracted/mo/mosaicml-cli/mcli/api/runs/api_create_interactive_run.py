""" Create a Run """
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.run import Run
from mcli.models.run_config import FinalRunConfig, RunConfig

__all__ = ['create_interactive_run']

QUERY_FUNCTION = 'createInteractiveRun'
VARIABLE_DATA_NAME = 'createRunData'
QUERY = f"""
mutation CreateInteractiveRun(${VARIABLE_DATA_NAME}: CreateInteractiveRunInput!) {{
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
    details {{
        originalRunInput
        metadata
        lastExecutionId
    }}
  }}
}}"""


@overload
def create_interactive_run(run: Union[RunConfig, FinalRunConfig],
                           *,
                           timeout: Optional[float] = 10,
                           seconds: Optional[int] = None,
                           future: Literal[False] = False) -> Run:
    ...


@overload
def create_interactive_run(run: Union[RunConfig, FinalRunConfig],
                           *,
                           timeout: Optional[float] = None,
                           seconds: Optional[int] = None,
                           future: Literal[True] = True) -> Future[Run]:
    ...


def create_interactive_run(run: Union[RunConfig, FinalRunConfig],
                           *,
                           timeout: Optional[float] = 10,
                           seconds: Optional[int] = None,
                           future: bool = False) -> Union[Run, Future[Run]]:
    """Launch an interactive run in the MosaicML platform

    Users are not required to provide a name, image, or 'hours' variable for an interactive 
    run. If these variables are not provided, they will be filled in with defaults. If the 
    user provides a value for the 'command' variable, this will be overwritten with 
    `sleep <hours>`, where <hours> is the value of the 'hours' variable.

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
        hours: How many hours an interactive run can sleep for until MORC marks it as 
            completed.

    Returns:
        A Run that includes the launched run details and the run status
    """

    if isinstance(run, RunConfig):
        run = FinalRunConfig.finalize_config(run)

    variables = {
        VARIABLE_DATA_NAME: {
            **run.to_create_run_api_input(), "seconds": seconds
        },
    }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
