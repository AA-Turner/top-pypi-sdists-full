"""Set job progress via the FastAPI backend."""

from http import HTTPStatus
from typing import Any, Dict, Optional
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response
from ... import errors
from ...models.progress_request import ProgressRequest


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _parse_progress_string(progress_string: str) -> tuple[float, str]:
    """Parse a progress string into a float value and message.

    Handles formats like:
    - "0.5" -> (0.5, "0.5")
    - "50%" -> (0.5, "50%")
    - "50" -> (0.5, "50")
    - "Processing: 75%" -> (0.75, "Processing: 75%")

    Returns:
        Tuple of (progress_float, message_string)
    """
    import re

    # Try to extract a percentage from the string
    percent_match = re.search(r"(\d+(?:\.\d+)?)\s*%", progress_string)
    if percent_match:
        value = float(percent_match.group(1)) / 100.0
        return (min(1.0, max(0.0, value)), progress_string)

    # Try to parse as a plain float
    try:
        value = float(progress_string.strip())
        # If > 1, assume it's a percentage
        if value > 1.0:
            value = value / 100.0
        return (min(1.0, max(0.0, value)), progress_string)
    except ValueError:
        pass

    # Can't parse, default to 0
    return (0.0, progress_string)


def _get_kwargs(
    job_id: str,
    *,
    client: Client = None,
    json_body: ProgressRequest = None,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/apps/jobs/{job_id}/progress"

    headers: Dict[str, str] = client.get_headers()
    headers["Content-Type"] = "application/json"
    cookies: Dict[str, Any] = client.get_cookies()

    if not json_body:
        raise ValueError("json_body is required for setting job progress")

    # Convert old ProgressRequest (string) to new format (float + message)
    progress_float, message = _parse_progress_string(json_body.progress)
    json_data = {
        "progress": progress_float,
        "message": message,
    }

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_data,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    if response.status_code == HTTPStatus.OK:
        return response.json()
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    job_id: str,
    *,
    client: Client = None,
    json_body: ProgressRequest = None,
) -> Response[Dict[str, Any]]:
    """Set job progress.

    Args:
        job_id: The job ID to set progress for.
        client: The Client with which to connect to Octostar.
        json_body: ProgressRequest with the progress string.

    Returns:
        Response with updated job progress data.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(job_id=job_id, client=client, json_body=json_body)

    response = httpx.request(verify=client.verify_ssl, **kwargs)
    if response.is_error:
        print(
            f"{response.status_code} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    job_id: str,
    *,
    client: Client = None,
    json_body: ProgressRequest = None,
) -> Optional[Dict[str, Any]]:
    """Set job progress.

    Args:
        job_id: The job ID to set progress for.
        client: The Client with which to connect to Octostar.
        json_body: ProgressRequest with the progress string.

    Returns:
        Updated job progress data or None if request failed.
    """
    return sync_detailed(job_id=job_id, client=client, json_body=json_body).parsed


async def asyncio_detailed(
    job_id: str,
    *,
    client: Client = None,
    json_body: ProgressRequest = None,
) -> Response[Dict[str, Any]]:
    """Set job progress asynchronously.

    Args:
        job_id: The job ID to set progress for.
        client: The Client with which to connect to Octostar.
        json_body: ProgressRequest with the progress string.

    Returns:
        Response with updated job progress data.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(job_id=job_id, client=client, json_body=json_body)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Client = None,
    json_body: ProgressRequest = None,
) -> Optional[Dict[str, Any]]:
    """Set job progress asynchronously.

    Args:
        job_id: The job ID to set progress for.
        client: The Client with which to connect to Octostar.
        json_body: ProgressRequest with the progress string.

    Returns:
        Updated job progress data or None if request failed.
    """
    return (
        await asyncio_detailed(job_id=job_id, client=client, json_body=json_body)
    ).parsed
