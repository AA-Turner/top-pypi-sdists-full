# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, SequenceNotStr, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.agent_list_response import AgentListResponse
from trajectory.types.delete_agent_response import DeleteAgentResponse
from trajectory.types.evals.eval_run import EvalRun
from trajectory.types.projects.agent_response import AgentResponse
from trajectory.types.projects.projects_create_params import ProjectsCreateParams
from trajectory.types.projects.projects_update_params import ProjectsUpdateParams
from trajectory.types.rl.training_run_response import TrainingRunResponse


class Projects(APIResource):
  @cached_property
  def with_raw_response(self) -> ProjectsWithRawResponse:
    return ProjectsWithRawResponse(self)

  def create(
    self,
    *,
    name: str,
    description: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> AgentResponse:
    """Register an agent for the authenticated organization.

    Args:
      name: Agent name, unique within the organization. Only letters, digits, spaces, hyphens,
        underscores, and periods.

      description: Optional description of the agent's purpose.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/projects",
      cast_to=AgentResponse,
      body=maybe_transform(
        {
          "name": name,
          "description": description,
        },
        ProjectsCreateParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list(
    self,
    *,
    has_deployment: bool | None | Omit = omit,
    has_benchmarks: bool | None | Omit = omit,
    agent_id: SequenceNotStr[str] | None | Omit = omit,
    production_model_slug: str | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> AgentListResponse:
    """List the authenticated organization's agents, newest first unless `sort` is given
    (created_at, updated_at, name, agent_id or benchmark_count).

    Args:
      has_deployment: Return only agents that do (or do not) own an active deployed model.

      has_benchmarks: Return only agents that do (or do not) own a benchmark.

      agent_id: Return only these agents; repeat for each agent ID.

      production_model_slug: Filter by exact production model slug.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/projects",
      cast_to=AgentListResponse,
      options=make_request_options(
        params=maybe_transform(
          {
            "has_deployment": has_deployment,
            "has_benchmarks": has_benchmarks,
            "agent_id": agent_id,
            "production_model_slug": production_model_slug,
            "cursor": omit if cursor is None else cursor,
            "limit": limit,
            "sort": sort,
            "order": order,
            "search": search,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    agent_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> AgentResponse:
    """Retrieve an agent by ID.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._get(
      path_template(
        "/api/v1/projects/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=AgentResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve_by_name(
    self,
    name: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> AgentResponse:
    """Retrieve an agent by its exact organization-scoped name.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(name, str) and not name:
      raise ValueError(f"Expected a non-empty value for `name` but received {name!r}")
    return self._get(
      path_template(
        "/api/v1/projects/name/{name}",
        name=name,
      ),
      cast_to=AgentResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_training_runs(
    self,
    agent_id: str,
    *,
    limit: int | Omit = omit,
    cursor: str | None | Omit = omit,
    bench_id: str | None | Omit = omit,
    status: str | None | Omit = omit,
    has_training_execution: bool | None | Omit = omit,
    has_checkpoints: bool | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[TrainingRunResponse]:
    """List Agent Training Runs

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._get(
      path_template(
        "/api/v1/projects/{agent_id}/training-runs",
        agent_id=agent_id,
      ),
      cast_to=SyncPage[TrainingRunResponse],
      options=make_request_options(
        params=maybe_transform(
          {
            "limit": limit,
            "cursor": omit if cursor is None else cursor,
            "bench_id": bench_id,
            "status": status,
            "has_training_execution": has_training_execution,
            "has_checkpoints": has_checkpoints,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_evaluation_runs(
    self,
    agent_id: str,
    *,
    limit: int | Omit = omit,
    cursor: str | None | Omit = omit,
    bench_id: str | None | Omit = omit,
    status: str | None | Omit = omit,
    training_run_id: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[EvalRun]:
    """List Agent Evaluation Runs

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._get(
      path_template(
        "/api/v1/projects/{agent_id}/evaluation-runs",
        agent_id=agent_id,
      ),
      cast_to=SyncPage[EvalRun],
      options=make_request_options(
        params=maybe_transform(
          {
            "limit": limit,
            "cursor": omit if cursor is None else cursor,
            "bench_id": bench_id,
            "status": status,
            "training_run_id": training_run_id,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def update(
    self,
    agent_id: str,
    *,
    name: str | Omit = omit,
    description: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> AgentResponse:
    """Update an agent's name or description.

    Args:
      name: New agent name using only letters, digits, spaces, hyphens, underscores, and
        periods. Omit to leave unchanged.

      description: New agent description. Set to null to clear it; omit to leave unchanged.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._patch(
      path_template(
        "/api/v1/projects/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=AgentResponse,
      body=maybe_transform(
        {
          "name": name,
          "description": description,
        },
        ProjectsUpdateParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def delete(
    self,
    agent_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DeleteAgentResponse:
    """Delete an agent and its benchmarks after all runs and cleanup have finished. The request
    succeeds if the agent was already deleted.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._delete(
      path_template(
        "/api/v1/projects/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=DeleteAgentResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class ProjectsWithRawResponse:
  def __init__(self, resource: Projects) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.retrieve_by_name = to_raw_response_wrapper(resource.retrieve_by_name)
    self.list_training_runs = to_raw_response_wrapper(resource.list_training_runs)
    self.list_evaluation_runs = to_raw_response_wrapper(resource.list_evaluation_runs)
    self.update = to_raw_response_wrapper(resource.update)
    self.delete = to_raw_response_wrapper(resource.delete)
