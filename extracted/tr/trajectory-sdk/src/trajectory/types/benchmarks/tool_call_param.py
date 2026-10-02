# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Required, TypedDict


class ToolCallParam(TypedDict, total=False):
  name: Required[str]
  arguments: Required[Mapping[str, Any]]
  id: str | None
  raw_string: str | None
  argument_encoding: Literal["json", "xml"]
  is_parsed_successfully: bool
  parser_error_msg: str | None
