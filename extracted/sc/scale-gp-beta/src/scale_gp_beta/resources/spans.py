# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from datetime import datetime

import httpx

from ..types import (
    SpanType,
    SpanStatus,
    span_batch_params,
    span_create_params,
    span_search_params,
    span_update_params,
    span_upsert_batch_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder
from ..types.span import Span
from .._base_client import AsyncPaginator, make_request_options
from ..types.span_type import SpanType
from ..types.span_status import SpanStatus
from ..types.api_list_span import APIListSpan
from ..types.chat.sort_order import SortOrder
from ..types.span_create_param import SpanCreateParam

__all__ = ["SpansResource", "AsyncSpansResource"]


class SpansResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpansResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return SpansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpansResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return SpansResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | Omit = omit,
        application_interaction_id: str | Omit = omit,
        application_variant_id: str | Omit = omit,
        end_timestamp: Union[str, datetime] | Omit = omit,
        expected: Dict[str, object] | Omit = omit,
        group_id: str | Omit = omit,
        input: Dict[str, object] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        output: Dict[str, object] | Omit = omit,
        parent_id: str | Omit = omit,
        status: SpanStatus | Omit = omit,
        type: SpanType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Span:
        """
        Create Span

        Args:
          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span

          application_interaction_id: The optional application interaction ID this span belongs to

          application_variant_id: The optional application variant ID this span belongs to

          group_id: Reference to a group_id

          parent_id: Reference to a parent span_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/spans",
            body=maybe_transform(
                {
                    "name": name,
                    "start_timestamp": start_timestamp,
                    "trace_id": trace_id,
                    "id": id,
                    "application_interaction_id": application_interaction_id,
                    "application_variant_id": application_variant_id,
                    "end_timestamp": end_timestamp,
                    "expected": expected,
                    "group_id": group_id,
                    "input": input,
                    "metadata": metadata,
                    "output": output,
                    "parent_id": parent_id,
                    "status": status,
                    "type": type,
                },
                span_create_params.SpanCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def retrieve(
        self,
        span_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Span:
        """
        Get Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return self._get(
            path_template("/v5/spans/{span_id}", span_id=span_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def update(
        self,
        span_id: str,
        *,
        end_timestamp: Union[str, datetime] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        output: Dict[str, object] | Omit = omit,
        status: SpanStatus | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Span:
        """
        Update Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return self._patch(
            path_template("/v5/spans/{span_id}", span_id=span_id),
            body=maybe_transform(
                {
                    "end_timestamp": end_timestamp,
                    "metadata": metadata,
                    "name": name,
                    "output": output,
                    "status": status,
                },
                span_update_params.SpanUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    def batch(
        self,
        *,
        items: Iterable[SpanCreateParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIListSpan:
        """
        Create Spans in Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/spans/batch",
            body=maybe_transform({"items": items}, span_batch_params.SpanBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIListSpan,
        )

    def search(
        self,
        *,
        ending_before: str | Omit = omit,
        from_ts: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        to_ts: Union[str, datetime] | Omit = omit,
        acp_types: SequenceNotStr[str] | Omit = omit,
        agentex_agent_ids: SequenceNotStr[str] | Omit = omit,
        agentex_agent_names: SequenceNotStr[str] | Omit = omit,
        application_variant_ids: SequenceNotStr[str] | Omit = omit,
        assessment_types: SequenceNotStr[str] | Omit = omit,
        excluded_span_ids: SequenceNotStr[str] | Omit = omit,
        excluded_trace_ids: SequenceNotStr[str] | Omit = omit,
        extra_metadata: Dict[str, object] | Omit = omit,
        group_id: str | Omit = omit,
        max_duration_ms: int | Omit = omit,
        min_duration_ms: int | Omit = omit,
        names: SequenceNotStr[str] | Omit = omit,
        parents_only: bool | Omit = omit,
        search_texts: SequenceNotStr[str] | Omit = omit,
        span_ids: SequenceNotStr[str] | Omit = omit,
        statuses: List[SpanStatus] | Omit = omit,
        trace_ids: SequenceNotStr[str] | Omit = omit,
        types: List[SpanType] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[Span]:
        """
        Search and list spans

        Args:
          from_ts: The starting (oldest) timestamp in ISO format.

          to_ts: The ending (most recent) timestamp in ISO format.

          acp_types: Filter by ACP types

          agentex_agent_ids: Filter by Agentex agent IDs

          agentex_agent_names: Filter by Agentex agent names

          application_variant_ids: Filter by application variant IDs

          assessment_types: Filter spans by traces that have assessments of these types

          excluded_span_ids: List of span IDs to exclude from results

          excluded_trace_ids: List of trace IDs to exclude from results

          extra_metadata: Filter on custom metadata key-value pairs

          group_id: Filter by group ID

          max_duration_ms: Maximum span duration in milliseconds (inclusive)

          min_duration_ms: Minimum span duration in milliseconds (inclusive)

          names: Filter by trace/span name

          parents_only: Only fetch spans that are the top-level (ie. have no parent_id)

          search_texts: Free text search across span input and output fields. For exact trace ID lookup,
              use the `trace_ids` filter.

          span_ids: Filter by span IDs

          statuses: Filter on span status

          trace_ids: Filter by trace IDs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/spans/search",
            page=SyncCursorPage[Span],
            body=maybe_transform(
                {
                    "acp_types": acp_types,
                    "agentex_agent_ids": agentex_agent_ids,
                    "agentex_agent_names": agentex_agent_names,
                    "application_variant_ids": application_variant_ids,
                    "assessment_types": assessment_types,
                    "excluded_span_ids": excluded_span_ids,
                    "excluded_trace_ids": excluded_trace_ids,
                    "extra_metadata": extra_metadata,
                    "group_id": group_id,
                    "max_duration_ms": max_duration_ms,
                    "min_duration_ms": min_duration_ms,
                    "names": names,
                    "parents_only": parents_only,
                    "search_texts": search_texts,
                    "span_ids": span_ids,
                    "statuses": statuses,
                    "trace_ids": trace_ids,
                    "types": types,
                },
                span_search_params.SpanSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "from_ts": from_ts,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "to_ts": to_ts,
                    },
                    span_search_params.SpanSearchParams,
                ),
            ),
            model=Span,
            method="post",
        )

    def upsert_batch(
        self,
        *,
        items: Iterable[SpanCreateParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIListSpan:
        """
        Upsert Spans in Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            "/v5/spans/batch",
            body=maybe_transform({"items": items}, span_upsert_batch_params.SpanUpsertBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIListSpan,
        )


class AsyncSpansResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpansResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncSpansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpansResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncSpansResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        start_timestamp: Union[str, datetime],
        trace_id: str,
        id: str | Omit = omit,
        application_interaction_id: str | Omit = omit,
        application_variant_id: str | Omit = omit,
        end_timestamp: Union[str, datetime] | Omit = omit,
        expected: Dict[str, object] | Omit = omit,
        group_id: str | Omit = omit,
        input: Dict[str, object] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        output: Dict[str, object] | Omit = omit,
        parent_id: str | Omit = omit,
        status: SpanStatus | Omit = omit,
        type: SpanType | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Span:
        """
        Create Span

        Args:
          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span

          application_interaction_id: The optional application interaction ID this span belongs to

          application_variant_id: The optional application variant ID this span belongs to

          group_id: Reference to a group_id

          parent_id: Reference to a parent span_id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/spans",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "start_timestamp": start_timestamp,
                    "trace_id": trace_id,
                    "id": id,
                    "application_interaction_id": application_interaction_id,
                    "application_variant_id": application_variant_id,
                    "end_timestamp": end_timestamp,
                    "expected": expected,
                    "group_id": group_id,
                    "input": input,
                    "metadata": metadata,
                    "output": output,
                    "parent_id": parent_id,
                    "status": status,
                    "type": type,
                },
                span_create_params.SpanCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    async def retrieve(
        self,
        span_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Span:
        """
        Get Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return await self._get(
            path_template("/v5/spans/{span_id}", span_id=span_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    async def update(
        self,
        span_id: str,
        *,
        end_timestamp: Union[str, datetime] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        output: Dict[str, object] | Omit = omit,
        status: SpanStatus | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Span:
        """
        Update Span

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_id:
            raise ValueError(f"Expected a non-empty value for `span_id` but received {span_id!r}")
        return await self._patch(
            path_template("/v5/spans/{span_id}", span_id=span_id),
            body=await async_maybe_transform(
                {
                    "end_timestamp": end_timestamp,
                    "metadata": metadata,
                    "name": name,
                    "output": output,
                    "status": status,
                },
                span_update_params.SpanUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Span,
        )

    async def batch(
        self,
        *,
        items: Iterable[SpanCreateParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIListSpan:
        """
        Create Spans in Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/spans/batch",
            body=await async_maybe_transform({"items": items}, span_batch_params.SpanBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIListSpan,
        )

    def search(
        self,
        *,
        ending_before: str | Omit = omit,
        from_ts: Union[str, datetime] | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        to_ts: Union[str, datetime] | Omit = omit,
        acp_types: SequenceNotStr[str] | Omit = omit,
        agentex_agent_ids: SequenceNotStr[str] | Omit = omit,
        agentex_agent_names: SequenceNotStr[str] | Omit = omit,
        application_variant_ids: SequenceNotStr[str] | Omit = omit,
        assessment_types: SequenceNotStr[str] | Omit = omit,
        excluded_span_ids: SequenceNotStr[str] | Omit = omit,
        excluded_trace_ids: SequenceNotStr[str] | Omit = omit,
        extra_metadata: Dict[str, object] | Omit = omit,
        group_id: str | Omit = omit,
        max_duration_ms: int | Omit = omit,
        min_duration_ms: int | Omit = omit,
        names: SequenceNotStr[str] | Omit = omit,
        parents_only: bool | Omit = omit,
        search_texts: SequenceNotStr[str] | Omit = omit,
        span_ids: SequenceNotStr[str] | Omit = omit,
        statuses: List[SpanStatus] | Omit = omit,
        trace_ids: SequenceNotStr[str] | Omit = omit,
        types: List[SpanType] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Span, AsyncCursorPage[Span]]:
        """
        Search and list spans

        Args:
          from_ts: The starting (oldest) timestamp in ISO format.

          to_ts: The ending (most recent) timestamp in ISO format.

          acp_types: Filter by ACP types

          agentex_agent_ids: Filter by Agentex agent IDs

          agentex_agent_names: Filter by Agentex agent names

          application_variant_ids: Filter by application variant IDs

          assessment_types: Filter spans by traces that have assessments of these types

          excluded_span_ids: List of span IDs to exclude from results

          excluded_trace_ids: List of trace IDs to exclude from results

          extra_metadata: Filter on custom metadata key-value pairs

          group_id: Filter by group ID

          max_duration_ms: Maximum span duration in milliseconds (inclusive)

          min_duration_ms: Minimum span duration in milliseconds (inclusive)

          names: Filter by trace/span name

          parents_only: Only fetch spans that are the top-level (ie. have no parent_id)

          search_texts: Free text search across span input and output fields. For exact trace ID lookup,
              use the `trace_ids` filter.

          span_ids: Filter by span IDs

          statuses: Filter on span status

          trace_ids: Filter by trace IDs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/spans/search",
            page=AsyncCursorPage[Span],
            body=maybe_transform(
                {
                    "acp_types": acp_types,
                    "agentex_agent_ids": agentex_agent_ids,
                    "agentex_agent_names": agentex_agent_names,
                    "application_variant_ids": application_variant_ids,
                    "assessment_types": assessment_types,
                    "excluded_span_ids": excluded_span_ids,
                    "excluded_trace_ids": excluded_trace_ids,
                    "extra_metadata": extra_metadata,
                    "group_id": group_id,
                    "max_duration_ms": max_duration_ms,
                    "min_duration_ms": min_duration_ms,
                    "names": names,
                    "parents_only": parents_only,
                    "search_texts": search_texts,
                    "span_ids": span_ids,
                    "statuses": statuses,
                    "trace_ids": trace_ids,
                    "types": types,
                },
                span_search_params.SpanSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "from_ts": from_ts,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "to_ts": to_ts,
                    },
                    span_search_params.SpanSearchParams,
                ),
            ),
            model=Span,
            method="post",
        )

    async def upsert_batch(
        self,
        *,
        items: Iterable[SpanCreateParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> APIListSpan:
        """
        Upsert Spans in Batch

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            "/v5/spans/batch",
            body=await async_maybe_transform({"items": items}, span_upsert_batch_params.SpanUpsertBatchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIListSpan,
        )


class SpansResourceWithRawResponse:
    def __init__(self, spans: SpansResource) -> None:
        self._spans = spans

        self.create = to_raw_response_wrapper(
            spans.create,
        )
        self.retrieve = to_raw_response_wrapper(
            spans.retrieve,
        )
        self.update = to_raw_response_wrapper(
            spans.update,
        )
        self.batch = to_raw_response_wrapper(
            spans.batch,
        )
        self.search = to_raw_response_wrapper(
            spans.search,
        )
        self.upsert_batch = to_raw_response_wrapper(
            spans.upsert_batch,
        )


class AsyncSpansResourceWithRawResponse:
    def __init__(self, spans: AsyncSpansResource) -> None:
        self._spans = spans

        self.create = async_to_raw_response_wrapper(
            spans.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            spans.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            spans.update,
        )
        self.batch = async_to_raw_response_wrapper(
            spans.batch,
        )
        self.search = async_to_raw_response_wrapper(
            spans.search,
        )
        self.upsert_batch = async_to_raw_response_wrapper(
            spans.upsert_batch,
        )


class SpansResourceWithStreamingResponse:
    def __init__(self, spans: SpansResource) -> None:
        self._spans = spans

        self.create = to_streamed_response_wrapper(
            spans.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            spans.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            spans.update,
        )
        self.batch = to_streamed_response_wrapper(
            spans.batch,
        )
        self.search = to_streamed_response_wrapper(
            spans.search,
        )
        self.upsert_batch = to_streamed_response_wrapper(
            spans.upsert_batch,
        )


class AsyncSpansResourceWithStreamingResponse:
    def __init__(self, spans: AsyncSpansResource) -> None:
        self._spans = spans

        self.create = async_to_streamed_response_wrapper(
            spans.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            spans.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            spans.update,
        )
        self.batch = async_to_streamed_response_wrapper(
            spans.batch,
        )
        self.search = async_to_streamed_response_wrapper(
            spans.search,
        )
        self.upsert_batch = async_to_streamed_response_wrapper(
            spans.upsert_batch,
        )
