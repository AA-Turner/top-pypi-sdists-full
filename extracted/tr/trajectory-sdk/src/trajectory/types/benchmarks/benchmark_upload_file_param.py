# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class BenchmarkUploadFileParam(TypedDict, total=False):
  path: Required[str]
  content_type: Required[str]
  size_bytes: Required[int]
