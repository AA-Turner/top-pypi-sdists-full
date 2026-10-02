# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory._utils import maybe_transform
from trajectory.types.artifact_upload import ArtifactUpload
from trajectory.types.artifacts.artifact import Artifact
from trajectory.types.trajectories.artifacts.artifacts_create_upload_params import (
  ArtifactsCreateUploadParams,
)


class Artifacts(APIResource):
  @cached_property
  def with_raw_response(self) -> ArtifactsWithRawResponse:
    return ArtifactsWithRawResponse(self)

  def create_upload(
    self,
    trajectory_id: str,
    *,
    media_type: str,
    size_bytes: int,
    md5: str,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ArtifactUpload:
    """Reserve an upload, then PUT the file to the returned URL and complete it.

    Args:
      media_type: MIME type of the file, such as image/png.

      size_bytes: Exact file size in bytes, at most 16 MiB.

      md5: Base64-encoded MD5 of the file; GCS rejects bytes that do not match.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/artifacts",
        trajectory_id=trajectory_id,
      ),
      cast_to=ArtifactUpload,
      body=maybe_transform(
        {
          "media_type": media_type,
          "size_bytes": size_bytes,
          "md5": md5,
        },
        ArtifactsCreateUploadParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def complete_upload(
    self,
    trajectory_id: str,
    artifact_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> Artifact:
    """Publish the uploaded object's verified metadata and attach it to the trajectory.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    if isinstance(artifact_id, str) and not artifact_id:
      raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
    return self._post(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/artifacts/{artifact_id}/complete",
        trajectory_id=trajectory_id,
        artifact_id=artifact_id,
      ),
      cast_to=Artifact,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class ArtifactsWithRawResponse:
  def __init__(self, resource: Artifacts) -> None:
    self._resource = resource
    self.create_upload = to_raw_response_wrapper(resource.create_upload)
    self.complete_upload = to_raw_response_wrapper(resource.complete_upload)
