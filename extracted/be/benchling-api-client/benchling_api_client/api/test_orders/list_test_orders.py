from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.list_test_orders_sort import ListTestOrdersSort
from ...models.test_order_status import TestOrderStatus
from ...models.test_orders_paginated_list import TestOrdersPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListTestOrdersSort] = ListTestOrdersSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    container_idsany_of: Union[Unset, str] = UNSET,
    sample_idsany_of: Union[Unset, str] = UNSET,
    status: Union[Unset, TestOrderStatus] = UNSET,
) -> Dict[str, Any]:
    url = "{}/test-orders".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(created_atlt, Unset) and created_atlt is not None:
        params["createdAt.lt"] = created_atlt
    if not isinstance(created_atgt, Unset) and created_atgt is not None:
        params["createdAt.gt"] = created_atgt
    if not isinstance(created_atlte, Unset) and created_atlte is not None:
        params["createdAt.lte"] = created_atlte
    if not isinstance(created_atgte, Unset) and created_atgte is not None:
        params["createdAt.gte"] = created_atgte
    if not isinstance(modified_atlt, Unset) and modified_atlt is not None:
        params["modifiedAt.lt"] = modified_atlt
    if not isinstance(modified_atgt, Unset) and modified_atgt is not None:
        params["modifiedAt.gt"] = modified_atgt
    if not isinstance(modified_atlte, Unset) and modified_atlte is not None:
        params["modifiedAt.lte"] = modified_atlte
    if not isinstance(modified_atgte, Unset) and modified_atgte is not None:
        params["modifiedAt.gte"] = modified_atgte
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(container_idsany_of, Unset) and container_idsany_of is not None:
        params["containerIds.anyOf"] = container_idsany_of
    if not isinstance(sample_idsany_of, Unset) and sample_idsany_of is not None:
        params["sampleIds.anyOf"] = sample_idsany_of
    if not isinstance(json_status, Unset) and json_status is not None:
        params["status"] = json_status

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[TestOrdersPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = TestOrdersPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[TestOrdersPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListTestOrdersSort] = ListTestOrdersSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    container_idsany_of: Union[Unset, str] = UNSET,
    sample_idsany_of: Union[Unset, str] = UNSET,
    status: Union[Unset, TestOrderStatus] = UNSET,
) -> Response[Union[TestOrdersPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        ids=ids,
        container_idsany_of=container_idsany_of,
        sample_idsany_of=sample_idsany_of,
        status=status,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListTestOrdersSort] = ListTestOrdersSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    container_idsany_of: Union[Unset, str] = UNSET,
    sample_idsany_of: Union[Unset, str] = UNSET,
    status: Union[Unset, TestOrderStatus] = UNSET,
) -> Optional[Union[TestOrdersPaginatedList, BadRequestError]]:
    """ List test orders """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        ids=ids,
        container_idsany_of=container_idsany_of,
        sample_idsany_of=sample_idsany_of,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListTestOrdersSort] = ListTestOrdersSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    container_idsany_of: Union[Unset, str] = UNSET,
    sample_idsany_of: Union[Unset, str] = UNSET,
    status: Union[Unset, TestOrderStatus] = UNSET,
) -> Response[Union[TestOrdersPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        ids=ids,
        container_idsany_of=container_idsany_of,
        sample_idsany_of=sample_idsany_of,
        status=status,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListTestOrdersSort] = ListTestOrdersSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    container_idsany_of: Union[Unset, str] = UNSET,
    sample_idsany_of: Union[Unset, str] = UNSET,
    status: Union[Unset, TestOrderStatus] = UNSET,
) -> Optional[Union[TestOrdersPaginatedList, BadRequestError]]:
    """ List test orders """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            created_atlt=created_atlt,
            created_atgt=created_atgt,
            created_atlte=created_atlte,
            created_atgte=created_atgte,
            modified_atlt=modified_atlt,
            modified_atgt=modified_atgt,
            modified_atlte=modified_atlte,
            modified_atgte=modified_atgte,
            ids=ids,
            container_idsany_of=container_idsany_of,
            sample_idsany_of=sample_idsany_of,
            status=status,
        )
    ).parsed
