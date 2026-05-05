# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast

import httpx

from ..types import build_list_params, build_create_params
from .._files import deepcopy_with_paths
from .._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder
from .._base_client import AsyncPaginator, make_request_options
from ..types.stream_chunk import StreamChunk
from ..types.chat.sort_order import SortOrder
from ..types.agentex_cloud_build import AgentexCloudBuild
from ..types.build_list_undeployed_response import BuildListUndeployedResponse

__all__ = ["BuildResource", "AsyncBuildResource"]


class BuildResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BuildResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return BuildResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BuildResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return BuildResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        agent_name: str,
        context_archive: FileTypes,
        image_name: str,
        build_args: str | Omit = omit,
        image_tag: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Submit a container image build.

        Upload a tar.gz archive containing the build context (Dockerfile and any files
        needed for the build) along with image name, tag, and optional build arguments.

        Maximum file size: 500MB

        Args:
          agent_name: Name of the agent that this build belongs to

          context_archive: tar.gz archive containing the build context (Dockerfile and any files needed for
              the build)

          image_name: Name for the built image

          build_args: JSON string of build arguments

          image_tag: Tag for the built image

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "agent_name": agent_name,
                "context_archive": context_archive,
                "image_name": image_name,
                "build_args": build_args,
                "image_tag": image_tag,
            },
            [["context_archive"]],
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["context_archive"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v5/builds",
            body=maybe_transform(body, build_create_params.BuildCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudBuild,
        )

    def retrieve(
        self,
        build_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Get a build by ID, including current status from the cloud provider.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not build_id:
            raise ValueError(f"Expected a non-empty value for `build_id` but received {build_id!r}")
        return self._get(
            path_template("/v5/builds/{build_id}", build_id=build_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudBuild,
        )

    def list(
        self,
        *,
        agent_name: str | Omit = omit,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[AgentexCloudBuild]:
        """
        List Builds

        Args:
          agent_name: Filter builds by agent name

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/builds",
            page=SyncCursorPage[AgentexCloudBuild],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_name": agent_name,
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    build_list_params.BuildListParams,
                ),
            ),
            model=AgentexCloudBuild,
        )

    def cancel(
        self,
        build_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Cancel a pending or running build.

        Returns 202 Accepted — the actual cancellation happens asynchronously via a
        Temporal workflow.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not build_id:
            raise ValueError(f"Expected a non-empty value for `build_id` but received {build_id!r}")
        return self._post(
            path_template("/v5/builds/{build_id}/cancel", build_id=build_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudBuild,
        )

    def list_undeployed(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BuildListUndeployedResponse:
        """
        List agents that exist only as cloud builds with no healthy deployment.

        Returns distinct agent names from builds that have never had a deploy reach
        'healthy' status, along with each agent's latest build info and total build
        count. Useful for surfacing agents that have been built but not yet deployed.
        """
        return self._get(
            "/v5/builds/undeployed",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildListUndeployedResponse,
        )

    def logs(
        self,
        build_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[StreamChunk]:
        """
        Stream build logs via Server-Sent Events (SSE).

        Returns a streaming response with content-type text/event-stream. Each log line
        is sent as an SSE data event.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not build_id:
            raise ValueError(f"Expected a non-empty value for `build_id` but received {build_id!r}")
        return self._get(
            path_template("/v5/builds/{build_id}/logs", build_id=build_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StreamChunk,
            stream=True,
            stream_cls=Stream[StreamChunk],
        )


class AsyncBuildResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBuildResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncBuildResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBuildResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncBuildResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        agent_name: str,
        context_archive: FileTypes,
        image_name: str,
        build_args: str | Omit = omit,
        image_tag: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Submit a container image build.

        Upload a tar.gz archive containing the build context (Dockerfile and any files
        needed for the build) along with image name, tag, and optional build arguments.

        Maximum file size: 500MB

        Args:
          agent_name: Name of the agent that this build belongs to

          context_archive: tar.gz archive containing the build context (Dockerfile and any files needed for
              the build)

          image_name: Name for the built image

          build_args: JSON string of build arguments

          image_tag: Tag for the built image

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "agent_name": agent_name,
                "context_archive": context_archive,
                "image_name": image_name,
                "build_args": build_args,
                "image_tag": image_tag,
            },
            [["context_archive"]],
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["context_archive"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v5/builds",
            body=await async_maybe_transform(body, build_create_params.BuildCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudBuild,
        )

    async def retrieve(
        self,
        build_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Get a build by ID, including current status from the cloud provider.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not build_id:
            raise ValueError(f"Expected a non-empty value for `build_id` but received {build_id!r}")
        return await self._get(
            path_template("/v5/builds/{build_id}", build_id=build_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudBuild,
        )

    def list(
        self,
        *,
        agent_name: str | Omit = omit,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AgentexCloudBuild, AsyncCursorPage[AgentexCloudBuild]]:
        """
        List Builds

        Args:
          agent_name: Filter builds by agent name

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/builds",
            page=AsyncCursorPage[AgentexCloudBuild],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_name": agent_name,
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    build_list_params.BuildListParams,
                ),
            ),
            model=AgentexCloudBuild,
        )

    async def cancel(
        self,
        build_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Cancel a pending or running build.

        Returns 202 Accepted — the actual cancellation happens asynchronously via a
        Temporal workflow.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not build_id:
            raise ValueError(f"Expected a non-empty value for `build_id` but received {build_id!r}")
        return await self._post(
            path_template("/v5/builds/{build_id}/cancel", build_id=build_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudBuild,
        )

    async def list_undeployed(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BuildListUndeployedResponse:
        """
        List agents that exist only as cloud builds with no healthy deployment.

        Returns distinct agent names from builds that have never had a deploy reach
        'healthy' status, along with each agent's latest build info and total build
        count. Useful for surfacing agents that have been built but not yet deployed.
        """
        return await self._get(
            "/v5/builds/undeployed",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BuildListUndeployedResponse,
        )

    async def logs(
        self,
        build_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[StreamChunk]:
        """
        Stream build logs via Server-Sent Events (SSE).

        Returns a streaming response with content-type text/event-stream. Each log line
        is sent as an SSE data event.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not build_id:
            raise ValueError(f"Expected a non-empty value for `build_id` but received {build_id!r}")
        return await self._get(
            path_template("/v5/builds/{build_id}/logs", build_id=build_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StreamChunk,
            stream=True,
            stream_cls=AsyncStream[StreamChunk],
        )


class BuildResourceWithRawResponse:
    def __init__(self, build: BuildResource) -> None:
        self._build = build

        self.create = to_raw_response_wrapper(
            build.create,
        )
        self.retrieve = to_raw_response_wrapper(
            build.retrieve,
        )
        self.list = to_raw_response_wrapper(
            build.list,
        )
        self.cancel = to_raw_response_wrapper(
            build.cancel,
        )
        self.list_undeployed = to_raw_response_wrapper(
            build.list_undeployed,
        )
        self.logs = to_raw_response_wrapper(
            build.logs,
        )


class AsyncBuildResourceWithRawResponse:
    def __init__(self, build: AsyncBuildResource) -> None:
        self._build = build

        self.create = async_to_raw_response_wrapper(
            build.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            build.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            build.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            build.cancel,
        )
        self.list_undeployed = async_to_raw_response_wrapper(
            build.list_undeployed,
        )
        self.logs = async_to_raw_response_wrapper(
            build.logs,
        )


class BuildResourceWithStreamingResponse:
    def __init__(self, build: BuildResource) -> None:
        self._build = build

        self.create = to_streamed_response_wrapper(
            build.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            build.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            build.list,
        )
        self.cancel = to_streamed_response_wrapper(
            build.cancel,
        )
        self.list_undeployed = to_streamed_response_wrapper(
            build.list_undeployed,
        )
        self.logs = to_streamed_response_wrapper(
            build.logs,
        )


class AsyncBuildResourceWithStreamingResponse:
    def __init__(self, build: AsyncBuildResource) -> None:
        self._build = build

        self.create = async_to_streamed_response_wrapper(
            build.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            build.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            build.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            build.cancel,
        )
        self.list_undeployed = async_to_streamed_response_wrapper(
            build.list_undeployed,
        )
        self.logs = async_to_streamed_response_wrapper(
            build.logs,
        )
