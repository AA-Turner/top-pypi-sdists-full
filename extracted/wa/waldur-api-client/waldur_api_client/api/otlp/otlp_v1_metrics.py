from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.otlp_v1_metrics_json_body import OtlpV1MetricsJsonBody
from ...models.otlp_v1_metrics_response_200 import OtlpV1MetricsResponse200
from ...types import Response


def _get_kwargs(
    *,
    body: OtlpV1MetricsJsonBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/otlp/v1/metrics/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> OtlpV1MetricsResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OtlpV1MetricsResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OtlpV1MetricsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: OtlpV1MetricsJsonBody,
) -> Response[OtlpV1MetricsResponse200]:
    """Receive OTLP/HTTP metrics

     Accepts an OpenTelemetry ExportMetricsServiceRequest as JSON or protobuf, optionally gzip-encoded.
    Each resource must carry the waldur.resource.uuid attribute; a metric's name is the key of a metric
    the resource's offering adopts. Gauge and Sum (delta or cumulative) are accepted; other types and
    refused points are counted in partial_success.

    Args:
        body (OtlpV1MetricsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OtlpV1MetricsResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: OtlpV1MetricsJsonBody,
) -> OtlpV1MetricsResponse200:
    """Receive OTLP/HTTP metrics

     Accepts an OpenTelemetry ExportMetricsServiceRequest as JSON or protobuf, optionally gzip-encoded.
    Each resource must carry the waldur.resource.uuid attribute; a metric's name is the key of a metric
    the resource's offering adopts. Gauge and Sum (delta or cumulative) are accepted; other types and
    refused points are counted in partial_success.

    Args:
        body (OtlpV1MetricsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OtlpV1MetricsResponse200
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: OtlpV1MetricsJsonBody,
) -> Response[OtlpV1MetricsResponse200]:
    """Receive OTLP/HTTP metrics

     Accepts an OpenTelemetry ExportMetricsServiceRequest as JSON or protobuf, optionally gzip-encoded.
    Each resource must carry the waldur.resource.uuid attribute; a metric's name is the key of a metric
    the resource's offering adopts. Gauge and Sum (delta or cumulative) are accepted; other types and
    refused points are counted in partial_success.

    Args:
        body (OtlpV1MetricsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OtlpV1MetricsResponse200]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: OtlpV1MetricsJsonBody,
) -> OtlpV1MetricsResponse200:
    """Receive OTLP/HTTP metrics

     Accepts an OpenTelemetry ExportMetricsServiceRequest as JSON or protobuf, optionally gzip-encoded.
    Each resource must carry the waldur.resource.uuid attribute; a metric's name is the key of a metric
    the resource's offering adopts. Gauge and Sum (delta or cumulative) are accepted; other types and
    refused points are counted in partial_success.

    Args:
        body (OtlpV1MetricsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OtlpV1MetricsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
