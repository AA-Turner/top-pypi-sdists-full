# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.response_function_tool_call import ResponseFunctionToolCall
from trajectory.types.response_output_message import ResponseOutputMessage
from trajectory.types.response_reasoning_item import ResponseReasoningItem
from trajectory.types.responses.create_response_result import CreateResponseResult


class ResponseStreamEvent(BaseModel):
  type: str

  sequence_number: int

  response: CreateResponseResult | None = None

  item: ResponseOutputMessage | ResponseFunctionToolCall | ResponseReasoningItem | None = None

  output_index: int | None = None

  content_index: int | None = None

  item_id: str | None = None

  delta: str | None = None

  text: str | None = None
