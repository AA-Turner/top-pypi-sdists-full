# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
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
from ...types.scorers import version_create_params
from ...types.scorers.version_get_response import VersionGetResponse
from ...types.scorers.version_create_response import VersionCreateResponse

__all__ = ["VersionsResource", "AsyncVersionsResource"]


class VersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return VersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return VersionsResourceWithStreamingResponse(self)

    def create(
        self,
        scorer_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        allowed_target_kinds: List[Literal["case", "comparison", "trajectory"]],
        name: str,
        value_type: Literal["null", "boolean", "integer", "number", "string", "json"],
        description: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> VersionCreateResponse:
        """
        Creates an immutable specification under an existing scorer, with its own name,
        score value type, allowed target kinds, and optional description. Existing
        versions and their scores remain unchanged.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          allowed_target_kinds: Kinds of resource this scorer version can score: individual cases, comparisons,
              or trajectories.

          name: Name of this scoring specification, such as accuracy or relevance. Leading and
              trailing whitespace are not allowed.

          value_type: JSON type that every score recorded with this scorer version must use.

          description: Human-readable explanation of what this scorer version measures.

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
        if not scorer_id:
            raise ValueError(f"Expected a non-empty value for `scorer_id` but received {scorer_id!r}")
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scorers/{scorer_id}/versions",
                namespace=namespace,
                scope_id=scope_id,
                scorer_id=scorer_id,
            ),
            body=maybe_transform(
                {
                    "allowed_target_kinds": allowed_target_kinds,
                    "name": name,
                    "value_type": value_type,
                    "description": description,
                },
                version_create_params.VersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=VersionCreateResponse,
        )

    def get(
        self,
        scorer_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        scorer_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionGetResponse:
        """
        Returns one immutable scorer specification, including its name, score value
        type, and allowed target kinds.

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
        if not scorer_id:
            raise ValueError(f"Expected a non-empty value for `scorer_id` but received {scorer_id!r}")
        if not scorer_version_id:
            raise ValueError(f"Expected a non-empty value for `scorer_version_id` but received {scorer_version_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scorers/{scorer_id}/versions/{scorer_version_id}",
                namespace=namespace,
                scope_id=scope_id,
                scorer_id=scorer_id,
                scorer_version_id=scorer_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VersionGetResponse,
        )


class AsyncVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        scorer_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        allowed_target_kinds: List[Literal["case", "comparison", "trajectory"]],
        name: str,
        value_type: Literal["null", "boolean", "integer", "number", "string", "json"],
        description: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> VersionCreateResponse:
        """
        Creates an immutable specification under an existing scorer, with its own name,
        score value type, allowed target kinds, and optional description. Existing
        versions and their scores remain unchanged.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          allowed_target_kinds: Kinds of resource this scorer version can score: individual cases, comparisons,
              or trajectories.

          name: Name of this scoring specification, such as accuracy or relevance. Leading and
              trailing whitespace are not allowed.

          value_type: JSON type that every score recorded with this scorer version must use.

          description: Human-readable explanation of what this scorer version measures.

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
        if not scorer_id:
            raise ValueError(f"Expected a non-empty value for `scorer_id` but received {scorer_id!r}")
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scorers/{scorer_id}/versions",
                namespace=namespace,
                scope_id=scope_id,
                scorer_id=scorer_id,
            ),
            body=await async_maybe_transform(
                {
                    "allowed_target_kinds": allowed_target_kinds,
                    "name": name,
                    "value_type": value_type,
                    "description": description,
                },
                version_create_params.VersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=VersionCreateResponse,
        )

    async def get(
        self,
        scorer_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        scorer_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionGetResponse:
        """
        Returns one immutable scorer specification, including its name, score value
        type, and allowed target kinds.

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
        if not scorer_id:
            raise ValueError(f"Expected a non-empty value for `scorer_id` but received {scorer_id!r}")
        if not scorer_version_id:
            raise ValueError(f"Expected a non-empty value for `scorer_version_id` but received {scorer_version_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scorers/{scorer_id}/versions/{scorer_version_id}",
                namespace=namespace,
                scope_id=scope_id,
                scorer_id=scorer_id,
                scorer_version_id=scorer_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VersionGetResponse,
        )


class VersionsResourceWithRawResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.create = to_raw_response_wrapper(
            versions.create,
        )
        self.get = to_raw_response_wrapper(
            versions.get,
        )


class AsyncVersionsResourceWithRawResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.create = async_to_raw_response_wrapper(
            versions.create,
        )
        self.get = async_to_raw_response_wrapper(
            versions.get,
        )


class VersionsResourceWithStreamingResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.create = to_streamed_response_wrapper(
            versions.create,
        )
        self.get = to_streamed_response_wrapper(
            versions.get,
        )


class AsyncVersionsResourceWithStreamingResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.create = async_to_streamed_response_wrapper(
            versions.create,
        )
        self.get = async_to_streamed_response_wrapper(
            versions.get,
        )
