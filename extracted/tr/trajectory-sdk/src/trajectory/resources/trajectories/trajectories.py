# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal, Mapping
from uuid import uuid4

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.resources.trajectories.artifacts import Artifacts, ArtifactsWithRawResponse
from trajectory.resources.trajectories.steps import Steps, StepsWithRawResponse
from trajectory.types.complete_trajectory_response import CompleteTrajectoryResponse
from trajectory.types.create_trajectory_response import CreateTrajectoryResponse
from trajectory.types.log_trajectory_event_response import LogTrajectoryEventResponse
from trajectory.types.log_trajectory_reward_response import LogTrajectoryRewardResponse
from trajectory.types.trajectories.trajectories_complete_params import TrajectoriesCompleteParams
from trajectory.types.trajectories.trajectories_create_params import TrajectoriesCreateParams
from trajectory.types.trajectories.trajectories_log_event_params import TrajectoriesLogEventParams
from trajectory.types.trajectories.trajectories_log_reward_params import TrajectoriesLogRewardParams
from trajectory.types.trajectories.trajectories_upload_params import TrajectoriesUploadParams
from trajectory.types.trajectories.trajectory import Trajectory
from trajectory.types.trajectory_event import TrajectoryEvent
from trajectory.types.trajectory_metadata import TrajectoryMetadata
from trajectory.types.trajectory_upload_response import TrajectoryUploadResponse


