import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feedback import Feedback
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_after: Union[Unset, str] = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["created_after"] = json_created_after

    json_created_before: Union[Unset, str] = UNSET
    if not isinstance(created_before, Unset):
        json_created_before = created_before.isoformat()
    params["created_before"] = json_created_before

    params["evaluation"] = evaluation

    params["issue"] = issue

    params["issue_key"] = issue_key

    json_issue_uuid: Union[Unset, str] = UNSET
    if not isinstance(issue_uuid, Unset):
        json_issue_uuid = str(issue_uuid)
    params["issue_uuid"] = json_issue_uuid

    params["page"] = page

    params["page_size"] = page_size

    params["user"] = user

    params["user_full_name"] = user_full_name

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/support-feedbacks/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["Feedback"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Feedback.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["Feedback"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["Feedback"]]:
    """
    Args:
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        evaluation (Union[Unset, int]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Feedback']]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        evaluation=evaluation,
        issue=issue,
        issue_key=issue_key,
        issue_uuid=issue_uuid,
        page=page,
        page_size=page_size,
        user=user,
        user_full_name=user_full_name,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["Feedback"]:
    """
    Args:
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        evaluation (Union[Unset, int]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Feedback']
    """

    return sync_detailed(
        client=client,
        created_after=created_after,
        created_before=created_before,
        evaluation=evaluation,
        issue=issue,
        issue_key=issue_key,
        issue_uuid=issue_uuid,
        page=page,
        page_size=page_size,
        user=user,
        user_full_name=user_full_name,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["Feedback"]]:
    """
    Args:
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        evaluation (Union[Unset, int]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['Feedback']]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        evaluation=evaluation,
        issue=issue,
        issue_key=issue_key,
        issue_uuid=issue_uuid,
        page=page,
        page_size=page_size,
        user=user,
        user_full_name=user_full_name,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["Feedback"]:
    """
    Args:
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        evaluation (Union[Unset, int]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Feedback']
    """

    return (
        await asyncio_detailed(
            client=client,
            created_after=created_after,
            created_before=created_before,
            evaluation=evaluation,
            issue=issue,
            issue_key=issue_key,
            issue_uuid=issue_uuid,
            page=page,
            page_size=page_size,
            user=user,
            user_full_name=user_full_name,
            user_uuid=user_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["Feedback"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        evaluation (Union[Unset, int]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Feedback']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Feedback] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        evaluation=evaluation,
        issue=issue,
        issue_key=issue_key,
        issue_uuid=issue_uuid,
        user=user,
        user_full_name=user_full_name,
        user_uuid=user_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    created_after: Union[Unset, datetime.datetime] = UNSET,
    created_before: Union[Unset, datetime.datetime] = UNSET,
    evaluation: Union[Unset, int] = UNSET,
    issue: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_uuid: Union[Unset, UUID] = UNSET,
    user: Union[Unset, str] = UNSET,
    user_full_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> list["Feedback"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_after (Union[Unset, datetime.datetime]):
        created_before (Union[Unset, datetime.datetime]):
        evaluation (Union[Unset, int]):
        issue (Union[Unset, str]):
        issue_key (Union[Unset, str]):
        issue_uuid (Union[Unset, UUID]):
        user (Union[Unset, str]):
        user_full_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['Feedback']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[Feedback] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_after=created_after,
        created_before=created_before,
        evaluation=evaluation,
        issue=issue,
        issue_key=issue_key,
        issue_uuid=issue_uuid,
        user=user,
        user_full_name=user_full_name,
        user_uuid=user_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
