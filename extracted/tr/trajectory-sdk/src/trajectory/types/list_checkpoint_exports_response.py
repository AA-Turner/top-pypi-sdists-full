# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel
from trajectory.types.beta.checkpoint_exports.checkpoint_export import CheckpointExport
from trajectory.types.checkpoint_export_precision import CheckpointExportPrecision


class CheckpointExportPrecisionOption(BaseModel):
  precision: CheckpointExportPrecision

  estimated_size_bytes: int
  """Measured size of this model's merged files."""

  warnings: list[str]
  """Known limits of this format for this model."""


CheckpointExportType: TypeAlias = Literal["lora_adapter", "merged_model"]


class ListCheckpointExportsResponse(SyncPage[CheckpointExport]):
  items: list[CheckpointExport]
  """The checkpoint's exports, newest first."""

  available_export_types: list[CheckpointExportType] | None = None
  """The export types this checkpoint supports."""

  available_merge_precisions: list[CheckpointExportPrecisionOption] | None = None
  """The formats a merged_model export of it can use."""

  next_cursor: str | None = None
  """Always null; one page holds all."""

  has_more: bool = False
  """Always false; one page holds all."""
