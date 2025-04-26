from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.async_task_link import AsyncTaskLink
from ...models.bad_request_error import BadRequestError
from ...models.data_frame_update import DataFrameUpdate
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    data_frame_id: str,
    json_body: DataFrameUpdate,
) -> Dict[str, Any]:
    url = "{}/data-frames/{data_frame_id}".format(client.base_url, data_frame_id=data_frame_id)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 202:
        response_202 = AsyncTaskLink.from_dict(response.json(), strict=False)

        return response_202
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    data_frame_id: str,
    json_body: DataFrameUpdate,
) -> Response[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        data_frame_id=data_frame_id,
        json_body=json_body,
    )

    response = client.httpx_client.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    data_frame_id: str,
    json_body: DataFrameUpdate,
) -> Optional[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    """Update a data frame.

    After uploading a `.csv` data drame file to S3, call this endpoint to mark the upload status as `IN_PROGRESS`
    to launch a [long-running task](#/Tasks/getTask) to validate and transform the raw `.csv` file into a
    data frame. Once complete, the data frame's status will either be updated to `SUCCEEDED` or `FAILED_VALIDATION`.

    For more details on how we process and validate data frames, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference).

    See [Create a data frame](#/Data%20Frames/createDataFrame) for documentation of the full upload flow.
    """

    return sync_detailed(
        client=client,
        data_frame_id=data_frame_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    data_frame_id: str,
    json_body: DataFrameUpdate,
) -> Response[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        data_frame_id=data_frame_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    data_frame_id: str,
    json_body: DataFrameUpdate,
) -> Optional[Union[AsyncTaskLink, BadRequestError, ForbiddenError, NotFoundError]]:
    """Update a data frame.

    After uploading a `.csv` data drame file to S3, call this endpoint to mark the upload status as `IN_PROGRESS`
    to launch a [long-running task](#/Tasks/getTask) to validate and transform the raw `.csv` file into a
    data frame. Once complete, the data frame's status will either be updated to `SUCCEEDED` or `FAILED_VALIDATION`.

    For more details on how we process and validate data frames, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference).

    See [Create a data frame](#/Data%20Frames/createDataFrame) for documentation of the full upload flow.
    """

    return (
        await asyncio_detailed(
            client=client,
            data_frame_id=data_frame_id,
            json_body=json_body,
        )
    ).parsed
