from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.rule_test_match_request_request import RuleTestMatchRequestRequest
from ...models.rule_test_match_response import RuleTestMatchResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: RuleTestMatchRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/autoprovisioning-rules/{uuid}/test-match/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> RuleTestMatchResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = RuleTestMatchResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RuleTestMatchResponse]:
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
    body: RuleTestMatchRequestRequest,
) -> Response[RuleTestMatchResponse]:
    """Dry-run rule evaluation against a target user.

     Evaluate this rule against the given user without provisioning. Returns per-filter outcomes, the
    customer-lookup verdict (when the rule uses use_user_organization_as_customer_name) and a top-line
    would_provision flag together with a human-readable block_reason.

    Args:
        uuid (UUID):
        body (RuleTestMatchRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleTestMatchResponse]
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
    body: RuleTestMatchRequestRequest,
) -> RuleTestMatchResponse:
    """Dry-run rule evaluation against a target user.

     Evaluate this rule against the given user without provisioning. Returns per-filter outcomes, the
    customer-lookup verdict (when the rule uses use_user_organization_as_customer_name) and a top-line
    would_provision flag together with a human-readable block_reason.

    Args:
        uuid (UUID):
        body (RuleTestMatchRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RuleTestMatchResponse
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
    body: RuleTestMatchRequestRequest,
) -> Response[RuleTestMatchResponse]:
    """Dry-run rule evaluation against a target user.

     Evaluate this rule against the given user without provisioning. Returns per-filter outcomes, the
    customer-lookup verdict (when the rule uses use_user_organization_as_customer_name) and a top-line
    would_provision flag together with a human-readable block_reason.

    Args:
        uuid (UUID):
        body (RuleTestMatchRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RuleTestMatchResponse]
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
    body: RuleTestMatchRequestRequest,
) -> RuleTestMatchResponse:
    """Dry-run rule evaluation against a target user.

     Evaluate this rule against the given user without provisioning. Returns per-filter outcomes, the
    customer-lookup verdict (when the rule uses use_user_organization_as_customer_name) and a top-line
    would_provision flag together with a human-readable block_reason.

    Args:
        uuid (UUID):
        body (RuleTestMatchRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RuleTestMatchResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
