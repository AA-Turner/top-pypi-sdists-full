from typing import Any, Dict, List, Optional, Union

import grpc
from grpc import aio

from .._types import OMIT, Omit, is_given
from ..exceptions import map_rpc_error
from . import (
    DEFAULT_TIMEOUT_SECONDS,
    Fields,
    SearchRequest,
    SearchResponse,
    SeltzServiceStub,
    auth_metadata,
)

# The tier names the service accepts, and what a caller passes here. The wire
# field is a plain string, so there is nothing to map: the name is forwarded as
# written.
#
# `str` rather than a `Literal` of the tiers that happen to exist today. The
# service owns the set of tier names: it matches them case-insensitively and
# rejects one it does not recognize, in a 400 that names the tiers it accepts.
# Enumerating them here would put that list in two places and make adding or
# renaming a tier an SDK release -- a caller on an older version could not name
# a tier the service already serves. So this SDK carries no list of tier names
# and needs no update when they change; see the API reference for the current
# ones.
SearchTierName = str


def _build_search_request(
    *,
    query: str,
    api_key: Optional[str],
    max_results: int,
    scope: Union[str, None, Omit],
    include_domains: Union[List[str], None, Omit],
    exclude_domains: Union[List[str], None, Omit],
    from_date: Union[str, None, Omit],
    to_date: Union[str, None, Omit],
    tier: Union[SearchTierName, None, Omit],
    fields: Union[Fields, None, Omit],
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

        tier (str, optional):
            Which search tier serves the request, "base" or "pro". Forwarded as
            given and not checked here; the service owns the set of tiers.
            Pass OMIT to leave the field unset on the request, which defaults
            to "pro".

        fields (Fields, optional):
            Which members of each result document to populate.
            Pass OMIT to leave the field unset on the request, which returns
            content only.

    Returns:
        SearchRequest: The request message with any OMIT field left unset.
    """

    request_fields: Dict[str, Any] = {
        "query": query,
        "max_results": max_results,
        "api_key": api_key,
    }

    if is_given(scope) and scope is not None:
        request_fields["scope"] = scope

    if is_given(include_domains) and include_domains is not None:
        request_fields["include_domains"] = include_domains

    if is_given(exclude_domains) and exclude_domains is not None:
        request_fields["exclude_domains"] = exclude_domains

    if is_given(from_date) and from_date is not None:
        request_fields["from_date"] = from_date

    if is_given(to_date) and to_date is not None:
        request_fields["to_date"] = to_date

    # Forwarded as given, with no local validation: the service matches the name
    # case-insensitively and rejects one it does not recognize, quoting the
    # tiers it accepts. Checking here would only duplicate that, and would go
    # stale the first time a tier is added.
    if is_given(tier) and tier is not None:
        request_fields["tier"] = tier

    if is_given(fields) and fields is not None:
        request_fields["fields"] = fields

    return SearchRequest(**request_fields)


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
        scope: Union[str, None, Omit] = OMIT,
        include_domains: Union[List[str], None, Omit] = OMIT,
        exclude_domains: Union[List[str], None, Omit] = OMIT,
        from_date: Union[str, None, Omit] = OMIT,
        to_date: Union[str, None, Omit] = OMIT,
        tier: Union[SearchTierName, None, Omit] = OMIT,
        fields: Union[Fields, None, Omit] = OMIT,
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

            tier (str, optional):
                Which search tier serves the request, "base" or "pro". This
                never changes which corpus is searched -- that is `scope`, and
                the two are orthogonal.
                Omitted from the request when not provided, which defaults to
                "pro", the higher-precision tier; name the "base" tier to opt
                out of its reranking.
                The name is forwarded as given and is not checked here: the
                service folds case, rejects a name it does not recognize, and
                names the accepted tiers in the error. The SDK holds no list of
                tier names, so it needs no update when they change.

            fields (Fields, optional):
                Which members of each result document to populate.
                `Fields(snippets=True)` returns passages and no content: a
                member you do not set is off, so pass
                `Fields(content=True, snippets=True)` to get both.
                Omitted from the request when not provided, which returns
                content only.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            SearchResponse: The response containing the search results.
            Only the members `fields` asked for are populated; `url` and
            `published_date` always are.
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
            tier=tier,
            fields=fields,
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
        scope: Union[str, None, Omit] = OMIT,
        include_domains: Union[List[str], None, Omit] = OMIT,
        exclude_domains: Union[List[str], None, Omit] = OMIT,
        from_date: Union[str, None, Omit] = OMIT,
        to_date: Union[str, None, Omit] = OMIT,
        tier: Union[SearchTierName, None, Omit] = OMIT,
        fields: Union[Fields, None, Omit] = OMIT,
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

            tier (str, optional):
                Which search tier serves the request, "base" or "pro". This
                never changes which corpus is searched -- that is `scope`, and
                the two are orthogonal.
                Omitted from the request when not provided, which defaults to
                "pro", the higher-precision tier; name the "base" tier to opt
                out of its reranking.
                The name is forwarded as given and is not checked here: the
                service folds case, rejects a name it does not recognize, and
                names the accepted tiers in the error. The SDK holds no list of
                tier names, so it needs no update when they change.

            fields (Fields, optional):
                Which members of each result document to populate.
                `Fields(snippets=True)` returns passages and no content: a
                member you do not set is off, so pass
                `Fields(content=True, snippets=True)` to get both.
                Omitted from the request when not provided, which returns
                content only.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            SearchResponse: The response containing the search results.
            Only the members `fields` asked for are populated; `url` and
            `published_date` always are.
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
            tier=tier,
            fields=fields,
        )

        try:
            return await self._stub.Search(
                req,
                metadata=auth_metadata(self._api_key),
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e
