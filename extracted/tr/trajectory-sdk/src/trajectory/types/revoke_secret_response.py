# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class RevokeSecretResponse(BaseModel):
  secret_id: str
  """Identifier of the secret that was revoked."""
