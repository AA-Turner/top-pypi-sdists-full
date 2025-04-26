from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.data_frame import DataFrame
from ...models.forbidden_error import ForbiddenError
from ...models.get_data_frame_row_data_format import GetDataFrameRowDataFormat
from ...models.not_found_error import NotFoundError
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    data_frame_id: str,
    returning: Union[Unset, str] = UNSET,
    row_data_format: Union[Unset, GetDataFrameRowDataFormat] = UNSET,
) -> Dict[str, Any]:
    url = "{}/data-frames/{data_frame_id}".format(client.base_url, data_frame_id=data_frame_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_row_data_format: Union[Unset, int] = UNSET
    if not isinstance(row_data_format, Unset):
        json_row_data_format = row_data_format.value

    params: Dict[str, Any] = {}
    if not isinstance(returning, Unset) and returning is not None:
        params["returning"] = returning
    if not isinstance(json_row_data_format, Unset) and json_row_data_format is not None:
        params["rowDataFormat"] = json_row_data_format

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DataFrame, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = DataFrame.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DataFrame, ForbiddenError, NotFoundError]]:
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
    returning: Union[Unset, str] = UNSET,
    row_data_format: Union[Unset, GetDataFrameRowDataFormat] = UNSET,
) -> Response[Union[DataFrame, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        data_frame_id=data_frame_id,
        returning=returning,
        row_data_format=row_data_format,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    data_frame_id: str,
    returning: Union[Unset, str] = UNSET,
    row_data_format: Union[Unset, GetDataFrameRowDataFormat] = UNSET,
) -> Optional[Union[DataFrame, ForbiddenError, NotFoundError]]:
    """Get a data frame and URLs to download its data.

    If the data frame has `SUCCEEDED` status, the `manifest` field in the response will contain URLs to each
    part of a data frame that can be downloaded and the names of the files.

    If the data frame has `NOT_UPLOADED` status, the `manifest` field in the response will contain S3 `PUT` URLs
    to upload data frame `.csv` files. See [Create a data frame](#/Data%20Frames/createDataFrames) for documentation of
    the full upload flow.

    If the data frame has `FAILED_VALIDATION` or `IN_PROGRESS` status, the `manifest` field in the response will
    only contain the names of the files and urls will be `null`.

    Notes:
      - Using this endpoint with `rowDataFormat=csv` might be slow and timeout on large data frames.
       We suggest using `rowDataFormat=parquet` for large data frames.
      - Manifest URLs are valid for 1 hour after being returned from this endpoint. They should not be stored
    persistently for later use.
    """

    return sync_detailed(
        client=client,
        data_frame_id=data_frame_id,
        returning=returning,
        row_data_format=row_data_format,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    data_frame_id: str,
    returning: Union[Unset, str] = UNSET,
    row_data_format: Union[Unset, GetDataFrameRowDataFormat] = UNSET,
) -> Response[Union[DataFrame, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        data_frame_id=data_frame_id,
        returning=returning,
        row_data_format=row_data_format,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    data_frame_id: str,
    returning: Union[Unset, str] = UNSET,
    row_data_format: Union[Unset, GetDataFrameRowDataFormat] = UNSET,
) -> Optional[Union[DataFrame, ForbiddenError, NotFoundError]]:
    """Get a data frame and URLs to download its data.

    If the data frame has `SUCCEEDED` status, the `manifest` field in the response will contain URLs to each
    part of a data frame that can be downloaded and the names of the files.

    If the data frame has `NOT_UPLOADED` status, the `manifest` field in the response will contain S3 `PUT` URLs
    to upload data frame `.csv` files. See [Create a data frame](#/Data%20Frames/createDataFrames) for documentation of
    the full upload flow.

    If the data frame has `FAILED_VALIDATION` or `IN_PROGRESS` status, the `manifest` field in the response will
    only contain the names of the files and urls will be `null`.

    Notes:
      - Using this endpoint with `rowDataFormat=csv` might be slow and timeout on large data frames.
       We suggest using `rowDataFormat=parquet` for large data frames.
      - Manifest URLs are valid for 1 hour after being returned from this endpoint. They should not be stored
    persistently for later use.
    """

    return (
        await asyncio_detailed(
            client=client,
            data_frame_id=data_frame_id,
            returning=returning,
            row_data_format=row_data_format,
        )
    ).parsed
