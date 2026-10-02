# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypedDict


class TrajectoriesCompleteParams(TypedDict, total=False):
  termination_reason: Literal[
    "TIMEOUT",
    "ENV_DONE",
    "GOLDEN_PATCH",
    "MAX_STEPS",
    "TRUNCATION",
    "LIMIT_REACHED",
    "STALE",
    "ERROR",
    "MISSING_SUBMIT",
  ]
  """
  Why the harness finished. ENV_DONE is successful completion.
  """
