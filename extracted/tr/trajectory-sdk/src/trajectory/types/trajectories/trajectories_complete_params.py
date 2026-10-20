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
  How the attempt ended. Use ENV_DONE only when it finished normally.
  - ENV_DONE: finished normally, including a graded wrong answer.
  - ERROR: model requests failed after retries, or the environment or grader failed.
  - TIMEOUT: the harness stopped the agent at its own time limit.
  - TRUNCATION: the final reply was cut off at its output-token limit, or the conversation
    no longer fit the model's context.
  - MISSING_SUBMIT: the task requires a submission and the agent stopped without one.
  - MAX_STEPS: the harness or platform stopped the agent at its turn or step limit.
  - LIMIT_REACHED, STALE: set by the platform. It preserves a previously recorded
    LIMIT_REACHED or MAX_STEPS.
  - GOLDEN_PATCH: reserved; do not send.
  
  Training admits ENV_DONE, LIMIT_REACHED and MAX_STEPS; TRUNCATION requires
  train_on_truncation. In training and evaluation, LIMIT_REACHED, MAX_STEPS and TRUNCATION
  use 0 if ungraded and cap positive rewards at 0.
  train_on_error admits ERROR; train_on_timeout admits TIMEOUT and SANDBOX_TIMEOUT.
  These enabled failures use the recorded reward, or 0 when none is recorded.
  An ungraded ENV_DONE is excluded. Admitted samples can still be
  rejected by other training filters. ERROR is a failed evaluation attempt.
  """
