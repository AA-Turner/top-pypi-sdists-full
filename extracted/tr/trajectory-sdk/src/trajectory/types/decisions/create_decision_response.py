# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class ChoiceProbabilityResponse(BaseModel):
  value: str

  probability: float


class DecisionUsageResponse(BaseModel):
  prompt_tokens: int

  completion_tokens: int

  total_tokens: int


class DecisionAnswerResponse(BaseModel):
  name: str

  choice: str

  probabilities: list[ChoiceProbabilityResponse]

  confidence: float

  usage: DecisionUsageResponse | None = None


class CreateDecisionResponse(BaseModel):
  id: str

  object: Literal["decision"] = "decision"

  created: int

  model: str

  result: DecisionAnswerResponse | None
