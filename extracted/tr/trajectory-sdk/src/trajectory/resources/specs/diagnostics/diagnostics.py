# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property

from trajectory._resource import APIResource
from trajectory.resources.specs.diagnostics.findings import Findings, FindingsWithRawResponse


class Diagnostics(APIResource):
  @cached_property
  def with_raw_response(self) -> DiagnosticsWithRawResponse:
    return DiagnosticsWithRawResponse(self)

  @cached_property
  def findings(self) -> Findings:
    return Findings(self._client)


class DiagnosticsWithRawResponse:
  def __init__(self, resource: Diagnostics) -> None:
    self._resource = resource

  @cached_property
  def findings(self) -> FindingsWithRawResponse:
    return FindingsWithRawResponse(self._resource.findings)
