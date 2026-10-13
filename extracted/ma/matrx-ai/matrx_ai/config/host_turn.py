"""THE HOST TURN — the one way code starts or continues a turn the person did not write.

THE USER-INPUT LAW: ``user_input`` carries only what a person typed, dictated or
said. A MACHINE-started turn (a pre-send review, an orchestra hand-off, an inbox
wake, a group-chat cadence, a response-check revision) carries a short
activation line here and its substance as named variables or context entries.

Persisted through :func:`host_authored_user_turn`: ``user_content=[]`` (the
person said nothing) and ``metadata.authored_by='host'`` with
``authored_reason`` — so no reader can ever quote the machine as the person.

ONE type for every door: ``Agent.execute`` / ``run_agent`` (``host_turn=``), the
aidream ``AgentStartRequest`` / continue request, ``run_mandate`` and the
``ai.agent.start`` workflow node. Always mutually exclusive with ``user_input``.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from matrx_ai.config.message_config import UnifiedMessage, host_authored_user_turn


class HostTurn(BaseModel):
    """A user-role turn the HOST writes — never something a person typed."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, description="The activation line the model reads.")
    reason: str = Field(min_length=1, max_length=80, description="Which host feature wrote it.")
    metadata: dict[str, Any] = Field(  # api-any-ok: stamped verbatim onto the stored message
        default_factory=dict,
        description="Extra stamps for the stored message (e.g. revision_key).",
    )

    def to_message(self) -> UnifiedMessage:
        """The stored turn: empty ``user_content``, ``authored_by: host``, plus this turn's stamps."""
        message = host_authored_user_turn(self.text, reason=self.reason)
        message.metadata.update(self.metadata)
        return message


class HostTurnConflict(ValueError):
    """A host turn was sent together with ``user_input`` — a turn has ONE author."""


def refuse_both(user_input: Any, host_turn: Any) -> None:
    """Raise when one turn claims two authors (``user_input`` AND ``host_turn``)."""
    if host_turn is not None and user_input:
        raise HostTurnConflict(
            "host_turn is a turn the host writes; it cannot be sent with user_input "
            "(what a person typed). Put the run's specifics in variables or context."
        )


__all__ = ["HostTurn", "HostTurnConflict", "refuse_both"]
