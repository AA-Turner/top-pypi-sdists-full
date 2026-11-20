from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.run_flow_test_json_body import RunFlowTestJsonBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    json_body: RunFlowTestJsonBody,
    job_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["job_id"] = job_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/jobs/run/flow_test/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "json": json_json_body,
        "params": params,
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
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunFlowTestJsonBody,
    job_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    r"""run a deployed flow with some steps overridden, for tests

     Runs the latest deployed version of the flow as a flow preview, with each step named in `steps`
    either mocked (`{\"return_value\": ...}`) or replaced by a function of the code of `caller_job_id`
    (`{\"function\": \"<name>\"}`), called with the step's inputs. Needs the same rights as a flow
    preview.

    Args:
        workspace (str):
        path (str):
        job_id (Union[Unset, None, str]):
        json_body (RunFlowTestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: RunFlowTestJsonBody,
    job_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    r"""run a deployed flow with some steps overridden, for tests

     Runs the latest deployed version of the flow as a flow preview, with each step named in `steps`
    either mocked (`{\"return_value\": ...}`) or replaced by a function of the code of `caller_job_id`
    (`{\"function\": \"<name>\"}`), called with the step's inputs. Needs the same rights as a flow
    preview.

    Args:
        workspace (str):
        path (str):
        job_id (Union[Unset, None, str]):
        json_body (RunFlowTestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
