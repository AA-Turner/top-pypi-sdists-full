"""Get job logs from the FastAPI backend."""

from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    job_id: str,
    *,
    client: Client = None,
    since_seconds: Union[Unset, None, int] = UNSET,
    tail_lines: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/apps/jobs/{job_id}/logs"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    if not isinstance(since_seconds, Unset) and since_seconds is not None:
        params["since_seconds"] = since_seconds
    if not isinstance(tail_lines, Unset) and tail_lines is not None:
        params["tail_lines"] = tail_lines

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "params": params,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[bytes]:
    """Parse response - returns raw bytes for log content."""
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    if response.status_code == HTTPStatus.OK:
        return response.content
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[bytes]:
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
    since_seconds: Union[Unset, None, int] = UNSET,
    tail_lines: Union[Unset, None, int] = UNSET,
) -> Response[bytes]:
    """Get job logs.

    Args:
        job_id: The job ID to get logs for.
        client: The Client with which to connect to Octostar.
        since_seconds: Only return logs from the last N seconds.
        tail_lines: Only return the last N lines.

    Returns:
        Response with raw log content in bytes.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(
        job_id=job_id,
        client=client,
        since_seconds=since_seconds,
        tail_lines=tail_lines,
    )

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
    since_seconds: Union[Unset, None, int] = UNSET,
    tail_lines: Union[Unset, None, int] = UNSET,
) -> Optional[bytes]:
    """Get job logs.

    Args:
        job_id: The job ID to get logs for.
        client: The Client with which to connect to Octostar.
        since_seconds: Only return logs from the last N seconds.
        tail_lines: Only return the last N lines.

    Returns:
        Raw log content or None if request failed.
    """
    response = sync_detailed(
        job_id=job_id,
        client=client,
        since_seconds=since_seconds,
        tail_lines=tail_lines,
    )
    if response.status_code == HTTPStatus.OK:
        return response.content
    return None


async def asyncio_detailed(
    job_id: str,
    *,
    client: Client = None,
    since_seconds: Union[Unset, None, int] = UNSET,
    tail_lines: Union[Unset, None, int] = UNSET,
) -> Response[bytes]:
    """Get job logs asynchronously.

    Args:
        job_id: The job ID to get logs for.
        client: The Client with which to connect to Octostar.
        since_seconds: Only return logs from the last N seconds.
        tail_lines: Only return the last N lines.

    Returns:
        Response with raw log content.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(
        job_id=job_id,
        client=client,
        since_seconds=since_seconds,
        tail_lines=tail_lines,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    job_id: str,
    *,
    client: Client = None,
    since_seconds: Union[Unset, None, int] = UNSET,
    tail_lines: Union[Unset, None, int] = UNSET,
) -> Optional[bytes]:
    """Get job logs asynchronously.

    Args:
        job_id: The job ID to get logs for.
        client: The Client with which to connect to Octostar.
        since_seconds: Only return logs from the last N seconds.
        tail_lines: Only return the last N lines.

    Returns:
        Raw log content or None if request failed.
    """
    response = await asyncio_detailed(
        job_id=job_id,
        client=client,
        since_seconds=since_seconds,
        tail_lines=tail_lines,
    )
    if response.status_code == HTTPStatus.OK:
        return response.content
    return None
