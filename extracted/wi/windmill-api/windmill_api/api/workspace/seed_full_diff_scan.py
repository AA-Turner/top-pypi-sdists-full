from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.seed_full_diff_scan_response_200 import SeedFullDiffScanResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    target_workspace_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/seed_full_diff/{target_workspace_id}".format(
            workspace=workspace,
            target_workspace_id=target_workspace_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SeedFullDiffScanResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SeedFullDiffScanResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SeedFullDiffScanResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SeedFullDiffScanResponse200]:
    """Seed the diff candidate set against an arbitrary workspace

     Enumerates every item of both workspaces as an undecided diff candidate so `compareWorkspaces` can
    compare a pair the fork lineage does not track. Requires being an admin of both workspaces, and is
    rejected for a pair already linked by the lineage (whose diff is tallied continuously). The
    comparison itself is what compares the candidates, and is the expensive step.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SeedFullDiffScanResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        target_workspace_id=target_workspace_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SeedFullDiffScanResponse200]:
    """Seed the diff candidate set against an arbitrary workspace

     Enumerates every item of both workspaces as an undecided diff candidate so `compareWorkspaces` can
    compare a pair the fork lineage does not track. Requires being an admin of both workspaces, and is
    rejected for a pair already linked by the lineage (whose diff is tallied continuously). The
    comparison itself is what compares the candidates, and is the expensive step.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SeedFullDiffScanResponse200
    """

    return sync_detailed(
        workspace=workspace,
        target_workspace_id=target_workspace_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[SeedFullDiffScanResponse200]:
    """Seed the diff candidate set against an arbitrary workspace

     Enumerates every item of both workspaces as an undecided diff candidate so `compareWorkspaces` can
    compare a pair the fork lineage does not track. Requires being an admin of both workspaces, and is
    rejected for a pair already linked by the lineage (whose diff is tallied continuously). The
    comparison itself is what compares the candidates, and is the expensive step.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SeedFullDiffScanResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        target_workspace_id=target_workspace_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    target_workspace_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[SeedFullDiffScanResponse200]:
    """Seed the diff candidate set against an arbitrary workspace

     Enumerates every item of both workspaces as an undecided diff candidate so `compareWorkspaces` can
    compare a pair the fork lineage does not track. Requires being an admin of both workspaces, and is
    rejected for a pair already linked by the lineage (whose diff is tallied continuously). The
    comparison itself is what compares the candidates, and is the expensive step.

    Args:
        workspace (str):
        target_workspace_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SeedFullDiffScanResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            target_workspace_id=target_workspace_id,
            client=client,
        )
    ).parsed
