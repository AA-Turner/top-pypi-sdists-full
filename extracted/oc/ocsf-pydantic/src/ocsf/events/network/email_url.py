from enum import Enum

from pydantic import AnyUrl

from ocsf.events.base import BaseEvent


class EmailURLActivityActivityId(Enum):
    Send: int = 1
    Receive: int = 2
    Scan: int = 3 # Email URL being scanned (example: security scanning).

class EmailURLActivity(BaseEvent):
    """
    Email URL Activity events report URLs within an email.
    """

    category_uid: int = 4

    class_uid: int = 4012
    class_name: str = 'Email URL Activity'

    email_uid: str
    url: AnyUrl # The URL included in the email content.

    # Optional:
    activity_id: EmailURLActivityActivityId | None = None
