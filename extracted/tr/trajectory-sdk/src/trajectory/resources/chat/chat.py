# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property

from trajectory._resource import APIResource
from trajectory.resources.chat.completions import Completions, CompletionsWithRawResponse


class Chat(APIResource):
  @cached_property
  def with_raw_response(self) -> ChatWithRawResponse:
    return ChatWithRawResponse(self)

  @cached_property
  def completions(self) -> Completions:
    return Completions(self._client)


class ChatWithRawResponse:
  def __init__(self, resource: Chat) -> None:
    self._resource = resource

  @cached_property
  def completions(self) -> CompletionsWithRawResponse:
    return CompletionsWithRawResponse(self._resource.completions)
