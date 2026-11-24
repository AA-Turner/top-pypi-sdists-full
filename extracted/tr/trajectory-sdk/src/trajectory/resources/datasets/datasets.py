# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Literal

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, SequenceNotStr, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.resources.datasets.members import Members, MembersWithRawResponse
from trajectory.resources.datasets.operations import Operations, OperationsWithRawResponse
from trajectory.types.datasets.dataset_version import DatasetVersion
from trajectory.types.datasets.datasets_add_trajectories_params import (
  BestPerTaskFilterParam,
  DatasetsAddTrajectoriesParams,
  NoErrorsFilterParam,
  RewardThresholdFilterParam,
)
from trajectory.types.datasets.datasets_copy_params import DatasetsCopyParams
from trajectory.types.datasets.datasets_create_params import DatasetsCreateParams
from trajectory.types.datasets.operations.dataset_operation import DatasetOperation


class Datasets(APIResource):
  @cached_property
  def with_raw_response(self) -> DatasetsWithRawResponse:
    return DatasetsWithRawResponse(self)

  @cached_property
  def members(self) -> Members:
    return Members(self._client)

  @cached_property
  def operations(self) -> Operations:
    return Operations(self._client)

  def create(
    self,
    *,
    name: str,
    idempotency_key: str | Omit = omit,
    agent_id: str | None | Omit = omit,
    agent_name: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetVersion:
    """Create an empty draft dataset. When finished adding trajectories, call finalize to use
    the dataset.

    Args:
      name: Dataset name; datasets that share a name are versions of it. Only letters, digits,
        spaces, hyphens, underscores, and periods.

      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      agent_id: The dataset's agent ID. Provide agent_id or agent_name.

      agent_name: The dataset's agent name. Provide agent_id or agent_name.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/datasets",
      cast_to=DatasetVersion,
      body=maybe_transform(
        {
          "name": name,
          "agent_id": agent_id,
          "agent_name": agent_name,
        },
        DatasetsCreateParams,
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
    agent_id: str,
    name: str | None | Omit = omit,
    status: Literal["draft", "finalized"] | None | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[DatasetVersion]:
    """List the versions of a dataset name, newest first.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/datasets",
      cast_to=SyncPage[DatasetVersion],
      options=make_request_options(
        params=maybe_transform(
          {
            "agent_id": agent_id,
            "name": name,
            "status": status,
            "cursor": omit if cursor is None else cursor,
            "limit": limit,
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
    dataset_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetVersion:
    """Retrieve a draft or finalized dataset with its metadata and split counts.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(dataset_id, str) and not dataset_id:
      raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
    return self._get(
      path_template(
        "/api/v1/datasets/{dataset_id}",
        dataset_id=dataset_id,
      ),
      cast_to=DatasetVersion,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve_by_name(
    self,
    *,
    agent_id: str,
    name: str,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetVersion:
    """Retrieve the latest finalized dataset by agent ID and dataset name.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/datasets/latest",
      cast_to=DatasetVersion,
      options=make_request_options(
        params=maybe_transform(
          {
            "agent_id": agent_id,
            "name": name,
          }
        ),
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def add_trajectories(
    self,
    dataset_id: str,
    *,
    filter: RewardThresholdFilterParam | NoErrorsFilterParam | BestPerTaskFilterParam,
    idempotency_key: str | Omit = omit,
    training_run_ids: SequenceNotStr[str] | Omit = omit,
    eval_run_ids: SequenceNotStr[str] | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetOperation:
    """Add a training/eval run's trajectories to a draft dataset. Poll the returned operation.

    Args:
      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      training_run_ids: Succeeded or cancelled training runs whose completed train attempts join the train
        split.

      eval_run_ids: Completed eval runs whose scored attempts join the heldout split.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(dataset_id, str) and not dataset_id:
      raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
    return self._post(
      path_template(
        "/api/v1/datasets/{dataset_id}/trajectories",
        dataset_id=dataset_id,
      ),
      cast_to=DatasetOperation,
      body=maybe_transform(
        {
          "filter": filter,
          "training_run_ids": training_run_ids,
          "eval_run_ids": eval_run_ids,
        },
        DatasetsAddTrajectoriesParams,
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

  def copy(
    self,
    dataset_id: str,
    *,
    source_dataset_id: str,
    idempotency_key: str | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetOperation:
    """Copy a finalized dataset's trajectories into this draft. Poll the returned operation.

    Args:
      source_dataset_id: Finalized dataset whose trajectories are copied, keeping their splits.

      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(dataset_id, str) and not dataset_id:
      raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
    return self._post(
      path_template(
        "/api/v1/datasets/{dataset_id}/copy",
        dataset_id=dataset_id,
      ),
      cast_to=DatasetOperation,
      body=maybe_transform(
        {
          "source_dataset_id": source_dataset_id,
        },
        DatasetsCopyParams,
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

  def finalize(
    self,
    dataset_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DatasetVersion:
    """Finalize a dataset to make it usable for training.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(dataset_id, str) and not dataset_id:
      raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
    return self._post(
      path_template(
        "/api/v1/datasets/{dataset_id}/finalize",
        dataset_id=dataset_id,
      ),
      cast_to=DatasetVersion,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def delete(
    self,
    dataset_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> httpx2.Response:
    """Delete a dataset; refused while a training or evaluation run reads it

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(dataset_id, str) and not dataset_id:
      raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
    return self._delete(
      path_template(
        "/api/v1/datasets/{dataset_id}",
        dataset_id=dataset_id,
      ),
      cast_to=None,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class DatasetsWithRawResponse:
  def __init__(self, resource: Datasets) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
    self.list = to_raw_response_wrapper(resource.list)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.retrieve_by_name = to_raw_response_wrapper(resource.retrieve_by_name)
    self.add_trajectories = to_raw_response_wrapper(resource.add_trajectories)
    self.copy = to_raw_response_wrapper(resource.copy)
    self.finalize = to_raw_response_wrapper(resource.finalize)
    self.delete = to_raw_response_wrapper(resource.delete)

  @cached_property
  def members(self) -> MembersWithRawResponse:
    return MembersWithRawResponse(self._resource.members)

  @cached_property
  def operations(self) -> OperationsWithRawResponse:
    return OperationsWithRawResponse(self._resource.operations)
