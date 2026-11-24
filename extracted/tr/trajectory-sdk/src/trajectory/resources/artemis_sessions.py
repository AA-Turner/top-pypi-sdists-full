# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from functools import cached_property
from typing import Any

import httpx2

from trajectory._base_client import make_request_options, path_template, serialize_header
from trajectory._resource import APIResource
from trajectory._response import to_raw_response_wrapper
from trajectory._types import Headers, NotGiven, Omit, not_given, omit
from trajectory._utils import maybe_transform
from trajectory.types.artemis_sessions.artemis_session import ArtemisSession
from trajectory.types.artemis_sessions.artemis_sessions_decide_params import (
  ArtemisSessionsDecideParams,
)
from trajectory.types.artemis_sessions.artemis_sessions_send_params import ArtemisSessionsSendParams
from trajectory.types.decide_artemis_response import DecideArtemisResponse
from trajectory.types.send_artemis_message_response import SendArtemisMessageResponse


class ArtemisSessions(APIResource):
  @cached_property
  def with_raw_response(self) -> ArtemisSessionsWithRawResponse:
    return ArtemisSessionsWithRawResponse(self)

  def send(
    self,
    *,
    message: str,
    idempotency_key: str | Omit = omit,
    session_id: str | None | Omit = omit,
    write_handoff: bool | Omit = omit,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> SendArtemisMessageResponse:
    """Store a message for Artemis, starting a session or continuing one, and wake the session.
    Answers at once; read the session to follow its turns. Retrying with the same
    Idempotency-Key stores and answers the message once.

    Args:
      message: What to ask Artemis, at most 32768 UTF-8 bytes.

      idempotency_key: Optional. Without a key, repeated submissions are treated as separate actions. A
        blank or over-long key is rejected. Reuse this key when retrying a submission; the
        SDK generates one per call and reuses it across automatic retries.

      session_id: A session to continue; omit it to start a new session.

      write_handoff: Start a session whose writes come back to the caller as each turn's proposals, for
        it to make itself, instead of waiting for an approval here. Set when starting a
        session; a message to a session started otherwise is refused.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    return self._post(
      "/api/v1/artemis/sessions/messages",
      cast_to=SendArtemisMessageResponse,
      body=maybe_transform(
        {
          "message": message,
          "session_id": session_id,
          "write_handoff": write_handoff,
        },
        ArtemisSessionsSendParams,
      ),
      options=make_request_options(
        headers={
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

  def retrieve(
    self,
    session_id: str,
    *,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> ArtemisSession:
    """A session's latest 20 turns: each completed turn's answer, links and saved files, then a
    running or failed turn while messages wait. Poll until running is false.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(session_id, str) and not session_id:
      raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
    return self._get(
      path_template(
        "/api/v1/artemis/sessions/{session_id}",
        session_id=session_id,
      ),
      cast_to=ArtemisSession,
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )

  def decide(
    self,
    session_id: str,
    *,
    request_id: str,
    digest: str,
    approve: bool,
    extra_headers: Headers | None = None,
    extra_query: dict[str, Any] | None = None,
    extra_body: dict[str, Any] | None = None,
    timeout: float | httpx2.Timeout | None | NotGiven = not_given,
  ) -> DecideArtemisResponse:
    """Approve or reject one pending request, named by its request_id and digest, and wake the
    session. A request takes one decision; the turn it runs reads like any other. Any API
    key of the organization can decide, with no person involved: decide on the request's
    command, config and files, never on its model-written description.

    Args:
      request_id: A pending request's request_id.

      digest: The digest the session showed for it.

      approve: True runs the write; false rejects it.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds
    """
    if isinstance(session_id, str) and not session_id:
      raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
    return self._post(
      path_template(
        "/api/v1/artemis/sessions/{session_id}/decisions",
        session_id=session_id,
      ),
      cast_to=DecideArtemisResponse,
      body=maybe_transform(
        {
          "request_id": request_id,
          "digest": digest,
          "approve": approve,
        },
        ArtemisSessionsDecideParams,
      ),
      options=make_request_options(
        extra_headers=extra_headers,
        extra_query=extra_query,
        extra_body=extra_body,
        timeout=timeout,
      ),
    )


class ArtemisSessionsWithRawResponse:
  def __init__(self, resource: ArtemisSessions) -> None:
    self._resource = resource
    self.send = to_raw_response_wrapper(resource.send)
    self.retrieve = to_raw_response_wrapper(resource.retrieve)
    self.decide = to_raw_response_wrapper(resource.decide)
