from enum import Enum


class ThreadSessionFieldEnum(str, Enum):
    CHAT_SESSION = "chat_session"
    CREATED = "created"
    FLAGS = "flags"
    HAS_FEEDBACK = "has_feedback"
    INPUT_TOKENS = "input_tokens"
    IS_ARCHIVED = "is_archived"
    IS_FLAGGED = "is_flagged"
    MAX_SEVERITY = "max_severity"
    MESSAGE_COUNT = "message_count"
    MODIFIED = "modified"
    NAME = "name"
    OUTPUT_TOKENS = "output_tokens"
    TITLE_GEN_INPUT_TOKENS = "title_gen_input_tokens"
    TITLE_GEN_OUTPUT_TOKENS = "title_gen_output_tokens"
    TOTAL_TOKENS = "total_tokens"
    USER_FULL_NAME = "user_full_name"
    USER_USERNAME = "user_username"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
