# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypedDict


class TrajectoriesCompleteParams(TypedDict, total=False):
  termination_reason: Literal[
    "TIMEOUT",
    "ENV_DONE",
    "TRUNCATION",
    "STALE",
    "ERROR",
    "MAX_STEPS",
    "LIMIT_REACHED",
    "MISSING_SUBMIT",
    "GOLDEN_PATCH",
  ]
  """
  How the attempt ended. Use ENV_DONE only when it finished normally.
  - ENV_DONE: finished normally, including a graded wrong answer.
  - ERROR: model requests failed after retries, or the environment or grader failed (including
    sandbox loss, crash, or startup timeout).
  - TIMEOUT: the harness stopped the agent at its own time limit.
  - TRUNCATION: a turn, step, output-token, or context limit stopped the attempt.
  - STALE: stopped because the policy became stale.
  Deprecated inputs: MAX_STEPS, LIMIT_REACHED and MISSING_SUBMIT map to TRUNCATION; GOLDEN_PATCH
  maps to ENV_DONE.
  
  Training admits ENV_DONE; all incomplete attempts require train_on_truncation.
  train_on_error admits ERROR; train_on_timeout admits TIMEOUT.
  Admitted TRUNCATION, TIMEOUT and ERROR attempts train with reward 0; recorded rewards are
  unchanged.
  An ungraded ENV_DONE is excluded unless train_on_error is enabled. Admitted samples can still
  be
  rejected by other training filters. In evaluation, TRUNCATION uses 0 if ungraded and caps
  positive rewards at 0, and ERROR is a failed attempt.
  """
