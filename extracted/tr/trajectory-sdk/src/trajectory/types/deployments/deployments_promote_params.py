# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TypedDict


class DeploymentsPromoteParams(TypedDict, total=False):
  demote_deployment_id: str | None
  """
  Optional previous deployment of the same model slug to replace atomically.
  """
