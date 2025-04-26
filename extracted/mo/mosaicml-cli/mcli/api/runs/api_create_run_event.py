""" Create a Run Event """
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_singular_mapi_request
from mcli.api.model.run_event import RunEvent

__all__ = ['create_run_event']

QUERY_FUNCTION = 'createRunEvent'
VARIABLE_DATA_NAME = 'createRunEventData'
QUERY = f"""
mutation CreateRunEvent(${VARIABLE_DATA_NAME}: CreateRunEventInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    runId
    executionId
    eventType
    eventData
    updatedAt
}}
}}"""


@overload
def create_run_event(run_name: str,
                     event_type: str,
                     event_data: dict,
                     *,
                     timeout: Optional[float] = 10,
                     future: Literal[False] = False) -> RunEvent:
    ...


@overload
def create_run_event(run_name: str,
                     event_type: str,
                     event_data: dict,
                     *,
                     timeout: Optional[float] = None,
                     future: Literal[True] = True) -> Future[RunEvent]:
    ...


def create_run_event(run_name: str,
                     event_type: str,
                     event_data: dict,
                     *,
                     timeout: Optional[float] = 10,
                     future: bool = False) -> Union[RunEvent, Future[RunEvent]]:
    """Create a run event in the MosaicML platform.

    Args:
        run_name: The name of an existing, non-deleted run. This run must belong to the
            user who is creating the run event.
        event_type: The type of event to create.
        event_data: The data associated with the event.
        timeout: Time, in seconds, in which the call should complete. If the event creation
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `create_run_event` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :type RunEvent: output, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Returns:
        A RunEvent object.
    """

    variables = {
        VARIABLE_DATA_NAME: {
            'runName': run_name,
            'eventType': event_type,
            'eventData': event_data,
        }
    }

    response = run_singular_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=RunEvent,
        variables=variables,
    )

    return get_return_response(response, future=future, timeout=timeout)
