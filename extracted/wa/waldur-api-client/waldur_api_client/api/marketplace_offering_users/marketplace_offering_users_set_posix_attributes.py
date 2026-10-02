from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_user_posix_attributes_request import OfferingUserPosixAttributesRequest
from ...models.offering_user_posix_update_response import OfferingUserPosixUpdateResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: OfferingUserPosixAttributesRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-offering-users/{uuid}/set_posix_attributes/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> OfferingUserPosixUpdateResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OfferingUserPosixUpdateResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OfferingUserPosixUpdateResponse]:
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
    body: OfferingUserPosixAttributesRequest,
) -> Response[OfferingUserPosixUpdateResponse]:
    """Set POSIX attributes for an offering user

     Override the login shell, home directory, UID and/or primary GID for a single offering user, taking
    precedence over the offering-level defaults / the range allocator. This is the programmatic
    equivalent of the 'Edit POSIX attributes' dialog. The accepted fields are 'login_shell',
    'home_directory', 'uidnumber' and 'primarygroup'; all are optional, but at least one must be
    provided.

    A UID or primary GID re-points the allocation ledger and must fall within the POSIX ID pool resolved
    for the offering: a value outside that pool's range is rejected with 400, as is a value already held
    by another active identity (another account, a robot account or a group) and any override on an
    offering for which no pool resolves. The action is all-or-nothing - a conflict on the second
    identifier rolls back the change made for the first.

    The response 'warnings' list carries only non-fatal advisories about values that were accepted: the
    reserved POSIX ids 65534 and 65535, and values of 2^31 or above, which may break software using
    signed 32-bit ids.

    Args:
        uuid (UUID):
        body (OfferingUserPosixAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingUserPosixUpdateResponse]
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
    body: OfferingUserPosixAttributesRequest,
) -> OfferingUserPosixUpdateResponse:
    """Set POSIX attributes for an offering user

     Override the login shell, home directory, UID and/or primary GID for a single offering user, taking
    precedence over the offering-level defaults / the range allocator. This is the programmatic
    equivalent of the 'Edit POSIX attributes' dialog. The accepted fields are 'login_shell',
    'home_directory', 'uidnumber' and 'primarygroup'; all are optional, but at least one must be
    provided.

    A UID or primary GID re-points the allocation ledger and must fall within the POSIX ID pool resolved
    for the offering: a value outside that pool's range is rejected with 400, as is a value already held
    by another active identity (another account, a robot account or a group) and any override on an
    offering for which no pool resolves. The action is all-or-nothing - a conflict on the second
    identifier rolls back the change made for the first.

    The response 'warnings' list carries only non-fatal advisories about values that were accepted: the
    reserved POSIX ids 65534 and 65535, and values of 2^31 or above, which may break software using
    signed 32-bit ids.

    Args:
        uuid (UUID):
        body (OfferingUserPosixAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingUserPosixUpdateResponse
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
    body: OfferingUserPosixAttributesRequest,
) -> Response[OfferingUserPosixUpdateResponse]:
    """Set POSIX attributes for an offering user

     Override the login shell, home directory, UID and/or primary GID for a single offering user, taking
    precedence over the offering-level defaults / the range allocator. This is the programmatic
    equivalent of the 'Edit POSIX attributes' dialog. The accepted fields are 'login_shell',
    'home_directory', 'uidnumber' and 'primarygroup'; all are optional, but at least one must be
    provided.

    A UID or primary GID re-points the allocation ledger and must fall within the POSIX ID pool resolved
    for the offering: a value outside that pool's range is rejected with 400, as is a value already held
    by another active identity (another account, a robot account or a group) and any override on an
    offering for which no pool resolves. The action is all-or-nothing - a conflict on the second
    identifier rolls back the change made for the first.

    The response 'warnings' list carries only non-fatal advisories about values that were accepted: the
    reserved POSIX ids 65534 and 65535, and values of 2^31 or above, which may break software using
    signed 32-bit ids.

    Args:
        uuid (UUID):
        body (OfferingUserPosixAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingUserPosixUpdateResponse]
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
    body: OfferingUserPosixAttributesRequest,
) -> OfferingUserPosixUpdateResponse:
    """Set POSIX attributes for an offering user

     Override the login shell, home directory, UID and/or primary GID for a single offering user, taking
    precedence over the offering-level defaults / the range allocator. This is the programmatic
    equivalent of the 'Edit POSIX attributes' dialog. The accepted fields are 'login_shell',
    'home_directory', 'uidnumber' and 'primarygroup'; all are optional, but at least one must be
    provided.

    A UID or primary GID re-points the allocation ledger and must fall within the POSIX ID pool resolved
    for the offering: a value outside that pool's range is rejected with 400, as is a value already held
    by another active identity (another account, a robot account or a group) and any override on an
    offering for which no pool resolves. The action is all-or-nothing - a conflict on the second
    identifier rolls back the change made for the first.

    The response 'warnings' list carries only non-fatal advisories about values that were accepted: the
    reserved POSIX ids 65534 and 65535, and values of 2^31 or above, which may break software using
    signed 32-bit ids.

    Args:
        uuid (UUID):
        body (OfferingUserPosixAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingUserPosixUpdateResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
