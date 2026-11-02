from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_success_handler_json_body_type_0 import EditSuccessHandlerJsonBodyType0
from ...models.edit_success_handler_json_body_type_1 import EditSuccessHandlerJsonBodyType1
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: Union["EditSuccessHandlerJsonBodyType0", "EditSuccessHandlerJsonBodyType1"],
) -> Dict[str, Any]:
    pass

    json_json_body: Dict[str, Any]

    if isinstance(json_body, EditSuccessHandlerJsonBodyType0):
        json_json_body = json_body.to_dict()

    else:
        json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/edit_success_handler".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    json_body: Union["EditSuccessHandlerJsonBodyType0", "EditSuccessHandlerJsonBodyType1"],
) -> Response[Any]:
    """edit success handler

    Args:
        workspace (str):
        json_body (Union['EditSuccessHandlerJsonBodyType0', 'EditSuccessHandlerJsonBodyType1']):
            Request body for editing the workspace success handler. Accepts both new grouped format
            and legacy flat format for backward compatibility.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: Union["EditSuccessHandlerJsonBodyType0", "EditSuccessHandlerJsonBodyType1"],
) -> Response[Any]:
    """edit success handler

    Args:
        workspace (str):
        json_body (Union['EditSuccessHandlerJsonBodyType0', 'EditSuccessHandlerJsonBodyType1']):
            Request body for editing the workspace success handler. Accepts both new grouped format
            and legacy flat format for backward compatibility.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
