# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory.types.beta.checkpoint_exports.checkpoint_export import CheckpointExport


class CheckpointExports(APIResource):
  @cached_property
  def with_raw_response(self) -> CheckpointExportsWithRawResponse:
    return CheckpointExportsWithRawResponse(self)

  def create(
    self,
    checkpoint_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> CheckpointExport:
    """Start or reuse the LoRA adapter download for a committed checkpoint.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(checkpoint_id, str) and not checkpoint_id:
      raise ValueError(
        f"Expected a non-empty value for `checkpoint_id` but received {checkpoint_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/checkpoints/{checkpoint_id}/exports",
        checkpoint_id=checkpoint_id,
      ),
      cast_to=CheckpointExport,
      options=make_request_options(
        extra_headers={"Trajectory-Beta": "checkpoint-exports-2026-10-29", **(extra_headers or {})},
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list(
    self,
    checkpoint_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[CheckpointExport]:
    """List Checkpoint Exports

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(checkpoint_id, str) and not checkpoint_id:
      raise ValueError(
        f"Expected a non-empty value for `checkpoint_id` but received {checkpoint_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/checkpoints/{checkpoint_id}/exports",
        checkpoint_id=checkpoint_id,
      ),
      cast_to=SyncPage[CheckpointExport],
      options=make_request_options(
        extra_headers={"Trajectory-Beta": "checkpoint-exports-2026-10-29", **(extra_headers or {})},
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    export_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> CheckpointExport:
    """Read export status; a ready export includes a fresh signed download link.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(export_id, str) and not export_id:
      raise ValueError(f"Expected a non-empty value for `export_id` but received {export_id!r}")
    return self._get(
      path_template(
        "/api/v1/checkpoints/exports/{export_id}",
        export_id=export_id,
      ),
      cast_to=CheckpointExport,
      options=make_request_options(
        extra_headers={"Trajectory-Beta": "checkpoint-exports-2026-10-29", **(extra_headers or {})},
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class CheckpointExportsWithRawResponse:
  def __init__(self, resource: CheckpointExports) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
