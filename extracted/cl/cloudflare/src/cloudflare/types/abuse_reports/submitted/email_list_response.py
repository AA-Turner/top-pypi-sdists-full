# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ...._models import BaseModel

__all__ = ["EmailListResponse", "Email"]


class Email(BaseModel):
    """An email sent to the customer for an abuse report."""

    id: str
    """Unique identifier of the email."""

    body: str
    """Body content of the email."""

    recipient: str
    """Email address of the recipient."""

    sent_at: str
    """When the email was sent.

    Time in RFC 3339 format (https://www.rfc-editor.org/rfc/rfc3339.html)
    """

    subject: str
    """Subject line of the email."""


class EmailListResponse(BaseModel):
    emails: List[Email]
