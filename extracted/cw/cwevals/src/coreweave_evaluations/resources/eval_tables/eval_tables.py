# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from .rows import (
    RowsResource,
    AsyncRowsResource,
    RowsResourceWithRawResponse,
    AsyncRowsResourceWithRawResponse,
    RowsResourceWithStreamingResponse,
    AsyncRowsResourceWithStreamingResponse,
)
from ...types import eval_table_create_params
from .columns import (
    ColumnsResource,
    AsyncColumnsResource,
    ColumnsResourceWithRawResponse,
    AsyncColumnsResourceWithRawResponse,
    ColumnsResourceWithStreamingResponse,
    AsyncColumnsResourceWithStreamingResponse,
)
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
from .versions.versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ...types.eval_table_create_response import EvalTableCreateResponse

__all__ = ["EvalTablesResource", "AsyncEvalTablesResource"]


class EvalTablesResource(SyncAPIResource):
    @cached_property
    def columns(self) -> ColumnsResource:
        return ColumnsResource(self._client)

    @cached_property
    def rows(self) -> RowsResource:
        return RowsResource(self._client)

    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EvalTablesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return EvalTablesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvalTablesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return EvalTablesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        name: str,
        attributes: Dict[str, object] | Omit = omit,
        uri: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> EvalTableCreateResponse:
        """
        Creates a dataset and a live evaluation together so you can log inputs, outputs,
        and scores as rows.

        Use the returned `evaluation_id` for this table's column, row, and version
        operations. The returned `dataset_id` identifies the underlying dataset.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          uri: Location of externally stored data, such as s3://bucket/prefix/ or
              hf://datasets/org/name. The service stores this URI as metadata and does not
              read from it. Dataset versions inherit it until you supply a replacement when
              publishing a version.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-tables", namespace=namespace, scope_id=scope_id
            ),
            body=maybe_transform(
                {
                    "name": name,
                    "attributes": attributes,
                    "uri": uri,
                },
                eval_table_create_params.EvalTableCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=EvalTableCreateResponse,
        )


class AsyncEvalTablesResource(AsyncAPIResource):
    @cached_property
    def columns(self) -> AsyncColumnsResource:
        return AsyncColumnsResource(self._client)

    @cached_property
    def rows(self) -> AsyncRowsResource:
        return AsyncRowsResource(self._client)

    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEvalTablesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncEvalTablesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvalTablesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncEvalTablesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        name: str,
        attributes: Dict[str, object] | Omit = omit,
        uri: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> EvalTableCreateResponse:
        """
        Creates a dataset and a live evaluation together so you can log inputs, outputs,
        and scores as rows.

        Use the returned `evaluation_id` for this table's column, row, and version
        operations. The returned `dataset_id` identifies the underlying dataset.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          uri: Location of externally stored data, such as s3://bucket/prefix/ or
              hf://datasets/org/name. The service stores this URI as metadata and does not
              read from it. Dataset versions inherit it until you supply a replacement when
              publishing a version.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-tables", namespace=namespace, scope_id=scope_id
            ),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "attributes": attributes,
                    "uri": uri,
                },
                eval_table_create_params.EvalTableCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=EvalTableCreateResponse,
        )


class EvalTablesResourceWithRawResponse:
    def __init__(self, eval_tables: EvalTablesResource) -> None:
        self._eval_tables = eval_tables

        self.create = to_raw_response_wrapper(
            eval_tables.create,
        )

    @cached_property
    def columns(self) -> ColumnsResourceWithRawResponse:
        return ColumnsResourceWithRawResponse(self._eval_tables.columns)

    @cached_property
    def rows(self) -> RowsResourceWithRawResponse:
        return RowsResourceWithRawResponse(self._eval_tables.rows)

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._eval_tables.versions)


class AsyncEvalTablesResourceWithRawResponse:
    def __init__(self, eval_tables: AsyncEvalTablesResource) -> None:
        self._eval_tables = eval_tables

        self.create = async_to_raw_response_wrapper(
            eval_tables.create,
        )

    @cached_property
    def columns(self) -> AsyncColumnsResourceWithRawResponse:
        return AsyncColumnsResourceWithRawResponse(self._eval_tables.columns)

    @cached_property
    def rows(self) -> AsyncRowsResourceWithRawResponse:
        return AsyncRowsResourceWithRawResponse(self._eval_tables.rows)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._eval_tables.versions)


class EvalTablesResourceWithStreamingResponse:
    def __init__(self, eval_tables: EvalTablesResource) -> None:
        self._eval_tables = eval_tables

        self.create = to_streamed_response_wrapper(
            eval_tables.create,
        )

    @cached_property
    def columns(self) -> ColumnsResourceWithStreamingResponse:
        return ColumnsResourceWithStreamingResponse(self._eval_tables.columns)

    @cached_property
    def rows(self) -> RowsResourceWithStreamingResponse:
        return RowsResourceWithStreamingResponse(self._eval_tables.rows)

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._eval_tables.versions)


class AsyncEvalTablesResourceWithStreamingResponse:
    def __init__(self, eval_tables: AsyncEvalTablesResource) -> None:
        self._eval_tables = eval_tables

        self.create = async_to_streamed_response_wrapper(
            eval_tables.create,
        )

    @cached_property
    def columns(self) -> AsyncColumnsResourceWithStreamingResponse:
        return AsyncColumnsResourceWithStreamingResponse(self._eval_tables.columns)

    @cached_property
    def rows(self) -> AsyncRowsResourceWithStreamingResponse:
        return AsyncRowsResourceWithStreamingResponse(self._eval_tables.rows)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._eval_tables.versions)
