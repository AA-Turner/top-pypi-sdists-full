# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AzureBlobStorageDataSourceConfigParam"]


class AzureBlobStorageDataSourceConfigParam(TypedDict, total=False):
    container_url: Required[str]
    """
    The full URL of the container such as
    'https://your-account-name.blob.core.windows.net/your-container-name'
    """

    source: Required[Literal["AzureBlobStorage"]]
