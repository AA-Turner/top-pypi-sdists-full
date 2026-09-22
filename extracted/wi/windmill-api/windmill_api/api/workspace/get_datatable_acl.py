from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_datatable_acl_kind import GetDatatableAclKind
from ...models.get_datatable_acl_response_200 import GetDatatableAclResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    datatable_name: str,
    *,
    kind: GetDatatableAclKind,
    schema: Union[Unset, None, str] = UNSET,
    table: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    json_kind = kind.value

    params["kind"] = json_kind

    params["schema"] = schema

    params["table"] = table

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/datatable_acl/{datatable_name}".format(
            workspace=workspace,
            datatable_name=datatable_name,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetDatatableAclResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetDatatableAclResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetDatatableAclResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: GetDatatableAclKind,
    schema: Union[Unset, None, str] = UNSET,
    table: Union[Unset, None, str] = UNSET,
) -> Response[GetDatatableAclResponse200]:
    """read the owner and grants of an instance data table's database, schema or table

    Args:
        workspace (str):
        datatable_name (str):
        kind (GetDatatableAclKind):
        schema (Union[Unset, None, str]):
        table (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDatatableAclResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        kind=kind,
        schema=schema,
        table=table,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: GetDatatableAclKind,
    schema: Union[Unset, None, str] = UNSET,
    table: Union[Unset, None, str] = UNSET,
) -> Optional[GetDatatableAclResponse200]:
    """read the owner and grants of an instance data table's database, schema or table

    Args:
        workspace (str):
        datatable_name (str):
        kind (GetDatatableAclKind):
        schema (Union[Unset, None, str]):
        table (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDatatableAclResponse200
    """

    return sync_detailed(
        workspace=workspace,
        datatable_name=datatable_name,
        client=client,
        kind=kind,
        schema=schema,
        table=table,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: GetDatatableAclKind,
    schema: Union[Unset, None, str] = UNSET,
    table: Union[Unset, None, str] = UNSET,
) -> Response[GetDatatableAclResponse200]:
    """read the owner and grants of an instance data table's database, schema or table

    Args:
        workspace (str):
        datatable_name (str):
        kind (GetDatatableAclKind):
        schema (Union[Unset, None, str]):
        table (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetDatatableAclResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        kind=kind,
        schema=schema,
        table=table,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: GetDatatableAclKind,
    schema: Union[Unset, None, str] = UNSET,
    table: Union[Unset, None, str] = UNSET,
) -> Optional[GetDatatableAclResponse200]:
    """read the owner and grants of an instance data table's database, schema or table

    Args:
        workspace (str):
        datatable_name (str):
        kind (GetDatatableAclKind):
        schema (Union[Unset, None, str]):
        table (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetDatatableAclResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            datatable_name=datatable_name,
            client=client,
            kind=kind,
            schema=schema,
            table=table,
        )
    ).parsed
