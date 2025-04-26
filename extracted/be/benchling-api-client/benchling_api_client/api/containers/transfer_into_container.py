from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.container_transfer import ContainerTransfer
from ...models.empty_object import EmptyObject
from ...models.forbidden_restricted_sample_error import ForbiddenRestrictedSampleError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    destination_container_id: str,
    json_body: ContainerTransfer,
) -> Dict[str, Any]:
    url = "{}/containers/{destination_container_id}:transfer".format(
        client.base_url, destination_container_id=destination_container_id
    )

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
) -> Optional[Union[EmptyObject, BadRequestError, ForbiddenRestrictedSampleError]]:
    if response.status_code == 200:
        response_200 = EmptyObject.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenRestrictedSampleError.from_dict(response.json(), strict=False)

        return response_403
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[EmptyObject, BadRequestError, ForbiddenRestrictedSampleError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    destination_container_id: str,
    json_body: ContainerTransfer,
) -> Response[Union[EmptyObject, BadRequestError, ForbiddenRestrictedSampleError]]:
    kwargs = _get_kwargs(
        client=client,
        destination_container_id=destination_container_id,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    destination_container_id: str,
    json_body: ContainerTransfer,
) -> Optional[Union[EmptyObject, BadRequestError, ForbiddenRestrictedSampleError]]:
    """Transfers a volume of an entity or container into a destination container.
    Transfering a volume is cumulative with the existing destination container's contents. To transfer an entire container's contents, the sourceContainerId should be specified. To otherwise transfer multiple entities within a container, you can make multiple calls to this endpoint, specifying a single entity with each call.
    """

    return sync_detailed(
        client=client,
        destination_container_id=destination_container_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    destination_container_id: str,
    json_body: ContainerTransfer,
) -> Response[Union[EmptyObject, BadRequestError, ForbiddenRestrictedSampleError]]:
    kwargs = _get_kwargs(
        client=client,
        destination_container_id=destination_container_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    destination_container_id: str,
    json_body: ContainerTransfer,
) -> Optional[Union[EmptyObject, BadRequestError, ForbiddenRestrictedSampleError]]:
    """Transfers a volume of an entity or container into a destination container.
    Transfering a volume is cumulative with the existing destination container's contents. To transfer an entire container's contents, the sourceContainerId should be specified. To otherwise transfer multiple entities within a container, you can make multiple calls to this endpoint, specifying a single entity with each call.
    """

    return (
        await asyncio_detailed(
            client=client,
            destination_container_id=destination_container_id,
            json_body=json_body,
        )
    ).parsed
