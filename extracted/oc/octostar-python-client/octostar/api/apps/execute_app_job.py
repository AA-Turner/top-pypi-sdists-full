"""Execute a job via the FastAPI backend."""

from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors
from ...models.execute_app_job_json_body import ExecuteAppJobJsonBody


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    json_body: ExecuteAppJobJsonBody = None,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/apps/jobs/execute"

    headers: Dict[str, str] = client.get_headers()
    headers["Content-Type"] = "application/json"
    cookies: Dict[str, Any] = client.get_cookies()

    if not json_body:
        raise ValueError("json_body is required for executing a job")

    # Convert old ExecuteAppJobJsonBody to new JobExecuteRequest format
    body_dict = json_body.to_dict()

    # Map old format to new format
    # Old: ancestor, ontology, image, is_frontend, archive, manifest, annotation, commands
    # New: ancestor, commands, environment, annotations, timeout

    commands = body_dict.get("commands", [])
    if isinstance(commands, str):
        commands = [commands]

    json_data = {
        "ancestor": body_dict["ancestor"],
        "commands": commands,
    }

    # Map annotation to annotations
    if "annotation" in body_dict and body_dict["annotation"]:
        json_data["annotations"] = body_dict["annotation"]

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
    *,
    client: Client = None,
    json_body: ExecuteAppJobJsonBody = None,
) -> Response[Dict[str, Any]]:
    """Execute a new job.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: ExecuteAppJobJsonBody with job configuration.

    Returns:
        Response with job execution data including:
        - job_id: The generated job ID
        - status: Job status
        - ancestor: Parent app ID
        - namespace: K8s namespace
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(client=client, json_body=json_body)

    response = httpx.request(verify=client.verify_ssl, **kwargs)
    if response.is_error:
        print(
            f"{response.status_code} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client = None,
    json_body: ExecuteAppJobJsonBody = None,
) -> Optional[Dict[str, Any]]:
    """Execute a new job.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: ExecuteAppJobJsonBody with job configuration.

    Returns:
        Job execution data or None if request failed.
    """
    return sync_detailed(client=client, json_body=json_body).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: ExecuteAppJobJsonBody = None,
) -> Response[Dict[str, Any]]:
    """Execute a new job asynchronously.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: ExecuteAppJobJsonBody with job configuration.

    Returns:
        Response with job execution data.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(client=client, json_body=json_body)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: ExecuteAppJobJsonBody = None,
) -> Optional[Dict[str, Any]]:
    """Execute a new job asynchronously.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: ExecuteAppJobJsonBody with job configuration.

    Returns:
        Job execution data or None if request failed.
    """
    return (await asyncio_detailed(client=client, json_body=json_body)).parsed
