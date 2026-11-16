# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable

import httpx2

from trajectory._base_client import make_request_options, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.create_decision_params import CreateDecisionParams, DecisionQuestionInputParam
from trajectory.types.decisions.create_decision_response import CreateDecisionResponse


class Decisions(APIResource):
  @cached_property
  def with_raw_response(self) -> DecisionsWithRawResponse:
    return DecisionsWithRawResponse(self)

  def create(
    self,
    *,
    x_trajectory_id: str,
    model: str,
    input: str,
    questions: Iterable[DecisionQuestionInputParam],
    idempotency_key: str | None | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> CreateDecisionResponse:
    """Create Decision

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/v1/decisions",
      cast_to=CreateDecisionResponse,
      body=maybe_transform(
        {
          "model": model,
          "input": input,
          "questions": questions,
        },
        CreateDecisionParams,
      ),
      options=make_request_options(
        headers={
          "X-Trajectory-Id": serialize_header(x_trajectory_id),
          "Idempotency-Key": serialize_header(idempotency_key),
        },
        extra_headers=(
          {"Idempotency-Key": omit, **(extra_headers or {})}
          if idempotency_key is None
          else extra_headers
        ),
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
        idempotency_header=("Idempotency-Key" if isinstance(idempotency_key, Omit) else None),
      ),
    )


class DecisionsWithRawResponse:
  def __init__(self, resource: Decisions) -> None:
    self._resource = resource
    self.create = to_raw_response_wrapper(resource.create)
