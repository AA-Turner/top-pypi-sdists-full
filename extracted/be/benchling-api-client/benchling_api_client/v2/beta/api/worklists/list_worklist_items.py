from typing import Any, cast, Dict, Optional, Union

import httpx

from ...client import Client
from ...extensions import UnknownType
from ...models.bad_request_error import BadRequestError
from ...models.batch_worklist_items_list import BatchWorklistItemsList
from ...models.container_worklist_items_list import ContainerWorklistItemsList
from ...models.entity_worklist_items_list import EntityWorklistItemsList
from ...models.plate_worklist_items_list import PlateWorklistItemsList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    worklist_id: str,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/worklists/{worklist_id}/items".format(client.base_url, worklist_id=worklist_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[
    Union[
        Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: Union[Dict[str, Any]]
        ) -> Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ]:
            response_200: Union[
                ContainerWorklistItemsList,
                EntityWorklistItemsList,
                PlateWorklistItemsList,
                BatchWorklistItemsList,
                UnknownType,
            ]
            discriminator_value: str = cast(str, data.get("type"))
            if discriminator_value is not None:
                worklist_items_paginated_list: Union[
                    ContainerWorklistItemsList,
                    EntityWorklistItemsList,
                    PlateWorklistItemsList,
                    BatchWorklistItemsList,
                    UnknownType,
                ]
                if discriminator_value == "batch":
                    worklist_items_paginated_list = BatchWorklistItemsList.from_dict(data, strict=False)

                    return worklist_items_paginated_list
                if discriminator_value == "bioentity":
                    worklist_items_paginated_list = EntityWorklistItemsList.from_dict(data, strict=False)

                    return worklist_items_paginated_list
                if discriminator_value == "container":
                    worklist_items_paginated_list = ContainerWorklistItemsList.from_dict(data, strict=False)

                    return worklist_items_paginated_list
                if discriminator_value == "plate":
                    worklist_items_paginated_list = PlateWorklistItemsList.from_dict(data, strict=False)

                    return worklist_items_paginated_list

                return UnknownType(value=data)
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_items_paginated_list = ContainerWorklistItemsList.from_dict(data, strict=True)

                return worklist_items_paginated_list
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_items_paginated_list = EntityWorklistItemsList.from_dict(data, strict=True)

                return worklist_items_paginated_list
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_items_paginated_list = PlateWorklistItemsList.from_dict(data, strict=True)

                return worklist_items_paginated_list
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                worklist_items_paginated_list = BatchWorklistItemsList.from_dict(data, strict=True)

                return worklist_items_paginated_list
            except:  # noqa: E722
                pass
            return UnknownType(data)

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[
    Union[
        Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ],
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
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        worklist_id=worklist_id,
        page_size=page_size,
        next_token=next_token,
        archive_reason=archive_reason,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    worklist_id: str,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    """List items in a worklist. Items are ordered by their position within the worklist."""

    return sync_detailed(
        client=client,
        worklist_id=worklist_id,
        page_size=page_size,
        next_token=next_token,
        archive_reason=archive_reason,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    worklist_id: str,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Response[
    Union[
        Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        worklist_id=worklist_id,
        page_size=page_size,
        next_token=next_token,
        archive_reason=archive_reason,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    worklist_id: str,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Optional[
    Union[
        Union[
            ContainerWorklistItemsList,
            EntityWorklistItemsList,
            PlateWorklistItemsList,
            BatchWorklistItemsList,
            UnknownType,
        ],
        BadRequestError,
    ]
]:
    """List items in a worklist. Items are ordered by their position within the worklist."""

    return (
        await asyncio_detailed(
            client=client,
            worklist_id=worklist_id,
            page_size=page_size,
            next_token=next_token,
            archive_reason=archive_reason,
        )
    ).parsed
