""" Update the metadata of a run. """
from __future__ import annotations

import json
import logging
import math
from concurrent.futures import Future
from typing import Any, Dict, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.run import Run
from mcli.config import MCLIConfig
from mcli.utils.utils_logging import WARN

logger = logging.getLogger(__name__)

__all__ = ['update_run_metadata']

QUERY_FUNCTION = 'updateRunMetadata'
VARIABLE_DATA_GET_RUNS = 'getRunsData'
VARIABLE_DATA_UPDATE_RUN_METADATA = 'updateRunMetadataData'
QUERY = f"""
mutation UpdateRunMetadata(${VARIABLE_DATA_GET_RUNS}: GetRunsInput!, ${VARIABLE_DATA_UPDATE_RUN_METADATA}: UpdateRunMetadataInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_GET_RUNS}: ${VARIABLE_DATA_GET_RUNS}, {VARIABLE_DATA_UPDATE_RUN_METADATA}: ${VARIABLE_DATA_UPDATE_RUN_METADATA}) {{
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
        metadata
    }}
  }}
}}"""


@overload
def update_run_metadata(run: Union[str, Run],
                        metadata: Dict[str, Any],
                        *,
                        timeout: Optional[float] = None,
                        future: Literal[False] = False,
                        protect: bool = False) -> Run:
    ...


@overload
def update_run_metadata(run: Union[str, Run],
                        metadata: Dict[str, Any],
                        *,
                        timeout: Optional[float] = None,
                        future: Literal[True] = True,
                        protect: bool = False) -> Future[Run]:
    ...


@overload
def update_run_metadata(run: Union[str, Run],
                        metadata: Dict[str, Any],
                        *,
                        timeout: Literal[None] = None,
                        future: bool = False,
                        protect: Literal[True] = True) -> Union[Run, Future[Run]]:
    ...


def update_run_metadata(run: Union[str, Run],
                        metadata: Dict[str, Any],
                        *,
                        timeout: Optional[float] = 10,
                        future: bool = False,
                        protect: bool = False):
    """Update a run's metadata in the MosaicML platform.

    Args:
        run (``Optional[str | ``:class:`~mcli.api.model.run.Run` ``]``):
            A run or run name to update. Using :class:`~mcli.api.model.run.Run` objects is most
            efficient. See the note below.
        metadata (`Dict[str, Any]`): The metadata to update the run with. This will be merged with
            the existing metadata. Keys not specified in this dictionary will not be modified.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the call takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`update_run_metadata` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of :class:`~mcli.api.model.run.Run` output,
            use ``return_value.result()`` with an optional ``timeout`` argument.
        protect (``bool``): If True, the call will be protected from SIGTERMs to allow it to 
            complete reliably. Defaults to False.

    Raises:
        MAPIException: Raised if updating the requested run failed

    Returns:
        If future is False:
            Updated :class:`~mcli.api.model.run.Run` object
        Otherwise:
            A :class:`~concurrent.futures.Future` for the list
    """
    valid_metadata = validate_metadata(metadata)
    variables = {
        VARIABLE_DATA_GET_RUNS: {
            'filters': {
                'name': {
                    'in': [run.name if isinstance(run, Run) else run]
                },
            }
        },
        VARIABLE_DATA_UPDATE_RUN_METADATA: {
            'metadata': valid_metadata
        },
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_GET_RUNS])

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Run,
        variables=variables,
        protect=protect,
    )
    return get_return_response(response, future=future, timeout=timeout)


def validate_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Validate a metadata dictionary to ensure it can be serialized to JSON.

    Args:
        metadata (`Dict[str, Any]`): The metadata to validate.

    Raises:
        TypeError: Raised if keys in the metadata cannot be serialized to JSON.

    Returns:
        A validate metadata dictionary.
    """
    valid_metadata = {}
    invalid_keys = []

    for key, value in metadata.items():
        # Serialize metadata values if possible, else ignore them
        serialized_value, is_serializable = serialize_value(value)
        if is_serializable:
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                value = serialized_value
            valid_metadata[key] = value
        else:
            invalid_keys.append(key)
    if invalid_keys:
        # pylint: disable=deprecated-method
        logger.warn(f"{WARN} Metadata value for key '{invalid_keys}' is not JSON serializable. Ignoring.")
    return valid_metadata


def serialize_value(value: Any) -> tuple[Any, bool]:
    """Determine if a value is JSON serializable and serialize it if possible."""
    try:
        return json.dumps(value), True
    except TypeError:
        return None, False
