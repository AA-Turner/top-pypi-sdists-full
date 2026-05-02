# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Mapping, Iterable, cast
from typing_extensions import Literal

import httpx

from ...types import application_process_params, application_validate_params, application_upload_files_params
from ..._types import (
    Body,
    Omit,
    Query,
    Headers,
    NotGiven,
    FileTypes,
    SequenceNotStr,
    omit,
    not_given,
)
from ..._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from ..._compat import cached_property
from .dashboards import (
    DashboardsResource,
    AsyncDashboardsResource,
    DashboardsResourceWithRawResponse,
    AsyncDashboardsResourceWithRawResponse,
    DashboardsResourceWithStreamingResponse,
    AsyncDashboardsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .metrics.metrics import (
    MetricsResource,
    AsyncMetricsResource,
    MetricsResourceWithRawResponse,
    AsyncMetricsResourceWithRawResponse,
    MetricsResourceWithStreamingResponse,
    AsyncMetricsResourceWithStreamingResponse,
)
from .chat_threads.chat_threads import (
    ChatThreadsResource,
    AsyncChatThreadsResource,
    ChatThreadsResourceWithRawResponse,
    AsyncChatThreadsResourceWithRawResponse,
    ChatThreadsResourceWithStreamingResponse,
    AsyncChatThreadsResourceWithStreamingResponse,
)
from ...types.application_edge_param import ApplicationEdgeParam
from ...types.application_node_param import ApplicationNodeParam
from ...types.application_upload_files_response import ApplicationUploadFilesResponse

__all__ = ["ApplicationsResource", "AsyncApplicationsResource"]


class ApplicationsResource(SyncAPIResource):
    @cached_property
    def chat_threads(self) -> ChatThreadsResource:
        return ChatThreadsResource(self._client)

    @cached_property
    def dashboards(self) -> DashboardsResource:
        return DashboardsResource(self._client)

    @cached_property
    def metrics(self) -> MetricsResource:
        return MetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ApplicationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationsResourceWithStreamingResponse(self)

    def process(
        self,
        *,
        edges: Iterable[ApplicationEdgeParam],
        inputs: Dict[str, Dict[str, object]],
        nodes: Iterable[ApplicationNodeParam],
        version: Literal["V0"],
        history: Iterable[application_process_params.History] | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        overrides: application_process_params.Overrides | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Process Application

        Args:
          edges: List of edges in the application graph

          inputs: Input data for the application. You must provide inputs for each input node

          nodes: List of nodes in the application graph

          version: Version of the application schema

          history: History of the application

          operation_metadata: Arbitrary user-defined metadata that can be attached to the process operations
              and will be registered in the interaction.

          overrides: Optional overrides for the application

          stream: Control to have streaming of the endpoint. If the last node before the output is
              a completion node, you can set this to true to get the output as soon as the
              completion node has a token

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/applications/process",
            body=maybe_transform(
                {
                    "edges": edges,
                    "inputs": inputs,
                    "nodes": nodes,
                    "version": version,
                    "history": history,
                    "operation_metadata": operation_metadata,
                    "overrides": overrides,
                    "stream": stream,
                },
                application_process_params.ApplicationProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def upload_files(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        account_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationUploadFilesResponse:
        """
        Upload Application Files

        Args:
          files: Upload files to be used in an application.

          account_id: Account which the file will be tied to. Use this account id query param if you
              are using the API or the SDK.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"files": files})
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v4/applications/upload-files",
            body=maybe_transform(body, application_upload_files_params.ApplicationUploadFilesParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"account_id": account_id}, application_upload_files_params.ApplicationUploadFilesParams
                ),
            ),
            cast_to=ApplicationUploadFilesResponse,
        )

    def validate(
        self,
        *,
        edges: Iterable[ApplicationEdgeParam],
        nodes: Iterable[ApplicationNodeParam],
        version: Literal["V0"],
        overrides: application_validate_params.Overrides | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Validate Application

        Args:
          edges: List of edges in the application graph

          nodes: List of nodes in the application graph

          version: Version of the application schema

          overrides: Optional overrides for the application

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/applications/validate",
            body=maybe_transform(
                {
                    "edges": edges,
                    "nodes": nodes,
                    "version": version,
                    "overrides": overrides,
                },
                application_validate_params.ApplicationValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncApplicationsResource(AsyncAPIResource):
    @cached_property
    def chat_threads(self) -> AsyncChatThreadsResource:
        return AsyncChatThreadsResource(self._client)

    @cached_property
    def dashboards(self) -> AsyncDashboardsResource:
        return AsyncDashboardsResource(self._client)

    @cached_property
    def metrics(self) -> AsyncMetricsResource:
        return AsyncMetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncApplicationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationsResourceWithStreamingResponse(self)

    async def process(
        self,
        *,
        edges: Iterable[ApplicationEdgeParam],
        inputs: Dict[str, Dict[str, object]],
        nodes: Iterable[ApplicationNodeParam],
        version: Literal["V0"],
        history: Iterable[application_process_params.History] | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        overrides: application_process_params.Overrides | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Process Application

        Args:
          edges: List of edges in the application graph

          inputs: Input data for the application. You must provide inputs for each input node

          nodes: List of nodes in the application graph

          version: Version of the application schema

          history: History of the application

          operation_metadata: Arbitrary user-defined metadata that can be attached to the process operations
              and will be registered in the interaction.

          overrides: Optional overrides for the application

          stream: Control to have streaming of the endpoint. If the last node before the output is
              a completion node, you can set this to true to get the output as soon as the
              completion node has a token

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/applications/process",
            body=await async_maybe_transform(
                {
                    "edges": edges,
                    "inputs": inputs,
                    "nodes": nodes,
                    "version": version,
                    "history": history,
                    "operation_metadata": operation_metadata,
                    "overrides": overrides,
                    "stream": stream,
                },
                application_process_params.ApplicationProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def upload_files(
        self,
        *,
        files: SequenceNotStr[FileTypes],
        account_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationUploadFilesResponse:
        """
        Upload Application Files

        Args:
          files: Upload files to be used in an application.

          account_id: Account which the file will be tied to. Use this account id query param if you
              are using the API or the SDK.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"files": files})
        extracted_files = extract_files(cast(Mapping[str, object], body), paths=[["files", "<array>"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v4/applications/upload-files",
            body=await async_maybe_transform(body, application_upload_files_params.ApplicationUploadFilesParams),
            files=extracted_files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"account_id": account_id}, application_upload_files_params.ApplicationUploadFilesParams
                ),
            ),
            cast_to=ApplicationUploadFilesResponse,
        )

    async def validate(
        self,
        *,
        edges: Iterable[ApplicationEdgeParam],
        nodes: Iterable[ApplicationNodeParam],
        version: Literal["V0"],
        overrides: application_validate_params.Overrides | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Validate Application

        Args:
          edges: List of edges in the application graph

          nodes: List of nodes in the application graph

          version: Version of the application schema

          overrides: Optional overrides for the application

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/applications/validate",
            body=await async_maybe_transform(
                {
                    "edges": edges,
                    "nodes": nodes,
                    "version": version,
                    "overrides": overrides,
                },
                application_validate_params.ApplicationValidateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ApplicationsResourceWithRawResponse:
    def __init__(self, applications: ApplicationsResource) -> None:
        self._applications = applications

        self.process = to_raw_response_wrapper(
            applications.process,
        )
        self.upload_files = to_raw_response_wrapper(
            applications.upload_files,
        )
        self.validate = to_raw_response_wrapper(
            applications.validate,
        )

    @cached_property
    def chat_threads(self) -> ChatThreadsResourceWithRawResponse:
        return ChatThreadsResourceWithRawResponse(self._applications.chat_threads)

    @cached_property
    def dashboards(self) -> DashboardsResourceWithRawResponse:
        return DashboardsResourceWithRawResponse(self._applications.dashboards)

    @cached_property
    def metrics(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self._applications.metrics)


class AsyncApplicationsResourceWithRawResponse:
    def __init__(self, applications: AsyncApplicationsResource) -> None:
        self._applications = applications

        self.process = async_to_raw_response_wrapper(
            applications.process,
        )
        self.upload_files = async_to_raw_response_wrapper(
            applications.upload_files,
        )
        self.validate = async_to_raw_response_wrapper(
            applications.validate,
        )

    @cached_property
    def chat_threads(self) -> AsyncChatThreadsResourceWithRawResponse:
        return AsyncChatThreadsResourceWithRawResponse(self._applications.chat_threads)

    @cached_property
    def dashboards(self) -> AsyncDashboardsResourceWithRawResponse:
        return AsyncDashboardsResourceWithRawResponse(self._applications.dashboards)

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self._applications.metrics)


class ApplicationsResourceWithStreamingResponse:
    def __init__(self, applications: ApplicationsResource) -> None:
        self._applications = applications

        self.process = to_streamed_response_wrapper(
            applications.process,
        )
        self.upload_files = to_streamed_response_wrapper(
            applications.upload_files,
        )
        self.validate = to_streamed_response_wrapper(
            applications.validate,
        )

    @cached_property
    def chat_threads(self) -> ChatThreadsResourceWithStreamingResponse:
        return ChatThreadsResourceWithStreamingResponse(self._applications.chat_threads)

    @cached_property
    def dashboards(self) -> DashboardsResourceWithStreamingResponse:
        return DashboardsResourceWithStreamingResponse(self._applications.dashboards)

    @cached_property
    def metrics(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self._applications.metrics)


class AsyncApplicationsResourceWithStreamingResponse:
    def __init__(self, applications: AsyncApplicationsResource) -> None:
        self._applications = applications

        self.process = async_to_streamed_response_wrapper(
            applications.process,
        )
        self.upload_files = async_to_streamed_response_wrapper(
            applications.upload_files,
        )
        self.validate = async_to_streamed_response_wrapper(
            applications.validate,
        )

    @cached_property
    def chat_threads(self) -> AsyncChatThreadsResourceWithStreamingResponse:
        return AsyncChatThreadsResourceWithStreamingResponse(self._applications.chat_threads)

    @cached_property
    def dashboards(self) -> AsyncDashboardsResourceWithStreamingResponse:
        return AsyncDashboardsResourceWithStreamingResponse(self._applications.dashboards)

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self._applications.metrics)
