from typing import Any, Dict, List, Optional, Union

import grpc
from grpc import aio

from .._types import OMIT, Omit
from ..exceptions import map_rpc_error
from . import (
    DEFAULT_TIMEOUT_SECONDS,
    SearchRequest,
    SearchResponse,
    SeltzServiceStub,
    auth_metadata,
)


def _build_search_request(
    *,
    query: str,
    api_key: Optional[str],
    max_results: int,
    scope: Union[str, Omit],
    include_domains: Union[List[str], Omit],
    exclude_domains: Union[List[str], Omit],
    from_date: Union[str, Omit],
    to_date: Union[str, Omit],
) -> SearchRequest:
    """Build a SearchRequest, leaving any field passed as OMIT unset.

    Args:
        query (str):
            The query string.

        api_key (str, optional):
            API key to embed in the request, or None when not configured.

        max_results (int):
            The maximum number of search results to return.

        scope (str, optional):
            Restrict the search to a specific scope (e.g. "news").
            Pass OMIT to leave the field unset on the request.

        include_domains (list[str], optional):
            Only include results from these domains (e.g., ["techcrunch.com"]).
            Pass OMIT to leave the field unset on the request.

        exclude_domains (list[str], optional):
            Exclude results from these domains.
            Pass OMIT to leave the field unset on the request.

        from_date (str, optional):
            Only include results published on or after this date (ISO 8601, e.g. "2025-10-28").
            Pass OMIT to leave the field unset on the request.

        to_date (str, optional):
            Only include results published on or before this date (ISO 8601, e.g. "2026-04-29").
            Pass OMIT to leave the field unset on the request.

    Returns:
        SearchRequest: The request message with any OMIT field left unset.
    """

    fields: Dict[str, Any] = {
        "query": query,
        "max_results": max_results,
        "api_key": api_key,
    }

    if not isinstance(scope, Omit):
        fields["scope"] = scope

    if not isinstance(include_domains, Omit):
        fields["include_domains"] = include_domains

    if not isinstance(exclude_domains, Omit):
        fields["exclude_domains"] = exclude_domains

    if not isinstance(from_date, Omit):
        fields["from_date"] = from_date

    if not isinstance(to_date, Omit):
        fields["to_date"] = to_date

    return SearchRequest(**fields)


class SearchService:
    """Service for performing search operations via gRPC."""

    def __init__(self, channel: grpc.Channel, api_key: Optional[str] = None):
        """Initialize the search service.

        Args:
            channel (grpc.Channel):
                gRPC channel for communication.

            api_key (str, optional, default=None):
                API key for authentication.
        """
        self._stub = SeltzServiceStub(channel)
        self._api_key = api_key

    def search(
        self,
        query: str,
        *,
        max_results: int = 10,
        scope: Union[str, Omit] = OMIT,
        include_domains: Union[List[str], Omit] = OMIT,
        exclude_domains: Union[List[str], Omit] = OMIT,
        from_date: Union[str, Omit] = OMIT,
        to_date: Union[str, Omit] = OMIT,
    ) -> SearchResponse:
        """Perform a search query.

        Args:
            query (str):
                The query string.

            max_results (int, optional, default=10):
                The maximum number of search results to return.

            scope (str, optional):
                Restrict the search to a specific scope.
                Omitted from the request when not provided.

            include_domains (list[str], optional):
                Only include results from these domains (e.g., ["techcrunch.com"]).
                Omitted from the request when not provided.

            exclude_domains (list[str], optional):
                Exclude results from these domains.
                Omitted from the request when not provided.

            from_date (str, optional):
                Only include results published on or after this date (ISO 8601, e.g. "2025-10-28").
                Omitted from the request when not provided.

            to_date (str, optional):
                Only include results published on or before this date (ISO 8601, e.g. "2026-04-29").
                Omitted from the request when not provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            SearchResponse: The response containing the search results.
            Search results have URL and content fields provided as empty strings when not available.
        """

        req = _build_search_request(
            query=query,
            api_key=self._api_key,
            max_results=max_results,
            scope=scope,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            from_date=from_date,
            to_date=to_date,
        )

        try:
            return self._stub.Search(
                req,
                metadata=auth_metadata(self._api_key),
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e


class AsyncSearchService:
    """Service for performing search operations via async gRPC."""

    def __init__(self, channel: aio.Channel, api_key: Optional[str] = None):
        """Initialize the async search service.

        Args:
            channel (grpc.aio.Channel):
                Async gRPC channel for communication.

            api_key (str, optional, default=None):
                API key for authentication.
        """
        self._stub = SeltzServiceStub(channel)
        self._api_key = api_key

    async def search(
        self,
        query: str,
        *,
        max_results: int = 10,
        scope: Union[str, Omit] = OMIT,
        include_domains: Union[List[str], Omit] = OMIT,
        exclude_domains: Union[List[str], Omit] = OMIT,
        from_date: Union[str, Omit] = OMIT,
        to_date: Union[str, Omit] = OMIT,
    ) -> SearchResponse:
        """Perform a search query.

        Args:
            query (str):
                The query string.

            max_results (int, optional, default=10):
                The maximum number of search results to return.

            scope (str, optional):
                Restrict the search to a specific scope.
                Omitted from the request when not provided.

            include_domains (list[str], optional):
                Only include results from these domains (e.g., ["techcrunch.com"]).
                Omitted from the request when not provided.

            exclude_domains (list[str], optional):
                Exclude results from these domains.
                Omitted from the request when not provided.

            from_date (str, optional):
                Only include results published on or after this date (ISO 8601, e.g. "2025-10-28").
                Omitted from the request when not provided.

            to_date (str, optional):
                Only include results published on or before this date (ISO 8601, e.g. "2026-04-29").
                Omitted from the request when not provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            SearchResponse: The response containing the search results.
            Search results have URL and content fields provided as empty strings when not available.
        """

        req = _build_search_request(
            query=query,
            api_key=self._api_key,
            max_results=max_results,
            scope=scope,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            from_date=from_date,
            to_date=to_date,
        )

        try:
            return await self._stub.Search(
                req,
                metadata=auth_metadata(self._api_key),
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e
