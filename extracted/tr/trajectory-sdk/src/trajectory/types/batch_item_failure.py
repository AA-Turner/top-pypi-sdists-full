# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any

from trajectory._models import BaseModel


class BatchItemFailure(BaseModel):
  code: str
  """Stable programmatic reason for this item failure."""

  message: str
  """Human-readable explanation for this item occurrence."""

  item_index: int | None = None
  """Zero-based input index when the failed item came from a list."""

  context: dict[str, Any] | None = None
  """Machine-readable values specific to this failure code."""
