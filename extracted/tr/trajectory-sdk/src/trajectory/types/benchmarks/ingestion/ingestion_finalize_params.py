# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class IngestionFinalizeParams(TypedDict, total=False):
  object_count: Required[int]
  part_count: Required[int]
