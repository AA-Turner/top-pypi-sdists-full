# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class ProductionModelSlugResponse(BaseModel):
  agent_id: str

  production_model_slug: str | None

  deployment_id: str | None
