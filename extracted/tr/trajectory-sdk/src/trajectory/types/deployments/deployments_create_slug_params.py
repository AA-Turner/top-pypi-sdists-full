# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class DeploymentsCreateSlugParams(TypedDict, total=False):
  name: Required[str]
  """
  Slug name. Leading/trailing whitespace is trimmed and the stored name is lowercased. Must be a
  single token (no whitespace). Allowed characters: letters, numbers, '-' and '_'. Max length:
  32.
  """
