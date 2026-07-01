# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["EvaluationItemExport"]


class EvaluationItemExport(BaseModel):
    """
    Response model for exporting evaluation items.
    This class represents the response when users export evaluation items.
    It contains either a signed URL to download the exported data from object storage,
    or the actual content bytes when direct download is used (in environments where object storage is not configured).
    """

    filename: str
    """The name of the exported file"""

    content: Optional[str] = None
    """The raw file content as bytes, used when direct download is enabled"""

    signed_url: Optional[str] = None
    """Pre-signed URL to download the file from object storage, if applicable"""
