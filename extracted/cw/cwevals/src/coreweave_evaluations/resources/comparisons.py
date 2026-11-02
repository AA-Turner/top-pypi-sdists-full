# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import comparison_create_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.comparison_get_response import ComparisonGetResponse
from ..types.comparison_create_response import ComparisonCreateResponse

__all__ = ["ComparisonsResource", "AsyncComparisonsResource"]


class ComparisonsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ComparisonsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return ComparisonsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ComparisonsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return ComparisonsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        comparisons: Iterable[comparison_create_params.Comparison],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComparisonCreateResponse:
        """
        Groups existing, published cases into comparisons that can be scored together.
        Each member can have a role label to distinguish its part in the comparison.

        The response returns comparison IDs in request order. Cases are grouped by
        explicit membership, not by matching `example_key` values.

        Request bodies must be smaller than 16 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

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
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/comparisons", namespace=namespace, scope_id=scope_id
            ),
            body=maybe_transform({"comparisons": comparisons}, comparison_create_params.ComparisonCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComparisonCreateResponse,
        )

    def get(
        self,
        comparison_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComparisonGetResponse:
        """
        Returns a published comparison, its member cases in submitted order, and any
        role labels and attributes.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not comparison_id:
            raise ValueError(f"Expected a non-empty value for `comparison_id` but received {comparison_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/comparisons/{comparison_id}",
                namespace=namespace,
                scope_id=scope_id,
                comparison_id=comparison_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ComparisonGetResponse,
        )


class AsyncComparisonsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncComparisonsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncComparisonsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncComparisonsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncComparisonsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        comparisons: Iterable[comparison_create_params.Comparison],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComparisonCreateResponse:
        """
        Groups existing, published cases into comparisons that can be scored together.
        Each member can have a role label to distinguish its part in the comparison.

        The response returns comparison IDs in request order. Cases are grouped by
        explicit membership, not by matching `example_key` values.

        Request bodies must be smaller than 16 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

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
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/comparisons", namespace=namespace, scope_id=scope_id
            ),
            body=await async_maybe_transform(
                {"comparisons": comparisons}, comparison_create_params.ComparisonCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComparisonCreateResponse,
        )

    async def get(
        self,
        comparison_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComparisonGetResponse:
        """
        Returns a published comparison, its member cases in submitted order, and any
        role labels and attributes.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not comparison_id:
            raise ValueError(f"Expected a non-empty value for `comparison_id` but received {comparison_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/comparisons/{comparison_id}",
                namespace=namespace,
                scope_id=scope_id,
                comparison_id=comparison_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ComparisonGetResponse,
        )


class ComparisonsResourceWithRawResponse:
    def __init__(self, comparisons: ComparisonsResource) -> None:
        self._comparisons = comparisons

        self.create = to_raw_response_wrapper(
            comparisons.create,
        )
        self.get = to_raw_response_wrapper(
            comparisons.get,
        )


class AsyncComparisonsResourceWithRawResponse:
    def __init__(self, comparisons: AsyncComparisonsResource) -> None:
        self._comparisons = comparisons

        self.create = async_to_raw_response_wrapper(
            comparisons.create,
        )
        self.get = async_to_raw_response_wrapper(
            comparisons.get,
        )


class ComparisonsResourceWithStreamingResponse:
    def __init__(self, comparisons: ComparisonsResource) -> None:
        self._comparisons = comparisons

        self.create = to_streamed_response_wrapper(
            comparisons.create,
        )
        self.get = to_streamed_response_wrapper(
            comparisons.get,
        )


class AsyncComparisonsResourceWithStreamingResponse:
    def __init__(self, comparisons: AsyncComparisonsResource) -> None:
        self._comparisons = comparisons

        self.create = async_to_streamed_response_wrapper(
            comparisons.create,
        )
        self.get = async_to_streamed_response_wrapper(
            comparisons.get,
        )
