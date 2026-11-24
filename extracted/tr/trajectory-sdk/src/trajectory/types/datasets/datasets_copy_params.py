# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class DatasetsCopyParams(TypedDict, total=False):
  source_dataset_id: Required[str]
  """
  Finalized dataset whose trajectories are copied, keeping their splits.
  """
