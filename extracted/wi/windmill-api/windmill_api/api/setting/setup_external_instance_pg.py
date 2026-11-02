from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.setup_external_instance_pg_json_body import SetupExternalInstancePgJsonBody
from ...models.setup_external_instance_pg_response_200 import SetupExternalInstancePgResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: SetupExternalInstancePgJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/settings/external_instance_pg/setup",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SetupExternalInstancePgResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SetupExternalInstancePgResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SetupExternalInstancePgResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupExternalInstancePgJsonBody,
) -> Response[SetupExternalInstancePgResponse200]:
    """Sets up the external instance cluster with its saved admin login, optionally rotating the passwords
    Windmill manages on it (enterprise edition only)

    Args:
        json_body (SetupExternalInstancePgJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetupExternalInstancePgResponse200]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupExternalInstancePgJsonBody,
) -> Optional[SetupExternalInstancePgResponse200]:
    """Sets up the external instance cluster with its saved admin login, optionally rotating the passwords
    Windmill manages on it (enterprise edition only)

    Args:
        json_body (SetupExternalInstancePgJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetupExternalInstancePgResponse200
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupExternalInstancePgJsonBody,
) -> Response[SetupExternalInstancePgResponse200]:
    """Sets up the external instance cluster with its saved admin login, optionally rotating the passwords
    Windmill manages on it (enterprise edition only)

    Args:
        json_body (SetupExternalInstancePgJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetupExternalInstancePgResponse200]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetupExternalInstancePgJsonBody,
) -> Optional[SetupExternalInstancePgResponse200]:
    """Sets up the external instance cluster with its saved admin login, optionally rotating the passwords
    Windmill manages on it (enterprise edition only)

    Args:
        json_body (SetupExternalInstancePgJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetupExternalInstancePgResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
