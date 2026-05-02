# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AzureBlobStorageDataSourceConfig"]


class AzureBlobStorageDataSourceConfig(BaseModel):
    container_url: str
    """
    The full URL of the container such as
    'https://your-account-name.blob.core.windows.net/your-container-name'
    """

    source: Literal["AzureBlobStorage"]
