# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SharePointPageDataSourceConfig"]


class SharePointPageDataSourceConfig(BaseModel):
    client_id: str
    """Client ID associated with this SharePoint site"""

    site_id: str
    """Site ID for this SharePoint site"""

    source: Literal["SharePointPage"]

    tenant_id: str
    """Tenant ID that the SharePoint site is within"""
