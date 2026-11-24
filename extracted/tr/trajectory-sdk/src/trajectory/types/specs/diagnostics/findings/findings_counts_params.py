# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Required, TypedDict


class DataQcFindingCountTargetParam(TypedDict, total=False):
  bench_id: Required[str]
  task_id: str | None
  trajectory_id: str | None
  include_descendants: bool


class FindingsCountsParams(TypedDict, total=False):
  targets: Required[Iterable[DataQcFindingCountTargetParam]]
