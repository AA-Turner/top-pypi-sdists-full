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


class CreateDecisionParams(TypedDict, total=False):
  model: Required[str]
  input: Required[str]
  questions: Required[Iterable[DecisionQuestionInputParam]]
