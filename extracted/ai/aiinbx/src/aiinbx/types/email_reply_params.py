# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmailReplyParams", "Attachment"]


class EmailReplyParams(TypedDict, total=False):
    from_: Required[Annotated[str, PropertyInfo(alias="from")]]
    """Sender email address (must use a verified domain)"""

    html: Required[str]
    """HTML body of the reply"""

    attachments: Iterable[Attachment]
    """
    Optional list of attachments to include with this reply (e.g., inline images via
    cid).
    """

    bcc: Union[str, SequenceNotStr[str]]
    """Optional BCC recipients"""

    cc: Union[str, SequenceNotStr[str]]
    """Optional CC recipients"""

    from_name: str
    """Optional display name for the sender"""

    is_draft: bool
    """If true, the email is a draft"""

    reply_all: bool
    """If true, includes all original recipients (to/cc) in the reply"""

    subject: str
    """Email subject. If not provided, uses "Re: " + original subject"""

    text: str
    """Optional plain-text body of the reply"""

    to: Union[str, SequenceNotStr[str]]
    """Override recipient addresses.

    If not provided, replies to the original sender and any reply-to addresses.
    """

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
