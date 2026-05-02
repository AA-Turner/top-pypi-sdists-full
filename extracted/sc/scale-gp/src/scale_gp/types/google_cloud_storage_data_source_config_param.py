# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["GoogleCloudStorageDataSourceConfigParam"]


class GoogleCloudStorageDataSourceConfigParam(TypedDict, total=False):
    bucket: Required[str]
    """Name of the Google Cloud Storage bucket where the data is stored."""

    source: Required[Literal["GoogleCloudStorage"]]

    prefix: str
    """Prefix path within the Google Cloud Storage bucket.

    If not specified, the entire bucket will be used.
    """

    project_id: str
    """GCP project ID that owns the Google Cloud Storage bucket.

    If not specified, uses the default project.
    """
