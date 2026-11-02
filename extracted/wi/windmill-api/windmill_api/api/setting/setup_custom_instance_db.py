from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.setup_custom_instance_db_json_body import SetupCustomInstanceDbJsonBody
from ...models.setup_custom_instance_db_response_200 import SetupCustomInstanceDbResponse200
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    json_body: SetupCustomInstanceDbJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/settings/setup_custom_instance_pg_database/{name}".format(
            name=name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SetupCustomInstanceDbResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SetupCustomInstanceDbResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SetupCustomInstanceDbResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupCustomInstanceDbJsonBody,
) -> Response[SetupCustomInstanceDbResponse200]:
    """Runs CREATE DATABASE on the Windmill Postgres and grants access to the custom_instance_user

    Args:
        name (str):
        json_body (SetupCustomInstanceDbJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetupCustomInstanceDbResponse200]
    """

    kwargs = _get_kwargs(
        name=name,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupCustomInstanceDbJsonBody,
) -> Optional[SetupCustomInstanceDbResponse200]:
    """Runs CREATE DATABASE on the Windmill Postgres and grants access to the custom_instance_user

    Args:
        name (str):
        json_body (SetupCustomInstanceDbJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetupCustomInstanceDbResponse200
    """

    return sync_detailed(
        name=name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupCustomInstanceDbJsonBody,
) -> Response[SetupCustomInstanceDbResponse200]:
    """Runs CREATE DATABASE on the Windmill Postgres and grants access to the custom_instance_user

    Args:
        name (str):
        json_body (SetupCustomInstanceDbJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetupCustomInstanceDbResponse200]
    """

    kwargs = _get_kwargs(
        name=name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupCustomInstanceDbJsonBody,
) -> Optional[SetupCustomInstanceDbResponse200]:
    """Runs CREATE DATABASE on the Windmill Postgres and grants access to the custom_instance_user

    Args:
        name (str):
        json_body (SetupCustomInstanceDbJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetupCustomInstanceDbResponse200
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            json_body=json_body,
        )
    ).parsed
