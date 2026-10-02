# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any

from trajectory._models import BaseModel


class AsyncFailure(BaseModel):
  type: str
  """Stable category used for exception mapping."""

  code: str
  """Stable programmatic reason for the asynchronous failure."""

  message: str
  """Human-readable explanation for this failure occurrence."""

  context: dict[str, Any] | None = None
  """Machine-readable values specific to this failure code."""
