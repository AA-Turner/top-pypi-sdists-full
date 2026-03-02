from enum import Enum

from ocsf.events.base import BaseEvent

from ocsf.objects.file import File


class EmailFileActivityActivityId(Enum):
    Send: int = 1
    Receive: int = 2
    Scan: int = 3 # Email file being scanned (example: security scanning).

class EmailFileActivity(BaseEvent):
    """
    Email File Activity events report files within emails.
    """

    category_uid: int = 4

    class_uid: int = 4011
    class_name: str = 'Email File Activity'

    email_uid: str
    file: File # The email file attachment.


    # Optional:
    activity_id: EmailFileActivityActivityId | None = None
