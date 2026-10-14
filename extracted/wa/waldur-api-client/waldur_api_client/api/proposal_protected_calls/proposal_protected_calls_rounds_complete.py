from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.complete_round_refusal import CompleteRoundRefusal
from ...models.complete_round_response import CompleteRoundResponse
from ...types import Response


def _get_kwargs(
    uuid: str,
    obj_uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/rounds/{obj_uuid}/complete/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[CompleteRoundRefusal, CompleteRoundResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CompleteRoundResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = CompleteRoundRefusal.from_dict(response.json())

        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CompleteRoundRefusal, CompleteRoundResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[CompleteRoundRefusal, CompleteRoundResponse]]:
    """Close a round whose results have been published. Refused while a decision of the round is still held
    because its release failed (the refusal carries held_decisions_count; publish the results again to
    retry it). Every proposal of the round must have a decision. What happens to those that have none
    follows the round's undecided_at_round_completion, or else the call's: refuse (the refusal carries
    undecided_count) or reject each at its current step, listed in rejected_proposals. A rejection that
    fails is listed in failed_proposals and the round stays open; completing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CompleteRoundRefusal, CompleteRoundResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Union[CompleteRoundRefusal, CompleteRoundResponse]:
    """Close a round whose results have been published. Refused while a decision of the round is still held
    because its release failed (the refusal carries held_decisions_count; publish the results again to
    retry it). Every proposal of the round must have a decision. What happens to those that have none
    follows the round's undecided_at_round_completion, or else the call's: refuse (the refusal carries
    undecided_count) or reject each at its current step, listed in rejected_proposals. A rejection that
    fails is listed in failed_proposals and the round stays open; completing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CompleteRoundRefusal, CompleteRoundResponse]
    """

    return sync_detailed(
        uuid=uuid,
        obj_uuid=obj_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[CompleteRoundRefusal, CompleteRoundResponse]]:
    """Close a round whose results have been published. Refused while a decision of the round is still held
    because its release failed (the refusal carries held_decisions_count; publish the results again to
    retry it). Every proposal of the round must have a decision. What happens to those that have none
    follows the round's undecided_at_round_completion, or else the call's: refuse (the refusal carries
    undecided_count) or reject each at its current step, listed in rejected_proposals. A rejection that
    fails is listed in failed_proposals and the round stays open; completing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CompleteRoundRefusal, CompleteRoundResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Union[CompleteRoundRefusal, CompleteRoundResponse]:
    """Close a round whose results have been published. Refused while a decision of the round is still held
    because its release failed (the refusal carries held_decisions_count; publish the results again to
    retry it). Every proposal of the round must have a decision. What happens to those that have none
    follows the round's undecided_at_round_completion, or else the call's: refuse (the refusal carries
    undecided_count) or reject each at its current step, listed in rejected_proposals. A rejection that
    fails is listed in failed_proposals and the round stays open; completing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CompleteRoundRefusal, CompleteRoundResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            obj_uuid=obj_uuid,
            client=client,
        )
    ).parsed
