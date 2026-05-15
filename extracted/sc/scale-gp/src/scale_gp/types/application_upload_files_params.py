# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ApplicationUploadFilesParams"]


class ApplicationUploadFilesParams(TypedDict, total=False):
    files: Required[SequenceNotStr[str]]
    """Upload files to be used in an application."""

    account_id: str
    """Account which the file will be tied to.

    Use this account id query param if you are using the API or the SDK.
    """
