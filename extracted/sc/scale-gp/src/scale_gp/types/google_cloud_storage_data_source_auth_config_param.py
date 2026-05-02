# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["GoogleCloudStorageDataSourceAuthConfigParam"]


class GoogleCloudStorageDataSourceAuthConfigParam(TypedDict, total=False):
    source: Required[Literal["GoogleCloudStorage"]]

    encrypted: bool

    impersonated_service_account_email: str
    """Service account email to impersonate for Google Cloud Storage authentication.

    Similar to AWS AssumeRole. If provided, Scale will impersonate this service
    account using default credentials. If not provided, uses default credentials
    directly.
    """
