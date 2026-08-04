# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast
from typing_extensions import Literal

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
        context_archive: FileTypes,
        image_name: str,
        agent_id: str | Omit = omit,
        agent_name: str | Omit = omit,
        build_args: str | Omit = omit,
        image_tag: str | Omit = omit,
        platform: Literal["linux/amd64", "linux/arm64", "linux/arm/v7"] | Omit = omit,
        source_commit: str | Omit = omit,
        source_dirty: bool | Omit = omit,
        source_ref: str | Omit = omit,
        source_repo: str | Omit = omit,
        source_subpath: str | Omit = omit,
        working_tree_hash: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Submit a container image build from an uploaded build context and return the
        created build record.

        The request is multipart form data: a tar.gz `context_archive` with the
        Dockerfile at its root is streamed to cloud object storage, along with the
        target `image_name`, an optional `image_tag` (defaults to `latest`), optional
        Docker `build_args` supplied as a JSON string, and an optional target
        `platform`. Exactly one of `agent_name` or `agent_id` must be provided: pass
        `agent_name` to create a brand-new agent for a first-time build (rejected if an
        agent with that name already exists), or `agent_id` to build for an agent that
        already exists. The build is handed to the configured cloud build provider and
        runs asynchronously, so the returned record reflects the build's initial status
        (typically queued or running) rather than a finished image; poll Get Build or
        follow Stream Build Logs to observe progression to a terminal state. The request
        is rejected if the archive is missing or empty, exceeds 500MB, or if
        `build_args` is not valid JSON.

        Args:
          context_archive: tar.gz archive containing the build context (Dockerfile and any files needed for
              the build)

          image_name: Name for the built image

          agent_id: ID of the existing agent this build targets

          agent_name: Name of the brand-new agent to create from this build

          build_args: JSON string of build arguments

          image_tag: Tag for the built image

          platform: Target platform for the Docker build. Defaults to the build host's native
              architecture when not specified.

          source_commit: Git commit the build context was at.

          source_dirty: Whether the work tree had uncommitted changes at build time.

          source_ref: Git branch or tag for source_commit.

          source_repo: Normalized git remote the build context came from.

          source_subpath: Build-context path relative to the repo root.

          working_tree_hash: Deterministic SHA-256 content hash of the build inputs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "context_archive": context_archive,
                "image_name": image_name,
                "agent_id": agent_id,
                "agent_name": agent_name,
                "build_args": build_args,
                "image_tag": image_tag,
                "platform": platform,
                "source_commit": source_commit,
                "source_dirty": source_dirty,
                "source_ref": source_ref,
                "source_repo": source_repo,
                "source_subpath": source_subpath,
                "working_tree_hash": working_tree_hash,
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
        Retrieve a single build by its ID, including its current lifecycle status.

        Because builds run asynchronously after submission, the status returned here
        reflects the latest known state and may still be queued or running; call this
        endpoint again to observe progression to a terminal state such as success,
        failed, cancelled, or timed out. Responds with a not-found error if no such
        build exists for the caller's account.

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
        source_commit: str | Omit = omit,
        starting_after: str | Omit = omit,
        working_tree_hash: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[AgentexCloudBuild]:
        """
        List container image build records for the caller's account as a paginated
        collection.

        Each entry is one individual build with its current lifecycle status; pass
        `agent_name`, `source_commit`, or `working_tree_hash` to return only matching
        builds. Archived builds are excluded, and results are limited to builds the
        caller is permitted to read. Use this to enumerate individual builds; to instead
        list agents that have been built but not yet deployed, use
        `GET /v5/builds/undeployed`.

        Args:
          agent_name: Filter builds by agent name

          source_commit: Filter builds by source git commit

          working_tree_hash: Filter builds by build-context content hash

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
                        "source_commit": source_commit,
                        "starting_after": starting_after,
                        "working_tree_hash": working_tree_hash,
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
        Request cancellation of a build and return 202 Accepted.

        Cancellation runs asynchronously: the endpoint verifies the build exists and
        then hands it off to a background workflow that marks the build as cancelling,
        asks the cloud build provider to stop it, and polls until the build reaches a
        terminal state before recording the final status. Only builds that are still
        queued or running are actually cancelled; if the build has already finished, or
        cancellation is already in progress, the request is still accepted but has no
        effect. The returned record reflects the build's state at the time of the call,
        so it will not yet show the pending cancellation. The request is rejected if no
        such build exists for the caller's account.

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
        List agents that exist only as cloud builds and have no healthy deployment yet.

        Unlike listing builds, this aggregates by agent: it returns one entry per
        distinct agent name whose builds have never reached a healthy deploy, each
        carrying that agent's most recent build and its total build count. The result is
        a plain list (not paginated) and is limited to builds the caller is permitted to
        read. Use this to surface agents that were built but still need to be deployed;
        use `GET /v5/builds` when you need the individual build records instead.
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
        Stream a build's logs as Server-Sent Events.

        The response has content-type `text/event-stream`; each event carries one log
        line as an `AgentexCloudBuildLogLine` object, delivered as lines become
        available from the cloud build provider. The stream ends when the provider stops
        producing output. Responds with a not-found error if no such build exists for
        the caller's account.

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
        context_archive: FileTypes,
        image_name: str,
        agent_id: str | Omit = omit,
        agent_name: str | Omit = omit,
        build_args: str | Omit = omit,
        image_tag: str | Omit = omit,
        platform: Literal["linux/amd64", "linux/arm64", "linux/arm/v7"] | Omit = omit,
        source_commit: str | Omit = omit,
        source_dirty: bool | Omit = omit,
        source_ref: str | Omit = omit,
        source_repo: str | Omit = omit,
        source_subpath: str | Omit = omit,
        working_tree_hash: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudBuild:
        """
        Submit a container image build from an uploaded build context and return the
        created build record.

        The request is multipart form data: a tar.gz `context_archive` with the
        Dockerfile at its root is streamed to cloud object storage, along with the
        target `image_name`, an optional `image_tag` (defaults to `latest`), optional
        Docker `build_args` supplied as a JSON string, and an optional target
        `platform`. Exactly one of `agent_name` or `agent_id` must be provided: pass
        `agent_name` to create a brand-new agent for a first-time build (rejected if an
        agent with that name already exists), or `agent_id` to build for an agent that
        already exists. The build is handed to the configured cloud build provider and
        runs asynchronously, so the returned record reflects the build's initial status
        (typically queued or running) rather than a finished image; poll Get Build or
        follow Stream Build Logs to observe progression to a terminal state. The request
        is rejected if the archive is missing or empty, exceeds 500MB, or if
        `build_args` is not valid JSON.

        Args:
          context_archive: tar.gz archive containing the build context (Dockerfile and any files needed for
              the build)

          image_name: Name for the built image

          agent_id: ID of the existing agent this build targets

          agent_name: Name of the brand-new agent to create from this build

          build_args: JSON string of build arguments

          image_tag: Tag for the built image

          platform: Target platform for the Docker build. Defaults to the build host's native
              architecture when not specified.

          source_commit: Git commit the build context was at.

          source_dirty: Whether the work tree had uncommitted changes at build time.

          source_ref: Git branch or tag for source_commit.

          source_repo: Normalized git remote the build context came from.

          source_subpath: Build-context path relative to the repo root.

          working_tree_hash: Deterministic SHA-256 content hash of the build inputs.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "context_archive": context_archive,
                "image_name": image_name,
                "agent_id": agent_id,
                "agent_name": agent_name,
                "build_args": build_args,
                "image_tag": image_tag,
                "platform": platform,
                "source_commit": source_commit,
                "source_dirty": source_dirty,
                "source_ref": source_ref,
                "source_repo": source_repo,
                "source_subpath": source_subpath,
                "working_tree_hash": working_tree_hash,
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
        Retrieve a single build by its ID, including its current lifecycle status.

        Because builds run asynchronously after submission, the status returned here
        reflects the latest known state and may still be queued or running; call this
        endpoint again to observe progression to a terminal state such as success,
        failed, cancelled, or timed out. Responds with a not-found error if no such
        build exists for the caller's account.

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
        source_commit: str | Omit = omit,
        starting_after: str | Omit = omit,
        working_tree_hash: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AgentexCloudBuild, AsyncCursorPage[AgentexCloudBuild]]:
        """
        List container image build records for the caller's account as a paginated
        collection.

        Each entry is one individual build with its current lifecycle status; pass
        `agent_name`, `source_commit`, or `working_tree_hash` to return only matching
        builds. Archived builds are excluded, and results are limited to builds the
        caller is permitted to read. Use this to enumerate individual builds; to instead
        list agents that have been built but not yet deployed, use
        `GET /v5/builds/undeployed`.

        Args:
          agent_name: Filter builds by agent name

          source_commit: Filter builds by source git commit

          working_tree_hash: Filter builds by build-context content hash

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
                        "source_commit": source_commit,
                        "starting_after": starting_after,
                        "working_tree_hash": working_tree_hash,
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
        Request cancellation of a build and return 202 Accepted.

        Cancellation runs asynchronously: the endpoint verifies the build exists and
        then hands it off to a background workflow that marks the build as cancelling,
        asks the cloud build provider to stop it, and polls until the build reaches a
        terminal state before recording the final status. Only builds that are still
        queued or running are actually cancelled; if the build has already finished, or
        cancellation is already in progress, the request is still accepted but has no
        effect. The returned record reflects the build's state at the time of the call,
        so it will not yet show the pending cancellation. The request is rejected if no
        such build exists for the caller's account.

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
        List agents that exist only as cloud builds and have no healthy deployment yet.

        Unlike listing builds, this aggregates by agent: it returns one entry per
        distinct agent name whose builds have never reached a healthy deploy, each
        carrying that agent's most recent build and its total build count. The result is
        a plain list (not paginated) and is limited to builds the caller is permitted to
        read. Use this to surface agents that were built but still need to be deployed;
        use `GET /v5/builds` when you need the individual build records instead.
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
        Stream a build's logs as Server-Sent Events.

        The response has content-type `text/event-stream`; each event carries one log
        line as an `AgentexCloudBuildLogLine` object, delivered as lines become
        available from the cloud build provider. The stream ends when the provider stops
        producing output. Responds with a not-found error if no such build exists for
        the caller's account.

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
