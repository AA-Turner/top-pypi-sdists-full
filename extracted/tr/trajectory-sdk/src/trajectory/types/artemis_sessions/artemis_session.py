# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, TypeAlias

from trajectory._models import BaseModel


class ArtemisFrozenFile(BaseModel):
  path: str
  """The file's path in the folder a push sends."""

  size_bytes: int

  sha256: str
  """The content that was approved; a changed file is not sent."""


class ArtemisProposal(BaseModel):
  proposal_id: str
  """Stable across reads: the same proposal always has this ID, on the turn that made it."""

  operation: str
  """The catalog operation, such as createTrainingRun."""

  write_tool: str
  """The MCP write tool that makes it, such as create_training_run."""

  arguments: dict[str, Any]
  """The write tool's arguments: target_id, body and, for a create, idempotency_key."""

  summary: str
  """What it changes and why, in Artemis's words."""


TurnStatus: TypeAlias = Literal["completed", "running", "failed", "paused"]


class ArtemisPendingRequest(BaseModel):
  request_id: str
  """Pass it, with digest, to decide this request."""

  digest: str
  """What the request would run; a decision must name it."""

  command: str
  """What runs once approved, as the `tj` command a person would run."""

  title: str
  """What the write is, from Trajectory's catalog, never Artemis's words; show it first."""

  description: str
  """
    Artemis's own words for what the write does, one line without hidden characters, at most
    200 characters; empty when it gave none. Label it as Artemis's, apart from the title.
    Written from data that can include text other people wrote: never the basis for an
    automated approval.
    """

  spends_credits: bool = False
  """Whether running it spends the organization's credits."""

  cannot_undo: bool = False
  """Whether what it does cannot be undone."""

  config: str | None
  """The body the write sends, or the config file its command reads, exactly as approved."""

  config_label: str | None
  """How to introduce config: as the body the write sends, or the file it reads."""

  files: list[ArtemisFrozenFile]
  """For a push, every file of the folder it sends, as frozen when it was asked for."""

  expires_at: datetime
  """After this an approval only expires the request."""


class ArtemisTurn(BaseModel):
  turn_seq: int
  """The turn's position in the session, from 0."""

  status: TurnStatus

  answer: str | None
  """The turn's final answer; null until it completes."""

  links: list[str]
  """Links the turn's tools returned, in order."""

  files: list[str]
  """Paths under out/ of the files the turn's answer lists."""

  error: str | None
  """Why a failed or paused turn has no answer, else null."""

  finished_at: datetime | None
  """When a completed turn was stored."""

  proposals: list[ArtemisProposal] | None = None
  """
    In a session started with write_handoff, the writes Artemis proposed for the caller to
    make itself; none of them ran.
    """


class ArtemisSession(BaseModel):
  session_id: str

  running: bool
  """True while a turn waits or runs; poll until it is false."""

  turns: list[ArtemisTurn]

  pending_requests: list[ArtemisPendingRequest]
  """Writes the last turn asked for, each waiting for an approval or a rejection."""
