from enum import Enum


class AttachmentFieldEnum(str, Enum):
    BACKEND_ID = "backend_id"
    CREATED = "created"
    DESTROY_IS_AVAILABLE = "destroy_is_available"
    FILE = "file"
    FILE_NAME = "file_name"
    FILE_SIZE = "file_size"
    ISSUE = "issue"
    ISSUE_KEY = "issue_key"
    MIME_TYPE = "mime_type"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
