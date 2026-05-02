# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import deploy_list_params, deploy_logs_params, deploy_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from .._base_client import AsyncPaginator, make_request_options
from ..types.chat.sort_order import SortOrder
from ..types.agentex_cloud_deploy import AgentexCloudDeploy
from ..types.deploy_logs_response import DeployLogsResponse

__all__ = ["DeployResource", "AsyncDeployResource"]


class DeployResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DeployResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return DeployResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DeployResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return DeployResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        environment_config: str,
        manifest_file: str,
        build_id: str | Omit = omit,
        image_name: str | Omit = omit,
        image_tag: str | Omit = omit,
        preview: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudDeploy:
        """Create a new deployment.

        Submits a deployment request.

        The deployment will:

        1. Parse and merge configuration files
        2. Create a Kubernetes Job running helm install
        3. Wait for deployment completion
        4. Return results

        Args:
          build_id: The build_id of the cloud build. Required if image_name and image_tag are not
              provided.

          image_name: Name of the image to deploy. Required if build_id is not provided.

          image_tag: Tag of the image to deploy. Required if build_id is not provided.

          preview: When True, creates a preview deployment with a unique slug appended to the helm
              release name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/agentex/deployments",
            body=maybe_transform(
                {
                    "environment_config": environment_config,
                    "manifest_file": manifest_file,
                    "build_id": build_id,
                    "image_name": image_name,
                    "image_tag": image_tag,
                    "preview": preview,
                },
                deploy_create_params.DeployCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudDeploy,
        )

    def retrieve(
        self,
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudDeploy:
        """
        Get a deployment by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            path_template("/v5/agentex/deployments/{deployment_id}", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudDeploy,
        )

    def list(
        self,
        *,
        agent_name: str | Omit = omit,
        build_id: str | Omit = omit,
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
    ) -> SyncCursorPage[AgentexCloudDeploy]:
        """
        List all deployments with pagination and optional filters.

        Args:
          agent_name: Filter deployments by agent name (via associated build)

          build_id: Filter deployments by build ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/agentex/deployments",
            page=SyncCursorPage[AgentexCloudDeploy],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_name": agent_name,
                        "build_id": build_id,
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    deploy_list_params.DeployListParams,
                ),
            ),
            model=AgentexCloudDeploy,
        )

    def logs(
        self,
        deployment_id: str,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeployLogsResponse:
        """
        Get structured log lines for a deployment with cursor-based pagination.

        The CLI can poll this endpoint to stream logs incrementally:

        1. First call: no cursor
        2. Subsequent calls: cursor=next_cursor from the previous response
        3. Stop polling when the deployment reaches a terminal status

        Args:
          cursor: Cursor from previous response's next_cursor field

          limit: Maximum number of log lines to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._get(
            path_template("/v5/agentex/deployments/{deployment_id}/logs", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    deploy_logs_params.DeployLogsParams,
                ),
            ),
            cast_to=DeployLogsResponse,
        )


class AsyncDeployResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDeployResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncDeployResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDeployResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncDeployResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        environment_config: str,
        manifest_file: str,
        build_id: str | Omit = omit,
        image_name: str | Omit = omit,
        image_tag: str | Omit = omit,
        preview: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudDeploy:
        """Create a new deployment.

        Submits a deployment request.

        The deployment will:

        1. Parse and merge configuration files
        2. Create a Kubernetes Job running helm install
        3. Wait for deployment completion
        4. Return results

        Args:
          build_id: The build_id of the cloud build. Required if image_name and image_tag are not
              provided.

          image_name: Name of the image to deploy. Required if build_id is not provided.

          image_tag: Tag of the image to deploy. Required if build_id is not provided.

          preview: When True, creates a preview deployment with a unique slug appended to the helm
              release name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/agentex/deployments",
            body=await async_maybe_transform(
                {
                    "environment_config": environment_config,
                    "manifest_file": manifest_file,
                    "build_id": build_id,
                    "image_name": image_name,
                    "image_tag": image_tag,
                    "preview": preview,
                },
                deploy_create_params.DeployCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudDeploy,
        )

    async def retrieve(
        self,
        deployment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudDeploy:
        """
        Get a deployment by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            path_template("/v5/agentex/deployments/{deployment_id}", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudDeploy,
        )

    def list(
        self,
        *,
        agent_name: str | Omit = omit,
        build_id: str | Omit = omit,
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
    ) -> AsyncPaginator[AgentexCloudDeploy, AsyncCursorPage[AgentexCloudDeploy]]:
        """
        List all deployments with pagination and optional filters.

        Args:
          agent_name: Filter deployments by agent name (via associated build)

          build_id: Filter deployments by build ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/agentex/deployments",
            page=AsyncCursorPage[AgentexCloudDeploy],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_name": agent_name,
                        "build_id": build_id,
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    deploy_list_params.DeployListParams,
                ),
            ),
            model=AgentexCloudDeploy,
        )

    async def logs(
        self,
        deployment_id: str,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeployLogsResponse:
        """
        Get structured log lines for a deployment with cursor-based pagination.

        The CLI can poll this endpoint to stream logs incrementally:

        1. First call: no cursor
        2. Subsequent calls: cursor=next_cursor from the previous response
        3. Stop polling when the deployment reaches a terminal status

        Args:
          cursor: Cursor from previous response's next_cursor field

          limit: Maximum number of log lines to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._get(
            path_template("/v5/agentex/deployments/{deployment_id}/logs", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    deploy_logs_params.DeployLogsParams,
                ),
            ),
            cast_to=DeployLogsResponse,
        )


class DeployResourceWithRawResponse:
    def __init__(self, deploy: DeployResource) -> None:
        self._deploy = deploy

        self.create = to_raw_response_wrapper(
            deploy.create,
        )
        self.retrieve = to_raw_response_wrapper(
            deploy.retrieve,
        )
        self.list = to_raw_response_wrapper(
            deploy.list,
        )
        self.logs = to_raw_response_wrapper(
            deploy.logs,
        )


class AsyncDeployResourceWithRawResponse:
    def __init__(self, deploy: AsyncDeployResource) -> None:
        self._deploy = deploy

        self.create = async_to_raw_response_wrapper(
            deploy.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            deploy.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            deploy.list,
        )
        self.logs = async_to_raw_response_wrapper(
            deploy.logs,
        )


class DeployResourceWithStreamingResponse:
    def __init__(self, deploy: DeployResource) -> None:
        self._deploy = deploy

        self.create = to_streamed_response_wrapper(
            deploy.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            deploy.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            deploy.list,
        )
        self.logs = to_streamed_response_wrapper(
            deploy.logs,
        )


class AsyncDeployResourceWithStreamingResponse:
    def __init__(self, deploy: AsyncDeployResource) -> None:
        self._deploy = deploy

        self.create = async_to_streamed_response_wrapper(
            deploy.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            deploy.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            deploy.list,
        )
        self.logs = async_to_streamed_response_wrapper(
            deploy.logs,
        )
