"""The check a child Session makes before it opens: that the Agents API started it.

A child's start input says where the child belongs in its tree, and anyone allowed to start the
Workflow writes it. The Agents API records every child it starts. The child's worker asks it whether
its own Workflow execution is one of those children, at the place the start input claims, and runs
only on a yes. The answer never carries the recorded values.
"""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

VERIFY_CHILD_SESSION_PROCEDURE = "verify_child_session"


class VerifyChildSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: UUID
    """The child's Workflow id, as its worker reads it from its own execution."""
    root_session_id: UUID
    parent_session_id: UUID
    agent_path: str = Field(min_length=1)


ChildSessionVerdict = Literal["ok", "no_row", "mismatch"]
"""``no_row``: the Agents API started no such Session, as for a Workflow started directly.
``mismatch``: it did, but not as the start input claims, or it has ended.

The call carries the child's execution token, which the Agents API always checks: only the execution
the Agents API started for that Session, as its principal, can ask about it."""


class VerifyChildSessionResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    verdict: ChildSessionVerdict


__all__ = [
    "VERIFY_CHILD_SESSION_PROCEDURE",
    "ChildSessionVerdict",
    "VerifyChildSessionRequest",
    "VerifyChildSessionResult",
]
