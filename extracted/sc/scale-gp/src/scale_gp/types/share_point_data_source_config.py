# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SharePointDataSourceConfig"]


class SharePointDataSourceConfig(BaseModel):
    client_id: str
    """Client ID associated with this SharePoint site"""

    site_id: str
    """
    Site ID for this SharePoint site, can be found at
    https://[hostname].sharepoint.com/sites/[site name]/\\__api/site/id
    """

    source: Literal["SharePoint"]

    tenant_id: str
    """Tenant ID that the SharePoint site is within"""

    folder_path: Optional[str] = None
    """Nested folder path to read files from the root of the site.

    Please omit the leading slash. Example: 'Documents/sub_directory'
    """

    recursive: Optional[bool] = None
    """Recurse through the folder contents, default is True."""
