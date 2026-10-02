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
from trajectory.types.deployments.deployment import Deployment
from trajectory.types.deployments.deployments_create_params import (
  DeploymentsCreateParams,
  ModelEndpointConfigParam,
)
from trajectory.types.deployments.deployments_create_slug_params import DeploymentsCreateSlugParams
from trajectory.types.deployments.deployments_promote_params import DeploymentsPromoteParams
from trajectory.types.deployments_summary import DeploymentsSummary
from trajectory.types.model_slug import ModelSlug
from trajectory.types.promote_response import PromoteResponse
from trajectory.types.start_deploy_response import StartDeployResponse
from trajectory.types.undeploy_response import UndeployResponse


class Deployments(APIResource):
  @cached_property
  def with_raw_response(self) -> DeploymentsWithRawResponse:
    return DeploymentsWithRawResponse(self)

  def list(
    self,
    *,
    status: Literal["PENDING", "DEPLOYING", "DEPLOYED", "FAILED"] | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[Deployment]:
    """List Deployments Route

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/deploy",
      cast_to=SyncPage[Deployment],
      options=make_request_options(
        params=maybe_transform(
          {
            "status": status,
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

  def create(
    self,
    *,
    checkpoint_id: str,
    model_slug: str,
    agent_id: str | None | Omit = omit,
    role: Literal["production", "test"] | Omit = omit,
    model_endpoint_config: ModelEndpointConfigParam | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> StartDeployResponse:
    """Serve a committed checkpoint through Model Endpoint.

    Args:
      agent_id: Owning agent; inferred from the checkpoint or serving name when omitted.

      model_endpoint_config: Model Endpoint configuration for the deployment. Defaults to the exact
        configuration persisted for the originating Training Service run.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/deploy",
      cast_to=StartDeployResponse,
      body=maybe_transform(
        {
          "checkpoint_id": checkpoint_id,
          "model_slug": model_slug,
          "agent_id": agent_id,
          "role": role,
          "model_endpoint_config": model_endpoint_config,
        },
        DeploymentsCreateParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def create_slug(
    self,
    *,
    name: str,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ModelSlug:
    """Create Model Slug

    Args:
      name: Slug name. Leading/trailing whitespace is trimmed and the stored name is
        lowercased. Must be a single token (no whitespace). Allowed characters: letters,
        numbers, '-' and '_'. Max length: 32.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/models/slugs",
      cast_to=ModelSlug,
      body=maybe_transform(
        {
          "name": name,
        },
        DeploymentsCreateSlugParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    deployment_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> Deployment:
    """Get Deployment Route

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/deploy/{deployment_id}",
        deployment_id=deployment_id,
      ),
      cast_to=Deployment,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def delete(
    self,
    deployment_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> UndeployResponse:
    """Delete a deployment and its Model Endpoint resources.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._delete(
      path_template(
        "/api/v1/deploy/{deployment_id}",
        deployment_id=deployment_id,
      ),
      cast_to=UndeployResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def promote(
    self,
    deployment_id: str,
    *,
    body: DeploymentsPromoteParams | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> PromoteResponse:
    """Make a deployed deployment the active target for its slug.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/deploy/{deployment_id}/promote",
        deployment_id=deployment_id,
      ),
      cast_to=PromoteResponse,
      body=(
        None if isinstance(body, Omit) else maybe_transform(body, DeploymentsPromoteParams | None)
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def unpromote(
    self,
    deployment_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> PromoteResponse:
    """Clear a deployment's active flag so its slug serves nothing.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/deploy/{deployment_id}/unpromote",
        deployment_id=deployment_id,
      ),
      cast_to=PromoteResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def summarize(
    self,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> DeploymentsSummary:
    """Summary

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/deploy/summary",
      cast_to=DeploymentsSummary,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class DeploymentsWithRawResponse:
  def __init__(self, resource: Deployments) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.create = to_raw_response_wrapper(resource.create)
    self.create_slug = to_raw_response_wrapper(resource.create_slug)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.delete = to_raw_response_wrapper(resource.delete)
    self.promote = to_raw_response_wrapper(resource.promote)
    self.unpromote = to_raw_response_wrapper(resource.unpromote)
    self.summarize = to_raw_response_wrapper(resource.summarize)
