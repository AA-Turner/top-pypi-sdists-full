# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel


class SecretRef(BaseModel):
  secret_ref: str
  """Organization secret name. The containing env_vars key names the runtime variable."""
