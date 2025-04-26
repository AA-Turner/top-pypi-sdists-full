from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.list_studies_sort import ListStudiesSort
from ...models.studies_paginated_list import StudiesPaginatedList
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListStudiesSort] = ListStudiesSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/studies".format(client.base_url)

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
    if not isinstance(name, Unset) and name is not None:
        params["name"] = name
    if not isinstance(name_includes, Unset) and name_includes is not None:
        params["nameIncludes"] = name_includes
    if not isinstance(folder_id, Unset) and folder_id is not None:
        params["folderId"] = folder_id
    if not isinstance(project_id, Unset) and project_id is not None:
        params["projectId"] = project_id
    if not isinstance(schema_id, Unset) and schema_id is not None:
        params["schemaId"] = schema_id
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(namesany_of, Unset) and namesany_of is not None:
        params["names.anyOf"] = namesany_of
    if not isinstance(namesany_ofcase_sensitive, Unset) and namesany_ofcase_sensitive is not None:
        params["names.anyOf.caseSensitive"] = namesany_ofcase_sensitive
    if not isinstance(author_idsany_of, Unset) and author_idsany_of is not None:
        params["authorIds.anyOf"] = author_idsany_of

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[StudiesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = StudiesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[StudiesPaginatedList, BadRequestError]]:
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
    sort: Union[Unset, ListStudiesSort] = ListStudiesSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
) -> Response[Union[StudiesPaginatedList, BadRequestError]]:
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
        name=name,
        name_includes=name_includes,
        folder_id=folder_id,
        project_id=project_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        ids=ids,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        author_idsany_of=author_idsany_of,
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
    sort: Union[Unset, ListStudiesSort] = ListStudiesSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
) -> Optional[Union[StudiesPaginatedList, BadRequestError]]:
    """ List Studies """

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
        name=name,
        name_includes=name_includes,
        folder_id=folder_id,
        project_id=project_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        ids=ids,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        author_idsany_of=author_idsany_of,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListStudiesSort] = ListStudiesSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
) -> Response[Union[StudiesPaginatedList, BadRequestError]]:
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
        name=name,
        name_includes=name_includes,
        folder_id=folder_id,
        project_id=project_id,
        schema_id=schema_id,
        archive_reason=archive_reason,
        ids=ids,
        namesany_of=namesany_of,
        namesany_ofcase_sensitive=namesany_ofcase_sensitive,
        author_idsany_of=author_idsany_of,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    sort: Union[Unset, ListStudiesSort] = ListStudiesSort.MODIFIEDATDESC,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    name: Union[Unset, str] = UNSET,
    name_includes: Union[Unset, str] = UNSET,
    folder_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    schema_id: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    namesany_of: Union[Unset, str] = UNSET,
    namesany_ofcase_sensitive: Union[Unset, str] = UNSET,
    author_idsany_of: Union[Unset, str] = UNSET,
) -> Optional[Union[StudiesPaginatedList, BadRequestError]]:
    """ List Studies """

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
            name=name,
            name_includes=name_includes,
            folder_id=folder_id,
            project_id=project_id,
            schema_id=schema_id,
            archive_reason=archive_reason,
            ids=ids,
            namesany_of=namesany_of,
            namesany_ofcase_sensitive=namesany_ofcase_sensitive,
            author_idsany_of=author_idsany_of,
        )
    ).parsed
