# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["ThreadForwardParams", "Attachment"]


class ThreadForwardParams(TypedDict, total=False):
    to: Required[Union[str, SequenceNotStr[str]]]

    attachments: Iterable[Attachment]

    bcc: Union[str, SequenceNotStr[str]]

    cc: Union[str, SequenceNotStr[str]]

    from_: Annotated[str, PropertyInfo(alias="from")]

    from_name: str

    include_attachments: Annotated[bool, PropertyInfo(alias="includeAttachments")]

    is_draft: bool

    note: str

    track_clicks: bool

    track_opens: bool


class Attachment(TypedDict, total=False):
    content: Required[str]

    file_name: Required[str]

    cid: str

    content_type: str

    disposition: Literal["attachment", "inline"]
