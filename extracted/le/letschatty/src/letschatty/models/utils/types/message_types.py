from enum import StrEnum

"""https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/components"""

class MessageDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    STICKER = "sticker"
    AUDIO = "audio"
    REACTION="reaction"
    CENTRAL="central"
    CONTACT = "contacts"
    LOCATION = "location"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"
    INTERACTIVE = "interactive"
    SYSTEM = "system"
    ERRORS = "errors"
    BUTTON = "button"

    @staticmethod
    def values():
        return [member.value for member in MessageType]

    @staticmethod
    def special_system_messages():
        return [MessageType.SYSTEM, MessageType.ERRORS, MessageType.UNKNOWN, MessageType.UNSUPPORTED]

    @staticmethod
    def uncontrolled_messages():
        return [MessageType.INTERACTIVE, MessageType.LOCATION]

    @staticmethod
    def controlled_messages():
        return [member.value for member in MessageType if member not in MessageType.special_system_messages() + MessageType.uncontrolled_messages()]

class MessageSubtype(StrEnum):
    TEMPLATE = "template"
    CHATTY_FAST_ANSWER = "chatty_fast_answer"
    CONTINUOUS_CONVERSATION = "continuous_conversation"
    SCHEDULED_MESSAGE = "scheduled_message"
    NONE = ""
    # Central notification subtypes / Highlight subtypes
    FAST_ANSWER_SENT = "fast_answer_sent"
    PRODUCT_ADDED = "product_added"
    PRODUCT_UPDATED = "product_updated"
    PRODUCT_DELETED = "product_deleted"
    SALE_ADDED = "sale_added"
    SALE_UPDATED = "sale_updated"
    SALE_DELETED = "sale_deleted"
    HIGHLIGHT_ADDED = "highlight_added"
    HIGHLIGHT_UPDATED = "highlight_updated"
    HIGHLIGHT_DELETED = "highlight_deleted"
    CONTACT_POINT_ADDED = "contact_point_added"
    CONTACT_POINT_UPDATED = "contact_point_updated"
    CONTACT_POINT_DELETED = "contact_point_deleted"
    CHATTY_AI_AGENT_ADDED = "chatty_ai_agent_added"
    CHATTY_AI_AGENT_DELETED = "chatty_ai_agent_deleted"
    CHATTY_AI_AGENT_UPDATED = "chatty_ai_agent_updated"
    TAG_ADDED = "tag_added"
    TAG_UPDATED = "tag_updated"
    TAG_DELETED = "tag_deleted"
    WORKFLOW_ADDED = "workflow_added"
    WORKFLOW_UPDATED = "workflow_updated"
    WORKFLOW_DELETED = "workflow_deleted"
    CHATTY_AI_AGENT_NOTIFICATION = "chatty_ai_agent_notification"
    SYSTEM = "system"
    META_ERROR = "meta_error"
    CHAT_STARRED = "chat_starred"
    CHAT_UNSTARRED = "chat_unstarred"
    CHAT_ARCHIVED = "chat_archived"
    CHAT_UNARCHIVED = "chat_unarchived"
    CHAT_DESASSIGNED = "chat_desassigned"
    CHAT_ASSIGNED = "chat_assigned"
    CHAT_BLOCKED = "chat_blocked"
    CHAT_UNBLOCKED = "chat_unblocked"
    CHAT_TRANSFERRED = "chat_transferred"
    USER_NOTE = "user_note"
    CLIENT_INFO_UPDATED = "client_info_updated"