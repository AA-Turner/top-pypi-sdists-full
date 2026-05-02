"""Base DecisionOutput — every PGP must return a subclass of this.

Each PGP-specific subclass must:
  1. Set a literal `type` field matching its DecisionOutputType.
  2. Add a typed `data` field with the PGP-specific payload.

Examples:
  - CintiaResponderOutput  (data: messages)
  - CintiaSmartFollowOutput (data: next_call_time, messages)
  - CintiaTaggerOutput     (data: tags)
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Optional

from pydantic import BaseModel, Field
from enum import StrEnum
from letschatty.models.utils.types.identifier import StrObjectId


class DecisionOutputAction(StrEnum):
    EXECUTE = "EXECUTE"
    ESCALATE = "ESCALATE"

class DecisionOutputType(StrEnum):
    RESPONDER = "responder"
    SMART_FOLLOW_UP = "smart_follow_up"
    TAGGER = "tagger"
    AUDIO_TRANSCRIBER = "audio_transcriber"
    CUSTOMER_SUCCESS = "customer_success"

class AiOutput(BaseModel):
    action : DecisionOutputAction
    confidence : int = Field(ge=0, le=100, description="The confidence of the decision")
    chain_of_thought : str = Field(description="The chain of thought of the decision")

class DecisionOutput(BaseModel, ABC):
    """Abstract base for all PGP decision outputs.

    Cannot be instantiated directly — every concrete PGP must subclass this
    and define its own typed ``data`` field (or, for fire-and-forget PGPs
    like the audio transcriber, flat top-level fields).

    ``cintia_id`` and ``output`` are optional on the base so that lenient
    subclasses (e.g. audio transcriber) can skip them. Responder / tagger /
    smart-follow-up always populate both.
    """
    type : DecisionOutputType = Field(description="The type of the decision")
    cintia_id: Optional[StrObjectId] = Field(default=None, description="The cintia id of the decision")
    output : Optional[AiOutput] = Field(default=None, description="The output of the decision")
    pgp_id: Optional[StrObjectId] = Field(default=None, description="The pgp id of the decision")
    tokens_input: Optional[int] = Field(default=None, description="The tokens input of the decision")
    tokens_output: Optional[int] = Field(default=None, description="The tokens output of the decision")
    cost_usd: Optional[float] = Field(default=None, description="The cost of the decision in USD")
    ai_model: Optional[str] = Field(default=None, description="The ai model of the decision")

    raw: dict[str, Any] = {}


def _decision_output_union():
    """Lazily build the discriminated union over all concrete DecisionOutput subclasses.

    Defined as a function (not a module-level constant) to avoid import cycles:
    every concrete subclass imports ``DecisionOutput`` from this module. The
    union is materialised on first call and cached.
    """
    global _DECISION_OUTPUT_UNION_CACHE
    if _DECISION_OUTPUT_UNION_CACHE is not None:
        return _DECISION_OUTPUT_UNION_CACHE

    from typing import Annotated, Union

    from pydantic import Discriminator, Tag

    from .cintia_audio_transcriber_output import CintiaAudioTranscriberOutput
    from .cintia_customer_success_output import CintiaCustomerSuccessOutput
    from .cintia_responder_output import CintiaResponderOutput
    from .cintia_smart_follow_output import CintiaSmartFollowOutput
    from .cintia_tagger_output import CintiaTaggerOutput

    def _get_tag(value) -> str:
        """Route a raw dict or model instance to the right concrete subclass.

        Falls back to ``audio_transcriber`` for legacy docs that were written
        without a ``type`` field (the old ``{"status": "skipped"}`` marker).
        Unknown types also land on the audio transcriber branch, which has
        ``extra="allow"`` and therefore round-trips any shape safely.
        """
        if isinstance(value, dict):
            t = value.get("type")
        else:
            t = getattr(value, "type", None)
        if t in (
            DecisionOutputType.RESPONDER,
            DecisionOutputType.TAGGER,
            DecisionOutputType.SMART_FOLLOW_UP,
            DecisionOutputType.AUDIO_TRANSCRIBER,
            DecisionOutputType.CUSTOMER_SUCCESS,
        ):
            return str(t)
        # Back-compat for docs missing or carrying an unknown ``type``.
        return str(DecisionOutputType.AUDIO_TRANSCRIBER)

    _DECISION_OUTPUT_UNION_CACHE = Annotated[
        Union[
            Annotated[CintiaResponderOutput, Tag(str(DecisionOutputType.RESPONDER))],
            Annotated[CintiaTaggerOutput, Tag(str(DecisionOutputType.TAGGER))],
            Annotated[CintiaSmartFollowOutput, Tag(str(DecisionOutputType.SMART_FOLLOW_UP))],
            Annotated[
                CintiaAudioTranscriberOutput,
                Tag(str(DecisionOutputType.AUDIO_TRANSCRIBER)),
            ],
            Annotated[
                CintiaCustomerSuccessOutput,
                Tag(str(DecisionOutputType.CUSTOMER_SUCCESS)),
            ],
        ],
        Discriminator(_get_tag),
    ]
    return _DECISION_OUTPUT_UNION_CACHE


_DECISION_OUTPUT_UNION_CACHE = None
