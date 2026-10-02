# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict


class IngestionCreateSessionParams(TypedDict, total=False):
  agent_id: str | None
  """
  The benchmark's agent ID. Provide agent_id or agent_name for every ingestion.
  """
  agent_name: str | None
  """
  The benchmark's agent name. Provide agent_id or agent_name for every ingestion.
  """
  bench_name: Required[str]
  """
  Reusing a benchmark name pushes a new version of that benchmark.
  """
  metadata: Required[Mapping[str, Any]]
  upload_digest: Required[str]
  build_images: bool
