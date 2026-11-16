# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, Required, TypedDict

from trajectory.types.create_decision_params import CreateDecisionParams


class DecisionsInferenceOperationInputParam(TypedDict, total=False):
  api: Required[Literal["decisions"]]
  input: Required[CreateDecisionParams]
