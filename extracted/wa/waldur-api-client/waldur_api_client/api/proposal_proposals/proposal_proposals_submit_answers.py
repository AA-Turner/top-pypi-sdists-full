from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.answer_submit_request import AnswerSubmitRequest
from ...models.proposal_checklist_answer_submit_response import ProposalChecklistAnswerSubmitResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: list["AnswerSubmitRequest"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-proposals/{uuid}/submit_answers/",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, ProposalChecklistAnswerSubmitResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProposalChecklistAnswerSubmitResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = response.json()
        return response_400
    if response.status_code == 404:
        response_404 = response.json()
        return response_404
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ProposalChecklistAnswerSubmitResponse]]:
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
    body: list["AnswerSubmitRequest"],
) -> Response[Union[Any, ProposalChecklistAnswerSubmitResponse]]:
    """Submit checklist answers.

    Args:
        uuid (UUID):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProposalChecklistAnswerSubmitResponse]]
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
    body: list["AnswerSubmitRequest"],
) -> Union[Any, ProposalChecklistAnswerSubmitResponse]:
    """Submit checklist answers.

    Args:
        uuid (UUID):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProposalChecklistAnswerSubmitResponse]
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
    body: list["AnswerSubmitRequest"],
) -> Response[Union[Any, ProposalChecklistAnswerSubmitResponse]]:
    """Submit checklist answers.

    Args:
        uuid (UUID):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProposalChecklistAnswerSubmitResponse]]
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
    body: list["AnswerSubmitRequest"],
) -> Union[Any, ProposalChecklistAnswerSubmitResponse]:
    """Submit checklist answers.

    Args:
        uuid (UUID):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProposalChecklistAnswerSubmitResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
