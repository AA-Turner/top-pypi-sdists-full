# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, not_given
from trajectory.types.held_out_rewards_by_step_response import HeldOutRewardsByStepResponse
from trajectory.types.trainer_rewards_by_step_response import TrainerRewardsByStepResponse
from trajectory.types.training_trajectory_rewards_response import TrainingTrajectoryRewardsResponse


class Rewards(APIResource):
  @cached_property
  def with_raw_response(self) -> RewardsWithRawResponse:
    return RewardsWithRawResponse(self)

  def list_held_out_rewards(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> HeldOutRewardsByStepResponse:
    """Get Held Out Rewards By Step

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
      cast_to=HeldOutRewardsByStepResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_trainer_rewards(
    self,
    run_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> TrainerRewardsByStepResponse:
    """Get Trainer Rewards By Step

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
        "/api/v1/train/{run_id}/step/trainer-reward-by-step",
        run_id=run_id,
      ),
      cast_to=TrainerRewardsByStepResponse,
      options=make_request_options(
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
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> TrainingTrajectoryRewardsResponse:
    """Get Training Trajectory Rewards Route

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
      cast_to=TrainingTrajectoryRewardsResponse,
      options=make_request_options(
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
    self.list_trainer_rewards = to_raw_response_wrapper(resource.list_trainer_rewards)
    self.list_trajectory_rewards = to_raw_response_wrapper(resource.list_trajectory_rewards)
