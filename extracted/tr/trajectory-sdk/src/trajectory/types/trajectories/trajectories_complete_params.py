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
  - LIMIT_REACHED, MAX_STEPS, STALE: set by the platform. A LIMIT_REACHED or MAX_STEPS it
    already set is kept.
  - GOLDEN_PATCH: reserved; do not send.
  
  Training uses ENV_DONE, LIMIT_REACHED and MAX_STEPS, plus TRUNCATION when the run sets
  train_on_truncation. LIMIT_REACHED, MAX_STEPS and TRUNCATION count positive rewards as 0.
  ERROR counts toward the run's failure limit and as failed in evaluation.
  """
