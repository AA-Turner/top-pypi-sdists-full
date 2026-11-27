# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class ArtemisSessionsSendParams(TypedDict, total=False):
  message: Required[str]
  """
  What to ask Artemis, at most 32768 UTF-8 bytes.
  """
  queue: bool
  """
  Keep the message for the next turn instead of letting a running turn take it at its next step.
  """
  session_id: str | None
  """
  A session to continue; omit it to start a new session.
  """
  write_handoff: bool
  """
  Start a session whose writes come back to the caller as each turn's proposals, for it to make
  itself, instead of waiting for an approval here. Set when starting a session; a message to a
  session started otherwise is refused.
  """
