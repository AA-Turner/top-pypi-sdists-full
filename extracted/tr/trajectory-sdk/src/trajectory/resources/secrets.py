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
from trajectory.types.create_secret_response import CreateSecretResponse
from trajectory.types.revoke_secret_response import RevokeSecretResponse
from trajectory.types.secrets.secret import Secret
from trajectory.types.secrets.secrets_create_params import SecretsCreateParams


class Secrets(APIResource):
  @cached_property
  def with_raw_response(self) -> SecretsWithRawResponse:
    return SecretsWithRawResponse(self)

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
  ) -> SyncPage[Secret]:
    """List User Secrets

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/secrets",
      cast_to=SyncPage[Secret],
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

  def create(
    self,
    *,
    name: str,
    value: str,
    description: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> CreateSecretResponse:
    """Create Secret

    Args:
      name: Name to reference the secret by; unique among live secrets.

      value: The secret value. Write-only — never returned after creation.

      description: Optional human-readable description.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/secrets",
      cast_to=CreateSecretResponse,
      body=maybe_transform(
        {
          "name": name,
          "value": value,
          "description": description,
        },
        SecretsCreateParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def revoke(
    self,
    secret_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> RevokeSecretResponse:
    """Revoke Secret

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(secret_id, str) and not secret_id:
      raise ValueError(f"Expected a non-empty value for `secret_id` but received {secret_id!r}")
    return self._delete(
      path_template(
        "/api/v1/secrets/{secret_id}",
        secret_id=secret_id,
      ),
      cast_to=RevokeSecretResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class SecretsWithRawResponse:
  def __init__(self, resource: Secrets) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.create = to_raw_response_wrapper(resource.create)
    self.revoke = to_raw_response_wrapper(resource.revoke)
