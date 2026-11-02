from __future__ import annotations
from typing import List, TYPE_CHECKING

from .meta_base_notification_json import BaseMetaNotificationJson

if TYPE_CHECKING:
    from .schema.values.value_messages import StateSyncContact


class MetaStateSyncJson(BaseMetaNotificationJson):
    """WhatsApp Coexistence — `smb_app_state_sync` webhook.

    When a coexistence number connects, Meta syncs the owner's WhatsApp Business
    App state. The `value.state_sync[]` list carries heterogeneous entries
    (contacts, chat state, etc.); only `type == "contact"` entries hold a
    `contact` card. ``get_contacts()`` returns just the contact cards that carry
    a usable `phone_number`, so the import path can seed customer profiles
    without choking on non-contact state entries.
    """

    def get_display_phone_number(self) -> str:
        """The coexistence business number whose state this sync belongs to."""
        return self.get_metadata().display_phone_number

    def get_contacts(self) -> List[StateSyncContact]:
        """Return every synced contact card that has a phone number.

        Non-contact entries (``type != "contact"``) and contact entries missing a
        ``phone_number`` are skipped — a contact with no number is not addressable."""
        contacts: List[StateSyncContact] = []
        for entry in self.get_value().state_sync:
            if entry.type != "contact":
                continue
            if entry.contact is None or not entry.contact.phone_number:
                continue
            contacts.append(entry.contact)
        return contacts
