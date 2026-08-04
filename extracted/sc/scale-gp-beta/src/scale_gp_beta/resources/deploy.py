# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime

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
        expires_at: Union[str, datetime] | Omit = omit,
        image_name: str | Omit = omit,
        image_tag: str | Omit = omit,
        preview: bool | Omit = omit,
        preview_label: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudDeploy:
        """
        Deploy a successfully built agent image to Kubernetes as a Helm release.

        Takes a completed build (referenced by `build_id`, or by `image_name` +
        `image_tag`) together with the agent manifest and environment config, then
        starts an asynchronous Temporal workflow that provisions the agent as a Helm
        release. The call returns immediately with the deployment record in `PENDING`
        status — it does not wait for the release to become healthy; poll
        `GET /v5/agentex/deployments/{deployment_id}` for status and Kubernetes events
        and `GET /v5/agentex/deployments/{deployment_id}/logs` for progress. This is the
        deploy counterpart to `POST /v5/agentex/builds`: a build produces the container
        image, a deployment runs that image. The referenced build must have finished
        successfully, and the manifest's agent name must match the build's agent.

        Set `preview=True` for an ephemeral deployment: it gets a globally unique Helm
        release name (so concurrent redeploys never collide), an optional
        `preview_label` for grouping, and an expiry (`expires_at`, defaulting to 8 hours
        from now); `preview_label` and `expires_at` are rejected on non-preview deploys.
        A non-preview (production) deploy instead supersedes any prior active deployment
        that shares its Helm release name. Fails with a client error if the build is
        missing or not in a successful state, if the manifest or environment YAML is
        invalid or their agent names disagree, or if a secret referenced by the manifest
        does not exist.

        Args:
          environment_config: YAML content of environment configuration from the environment config file.

          manifest_file: YAML content of manifest configuration.

          build_id: The build_id of the cloud build. Required if image_name and image_tag are not
              provided.

          expires_at: ISO 8601 expiry timestamp. Only valid for preview deployments. If omitted on a
              preview deployment, defaults to 8 hours from now. Previews are always ephemeral
              and always have an expires_at.

          image_name: Name of the image to deploy. Required if build_id is not provided.

          image_tag: Tag of the image to deploy. Required if build_id is not provided.

          preview: When True, creates a preview deployment with a unique deployment-id suffix
              appended to the helm release name.

          preview_label: Non-unique grouping label for the preview (e.g. branch name, PR number).
              Persisted on the deployment record so callers can list all deploys for a given
              label via `GET /v5/agentex/deployments?preview_label=X&limit=1` (get the
              latest). Sanitized to lowercase alphanumeric + hyphens for K8s DNS-label
              compatibility (max 30 characters after sanitization). Each deploy still gets a
              unique helm release name regardless of label, so concurrent redeploys never
              share K8s resources. Only valid when preview=True.

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
                    "expires_at": expires_at,
                    "image_name": image_name,
                    "image_tag": image_tag,
                    "preview": preview,
                    "preview_label": preview_label,
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
        Get a single agent deployment by ID, including its current status and Kubernetes
        events.

        Returns the deployment record with its latest status and the associated
        Kubernetes events (`deploy_events`) observed for the release, which are useful
        for diagnosing why a deployment is still pending or unhealthy. Poll this after
        `POST /v5/agentex/deployments` to track the asynchronous deploy to completion.
        For the incremental log output rather than status and events, use
        `GET /v5/agentex/deployments/{deployment_id}/logs`. Returns 404 if no deployment
        with this ID exists for the caller's account.

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
        preview_label: str | Omit = omit,
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
        List the account's agent deployments, with pagination and optional filters.

        Returns the deployments the caller is authorized to read. Optionally filter by
        `build_id`, by `agent_name` (matched through each deployment's associated
        build), or by `preview_label`. A `preview_label` is non-unique — many
        deployments can share one (for example every deploy for a branch) — so combine
        it with `limit=1` to fetch the latest deployment for that label. This lists
        deployments (the running or attempted agent instances); to list the image builds
        they run, use the agentex builds API.

        Args:
          agent_name: Filter deployments by agent name (via associated build)

          build_id: Filter deployments by build ID

          preview_label: Filter deployments by preview label (e.g. branch name). The label is non-unique
              — many deployments can share it. Combine with limit=1 to get the latest deploy
              for that label.

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
                        "preview_label": preview_label,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    deploy_list_params.DeployListParams,
                ),
            ),
            model=AgentexCloudDeploy,
        )

    def delete(
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
        Delete an agent deployment and tear down its Kubernetes resources.

        Deletes the deployment's Kubernetes resources first, then marks the record as
        `DELETED`; the underlying Helm release is subsequently uninstalled
        asynchronously by FluxCD once the resource is removed. If the Kubernetes
        teardown fails, the record is left unchanged and the call errors, so the delete
        can be safely retried. Rejects the call with a client error if the deployment is
        already in a terminal state (`DELETED`, `CANCELLED`, or `SUPERSEDED`) — a
        `SUPERSEDED` record shares its Helm release with the deployment that replaced
        it, so deleting it would tear down the live release. Returns 404 if no
        deployment with this ID exists for the caller's account. This removes a running
        deployment, not the image build behind it, which is managed separately through
        the agentex builds API.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return self._delete(
            path_template("/v5/agentex/deployments/{deployment_id}", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudDeploy,
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
        Get structured deployment log lines, with cursor-based pagination.

        Returns the deployment's log lines in time order together with a `next_cursor`
        and a `has_more` flag. Poll to stream logs incrementally: make the first call
        without a cursor, then pass the previous response's `next_cursor` as `cursor` on
        each subsequent call, stopping once the deployment reaches a terminal status.
        Unlike `GET /v5/agentex/deployments/{deployment_id}`, which returns the
        deployment's status and Kubernetes events, this returns the raw log output from
        the deploy process. Returns 404 if no deployment with this ID exists for the
        caller's account.

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
        expires_at: Union[str, datetime] | Omit = omit,
        image_name: str | Omit = omit,
        image_tag: str | Omit = omit,
        preview: bool | Omit = omit,
        preview_label: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentexCloudDeploy:
        """
        Deploy a successfully built agent image to Kubernetes as a Helm release.

        Takes a completed build (referenced by `build_id`, or by `image_name` +
        `image_tag`) together with the agent manifest and environment config, then
        starts an asynchronous Temporal workflow that provisions the agent as a Helm
        release. The call returns immediately with the deployment record in `PENDING`
        status — it does not wait for the release to become healthy; poll
        `GET /v5/agentex/deployments/{deployment_id}` for status and Kubernetes events
        and `GET /v5/agentex/deployments/{deployment_id}/logs` for progress. This is the
        deploy counterpart to `POST /v5/agentex/builds`: a build produces the container
        image, a deployment runs that image. The referenced build must have finished
        successfully, and the manifest's agent name must match the build's agent.

        Set `preview=True` for an ephemeral deployment: it gets a globally unique Helm
        release name (so concurrent redeploys never collide), an optional
        `preview_label` for grouping, and an expiry (`expires_at`, defaulting to 8 hours
        from now); `preview_label` and `expires_at` are rejected on non-preview deploys.
        A non-preview (production) deploy instead supersedes any prior active deployment
        that shares its Helm release name. Fails with a client error if the build is
        missing or not in a successful state, if the manifest or environment YAML is
        invalid or their agent names disagree, or if a secret referenced by the manifest
        does not exist.

        Args:
          environment_config: YAML content of environment configuration from the environment config file.

          manifest_file: YAML content of manifest configuration.

          build_id: The build_id of the cloud build. Required if image_name and image_tag are not
              provided.

          expires_at: ISO 8601 expiry timestamp. Only valid for preview deployments. If omitted on a
              preview deployment, defaults to 8 hours from now. Previews are always ephemeral
              and always have an expires_at.

          image_name: Name of the image to deploy. Required if build_id is not provided.

          image_tag: Tag of the image to deploy. Required if build_id is not provided.

          preview: When True, creates a preview deployment with a unique deployment-id suffix
              appended to the helm release name.

          preview_label: Non-unique grouping label for the preview (e.g. branch name, PR number).
              Persisted on the deployment record so callers can list all deploys for a given
              label via `GET /v5/agentex/deployments?preview_label=X&limit=1` (get the
              latest). Sanitized to lowercase alphanumeric + hyphens for K8s DNS-label
              compatibility (max 30 characters after sanitization). Each deploy still gets a
              unique helm release name regardless of label, so concurrent redeploys never
              share K8s resources. Only valid when preview=True.

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
                    "expires_at": expires_at,
                    "image_name": image_name,
                    "image_tag": image_tag,
                    "preview": preview,
                    "preview_label": preview_label,
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
        Get a single agent deployment by ID, including its current status and Kubernetes
        events.

        Returns the deployment record with its latest status and the associated
        Kubernetes events (`deploy_events`) observed for the release, which are useful
        for diagnosing why a deployment is still pending or unhealthy. Poll this after
        `POST /v5/agentex/deployments` to track the asynchronous deploy to completion.
        For the incremental log output rather than status and events, use
        `GET /v5/agentex/deployments/{deployment_id}/logs`. Returns 404 if no deployment
        with this ID exists for the caller's account.

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
        preview_label: str | Omit = omit,
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
        List the account's agent deployments, with pagination and optional filters.

        Returns the deployments the caller is authorized to read. Optionally filter by
        `build_id`, by `agent_name` (matched through each deployment's associated
        build), or by `preview_label`. A `preview_label` is non-unique — many
        deployments can share one (for example every deploy for a branch) — so combine
        it with `limit=1` to fetch the latest deployment for that label. This lists
        deployments (the running or attempted agent instances); to list the image builds
        they run, use the agentex builds API.

        Args:
          agent_name: Filter deployments by agent name (via associated build)

          build_id: Filter deployments by build ID

          preview_label: Filter deployments by preview label (e.g. branch name). The label is non-unique
              — many deployments can share it. Combine with limit=1 to get the latest deploy
              for that label.

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
                        "preview_label": preview_label,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    deploy_list_params.DeployListParams,
                ),
            ),
            model=AgentexCloudDeploy,
        )

    async def delete(
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
        Delete an agent deployment and tear down its Kubernetes resources.

        Deletes the deployment's Kubernetes resources first, then marks the record as
        `DELETED`; the underlying Helm release is subsequently uninstalled
        asynchronously by FluxCD once the resource is removed. If the Kubernetes
        teardown fails, the record is left unchanged and the call errors, so the delete
        can be safely retried. Rejects the call with a client error if the deployment is
        already in a terminal state (`DELETED`, `CANCELLED`, or `SUPERSEDED`) — a
        `SUPERSEDED` record shares its Helm release with the deployment that replaced
        it, so deleting it would tear down the live release. Returns 404 if no
        deployment with this ID exists for the caller's account. This removes a running
        deployment, not the image build behind it, which is managed separately through
        the agentex builds API.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not deployment_id:
            raise ValueError(f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}")
        return await self._delete(
            path_template("/v5/agentex/deployments/{deployment_id}", deployment_id=deployment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentexCloudDeploy,
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
        Get structured deployment log lines, with cursor-based pagination.

        Returns the deployment's log lines in time order together with a `next_cursor`
        and a `has_more` flag. Poll to stream logs incrementally: make the first call
        without a cursor, then pass the previous response's `next_cursor` as `cursor` on
        each subsequent call, stopping once the deployment reaches a terminal status.
        Unlike `GET /v5/agentex/deployments/{deployment_id}`, which returns the
        deployment's status and Kubernetes events, this returns the raw log output from
        the deploy process. Returns 404 if no deployment with this ID exists for the
        caller's account.

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
        self.delete = to_raw_response_wrapper(
            deploy.delete,
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
        self.delete = async_to_raw_response_wrapper(
            deploy.delete,
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
        self.delete = to_streamed_response_wrapper(
            deploy.delete,
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
        self.delete = async_to_streamed_response_wrapper(
            deploy.delete,
        )
        self.logs = async_to_streamed_response_wrapper(
            deploy.logs,
        )
