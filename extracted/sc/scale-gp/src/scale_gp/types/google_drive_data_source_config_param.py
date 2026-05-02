# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["GoogleDriveDataSourceConfigParam"]


class GoogleDriveDataSourceConfigParam(TypedDict, total=False):
    drive_id: Required[str]
    """ID associated with the Google Drive to retrieve contents from"""

    source: Required[Literal["GoogleDrive"]]
