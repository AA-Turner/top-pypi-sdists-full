# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Literal

from trajectory._models import BaseModel


class ToolCall(BaseModel):
  name: str

  arguments: dict[str, Any]

  id: str | None = None

  raw_string: str | None = None

  argument_encoding: Literal["json", "xml"] = "json"

  is_parsed_successfully: bool = True

  parser_error_msg: str | None = None
