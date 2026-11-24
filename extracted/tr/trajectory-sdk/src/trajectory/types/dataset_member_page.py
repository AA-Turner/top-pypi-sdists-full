# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.datasets.members.dataset_member import DatasetMember


class DatasetMemberPage(SyncPage[DatasetMember]):
  """One page of a dataset version's trajectories, ordered by trajectory ID."""

  items: list[DatasetMember]

  next_cursor: str | None = None

  has_more: bool
