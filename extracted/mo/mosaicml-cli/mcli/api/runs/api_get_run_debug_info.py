"""Get debugging info for a run from the MosaicML platform, including the pod
and container status updates for the run across different executions.
"""
from __future__ import annotations

from concurrent.futures import Future
from typing import Any, Dict, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import convert_plural_future_to_singleton, get_return_response, run_plural_mapi_request
from mcli.api.model.run import Run
from mcli.api.model.run_debug_info import RunDebugInfo
from mcli.config import MCLIConfig

QUERY_FUNCTION = 'getRuns'
VARIABLE_DATA_NAME = 'getRunsData'
QUERY = f"""
query GetRunDebugInfo(${VARIABLE_DATA_NAME}: GetRunsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    createdAt
    executionsStatusUpdates {{
      containerStatusUpdates {{
        nodeRank
        containerName
        status
        reachedAt
        reason
      }}
      id
      executionIndex
      podStatusUpdates {{
        nodeRank
        nodeName
        status
        reachedAt
        reason
      }}
    }}
  }}
}}"""


@overload
def get_run_debug_info(run: Union[str, Run],
                       timeout: Optional[float] = 10,
                       future: Literal[False] = False) -> RunDebugInfo:
    ...


@overload
def get_run_debug_info(run: Union[str, Run],
                       timeout: Optional[float] = None,
                       future: Literal[True] = True) -> Future[RunDebugInfo]:
    ...


def get_run_debug_info(run: Union[str, Run], timeout: Optional[float] = 10, future: bool = False):
    run_name = run.name if isinstance(run, Run) else run
    error_message = f"Run {run_name} not found"

    filters: Dict[str, Any] = {'name': {'in': [run_name]}}
    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters,
            'includeDeleted': True,  # Always include deleted runs for debugging
        }
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME])

    response = run_plural_mapi_request(QUERY,
                                       query_function=QUERY_FUNCTION,
                                       return_model_type=RunDebugInfo,
                                       variables=variables)
    response = convert_plural_future_to_singleton(response, error_message)
    return get_return_response(response, future=future, timeout=timeout)
