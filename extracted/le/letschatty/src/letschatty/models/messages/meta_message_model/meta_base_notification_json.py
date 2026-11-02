from pydantic import BaseModel, Field, model_validator
from typing import List, Any, Dict, Optional
from enum import StrEnum
from .schema.values.value_messages import Message, HistoryEntry, StateSyncEntry
from .schema.values.value_statuses import StatusNotification
from .schema.values.value_errors import Error

class NotificationType(StrEnum):
    MESSAGES = "messages"
    STATUSES = "statuses"
    ERRORS = "errors"
    SMB_MESSAGE_ECHOES = "smb_message_echoes"
    HISTORY = "history"
    SMB_APP_STATE_SYNC = "smb_app_state_sync"
    GROUP_LIFECYCLE_UPDATE = "group_lifecycle_update"
    GROUP_PARTICIPANTS_UPDATE = "group_participants_update"
    GROUP_SETTINGS_UPDATE = "group_settings_update"
    GROUP_STATUS_UPDATE = "group_status_update"
    UNKNOWN = "unknown"
    
class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class Profile(BaseModel):
    # `name` is OPTIONAL on purpose: a user who adopted a WhatsApp username may have NO
    # display name, and Meta then sends `profile: {"username": ...}` with no `name`.
    # Keeping this required made pydantic reject the WHOLE webhook (422 → message dropped).
    name: Optional[str] = None
    # Meta nests the WhatsApp username here (observed in prod: `profile.username`).
    # DISPLAY-ONLY, mutable, never a key.
    username: Optional[str] = None

class Contact(BaseModel):
    profile: Optional[Profile] = Field(default=None)
    wa_id: Optional[str] = None
    user_id: Optional[str] = None          # BSUID (e.g. "CR.xxx") — present since Meta's March 2026 BSUID rollout
    parent_user_id: Optional[str] = None   # parent BSUID (CC.ENT.x), multi-portfolio; present only for enrolled parent accounts
    username: Optional[str] = None         # WhatsApp username — some payloads carry it here (contact-level) too; DISPLAY-ONLY, never a key

    def get_name(self) -> str:
        # Display label. A username-only profile has no `name`, so fall back to the
        # username (still captured separately by get_username): name → username → "".
        # Never returns None → safe for consumers that expect a str (Client.name).
        if self.profile is not None and self.profile.name:
            return self.profile.name
        return self.get_username() or ""

    def get_wa_id(self) -> Optional[str]:
        return self.wa_id

    def get_user_id(self) -> Optional[str]:
        return self.user_id

    def get_parent_user_id(self) -> Optional[str]:
        return self.parent_user_id

    def get_username(self) -> Optional[str]:
        # The username can arrive at the contact level OR nested inside `profile`. The
        # first real adopter (2026) sent it as `profile.username`, so check both.
        if self.username:
            return self.username
        if self.profile is not None and self.profile.username:
            return self.profile.username
        return None

class Value(BaseModel):
    messaging_product: str
    metadata: Metadata = Field(default=None)
    contacts: List[Contact] = Field(default_factory= lambda: [])
    messages: List[Message] = Field(default_factory= lambda: [])
    statuses: List[StatusNotification] = Field(default_factory= lambda: [])
    errors: List[Error] = Field(default_factory= lambda: [])
    message_echoes: List[Message] = Field(default_factory= lambda: [], description="WhatsApp Coexistence: messages the business owner sent from the WhatsApp Business App, mirrored to us via the smb_message_echoes webhook field")
    history: List[HistoryEntry] = Field(default_factory= lambda: [], description="WhatsApp Coexistence: chunked backfill of the business owner's prior WhatsApp Business App conversations, delivered via the history webhook field")
    state_sync: List[StateSyncEntry] = Field(default_factory= lambda: [], description="WhatsApp Coexistence: the owner's WhatsApp Business App contacts/state, delivered via the smb_app_state_sync webhook field")

    def is_messages(self) -> bool:
        return bool(self.messages != [])

    def is_statuses(self) -> bool:
        return bool(self.statuses != [])

    def is_errors(self) -> bool:
        return bool(self.errors != [])

    def is_smb_message_echoes(self) -> bool:
        return bool(self.message_echoes != [])

    def is_history(self) -> bool:
        return bool(self.history != [])

    def is_state_sync(self) -> bool:
        return bool(self.state_sync != [])

class Change(BaseModel):
    value: Value
    field: str

    @model_validator(mode='before')
    @classmethod
    def not_implemented_field(cls, data: Dict) -> Dict:
        # Handle case where data is None
        if not isinstance(data, dict):
            return data
        
        # Be explicit about which fields are not implemented.
        # These are WhatsApp Business Account administrative webhooks (not message
        # webhooks). We deliberately swallow them with NotImplementedError →
        # meta_receiver.py catches and returns 200 to backup-chatty (no SQS storm).
        not_implemented_fields = {
            'message_template_quality_update',
            'message_template_status_update',
            # ADDED (border 37): these two used to fall through to a ValidationError -> 422 + a per-webhook
            # Slack alert that misleadingly said "malformed payload". They carry no messaging_product just
            # like the two above, so blocklisting them converts that into the same clean NotImplementedError
            # -> 200 drop. The api-chatty pre-factory intercept (which reads them via MetaTemplateWebhookJson)
            # runs BEFORE this, so real handling is unaffected; this is only the factory-fallback hygiene.
            'template_category_update',
            'message_template_components_update',
            'account_update',
            'phone_number_name_update',
        }
        
        if data.get('field') in not_implemented_fields:
            raise NotImplementedError(f"Field '{data.get('field')}' is not implemented")
        return data

class Entry(BaseModel):
    id: str = Field(description="WABA id")
    changes: List[Change]

class BaseMetaNotificationJson(BaseModel):
    object: str
    entry: List[Entry]

    def get_notification_type(self) -> NotificationType:

        try:
            change = self.entry[0].changes[0]
            value = change.value

            # WhatsApp Coexistence: the Change-level `field` is Meta's AUTHORITATIVE
            # discriminator for the dedicated coexistence webhooks. Their historical /
            # contact messages can arrive FLAT under `value.messages` (with an empty
            # `value.history` / `value.state_sync`), so inferring the type from which
            # value array is populated would misclassify them as MESSAGES -> MetaMessageJson,
            # which then crashes in get_client() -> contacts[0] (IndexError -> HTTP 500 ->
            # SQS retry storm). Trust the field for these. `messages` / `statuses` /
            # `errors` all share field="messages", so those are still distinguished by
            # array presence below.
            if change.field == NotificationType.HISTORY.value:
                return NotificationType.HISTORY
            if change.field == NotificationType.SMB_APP_STATE_SYNC.value:
                return NotificationType.SMB_APP_STATE_SYNC

            if value.is_messages():
                return NotificationType.MESSAGES
            elif value.is_statuses():
                return NotificationType.STATUSES
            elif value.is_errors():
                return NotificationType.ERRORS
            elif value.is_smb_message_echoes():
                return NotificationType.SMB_MESSAGE_ECHOES
            elif value.is_history():
                return NotificationType.HISTORY
            elif value.is_state_sync():
                return NotificationType.SMB_APP_STATE_SYNC
            else:
                return NotificationType.UNKNOWN

        except (ValueError, IndexError):
            return NotificationType.UNKNOWN
        
    
    def get_value(self) -> Value:
        return self.entry[0].changes[0].value
    
    def get_metadata(self) -> Metadata:
        return self.get_value().metadata
    
    def get_phone_number_id(self) -> str:
        return self.get_metadata().phone_number_id
