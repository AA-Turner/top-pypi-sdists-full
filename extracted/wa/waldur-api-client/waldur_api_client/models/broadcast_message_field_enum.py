from enum import Enum


class BroadcastMessageFieldEnum(str, Enum):
    AUTHOR_FULL_NAME = "author_full_name"
    BODY = "body"
    CREATED = "created"
    EMAILS = "emails"
    QUERY = "query"
    SEND_AT = "send_at"
    STATE = "state"
    SUBJECT = "subject"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
