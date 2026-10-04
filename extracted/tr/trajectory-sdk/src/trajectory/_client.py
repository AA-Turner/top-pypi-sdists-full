# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from collections.abc import Mapping
from functools import cached_property
from typing import TYPE_CHECKING, Self

import httpx

from trajectory._base_client import DEFAULT_MAX_RETRIES, APIClient, _merge_headers
from trajectory._types import NotGiven, not_given

if TYPE_CHECKING:
  from trajectory.resources.agents import Agents
  from trajectory.resources.artifacts import Artifacts
  from trajectory.resources.benchmarks.benchmarks import Benchmarks
  from trajectory.resources.chat.chat import Chat
  from trajectory.resources.datasets import Datasets
  from trajectory.resources.deployments import Deployments
  from trajectory.resources.diagnostics import Diagnostics
  from trajectory.resources.evals.evals import Evals
  from trajectory.resources.inference import Inference
  from trajectory.resources.organizations import Organizations
  from trajectory.resources.responses import Responses
  from trajectory.resources.secrets import Secrets
  from trajectory.resources.telemetry import Telemetry
  from trajectory.resources.training.training import Training
  from trajectory.resources.trajectories.trajectories import Trajectories


class Client(APIClient):
  def __init__(
    self,
    api_key: str | None = None,
    base_url: str | httpx.URL | None = None,
    http_client: httpx.Client | None = None,
    timeout: httpx.Timeout | float | None | NotGiven = not_given,
    max_retries: int = DEFAULT_MAX_RETRIES,
    default_headers: Mapping[str, str] | None = None,
    default_query: Mapping[str, object] | None = None,
    _strict_response_validation: bool = False,
  ) -> None:
    if api_key is None:
      api_key = os.environ.get("TRAJECTORY_API_KEY")
    if base_url is None:
      base_url = os.environ.get("TRAJECTORY_BASE_URL", "https://api.trajectory.ai")
    self.api_key = api_key
    self._custom_headers = dict(default_headers or {})
    self._custom_query = dict(default_query or {})
    super().__init__(
      base_url=base_url,
      http_client=http_client,
      timeout=timeout,
      default_query=self._custom_query,
      max_retries=max_retries,
      _strict_response_validation=_strict_response_validation,
    )

  @property
  def auth_headers(self) -> dict[str, str]:
    if self.api_key is not None:
      return {"X-API-Key": self.api_key}
    return {}

  @property
  def default_headers(self) -> dict[str, str]:
    return _merge_headers(super().default_headers, self.auth_headers, self._custom_headers)

  def copy(
    self,
    api_key: str | None = None,
    base_url: str | httpx.URL | None = None,
    timeout: httpx.Timeout | float | None | NotGiven = not_given,
    http_client: httpx.Client | None = None,
    max_retries: int | NotGiven = not_given,
    default_headers: Mapping[str, str] | None = None,
    set_default_headers: Mapping[str, str] | None = None,
    default_query: Mapping[str, object] | None = None,
    set_default_query: Mapping[str, object] | None = None,
    _strict_response_validation: bool | None = None,
  ) -> Self:
    if default_headers is not None and set_default_headers is not None:
      raise ValueError("default_headers and set_default_headers are mutually exclusive")
    if default_query is not None and set_default_query is not None:
      raise ValueError("default_query and set_default_query are mutually exclusive")
    headers = self._custom_headers
    if default_headers is not None:
      headers = _merge_headers(headers, default_headers)
    elif set_default_headers is not None:
      headers = dict(set_default_headers)
    query = self._custom_query
    if default_query is not None:
      query = {**query, **default_query}
    elif set_default_query is not None:
      query = dict(set_default_query)
    copied_api_key = self.api_key
    if api_key is not None:
      copied_api_key = api_key
    return self.__class__(
      api_key=copied_api_key,
      base_url=base_url or self.base_url,
      timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
      http_client=http_client or self._client,
      max_retries=self.max_retries if isinstance(max_retries, NotGiven) else max_retries,
      default_headers=headers,
      default_query=query,
      _strict_response_validation=(
        self._strict_response_validation
        if _strict_response_validation is None
        else _strict_response_validation
      ),
    )

  with_options = copy

  @cached_property
  def agents(self) -> Agents:
    from trajectory.resources.agents import Agents

    return Agents(self)

  @cached_property
  def artifacts(self) -> Artifacts:
    from trajectory.resources.artifacts import Artifacts

    return Artifacts(self)

  @cached_property
  def benchmarks(self) -> Benchmarks:
    from trajectory.resources.benchmarks.benchmarks import Benchmarks

    return Benchmarks(self)

  @cached_property
  def diagnostics(self) -> Diagnostics:
    from trajectory.resources.diagnostics import Diagnostics

    return Diagnostics(self)

  @cached_property
  def chat(self) -> Chat:
    from trajectory.resources.chat.chat import Chat

    return Chat(self)

  @cached_property
  def responses(self) -> Responses:
    from trajectory.resources.responses import Responses

    return Responses(self)

  @cached_property
  def deployments(self) -> Deployments:
    from trajectory.resources.deployments import Deployments

    return Deployments(self)

  @cached_property
  def evals(self) -> Evals:
    from trajectory.resources.evals.evals import Evals

    return Evals(self)

  @cached_property
  def inference(self) -> Inference:
    from trajectory.resources.inference import Inference

    return Inference(self)

  @cached_property
  def organizations(self) -> Organizations:
    from trajectory.resources.organizations import Organizations

    return Organizations(self)

  @cached_property
  def secrets(self) -> Secrets:
    from trajectory.resources.secrets import Secrets

    return Secrets(self)

  @cached_property
  def telemetry(self) -> Telemetry:
    from trajectory.resources.telemetry import Telemetry

    return Telemetry(self)

  @cached_property
  def training(self) -> Training:
    from trajectory.resources.training.training import Training

    return Training(self)

  @cached_property
  def trajectories(self) -> Trajectories:
    from trajectory.resources.trajectories.trajectories import Trajectories

    return Trajectories(self)

  @cached_property
  def datasets(self) -> Datasets:
    from trajectory.resources.datasets import Datasets

    return Datasets(self)
