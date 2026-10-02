# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any

from trajectory._models import BaseModel


class ToolDefinition(BaseModel):
  name: str

  description: str

  parameters: dict[str, Any]
