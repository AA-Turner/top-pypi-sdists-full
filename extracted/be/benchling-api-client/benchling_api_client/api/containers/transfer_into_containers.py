from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.async_task_link import AsyncTaskLink
from ...models.bad_request_error import BadRequestError
from ...models.multiple_containers_transfers_list import MultipleContainersTransfersList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: MultipleContainersTransfersList,
) -> Dict[str, Any]:
    url = "{}/transfers".format(client.base_url)

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
    json_body: MultipleContainersTransfersList,
) -> Response[Union[AsyncTaskLink, BadRequestError]]:
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
    json_body: MultipleContainersTransfersList,
) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    """Transfers a volume of an entity or container into a destination container. Limit of 5000 transfers per request. Concentration of all contents in the destination container will be automatically updated based on the previous volume & concentrations of the contents in that container, the concentration of the contents being transferred in, the volume of the contents being transferred in, and the final volume of the container. If no concentration is specified, the concentration will not be tracked."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: MultipleContainersTransfersList,
) -> Response[Union[AsyncTaskLink, BadRequestError]]:
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
    json_body: MultipleContainersTransfersList,
) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    """Transfers a volume of an entity or container into a destination container. Limit of 5000 transfers per request. Concentration of all contents in the destination container will be automatically updated based on the previous volume & concentrations of the contents in that container, the concentration of the contents being transferred in, the volume of the contents being transferred in, and the final volume of the container. If no concentration is specified, the concentration will not be tracked."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
