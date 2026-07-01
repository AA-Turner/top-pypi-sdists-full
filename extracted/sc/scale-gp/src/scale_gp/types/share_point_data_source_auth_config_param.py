# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SharePointDataSourceAuthConfigParam"]


class SharePointDataSourceAuthConfigParam(TypedDict, total=False):
    client_secret: Required[str]
    """Secret for the app registration associated with this SharePoint site"""

    source: Required[Literal["SharePoint"]]

    encrypted: bool
