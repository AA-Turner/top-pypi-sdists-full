from typing import Any, Optional
from pydantic import BaseModel, ConfigDict

# The four WABA-scoped template webhook fields Meta delivers on the whatsapp_business_account object.
# They carry NO messaging_product, so the standard `Value` model cannot parse them — which is exactly why
# they are on the not_implemented blocklist in meta_base_notification_json (a clean 200 drop through the
# factory). This standalone parser is what api-chatty's pre-factory intercept uses to READ them.
TEMPLATE_WEBHOOK_FIELDS = {
    "message_template_status_update",
    "message_template_quality_update",
    "template_category_update",
    "message_template_components_update",
}


class MetaTemplateWebhookJson(BaseModel):
    """Tolerant parser for the 4 template webhook fields. Signal only (C10) — a webhook never writes a
    template field directly; it only tells api-chatty which WABA to re-GET. NOT registered in
    MetaNotificationFactory (S-2): if it were and the factory ever returned it, the receiver's isinstance
    dispatch would fall through to `raise ImpossibleError` -> 500 -> SQS storm. Kept out of the factory
    entirely; api-chatty imports and calls this directly before the factory parse.
    """
    model_config = ConfigDict(extra="allow")
    waba_id: str
    field: str
    message_template_id: Optional[str] = None    # unquoted int in the webhook, numeric str in REST — coerce (border 36)
    message_template_name: Optional[str] = None
    message_template_language: Optional[str] = None

    @classmethod
    def from_meta_json(cls, data: dict[str, Any]) -> "MetaTemplateWebhookJson":
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change.get("value", {}) or {}
        mtid = value.get("message_template_id")
        return cls(
            waba_id=str(entry["id"]),
            field=change["field"],
            message_template_id=str(mtid) if mtid is not None else None,
            message_template_name=value.get("message_template_name"),
            message_template_language=value.get("message_template_language"),
        )

    @staticmethod
    def is_template_webhook(data: dict[str, Any]) -> bool:
        """True if the raw payload's Change field is one of the four template webhooks. Defensive against
        any shape (never raises) so the api-chatty intercept can call it on an arbitrary body."""
        if not isinstance(data, dict):
            return False
        try:
            for entry in data.get("entry", []) or []:
                for change in entry.get("changes", []) or []:
                    if isinstance(change, dict) and change.get("field") in TEMPLATE_WEBHOOK_FIELDS:
                        return True
        except (AttributeError, TypeError):
            pass
        return False
