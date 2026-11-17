# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, Required, TypedDict


class DecisionChoiceInputParam(TypedDict, total=False):
  value: Required[str]
  description: str


class DecisionQuestionInputParam(TypedDict, total=False):
  type: Required[Literal["choice"]]
  name: Required[str]
  instructions: Required[str]
  choices: Required[Iterable[DecisionChoiceInputParam]]


class ImagePartParam(TypedDict, total=False):
  artifact_id: Required[str]
  """
  Image artifact attached to this trajectory. Use its artifact read endpoint to request a
  download URL.
  """
  type: Literal["image"]
  """
  Identifies an image content part.
  """


class TextPartParam(TypedDict, total=False):
  text: Required[str]
  """
  Text at this position in the message content.
  """
  type: Literal["text"]
  """
  Identifies a text content part.
  """


class CreateDecisionParams(TypedDict, total=False):
  model: Required[str]
  input: Required[str | Iterable[TextPartParam | ImagePartParam]]
  questions: Required[Iterable[DecisionQuestionInputParam]]
