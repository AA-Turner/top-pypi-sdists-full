import os
from types import TracebackType
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Type, Union

from ._types import OMIT, Omit
from .client import AsyncSeltzClient, SeltzClient
from .exceptions import SeltzConfigurationError
from .services import AnswerResponse, AnswerStreamResponse, SearchResponse
from .services.answer_service import AnswerService, AsyncAnswerService
from .services.monitor_service import AsyncMonitorService, MonitorService
from .services.search_service import AsyncSearchService, SearchService


class Seltz:
    """A client for interacting with Seltz API."""

    _ENDPOINT: str = "grpc.seltz.ai"

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = _ENDPOINT,
        insecure: bool = False,
    ):
        """Initialize the Seltz client with the provided API key.

        Args:
            api_key (str, optional, default=None):
                The API key for authenticating with the Seltz API.
                If not provided, the value is read from the `SELTZ_API_KEY` environment variable.

            endpoint (str, optional, default=grpc.seltz.ai):
                The API endpoint for the Seltz API.

            insecure (bool, optional, default=False):
                Whether to use insecure connection.

        Raises:
            SeltzConfigurationError: If no API key is provided
        """

        self.endpoint = endpoint
        self.insecure = insecure

        api_key = api_key or os.environ.get("SELTZ_API_KEY")

        if api_key is None:
            raise SeltzConfigurationError(
                "API key not found. Pass `api_key` or set the `SELTZ_API_KEY` environment variable."
            )

        self._client = SeltzClient(
            endpoint=endpoint, api_key=api_key, insecure=insecure
        )

        self._search = SearchService(self._client.channel, api_key)
        self._answer = AnswerService(self._client.channel, api_key)
        self._monitor = MonitorService(self._client.channel, api_key)

    @property
    def monitor(self) -> MonitorService:
        """Monitor CRUD, run history and the two record cursors."""
        return self._monitor

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
        """Perform a search.

        Args:
            query (str):
                The query string.

            max_results (int, optional, default=10):
                The maximum number of search results to return.

            scope (str, optional):
                Restrict the search to a specific scope.
                Must be one of: "news".
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

        Examples:
            response = seltz.search("best ai search engines", max_results=10)
            response = seltz.search("latest news", from_date="2025-01-01")
            response = seltz.search("tech news", include_domains=["techcrunch.com"])
        """

        return self._search.search(
            query=query,
            max_results=max_results,
            scope=scope,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            from_date=from_date,
            to_date=to_date,
        )

    def answer(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
        model: Union[str, Omit] = OMIT,
        response_format: Union[Dict[str, Any], Omit] = OMIT,
        system_prompt: Union[str, Omit] = OMIT,
    ) -> AnswerResponse:
        """Generate a natural-language answer for a query, grounded in search results.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

            model (str, optional):
                Select the answer tier (e.g. "seltz-pro").
                Defaults to "seltz-base" when not provided.

            response_format (dict, optional):
                An OpenAI-style ``response_format`` object requesting structured
                output (e.g. ``{"type": "json_schema", "json_schema": {...}}``).
                When provided, the ``answer`` field carries the JSON payload
                matching the requested schema instead of Markdown prose;
                ``citations`` are still returned. Omitted from the request when
                not provided (the answer stays Markdown).

            system_prompt (str, optional):
                Instructions steering how the answer is presented — tone,
                voice, format. Grounding and citations are unaffected.
                Composes with ``response_format`` and applies at every tier.
                Empty or whitespace-only is treated as absent.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            AnswerResponse: The response containing the markdown answer and its citations.

        Examples:
            response = seltz.answer("Who is Apple's next CEO?")
            response = seltz.answer("Summarize recent AI news", include_content=True)
            response = seltz.answer("Latest AI headlines", scope="news")
            response = seltz.answer("Who is Apple's next CEO?", model="seltz-pro")
        """

        return self._answer.answer(
            query=query,
            include_content=include_content,
            scope=scope,
            model=model,
            response_format=response_format,
            system_prompt=system_prompt,
        )

    def answer_stream(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
        model: Union[str, Omit] = OMIT,
        response_format: Union[Dict[str, Any], Omit] = OMIT,
        system_prompt: Union[str, Omit] = OMIT,
    ) -> Iterator[AnswerStreamResponse]:
        """Stream a natural-language answer for a query as it is generated.

        The first event carries the ``citations`` the answer is grounded in;
        subsequent events carry ``text_delta`` chunks; the final event carries a
        ``finish_reason``. Inspect each event with ``event.WhichOneof("event")``.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

            model (str, optional):
                Select the answer tier (e.g. "seltz-pro").
                Defaults to "seltz-base" when not provided.

            response_format (dict, optional):
                An OpenAI-style ``response_format`` object requesting structured
                output (e.g. ``{"type": "json_schema", "json_schema": {...}}``).
                When provided, the ``answer`` field carries the JSON payload
                matching the requested schema instead of Markdown prose;
                ``citations`` are still returned. Omitted from the request when
                not provided (the answer stays Markdown).

            system_prompt (str, optional):
                Instructions steering how the answer is presented — tone,
                voice, format. Grounding and citations are unaffected.
                Composes with ``response_format`` and applies at every tier.
                Empty or whitespace-only is treated as absent.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Yields:
            AnswerStreamResponse: One streamed event (``citations``,
            ``text_delta``, or ``finish_reason``).

        Examples:
            for event in seltz.answer_stream("Who is Apple's next CEO?"):
                kind = event.WhichOneof("event")
                if kind == "text_delta":
                    print(event.text_delta, end="", flush=True)
        """

        return self._answer.answer_stream(
            query=query,
            include_content=include_content,
            scope=scope,
            model=model,
            response_format=response_format,
            system_prompt=system_prompt,
        )

    def close(self) -> None:
        """Close the underlying gRPC channel and release its resources."""
        self._client.channel.close()

    def __enter__(self) -> "Seltz":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()


