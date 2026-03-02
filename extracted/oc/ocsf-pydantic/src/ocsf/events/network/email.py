from enum import Enum

from ocsf.events.base import BaseEvent

from ocsf.objects.email import Email
from ocsf.objects.email_auth import EmailAuthentication
from ocsf.objects.network_endpoint import NetworkEndpoint


class EmailActivityActivityId(Enum):
    Send: int = 1
    Receive: int = 2
    Scan: int = 3 # Email being scanned (example: security scanning)


class EmailActivityDirectionId(Enum):
    """
    The direction of the email relative to the scanning host or
    organization. Email scanned at an internet gateway might be characterized as
    inbound to the organization from the Internet, outbound from the organization to
    the Internet, or internal within the organization. Email scanned at a
    workstation might be characterized as inbound to, or outbound from the
    workstation.
    """
    Unknown: int = 0
    Inbound: int = 1
    Outbound: int = 2
    Internal: int = 3
    Other: int = 99


class EmailActivity(BaseEvent):
    """
    Email events report activities of emails.
    """

    category_uid: int = 4

    class_uid: int = 4009
    class_name: str = 'Email Activity'

    direction_id: EmailActivityDirectionId # The direction of the email relative to
                                           # the scanning host or organization. Email
                                           # scanned at an internet gateway might be
                                           # characterized as inbound to the organization
                                           # from the Internet, outbound from the
                                           # organization to the Internet, or internal
                                           # within the organization. Email scanned at a
                                           # workstation might be characterized as
                                           # inbound to, or outbound from the
                                           # workstation.
    email: Email

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # The responder (server) receiving the email.
    email_auth: EmailAuthentication | None = None
    src_endpoint: NetworkEndpoint | None = None # The initiator (client) sending the email.
    smtp_hello: str | None = None # The value of the SMTP HELO or EHLO command sent by the initiator
                                  # (client).

    # Optional:
    activity_id: EmailActivityActivityId | None = None
    attempt: int | None = None # The attempt number for attempting to deliver the email.
    banner: str | None = None
    direction: str | None = None # The direction of the email, as defined by the
                                 # `direction_id` value.
