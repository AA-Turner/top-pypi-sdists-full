from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.data_frame import DataFrame
from ...models.data_frame_create import DataFrameCreate
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: DataFrameCreate,
) -> Dict[str, Any]:
    url = "{}/data-frames".format(client.base_url)

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
) -> Optional[Union[DataFrame, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = DataFrame.from_dict(response.json(), strict=False)

        return response_200
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
) -> Response[Union[DataFrame, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: DataFrameCreate,
) -> Response[Union[DataFrame, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: DataFrameCreate,
) -> Optional[Union[DataFrame, BadRequestError, ForbiddenError, NotFoundError]]:
    """Create a data frame.

    Data frames can be created from `.csv` files, and only 1 `.csv` file can currently be uploaded.

    A successful data frame upload requires 3 calls in serial:
    1. [Create a data frame](#/Data%20Frames/createDataFrame), this endpoint, specifying the files to upload. This
       returns a `manifest` containing S3 `PUT` URLs corresponding to the files that will be uploaded for
       the 2nd call and a data frame ID for the 3rd call.
    2. Upload the data frame `.csv` content to S3. Add `x-amz-server-side-encryption: AES256` to the request
       headers, because we use server-side encryption. Here is a `curl` example:
       ```bash
       curl -H \"x-amz-server-side-encryption: AES256\" -X PUT -T <LOCAL_FILE> -L <S3_PUT_URL>
       ```
    3. [Update the data frame](#/Data%20Frames/patchDataFrame) to mark as `IN_PROGRESS` to start a [long-running task](#/Tasks/getTask)
      to process and validate the data frame.
        - For more details on how we process and validate data frames, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference).

    Note: Manifest URLs are valid for 1 hour after being returned from this endpoint. They should not be stored
    persistently for later use.

    CSV files up to 150MB are supported.
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: DataFrameCreate,
) -> Response[Union[DataFrame, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: DataFrameCreate,
) -> Optional[Union[DataFrame, BadRequestError, ForbiddenError, NotFoundError]]:
    """Create a data frame.

    Data frames can be created from `.csv` files, and only 1 `.csv` file can currently be uploaded.

    A successful data frame upload requires 3 calls in serial:
    1. [Create a data frame](#/Data%20Frames/createDataFrame), this endpoint, specifying the files to upload. This
       returns a `manifest` containing S3 `PUT` URLs corresponding to the files that will be uploaded for
       the 2nd call and a data frame ID for the 3rd call.
    2. Upload the data frame `.csv` content to S3. Add `x-amz-server-side-encryption: AES256` to the request
       headers, because we use server-side encryption. Here is a `curl` example:
       ```bash
       curl -H \"x-amz-server-side-encryption: AES256\" -X PUT -T <LOCAL_FILE> -L <S3_PUT_URL>
       ```
    3. [Update the data frame](#/Data%20Frames/patchDataFrame) to mark as `IN_PROGRESS` to start a [long-running task](#/Tasks/getTask)
      to process and validate the data frame.
        - For more details on how we process and validate data frames, [click here](https://docs.benchling.com/docs/datasets-ingestion-reference).

    Note: Manifest URLs are valid for 1 hour after being returned from this endpoint. They should not be stored
    persistently for later use.

    CSV files up to 150MB are supported.
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
