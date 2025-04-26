from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.list_nucleotide_alignments_sort import ListNucleotideAlignmentsSort
from ...models.nucleotide_alignments_paginated_list import NucleotideAlignmentsPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListNucleotideAlignmentsSort] = ListNucleotideAlignmentsSort.MODIFIEDATDESC,
    created_at: Union[Unset, str] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    sequence_ids: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/nucleotide-alignments".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(created_at, Unset) and created_at is not None:
        params["createdAt"] = created_at
    if not isinstance(modified_at, Unset) and modified_at is not None:
        params["modifiedAt"] = modified_at
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(name_includes, Unset) and name_includes is not None:
        params["nameIncludes"] = name_includes
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(namesany_of, Unset) and namesany_of is not None:
        params["names.anyOf"] = namesany_of
    if not isinstance(namesany_ofcase_sensitive, Unset) and namesany_ofcase_sensitive is not None:
        params["names.anyOf.caseSensitive"] = namesany_ofcase_sensitive
    if not isinstance(sequence_ids, Unset) and sequence_ids is not None:
        params["sequenceIds"] = sequence_ids

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[NucleotideAlignmentsPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = NucleotideAlignmentsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[NucleotideAlignmentsPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, ListNucleotideAlignmentsSort] = ListNucleotideAlignmentsSort.MODIFIEDATDESC,
    created_at: Union[Unset, str] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    sequence_ids: Union[Unset, str] = UNSET,
) -> Response[Union[NucleotideAlignmentsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        created_at=created_at,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ids=ids,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        sequence_ids=sequence_ids,
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
    sort: Union[Unset, ListNucleotideAlignmentsSort] = ListNucleotideAlignmentsSort.MODIFIEDATDESC,
    created_at: Union[Unset, str] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    sequence_ids: Union[Unset, str] = UNSET,
) -> Optional[Union[NucleotideAlignmentsPaginatedList, BadRequestError]]:
    """ List Nucleotide Alignments """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        created_at=created_at,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ids=ids,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        sequence_ids=sequence_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListNucleotideAlignmentsSort] = ListNucleotideAlignmentsSort.MODIFIEDATDESC,
    created_at: Union[Unset, str] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    sequence_ids: Union[Unset, str] = UNSET,
) -> Response[Union[NucleotideAlignmentsPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        created_at=created_at,
        modified_at=modified_at,
        name=name,
        name_includes=name_includes,
        ids=ids,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        sequence_ids=sequence_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListNucleotideAlignmentsSort] = ListNucleotideAlignmentsSort.MODIFIEDATDESC,
    created_at: Union[Unset, str] = UNSET,
    modified_at: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    sequence_ids: Union[Unset, str] = UNSET,
) -> Optional[Union[NucleotideAlignmentsPaginatedList, BadRequestError]]:
    """ List Nucleotide Alignments """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            created_at=created_at,
            modified_at=modified_at,
            name=name,
            name_includes=name_includes,
            ids=ids,
            namesany_of=namesany_of,
            namesany_ofcase_sensitive=namesany_ofcase_sensitive,
            sequence_ids=sequence_ids,
        )
    ).parsed
