# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class TrajectoriesLogRewardParams(TypedDict, total=False):
  reward_id: Required[str]
  """
  Caller-owned id used to dedupe retries of the same reward component.
  """
  name: Required[str]
  """
  Reward component name. Each call adds one component; the trajectory's logged reward is the
  weighted average of its components' scaled values, (value - min_value) / (max_value -
  min_value).
  """
  value: Required[float]
  """
  Raw reward value within the declared inclusive bounds.
  """
  min_value: float
  """
  Minimum raw reward; must be less than max_value.
  """
  max_value: float
  """
  Maximum raw reward, must be larger than min_value
  """
  explanation: str
  """
  Human-readable reason for this component's value.
  """
  weight: float
  """
  Weight of this component in the trajectory's weighted average reward. Use 0 to store the
  component for diagnostics without counting it. If every component has weight 0, the
  trajectory's reward is 0.
  """
