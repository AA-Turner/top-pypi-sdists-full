from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_alert_action_input import EmailAlertActionInput
from ...models.email_alert_action_response import EmailAlertActionResponse
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.trigger_type import TriggerType
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    trigger: TriggerType,
    *,
    body: EmailAlertActionInput,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/alerts/{trigger}/actions".format(
            workspace_id=quote(str(workspace_id), safe=""),
            trigger=quote(str(trigger), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    EmailAlertActionResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    if response.status_code == 201:
        response_201 = EmailAlertActionResponse.from_dict(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    EmailAlertActionResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    trigger: TriggerType,
    *,
    client: AuthenticatedClient | Client,
    body: EmailAlertActionInput,
) -> Response[
    EmailAlertActionResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    """CreateAlertAction

    Args:
        workspace_id (UUID):
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-
            run-failure')
        body (EmailAlertActionInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailAlertActionResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        trigger=trigger,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    trigger: TriggerType,
    *,
    client: AuthenticatedClient | Client,
    body: EmailAlertActionInput,
) -> (
    EmailAlertActionResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    """CreateAlertAction

    Args:
        workspace_id (UUID):
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-
            run-failure')
        body (EmailAlertActionInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailAlertActionResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """
    return sync_detailed(
        workspace_id=workspace_id,
        trigger=trigger,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    trigger: TriggerType,
    *,
    client: AuthenticatedClient | Client,
    body: EmailAlertActionInput,
) -> Response[
    EmailAlertActionResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
]:
    """CreateAlertAction

    Args:
        workspace_id (UUID):
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-
            run-failure')
        body (EmailAlertActionInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EmailAlertActionResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        trigger=trigger,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    trigger: TriggerType,
    *,
    client: AuthenticatedClient | Client,
    body: EmailAlertActionInput,
) -> (
    EmailAlertActionResponse
    | ErrorResponse400
    | ErrorResponse401
    | ErrorResponse403
    | ErrorResponse404
    | None
):
    """CreateAlertAction

    Args:
        workspace_id (UUID):
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-
            run-failure')
        body (EmailAlertActionInput):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EmailAlertActionResponse | ErrorResponse400 | ErrorResponse401 | ErrorResponse403 | ErrorResponse404
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            trigger=trigger,
            client=client,
            body=body,
        )
    ).parsed
