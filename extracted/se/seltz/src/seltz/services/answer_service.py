from typing import Any, AsyncIterator, Dict, Iterator, Optional, Union

import grpc
from grpc import aio

from .._types import OMIT, Omit
from ..exceptions import map_rpc_error
from . import (
    DEFAULT_TIMEOUT_SECONDS,
    AnswerRequest,
    AnswerResponse,
    AnswerServiceStub,
    AnswerStreamRequest,
    AnswerStreamResponse,
    auth_metadata,
)


def _build_answer_request(
    *,
    query: str,
    api_key: Optional[str],
    include_content: bool,
    scope: Union[str, Omit],
) -> AnswerRequest:
    """Build an AnswerRequest, leaving scope unset when passed as OMIT.

    Args:
        query (str):
            The natural-language question.

        api_key (str, optional):
            API key to embed in the request, or None when not configured.

        include_content (bool):
            When True, include the document content text on each citation.
            When False, citations carry only the URL.

        scope (str, optional):
            Restrict the grounding search to a specific scope (e.g. "news").
            Pass OMIT to leave the field unset on the request.

    Returns:
        AnswerRequest: The request message with any OMIT field left unset.
    """

    fields: Dict[str, Any] = {
        "query": query,
        "api_key": api_key,
        "include_content": include_content,
    }

    if not isinstance(scope, Omit):
        fields["scope"] = scope

    return AnswerRequest(**fields)


def _build_answer_stream_request(
    *,
    query: str,
    api_key: Optional[str],
    include_content: bool,
    scope: Union[str, Omit],
) -> AnswerStreamRequest:
    """Build an AnswerStreamRequest, leaving scope unset when passed as OMIT.

    Mirrors :func:`_build_answer_request`; the streaming RPC takes a distinct
    request message with the same fields (the public gRPC API keeps one message
    per RPC).

    Args:
        query (str):
            The natural-language question.

        api_key (str, optional):
            API key to embed in the request, or None when not configured.

        include_content (bool):
            When True, include the document content text on each citation.
            When False, citations carry only the URL.

        scope (str, optional):
            Restrict the grounding search to a specific scope (e.g. "news").
            Pass OMIT to leave the field unset on the request.

    Returns:
        AnswerStreamRequest: The request message with any OMIT field left unset.
    """

    fields: Dict[str, Any] = {
        "query": query,
        "api_key": api_key,
        "include_content": include_content,
    }

    if not isinstance(scope, Omit):
        fields["scope"] = scope

    return AnswerStreamRequest(**fields)


class AnswerService:
    """Service for performing answer (RAG) operations via gRPC."""

    def __init__(self, channel: grpc.Channel, api_key: Optional[str] = None):
        """Initialize the answer service.

        Args:
            channel (grpc.Channel):
                gRPC channel for communication.

            api_key (str, optional, default=None):
                API key for authentication.
        """
        self._stub = AnswerServiceStub(channel)
        self._api_key = api_key

    def answer(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
    ) -> AnswerResponse:
        """Generate a natural-language answer for a query.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            AnswerResponse: The response containing the markdown answer and its citations.
        """

        req = _build_answer_request(
            query=query,
            api_key=self._api_key,
            include_content=include_content,
            scope=scope,
        )

        try:
            return self._stub.Answer(
                req,
                metadata=auth_metadata(self._api_key),
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e

    def answer_stream(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
    ) -> Iterator[AnswerStreamResponse]:
        """Stream a natural-language answer for a query as it is generated.

        The first event carries the ``citations`` the answer is grounded in;
        subsequent events carry ``text_delta`` chunks; the final event carries a
        ``finish_reason``. Inspect each event with ``event.WhichOneof("event")``.

        Unlike :meth:`answer`, no per-call deadline is set: a streaming answer
        is long-lived by design.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Yields:
            AnswerStreamResponse: One streamed event (``citations``,
            ``text_delta``, or ``finish_reason``).
        """

        req = _build_answer_stream_request(
            query=query,
            api_key=self._api_key,
            include_content=include_content,
            scope=scope,
        )

        try:
            for event in self._stub.AnswerStream(
                req,
                metadata=auth_metadata(self._api_key),
            ):
                yield event

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e


class AsyncAnswerService:
    """Service for performing answer (RAG) operations via async gRPC."""

    def __init__(self, channel: aio.Channel, api_key: Optional[str] = None):
        """Initialize the async answer service.

        Args:
            channel (grpc.aio.Channel):
                Async gRPC channel for communication.

            api_key (str, optional, default=None):
                API key for authentication.
        """
        self._stub = AnswerServiceStub(channel)
        self._api_key = api_key

    async def answer(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
    ) -> AnswerResponse:
        """Generate a natural-language answer for a query.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Returns:
            AnswerResponse: The response containing the markdown answer and its citations.
        """

        req = _build_answer_request(
            query=query,
            api_key=self._api_key,
            include_content=include_content,
            scope=scope,
        )

        try:
            return await self._stub.Answer(
                req,
                metadata=auth_metadata(self._api_key),
                timeout=DEFAULT_TIMEOUT_SECONDS,
            )

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e

    async def answer_stream(
        self,
        query: str,
        *,
        include_content: bool = False,
        scope: Union[str, Omit] = OMIT,
    ) -> AsyncIterator[AnswerStreamResponse]:
        """Stream a natural-language answer for a query as it is generated.

        The first event carries the ``citations`` the answer is grounded in;
        subsequent events carry ``text_delta`` chunks; the final event carries a
        ``finish_reason``. Inspect each event with ``event.WhichOneof("event")``.

        Unlike :meth:`answer`, no per-call deadline is set: a streaming answer
        is long-lived by design.

        Args:
            query (str):
                The natural-language question.

            include_content (bool, optional, default=False):
                When True, include the document content text on each citation.
                When False, citations carry only the URL.

            scope (str, optional):
                Restrict the grounding search to a specific scope (e.g. "news").
                Omitted from the request when not provided.

        Raises:
            SeltzAuthenticationError: If the API key is invalid.
            SeltzConnectionError: If the connection to the API fails.
            SeltzTimeoutError: If the request times out.
            SeltzRateLimitError: If the rate limit is exceeded.
            SeltzAPIError: For other API errors.

        Yields:
            AnswerStreamResponse: One streamed event (``citations``,
            ``text_delta``, or ``finish_reason``).
        """

        req = _build_answer_stream_request(
            query=query,
            api_key=self._api_key,
            include_content=include_content,
            scope=scope,
        )

        try:
            async for event in self._stub.AnswerStream(
                req,
                metadata=auth_metadata(self._api_key),
            ):
                yield event

        except grpc.RpcError as e:
            raise map_rpc_error(e) from e