class AsyncSeltz:
    """An asyncio client for interacting with the Seltz API."""

    _ENDPOINT: str = "grpc.seltz.ai"

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = _ENDPOINT,
        insecure: bool = False,
    ):
        """Initialize the async Seltz client with the provided API key.

        Args:
            api_key (str, optional, default=None):
                The API key for authenticating with the Seltz API.
                If not provided, the value is read from the `SELTZ_API_KEY` environment variable.

            endpoint (str, optional, default=grpc.seltz.ai):
                The API endpoint for the Seltz API.

            insecure (bool, optional, default=False):
                Whether to use insecure connection.

        Raises:
            SeltzConfigurationError: If no API key is provided
        """

        self.endpoint = endpoint
        self.insecure = insecure

        api_key = api_key or os.environ.get("SELTZ_API_KEY")

        if api_key is None:
            raise SeltzConfigurationError(
                "API key not found. Pass `api_key` or set the `SELTZ_API_KEY` environment variable."
            )

        self._client = AsyncSeltzClient(
            endpoint=endpoint, api_key=api_key, insecure=insecure
        )

        self._search = AsyncSearchService(self._client.channel, api_key)
        self._answer = AsyncAnswerService(self._client.channel, api_key)
        self._monitor = AsyncMonitorService(self._client.channel, api_key)

    @property
    def monitor(self) -> AsyncMonitorService:
        """Monitor CRUD, run history and the two record cursors."""
        return self._monitor

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
        """Perform a search.

        Args:
            query (str):
                The query string.

            max_results (int, optional, default=10):
                The maximum number of search results to return.

            scope (str, optional):
                Restrict the search to a specific scope.
                Must be one of: "news".
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

        Examples:
            response = await seltz.search("best ai search engines", max_results=10)
            response = await seltz.search("latest news", from_date="2025-01-01")
            response = await seltz.search("tech news", include_domains=["techcrunch.com"])
        """

        return await self._search.search(
            query=query,
            max_results=max_results,
            scope=scope,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            from_date=from_date,
            to_date=to_date,
        )

    async def answer(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
        model: Union[str, Omit] = OMIT,
        response_format: Union[Dict[str, Any], Omit] = OMIT,
        system_prompt: Union[str, Omit] = OMIT,
    ) -> AnswerResponse:
        """Generate a natural-language answer for a query, grounded in search results.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

            model (str, optional):
                Select the answer tier (e.g. "seltz-pro").
                Defaults to "seltz-base" when not provided.

            response_format (dict, optional):
                An OpenAI-style ``response_format`` object requesting structured
                output (e.g. ``{"type": "json_schema", "json_schema": {...}}``).
                When provided, the ``answer`` field carries the JSON payload
                matching the requested schema instead of Markdown prose;
                ``citations`` are still returned. Omitted from the request when
                not provided (the answer stays Markdown).

            system_prompt (str, optional):
                Instructions steering how the answer is presented — tone,
                voice, format. Grounding and citations are unaffected.
                Composes with ``response_format`` and applies at every tier.
                Empty or whitespace-only is treated as absent.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            AnswerResponse: The response containing the markdown answer and its citations.

        Examples:
            response = await seltz.answer("Who is Apple's next CEO?")
            response = await seltz.answer("Summarize recent AI news", include_content=True)
            response = await seltz.answer("Latest AI headlines", scope="news")
            response = await seltz.answer("Who is Apple's next CEO?", model="seltz-pro")
        """

        return await self._answer.answer(
            query=query,
            include_content=include_content,
            scope=scope,
            model=model,
            response_format=response_format,
            system_prompt=system_prompt,
        )

    def answer_stream(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
        model: Union[str, Omit] = OMIT,
        response_format: Union[Dict[str, Any], Omit] = OMIT,
        system_prompt: Union[str, Omit] = OMIT,
    ) -> AsyncIterator[AnswerStreamResponse]:
        """Stream a natural-language answer for a query as it is generated.

        The first event carries the ``citations`` the answer is grounded in;
        subsequent events carry ``text_delta`` chunks; the final event carries a
        ``finish_reason``. Inspect each event with ``event.WhichOneof("event")``.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

            model (str, optional):
                Select the answer tier (e.g. "seltz-pro").
                Defaults to "seltz-base" when not provided.

            response_format (dict, optional):
                An OpenAI-style ``response_format`` object requesting structured
                output (e.g. ``{"type": "json_schema", "json_schema": {...}}``).
                When provided, the ``answer`` field carries the JSON payload
                matching the requested schema instead of Markdown prose;
                ``citations`` are still returned. Omitted from the request when
                not provided (the answer stays Markdown).

            system_prompt (str, optional):
                Instructions steering how the answer is presented — tone,
                voice, format. Grounding and citations are unaffected.
                Composes with ``response_format`` and applies at every tier.
                Empty or whitespace-only is treated as absent.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Yields:
            AnswerStreamResponse: One streamed event (``citations``,
            ``text_delta``, or ``finish_reason``).

        Examples:
            async for event in seltz.answer_stream("Who is Apple's next CEO?"):
                if event.WhichOneof("event") == "text_delta":
                    print(event.text_delta, end="", flush=True)
        """

        return self._answer.answer_stream(
            query=query,
            include_content=include_content,
            scope=scope,
            model=model,
            response_format=response_format,
            system_prompt=system_prompt,
        )

    async def close(self) -> None:
        """Close the underlying gRPC channel and release its resources."""
        await self._client.channel.close()

    async def __aenter__(self) -> "AsyncSeltz":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()
