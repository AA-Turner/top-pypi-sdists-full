# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class DeploymentsPromoteParams(TypedDict, total=False):
  expected_deployment_id: Required[str | None]
  """
  Expected current production target; null for initial promotion.
  """
