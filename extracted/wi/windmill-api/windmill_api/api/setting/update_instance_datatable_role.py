from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_instance_datatable_role_json_body import UpdateInstanceDatatableRoleJsonBody
from ...models.update_instance_datatable_role_response_200 import UpdateInstanceDatatableRoleResponse200
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    json_body: UpdateInstanceDatatableRoleJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/settings/datatable_roles/{id}".format(
            id=id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateInstanceDatatableRoleResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateInstanceDatatableRoleResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateInstanceDatatableRoleResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateInstanceDatatableRoleJsonBody,
) -> Response[UpdateInstanceDatatableRoleResponse200]:
    """rename a data table role or turn its login on and off

    Args:
        id (str):
        json_body (UpdateInstanceDatatableRoleJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateInstanceDatatableRoleResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateInstanceDatatableRoleJsonBody,
) -> Optional[UpdateInstanceDatatableRoleResponse200]:
    """rename a data table role or turn its login on and off

    Args:
        id (str):
        json_body (UpdateInstanceDatatableRoleJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateInstanceDatatableRoleResponse200
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateInstanceDatatableRoleJsonBody,
) -> Response[UpdateInstanceDatatableRoleResponse200]:
    """rename a data table role or turn its login on and off

    Args:
        id (str):
        json_body (UpdateInstanceDatatableRoleJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateInstanceDatatableRoleResponse200]
    """

    kwargs = _get_kwargs(
        id=id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateInstanceDatatableRoleJsonBody,
) -> Optional[UpdateInstanceDatatableRoleResponse200]:
    """rename a data table role or turn its login on and off

    Args:
        id (str):
        json_body (UpdateInstanceDatatableRoleJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateInstanceDatatableRoleResponse200
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
