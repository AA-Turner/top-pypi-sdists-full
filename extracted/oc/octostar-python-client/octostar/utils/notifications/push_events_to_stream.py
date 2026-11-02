import os
import logging
from typing import TypedDict, List

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


class __PushEvent(TypedDict, total=False):
    message: str
    description: str
    level: str


def sync(
    events: List[__PushEvent],
    channel: str = "octostar:desktop:builtins:showToast",
    stream_id: str = os.getenv("OS_JOB_ID") or os.getenv("OS_APP_ID"),
    client: Client = None,
):
    """
    # Add Multiple Events to Stream

    Adds N new events to an event stream, in order. Note that, when pulling from a stream,
    events are returned in LIFO order.

    ## Arguments
    - `events`: A list of dictionaries, one per event to add.
        Each dictionary must contain:
        - `message`: The main content to write to the event.
        - `description`: The secondary content to write to the event.
        - `level`: A string detailing the event level. Can be "debug", "error", "info" or "warning".
    - `channel`: The event channel. See OsMessageType for its possible values.
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The number of events successfully pushed to the stream.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    for i in range(len(events)):
        event = events[i]
        response = push_event_to_stream.sync_detailed(
            stream_id=stream_id,
            client=client,
            json_body=OctostarEvent(
                octostar_channel=channel,
                octostar_payload=OctostarEventOctostarPayload(
                    message=event["message"],
                    description=(
                        UNSET
                        if "description" not in event or not event["description"]
                        else event["description"]
                    ),
                    level=(
                        UNSET
                        if "level" not in event or not event["level"]
                        else OctostarEventOctostarPayloadLevel(event["level"])
                    ),
                ),
            ),
        )
        if response.status_code not in (200, 201) or (
            "status" in response.parsed.additional_properties
            and response.parsed.additional_properties["status"] != "success"
        ):
            raise ApiConnectionError("push_events_to_stream", response, client)
    return i


async def asyncio(
    events: List[__PushEvent],
    channel: str = "octostar:desktop:builtins:showToast",
    stream_id: str = os.getenv("OS_APP_ID"),
    client: Client = None,
):
    """
    # Add Multiple Events to Stream Asynchronously

    Asynchronously adds N new events to an event stream, in order. Note that, when pulling from a stream,
    events are returned in LIFO order.

    ## Arguments
    - `events`: A list of dictionaries, one per event to add.
        Each dictionary must contain:
        - `message`: The main content to write to the event.
        - `description`: The secondary content to write to the event.
        - `level`: A string detailing the event level. Can be "debug", "error", "info" or "warning".
    - `channel`: The event channel. See OsMessageType for its possible values.
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The number of events successfully pushed to the stream.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    for i in range(len(events)):
        event = events[i]
        response = await push_event_to_stream.asyncio_detailed(
            stream_id=stream_id,
            client=client,
            json_body=OctostarEvent(
                octostar_channel=channel,
                octostar_payload=OctostarEventOctostarPayload(
                    message=event["message"],
                    description=(
                        UNSET
                        if "description" not in event or not event["description"]
                        else event["description"]
                    ),
                    level=(
                        UNSET
                        if "level" not in event or not event["level"]
                        else event["level"]
                    ),
                ),
            ),
        )
        if response.status_code not in (200, 201) or (
            "status" in response.parsed.additional_properties
            and response.parsed.additional_properties["status"] != "success"
        ):
            raise ApiConnectionError("push_events_to_stream", response, client)
    return i