class Trajectories(APIResource):
  @cached_property
  def with_raw_response(self) -> TrajectoriesWithRawResponse:
    return TrajectoriesWithRawResponse(self)

  @cached_property
  def artifacts(self) -> Artifacts:
    return Artifacts(self._client)

  @cached_property
  def steps(self) -> Steps:
    return Steps(self._client)

  def create(
    self,
    *,
    idempotency_key: str | None | Omit = omit,
    body: TrajectoriesCreateParams | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> CreateTrajectoryResponse:
    """Create a trajectory, or return the existing trajectory for a managed run.

    Args:
      idempotency_key: Required with `Trajectory-API-Version: tmp-contract`, which rejects a missing,
        blank or over-long key, including an SDK call that passes `idempotency_key=None`.
        Optional for legacy callers, whose key the API generates. Reuse this key when
        retrying a submission; the SDK generates one per call and reuses it across
        automatic retries.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/trajectories",
      cast_to=CreateTrajectoryResponse,
      body=(
        None if isinstance(body, Omit) else maybe_transform(body, TrajectoriesCreateParams | None)
      ),
      options=make_request_options(
        headers={
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=(
          {"Idempotency-Key": omit, **(extra_headers or {})}
          if idempotency_key is None
          else extra_headers
        ),
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
        idempotency_header=("Idempotency-Key" if isinstance(idempotency_key, Omit) else None),
      ),
    )

  def list(
    self,
    *,
    dataset_name: str | None | Omit = omit,
    training_run_id: str | None | Omit = omit,
    eval_run_id: str | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[TrajectoryMetadata]:
    """List Trajectories Route

    Args:
      training_run_id: List this run's training rollouts, including unfinished and failed trajectories,
        newest first.

      eval_run_id: List this evaluation's trajectories, including unfinished and failed attempts,
        newest first.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/trajectories",
      cast_to=SyncPage[TrajectoryMetadata],
      options=make_request_options(
        params=maybe_transform(
          {
            "dataset_name": dataset_name,
            "training_run_id": training_run_id,
            "eval_run_id": eval_run_id,
            "cursor": cursor,
            "limit": limit,
            "sort": sort,
            "order": order,
            "search": search,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve(
    self,
    trajectory_id: str,
    *,
    include_steps: bool | None | Omit = omit,
    include_reward_components: bool | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> Trajectory:
    """Detail

    Args:
      include_steps: Include every step; listTrajectorySteps pages them. Defaults to false with
        Trajectory-API-Version: tmp-contract and to true otherwise.

      include_reward_components: Include the reward components logged with log_reward. Defaults to false with
        Trajectory-API-Version: tmp-contract and to true otherwise.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/trajectories/{trajectory_id}",
        trajectory_id=trajectory_id,
      ),
      cast_to=Trajectory,
      options=make_request_options(
        params=maybe_transform(
          {
            "include_steps": include_steps,
            "include_reward_components": include_reward_components,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def upload(
    self,
    *,
    agent_id: str,
    dataset: str,
    trajectories: Iterable[Mapping[str, Any]] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> TrajectoryUploadResponse:
    """Upload

    Args:
      agent_id: Agent that owns the uploaded trajectories.

      dataset: Dataset name to upload these trajectories into.

      trajectories: Trajectory payloads to validate, store, and index.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/trajectories/upload",
      cast_to=TrajectoryUploadResponse,
      body=maybe_transform(
        {
          "agent_id": agent_id,
          "dataset": dataset,
          "trajectories": trajectories,
        },
        TrajectoriesUploadParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def log_event(
    self,
    trajectory_id: str,
    *,
    event_id: str,
    name: str,
    payload: Mapping[str, Any] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> LogTrajectoryEventResponse:
    """Log Trajectory Event

    Args:
      event_id: Caller-owned id used to dedupe retries of the same event. Stored as
        {trajectory_id}:{event_id} in a 128-character column.

      name: Harness event name.

      payload: Optional JSON object recorded with the event. It is not a reward component, but
        an automatic grader can read it.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/events",
        trajectory_id=trajectory_id,
      ),
      cast_to=LogTrajectoryEventResponse,
      body=maybe_transform(
        {
          "event_id": event_id,
          "name": name,
          "payload": payload,
        },
        TrajectoriesLogEventParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_events(
    self,
    trajectory_id: str,
    *,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[TrajectoryEvent]:
    """Read customer-submitted trajectory events, newest first, without telemetry metadata.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/events",
        trajectory_id=trajectory_id,
      ),
      cast_to=SyncPage[TrajectoryEvent],
      options=make_request_options(
        params=maybe_transform(
          {
            "cursor": cursor,
            "limit": limit,
            "sort": sort,
            "order": order,
            "search": search,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def log_reward(
    self,
    trajectory_id: str,
    *,
    name: str,
    value: float,
    min_value: float = 0.0,
    max_value: float = 1.0,
    explanation: str | Omit = omit,
    weight: float | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> LogTrajectoryRewardResponse:
    """Log Trajectory Reward

    Args:
      name: Reward component name. Each call adds one component; the trajectory's logged
        reward is the weighted average of its components' scaled values, (value -
        min_value) / (max_value - min_value).

      value: Finite raw reward between min_value and max_value, including endpoints.

      min_value: Minimum raw reward, default 0. Must be less than max_value.

      max_value: Maximum raw reward, default 1. The server scales the declared range
        to [0, 1] for training and preserves the raw value.

      explanation: Human-readable reason for this component's value.

      weight: Weight of this component in the trajectory's weighted average reward. Use 0 to
        store the component for diagnostics without counting it. If every component has
        weight 0, the trajectory's reward is 0.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    reward_values = {"value": value, "min_value": min_value, "max_value": max_value}
    if extra_body:
      reward_values.update({key: extra_body[key] for key in reward_values if key in extra_body})
    if any(
      isinstance(number, bool)
      or not isinstance(number, (int, float))
      or not -float("inf") < number < float("inf")
      for number in reward_values.values()
    ):
      raise ValueError("value, min_value and max_value must be finite numbers")
    minimum, maximum = reward_values["min_value"], reward_values["max_value"]
    if not minimum < maximum:
      raise ValueError("min_value must be less than max_value")
    if maximum - minimum == float("inf"):
      raise ValueError("max_value - min_value must be finite")
    if not minimum <= reward_values["value"] <= maximum:
      raise ValueError("value must be between min_value and max_value, including endpoints")
    return self._post(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/rewards",
        trajectory_id=trajectory_id,
      ),
      cast_to=LogTrajectoryRewardResponse,
      body=maybe_transform(
        {
          "reward_id": str(uuid4()),
          "name": name,
          "value": value,
          "min_value": min_value,
          "max_value": max_value,
          "explanation": explanation,
          "weight": weight,
        },
        TrajectoriesLogRewardParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def complete(
    self,
    trajectory_id: str,
    *,
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
    | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> CompleteTrajectoryResponse:
    """Complete Trajectory Route

    Args:
      termination_reason: How the attempt ended. Use ENV_DONE only when it finished normally.
        - ENV_DONE: finished normally, including a graded wrong answer.
        - ERROR: model requests failed after retries, or the environment or grader failed.
        - TIMEOUT: the harness stopped the agent at its own time limit.
        - TRUNCATION: the final reply was cut off at its output-token limit, or the
          conversation
          no longer fit the model's context.
        - MISSING_SUBMIT: the task requires a submission and the agent stopped without
          one.
        - LIMIT_REACHED, MAX_STEPS, STALE: set by the platform. A LIMIT_REACHED or
          MAX_STEPS it
          already set is kept.
        - GOLDEN_PATCH: reserved; do not send.

        Training uses ENV_DONE, LIMIT_REACHED and MAX_STEPS, plus TRUNCATION when the run
        sets
        train_on_truncation. LIMIT_REACHED, MAX_STEPS and TRUNCATION count positive
        rewards as 0.
        ERROR counts toward the run's failure limit and as failed in evaluation.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(trajectory_id, str) and not trajectory_id:
      raise ValueError(
        f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/trajectories/{trajectory_id}/complete",
        trajectory_id=trajectory_id,
      ),
      cast_to=CompleteTrajectoryResponse,
      body=maybe_transform(
        {
          "termination_reason": termination_reason,
        },
        TrajectoriesCompleteParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class TrajectoriesWithRawResponse:
  def __init__(self, resource: Trajectories) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.upload = to_raw_response_wrapper(resource.upload)
    self.log_event = to_raw_response_wrapper(resource.log_event)
    self.list_events = to_raw_response_wrapper(resource.list_events)
    self.log_reward = to_raw_response_wrapper(resource.log_reward)
    self.complete = to_raw_response_wrapper(resource.complete)

  @cached_property
  def artifacts(self) -> ArtifactsWithRawResponse:
    return ArtifactsWithRawResponse(self._resource.artifacts)

  @cached_property
  def steps(self) -> StepsWithRawResponse:
    return StepsWithRawResponse(self._resource.steps)
