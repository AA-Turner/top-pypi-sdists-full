# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
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
from .._utils import path_template, maybe_transform, strip_not_given, async_maybe_transform
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
        obs_span_id: str | Omit = omit,
        obs_trace_id: str | Omit = omit,
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
        Create a single span and return the persisted span.

        Use this for one-off span ingestion; to write many spans in one request use POST
        /v5/spans/batch. When `id` is omitted the server generates a UUID. Depending on
        per-account server configuration the span is persisted to the legacy trace
        store, to the tracing service, or both. `end_timestamp` must not precede
        `start_timestamp`, which is rejected with a 422. When the tracing service is the
        primary store, its 400, 413 and 422 rejections keep that status and detail, as
        does a 403 when the request carried its own API key, and every other failure
        returns a 503 with a Retry-After header. A span whose parent belongs to another
        trace is rejected with 409 before either store is written. The parent is looked
        up in Postgres, so that check ends once the account's spans stop being written
        there. Which writes the tracing service rejects depends in part on its storage
        engine: on Postgres deployments a NUL byte or invalid UTF-8 inside `trace_id`,
        `id`, `parent_id` or `group_id` rejects the span with a 400 naming the field,
        because replacing the byte would change the identity the response echoes; a NUL
        byte or invalid UTF-8 in any other field is replaced with U+FFFD and the span is
        persisted. ClickHouse deployments store the bytes verbatim.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

        Args:
          start_timestamp: When the span started. With trace_id and id it forms the span's storage
              identity, so a span re-sent with a start_timestamp on another UTC day is stored
              as a second row that the store never collapses. Get span and trace detail return
              the newest version. Search returns the newest version whose start_timestamp
              falls in the queried window. Export, metrics and facets count both rows until
              the trace is deleted and re-sent.

          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span, at most 256 bytes. A value longer than 256 characters is
              refused here with a 422 before it is forwarded; a value within that count whose
              UTF-8 form exceeds 256 bytes is refused with a 400 naming the field once the
              tracing service is the account's primary store, and accepted for accounts still
              written primarily to the legacy trace store.

          application_interaction_id: The optional application interaction ID this span belongs to

          application_variant_id: The optional application variant ID this span belongs to

          group_id: Reference to a group_id, at most 256 bytes. A value longer than 256 characters
              is refused here with a 422 before it is forwarded; a value within that count
              whose UTF-8 form exceeds 256 bytes is refused with a 400 naming the field once
              the tracing service is the account's primary store, and accepted for accounts
              still written primarily to the legacy trace store.

          obs_span_id: W3C span id (16 lowercase hex chars) of the observability span this span
              executed in. Requires obs_trace_id.

          obs_trace_id: W3C trace id (32 lowercase hex chars) of the observability trace this span
              executed in, for correlating a business span with the infrastructure work it
              caused. Stored only by the sgp-traces service, so accounts still served by the
              legacy store accept the field and read it back as null.

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
                    "obs_span_id": obs_span_id,
                    "obs_trace_id": obs_trace_id,
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

    @typing_extensions.deprecated("deprecated")
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
        Retrieve a single span by its id.

        The span is read from the legacy trace store or, for accounts migrated to the
        tracing service, from that service — with automatic fallback to the legacy trace
        store on error unless the account is in strict mode, where a tracing-service
        failure surfaces as a 503. Access is authorized against the span's parent trace,
        so a span in a trace the caller cannot read is rejected; an unknown id
        returns 404. `input_tokens` and `output_tokens` carry the token usage the span's
        producer reported at ingest, and are absent both for a span that reported none
        and for every span served from the legacy trace store, which keeps no token
        counts.

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
        Partially update a span's mutable fields and return the updated span.

        Only the provided fields among name, end timestamp, output, metadata, and status
        are changed. This endpoint is available only for accounts still served solely by
        the legacy trace store: once an account begins dual-writing to the tracing
        service — which is upsert-only and has no partial-update operation — PATCH
        returns 501 and PUT /v5/spans/batch must be used instead. Updates are authorized
        against the span's parent trace, and an unknown id returns 404.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

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
        Create multiple spans (up to 1000) in a single request and return the created
        spans.

        Prefer this over repeated POST /v5/spans calls when ingesting many spans at
        once; use PUT /v5/spans/batch instead when a span with the same `id` may already
        exist, since this endpoint inserts new spans rather than overwriting. A batch
        larger than 1000 spans is rejected with a validation error. Each item follows
        the same id-generation and per-account dual-write rules as the single-span
        create, including that `end_timestamp` must not precede `start_timestamp`, which
        rejects the request with a 422. When the tracing service is the primary store,
        its 400, 413 and 422 rejections keep that status and detail, as does a 403 when
        the request carried its own API key, and every other failure returns a 503 with
        a Retry-After header. A batch that forms a cycle, or a span whose parent belongs
        to another trace, is rejected with 409 before either store is written. A parent
        outside the batch is looked up in Postgres, so that part of the check ends once
        the account's spans stop being written there. Postgres rejects an `id` that
        already exists, while the tracing service treats the write as an upsert. Which
        writes the tracing service rejects depends in part on its storage engine: on
        Postgres deployments a NUL byte or invalid UTF-8 inside `trace_id`, `id`,
        `parent_id` or `group_id` fails the whole batch with a 400 naming the field,
        because replacing the byte would change the identity the response echoes; a NUL
        byte or invalid UTF-8 in any other field is replaced with U+FFFD and the span is
        persisted. ClickHouse deployments store the bytes verbatim.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

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
        allow_partial_results: bool | Omit = omit,
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
        excluded_spans: Iterable[span_search_params.ExcludedSpan] | Omit = omit,
        excluded_trace_ids: SequenceNotStr[str] | Omit = omit,
        extra_metadata: Dict[str, object] | Omit = omit,
        group_id: str | Omit = omit,
        max_duration_ms: int | Omit = omit,
        min_duration_ms: int | Omit = omit,
        names: SequenceNotStr[str] | Omit = omit,
        obs_span_ids: SequenceNotStr[str] | Omit = omit,
        obs_trace_ids: SequenceNotStr[str] | Omit = omit,
        parent_ids: SequenceNotStr[str] | Omit = omit,
        parents_only: bool | Omit = omit,
        search_texts: SequenceNotStr[str] | Omit = omit,
        span_ids: SequenceNotStr[str] | Omit = omit,
        spans: Iterable[span_search_params.Span] | Omit = omit,
        statuses: List[SpanStatus] | Omit = omit,
        trace_ids: SequenceNotStr[str] | Omit = omit,
        types: List[SpanType] | Omit = omit,
        x_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[Span]:
        """
        Search and list spans matching a set of filters, returning a keyset-paginated
        page.

        Filters in the request body include trace and span ids, names, statuses, types,
        free-text search, metadata, duration bounds, and more, scoped to an optional
        time window. Results are keyset-paginated on indexed columns rather than
        offset-paginated, and `total` is not computed (it is always 0); use the
        pagination cursors to page through results. Reads route to the legacy trace
        store or the tracing service per account (with fallback to the legacy trace
        store outside strict mode), and results are narrowed to traces the caller is
        authorized to read — a filter that resolves to no authorized traces yields an
        empty page rather than an error. A reversed time window (`from_ts` after
        `to_ts`) is rejected with 422, as is a request whose combined `trace_ids`,
        `span_ids`, `excluded_span_ids`, `excluded_trace_ids`, and `parent_ids` count
        exceeds 10000. `sort_by` accepts `start_timestamp`, `duration_ms`,
        `input_tokens` and `output_tokens`; the token counts are read from usage
        reported at ingest, and a span whose producer reported none sorts as zero, so it
        lands last descending and first ascending. The two token sorts are rejected for
        an account still served by the legacy trace store, which keeps no token count to
        order by. Any other unsupported sort falls back to timestamp order there. Spans
        sharing a sort key are ordered by `trace_id` and `id` bytewise on both
        tracing-service engines. Text search tokenization, indexed-prefix, word-length,
        locale and metadata-bytes behavior differs between Postgres and ClickHouse
        deployments of the tracing service as the `search_texts` field describes.

        `x-project-id` narrows the result to traces whose root span carries that
        project, when `PROJECT_SCOPED_SPAN_LISTING` is on for the account, on either
        store.

        Args:
          allow_partial_results: Return however many spans fit the server byte budget instead of a 400
              SEARCH_RESULT_TOO_LARGE, reporting the rest through has_more plus next_cursor
              going forward or prev_cursor going back. A search that spends its time budget
              before the page fills also returns what it found, with search_status partial,
              searched_through and a next_cursor that resumes from there. Send it only if the
              client reads has_more, because under it a page shorter than limit no longer
              means the end of the list. Honored by the tracing service on either of its
              storage engines. Accounts still served by the legacy trace store ignore it and
              page by item count, where a short page still means the end of the list.

          from_ts: The starting (oldest) timestamp in ISO format.

          to_ts: The ending (most recent) timestamp in ISO format.

          acp_types: Filter by ACP types

          agentex_agent_ids: Filter by Agentex agent IDs

          agentex_agent_names: Filter by Agentex agent names

          application_variant_ids: Filter by application variant IDs

          assessment_types: Filter to spans that have at least one assessment of these types

          excluded_span_ids: List of span IDs to exclude from results

          excluded_spans: List of (trace_id, span_id) identities to exclude from results. Unlike
              excluded_span_ids, a pair never excludes a same-id span from another trace.
              Takes precedence over excluded_span_ids when both are set.

          excluded_trace_ids: List of trace IDs to exclude from results

          extra_metadata: Filter on custom metadata: each key must equal its value, or any value of an
              array, and keys are ANDed. On the ClickHouse read path `$or` and `$and` also
              compose nested groups of predicates. On Postgres a `$`-prefixed key is an
              ordinary metadata key matched literally. Array values match element-wise; a
              negative zero inside an array equals zero on Postgres-served accounts and not on
              ClickHouse-served ones.

          group_id: Filter by group ID

          max_duration_ms: Maximum span duration in milliseconds (inclusive). Matched on completed
              duration, so a span with no end time is never returned: fetch it by its own id
              or in its trace's span list.

          min_duration_ms: Minimum span duration in milliseconds (inclusive). Matched on completed
              duration, so a span with no end time is not reliably returned: fetch it by its
              own id or in its trace's span list.

          names: Filter by trace/span name

          obs_span_ids: Filter to the business spans that executed in any of these observability spans.
              Each id must be 16 lowercase hex characters. A W3C span id is unique per trace
              only, so combine with obs_trace_ids for exact identity, the same looseness
              span_ids carries versus the spans pair filter. ANDs with obs_trace_ids when both
              are set. Served only by the sgp-traces service, so a request using this filter
              against an account still on the legacy store returns 422 rather than silently
              ignoring it.

          obs_trace_ids: Filter to the business spans that executed in any of these observability traces
              (the obs-to-business reverse lookup). Each id must be 32 lowercase hex
              characters. Served only by the sgp-traces service, so a request using this
              filter against an account still on the legacy store returns 422 rather than
              silently ignoring it.

          parent_ids: Filter to the direct children of any of these parent span IDs

          parents_only: Only fetch spans that are the top-level (ie. have no parent_id)

          search_texts: Case-insensitive text search across span name, input, output, and metadata. A
              single-word term of ASCII letters and digits matches as a whole word in input,
              output, and metadata, and as a substring of the name. A term of up to 8 such
              words matches as a contiguous phrase whose words each appear as whole words. All
              other terms (punctuated, non-ASCII, longer) match as substrings, where mid-word
              fragments match and an inflected form such as a plural matches only where it
              appears literally. Wrapping a term in double quotes makes it a phrase: the
              quotes mark the phrase and are never matched, a backslash escapes a quote or a
              backslash inside them, the phrase must appear contiguously inside one searched
              value (the input, the output, or the metadata), a phrase of up to 8 ASCII
              letter-and-digit words additionally requires each of those words to appear there
              as a whole word, and a UUID-shaped phrase stays a text search. A term whose
              quote is unterminated or left unescaped mid-term is matched literally, quotes
              included. Multiple terms are ANDed, and UUID-shaped terms match trace IDs
              instead. A span must match every non-UUID term, and each term may match any of
              the searched fields. UUID matches are ORed onto the text match. Each term must
              be at least 2 characters, measured between the quotes and ignoring outer
              whitespace for a phrase, and at most 10 terms are supported. For exact trace ID
              lookup, use the `trace_ids` filter. The tracing service runs on either
              ClickHouse or Postgres, and the two engines match differently. On Postgres
              deployments the whole-word match uses the simple text-search parser, which keeps
              hosts, e-mail addresses, file paths, version strings, hyphenated compounds, URLs
              and query strings as single words (https://x.com/path?q=1 yields x.com/path?q=1,
              x.com and /path?q=1, never path, q or 1; user@example.com and v1.2.3 are one
              word each; gpt-4o yields the compound and its parts), whereas ClickHouse
              deployments split on every non-alphanumeric ASCII byte. A single word inside
              such a value is a whole-word hit on ClickHouse and a miss on Postgres; the
              substring forms behave identically on both. On Postgres deployments a value over
              80000 bytes has only its first 20000 characters indexed for whole-word matching;
              text past that is reachable only by the substring forms. Words longer than 2047
              bytes are matched as substrings, never as whole words. Case folding of non-ASCII
              text follows the database's LC_CTYPE on Postgres deployments, for the whole-word
              index, the quoted-phrase and substring forms and the word-boundary check alike;
              under a C-locale database non-ASCII letters are not folded. ASCII folds
              everywhere. Input and output behave identically on both engines. A
              substring-form term, or a text-filtered metrics request, reads every row of the
              time window that survives the other filters. A term that matches too many rows
              in the window is refused by the tracing service as QUERY_TOO_BROAD, at an
              engine-specific threshold; whether this API relays that refusal as a 400 or
              answers the page from the legacy trace store follows its read-routing rules, and
              an export's refusal is reported as the failed export's reason on the export
              status, not on the POST. On Postgres deployments each term is counted on its
              own, in every class (whole word, phrase and substring alike) and on every read
              that carries text, and is refused when it alone matches more than 50000 rows of
              the window that survive the other filters, with or without assessment_types. On
              ClickHouse deployments the refusal is the candidate-set cap, a
              deployment-configured limit counted over the matches of all terms together: a
              search page bounds its candidates to the page, so there the cap is a backstop
              rather than a limit a common term meets; metrics and by-span resolve every match
              and can trip it; and an export runs under its own 2000000-row set cap on every
              request, assessment_types included. Accounts still served by the legacy trace
              store match differently until migrated: every term matches as stemmed whole
              words (so inflected forms match and multi-word terms match word-adjacent), only
              input and output are searched, the 2-character minimum is not enforced, quoting
              a term changes nothing (the quotes are stripped and a multi-word term is already
              matched word-adjacent), and characters like `:`, `|`, or `!` inside a term may
              be interpreted as query operators or cause an error.

          span_ids: Filter by span IDs

          spans: Filter by exact (trace_id, span_id) identity. Unlike span_ids, a pair never
              matches a same-id span from another trace. ANDs with span_ids when both are set.

          statuses: Filter on span status

          trace_ids: Filter by trace IDs. The combined count of trace_ids, span_ids,
              excluded_span_ids, excluded_trace_ids, parent_ids, and (trace_id, span_id) pairs
              (each pair counting 2) may not exceed 10000. A request over that returns 422.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-project-id": x_project_id}), **(extra_headers or {})}
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
                    "excluded_spans": excluded_spans,
                    "excluded_trace_ids": excluded_trace_ids,
                    "extra_metadata": extra_metadata,
                    "group_id": group_id,
                    "max_duration_ms": max_duration_ms,
                    "min_duration_ms": min_duration_ms,
                    "names": names,
                    "obs_span_ids": obs_span_ids,
                    "obs_trace_ids": obs_trace_ids,
                    "parent_ids": parent_ids,
                    "parents_only": parents_only,
                    "search_texts": search_texts,
                    "span_ids": span_ids,
                    "spans": spans,
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
                        "allow_partial_results": allow_partial_results,
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
        Insert or replace multiple spans (up to 1000) in a single request.

        Use this for idempotent ingestion when spans may already exist, unlike POST
        /v5/spans/batch, which only inserts. Items without an `id` are assigned a
        generated UUID. The legacy trace store treats `id` as global and collapses
        repeated `id`s to the last occurrence. The tracing service keys spans by
        `trace_id` and `id`; it retains cross-trace ID collisions, and for a repeated
        pair keeps a completed span over an in-progress one, otherwise the later
        occurrence wins. In dual-write phases each store applies its own rule, and the
        primary store determines the returned list. A batch larger than 1000 spans is
        rejected with a validation error, as is any item whose `end_timestamp` precedes
        its `start_timestamp`, which returns a 422. When the tracing service is the
        primary store, its 400, 413 and 422 rejections keep that status and detail, as
        does a 403 when the request carried its own API key, and every other failure
        returns a 503 with a Retry-After header. A batch that forms a cycle, or a span
        whose parent belongs to another trace, is rejected with 409 before either store
        is written. A parent outside the batch is looked up in Postgres, so that part of
        the check ends once the account's spans stop being written there. Which writes
        the tracing service rejects depends in part on its storage engine: on Postgres
        deployments a NUL byte or invalid UTF-8 inside `trace_id`, `id`, `parent_id` or
        `group_id` fails the whole batch with a 400 naming the field, because replacing
        the byte would change the identity the response echoes; a NUL byte or invalid
        UTF-8 in any other field is replaced with U+FFFD and the span is persisted.
        ClickHouse deployments store the bytes verbatim.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

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
        obs_span_id: str | Omit = omit,
        obs_trace_id: str | Omit = omit,
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
        Create a single span and return the persisted span.

        Use this for one-off span ingestion; to write many spans in one request use POST
        /v5/spans/batch. When `id` is omitted the server generates a UUID. Depending on
        per-account server configuration the span is persisted to the legacy trace
        store, to the tracing service, or both. `end_timestamp` must not precede
        `start_timestamp`, which is rejected with a 422. When the tracing service is the
        primary store, its 400, 413 and 422 rejections keep that status and detail, as
        does a 403 when the request carried its own API key, and every other failure
        returns a 503 with a Retry-After header. A span whose parent belongs to another
        trace is rejected with 409 before either store is written. The parent is looked
        up in Postgres, so that check ends once the account's spans stop being written
        there. Which writes the tracing service rejects depends in part on its storage
        engine: on Postgres deployments a NUL byte or invalid UTF-8 inside `trace_id`,
        `id`, `parent_id` or `group_id` rejects the span with a 400 naming the field,
        because replacing the byte would change the identity the response echoes; a NUL
        byte or invalid UTF-8 in any other field is replaced with U+FFFD and the span is
        persisted. ClickHouse deployments store the bytes verbatim.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

        Args:
          start_timestamp: When the span started. With trace_id and id it forms the span's storage
              identity, so a span re-sent with a start_timestamp on another UTC day is stored
              as a second row that the store never collapses. Get span and trace detail return
              the newest version. Search returns the newest version whose start_timestamp
              falls in the queried window. Export, metrics and facets count both rows until
              the trace is deleted and re-sent.

          trace_id: id for grouping traces together, uuid is recommended

          id: The id of the span, at most 256 bytes. A value longer than 256 characters is
              refused here with a 422 before it is forwarded; a value within that count whose
              UTF-8 form exceeds 256 bytes is refused with a 400 naming the field once the
              tracing service is the account's primary store, and accepted for accounts still
              written primarily to the legacy trace store.

          application_interaction_id: The optional application interaction ID this span belongs to

          application_variant_id: The optional application variant ID this span belongs to

          group_id: Reference to a group_id, at most 256 bytes. A value longer than 256 characters
              is refused here with a 422 before it is forwarded; a value within that count
              whose UTF-8 form exceeds 256 bytes is refused with a 400 naming the field once
              the tracing service is the account's primary store, and accepted for accounts
              still written primarily to the legacy trace store.

          obs_span_id: W3C span id (16 lowercase hex chars) of the observability span this span
              executed in. Requires obs_trace_id.

          obs_trace_id: W3C trace id (32 lowercase hex chars) of the observability trace this span
              executed in, for correlating a business span with the infrastructure work it
              caused. Stored only by the sgp-traces service, so accounts still served by the
              legacy store accept the field and read it back as null.

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
                    "obs_span_id": obs_span_id,
                    "obs_trace_id": obs_trace_id,
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

    @typing_extensions.deprecated("deprecated")
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
        Retrieve a single span by its id.

        The span is read from the legacy trace store or, for accounts migrated to the
        tracing service, from that service — with automatic fallback to the legacy trace
        store on error unless the account is in strict mode, where a tracing-service
        failure surfaces as a 503. Access is authorized against the span's parent trace,
        so a span in a trace the caller cannot read is rejected; an unknown id
        returns 404. `input_tokens` and `output_tokens` carry the token usage the span's
        producer reported at ingest, and are absent both for a span that reported none
        and for every span served from the legacy trace store, which keeps no token
        counts.

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
        Partially update a span's mutable fields and return the updated span.

        Only the provided fields among name, end timestamp, output, metadata, and status
        are changed. This endpoint is available only for accounts still served solely by
        the legacy trace store: once an account begins dual-writing to the tracing
        service — which is upsert-only and has no partial-update operation — PATCH
        returns 501 and PUT /v5/spans/batch must be used instead. Updates are authorized
        against the span's parent trace, and an unknown id returns 404.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

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
        Create multiple spans (up to 1000) in a single request and return the created
        spans.

        Prefer this over repeated POST /v5/spans calls when ingesting many spans at
        once; use PUT /v5/spans/batch instead when a span with the same `id` may already
        exist, since this endpoint inserts new spans rather than overwriting. A batch
        larger than 1000 spans is rejected with a validation error. Each item follows
        the same id-generation and per-account dual-write rules as the single-span
        create, including that `end_timestamp` must not precede `start_timestamp`, which
        rejects the request with a 422. When the tracing service is the primary store,
        its 400, 413 and 422 rejections keep that status and detail, as does a 403 when
        the request carried its own API key, and every other failure returns a 503 with
        a Retry-After header. A batch that forms a cycle, or a span whose parent belongs
        to another trace, is rejected with 409 before either store is written. A parent
        outside the batch is looked up in Postgres, so that part of the check ends once
        the account's spans stop being written there. Postgres rejects an `id` that
        already exists, while the tracing service treats the write as an upsert. Which
        writes the tracing service rejects depends in part on its storage engine: on
        Postgres deployments a NUL byte or invalid UTF-8 inside `trace_id`, `id`,
        `parent_id` or `group_id` fails the whole batch with a 400 naming the field,
        because replacing the byte would change the identity the response echoes; a NUL
        byte or invalid UTF-8 in any other field is replaced with U+FFFD and the span is
        persisted. ClickHouse deployments store the bytes verbatim.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

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
        allow_partial_results: bool | Omit = omit,
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
        excluded_spans: Iterable[span_search_params.ExcludedSpan] | Omit = omit,
        excluded_trace_ids: SequenceNotStr[str] | Omit = omit,
        extra_metadata: Dict[str, object] | Omit = omit,
        group_id: str | Omit = omit,
        max_duration_ms: int | Omit = omit,
        min_duration_ms: int | Omit = omit,
        names: SequenceNotStr[str] | Omit = omit,
        obs_span_ids: SequenceNotStr[str] | Omit = omit,
        obs_trace_ids: SequenceNotStr[str] | Omit = omit,
        parent_ids: SequenceNotStr[str] | Omit = omit,
        parents_only: bool | Omit = omit,
        search_texts: SequenceNotStr[str] | Omit = omit,
        span_ids: SequenceNotStr[str] | Omit = omit,
        spans: Iterable[span_search_params.Span] | Omit = omit,
        statuses: List[SpanStatus] | Omit = omit,
        trace_ids: SequenceNotStr[str] | Omit = omit,
        types: List[SpanType] | Omit = omit,
        x_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Span, AsyncCursorPage[Span]]:
        """
        Search and list spans matching a set of filters, returning a keyset-paginated
        page.

        Filters in the request body include trace and span ids, names, statuses, types,
        free-text search, metadata, duration bounds, and more, scoped to an optional
        time window. Results are keyset-paginated on indexed columns rather than
        offset-paginated, and `total` is not computed (it is always 0); use the
        pagination cursors to page through results. Reads route to the legacy trace
        store or the tracing service per account (with fallback to the legacy trace
        store outside strict mode), and results are narrowed to traces the caller is
        authorized to read — a filter that resolves to no authorized traces yields an
        empty page rather than an error. A reversed time window (`from_ts` after
        `to_ts`) is rejected with 422, as is a request whose combined `trace_ids`,
        `span_ids`, `excluded_span_ids`, `excluded_trace_ids`, and `parent_ids` count
        exceeds 10000. `sort_by` accepts `start_timestamp`, `duration_ms`,
        `input_tokens` and `output_tokens`; the token counts are read from usage
        reported at ingest, and a span whose producer reported none sorts as zero, so it
        lands last descending and first ascending. The two token sorts are rejected for
        an account still served by the legacy trace store, which keeps no token count to
        order by. Any other unsupported sort falls back to timestamp order there. Spans
        sharing a sort key are ordered by `trace_id` and `id` bytewise on both
        tracing-service engines. Text search tokenization, indexed-prefix, word-length,
        locale and metadata-bytes behavior differs between Postgres and ClickHouse
        deployments of the tracing service as the `search_texts` field describes.

        `x-project-id` narrows the result to traces whose root span carries that
        project, when `PROJECT_SCOPED_SPAN_LISTING` is on for the account, on either
        store.

        Args:
          allow_partial_results: Return however many spans fit the server byte budget instead of a 400
              SEARCH_RESULT_TOO_LARGE, reporting the rest through has_more plus next_cursor
              going forward or prev_cursor going back. A search that spends its time budget
              before the page fills also returns what it found, with search_status partial,
              searched_through and a next_cursor that resumes from there. Send it only if the
              client reads has_more, because under it a page shorter than limit no longer
              means the end of the list. Honored by the tracing service on either of its
              storage engines. Accounts still served by the legacy trace store ignore it and
              page by item count, where a short page still means the end of the list.

          from_ts: The starting (oldest) timestamp in ISO format.

          to_ts: The ending (most recent) timestamp in ISO format.

          acp_types: Filter by ACP types

          agentex_agent_ids: Filter by Agentex agent IDs

          agentex_agent_names: Filter by Agentex agent names

          application_variant_ids: Filter by application variant IDs

          assessment_types: Filter to spans that have at least one assessment of these types

          excluded_span_ids: List of span IDs to exclude from results

          excluded_spans: List of (trace_id, span_id) identities to exclude from results. Unlike
              excluded_span_ids, a pair never excludes a same-id span from another trace.
              Takes precedence over excluded_span_ids when both are set.

          excluded_trace_ids: List of trace IDs to exclude from results

          extra_metadata: Filter on custom metadata: each key must equal its value, or any value of an
              array, and keys are ANDed. On the ClickHouse read path `$or` and `$and` also
              compose nested groups of predicates. On Postgres a `$`-prefixed key is an
              ordinary metadata key matched literally. Array values match element-wise; a
              negative zero inside an array equals zero on Postgres-served accounts and not on
              ClickHouse-served ones.

          group_id: Filter by group ID

          max_duration_ms: Maximum span duration in milliseconds (inclusive). Matched on completed
              duration, so a span with no end time is never returned: fetch it by its own id
              or in its trace's span list.

          min_duration_ms: Minimum span duration in milliseconds (inclusive). Matched on completed
              duration, so a span with no end time is not reliably returned: fetch it by its
              own id or in its trace's span list.

          names: Filter by trace/span name

          obs_span_ids: Filter to the business spans that executed in any of these observability spans.
              Each id must be 16 lowercase hex characters. A W3C span id is unique per trace
              only, so combine with obs_trace_ids for exact identity, the same looseness
              span_ids carries versus the spans pair filter. ANDs with obs_trace_ids when both
              are set. Served only by the sgp-traces service, so a request using this filter
              against an account still on the legacy store returns 422 rather than silently
              ignoring it.

          obs_trace_ids: Filter to the business spans that executed in any of these observability traces
              (the obs-to-business reverse lookup). Each id must be 32 lowercase hex
              characters. Served only by the sgp-traces service, so a request using this
              filter against an account still on the legacy store returns 422 rather than
              silently ignoring it.

          parent_ids: Filter to the direct children of any of these parent span IDs

          parents_only: Only fetch spans that are the top-level (ie. have no parent_id)

          search_texts: Case-insensitive text search across span name, input, output, and metadata. A
              single-word term of ASCII letters and digits matches as a whole word in input,
              output, and metadata, and as a substring of the name. A term of up to 8 such
              words matches as a contiguous phrase whose words each appear as whole words. All
              other terms (punctuated, non-ASCII, longer) match as substrings, where mid-word
              fragments match and an inflected form such as a plural matches only where it
              appears literally. Wrapping a term in double quotes makes it a phrase: the
              quotes mark the phrase and are never matched, a backslash escapes a quote or a
              backslash inside them, the phrase must appear contiguously inside one searched
              value (the input, the output, or the metadata), a phrase of up to 8 ASCII
              letter-and-digit words additionally requires each of those words to appear there
              as a whole word, and a UUID-shaped phrase stays a text search. A term whose
              quote is unterminated or left unescaped mid-term is matched literally, quotes
              included. Multiple terms are ANDed, and UUID-shaped terms match trace IDs
              instead. A span must match every non-UUID term, and each term may match any of
              the searched fields. UUID matches are ORed onto the text match. Each term must
              be at least 2 characters, measured between the quotes and ignoring outer
              whitespace for a phrase, and at most 10 terms are supported. For exact trace ID
              lookup, use the `trace_ids` filter. The tracing service runs on either
              ClickHouse or Postgres, and the two engines match differently. On Postgres
              deployments the whole-word match uses the simple text-search parser, which keeps
              hosts, e-mail addresses, file paths, version strings, hyphenated compounds, URLs
              and query strings as single words (https://x.com/path?q=1 yields x.com/path?q=1,
              x.com and /path?q=1, never path, q or 1; user@example.com and v1.2.3 are one
              word each; gpt-4o yields the compound and its parts), whereas ClickHouse
              deployments split on every non-alphanumeric ASCII byte. A single word inside
              such a value is a whole-word hit on ClickHouse and a miss on Postgres; the
              substring forms behave identically on both. On Postgres deployments a value over
              80000 bytes has only its first 20000 characters indexed for whole-word matching;
              text past that is reachable only by the substring forms. Words longer than 2047
              bytes are matched as substrings, never as whole words. Case folding of non-ASCII
              text follows the database's LC_CTYPE on Postgres deployments, for the whole-word
              index, the quoted-phrase and substring forms and the word-boundary check alike;
              under a C-locale database non-ASCII letters are not folded. ASCII folds
              everywhere. Input and output behave identically on both engines. A
              substring-form term, or a text-filtered metrics request, reads every row of the
              time window that survives the other filters. A term that matches too many rows
              in the window is refused by the tracing service as QUERY_TOO_BROAD, at an
              engine-specific threshold; whether this API relays that refusal as a 400 or
              answers the page from the legacy trace store follows its read-routing rules, and
              an export's refusal is reported as the failed export's reason on the export
              status, not on the POST. On Postgres deployments each term is counted on its
              own, in every class (whole word, phrase and substring alike) and on every read
              that carries text, and is refused when it alone matches more than 50000 rows of
              the window that survive the other filters, with or without assessment_types. On
              ClickHouse deployments the refusal is the candidate-set cap, a
              deployment-configured limit counted over the matches of all terms together: a
              search page bounds its candidates to the page, so there the cap is a backstop
              rather than a limit a common term meets; metrics and by-span resolve every match
              and can trip it; and an export runs under its own 2000000-row set cap on every
              request, assessment_types included. Accounts still served by the legacy trace
              store match differently until migrated: every term matches as stemmed whole
              words (so inflected forms match and multi-word terms match word-adjacent), only
              input and output are searched, the 2-character minimum is not enforced, quoting
              a term changes nothing (the quotes are stripped and a multi-word term is already
              matched word-adjacent), and characters like `:`, `|`, or `!` inside a term may
              be interpreted as query operators or cause an error.

          span_ids: Filter by span IDs

          spans: Filter by exact (trace_id, span_id) identity. Unlike span_ids, a pair never
              matches a same-id span from another trace. ANDs with span_ids when both are set.

          statuses: Filter on span status

          trace_ids: Filter by trace IDs. The combined count of trace_ids, span_ids,
              excluded_span_ids, excluded_trace_ids, parent_ids, and (trace_id, span_id) pairs
              (each pair counting 2) may not exceed 10000. A request over that returns 422.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"x-project-id": x_project_id}), **(extra_headers or {})}
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
                    "excluded_spans": excluded_spans,
                    "excluded_trace_ids": excluded_trace_ids,
                    "extra_metadata": extra_metadata,
                    "group_id": group_id,
                    "max_duration_ms": max_duration_ms,
                    "min_duration_ms": min_duration_ms,
                    "names": names,
                    "obs_span_ids": obs_span_ids,
                    "obs_trace_ids": obs_trace_ids,
                    "parent_ids": parent_ids,
                    "parents_only": parents_only,
                    "search_texts": search_texts,
                    "span_ids": span_ids,
                    "spans": spans,
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
                        "allow_partial_results": allow_partial_results,
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
        Insert or replace multiple spans (up to 1000) in a single request.

        Use this for idempotent ingestion when spans may already exist, unlike POST
        /v5/spans/batch, which only inserts. Items without an `id` are assigned a
        generated UUID. The legacy trace store treats `id` as global and collapses
        repeated `id`s to the last occurrence. The tracing service keys spans by
        `trace_id` and `id`; it retains cross-trace ID collisions, and for a repeated
        pair keeps a completed span over an in-progress one, otherwise the later
        occurrence wins. In dual-write phases each store applies its own rule, and the
        primary store determines the returned list. A batch larger than 1000 spans is
        rejected with a validation error, as is any item whose `end_timestamp` precedes
        its `start_timestamp`, which returns a 422. When the tracing service is the
        primary store, its 400, 413 and 422 rejections keep that status and detail, as
        does a 403 when the request carried its own API key, and every other failure
        returns a 503 with a Retry-After header. A batch that forms a cycle, or a span
        whose parent belongs to another trace, is rejected with 409 before either store
        is written. A parent outside the batch is looked up in Postgres, so that part of
        the check ends once the account's spans stop being written there. Which writes
        the tracing service rejects depends in part on its storage engine: on Postgres
        deployments a NUL byte or invalid UTF-8 inside `trace_id`, `id`, `parent_id` or
        `group_id` fails the whole batch with a 400 naming the field, because replacing
        the byte would change the identity the response echoes; a NUL byte or invalid
        UTF-8 in any other field is replaced with U+FFFD and the span is persisted.
        ClickHouse deployments store the bytes verbatim.

        Credential redaction: values in the free-form `input`, `output`, `metadata`, and
        `expected` objects, and in `name`, that are credential-shaped (bearer/JWT, API
        keys, connection-string passwords) or under a credential-named key are replaced
        with `[REDACTED:credential]` before the span is persisted, so the stored and
        returned span reflects the redacted value (EY 12.3).

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
        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                spans.retrieve,  # pyright: ignore[reportDeprecated],
            )
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
        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                spans.retrieve,  # pyright: ignore[reportDeprecated],
            )
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
        self.retrieve = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                spans.retrieve,  # pyright: ignore[reportDeprecated],
            )
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
        self.retrieve = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                spans.retrieve,  # pyright: ignore[reportDeprecated],
            )
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
