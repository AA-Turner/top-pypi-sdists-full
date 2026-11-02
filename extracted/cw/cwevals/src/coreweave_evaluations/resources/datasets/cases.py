# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.datasets import case_add_params
from ...types.datasets.case_add_response import CaseAddResponse

__all__ = ["CasesResource", "AsyncCasesResource"]


class CasesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return CasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return CasesResourceWithStreamingResponse(self)

    def add(
        self,
        dataset_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cases: Iterable[case_add_params.Case],
        example_key_fields: List[Literal["input"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> CaseAddResponse:
        """Stores a batch of cases.

        Each case contains an input, an output, and optional
        metadata, such as the model or checkpoint that produced the output.

        Top-level fields in input and output objects are added to the dataset's field
        catalog. The response returns case IDs in request order.

        Request bodies must be smaller than 16 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          example_key_fields: Derives an example key for each case from a hash of its input, so row comparison
              can match cases by input. Each top-level extension field hashes by its identity,
              which leaves out file locations. Numbers hash as float64, so integers that
              differ only beyond 2^53 derive the same example key, and a number never matches
              a string. Log numeric identifiers as strings. A case with a null input gets no
              example key. Without it, a case logged without an example key matches only
              itself, in versions that read its dataset.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return self._patch(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/datasets/{dataset_id}/cases",
                namespace=namespace,
                scope_id=scope_id,
                dataset_id=dataset_id,
            ),
            body=maybe_transform(
                {
                    "cases": cases,
                    "example_key_fields": example_key_fields,
                },
                case_add_params.CaseAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CaseAddResponse,
        )


class AsyncCasesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncCasesResourceWithStreamingResponse(self)

    async def add(
        self,
        dataset_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cases: Iterable[case_add_params.Case],
        example_key_fields: List[Literal["input"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> CaseAddResponse:
        """Stores a batch of cases.

        Each case contains an input, an output, and optional
        metadata, such as the model or checkpoint that produced the output.

        Top-level fields in input and output objects are added to the dataset's field
        catalog. The response returns case IDs in request order.

        Request bodies must be smaller than 16 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          example_key_fields: Derives an example key for each case from a hash of its input, so row comparison
              can match cases by input. Each top-level extension field hashes by its identity,
              which leaves out file locations. Numbers hash as float64, so integers that
              differ only beyond 2^53 derive the same example key, and a number never matches
              a string. Log numeric identifiers as strings. A case with a null input gets no
              example key. Without it, a case logged without an example key matches only
              itself, in versions that read its dataset.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return await self._patch(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/datasets/{dataset_id}/cases",
                namespace=namespace,
                scope_id=scope_id,
                dataset_id=dataset_id,
            ),
            body=await async_maybe_transform(
                {
                    "cases": cases,
                    "example_key_fields": example_key_fields,
                },
                case_add_params.CaseAddParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CaseAddResponse,
        )


class CasesResourceWithRawResponse:
    def __init__(self, cases: CasesResource) -> None:
        self._cases = cases

        self.add = to_raw_response_wrapper(
            cases.add,
        )


class AsyncCasesResourceWithRawResponse:
    def __init__(self, cases: AsyncCasesResource) -> None:
        self._cases = cases

        self.add = async_to_raw_response_wrapper(
            cases.add,
        )


class CasesResourceWithStreamingResponse:
    def __init__(self, cases: CasesResource) -> None:
        self._cases = cases

        self.add = to_streamed_response_wrapper(
            cases.add,
        )


class AsyncCasesResourceWithStreamingResponse:
    def __init__(self, cases: AsyncCasesResource) -> None:
        self._cases = cases

        self.add = async_to_streamed_response_wrapper(
            cases.add,
        )
