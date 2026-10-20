# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Literal

from trajectory._models import BaseModel


class BillingRunCost(BaseModel):
  run_id: str

  name: str

  type: Literal["training", "eval"] | None

  status: str | None

  launch_at: datetime | None

  cents: float

  training_cents: float

  inference_cents: float

  grading_cents: float

  sandbox_cents: float
