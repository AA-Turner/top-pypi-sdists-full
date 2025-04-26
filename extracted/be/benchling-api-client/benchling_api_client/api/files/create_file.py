from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.file import File
from ...models.file_create import FileCreate
from ...models.forbidden_error import ForbiddenError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: FileCreate,
) -> Dict[str, Any]:
    url = "{}/files".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[File, BadRequestError, ForbiddenError]]:
    if response.status_code == 200:
        response_200 = File.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[File, BadRequestError, ForbiddenError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: FileCreate,
) -> Response[Union[File, BadRequestError, ForbiddenError]]:
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
    json_body: FileCreate,
) -> Optional[Union[File, BadRequestError, ForbiddenError]]:
    """Create a file of a supported type. Currently, we support these file extensions: .csv; .html;
    .jmp, .jrn, .jrp (JMP); .jpeg, .jpg (JPEG); .png; .pdf; .zip; and .txt.

    A successful file upload requires 3 calls in serial:
    1. [Create a file](#/Analyses/createFile), this endpoint, which returns an S3 `PUT` URL for the 2nd
       call and a file ID for the 3rd call
    2. Upload the file contents to S3. Add `x-amz-server-side-encryption: AES256` to the request headers,
       because we use server-side encryption. Here is a `curl` example:
       ```bash
       curl -H \"x-amz-server-side-encryption: AES256\" -X PUT -T <LOCAL_FILE> -L <S3_PUT_URL>
       ```
    3. [Update the file](#/Analyses/patchFile), which marks the upload as `SUCCEEDED`

    Note: URL is valid for 1 hour after being returned from this endpoint. It should not be stored
    persistently for later use.

    Files up to 30MB are supported.
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: FileCreate,
) -> Response[Union[File, BadRequestError, ForbiddenError]]:
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
    json_body: FileCreate,
) -> Optional[Union[File, BadRequestError, ForbiddenError]]:
    """Create a file of a supported type. Currently, we support these file extensions: .csv; .html;
    .jmp, .jrn, .jrp (JMP); .jpeg, .jpg (JPEG); .png; .pdf; .zip; and .txt.

    A successful file upload requires 3 calls in serial:
    1. [Create a file](#/Analyses/createFile), this endpoint, which returns an S3 `PUT` URL for the 2nd
       call and a file ID for the 3rd call
    2. Upload the file contents to S3. Add `x-amz-server-side-encryption: AES256` to the request headers,
       because we use server-side encryption. Here is a `curl` example:
       ```bash
       curl -H \"x-amz-server-side-encryption: AES256\" -X PUT -T <LOCAL_FILE> -L <S3_PUT_URL>
       ```
    3. [Update the file](#/Analyses/patchFile), which marks the upload as `SUCCEEDED`

    Note: URL is valid for 1 hour after being returned from this endpoint. It should not be stored
    persistently for later use.

    Files up to 30MB are supported.
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
