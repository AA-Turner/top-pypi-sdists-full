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
  Reward component name.
  """
  value: Required[float]
  """
  Raw reward value.
  """
  explanation: str
  """
  Human-readable reason for the reward.
  """
  weight: float
  """
  Weight of this component in the trajectory's summed reward. Use 0 to store the component for
  diagnostics without counting it. If every component has weight 0, the trajectory's reward is
  0.
  """
