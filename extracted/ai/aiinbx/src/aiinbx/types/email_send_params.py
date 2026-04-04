# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmailSendParams", "Attachment"]


class EmailSendParams(TypedDict, total=False):
    from_: Required[Annotated[str, PropertyInfo(alias="from")]]
    """Sender email address (must use a verified domain)"""

    html: Required[str]
    """HTML body of the email"""

    subject: Required[str]
    """Email subject"""

    to: Required[Union[str, SequenceNotStr[str]]]
    """Recipient email address or list of addresses"""

    attachments: Iterable[Attachment]
    """Optional list of attachments. Supports base64 or data URL; use cid for inline."""

    bcc: Union[str, SequenceNotStr[str]]
    """Optional BCC recipients"""

    cc: Union[str, SequenceNotStr[str]]
    """Optional CC recipients"""

    from_name: str
    """Optional display name for the sender"""

    in_reply_to: str
    """Optional Message-ID of the email being replied to"""

    is_draft: bool
    """If true, the email is a draft"""

    references: SequenceNotStr[str]
    """Optional list of Message-ID references"""

    reply_to: Union[str, SequenceNotStr[str]]
    """Optional Reply-To addresses"""

    text: str
    """Optional plain-text body of the email"""

    thread_id: Annotated[str, PropertyInfo(alias="threadId")]
    """Optional existing thread ID to attach this email to"""

    track_clicks: bool
    """Enable click tracking for this email. Overrides API key and org defaults."""

    track_opens: bool
    """Enable open tracking for this email. Overrides API key and org defaults."""


class Attachment(TypedDict, total=False):
    """Attachment input; provide content as base64 or data URL"""

    content: Required[str]
    """Required: base64 string or data URL for the file content"""

    file_name: Required[str]
    """Original file name to display"""

    cid: str
    """Content-ID for inline images referenced via cid:"""

    content_type: str
    """MIME type when using raw base64 (ignored for data URLs)"""

    disposition: Literal["attachment", "inline"]
    """How the attachment should be presented"""
