from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_deployment_request_json_body import CreateDeploymentRequestJsonBody
from ...models.create_deployment_request_response_200 import CreateDeploymentRequestResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: CreateDeploymentRequestJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/deployment_request".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CreateDeploymentRequestResponse200]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateDeploymentRequestResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = cast(Any, None)
        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, CreateDeploymentRequestResponse200]]:
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
    json_body: CreateDeploymentRequestJsonBody,
) -> Response[Union[Any, CreateDeploymentRequestResponse200]]:
    """create a new deployment request

    Args:
        workspace (str):
        json_body (CreateDeploymentRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateDeploymentRequestResponse200]]
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
    json_body: CreateDeploymentRequestJsonBody,
) -> Optional[Union[Any, CreateDeploymentRequestResponse200]]:
    """create a new deployment request

    Args:
        workspace (str):
        json_body (CreateDeploymentRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateDeploymentRequestResponse200]
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
    json_body: CreateDeploymentRequestJsonBody,
) -> Response[Union[Any, CreateDeploymentRequestResponse200]]:
    """create a new deployment request

    Args:
        workspace (str):
        json_body (CreateDeploymentRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CreateDeploymentRequestResponse200]]
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
    json_body: CreateDeploymentRequestJsonBody,
) -> Optional[Union[Any, CreateDeploymentRequestResponse200]]:
    """create a new deployment request

    Args:
        workspace (str):
        json_body (CreateDeploymentRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CreateDeploymentRequestResponse200]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
