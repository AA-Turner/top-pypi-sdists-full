import logging
import httpx

_logger = logging.getLogger(__name__)

from ...client import Client, get_default_client
from ..commons import network_retry_strategy
from ..exceptions import ApiConnectionError


DEFAULT_TIMEOUT = 120


def _delete_api_url(client: Client, filename: str) -> str:
    """Build the blob delete API endpoint URL."""
    base = client.get_base_url_v1()
    return f"{base}/api/v1/files/delete-blob/{filename}"


def sync(
    filename: str,
    client: Client = None,
):
    """
    # Delete a temporary blob from the user's temp bucket

    Permanently removes a file from the authenticated user's temporary S3 bucket.
    Use this to clean up temporary files that are no longer needed.

    ## Arguments
    - `filename`: The name of the file in the temp bucket to delete
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Raises
    - `ApiConnectionError`: If the deletion request failed
    """
    if not client:
        client = get_default_client()

    api_url = _delete_api_url(client, filename)
    headers = dict(client.get_headers())

    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                with httpx.Client(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = http_client.delete(api_url, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("delete_temporary_blob", response, client)


async def asyncio(
    filename: str,
    client: Client = None,
):
    """
    # Delete a temporary blob from the user's temp bucket (async)

    Permanently removes a file from the authenticated user's temporary S3 bucket.
    Use this to clean up temporary files that are no longer needed.

    ## Arguments
    - `filename`: The name of the file in the temp bucket to delete
    - `client`: The Client with which to connect to Octostar. If None, the default one is used

    ## Raises
    - `ApiConnectionError`: If the deletion request failed
    """
    if not client:
        client = get_default_client()

    api_url = _delete_api_url(client, filename)
    headers = dict(client.get_headers())

    response = None
    try:
        for attempt in network_retry_strategy():
            with attempt:
                async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as http_client:
                    response = await http_client.delete(api_url, headers=headers)
                    response.raise_for_status()
    except Exception:
        raise ApiConnectionError("delete_temporary_blob", response, client)
