# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["ThreadForwardParams", "Attachment"]


class ThreadForwardParams(TypedDict, total=False):
    to: Required[Union[str, SequenceNotStr[str]]]
    """Recipient email address or list of addresses"""

    attachments: Iterable[Attachment]
    """
    Optional additional attachments to include alongside any originals (if
    included).
    """

    bcc: Union[str, SequenceNotStr[str]]
    """Optional BCC recipients"""

    cc: Union[str, SequenceNotStr[str]]
    """Optional CC recipients"""

    from_: Annotated[str, PropertyInfo(alias="from")]
    """Optional sender address; auto-resolved if omitted"""

    from_name: str
    """Optional display name for the sender"""

    include_attachments: Annotated[bool, PropertyInfo(alias="includeAttachments")]
    """
    Include original attachments as real file attachments (inline images embedded
    when referenced by CID)
    """

    is_draft: bool
    """If true, the forward is created as a draft"""

    note: str
    """Optional short context shown above the transcript"""

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
