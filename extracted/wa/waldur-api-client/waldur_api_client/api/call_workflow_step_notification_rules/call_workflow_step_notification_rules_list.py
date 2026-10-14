from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_workflow_step_notification_rule import CallWorkflowStepNotificationRule
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_call_uuid: Union[Unset, str] = UNSET
    if not isinstance(call_uuid, Unset):
        json_call_uuid = str(call_uuid)
    params["call_uuid"] = json_call_uuid

    params["is_enabled"] = is_enabled

    params["page"] = page

    params["page_size"] = page_size

    params["step"] = step

    params["trigger"] = trigger

    json_workflow_step_uuid: Union[Unset, str] = UNSET
    if not isinstance(workflow_step_uuid, Unset):
        json_workflow_step_uuid = str(workflow_step_uuid)
    params["workflow_step_uuid"] = json_workflow_step_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/call-workflow-step-notification-rules/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["CallWorkflowStepNotificationRule"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CallWorkflowStepNotificationRule.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["CallWorkflowStepNotificationRule"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["CallWorkflowStepNotificationRule"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        is_enabled (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        step (Union[Unset, str]):
        trigger (Union[Unset, str]):
        workflow_step_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CallWorkflowStepNotificationRule']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        is_enabled=is_enabled,
        page=page,
        page_size=page_size,
        step=step,
        trigger=trigger,
        workflow_step_uuid=workflow_step_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> list["CallWorkflowStepNotificationRule"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        is_enabled (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        step (Union[Unset, str]):
        trigger (Union[Unset, str]):
        workflow_step_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CallWorkflowStepNotificationRule']
    """

    return sync_detailed(
        client=client,
        call_uuid=call_uuid,
        is_enabled=is_enabled,
        page=page,
        page_size=page_size,
        step=step,
        trigger=trigger,
        workflow_step_uuid=workflow_step_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> Response[list["CallWorkflowStepNotificationRule"]]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        is_enabled (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        step (Union[Unset, str]):
        trigger (Union[Unset, str]):
        workflow_step_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CallWorkflowStepNotificationRule']]
    """

    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        is_enabled=is_enabled,
        page=page,
        page_size=page_size,
        step=step,
        trigger=trigger,
        workflow_step_uuid=workflow_step_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> list["CallWorkflowStepNotificationRule"]:
    """
    Args:
        call_uuid (Union[Unset, UUID]):
        is_enabled (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        step (Union[Unset, str]):
        trigger (Union[Unset, str]):
        workflow_step_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CallWorkflowStepNotificationRule']
    """

    return (
        await asyncio_detailed(
            client=client,
            call_uuid=call_uuid,
            is_enabled=is_enabled,
            page=page,
            page_size=page_size,
            step=step,
            trigger=trigger,
            workflow_step_uuid=workflow_step_uuid,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> list["CallWorkflowStepNotificationRule"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        is_enabled (Union[Unset, bool]):
        step (Union[Unset, str]):
        trigger (Union[Unset, str]):
        workflow_step_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CallWorkflowStepNotificationRule']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[CallWorkflowStepNotificationRule] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        is_enabled=is_enabled,
        step=step,
        trigger=trigger,
        workflow_step_uuid=workflow_step_uuid,
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
    call_uuid: Union[Unset, UUID] = UNSET,
    is_enabled: Union[Unset, bool] = UNSET,
    step: Union[Unset, str] = UNSET,
    trigger: Union[Unset, str] = UNSET,
    workflow_step_uuid: Union[Unset, UUID] = UNSET,
) -> list["CallWorkflowStepNotificationRule"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        call_uuid (Union[Unset, UUID]):
        is_enabled (Union[Unset, bool]):
        step (Union[Unset, str]):
        trigger (Union[Unset, str]):
        workflow_step_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CallWorkflowStepNotificationRule']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[CallWorkflowStepNotificationRule] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        call_uuid=call_uuid,
        is_enabled=is_enabled,
        step=step,
        trigger=trigger,
        workflow_step_uuid=workflow_step_uuid,
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
