from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.async_task_link import AsyncTaskLink
from ...models.audit_log_export import AuditLogExport
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    object_id: str,
    json_body: AuditLogExport,
) -> Dict[str, Any]:
    url = "{}/audit/log/{object_id}".format(client.base_url, object_id=object_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    if response.status_code == 202:
        response_202 = AsyncTaskLink.from_dict(response.json(), strict=False)

        return response_202
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AsyncTaskLink, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    object_id: str,
    json_body: AuditLogExport,
) -> Response[Union[AsyncTaskLink, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        object_id=object_id,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    object_id: str,
    json_body: AuditLogExport,
) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    """This endpoint launches a [long-running task](#/Tasks/getTask) and returns the Task ID of the launched task. The `ExportAuditLogAsyncTask` response contains a link to download the exported audit log file from Amazon S3. This endpoint is subject to a rate limit of 500 requests per hour, in conjunction with the global request rate limit. Export throughput will additionally be rate limited around the scale of 70,000 total audit events exported in csv format or 30,000 total audit events exported in pdf format per hour."""

    return sync_detailed(
        client=client,
        object_id=object_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    object_id: str,
    json_body: AuditLogExport,
) -> Response[Union[AsyncTaskLink, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        object_id=object_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    object_id: str,
    json_body: AuditLogExport,
) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    """This endpoint launches a [long-running task](#/Tasks/getTask) and returns the Task ID of the launched task. The `ExportAuditLogAsyncTask` response contains a link to download the exported audit log file from Amazon S3. This endpoint is subject to a rate limit of 500 requests per hour, in conjunction with the global request rate limit. Export throughput will additionally be rate limited around the scale of 70,000 total audit events exported in csv format or 30,000 total audit events exported in pdf format per hour."""

    return (
        await asyncio_detailed(
            client=client,
            object_id=object_id,
            json_body=json_body,
        )
    ).parsed
