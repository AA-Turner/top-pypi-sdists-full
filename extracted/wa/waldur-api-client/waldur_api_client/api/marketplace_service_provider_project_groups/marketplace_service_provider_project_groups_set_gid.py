from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_group_gid_request import ProjectGroupGidRequest
from ...models.service_provider_project_group import ServiceProviderProjectGroup
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ProjectGroupGidRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-service-provider-project-groups/{uuid}/set_gid/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ServiceProviderProjectGroup:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ServiceProviderProjectGroup.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ServiceProviderProjectGroup]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectGroupGidRequest,
) -> Response[ServiceProviderProjectGroup]:
    """Set the GID of a POSIX project group

     Move the group to another GID, e.g. one assigned outside Waldur. The previous GID is released but
    never handed out again automatically, since files may still carry it; renumbering them is the
    operator's job. Refused with 400 on the same conditions as adopting a group. Recorded as an event
    with both GIDs.

    Args:
        uuid (UUID):
        body (ProjectGroupGidRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProviderProjectGroup]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectGroupGidRequest,
) -> ServiceProviderProjectGroup:
    """Set the GID of a POSIX project group

     Move the group to another GID, e.g. one assigned outside Waldur. The previous GID is released but
    never handed out again automatically, since files may still carry it; renumbering them is the
    operator's job. Refused with 400 on the same conditions as adopting a group. Recorded as an event
    with both GIDs.

    Args:
        uuid (UUID):
        body (ProjectGroupGidRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProviderProjectGroup
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectGroupGidRequest,
) -> Response[ServiceProviderProjectGroup]:
    """Set the GID of a POSIX project group

     Move the group to another GID, e.g. one assigned outside Waldur. The previous GID is released but
    never handed out again automatically, since files may still carry it; renumbering them is the
    operator's job. Refused with 400 on the same conditions as adopting a group. Recorded as an event
    with both GIDs.

    Args:
        uuid (UUID):
        body (ProjectGroupGidRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ServiceProviderProjectGroup]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectGroupGidRequest,
) -> ServiceProviderProjectGroup:
    """Set the GID of a POSIX project group

     Move the group to another GID, e.g. one assigned outside Waldur. The previous GID is released but
    never handed out again automatically, since files may still carry it; renumbering them is the
    operator's job. Refused with 400 on the same conditions as adopting a group. Recorded as an event
    with both GIDs.

    Args:
        uuid (UUID):
        body (ProjectGroupGidRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ServiceProviderProjectGroup
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
