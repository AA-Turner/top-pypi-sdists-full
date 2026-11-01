# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, Required, TypedDict

from trajectory.types.create_response_params import CreateResponseParams


class ResponsesInferenceOperationInputParam(TypedDict, total=False):
  api: Required[Literal["responses"]]
  input: Required[CreateResponseParams | Mapping[str, Any]]
