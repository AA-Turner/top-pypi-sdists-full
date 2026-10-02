# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal, Mapping, overload

import httpx

from trajectory._base_client import make_request_options, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._streaming import Stream
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.chat_completion_params import ChatCompletionParams, ChatMessageParam
from trajectory.types.inference.chat_completion_chunk import ChatCompletionChunk
from trajectory.types.inference.chat_completion_response import ChatCompletionResponse


class Completions(APIResource):
  @cached_property
  def with_raw_response(self) -> CompletionsWithRawResponse:
    return CompletionsWithRawResponse(self)

  @overload
  def create(
    self,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    x_trajectory_id: str | None | Omit = omit,
    idempotency_key: str | None | Omit = omit,
    x_model_endpoint_id: str | None | Omit = omit,
    x_model_endpoint_access_token: str | None | Omit = omit,
    stream: Literal[False] | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse: ...

  @overload
  def create(
    self,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    x_trajectory_id: str | None | Omit = omit,
    idempotency_key: str | None | Omit = omit,
    x_model_endpoint_id: str | None | Omit = omit,
    x_model_endpoint_access_token: str | None | Omit = omit,
    stream: Literal[True],
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> Stream[ChatCompletionChunk]: ...

  @overload
  def create(
    self,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    x_trajectory_id: str | None | Omit = omit,
    idempotency_key: str | None | Omit = omit,
    x_model_endpoint_id: str | None | Omit = omit,
    x_model_endpoint_access_token: str | None | Omit = omit,
    stream: bool,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse | Stream[ChatCompletionChunk]: ...

  def create(
    self,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    x_trajectory_id: str | None | Omit = omit,
    idempotency_key: str | None | Omit = omit,
    x_model_endpoint_id: str | None | Omit = omit,
    x_model_endpoint_access_token: str | None | Omit = omit,
    stream: bool | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse | Stream[ChatCompletionChunk]:
    """Create Chat Completion

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/v1/chat/completions",
      cast_to=ChatCompletionResponse,
      stream=stream is True,
      stream_cls=Stream[ChatCompletionChunk],
      body=maybe_transform(
        {
          "model": model,
          "messages": messages,
          "stream": stream,
          "temperature": temperature,
          "max_tokens": max_tokens,
          "top_p": top_p,
        },
        ChatCompletionParams,
      ),
      options=make_request_options(
        headers={
          "X-Trajectory-Id": serialize_header(x_trajectory_id),
          "Idempotency-Key": serialize_header(idempotency_key),
          "X-Model-Endpoint-Id": serialize_header(x_model_endpoint_id),
          "x-model-endpoint-access-token": serialize_header(x_model_endpoint_access_token),
        },
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class CompletionsWithRawResponse:
  def __init__(self, resource: Completions) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
