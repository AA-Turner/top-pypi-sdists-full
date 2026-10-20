# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._base_client import SyncPage
from trajectory._models import BaseModel


class TrainingStepSummary(BaseModel):
  step: int
  """Training step these rollout, group, and termination aggregates cover."""

  trajectory_count: int
  """Rollouts generated at this training step."""

  completed_count: int
  """Finished rollouts at this training step."""

  avg_turns: float | None
  """
    Mean agent turns (num_steps) per finished rollout; a turn is an agent step inside a
    trajectory, distinct from a training step.
    """

  min_turns: int | None
  """Fewest agent turns among finished rollouts at this training step."""

  max_turns: int | None
  """Most agent turns among finished rollouts at this training step."""

  avg_tokens: float | None
  """Mean generated tokens per finished rollout."""

  min_tokens: int | None
  """Fewest generated tokens among finished rollouts at this training step."""

  max_tokens: int | None
  """Most generated tokens among finished rollouts at this training step."""

  tool_failure_count: int
  """
    Finished rollouts with at least one tool failure (recoverable; not folded into
    error_count).
    """

  tool_failure_exec_count: int
  """Finished rollouts with at least one tool call that raised while executing."""

  tool_failure_parse_count: int
  """Finished rollouts with at least one tool call the runtime could not parse."""

  tool_failure_unk_count: int
  """
    Finished rollouts with at least one tool call that returned neither a result nor an
    error.
    """

  correct_count: int
  """Finished rollouts with reward = 1."""

  partial_count: int
  """Finished rollouts with 0 < reward < 1."""

  incorrect_count: int
  """Finished rollouts with reward = 0."""

  error_count: int
  """Finished rollouts whose termination_reason is ERROR (reward not meaningful)."""

  incomplete_count: int
  """
    Finished rollouts stopped by TIMEOUT, MAX_STEPS, TRUNCATION, or LIMIT_REACHED (real
    reward, task unfinished).
    """

  termination_reasons: dict[str, int]
  """Finished rollouts per termination reason."""

  group_count: int
  """Rollout groups (distinct uid) at the training step."""

  completed_groups: int
  """Groups whose rollouts are all finished with a reward."""

  no_signal_groups: int
  """
    Completed groups whose rewards are all identical. Group-relative algorithms give them
    zero advantage; other algorithms can train on them.
    """

  all_success_groups: int
  """Subset of no_signal_groups with every reward >= 1."""

  all_failed_groups: int
  """Subset of no_signal_groups with every reward <= 0."""

  used_groups: int
  """
    Completed groups with non-identical rewards that the trainer consumed. This count need
    not equal the number of groups in the optimizer batch.
    """

  discarded_groups: int
  """
    Completed groups with reward contrast the trainer did not and will not consume: stale,
    or unconsumed once the step settled.
    """

  pending_groups: int
  """Completed groups with reward contrast the trainer has not consumed yet but still could."""

  stale_groups: int
  """Subset of discarded_groups with at least one STALE rollout."""

  settled: bool
  """
    True once used/discarded can no longer change: the run is terminal, or the trainer's
    latest step > step + max_steps_off_policy with a nonnegative staleness bound.
    """


class TrainingStepSummariesPage(SyncPage[TrainingStepSummary]):
  items: list[TrainingStepSummary]

  next_cursor: str | None = None

  has_more: bool

  training_run_id: str
  """Training run whose per-step summaries are returned."""
