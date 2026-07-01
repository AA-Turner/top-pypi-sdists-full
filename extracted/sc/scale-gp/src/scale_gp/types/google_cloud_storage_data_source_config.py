# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["GoogleCloudStorageDataSourceConfig"]


class GoogleCloudStorageDataSourceConfig(BaseModel):
    bucket: str
    """Name of the Google Cloud Storage bucket where the data is stored."""

    source: Literal["GoogleCloudStorage"]

    prefix: Optional[str] = None
    """Prefix path within the Google Cloud Storage bucket.

    If not specified, the entire bucket will be used.
    """

    project_id: Optional[str] = None
    """GCP project ID that owns the Google Cloud Storage bucket.

    If not specified, uses the default project.
    """
