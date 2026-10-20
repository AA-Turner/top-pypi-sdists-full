# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.billing.billing_run_cost import BillingRunCost


class BillingRunCostsResponse(BaseModel):
  snapshot_id: str

  items: list[BillingRunCost]

  total: int
