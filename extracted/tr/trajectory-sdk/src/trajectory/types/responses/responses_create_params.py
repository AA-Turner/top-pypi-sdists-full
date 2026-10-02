# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Required, TypedDict


class ResponsesCreateParams(TypedDict, total=False):
  model: Required[str]
  input: Required[str | Iterable[Mapping[str, Any]]]
  stream: bool
