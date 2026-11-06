# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory.types.checkpoint_export_file import CheckpointExportFile


class ListCheckpointExportFilesResponse(SyncPage[CheckpointExportFile]):
  items: list[CheckpointExportFile]
  """Every file in the model folder."""

  next_cursor: str | None = None
  """Always null; one page holds all."""

  has_more: bool = False
  """Always false; one page holds all."""
