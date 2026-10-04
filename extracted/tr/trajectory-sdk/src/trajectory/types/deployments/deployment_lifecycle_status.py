# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypeAlias

DeploymentLifecycleStatus: TypeAlias = Literal[
  "PENDING", "DEPLOYING", "DEPLOYED", "FAILED", "CANCELLING", "CANCELLED"
]
"""Spanner deployment row status."""
