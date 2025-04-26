from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...extensions import UnknownType
from ...models.bad_request_error import BadRequestError
from ...models.batch import Batch
from ...models.container import Container
from ...models.generic_entity import GenericEntity
from ...models.plate import Plate
from ...models.worklist_item_create import WorklistItemCreate
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    worklist_id: str,
    json_body: WorklistItemCreate,
) -> Dict[str, Any]:
    url = "{}/worklists/{worklist_id}/items".format(client.base_url, worklist_id=worklist_id)

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
) -> Optional[
    Union[
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        BadRequestError,
    ]
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: Union[Dict[str, Any]]
        ) -> Union[Batch, Container, GenericEntity, Plate, UnknownType]:
            response_200: Union[Batch, Container, GenericEntity, Plate, UnknownType]
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = Batch.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = Container.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = GenericEntity.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = Plate.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            return UnknownType(data)

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 201:

        def _parse_response_201(
            data: Union[Dict[str, Any]]
        ) -> Union[Batch, Container, GenericEntity, Plate, UnknownType]:
            response_201: Union[Batch, Container, GenericEntity, Plate, UnknownType]
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = Batch.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = Container.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = GenericEntity.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_item = Plate.from_dict(data, strict=True)

                return worklist_item
            except:  # noqa: E722
                pass
            return UnknownType(data)

        response_201 = _parse_response_201(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[
    Union[
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        BadRequestError,
    ]
]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    worklist_id: str,
    json_body: WorklistItemCreate,
) -> Response[
    Union[
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        BadRequestError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        worklist_id=worklist_id,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    worklist_id: str,
    json_body: WorklistItemCreate,
) -> Optional[
    Union[
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        BadRequestError,
    ]
]:
    """Appends an item to the end of a worklist if the item is not already present in the worklist. Returns 200 OK if the item was already present in the worklist and does not change that item's position."""

    return sync_detailed(
        client=client,
        worklist_id=worklist_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    worklist_id: str,
    json_body: WorklistItemCreate,
) -> Response[
    Union[
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        BadRequestError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        worklist_id=worklist_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    worklist_id: str,
    json_body: WorklistItemCreate,
) -> Optional[
    Union[
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        Union[Batch, Container, GenericEntity, Plate, UnknownType],
        BadRequestError,
    ]
]:
    """Appends an item to the end of a worklist if the item is not already present in the worklist. Returns 200 OK if the item was already present in the worklist and does not change that item's position."""

    return (
        await asyncio_detailed(
            client=client,
            worklist_id=worklist_id,
            json_body=json_body,
        )
    ).parsed
