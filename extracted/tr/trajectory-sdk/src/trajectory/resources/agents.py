# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx

from trajectory._base_client import SyncPage, make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.agents.agent_response import AgentResponse
from trajectory.types.agents.agents_create_params import AgentsCreateParams
from trajectory.types.agents.agents_update_params import AgentsUpdateParams
from trajectory.types.delete_agent_response import DeleteAgentResponse


class Agents(APIResource):
  @cached_property
  def with_raw_response(self) -> AgentsWithRawResponse:
    return AgentsWithRawResponse(self)

  def create(
    self,
    *,
    name: str,
    description: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
      "/api/v1/agents",
      cast_to=AgentResponse,
      body=maybe_transform(
        {
          "name": name,
          "description": description,
        },
        AgentsCreateParams,
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
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[AgentResponse]:
    """List the authenticated organization's agents, newest first.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/agents",
      cast_to=SyncPage[AgentResponse],
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": cursor,
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        "/api/v1/agents/{agent_id}",
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        "/api/v1/agents/name/{name}",
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

  def update(
    self,
    agent_id: str,
    *,
    name: str | Omit = omit,
    description: str | None | Omit = omit,
    model_slug: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> AgentResponse:
    """Update an agent's name, description, or serving model assignment.

    Args:
      name: New agent name using only letters, digits, spaces, hyphens, underscores, and
        periods. Omit to leave unchanged.

      description: New agent description. Set to null to clear it; omit to leave unchanged.

      model_slug: Existing serving model slug in this organization. Set null to unassign it.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._patch(
      path_template(
        "/api/v1/agents/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=AgentResponse,
      body=maybe_transform(
        {
          "name": name,
          "description": description,
          "model_slug": model_slug,
        },
        AgentsUpdateParams,
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> DeleteAgentResponse:
    """Delete an agent that is not referenced by any dependent resources. The request succeeds
    if the agent was already deleted.

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
        "/api/v1/agents/{agent_id}",
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


class AgentsWithRawResponse:
  def __init__(self, resource: Agents) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.retrieve_by_name = to_raw_response_wrapper(resource.retrieve_by_name)
    self.update = to_raw_response_wrapper(resource.update)
    self.delete = to_raw_response_wrapper(resource.delete)
