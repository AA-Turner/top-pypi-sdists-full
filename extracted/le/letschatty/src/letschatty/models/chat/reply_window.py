"""Can free text be written in a WhatsApp chat now? The 24 h window (api-chatty `docs/canales/envio-y-politica.md`,
REQ-CEN-001, ENG-340): free text only while `free_conversation_expire_date` is strictly after `now`.

One rule, two readers (it lives with the model, not in `domain/`, so that `Chat` can import it without loading
the domain package): `Chat.is_free_conversation_active` (the continuous conversation, the follow-up steps and the
scheduled messages read it) and `ReplyPolicy` of api-chatty. The clock is handed in; this module never reads it.

No date means closed. A date without a zone is read as UTC (Mongo returns them that way). The 7 days after an ad
(`free_template_window_expire_date`) are not read: they price the template, they do not say whether text can be
written."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional


def is_free_window_open(expires: Optional[datetime], now: datetime) -> bool:
    """`now` has a zone. Open only while `expires` is strictly after it: in the instant it ends it is already closed."""
    if expires is None:
        return False
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return expires > now
