"""CintiaAssistantOutput — decision output for the assistant PGP.

The assistant PGP runs on the owner's control chat and has two roles:
- "ask"      : frame the question to the owner over WhatsApp (the ticket).
- "interpret": read the owner's reply and pick one of the interpret_action
               values to route back to the customer chat (compose a reply,
               send verbatim, approve a draft, chat action, defer, clarify).

Spec (cintia-lambdas repo): docs/superpowers/specs/2026-06-01-assistant-pgp-design.md
"""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import ConfigDict, Field, BaseModel

from .cintia_decision_output import DecisionOutput, DecisionOutputType


class CintiaAssistantData(BaseModel):
    model_config = ConfigDict(extra="allow")  # roles carry disjoint fields

    role: Literal["ask", "interpret"] = "ask"
    interpret_action: Optional[
        Literal[
            "COMPOSE_REPLY",
            "SEND_VERBATIM",
            "APPROVE",
            "EDIT_DRAFT",
            "CHAT_ACTION",
            "DEFER",
            "CLARIFY",
        ]
    ] = None
    messages: list[dict[str, Any]] = Field(default_factory=list)


class CintiaAssistantOutput(DecisionOutput):
    type: Literal[DecisionOutputType.ASSISTANT] = DecisionOutputType.ASSISTANT
    data: CintiaAssistantData
