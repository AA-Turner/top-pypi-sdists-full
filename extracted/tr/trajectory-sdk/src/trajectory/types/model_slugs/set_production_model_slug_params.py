# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class SetProductionModelSlugParams(TypedDict, total=False):
  production_model_slug: Required[str]
  """
  Exact production model slug, unique within this organization. Never normalized.
  """
