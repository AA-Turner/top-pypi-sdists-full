# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable, Literal, Mapping, overload

import httpx

from trajectory._base_client import make_request_options, path_template
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._streaming import Stream
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.chat_completion_params import ChatCompletionParams, ChatMessageParam
from trajectory.types.inference.chat_completion_chunk import ChatCompletionChunk
from trajectory.types.inference.chat_completion_response import ChatCompletionResponse
from trajectory.types.inference.model import Model
from trajectory.types.model_list import ModelList


class Inference(APIResource):
  @cached_property
  def with_raw_response(self) -> InferenceWithRawResponse:
    return InferenceWithRawResponse(self)

  @overload
  def create_playground_chat_completion(
    self,
    path_model: str,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
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
  def create_playground_chat_completion(
    self,
    path_model: str,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
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
  def create_playground_chat_completion(
    self,
    path_model: str,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    stream: bool,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse | Stream[ChatCompletionChunk]: ...

  def create_playground_chat_completion(
    self,
    path_model: str,
    *,
    model: str,
    messages: Iterable[ChatMessageParam | Mapping[str, Any]],
    stream: bool | Omit = omit,
    temperature: float | None | Omit = omit,
    max_tokens: int | None | Omit = omit,
    top_p: float | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ChatCompletionResponse | Stream[ChatCompletionChunk]:
    """Create Playground Chat Completion

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(path_model, str) and not path_model:
      raise ValueError(f"Expected a non-empty value for `path_model` but received {path_model!r}")
    return self._post(
      path_template(
        "/v1/playground/{path_model}/chat/completions",
        path_model=path_model,
      ),
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
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def list_models(
    self,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> ModelList:
    """List Models

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._get(
      "/v1/models",
      cast_to=ModelList,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def retrieve_model(
    self,
    model: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx.Timeout | None | NotGiven = not_given,
  ) -> Model:
    """Get Model

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(model, str) and not model:
      raise ValueError(f"Expected a non-empty value for `model` but received {model!r}")
    return self._get(
      path_template(
        "/v1/models/{model}",
        model=model,
      ),
      cast_to=Model,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class InferenceWithRawResponse:
  def __init__(self, resource: Inference) -> None:
    self._resource = resource
    self.create_playground_chat_completion = to_raw_response_wrapper(
      resource.create_playground_chat_completion
    )
    self.list_models = to_raw_response_wrapper(resource.list_models)
    self.retrieve_model = to_raw_response_wrapper(resource.retrieve_model)
