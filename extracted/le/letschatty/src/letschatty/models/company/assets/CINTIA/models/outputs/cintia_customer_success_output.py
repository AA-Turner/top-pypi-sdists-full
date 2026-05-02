"""CintiaCustomerSuccessOutput — decision output for the customer-success PGP.

The CS PGP pairs Claude-generated chat messages with zero or more
``SuggestedAction`` records — Tier C CRUD operations that require a human
reviewer to accept or decline before they are executed on the target workspace.

Spec: docs/superpowers/specs/2026-04-20-customer-success-pgp-design.md §6a
"""
from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, List, Literal, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, model_validator

from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft
from letschatty.models.utils.types.identifier import StrObjectId

from .cintia_decision_output import DecisionOutput, DecisionOutputType


class SuggestedActionStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    FAILED = "failed"  # accept was clicked but the MCP call errored


class SuggestedAction(BaseModel):
    """A single Tier C CRUD operation proposed by the AI, pending human review.

    ``action_id`` is auto-generated (ObjectId hex) so the review endpoint can
    reference individual actions without relying on list position.

    Invariants enforced by the model validator:
    - ``create`` actions must have ``asset_id=None``  (the asset doesn't exist yet).
    - ``update`` / ``delete`` actions must have a non-None ``asset_id``.
    """

    action_id: str = Field(default_factory=lambda: str(ObjectId()))
    action: Literal["create", "update", "delete"]
    asset_type: str  # e.g. "ai_component", "filter_criteria", "workflow"
    asset_id: Optional[StrObjectId] = None  # None for create; required for update/delete
    title: str  # 1-line human-readable summary
    rationale: str  # paragraph explaining why the AI wants this
    mcp_tool: str  # exact MCP tool name: "ai_component_update", "workflow_delete", …
    mcp_params: dict[str, Any]  # the exact arguments the tool call will receive
    status: SuggestedActionStatus = SuggestedActionStatus.PENDING
    reviewer_user_id: Optional[StrObjectId] = None
    reviewed_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    # Populated on accept of a "create" action once the asset is created
    resolved_asset_id: Optional[StrObjectId] = None

    @model_validator(mode="after")
    def _check_asset_id_by_action(self) -> "SuggestedAction":
        if self.action == "create" and self.asset_id is not None:
            raise ValueError("asset_id must be None on action='create'")
        if self.action in ("update", "delete") and self.asset_id is None:
            raise ValueError("asset_id is required on action='update' or 'delete'")
        return self


class CintiaCustomerSuccessOutputData(BaseModel):
    messages: Optional[List[MessageDraft]] = Field(default=[])
    suggested_actions: List[SuggestedAction] = Field(default_factory=list)


class CintiaCustomerSuccessOutput(DecisionOutput):
    type: Literal[DecisionOutputType.CUSTOMER_SUCCESS] = DecisionOutputType.CUSTOMER_SUCCESS
    data: CintiaCustomerSuccessOutputData

    @model_validator(mode="after")
    def set_cintia_id_on_messages(self) -> "CintiaCustomerSuccessOutput":
        if self.data.messages:
            for message in self.data.messages:
                message.context_value.cintia_id = self.cintia_id
        return self
