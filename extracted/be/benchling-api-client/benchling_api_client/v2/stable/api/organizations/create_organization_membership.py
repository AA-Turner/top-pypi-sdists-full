from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.forbidden_error import ForbiddenError
from ...models.membership import Membership
from ...models.membership_create import MembershipCreate
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    organization_id: str,
    json_body: MembershipCreate,
) -> Dict[str, Any]:
    url = "{}/organizations/{organization_id}/memberships".format(
        client.base_url, organization_id=organization_id
    )

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Membership, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 201:
        response_201 = Membership.from_dict(response.json(), strict=False)

        return response_201
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json(), strict=False)

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json(), strict=False)

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Membership, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    organization_id: str,
    json_body: MembershipCreate,
) -> Response[Union[Membership, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        organization_id=organization_id,
        json_body=json_body,
    )

    response = client.httpx_client.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    organization_id: str,
    json_body: MembershipCreate,
) -> Optional[Union[Membership, BadRequestError, ForbiddenError, NotFoundError]]:
    """Create organization membership for the given user, role, and organization"""

    return sync_detailed(
        client=client,
        organization_id=organization_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    organization_id: str,
    json_body: MembershipCreate,
) -> Response[Union[Membership, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        organization_id=organization_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    organization_id: str,
    json_body: MembershipCreate,
) -> Optional[Union[Membership, BadRequestError, ForbiddenError, NotFoundError]]:
    """Create organization membership for the given user, role, and organization"""

    return (
        await asyncio_detailed(
            client=client,
            organization_id=organization_id,
            json_body=json_body,
        )
    ).parsed
