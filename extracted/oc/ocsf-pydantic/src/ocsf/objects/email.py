
from pydantic.networks import IPvAnyAddress
from .data_classification import DataClassification
from pydantic import EmailStr


class Email(DataClassification):
    """
    The Email object describes the email metadata such as sender, recipients, and
    direction
    """

    from_: EmailStr
    to: list[EmailStr]

    # Recommended:
    message_uid: str | None = None
    reply_to: EmailStr | None = None
    size: int | None = None # The size in bytes of the email, including attachments.
    smtp_from: EmailStr | None = None
    smtp_to: list[EmailStr] | None = None
    subject: str | None = None # The email header Subject value, as defined by RFC 5322.
    uid: str | None = None # The email unique identifier.

    # Optional:
    cc: list[EmailStr] | None = None
    delivered_to: EmailStr | None = None
    raw_header: str | None = None
    x_originating_ip: list[IPvAnyAddress] | None = None
