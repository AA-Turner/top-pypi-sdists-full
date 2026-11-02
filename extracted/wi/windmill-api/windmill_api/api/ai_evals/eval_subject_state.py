from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.eval_subject_state_response_200 import EvalSubjectStateResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    path: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai_evals/subject_state".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[EvalSubjectStateResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EvalSubjectStateResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[EvalSubjectStateResponse200]:
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
    path: str,
) -> Response[EvalSubjectStateResponse200]:
    """what the agent under test is right now

     The version it is deployed at. Small on purpose: the results endpoint reports the same thing but
    harvests scores and reads every job to do it, so it is not something to ask for on its own.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EvalSubjectStateResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Optional[EvalSubjectStateResponse200]:
    """what the agent under test is right now

     The version it is deployed at. Small on purpose: the results endpoint reports the same thing but
    harvests scores and reads every job to do it, so it is not something to ask for on its own.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EvalSubjectStateResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Response[EvalSubjectStateResponse200]:
    """what the agent under test is right now

     The version it is deployed at. Small on purpose: the results endpoint reports the same thing but
    harvests scores and reads every job to do it, so it is not something to ask for on its own.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EvalSubjectStateResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Optional[EvalSubjectStateResponse200]:
    """what the agent under test is right now

     The version it is deployed at. Small on purpose: the results endpoint reports the same thing but
    harvests scores and reads every job to do it, so it is not something to ask for on its own.

    Args:
        workspace (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EvalSubjectStateResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            path=path,
        )
    ).parsed
