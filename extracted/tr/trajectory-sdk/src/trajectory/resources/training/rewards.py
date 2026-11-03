# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx2

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.aperture_reward_point import ApertureRewardPoint
from trajectory.types.held_out_rewards_by_step_page import HeldOutRewardsByStepPage
from trajectory.types.training_trajectory_rewards_page import TrainingTrajectoryRewardsPage


class Rewards(APIResource):
  @cached_property
  def with_raw_response(self) -> RewardsWithRawResponse:
    return RewardsWithRawResponse(self)

  def list_held_out_rewards(
    self,
    run_id: str,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> HeldOutRewardsByStepPage:
    """Held-out evaluation rewards and sample coverage for a training run, in ascending
    training-step order. Only rounds with a published reward metric appear; use the step
    trajectories route for attempts before reward publication. These rounds do not appear in
    standalone evaluation-run lists.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    return self._get(
      path_template(
        "/api/v1/train/{run_id}/step/held-out-reward-by-step",
        run_id=run_id,
      ),
      cast_to=HeldOutRewardsByStepPage,
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": cursor,
            "limit": limit,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_history(
    self,
    training_run_id: str,
    *,
    mode: Literal["training", "eval", "augmentation"] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> list[ApertureRewardPoint]:
    """Mean trajectory reward by policy step, matching the product reward chart. Includes
    trajectory and pending counts; distinct from trainer collection metrics.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(training_run_id, str) and not training_run_id:
      raise ValueError(
        f"Expected a non-empty value for `training_run_id` but received {training_run_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/train/{training_run_id}/trajectory-view/reward-history",
        training_run_id=training_run_id,
      ),
      cast_to=list[ApertureRewardPoint],
      options=make_request_options(
        params=maybe_transform(
          {
            "mode": mode,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_trajectory_rewards(
    self,
    run_id: str,
    step: int,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> TrainingTrajectoryRewardsPage:
    """Per-trajectory rewards recorded at one training step, in ascending trajectory-ID order.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(run_id, str) and not run_id:
      raise ValueError(f"Expected a non-empty value for `run_id` but received {run_id!r}")
    if isinstance(step, str) and not step:
      raise ValueError(f"Expected a non-empty value for `step` but received {step!r}")
    return self._get(
      path_template(
        "/api/v1/train/{run_id}/steps/{step}/trajectory-rewards",
        run_id=run_id,
        step=step,
      ),
      cast_to=TrainingTrajectoryRewardsPage,
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": cursor,
            "limit": limit,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class RewardsWithRawResponse:
  def __init__(self, resource: Rewards) -> None:
    self._resource = resource
    self.list_held_out_rewards = to_raw_response_wrapper(resource.list_held_out_rewards)
    self.list_history = to_raw_response_wrapper(resource.list_history)
    self.list_trajectory_rewards = to_raw_response_wrapper(resource.list_trajectory_rewards)
