# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict


class ToolDefinitionParam(TypedDict, total=False):
  name: Required[str]
  description: Required[str]
  parameters: Required[Mapping[str, Any]]
