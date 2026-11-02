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
    MEDIA_PLACEHOLDER = "media_placeholder"  # WhatsApp Coexistence history backfill: historical media arrives with no content sub-object
    REVOKE = "revoke"  # Meta "message deleted" notification: references revoke.original_message_id, carries no content of its own
    EDIT = "edit"  # Meta "message edited" notification: references edit.original_message_id + carries the NEW content; never instantiated as a ChattyMessage itself
    ORDER = "order"  # Pedido del catálogo de WhatsApp: api-chatty lo guarda como TextMessage con un resumen legible (nunca se guarda con este tipo)

    @staticmethod
    def values():
        return [member.value for member in MessageType]

    @staticmethod
    def special_system_messages():
        # REVOKE and EDIT are special: they are NOT instantiated as ChattyMessages (they
        # act ON an existing message — delete / replace content). Callers intercept them
        # explicitly to mutate the referenced message; listing them here is the safety net
        # that keeps the generic instantiate path from trying to build a content message
        # out of them (which would crash / dead-letter).
        return [MessageType.SYSTEM, MessageType.ERRORS, MessageType.UNKNOWN, MessageType.UNSUPPORTED, MessageType.REVOKE, MessageType.EDIT]

    @staticmethod
    def uncontrolled_messages():
        # Empty since 2026-09: INTERACTIVE (the only member) became a controlled
        # message — nfm_reply (WhatsApp Flow forms), button_reply and list_reply
        # carry REAL customer content (a completed form was silently dropped, ad
        # attribution included). The method stays as the parking lot for future
        # Meta types we map before we support them.
        #
        # ⚠️ Moving a type OUT of here makes it controlled by exclusion (see
        # controlled_messages), which means api-chatty's
        # MetaToChattyMessageFactory.instantiate_message MUST have a case for it —
        # otherwise its `case _` raises → 500 → SQS poison. Ship both together.
        return []

    @staticmethod
    def controlled_messages():
        return [member.value for member in MessageType if member not in MessageType.special_system_messages() + MessageType.uncontrolled_messages()]

class MessageSubtype(StrEnum):
    TEMPLATE = "template"
    CHATTY_FAST_ANSWER = "chatty_fast_answer"
    CONTINUOUS_CONVERSATION = "continuous_conversation"
    SCHEDULED_MESSAGE = "scheduled_message"
    COEXISTENCE_ECHO = "coexistence_echo"
    COEXISTENCE_IMPORT = "coexistence_import"
    # Un mensaje que ocurrió DENTRO de un grupo de WhatsApp (Groups API). Marca el
    # único caso en que un ENTRANTE lleva `sent_by`: el waid del participante que
    # escribió (en un 1:1 el autor es siempre el cliente y no hay nada que guardar).
    # Sobre una letschatty vieja, validate_subtype lo degrada a NONE en vez de romper
    # el chat entero — compat cross-service deliberada.
    GROUP = "group"
    # HEURISTIC subtype — the value literally says "possible" on purpose. Meta does NOT
    # tell us a message is a reply to a WhatsApp Status; we INFER it from the context
    # shape (only `from`, no `id`). It is NOT an exact/guaranteed classification. See
    # MetaContext.is_possible_status_reply().
    POSSIBLE_STATUS_REPLY = "possible_status_reply"
    # A coexistence HISTORY-import message Meta delivered as an `errors` entry (code
    # 131051 "Unsupported message received") — Meta didn't share the original content
    # when migrating the history. Rendered with an explanatory legend, not as "[errors]".
    HISTORY_UNSHARED_CONTENT = "history_unshared_content"
    # Un mensaje EN VIVO cuyo contenido Meta no entrego: llega como `errors` (131051
    # "tipo no soportado" — encuesta, videollamada, edicion; o 131060 "mensaje no
    # disponible", tipico del primer entrante en coexistence). Es el hermano LIVE de
    # HISTORY_UNSHARED_CONTENT y existe separado a proposito: la leyenda del frontend
    # para el historial dice "al migrar el historial", que es FALSO para un mensaje que
    # el cliente acaba de mandar. El texto final (revisar la app de WhatsApp Business vs
    # simplemente "Meta no lo compartio") lo decide el frontend segun si la empresa es
    # coexistence HOY, igual que el resto de las leyendas.
    UNSUPPORTED_CONTENT = "unsupported_content"
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