# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TypedDict

from trajectory.types.image_spec_param import ImageSpecParam


class RuntimeSpecParam(TypedDict, total=False):
  runtime_id: str | None
  source: ImageSpecParam | None
