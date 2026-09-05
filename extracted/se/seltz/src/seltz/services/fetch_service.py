"""Fetch URLs as LLM-ready content, over the generated gRPC stubs."""

from typing import Any, Dict, Iterable, Optional, Union

import grpc
from grpc import aio

from .._types import OMIT, Omit, is_given
from ..exceptions import map_rpc_error
from . import FetchRequest, FetchResponse, FetchServiceStub, auth_metadata


def _build_fetch_request(
    *,
    urls: Iterable[str],
    api_key: Optional[str],
    formats: Union[Iterable[str], None, Omit],
    tier: Union[str, None, Omit],
    timeout_ms: Union[int, None, Omit],
) -> FetchRequest:
    """Build a FetchRequest, leaving formats, tier and timeout_ms unset when
    passed as OMIT.

    Args:
        urls (Iterable[str]):
            The URLs to fetch.

        api_key (str, optional):
            API key to embed in the request, or None when not configured.

        formats (Iterable[str], optional):
            Representations to return. Pass OMIT to leave the field unset.

        tier (str, optional):
            The service tier. Pass OMIT to leave the field unset.

        timeout_ms (int, optional):
            Per-URL wall-clock budget in milliseconds. Pass OMIT to leave the
            field unset.

    Returns:
        FetchRequest: The request message with any OMIT field left unset.
    """

    fields: Dict[str, Any] = {"urls": urls, "api_key": api_key}

    if is_given(formats) and formats is not None:
        fields["formats"] = formats

    if is_given(tier) and tier is not None:
        fields["tier"] = tier

    if is_given(timeout_ms) and timeout_ms is not None:
        fields["timeout_ms"] = timeout_ms

    return FetchRequest(**fields)


class FetchService:
    """Service for fetching URLs as LLM-ready content via gRPC."""

    def __init__(self, channel: grpc.Channel, api_key: Optional[str] = None):
        """Initialize the fetch service.

        Args:
            channel (grpc.Channel):
                gRPC channel for communication.

            api_key (str, optional, default=None):
                API key for authentication.
        """
        self._stub = FetchServiceStub(channel)
        self._api_key = api_key

    def fetch(
        self,
        urls: Iterable[str],
        *,
        formats: Union[Iterable[str], None, Omit] = OMIT,
        tier: Union[str, None, Omit] = OMIT,
        timeout_ms: Union[int, None, Omit] = OMIT,
    ) -> FetchResponse:
        """Fetch the content of up to 20 URLs.

        A failure to fetch one page is not a call failure. The response carries
        one result per requested URL, in the order requested, and a page that
        could not be fetched arrives as that result's
        ``status = FetchStatus.FETCH_STATUS_ERROR`` with an ``error.code``.
        Correlate on ``result.requested_url`` rather than on position.

        Args:
            urls (Iterable[str]):
                The URLs to fetch. At least one, at most 20. Each must be an
                absolute http or https URL of at most 2048 bytes, and no two
                may be equal.

            formats (Iterable[str], optional):
                Representations to return. Omitted from the request when not
                provided, which the service reads as ``["markdown"]``.

            tier (str, optional):
                The service tier, which selects the price. Omitted from the
                request when not provided, which the service reads as
                ``"pro"``.

            timeout_ms (int, optional):
                Wall-clock budget for one URL, in milliseconds. Applies per
                URL, not to the batch. Omitted from the request when not
                provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            FetchResponse: One ``FetchResult`` per requested URL.

        Examples:
            response = seltz.fetch(["https://example.com/"])
            for result in response.results:
                print(result.requested_url, result.status)
        """

        req = _build_fetch_request(
            urls=urls,
            api_key=self._api_key,
            formats=formats,
            tier=tier,
            timeout_ms=timeout_ms,
        )

        try:
            # No client deadline: `timeout_ms` is the per-URL budget and the
            # server enforces it.
            return self._stub.Fetch(
                req,
                metadata=auth_metadata(self._api_key),
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e


class AsyncFetchService:
    """Service for fetching URLs as LLM-ready content via async gRPC."""

    def __init__(self, channel: aio.Channel, api_key: Optional[str] = None):
        """Initialize the async fetch service.

        Args:
            channel (grpc.aio.Channel):
                Async gRPC channel for communication.

            api_key (str, optional, default=None):
                API key for authentication.
        """
        self._stub = FetchServiceStub(channel)
        self._api_key = api_key

    async def fetch(
        self,
        urls: Iterable[str],
        *,
        formats: Union[Iterable[str], None, Omit] = OMIT,
        tier: Union[str, None, Omit] = OMIT,
        timeout_ms: Union[int, None, Omit] = OMIT,
    ) -> FetchResponse:
        """Fetch the content of up to 20 URLs.

        A failure to fetch one page is not a call failure. The response carries
        one result per requested URL, in the order requested, and a page that
        could not be fetched arrives as that result's
        ``status = FetchStatus.FETCH_STATUS_ERROR`` with an ``error.code``.
        Correlate on ``result.requested_url`` rather than on position.

        Args:
            urls (Iterable[str]):
                The URLs to fetch. At least one, at most 20. Each must be an
                absolute http or https URL of at most 2048 bytes, and no two
                may be equal.

            formats (Iterable[str], optional):
                Representations to return. Omitted from the request when not
                provided, which the service reads as ``["markdown"]``.

            tier (str, optional):
                The service tier, which selects the price. Omitted from the
                request when not provided, which the service reads as
                ``"pro"``.

            timeout_ms (int, optional):
                Wall-clock budget for one URL, in milliseconds. Applies per
                URL, not to the batch. Omitted from the request when not
                provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            FetchResponse: One ``FetchResult`` per requested URL.

        Examples:
            response = await seltz.fetch(["https://example.com/"])
            for result in response.results:
                print(result.requested_url, result.status)
        """

        req = _build_fetch_request(
            urls=urls,
            api_key=self._api_key,
            formats=formats,
            tier=tier,
            timeout_ms=timeout_ms,
        )

        try:
            # No client deadline: `timeout_ms` is the per-URL budget and the
            # server enforces it.
            return await self._stub.Fetch(
                req,
                metadata=auth_metadata(self._api_key),
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e
