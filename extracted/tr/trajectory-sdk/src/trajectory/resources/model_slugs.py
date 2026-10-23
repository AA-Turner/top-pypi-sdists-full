# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory._utils import maybe_transform
from trajectory.types.model_slugs.set_production_model_slug_params import (
  SetProductionModelSlugParams,
)
from trajectory.types.production_model_slug_response import ProductionModelSlugResponse


class ModelSlugs(APIResource):
  @cached_property
  def with_raw_response(self) -> ModelSlugsWithRawResponse:
    return ModelSlugsWithRawResponse(self)

  def get_production(
    self,
    agent_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ProductionModelSlugResponse:
    """Get Production Model Slug

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
        "/api/v1/model-slugs/production/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=ProductionModelSlugResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def create_production(
    self,
    agent_id: str,
    *,
    production_model_slug: str,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ProductionModelSlugResponse:
    """Create Production Model Slug

    Args:
      production_model_slug: Exact production model slug, unique within this organization. Never normalized.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._post(
      path_template(
        "/api/v1/model-slugs/production/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=ProductionModelSlugResponse,
      body=maybe_transform(
        {
          "production_model_slug": production_model_slug,
        },
        SetProductionModelSlugParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def update_production(
    self,
    agent_id: str,
    *,
    production_model_slug: str,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ProductionModelSlugResponse:
    """Update Production Model Slug

    Args:
      production_model_slug: Exact production model slug, unique within this organization. Never normalized.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(agent_id, str) and not agent_id:
      raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
    return self._patch(
      path_template(
        "/api/v1/model-slugs/production/{agent_id}",
        agent_id=agent_id,
      ),
      cast_to=ProductionModelSlugResponse,
      body=maybe_transform(
        {
          "production_model_slug": production_model_slug,
        },
        SetProductionModelSlugParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class ModelSlugsWithRawResponse:
  def __init__(self, resource: ModelSlugs) -> None:
    self._resource = resource
    self.get_production = to_raw_response_wrapper(resource.get_production)
    self.create_production = to_raw_response_wrapper(resource.create_production)
    self.update_production = to_raw_response_wrapper(resource.update_production)
