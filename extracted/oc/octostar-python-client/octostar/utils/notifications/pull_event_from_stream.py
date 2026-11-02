import logging

_logger = logging.getLogger(__name__)

from ...api.notifications import pull_events_from_stream
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(stream_id: str, client: Client = None):
    """
    # Get Latest Event from Stream

    Retrieves the latest event in a stream.

    ## Arguments
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    An Octostar event instance (containing the event info and contents).

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = pull_events_from_stream.sync_detailed(
        stream_id=stream_id, count=1, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("pull_event_from_stream", response, client)
    events = response.parsed
    if events:
        return events[0]
    else:
        return events


async def asyncio(stream_id: str, client: Client = None):
    """
    # Get Latest Event from Stream Asynchronously

    Asynchronously retrieves the latest event in a stream.

    ## Arguments
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    An Octostar event instance (containing the event info and contents).

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await pull_events_from_stream.asyncio_detailed(
        stream_id=stream_id, count=1, client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("pull_event_from_stream", response, client)
    events = response.parsed
    if events:
        return events[0]
    else:
        return events
