# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class PromoteResponse(BaseModel):
  deployment_id: str

  is_active: bool
