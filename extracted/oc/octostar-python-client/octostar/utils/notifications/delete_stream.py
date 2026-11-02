import os
import logging

_logger = logging.getLogger(__name__)

from ...api.notifications import delete_stream
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(stream_id: str, client: Client = None):
    """
    # Delete Event Stream

    Deletes an event stream.

    ## Arguments
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    `True` if the event stream has been deleted successfully.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = delete_stream.sync_detailed(stream_id=stream_id, client=client)
    if response.status_code != 200 or (
        "status" in response.parsed.additional_properties
        and response.parsed.additional_properties["status"] != "success"
    ):
        raise ApiConnectionError("delete_stream", response, client)
    return True


async def asyncio(stream_id: str, client: Client = None):
    """
    # Delete Event Stream Asynchronously

    Asynchronously deletes an event stream.

    ## Arguments
    - `stream_id`: The unique ID for the event stream.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    `True` if the event stream has been deleted successfully.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await delete_stream.asyncio_detailed(stream_id=stream_id, client=client)
    if response.status_code != 200 or (
        "status" in response.parsed.additional_properties
        and response.parsed.additional_properties["status"] != "success"
    ):
        raise ApiConnectionError("delete_stream", response, client)
    return True
