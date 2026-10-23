# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal, Mapping, overload

import httpx2

from trajectory._base_client import SyncPage, make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._streaming import Stream
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.chat_completion_params import ChatCompletionParams, ChatMessageParam
from trajectory.types.deployments.deployment import Deployment
from trajectory.types.deployments.deployments_create_params import (
  DeploymentsCreateParams,
  ModelEndpointConfigParam,
)
from trajectory.types.deployments.deployments_promote_params import DeploymentsPromoteParams
from trajectory.types.deployments_summary import DeploymentsSummary
from trajectory.types.inference.chat_completion_chunk import ChatCompletionChunk
from trajectory.types.inference.chat_completion_response import ChatCompletionResponse
from trajectory.types.promote_response import PromoteResponse
from trajectory.types.start_deploy_response import StartDeployResponse
from trajectory.types.undeploy_response import UndeployResponse


class Deployments(APIResource):
  @cached_property
  def with_raw_response(self) -> DeploymentsWithRawResponse:
    return DeploymentsWithRawResponse(self)

  def list(
    self,
    *,
    status: Literal["PENDING", "DEPLOYING", "DEPLOYED", "FAILED", "CANCELLING", "CANCELLED"]
    | None
    | Omit = omit,
    cursor: str | None | Omit = omit,
    limit: int | Omit = omit,
    sort: str | None | Omit = omit,
    order: Literal["asc", "desc"] | Omit = omit,
    search: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SyncPage[Deployment]:
    """List Deployments Route

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/deploy",
      cast_to=SyncPage[Deployment],
      options=make_request_options(
        params=maybe_transform(
          {
            "status": status,
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

  def create(
    self,
    *,
    checkpoint_id: str,
    test_model_slug: str,
    idempotency_key: str | Omit = omit,
    agent_id: str | None | Omit = omit,
    model_endpoint_config: ModelEndpointConfigParam | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> StartDeployResponse:
    """Serve a committed checkpoint through Model Endpoint.

    Args:
      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      agent_id: Owning agent; inferred from the checkpoint when omitted.

      model_endpoint_config: Model and tokenizer identity for the deployment; defaults to the originating
        Training Service run. Sampling overrides and training limits are cleared.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/deploy",
      cast_to=StartDeployResponse,
      body=maybe_transform(
        {
          "checkpoint_id": checkpoint_id,
          "test_model_slug": test_model_slug,
          "agent_id": agent_id,
          "model_endpoint_config": model_endpoint_config,
        },
        DeploymentsCreateParams,
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

  def retrieve(
    self,
    deployment_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> Deployment:
    """Get Deployment Route

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._get(
      path_template(
        "/api/v1/deploy/{deployment_id}",
        deployment_id=deployment_id,
      ),
      cast_to=Deployment,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retry(
    self,
    deployment_id: str,
    *,
    idempotency_key: str | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> StartDeployResponse:
    """Retry a failed or cancelled deployment in place after cleanup. Keeps its deployment ID,
    test model slug, checkpoint, and saved configuration.

    Args:
      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/deploy/{deployment_id}/retry",
        deployment_id=deployment_id,
      ),
      cast_to=StartDeployResponse,
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

  def delete(
    self,
    deployment_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> UndeployResponse:
    """Delete a deployment and its Model Endpoint resources.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._delete(
      path_template(
        "/api/v1/deploy/{deployment_id}",
        deployment_id=deployment_id,
      ),
      cast_to=UndeployResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def promote(
    self,
    deployment_id: str,
    *,
    expected_deployment_id: str | None,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> PromoteResponse:
    """Make a deployed deployment the active target for its slug.

    Args:
      expected_deployment_id: Expected current production target; null for initial promotion.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/deploy/{deployment_id}/promote",
        deployment_id=deployment_id,
      ),
      cast_to=PromoteResponse,
      body=maybe_transform(
        {
          "expected_deployment_id": expected_deployment_id,
        },
        DeploymentsPromoteParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def unpromote(
    self,
    deployment_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> PromoteResponse:
    """Clear a deployment's active flag so its slug serves nothing.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/deploy/{deployment_id}/unpromote",
        deployment_id=deployment_id,
      ),
      cast_to=PromoteResponse,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def summarize(
    self,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DeploymentsSummary:
    """Summary

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/api/v1/deploy/summary",
      cast_to=DeploymentsSummary,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  @overload
  def create_chat_completion(
    self,
    deployment_id: str,
    *,
    x_trajectory_id: str,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    stream: Literal[False] | None | Omit = omit,
    disable_thinking: bool | None | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse: ...

  @overload
  def create_chat_completion(
    self,
    deployment_id: str,
    *,
    x_trajectory_id: str,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    stream: Literal[True],
    disable_thinking: bool | None | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> Stream[ChatCompletionChunk]: ...

  @overload
  def create_chat_completion(
    self,
    deployment_id: str,
    *,
    x_trajectory_id: str,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    stream: bool,
    disable_thinking: bool | None | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse | Stream[ChatCompletionChunk]: ...

  def create_chat_completion(
    self,
    deployment_id: str,
    *,
    x_trajectory_id: str,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    stream: bool | None | Omit = omit,
    disable_thinking: bool | None | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse | Stream[ChatCompletionChunk]:
    """Test this exact deployment without changing the slug's production target.

    Args:
      max_tokens: Maximum generated tokens, including reasoning tokens when emitted.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(deployment_id, str) and not deployment_id:
      raise ValueError(
        f"Expected a non-empty value for `deployment_id` but received {deployment_id!r}"
      )
    return self._post(
      path_template(
        "/api/v1/deploy/{deployment_id}/chat/completions",
        deployment_id=deployment_id,
      ),
      cast_to=ChatCompletionResponse,
      stream=stream is True,
      stream_cls=Stream[ChatCompletionChunk],
      body=maybe_transform(
        {
          "model": model,
          "messages": messages,
          "stream": stream,
          "disable_thinking": disable_thinking,
          "temperature": temperature,
          "max_tokens": max_tokens,
          "top_p": top_p,
        },
        ChatCompletionParams,
      ),
      options=make_request_options(
        headers={
          "X-Trajectory-Id": serialize_header(x_trajectory_id),
        },
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class DeploymentsWithRawResponse:
  def __init__(self, resource: Deployments) -> None:
    self._resource = resource
    self.list = to_raw_response_wrapper(resource.list)
    self.create = to_raw_response_wrapper(resource.create)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.retry = to_raw_response_wrapper(resource.retry)
    self.delete = to_raw_response_wrapper(resource.delete)
    self.promote = to_raw_response_wrapper(resource.promote)
    self.unpromote = to_raw_response_wrapper(resource.unpromote)
    self.summarize = to_raw_response_wrapper(resource.summarize)
    self.create_chat_completion = to_raw_response_wrapper(resource.create_chat_completion)
