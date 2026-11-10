from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.hpc_output_series import HpcOutputSeries
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    forecast_hours: Union[None, Unset, float] = UNSET,
    path: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_forecast_hours: Union[None, Unset, float]
    if isinstance(forecast_hours, Unset):
        json_forecast_hours = UNSET
    else:
        json_forecast_hours = forecast_hours
    params["forecast_hours"] = json_forecast_hours

    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/hpc-workspaces/{uuid}/output_series/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> HpcOutputSeries:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = HpcOutputSeries.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HpcOutputSeries]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    forecast_hours: Union[None, Unset, float] = UNSET,
    path: str,
) -> Response[HpcOutputSeries]:
    """Plot a job output file

     Reads a GROMACS .xvg, a CSV/TSV table or a WRF rsl log from the cluster and returns its series as a
    chart spec, with a short summary.

    Args:
        uuid (UUID):
        forecast_hours (Union[None, Unset, float]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcOutputSeries]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        forecast_hours=forecast_hours,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    forecast_hours: Union[None, Unset, float] = UNSET,
    path: str,
) -> HpcOutputSeries:
    """Plot a job output file

     Reads a GROMACS .xvg, a CSV/TSV table or a WRF rsl log from the cluster and returns its series as a
    chart spec, with a short summary.

    Args:
        uuid (UUID):
        forecast_hours (Union[None, Unset, float]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcOutputSeries
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        forecast_hours=forecast_hours,
        path=path,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    forecast_hours: Union[None, Unset, float] = UNSET,
    path: str,
) -> Response[HpcOutputSeries]:
    """Plot a job output file

     Reads a GROMACS .xvg, a CSV/TSV table or a WRF rsl log from the cluster and returns its series as a
    chart spec, with a short summary.

    Args:
        uuid (UUID):
        forecast_hours (Union[None, Unset, float]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HpcOutputSeries]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        forecast_hours=forecast_hours,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    forecast_hours: Union[None, Unset, float] = UNSET,
    path: str,
) -> HpcOutputSeries:
    """Plot a job output file

     Reads a GROMACS .xvg, a CSV/TSV table or a WRF rsl log from the cluster and returns its series as a
    chart spec, with a short summary.

    Args:
        uuid (UUID):
        forecast_hours (Union[None, Unset, float]):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HpcOutputSeries
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            forecast_hours=forecast_hours,
            path=path,
        )
    ).parsed
