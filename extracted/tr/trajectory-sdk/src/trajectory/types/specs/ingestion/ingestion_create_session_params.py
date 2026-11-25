# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Required, TypedDict


class IngestionCreateSessionParams(TypedDict, total=False):
  metadata: Required[Mapping[str, Any]]
  upload_digest: Required[str]
  build_images: bool
  skip_image_cache: bool
  """
  Build every image from its Dockerfile without reusing one already built from the same files.
  Requires build_images.
  """
  project_id: str | None
  """
  The spec's project ID. Provide project_id or project_name for every ingestion.
  """
  project_name: str | None
  """
  The spec's project name. Provide project_id or project_name for every ingestion.
  """
  spec_name: Required[str]
  """
  Reusing a spec name pushes a new version of that spec.
  """
