from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.publish_round_results_refusal import PublishRoundResultsRefusal
from ...models.publish_round_results_request import PublishRoundResultsRequest
from ...models.publish_round_results_response import PublishRoundResultsResponse
from ...types import Response


def _get_kwargs(
    uuid: str,
    obj_uuid: str,
    *,
    body: PublishRoundResultsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/proposal-protected-calls/{uuid}/rounds/{obj_uuid}/publish_results/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PublishRoundResultsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PublishRoundResultsRefusal.from_dict(response.json())

        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]]:
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
    body: PublishRoundResultsRequest,
) -> Response[Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]]:
    """Publish all allocation decisions of an ended round at once: announce every held decision to its
    applicant and carry it out. Refused while a proposal of the round has no decision, unless forced
    with a reason; that refusal carries undecided_count. A decision that cannot be carried out stays
    held and is listed in failed_proposals; publishing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):
        body (PublishRoundResultsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
        body=body,
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
    body: PublishRoundResultsRequest,
) -> Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]:
    """Publish all allocation decisions of an ended round at once: announce every held decision to its
    applicant and carry it out. Refused while a proposal of the round has no decision, unless forced
    with a reason; that refusal carries undecided_count. A decision that cannot be carried out stays
    held and is listed in failed_proposals; publishing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):
        body (PublishRoundResultsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]
    """

    return sync_detailed(
        uuid=uuid,
        obj_uuid=obj_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
    body: PublishRoundResultsRequest,
) -> Response[Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]]:
    """Publish all allocation decisions of an ended round at once: announce every held decision to its
    applicant and carry it out. Refused while a proposal of the round has no decision, unless forced
    with a reason; that refusal carries undecided_count. A decision that cannot be carried out stays
    held and is listed in failed_proposals; publishing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):
        body (PublishRoundResultsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
    body: PublishRoundResultsRequest,
) -> Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]:
    """Publish all allocation decisions of an ended round at once: announce every held decision to its
    applicant and carry it out. Refused while a proposal of the round has no decision, unless forced
    with a reason; that refusal carries undecided_count. A decision that cannot be carried out stays
    held and is listed in failed_proposals; publishing again retries it.

    Args:
        uuid (str):
        obj_uuid (str):
        body (PublishRoundResultsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PublishRoundResultsRefusal, PublishRoundResultsResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            obj_uuid=obj_uuid,
            client=client,
            body=body,
        )
    ).parsed
