from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_run_assets_response_200 import ListRunAssetsResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs/run_assets/{id}".format(
            workspace=workspace,
            id=id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListRunAssetsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListRunAssetsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListRunAssetsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListRunAssetsResponse200]:
    """List the assets a run touched at runtime

     Assets detected while the run executed (SDK S3 calls, resources passed as arguments), aggregated
    over the job and all of its child jobs so a flow or workflow-as-code run reports what its steps and
    tasks touched. Authorized through the job, the same gate as `run_progress`. Recording is
    asynchronous, so an asset can take a few minutes after the run to appear, and only the most recent
    runs that touched an asset keep that record. A run that fans out can touch more assets than one
    response should carry, so the list is capped and `truncated` says when it was cut.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListRunAssetsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListRunAssetsResponse200]:
    """List the assets a run touched at runtime

     Assets detected while the run executed (SDK S3 calls, resources passed as arguments), aggregated
    over the job and all of its child jobs so a flow or workflow-as-code run reports what its steps and
    tasks touched. Authorized through the job, the same gate as `run_progress`. Recording is
    asynchronous, so an asset can take a few minutes after the run to appear, and only the most recent
    runs that touched an asset keep that record. A run that fans out can touch more assets than one
    response should carry, so the list is capped and `truncated` says when it was cut.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListRunAssetsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ListRunAssetsResponse200]:
    """List the assets a run touched at runtime

     Assets detected while the run executed (SDK S3 calls, resources passed as arguments), aggregated
    over the job and all of its child jobs so a flow or workflow-as-code run reports what its steps and
    tasks touched. Authorized through the job, the same gate as `run_progress`. Recording is
    asynchronous, so an asset can take a few minutes after the run to appear, and only the most recent
    runs that touched an asset keep that record. A run that fans out can touch more assets than one
    response should carry, so the list is capped and `truncated` says when it was cut.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListRunAssetsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ListRunAssetsResponse200]:
    """List the assets a run touched at runtime

     Assets detected while the run executed (SDK S3 calls, resources passed as arguments), aggregated
    over the job and all of its child jobs so a flow or workflow-as-code run reports what its steps and
    tasks touched. Authorized through the job, the same gate as `run_progress`. Recording is
    asynchronous, so an asset can take a few minutes after the run to appear, and only the most recent
    runs that touched an asset keep that record. A run that fans out can touch more assets than one
    response should carry, so the list is capped and `truncated` says when it was cut.

    Args:
        workspace (str):
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListRunAssetsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
        )
    ).parsed
