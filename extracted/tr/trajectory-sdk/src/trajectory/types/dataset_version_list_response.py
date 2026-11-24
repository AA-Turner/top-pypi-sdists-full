# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.datasets.dataset_version import DatasetVersion


class DatasetVersionListResponse(SyncPage[DatasetVersion]):
  """Live versions of one dataset name."""

  items: list[DatasetVersion]

  next_cursor: str | None = None

  has_more: bool
