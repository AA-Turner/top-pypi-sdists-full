from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assay_results_paginated_list import AssayResultsPaginatedList
from ...models.list_assay_results_sort import ListAssayResultsSort
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    schema_id: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    sort: Union[Unset, ListAssayResultsSort] = ListAssayResultsSort.CREATEDATASC,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    storage_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    automation_output_processor_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/assay-results".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_sort: Union[Unset, int] = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params: Dict[str, Any] = {}
    if not isinstance(schema_id, Unset) and schema_id is not None:
        params["schemaId"] = schema_id
    if not isinstance(created_atlt, Unset) and created_atlt is not None:
        params["createdAt.lt"] = created_atlt
    if not isinstance(created_atgt, Unset) and created_atgt is not None:
        params["createdAt.gt"] = created_atgt
    if not isinstance(created_atlte, Unset) and created_atlte is not None:
        params["createdAt.lte"] = created_atlte
    if not isinstance(created_atgte, Unset) and created_atgte is not None:
        params["createdAt.gte"] = created_atgte
    if not isinstance(min_created_time, Unset) and min_created_time is not None:
        params["minCreatedTime"] = min_created_time
    if not isinstance(max_created_time, Unset) and max_created_time is not None:
        params["maxCreatedTime"] = max_created_time
    if not isinstance(json_sort, Unset) and json_sort is not None:
        params["sort"] = json_sort
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(entity_ids, Unset) and entity_ids is not None:
        params["entityIds"] = entity_ids
    if not isinstance(storage_ids, Unset) and storage_ids is not None:
        params["storageIds"] = storage_ids
    if not isinstance(assay_run_ids, Unset) and assay_run_ids is not None:
        params["assayRunIds"] = assay_run_ids
    if not isinstance(automation_output_processor_id, Unset) and automation_output_processor_id is not None:
        params["automationOutputProcessorId"] = automation_output_processor_id
    if not isinstance(ids, Unset) and ids is not None:
        params["ids"] = ids
    if not isinstance(modified_atlt, Unset) and modified_atlt is not None:
        params["modifiedAt.lt"] = modified_atlt
    if not isinstance(modified_atgt, Unset) and modified_atgt is not None:
        params["modifiedAt.gt"] = modified_atgt
    if not isinstance(modified_atlte, Unset) and modified_atlte is not None:
        params["modifiedAt.lte"] = modified_atlte
    if not isinstance(modified_atgte, Unset) and modified_atgte is not None:
        params["modifiedAt.gte"] = modified_atgte
    if not isinstance(archive_reason, Unset) and archive_reason is not None:
        params["archiveReason"] = archive_reason

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayResultsPaginatedList]:
    if response.status_code == 200:
        response_200 = AssayResultsPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayResultsPaginatedList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    schema_id: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    sort: Union[Unset, ListAssayResultsSort] = ListAssayResultsSort.CREATEDATASC,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    storage_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    automation_output_processor_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Response[AssayResultsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        sort=sort,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        storage_ids=storage_ids,
        assay_run_ids=assay_run_ids,
        automation_output_processor_id=automation_output_processor_id,
        ids=ids,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        archive_reason=archive_reason,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    schema_id: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    sort: Union[Unset, ListAssayResultsSort] = ListAssayResultsSort.CREATEDATASC,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    storage_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    automation_output_processor_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Optional[AssayResultsPaginatedList]:
    """ List results """

    return sync_detailed(
        client=client,
        schema_id=schema_id,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        sort=sort,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        storage_ids=storage_ids,
        assay_run_ids=assay_run_ids,
        automation_output_processor_id=automation_output_processor_id,
        ids=ids,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        archive_reason=archive_reason,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    schema_id: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    sort: Union[Unset, ListAssayResultsSort] = ListAssayResultsSort.CREATEDATASC,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    storage_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    automation_output_processor_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Response[AssayResultsPaginatedList]:
    kwargs = _get_kwargs(
        client=client,
        schema_id=schema_id,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        min_created_time=min_created_time,
        max_created_time=max_created_time,
        sort=sort,
        next_token=next_token,
        page_size=page_size,
        entity_ids=entity_ids,
        storage_ids=storage_ids,
        assay_run_ids=assay_run_ids,
        automation_output_processor_id=automation_output_processor_id,
        ids=ids,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        archive_reason=archive_reason,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    schema_id: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    min_created_time: Union[Unset, int] = UNSET,
    max_created_time: Union[Unset, int] = UNSET,
    sort: Union[Unset, ListAssayResultsSort] = ListAssayResultsSort.CREATEDATASC,
    next_token: Union[Unset, str] = UNSET,
    page_size: Union[Unset, int] = 50,
    entity_ids: Union[Unset, str] = UNSET,
    storage_ids: Union[Unset, str] = UNSET,
    assay_run_ids: Union[Unset, str] = UNSET,
    automation_output_processor_id: Union[Unset, str] = UNSET,
    ids: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    archive_reason: Union[Unset, str] = UNSET,
) -> Optional[AssayResultsPaginatedList]:
    """ List results """

    return (
        await asyncio_detailed(
            client=client,
            schema_id=schema_id,
            created_atlt=created_atlt,
            created_atgt=created_atgt,
            created_atlte=created_atlte,
            created_atgte=created_atgte,
            min_created_time=min_created_time,
            max_created_time=max_created_time,
            sort=sort,
            next_token=next_token,
            page_size=page_size,
            entity_ids=entity_ids,
            storage_ids=storage_ids,
            assay_run_ids=assay_run_ids,
            automation_output_processor_id=automation_output_processor_id,
            ids=ids,
            modified_atlt=modified_atlt,
            modified_atgt=modified_atgt,
            modified_atlte=modified_atlte,
            modified_atgte=modified_atgte,
            archive_reason=archive_reason,
        )
    ).parsed
