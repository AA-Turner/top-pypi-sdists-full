from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.run_script_by_hash_inline_json_body import RunScriptByHashInlineJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    hash_: str,
    *,
    json_body: RunScriptByHashInlineJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/jobs/run_inline/h/{hash}".format(
            workspace=workspace,
            hash=hash_,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.OK:
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
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunScriptByHashInlineJsonBody,
) -> Response[Any]:
    """run script by hash without starting a new job

    Args:
        workspace (str):
        hash_ (str):
        json_body (RunScriptByHashInlineJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        hash_=hash_,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    hash_: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunScriptByHashInlineJsonBody,
) -> Response[Any]:
    """run script by hash without starting a new job

    Args:
        workspace (str):
        hash_ (str):
        json_body (RunScriptByHashInlineJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        hash_=hash_,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
