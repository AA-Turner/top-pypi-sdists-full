# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class BenchmarkTaskWriteFailure(BaseModel):
  """A task that did not land; its siblings did, so the bench is short exactly these."""

  task_id: str

  label: str | None = None

  error: str
