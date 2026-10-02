# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict

from trajectory._types import SequenceNotStr


class McpServerSpecParam(TypedDict, total=False):
  name: Required[str]
  transport: Literal["sse", "streamable-http", "stdio"]
  url: str | None
  command: str | None
  args: SequenceNotStr[str]
