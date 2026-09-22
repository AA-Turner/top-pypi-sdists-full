from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.plan_datatable_acl_json_body import PlanDatatableAclJsonBody
from ...models.plan_datatable_acl_response_200 import PlanDatatableAclResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    datatable_name: str,
    *,
    json_body: PlanDatatableAclJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/datatable_acl/{datatable_name}/plan".format(
            workspace=workspace,
            datatable_name=datatable_name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PlanDatatableAclResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PlanDatatableAclResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PlanDatatableAclResponse200]:
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
    json_body: PlanDatatableAclJsonBody,
) -> Response[PlanDatatableAclResponse200]:
    """preview the SQL an ownership or grant change would run (data table administrators only)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (PlanDatatableAclJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanDatatableAclResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        json_body=json_body,
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
    json_body: PlanDatatableAclJsonBody,
) -> Optional[PlanDatatableAclResponse200]:
    """preview the SQL an ownership or grant change would run (data table administrators only)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (PlanDatatableAclJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlanDatatableAclResponse200
    """

    return sync_detailed(
        workspace=workspace,
        datatable_name=datatable_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PlanDatatableAclJsonBody,
) -> Response[PlanDatatableAclResponse200]:
    """preview the SQL an ownership or grant change would run (data table administrators only)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (PlanDatatableAclJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PlanDatatableAclResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        datatable_name=datatable_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    datatable_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PlanDatatableAclJsonBody,
) -> Optional[PlanDatatableAclResponse200]:
    """preview the SQL an ownership or grant change would run (data table administrators only)

    Args:
        workspace (str):
        datatable_name (str):
        json_body (PlanDatatableAclJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PlanDatatableAclResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            datatable_name=datatable_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
