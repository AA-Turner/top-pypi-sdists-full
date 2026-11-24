# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict

from trajectory._types import SequenceNotStr


class BestPerTaskFilterParam(TypedDict, total=False):
  type: Required[Literal["best_per_task"]]
  """
  Keep each task's highest-reward attempt in the run, however often it was visited.
  """


class NoErrorsFilterParam(TypedDict, total=False):
  type: Required[Literal["no_errors"]]
  """
  Keep every attempt that did not end in an error.
  """


class RewardThresholdFilterParam(TypedDict, total=False):
  type: Required[Literal["reward_threshold"]]
  """
  Keep attempts by reward.
  """
  value: Required[float]
  """
  Keep attempts whose reward is at least this finite value.
  """


class DatasetsAddTrajectoriesParams(TypedDict, total=False):
  training_run_ids: SequenceNotStr[str]
  """
  Succeeded or cancelled training runs whose completed train attempts join the train split.
  """
  eval_run_ids: SequenceNotStr[str]
  """
  Completed eval runs whose scored attempts join the heldout split.
  """
  filter: Required[RewardThresholdFilterParam | NoErrorsFilterParam | BestPerTaskFilterParam]
