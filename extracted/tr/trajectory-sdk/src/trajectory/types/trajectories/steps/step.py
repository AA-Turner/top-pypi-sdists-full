# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class ImagePart(BaseModel):
  artifact_id: str
  """
    Image artifact attached to this trajectory. Use its artifact read endpoint to request a
    download URL.
    """

  type: Literal["image"] = "image"
  """Identifies an image content part."""


class TextPart(BaseModel):
  text: str
  """Text at this position in the message content."""

  type: Literal["text"] = "text"
  """Identifies a text content part."""


class Message(BaseModel):
  message_id: int

  role: str | None = None

  content: str | list[TextPart | ImagePart] | None = None
  """Message text, an ordered list of text and image artifact references, or null."""

  tool_calls: str | None = None

  tool_response: str | None = None

  reasoning: str | None = None

  finish_reason: str | None = None

  prompt_tokens: int | None = None

  completion_tokens: int | None = None


class Step(BaseModel):
  step_index: int

  reward: float | None = None

  has_error: bool = False

  messages: list[Message] | None = None
