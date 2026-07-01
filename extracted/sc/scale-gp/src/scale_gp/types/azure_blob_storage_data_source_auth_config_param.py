# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AzureBlobStorageDataSourceAuthConfigParam"]


class AzureBlobStorageDataSourceAuthConfigParam(TypedDict, total=False):
    blob_sas_token: Required[str]
    """Shared Access Signature token for the Azure Blob Storage container"""

    source: Required[Literal["AzureBlobStorage"]]

    encrypted: bool
