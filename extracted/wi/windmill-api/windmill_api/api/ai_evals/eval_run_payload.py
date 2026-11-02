from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.eval_run_payload_response_200 import EvalRunPayloadResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    job_id: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["job_id"] = job_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai_evals/run_payload".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[EvalRunPayloadResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EvalRunPayloadResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[EvalRunPayloadResponse200]:
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
    job_id: str,
) -> Response[EvalRunPayloadResponse200]:
    """the run one iteration of an eval run answered, as its scorers read it

     Called by the step a run's flow places between the agent and its scorers. Every tool call is
    enriched with the arguments, result, status and duration of the job that ran it, and with the schema
    of the script version it ran, none of which the flow itself can read.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EvalRunPayloadResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    job_id: str,
) -> Optional[EvalRunPayloadResponse200]:
    """the run one iteration of an eval run answered, as its scorers read it

     Called by the step a run's flow places between the agent and its scorers. Every tool call is
    enriched with the arguments, result, status and duration of the job that ran it, and with the schema
    of the script version it ran, none of which the flow itself can read.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EvalRunPayloadResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        job_id=job_id,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    job_id: str,
) -> Response[EvalRunPayloadResponse200]:
    """the run one iteration of an eval run answered, as its scorers read it

     Called by the step a run's flow places between the agent and its scorers. Every tool call is
    enriched with the arguments, result, status and duration of the job that ran it, and with the schema
    of the script version it ran, none of which the flow itself can read.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EvalRunPayloadResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    job_id: str,
) -> Optional[EvalRunPayloadResponse200]:
    """the run one iteration of an eval run answered, as its scorers read it

     Called by the step a run's flow places between the agent and its scorers. Every tool call is
    enriched with the arguments, result, status and duration of the job that ran it, and with the schema
    of the script version it ran, none of which the flow itself can read.

    Args:
        workspace (str):
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EvalRunPayloadResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            job_id=job_id,
        )
    ).parsed
