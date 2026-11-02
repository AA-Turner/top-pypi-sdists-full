import os
import logging
from typing import Union

_logger = logging.getLogger(__name__)

from ...api.notifications import push_event_to_stream
from ...models.octostar_event import OctostarEvent
from ...models.octostar_event_octostar_payload import OctostarEventOctostarPayload
from ...models.octostar_event_octostar_payload_level import (
    OctostarEventOctostarPayloadLevel,
)
from ...client import Client
from ...types import UNSET
from ..exceptions import ApiConnectionError


def sync(
    message: str,
    description: Union[str, None] = None,
    level: Union[str, None] = None,
    channel: str = "octostar:desktop:builtins:showToast",
    stream_id: str = os.getenv("OS_JOB_ID") or os.getenv("OS_APP_ID"),
    client: Client = None,
):
    """
    # Add Event to Stream

    Adds a new event to an event stream.

    ## Arguments
    - `message`: The main content to write to the event.
    - `description`: The secondary content to write to the event.
    - `level`: A string detailing the event level. Can be "debug", "error", "info" or "warning".
    - `channel`: The event channel. See OsMessageType for its possible values.
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    `True` if the event was added successfully to the stream.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = push_event_to_stream.sync_detailed(
        stream_id=stream_id,
        client=client,
        json_body=OctostarEvent(
            octostar_stream=channel,
            octostar_payload=OctostarEventOctostarPayload(
                message=message,
                description=description if description else UNSET,
                level=OctostarEventOctostarPayloadLevel(level) if level else UNSET,
            ),
        ),
    )
    if response.status_code not in (200, 201) or (
        "status" in response.parsed.additional_properties
        and response.parsed.additional_properties["status"] != "success"
    ):
        raise ApiConnectionError("push_event_from_stream", response, client)
    return True


async def asyncio(
    message: str,
    description: Union[str, None] = None,
    level: Union[str, None] = None,
    channel: str = "octostar:desktop:builtins:showToast",
    stream_id: str = os.getenv("OS_JOB_ID") or os.getenv("OS_APP_ID"),
    client: Client = None,
):
    """
    # Add Event to Stream Asynchronously

    Asynchronously adds a new event to an event stream.

    ## Arguments
    - `message`: The main content to write to the event.
    - `description`: The secondary content to write to the event.
    - `level`: A string detailing the event level. Can be "debug", "error", "info" or "warning".
    - `channel`: The event channel. See OsMessageType for its possible values.
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    `True` if the event was added successfully to the stream.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await push_event_to_stream.asyncio_detailed(
        stream_id=stream_id,
        client=client,
        json_body=OctostarEvent(
            octostar_stream=channel,
            octostar_payload=OctostarEventOctostarPayload(
                message=message,
                description=description if description else UNSET,
                level=OctostarEventOctostarPayloadLevel(level) if level else UNSET,
            ),
        ),
    )
    if response.status_code not in (200, 201) or (
        "status" in response.parsed.additional_properties
        and response.parsed.additional_properties["status"] != "success"
    ):
        raise ApiConnectionError("push_event_from_stream", response, client)
    return True
