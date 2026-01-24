# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["EmailSendParams", "Attachment"]


class EmailSendParams(TypedDict, total=False):
    from_: Required[Annotated[str, PropertyInfo(alias="from")]]

    html: Required[str]

    subject: Required[str]

    to: Required[Union[str, SequenceNotStr[str]]]

    attachments: Iterable[Attachment]

    bcc: Union[str, SequenceNotStr[str]]

    cc: Union[str, SequenceNotStr[str]]

    from_name: str

    in_reply_to: str

    is_draft: bool

    references: SequenceNotStr[str]

    reply_to: Union[str, SequenceNotStr[str]]

    text: str

    thread_id: Annotated[str, PropertyInfo(alias="threadId")]

    track_clicks: bool

    track_opens: bool


class Attachment(TypedDict, total=False):
    content: Required[str]

    file_name: Required[str]

    cid: str

    content_type: str

    disposition: Literal["attachment", "inline"]
