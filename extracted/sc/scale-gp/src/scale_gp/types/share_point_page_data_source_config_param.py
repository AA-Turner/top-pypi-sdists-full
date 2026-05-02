# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SharePointPageDataSourceConfigParam"]


class SharePointPageDataSourceConfigParam(TypedDict, total=False):
    client_id: Required[str]
    """Client ID associated with this SharePoint site"""

    site_id: Required[str]
    """Site ID for this SharePoint site"""

    source: Required[Literal["SharePointPage"]]

    tenant_id: Required[str]
    """Tenant ID that the SharePoint site is within"""
