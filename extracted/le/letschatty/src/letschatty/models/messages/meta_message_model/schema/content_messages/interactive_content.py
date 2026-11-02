from typing import Any
from pydantic import BaseModel, ConfigDict

class MetaButtonReply(BaseModel):
    id: str
    title: str

class MetaListReply(BaseModel):
    id: str
    title: str
    description: str

class MetaInteractiveType(BaseModel):
    button_reply: MetaButtonReply
    list_reply: MetaListReply

class MetaInteractiveContent(BaseModel):
    """Interactive payloads from Meta: `nfm_reply` (WhatsApp Flows / formularios),
    `button_reply`, `list_reply` — plus whatever type Meta ships next.

    Since 2026-09 these ARE processed: MessageType.INTERACTIVE left
    uncontrolled_messages(), so the receiver instantiates a real InteractiveMessage
    whose content is built by ChattyContentInteractive.from_meta (which does all the
    interpretation: parsing nfm_reply.response_json, cleaning screen_N_Label_M keys,
    building the readable body).

    This model stays intentionally lenient — every declared field is `Any` and extra
    fields are allowed — so pydantic parsing NEVER fails on an interactive message,
    no matter how malformed or novel. Failing parse here rejects the WHOLE webhook
    envelope (422) and the customer's message is lost; a deterministic failure would
    poison backup-chatty's SQS queue. Interpretation (and its tolerance) lives in
    ChattyContentInteractive.from_meta, never in validation."""
    model_config = ConfigDict(extra="allow")
    type: Any = None
    # Declared as Any (not typed sub-models) on purpose: a malformed sub-shape must
    # degrade at interpretation time, never fail at parse time.
    nfm_reply: Any = None
    button_reply: Any = None
    list_reply: Any = None

    def get_interactive_type(self) -> str:
        """The raw interactive type ("nfm_reply" | "button_reply" | "list_reply" |
        whatever Meta ships next), inferred from the present sub-object when `type`
        is absent. Never raises."""
        if self.type:
            return str(self.type)
        for candidate in ("nfm_reply", "button_reply", "list_reply"):
            if isinstance(getattr(self, candidate, None), dict):
                return candidate
        return "unknown"
