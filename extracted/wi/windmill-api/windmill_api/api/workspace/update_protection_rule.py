from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_protection_rule_json_body import UpdateProtectionRuleJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    rule_name: str,
    *,
    json_body: UpdateProtectionRuleJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/protection_rules/{rule_name}".format(
            workspace=workspace,
            rule_name=rule_name,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.NOT_FOUND:
        return None
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
    rule_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateProtectionRuleJsonBody,
) -> Response[Any]:
    """update an existing protection rule

    Args:
        workspace (str):
        rule_name (str):
        json_body (UpdateProtectionRuleJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        rule_name=rule_name,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    rule_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateProtectionRuleJsonBody,
) -> Response[Any]:
    """update an existing protection rule

    Args:
        workspace (str):
        rule_name (str):
        json_body (UpdateProtectionRuleJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        rule_name=rule_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
