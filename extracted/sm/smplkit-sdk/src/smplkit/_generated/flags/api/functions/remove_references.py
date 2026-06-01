from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.remove_references_request import RemoveReferencesRequest
from ...models.remove_references_result_envelope import RemoveReferencesResultEnvelope


def _get_kwargs(
    *,
    body: RemoveReferencesRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/functions/remove_references/actions/execute",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> RemoveReferencesResultEnvelope | None:
    if response.status_code == 200:
        response_200 = RemoveReferencesResultEnvelope.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[RemoveReferencesResultEnvelope]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RemoveReferencesRequest,
) -> Response[RemoveReferencesResultEnvelope]:
    """Execute Remove References

     Remove every rule that references a specific context across every flag.

    Provide exactly one of `context` (matches a single instance,
    formatted as `{type}:{key}`) or `context_type` (matches any
    attribute of that context type). Rules whose reference sits inside
    an AND expression are not removed automatically; they are returned
    in `rules_needing_manual_review` for the caller to handle.

    Args:
        body (RemoveReferencesRequest): Inputs to the remove-references action.

            Exactly one of `context` or `context_type` must be provided.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoveReferencesResultEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: RemoveReferencesRequest,
) -> RemoveReferencesResultEnvelope | None:
    """Execute Remove References

     Remove every rule that references a specific context across every flag.

    Provide exactly one of `context` (matches a single instance,
    formatted as `{type}:{key}`) or `context_type` (matches any
    attribute of that context type). Rules whose reference sits inside
    an AND expression are not removed automatically; they are returned
    in `rules_needing_manual_review` for the caller to handle.

    Args:
        body (RemoveReferencesRequest): Inputs to the remove-references action.

            Exactly one of `context` or `context_type` must be provided.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoveReferencesResultEnvelope
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RemoveReferencesRequest,
) -> Response[RemoveReferencesResultEnvelope]:
    """Execute Remove References

     Remove every rule that references a specific context across every flag.

    Provide exactly one of `context` (matches a single instance,
    formatted as `{type}:{key}`) or `context_type` (matches any
    attribute of that context type). Rules whose reference sits inside
    an AND expression are not removed automatically; they are returned
    in `rules_needing_manual_review` for the caller to handle.

    Args:
        body (RemoveReferencesRequest): Inputs to the remove-references action.

            Exactly one of `context` or `context_type` must be provided.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoveReferencesResultEnvelope]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RemoveReferencesRequest,
) -> RemoveReferencesResultEnvelope | None:
    """Execute Remove References

     Remove every rule that references a specific context across every flag.

    Provide exactly one of `context` (matches a single instance,
    formatted as `{type}:{key}`) or `context_type` (matches any
    attribute of that context type). Rules whose reference sits inside
    an AND expression are not removed automatically; they are returned
    in `rules_needing_manual_review` for the caller to handle.

    Args:
        body (RemoveReferencesRequest): Inputs to the remove-references action.

            Exactly one of `context` or `context_type` must be provided.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoveReferencesResultEnvelope
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
