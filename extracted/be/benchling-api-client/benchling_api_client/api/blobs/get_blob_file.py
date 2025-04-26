from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    blob_id: str,
) -> Dict[str, Any]:
    url = "{}/blobs/{blob_id}/download".format(client.base_url, blob_id=blob_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, None, NotFoundError]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 302:
        response_302 = None

        return response_302
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, None, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    blob_id: str,
) -> Response[Union[None, None, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_id=blob_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    blob_id: str,
) -> Optional[Union[None, None, NotFoundError]]:
    """ Download a blob.

This endpoint issues a 302 redirect to a pre-signed download link.
It does not consume from the standard rate-limit.

Example `wget` usage with a User API Key:
```bash
export BLOB_ID=\"ffe43fd5-b928-4996-9b7f-40222cd33d8e\"
wget \"https://tenant.benchling.com/api/v2/blobs/$BLOB_ID/download\" \
    --user $API_TOKEN \      # Your API Key
    --password '' \          # Leave password empty
    --content-disposition    # Save file with original filename
```

**Note: Calling this endpoint from a browser is not supported.**
 """

    return sync_detailed(
        client=client,
        blob_id=blob_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    blob_id: str,
) -> Response[Union[None, None, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_id=blob_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    blob_id: str,
) -> Optional[Union[None, None, NotFoundError]]:
    """ Download a blob.

This endpoint issues a 302 redirect to a pre-signed download link.
It does not consume from the standard rate-limit.

Example `wget` usage with a User API Key:
```bash
export BLOB_ID=\"ffe43fd5-b928-4996-9b7f-40222cd33d8e\"
wget \"https://tenant.benchling.com/api/v2/blobs/$BLOB_ID/download\" \
    --user $API_TOKEN \      # Your API Key
    --password '' \          # Leave password empty
    --content-disposition    # Save file with original filename
```

**Note: Calling this endpoint from a browser is not supported.**
 """

    return (
        await asyncio_detailed(
            client=client,
            blob_id=blob_id,
        )
    ).parsed
