# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class SecretsCreateParams(TypedDict, total=False):
  name: Required[str]
  """
  Name to reference the secret by; unique among live secrets.
  """
  value: Required[str]
  """
  The secret value. Write-only — never returned after creation.
  """
  description: str | None
  """
  Optional human-readable description.
  """
