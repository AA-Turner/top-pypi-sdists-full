# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.datasets.dataset_metadata import DatasetMetadata


class PaginatedResponseDatasetMetadata(SyncPage[DatasetMetadata]):
  items: list[DatasetMetadata]

  next_cursor: str | None = None

  has_more: bool
