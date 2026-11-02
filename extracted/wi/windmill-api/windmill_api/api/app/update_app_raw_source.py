from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_app_raw_source_json_body import UpdateAppRawSourceJsonBody
from ...models.update_app_raw_source_response_200 import UpdateAppRawSourceResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    json_body: UpdateAppRawSourceJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/apps/update_raw_source/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[UpdateAppRawSourceResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateAppRawSourceResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UpdateAppRawSourceResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateAppRawSourceJsonBody,
) -> Response[UpdateAppRawSourceResponse200]:
    """update a raw app from its sources, compiling them on a worker (which runs the app's own dependencies
    to do so)

    Args:
        workspace (str):
        path (str):
        json_body (UpdateAppRawSourceJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateAppRawSourceResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateAppRawSourceJsonBody,
) -> Optional[UpdateAppRawSourceResponse200]:
    """update a raw app from its sources, compiling them on a worker (which runs the app's own dependencies
    to do so)

    Args:
        workspace (str):
        path (str):
        json_body (UpdateAppRawSourceJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateAppRawSourceResponse200
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateAppRawSourceJsonBody,
) -> Response[UpdateAppRawSourceResponse200]:
    """update a raw app from its sources, compiling them on a worker (which runs the app's own dependencies
    to do so)

    Args:
        workspace (str):
        path (str):
        json_body (UpdateAppRawSourceJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpdateAppRawSourceResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateAppRawSourceJsonBody,
) -> Optional[UpdateAppRawSourceResponse200]:
    """update a raw app from its sources, compiling them on a worker (which runs the app's own dependencies
    to do so)

    Args:
        workspace (str):
        path (str):
        json_body (UpdateAppRawSourceJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpdateAppRawSourceResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
            json_body=json_body,
        )
    ).parsed
