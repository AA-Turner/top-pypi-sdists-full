from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_email_policy_response import ProjectEmailPolicyResponse
from ...types import Response


def _get_kwargs(
    project_uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/openportal/project_email_policy/{project_uuid}/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ProjectEmailPolicyResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProjectEmailPolicyResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProjectEmailPolicyResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[ProjectEmailPolicyResponse]:
    """Return the allowed_domains list for a project derived from its AwardDetails. null means no
    restriction; [] means nothing allowed; a list contains permitted domain globs and/or specific email
    addresses.

    Args:
        project_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectEmailPolicyResponse]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_uuid: str,
    *,
    client: AuthenticatedClient,
) -> ProjectEmailPolicyResponse:
    """Return the allowed_domains list for a project derived from its AwardDetails. null means no
    restriction; [] means nothing allowed; a list contains permitted domain globs and/or specific email
    addresses.

    Args:
        project_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectEmailPolicyResponse
    """

    return sync_detailed(
        project_uuid=project_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    project_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[ProjectEmailPolicyResponse]:
    """Return the allowed_domains list for a project derived from its AwardDetails. null means no
    restriction; [] means nothing allowed; a list contains permitted domain globs and/or specific email
    addresses.

    Args:
        project_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectEmailPolicyResponse]
    """

    kwargs = _get_kwargs(
        project_uuid=project_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_uuid: str,
    *,
    client: AuthenticatedClient,
) -> ProjectEmailPolicyResponse:
    """Return the allowed_domains list for a project derived from its AwardDetails. null means no
    restriction; [] means nothing allowed; a list contains permitted domain globs and/or specific email
    addresses.

    Args:
        project_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectEmailPolicyResponse
    """

    return (
        await asyncio_detailed(
            project_uuid=project_uuid,
            client=client,
        )
    ).parsed
