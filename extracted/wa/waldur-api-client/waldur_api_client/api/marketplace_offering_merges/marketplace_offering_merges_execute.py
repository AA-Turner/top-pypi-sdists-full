from http import HTTPStatus
from typing import Any, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_merge import OfferingMerge
from ...models.offering_merge_execute_request import OfferingMergeExecuteRequest
from ...models.offering_merge_refusal import OfferingMergeRefusal
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: OfferingMergeExecuteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-offering-merges/{uuid}/execute/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, OfferingMerge, OfferingMergeRefusal]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 202:
        response_202 = OfferingMerge.from_dict(response.json())

        return response_202
    if response.status_code == 400:
        response_400 = OfferingMergeRefusal.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, OfferingMerge, OfferingMergeRefusal]]:
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
    body: OfferingMergeExecuteRequest,
) -> Response[Union[Any, OfferingMerge, OfferingMergeRefusal]]:
    """Queue a previewed merge for execution.

    Refused with 400 if the stored preview has blockers or a warning code
    is missing from ``acknowledged_warnings``, and with 409 unless the
    merge is ``previewed``, which also refuses a second request.

    Args:
        uuid (UUID):
        body (OfferingMergeExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OfferingMerge, OfferingMergeRefusal]]
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
    body: OfferingMergeExecuteRequest,
) -> Union[Any, OfferingMerge, OfferingMergeRefusal]:
    """Queue a previewed merge for execution.

    Refused with 400 if the stored preview has blockers or a warning code
    is missing from ``acknowledged_warnings``, and with 409 unless the
    merge is ``previewed``, which also refuses a second request.

    Args:
        uuid (UUID):
        body (OfferingMergeExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OfferingMerge, OfferingMergeRefusal]
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
    body: OfferingMergeExecuteRequest,
) -> Response[Union[Any, OfferingMerge, OfferingMergeRefusal]]:
    """Queue a previewed merge for execution.

    Refused with 400 if the stored preview has blockers or a warning code
    is missing from ``acknowledged_warnings``, and with 409 unless the
    merge is ``previewed``, which also refuses a second request.

    Args:
        uuid (UUID):
        body (OfferingMergeExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, OfferingMerge, OfferingMergeRefusal]]
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
    body: OfferingMergeExecuteRequest,
) -> Union[Any, OfferingMerge, OfferingMergeRefusal]:
    """Queue a previewed merge for execution.

    Refused with 400 if the stored preview has blockers or a warning code
    is missing from ``acknowledged_warnings``, and with 409 unless the
    merge is ``previewed``, which also refuses a second request.

    Args:
        uuid (UUID):
        body (OfferingMergeExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, OfferingMerge, OfferingMergeRefusal]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
