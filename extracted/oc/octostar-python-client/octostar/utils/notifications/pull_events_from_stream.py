import logging

_logger = logging.getLogger(__name__)

from ...api.notifications import pull_events_from_stream
from ...client import Client


def sync(stream_id: str, count: int = 10, client: Client = None):
    """
    # Get Latest Events from Stream

    Retrieves the N latest events in a stream. Events are returned in LIFO order.

    ## Arguments
    - `stream_id`: The unique ID for the event stream.
    - `count`: The number of events to fetch.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of Octostar event instances (containing the event info and contents).

    ## Raises
    - `ConnectionError`: If the request was unsuccessful on the server.
    """
    response = pull_events_from_stream.sync_detailed(
        stream_id=stream_id, count=count, client=client
    )
    if response.status_code != 200:
        logger.error(response.content)
        raise ConnectionError(
            "pull_events_from_stream failed with status code "
            + str(response.status_code)
        )
    return response.parsed


async def asyncio(stream_id: str, count: int = 10, client: Client = None):
    """
    # Get Latest Events from Stream Asynchronously

    Asynchronously retrieves the N latest events in a stream. Events are returned in LIFO order.

    ## Arguments
    - `stream_id`: The unique ID for the event stream.
    - `count`: The number of events to fetch.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of Octostar event instances (containing the event info and contents).

    ## Raises
    - `ConnectionError`: If the request was unsuccessful on the server.
    """
    response = await pull_events_from_stream.asyncio_detailed(
        stream_id=stream_id, count=count, client=client
    )
    if response.status_code != 200:
        logger.error(response.content)
        raise ConnectionError(
            "pull_events_from_stream failed with status code "
            + str(response.status_code)
        )
    return response.parsed
