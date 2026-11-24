# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.data_qc_finding_counts import DataQcFindingCounts
from trajectory.types.specs.diagnostics.findings.data_qc_finding import DataQcFinding
from trajectory.types.specs.diagnostics.findings.findings_counts_params import (
  DataQcFindingCountTargetParam,
  FindingsCountsParams,
)
from trajectory.types.specs.diagnostics.findings.findings_create_params import (
  FindingsCreateParams,
  SpecEvidenceParam,
  TaskEvidenceParam,
  TrajectoryEvidenceParam,
)
from trajectory.types.specs.diagnostics.findings.findings_resolve_params import (
  FindingsResolveParams,
)


class Findings(APIResource):
  @cached_property
  def with_raw_response(self) -> FindingsWithRawResponse:
    return FindingsWithRawResponse(self)

  def create(
    self,
    *,
    bench_id: str,
    title: str,
    explanation: str,
    detector_name: str,
    idempotency_key: str | Omit = omit,
    task_id: str | None | Omit = omit,
    trajectory_id: str | None | Omit = omit,
    suggested_fix: str | None | Omit = omit,
    evidence: Iterable[SpecEvidenceParam | TaskEvidenceParam | TrajectoryEvidenceParam]
    | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DataQcFinding:
    """Create a finding attached to a spec, one of its tasks, or a trajectory for that task.
    Evidence can cite other resources in the same organization. Retrying with the same
    Idempotency-Key and request content returns the original finding.

    Args:
      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/specs/diagnostics/findings",
      cast_to=DataQcFinding,
      body=maybe_transform(
        {
          "bench_id": bench_id,
          "title": title,
          "explanation": explanation,
          "detector_name": detector_name,
          "task_id": task_id,
          "trajectory_id": trajectory_id,
          "suggested_fix": suggested_fix,
          "evidence": evidence,
        },
        FindingsCreateParams,
      ),
      options=make_request_options(
        headers={
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=(
          {"Idempotency-Key": omit, **(extra_headers or {})}
          if idempotency_key is None
          else extra_headers
        ),
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
        idempotency_header=("Idempotency-Key" if isinstance(idempotency_key, Omit) else None),
      ),
    )

  def list(
    self,
    *,
    bench_id: str,
    task_id: str | None | Omit = omit,
    trajectory_id: str | None | Omit = omit,
    include_descendants: bool | Omit = omit,
    state: Literal["open", "resolved", "all"] | Omit = omit,
    detector_name: str | None | Omit = omit,
    limit: int | Omit = omit,
    cursor: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[DataQcFinding]:
    """List findings for an exact spec, task, or trajectory target. Set include_descendants to
    also include findings on its child resources. Results are ordered newest first.

    Args:
      trajectory_id: Requires task_id.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/specs/diagnostics/findings",
      cast_to=SyncPage[DataQcFinding],
      options=make_request_options(
        params=maybe_transform(
          {
            "bench_id": bench_id,
            "task_id": task_id,
            "trajectory_id": trajectory_id,
            "include_descendants": include_descendants,
            "state": state,
            "detector_name": detector_name,
            "limit": limit,
            "cursor": omit if cursor is None else cursor,
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
    finding_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DataQcFinding:
    """Get Data Qc Finding

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(finding_id, str) and not finding_id:
      raise ValueError(f"Expected a non-empty value for `finding_id` but received {finding_id!r}")
    return self._get(
      path_template(
        "/api/v1/specs/diagnostics/findings/{finding_id}",
        finding_id=finding_id,
      ),
      cast_to=DataQcFinding,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def resolve(
    self,
    finding_id: str,
    *,
    note: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DataQcFinding:
    """Resolve a finding. Send an empty JSON object to omit the note. Repeated calls return the
    original resolution.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(finding_id, str) and not finding_id:
      raise ValueError(f"Expected a non-empty value for `finding_id` but received {finding_id!r}")
    return self._post(
      path_template(
        "/api/v1/specs/diagnostics/findings/{finding_id}/resolve",
        finding_id=finding_id,
      ),
      cast_to=DataQcFinding,
      body=maybe_transform(
        {
          "note": note,
        },
        FindingsResolveParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def counts(
    self,
    *,
    targets: Iterable[DataQcFindingCountTargetParam],
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DataQcFindingCounts:
    """Read open and resolved counts for up to 200 targets in one consistent snapshot. Results
    follow the request order and include targets with zero findings.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/specs/diagnostics/findings/counts",
      cast_to=DataQcFindingCounts,
      body=maybe_transform(
        {
          "targets": targets,
        },
        FindingsCountsParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class FindingsWithRawResponse:
  def __init__(self, resource: Findings) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.resolve = to_raw_response_wrapper(resource.resolve)
    self.counts = to_raw_response_wrapper(resource.counts)
