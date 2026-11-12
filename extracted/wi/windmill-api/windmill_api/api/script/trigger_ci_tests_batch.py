from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.trigger_ci_tests_batch_json_body import TriggerCiTestsBatchJsonBody
from ...models.trigger_ci_tests_batch_response_200 import TriggerCiTestsBatchResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: TriggerCiTestsBatchJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/scripts/trigger_ci_tests_batch".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TriggerCiTestsBatchResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TriggerCiTestsBatchResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TriggerCiTestsBatchResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TriggerCiTestsBatchJsonBody,
) -> Response[TriggerCiTestsBatchResponse200]:
    """queue the CI tests of a batch of deploys

     Queues the CI tests of items deployed with `skip_ci_tests`, plus those of the scripts
    importing them, once nothing those tests read (the tested items, the test scripts and
    their imports) still has a dependency job queued or running. While one does, nothing is
    queued and `pending` lists those paths: call again later, or pass `ignore_pending` to
    queue them anyway. The tests run as the caller, who must be able to deploy each item.

    Args:
        workspace (str):
        json_body (TriggerCiTestsBatchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerCiTestsBatchResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TriggerCiTestsBatchJsonBody,
) -> Optional[TriggerCiTestsBatchResponse200]:
    """queue the CI tests of a batch of deploys

     Queues the CI tests of items deployed with `skip_ci_tests`, plus those of the scripts
    importing them, once nothing those tests read (the tested items, the test scripts and
    their imports) still has a dependency job queued or running. While one does, nothing is
    queued and `pending` lists those paths: call again later, or pass `ignore_pending` to
    queue them anyway. The tests run as the caller, who must be able to deploy each item.

    Args:
        workspace (str):
        json_body (TriggerCiTestsBatchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerCiTestsBatchResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TriggerCiTestsBatchJsonBody,
) -> Response[TriggerCiTestsBatchResponse200]:
    """queue the CI tests of a batch of deploys

     Queues the CI tests of items deployed with `skip_ci_tests`, plus those of the scripts
    importing them, once nothing those tests read (the tested items, the test scripts and
    their imports) still has a dependency job queued or running. While one does, nothing is
    queued and `pending` lists those paths: call again later, or pass `ignore_pending` to
    queue them anyway. The tests run as the caller, who must be able to deploy each item.

    Args:
        workspace (str):
        json_body (TriggerCiTestsBatchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerCiTestsBatchResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TriggerCiTestsBatchJsonBody,
) -> Optional[TriggerCiTestsBatchResponse200]:
    """queue the CI tests of a batch of deploys

     Queues the CI tests of items deployed with `skip_ci_tests`, plus those of the scripts
    importing them, once nothing those tests read (the tested items, the test scripts and
    their imports) still has a dependency job queued or running. While one does, nothing is
    queued and `pending` lists those paths: call again later, or pass `ignore_pending` to
    queue them anyway. The tests run as the caller, who must be able to deploy each item.

    Args:
        workspace (str):
        json_body (TriggerCiTestsBatchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerCiTestsBatchResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
