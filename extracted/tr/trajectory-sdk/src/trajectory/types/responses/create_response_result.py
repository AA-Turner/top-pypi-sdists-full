# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Literal

from trajectory._models import BaseModel
from trajectory.types.response_function_tool_call import ResponseFunctionToolCall
from trajectory.types.response_output_message import ResponseOutputMessage, ResponseOutputText
from trajectory.types.response_reasoning_item import ResponseReasoningItem


class ResponseFunctionTool(BaseModel):
  name: str

  type: Literal["function"]

  parameters: dict[str, Any] | None = None

  strict: bool | None = None

  description: str | None = None


class ResponseIncompleteDetails(BaseModel):
  reason: Literal["max_output_tokens", "content_filter"] | None = None


class ResponseInputTokensDetails(BaseModel):
  cached_tokens: int


class ResponseOutputTokensDetails(BaseModel):
  reasoning_tokens: int


class ResponseUsage(BaseModel):
  input_tokens: int

  input_tokens_details: ResponseInputTokensDetails

  output_tokens: int

  output_tokens_details: ResponseOutputTokensDetails

  total_tokens: int


class CreateResponseResult(BaseModel):
  id: str

  object: str

  created_at: float

  status: str

  model: str

  output: list[ResponseOutputMessage | ResponseFunctionToolCall | ResponseReasoningItem]

  usage: ResponseUsage | None = None

  incomplete_details: ResponseIncompleteDetails | None = None

  instructions: str | None = None

  parallel_tool_calls: bool | None = None

  previous_response_id: str | None = None

  tool_choice: str | None = None

  tools: list[ResponseFunctionTool] | None = None

  @property
  def output_text(self) -> str:
    """Return the concatenated text from response message output items."""
    return "".join(
      part.text
      for item in self.output
      if isinstance(item, ResponseOutputMessage) and item.type == "message"
      for part in item.content
      if isinstance(part, ResponseOutputText) and part.type == "output_text"
    )
