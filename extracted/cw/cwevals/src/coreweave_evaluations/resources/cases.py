# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import path_template
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.case_get_response import CaseGetResponse

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

    def get(
        self,
        case_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CaseGetResponse:
        """
        Returns one published case, including its input, output, variant, attributes,
        and the commit that published it.

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
        if not case_id:
            raise ValueError(f"Expected a non-empty value for `case_id` but received {case_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/cases/{case_id}",
                namespace=namespace,
                scope_id=scope_id,
                case_id=case_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CaseGetResponse,
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

    async def get(
        self,
        case_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CaseGetResponse:
        """
        Returns one published case, including its input, output, variant, attributes,
        and the commit that published it.

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
        if not case_id:
            raise ValueError(f"Expected a non-empty value for `case_id` but received {case_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/cases/{case_id}",
                namespace=namespace,
                scope_id=scope_id,
                case_id=case_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CaseGetResponse,
        )


class CasesResourceWithRawResponse:
    def __init__(self, cases: CasesResource) -> None:
        self._cases = cases

        self.get = to_raw_response_wrapper(
            cases.get,
        )


class AsyncCasesResourceWithRawResponse:
    def __init__(self, cases: AsyncCasesResource) -> None:
        self._cases = cases

        self.get = async_to_raw_response_wrapper(
            cases.get,
        )


class CasesResourceWithStreamingResponse:
    def __init__(self, cases: CasesResource) -> None:
        self._cases = cases

        self.get = to_streamed_response_wrapper(
            cases.get,
        )


class AsyncCasesResourceWithStreamingResponse:
    def __init__(self, cases: AsyncCasesResource) -> None:
        self._cases = cases

        self.get = async_to_streamed_response_wrapper(
            cases.get,
        )
