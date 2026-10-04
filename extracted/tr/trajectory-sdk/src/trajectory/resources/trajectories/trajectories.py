# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal, Mapping

import httpx

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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> CreateTrajectoryResponse:
    """Create a trajectory, or return the existing trajectory for a managed run.

    Args:
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
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
    include_steps: bool | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> Trajectory:
    """Detail

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
        "/api/v1/trajectories/{trajectory_id}",
        trajectory_id=trajectory_id,
      ),
      cast_to=Trajectory,
      options=make_request_options(
        params=maybe_transform(
          {
            "include_steps": include_steps,
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> LogTrajectoryEventResponse:
    """Log Trajectory Event

    Args:
      event_id: Caller-owned id used to dedupe retries of the same event. Stored as
        {trajectory_id}:{event_id} in a 128-character column.

      name: Harness event name.

      payload: Optional structured event payload. Does not affect training reward.

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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
    reward_id: str,
    name: str,
    value: float,
    explanation: str | Omit = omit,
    weight: float | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> LogTrajectoryRewardResponse:
    """Log Trajectory Reward

    Args:
      reward_id: Caller-owned id used to dedupe retries of the same reward component.

      name: Reward component name.

      value: Raw reward value.

      explanation: Human-readable reason for the reward.

      weight: Weight of this component in the trajectory's summed reward. Use 0 to store the
        component for diagnostics without counting it. If every component has weight 0,
        the trajectory's reward is 0.

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
        "/api/v1/trajectories/{trajectory_id}/rewards",
        trajectory_id=trajectory_id,
      ),
      cast_to=LogTrajectoryRewardResponse,
      body=maybe_transform(
        {
          "reward_id": reward_id,
          "name": name,
          "value": value,
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
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> CompleteTrajectoryResponse:
    """Complete Trajectory Route

    Args:
      termination_reason: Why the harness finished. ENV_DONE is successful completion.

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
