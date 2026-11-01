# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property

from trajectory._resource import APIResource
from trajectory.resources.beta.checkpoint_exports import (
  CheckpointExports,
  CheckpointExportsWithRawResponse,
)


class Beta(APIResource):
  @cached_property
  def with_raw_response(self) -> BetaWithRawResponse:
    return BetaWithRawResponse(self)

  @cached_property
  def checkpoint_exports(self) -> CheckpointExports:
    return CheckpointExports(self._client)


class BetaWithRawResponse:
  def __init__(self, resource: Beta) -> None:
    self._resource = resource

  @cached_property
  def checkpoint_exports(self) -> CheckpointExportsWithRawResponse:
    return CheckpointExportsWithRawResponse(self._resource.checkpoint_exports)
