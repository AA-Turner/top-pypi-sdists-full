# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SharePointDataSourceConfigParam"]


class SharePointDataSourceConfigParam(TypedDict, total=False):
    client_id: Required[str]
    """Client ID associated with this SharePoint site"""

    site_id: Required[str]
    """
    Site ID for this SharePoint site, can be found at
    https://[hostname].sharepoint.com/sites/[site name]/\\__api/site/id
    """

    source: Required[Literal["SharePoint"]]

    tenant_id: Required[str]
    """Tenant ID that the SharePoint site is within"""

    folder_path: str
    """Nested folder path to read files from the root of the site.

    Please omit the leading slash. Example: 'Documents/sub_directory'
    """

    recursive: bool
    """Recurse through the folder contents, default is True."""
