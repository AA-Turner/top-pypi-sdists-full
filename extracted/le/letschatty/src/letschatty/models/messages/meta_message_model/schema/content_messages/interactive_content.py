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
    """Interactive payloads from Meta come in many shapes (button_reply, list_reply,
    nfm_reply for WhatsApp Flows, and future types). We don't currently process any
    of them — MessageType.INTERACTIVE is in uncontrolled_messages(), so they get
    routed to process_uncontrolled_message which Slack-notifies and returns 200.

    This model is intentionally lenient (accepts any 'type' shape and extra fields)
    so pydantic parsing never fails on interactive messages. Failing parse here
    used to bubble up as a 4xx and trigger backup-chatty SQS mode.
    """
    model_config = ConfigDict(extra="allow")
    type: Any = None
