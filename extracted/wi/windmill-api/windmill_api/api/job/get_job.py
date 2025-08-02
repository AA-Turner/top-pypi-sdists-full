from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_job_response_200_type_0 import GetJobResponse200Type0
from ...models.get_job_response_200_type_1 import GetJobResponse200Type1
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    no_logs: Union[Unset, None, bool] = UNSET,
    no_code: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["no_logs"] = no_logs

    params["no_code"] = no_code

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/jobs_u/get/{id}".format(
            workspace=workspace,
            id=id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union["GetJobResponse200Type0", "GetJobResponse200Type1"]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(data: object) -> Union["GetJobResponse200Type0", "GetJobResponse200Type1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = GetJobResponse200Type0.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = GetJobResponse200Type1.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union["GetJobResponse200Type0", "GetJobResponse200Type1"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    no_logs: Union[Unset, None, bool] = UNSET,
    no_code: Union[Unset, None, bool] = UNSET,
) -> Response[Union["GetJobResponse200Type0", "GetJobResponse200Type1"]]:
    """get job

    Args:
        workspace (str):
        id (str):
        no_logs (Union[Unset, None, bool]):
        no_code (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['GetJobResponse200Type0', 'GetJobResponse200Type1']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        no_logs=no_logs,
        no_code=no_code,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    no_logs: Union[Unset, None, bool] = UNSET,
    no_code: Union[Unset, None, bool] = UNSET,
) -> Optional[Union["GetJobResponse200Type0", "GetJobResponse200Type1"]]:
    """get job

    Args:
        workspace (str):
        id (str):
        no_logs (Union[Unset, None, bool]):
        no_code (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['GetJobResponse200Type0', 'GetJobResponse200Type1']
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
        no_logs=no_logs,
        no_code=no_code,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    no_logs: Union[Unset, None, bool] = UNSET,
    no_code: Union[Unset, None, bool] = UNSET,
) -> Response[Union["GetJobResponse200Type0", "GetJobResponse200Type1"]]:
    """get job

    Args:
        workspace (str):
        id (str):
        no_logs (Union[Unset, None, bool]):
        no_code (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['GetJobResponse200Type0', 'GetJobResponse200Type1']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        no_logs=no_logs,
        no_code=no_code,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    no_logs: Union[Unset, None, bool] = UNSET,
    no_code: Union[Unset, None, bool] = UNSET,
) -> Optional[Union["GetJobResponse200Type0", "GetJobResponse200Type1"]]:
    """get job

    Args:
        workspace (str):
        id (str):
        no_logs (Union[Unset, None, bool]):
        no_code (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['GetJobResponse200Type0', 'GetJobResponse200Type1']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
            no_logs=no_logs,
            no_code=no_code,
        )
    ).parsed
