from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, SerializeAsAny

from letschatty.models.company.assets.CINTIA.models.chat_vector import ChatVector
from letschatty.models.company.assets.CINTIA.models.cintia_trigger import CintiaTrigger, IncomingMessageTrigger
from letschatty.models.company.assets.CINTIA.models.outputs.cintia_decision_output import DecisionOutput
from letschatty.models.utils.types.identifier import StrObjectId


class CintiaEventType(StrEnum):
    CREATE_CINTIAS_FOR_INCOMING_MESSAGE = "cintia.create_cintias_for_incoming_message"
    DEQUEUE_CINTIA = "cintia.dequeue_cintia"
    START_PGP_IMPLEMENTATION = "cintia.start_pgp_implementation"
    HANDLE_DECISION_OUTPUT = "cintia.handle_decision_output"
    HANDLE_CINTIA_FEEDBACK = "cintia.handle_cintia_feedback"
    ITERATE_CINTIA_OUTPUT = "cintia.iterate_cintia_output"


# ── Event body / data models ──────────────────────────────────────────────────

class CreateCintiasForIncomingMessageData(BaseModel):
    """Body for CREATE_CINTIAS_FOR_INCOMING_MESSAGE → cintia-creator."""
    chat_id: StrObjectId
    company_id: StrObjectId
    trigger: IncomingMessageTrigger


class DequeueCintiaData(BaseModel):
    """Body for DEQUEUE_CINTIA → pgp-orchestrator."""
    cintia_id: StrObjectId

class StartPgpImplementationData(BaseModel):
    """Body for START_PGP_IMPLEMENTATION → pgp-implementator."""
    cintia_id: StrObjectId
    chat_id: StrObjectId
    pgp_id: StrObjectId
    trigger: CintiaTrigger
    chat_vector: ChatVector
    trigger_embedding: list[float] | None = None

class HandleDecisionOutputData(BaseModel):
    """Body for HANDLE_DECISION_OUTPUT → pgp-implementator (ai-callback)."""
    cintia_id: StrObjectId
    decision_output: DecisionOutput


# ── Typed event envelopes (optional — useful for internal pub/sub) ────────────

class CintiaEvent(BaseModel):
    type: CintiaEventType
    data: dict[str, Any] | SerializeAsAny[BaseModel]
    sync: bool = Field(default=False, description="Whether to wait for the response from the handler or return immediately after receiving the event.")

class CreateCintiasForIncomingMessageEvent(CintiaEvent):
    type: Literal[CintiaEventType.CREATE_CINTIAS_FOR_INCOMING_MESSAGE]
    data: CreateCintiasForIncomingMessageData

class DequeueCintiaEvent(CintiaEvent):
    type: Literal[CintiaEventType.DEQUEUE_CINTIA]
    data: DequeueCintiaData


class StartPgpImplementationEvent(CintiaEvent):
    type: Literal[CintiaEventType.START_PGP_IMPLEMENTATION]
    data: StartPgpImplementationData

class HandleDecisionOutputEvent(CintiaEvent):
    type: Literal[CintiaEventType.HANDLE_DECISION_OUTPUT]
    data: HandleDecisionOutputData