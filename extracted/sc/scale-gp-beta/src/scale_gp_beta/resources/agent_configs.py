# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ..types import agent_config_list_params, agent_config_create_params, agent_config_update_params
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
from ..types.repo_spec_param import RepoSpecParam
from ..types.agent_config_list_response import AgentConfigListResponse
from ..types.agent_config_create_response import AgentConfigCreateResponse
from ..types.agent_config_delete_response import AgentConfigDeleteResponse
from ..types.agent_config_update_response import AgentConfigUpdateResponse
from ..types.agent_config_retrieve_response import AgentConfigRetrieveResponse
from ..types.agent_config_list_mcp_tools_response import AgentConfigListMcpToolsResponse

__all__ = ["AgentConfigsResource", "AsyncAgentConfigsResource"]


class AgentConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AgentConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AgentConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AgentConfigsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        harness: Literal["claude-code", "codex", "litellm"],
        model: str,
        name: str,
        system_prompt: str,
        allowed_tools: List[
            Literal[
                "Read",
                "Write",
                "Edit",
                "Bash",
                "Glob",
                "Grep",
                "List",
                "WebFetch",
                "WebSearch",
                "Task",
                "TodoWrite",
                "NotebookEdit",
                "ExitPlanMode",
                "Slack",
                "Linear",
                "GitHub",
                "Confluence",
                "Notion",
                "Datadog",
                "PagerDuty",
                "Salesforce",
                "Figma",
                "Granola",
                "Jira",
                "Gmail",
                "GoogleCalendar",
                "GoogleDrive",
                "GoogleDocs",
                "GoogleSheets",
                "GoogleSlides",
                "Snowflake",
                "Redash",
                "Tableau",
                "Metabase",
                "Gong",
                "ZoomInfo",
                "Clay",
            ]
        ]
        | Omit = omit,
        description: str | Omit = omit,
        persistent_workspace: bool | Omit = omit,
        repos: Iterable[RepoSpecParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigCreateResponse:
        """
        Create a reusable agent configuration (system prompt, harness, model, allowed
        tools) under the caller's account.

        The config is a template that a chat session or a non-chat trigger later turns
        into task params; creating one does not start any task. `persistent_workspace`
        opts tasks made from this config into a durable `/workspace` that survives
        sandbox death (off by default, and fixed once a task starts), and `repos`
        overrides which repositories provisioning clones into that workspace — omit it
        (null) to use the deployment default, or pass an empty list to clone nothing. A
        `repos` override is rejected with a 422 on the model-agnostic (litellm) harness
        unless `persistent_workspace` is also true, because non-persistent litellm tasks
        run in a pre-cloned warm-pool sandbox where the override would be ignored.
        `allowed_tools` may name MCP servers (Slack, Linear, GitHub, ...) alongside
        harness tools, and granting an MCP server name authorizes every tool it exposes.

        Args:
          harness: Harness strategy. See Harness enum for supported values.

          allowed_tools: Tools enabled for this config. See AllowedTool enum for the catalogue.

          persistent_workspace: Give tasks a persistent /workspace that survives sandbox death. Fixed for a
              task's life; defaults off.

          repos: Per-config repo override. None uses the deployment default; an empty list clones
              nothing.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/agent_configs",
            body=maybe_transform(
                {
                    "harness": harness,
                    "model": model,
                    "name": name,
                    "system_prompt": system_prompt,
                    "allowed_tools": allowed_tools,
                    "description": description,
                    "persistent_workspace": persistent_workspace,
                    "repos": repos,
                },
                agent_config_create_params.AgentConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigCreateResponse,
        )

    def retrieve(
        self,
        agent_config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigRetrieveResponse:
        """
        Fetch a single stored agent configuration by id, including its
        `persistent_workspace` flag and any `repos` override.

        This returns the saved record as-is and does not compute task params; use
        `{agent_config_id}/resolve` when you need the config projected into the params a
        task would run with. A user caller can only read a config they created unless
        fine-grained access control grants access, while a service account can read any
        config under the account; a missing or out-of-scope id returns a 404.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_config_id:
            raise ValueError(f"Expected a non-empty value for `agent_config_id` but received {agent_config_id!r}")
        return self._get(
            path_template("/v5/agent_configs/{agent_config_id}", agent_config_id=agent_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigRetrieveResponse,
        )

    def update(
        self,
        agent_config_id: str,
        *,
        task_id: str | Omit = omit,
        allowed_tools: List[
            Literal[
                "Read",
                "Write",
                "Edit",
                "Bash",
                "Glob",
                "Grep",
                "List",
                "WebFetch",
                "WebSearch",
                "Task",
                "TodoWrite",
                "NotebookEdit",
                "ExitPlanMode",
                "Slack",
                "Linear",
                "GitHub",
                "Confluence",
                "Notion",
                "Datadog",
                "PagerDuty",
                "Salesforce",
                "Figma",
                "Granola",
                "Jira",
                "Gmail",
                "GoogleCalendar",
                "GoogleDrive",
                "GoogleDocs",
                "GoogleSheets",
                "GoogleSlides",
                "Snowflake",
                "Redash",
                "Tableau",
                "Metabase",
                "Gong",
                "ZoomInfo",
                "Clay",
            ]
        ]
        | Omit = omit,
        description: str | Omit = omit,
        harness: Literal["claude-code", "codex", "litellm"] | Omit = omit,
        model: str | Omit = omit,
        name: str | Omit = omit,
        persistent_workspace: bool | Omit = omit,
        repos: Iterable[RepoSpecParam] | Omit = omit,
        system_prompt: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigUpdateResponse:
        """
        Partially update a stored agent config; only fields present in the request body
        are changed.

        `persistent_workspace` and `repos` are both patchable — an explicit null on
        `repos` clears the override back to the deployment default, while the
        always-present fields (name, system_prompt, harness, allowed_tools, model, and
        persistent_workspace) reject an explicit null. Because `persistent_workspace`
        and `repos` are read when a task is created and are fixed for a task's life,
        changing them affects only tasks created afterward, not one already running. The
        optional `task_id` query parameter opts into a live-config side effect: after
        the row is persisted, the changed pass-through fields (system_prompt, model,
        harness, and allowed_tools split into harness tools versus MCP servers) are
        shallow-merged into that running task's params on Agentex in a background task
        so the worker picks them up on its next turn; `persistent_workspace` and `repos`
        are intentionally not forwarded to a running task. That side effect runs after
        the response is sent, is best-effort, and no-ops if the task does not exist or
        the caller does not own it. A user caller can only update a config they created
        unless fine-grained access control grants access.

        Args:
          task_id: If set, after persisting the patch we shallow-merge the changed fields into this
              task's params column on Agentex so the worker picks up the new values on its
              next turn. Caller-provided context — Agentex enforces task ownership via its own
              auth, so the side-effect no-ops if the caller doesn't own the task.

          harness: Supported agent harness strategies.

              Mirrors `PROVIDERS` in golden-agent's `project/harness/activity.py`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_config_id:
            raise ValueError(f"Expected a non-empty value for `agent_config_id` but received {agent_config_id!r}")
        return self._patch(
            path_template("/v5/agent_configs/{agent_config_id}", agent_config_id=agent_config_id),
            body=maybe_transform(
                {
                    "allowed_tools": allowed_tools,
                    "description": description,
                    "harness": harness,
                    "model": model,
                    "name": name,
                    "persistent_workspace": persistent_workspace,
                    "repos": repos,
                    "system_prompt": system_prompt,
                },
                agent_config_update_params.AgentConfigUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"task_id": task_id}, agent_config_update_params.AgentConfigUpdateParams),
            ),
            cast_to=AgentConfigUpdateResponse,
        )

    def list(
        self,
        *,
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
    ) -> SyncCursorPage[AgentConfigListResponse]:
        """
        List agent configurations visible to the caller, with cursor-based pagination.

        A user caller sees only the configs they created unless fine-grained access
        control (FGAC) grants them access to others; a service-account caller sees every
        config under the account. This returns the stored config records as-is — use
        `{agent_config_id}/resolve` instead when you need a config projected into the
        params a task would run with. Because deleting a config removes it outright
        rather than archiving it, there are no archived configs to page through here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/agent_configs",
            page=SyncCursorPage[AgentConfigListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    agent_config_list_params.AgentConfigListParams,
                ),
            ),
            model=AgentConfigListResponse,
        )

    def delete(
        self,
        agent_config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigDeleteResponse:
        """
        Permanently delete an agent config; this is a hard delete, not an archive, so
        the row is removed and cannot be restored.

        Because a config is only a template, deleting it does not stop or alter any task
        already created from it. A user caller can only delete a config they created
        unless fine-grained access control grants access. The response echoes the
        deleted id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_config_id:
            raise ValueError(f"Expected a non-empty value for `agent_config_id` but received {agent_config_id!r}")
        return self._delete(
            path_template("/v5/agent_configs/{agent_config_id}", agent_config_id=agent_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigDeleteResponse,
        )

    def list_mcp_tools(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigListMcpToolsResponse:
        """
        Return the fixed set of tool names that route to MCP servers rather than
        harness-provided tools.

        These are the subset of `allowed_tools` values (Slack, Linear, GitHub, ...) the
        platform treats as MCP servers; the list is a static enum, not account data, so
        it is identical for every caller. It is exposed mainly so the generated SDK
        carries the `McpTool` type and the frontend can assert its own
        MCP-versus-harness tool classifier against the backend to prevent drift. It does
        not list configs or the tools actually granted to any particular config.
        """
        return self._get(
            "/v5/agent_configs/mcp_tools",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigListMcpToolsResponse,
        )


class AsyncAgentConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAgentConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncAgentConfigsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        harness: Literal["claude-code", "codex", "litellm"],
        model: str,
        name: str,
        system_prompt: str,
        allowed_tools: List[
            Literal[
                "Read",
                "Write",
                "Edit",
                "Bash",
                "Glob",
                "Grep",
                "List",
                "WebFetch",
                "WebSearch",
                "Task",
                "TodoWrite",
                "NotebookEdit",
                "ExitPlanMode",
                "Slack",
                "Linear",
                "GitHub",
                "Confluence",
                "Notion",
                "Datadog",
                "PagerDuty",
                "Salesforce",
                "Figma",
                "Granola",
                "Jira",
                "Gmail",
                "GoogleCalendar",
                "GoogleDrive",
                "GoogleDocs",
                "GoogleSheets",
                "GoogleSlides",
                "Snowflake",
                "Redash",
                "Tableau",
                "Metabase",
                "Gong",
                "ZoomInfo",
                "Clay",
            ]
        ]
        | Omit = omit,
        description: str | Omit = omit,
        persistent_workspace: bool | Omit = omit,
        repos: Iterable[RepoSpecParam] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigCreateResponse:
        """
        Create a reusable agent configuration (system prompt, harness, model, allowed
        tools) under the caller's account.

        The config is a template that a chat session or a non-chat trigger later turns
        into task params; creating one does not start any task. `persistent_workspace`
        opts tasks made from this config into a durable `/workspace` that survives
        sandbox death (off by default, and fixed once a task starts), and `repos`
        overrides which repositories provisioning clones into that workspace — omit it
        (null) to use the deployment default, or pass an empty list to clone nothing. A
        `repos` override is rejected with a 422 on the model-agnostic (litellm) harness
        unless `persistent_workspace` is also true, because non-persistent litellm tasks
        run in a pre-cloned warm-pool sandbox where the override would be ignored.
        `allowed_tools` may name MCP servers (Slack, Linear, GitHub, ...) alongside
        harness tools, and granting an MCP server name authorizes every tool it exposes.

        Args:
          harness: Harness strategy. See Harness enum for supported values.

          allowed_tools: Tools enabled for this config. See AllowedTool enum for the catalogue.

          persistent_workspace: Give tasks a persistent /workspace that survives sandbox death. Fixed for a
              task's life; defaults off.

          repos: Per-config repo override. None uses the deployment default; an empty list clones
              nothing.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/agent_configs",
            body=await async_maybe_transform(
                {
                    "harness": harness,
                    "model": model,
                    "name": name,
                    "system_prompt": system_prompt,
                    "allowed_tools": allowed_tools,
                    "description": description,
                    "persistent_workspace": persistent_workspace,
                    "repos": repos,
                },
                agent_config_create_params.AgentConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigCreateResponse,
        )

    async def retrieve(
        self,
        agent_config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigRetrieveResponse:
        """
        Fetch a single stored agent configuration by id, including its
        `persistent_workspace` flag and any `repos` override.

        This returns the saved record as-is and does not compute task params; use
        `{agent_config_id}/resolve` when you need the config projected into the params a
        task would run with. A user caller can only read a config they created unless
        fine-grained access control grants access, while a service account can read any
        config under the account; a missing or out-of-scope id returns a 404.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_config_id:
            raise ValueError(f"Expected a non-empty value for `agent_config_id` but received {agent_config_id!r}")
        return await self._get(
            path_template("/v5/agent_configs/{agent_config_id}", agent_config_id=agent_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigRetrieveResponse,
        )

    async def update(
        self,
        agent_config_id: str,
        *,
        task_id: str | Omit = omit,
        allowed_tools: List[
            Literal[
                "Read",
                "Write",
                "Edit",
                "Bash",
                "Glob",
                "Grep",
                "List",
                "WebFetch",
                "WebSearch",
                "Task",
                "TodoWrite",
                "NotebookEdit",
                "ExitPlanMode",
                "Slack",
                "Linear",
                "GitHub",
                "Confluence",
                "Notion",
                "Datadog",
                "PagerDuty",
                "Salesforce",
                "Figma",
                "Granola",
                "Jira",
                "Gmail",
                "GoogleCalendar",
                "GoogleDrive",
                "GoogleDocs",
                "GoogleSheets",
                "GoogleSlides",
                "Snowflake",
                "Redash",
                "Tableau",
                "Metabase",
                "Gong",
                "ZoomInfo",
                "Clay",
            ]
        ]
        | Omit = omit,
        description: str | Omit = omit,
        harness: Literal["claude-code", "codex", "litellm"] | Omit = omit,
        model: str | Omit = omit,
        name: str | Omit = omit,
        persistent_workspace: bool | Omit = omit,
        repos: Iterable[RepoSpecParam] | Omit = omit,
        system_prompt: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigUpdateResponse:
        """
        Partially update a stored agent config; only fields present in the request body
        are changed.

        `persistent_workspace` and `repos` are both patchable — an explicit null on
        `repos` clears the override back to the deployment default, while the
        always-present fields (name, system_prompt, harness, allowed_tools, model, and
        persistent_workspace) reject an explicit null. Because `persistent_workspace`
        and `repos` are read when a task is created and are fixed for a task's life,
        changing them affects only tasks created afterward, not one already running. The
        optional `task_id` query parameter opts into a live-config side effect: after
        the row is persisted, the changed pass-through fields (system_prompt, model,
        harness, and allowed_tools split into harness tools versus MCP servers) are
        shallow-merged into that running task's params on Agentex in a background task
        so the worker picks them up on its next turn; `persistent_workspace` and `repos`
        are intentionally not forwarded to a running task. That side effect runs after
        the response is sent, is best-effort, and no-ops if the task does not exist or
        the caller does not own it. A user caller can only update a config they created
        unless fine-grained access control grants access.

        Args:
          task_id: If set, after persisting the patch we shallow-merge the changed fields into this
              task's params column on Agentex so the worker picks up the new values on its
              next turn. Caller-provided context — Agentex enforces task ownership via its own
              auth, so the side-effect no-ops if the caller doesn't own the task.

          harness: Supported agent harness strategies.

              Mirrors `PROVIDERS` in golden-agent's `project/harness/activity.py`.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_config_id:
            raise ValueError(f"Expected a non-empty value for `agent_config_id` but received {agent_config_id!r}")
        return await self._patch(
            path_template("/v5/agent_configs/{agent_config_id}", agent_config_id=agent_config_id),
            body=await async_maybe_transform(
                {
                    "allowed_tools": allowed_tools,
                    "description": description,
                    "harness": harness,
                    "model": model,
                    "name": name,
                    "persistent_workspace": persistent_workspace,
                    "repos": repos,
                    "system_prompt": system_prompt,
                },
                agent_config_update_params.AgentConfigUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"task_id": task_id}, agent_config_update_params.AgentConfigUpdateParams
                ),
            ),
            cast_to=AgentConfigUpdateResponse,
        )

    def list(
        self,
        *,
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
    ) -> AsyncPaginator[AgentConfigListResponse, AsyncCursorPage[AgentConfigListResponse]]:
        """
        List agent configurations visible to the caller, with cursor-based pagination.

        A user caller sees only the configs they created unless fine-grained access
        control (FGAC) grants them access to others; a service-account caller sees every
        config under the account. This returns the stored config records as-is — use
        `{agent_config_id}/resolve` instead when you need a config projected into the
        params a task would run with. Because deleting a config removes it outright
        rather than archiving it, there are no archived configs to page through here.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/agent_configs",
            page=AsyncCursorPage[AgentConfigListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    agent_config_list_params.AgentConfigListParams,
                ),
            ),
            model=AgentConfigListResponse,
        )

    async def delete(
        self,
        agent_config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigDeleteResponse:
        """
        Permanently delete an agent config; this is a hard delete, not an archive, so
        the row is removed and cannot be restored.

        Because a config is only a template, deleting it does not stop or alter any task
        already created from it. A user caller can only delete a config they created
        unless fine-grained access control grants access. The response echoes the
        deleted id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_config_id:
            raise ValueError(f"Expected a non-empty value for `agent_config_id` but received {agent_config_id!r}")
        return await self._delete(
            path_template("/v5/agent_configs/{agent_config_id}", agent_config_id=agent_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigDeleteResponse,
        )

    async def list_mcp_tools(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentConfigListMcpToolsResponse:
        """
        Return the fixed set of tool names that route to MCP servers rather than
        harness-provided tools.

        These are the subset of `allowed_tools` values (Slack, Linear, GitHub, ...) the
        platform treats as MCP servers; the list is a static enum, not account data, so
        it is identical for every caller. It is exposed mainly so the generated SDK
        carries the `McpTool` type and the frontend can assert its own
        MCP-versus-harness tool classifier against the backend to prevent drift. It does
        not list configs or the tools actually granted to any particular config.
        """
        return await self._get(
            "/v5/agent_configs/mcp_tools",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentConfigListMcpToolsResponse,
        )


class AgentConfigsResourceWithRawResponse:
    def __init__(self, agent_configs: AgentConfigsResource) -> None:
        self._agent_configs = agent_configs

        self.create = to_raw_response_wrapper(
            agent_configs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            agent_configs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            agent_configs.update,
        )
        self.list = to_raw_response_wrapper(
            agent_configs.list,
        )
        self.delete = to_raw_response_wrapper(
            agent_configs.delete,
        )
        self.list_mcp_tools = to_raw_response_wrapper(
            agent_configs.list_mcp_tools,
        )


class AsyncAgentConfigsResourceWithRawResponse:
    def __init__(self, agent_configs: AsyncAgentConfigsResource) -> None:
        self._agent_configs = agent_configs

        self.create = async_to_raw_response_wrapper(
            agent_configs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            agent_configs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            agent_configs.update,
        )
        self.list = async_to_raw_response_wrapper(
            agent_configs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            agent_configs.delete,
        )
        self.list_mcp_tools = async_to_raw_response_wrapper(
            agent_configs.list_mcp_tools,
        )


class AgentConfigsResourceWithStreamingResponse:
    def __init__(self, agent_configs: AgentConfigsResource) -> None:
        self._agent_configs = agent_configs

        self.create = to_streamed_response_wrapper(
            agent_configs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            agent_configs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            agent_configs.update,
        )
        self.list = to_streamed_response_wrapper(
            agent_configs.list,
        )
        self.delete = to_streamed_response_wrapper(
            agent_configs.delete,
        )
        self.list_mcp_tools = to_streamed_response_wrapper(
            agent_configs.list_mcp_tools,
        )


class AsyncAgentConfigsResourceWithStreamingResponse:
    def __init__(self, agent_configs: AsyncAgentConfigsResource) -> None:
        self._agent_configs = agent_configs

        self.create = async_to_streamed_response_wrapper(
            agent_configs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            agent_configs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            agent_configs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            agent_configs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            agent_configs.delete,
        )
        self.list_mcp_tools = async_to_streamed_response_wrapper(
            agent_configs.list_mcp_tools,
        )
