# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ArtifactListParams"]


class ArtifactListParams(TypedDict, total=False):
    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    status: Literal["Pending", "Completed", "Failed", "Uploading", "Deleting"]
    """Get artifacts only with the specified status.

    Accepted values are: Pending, Completed, Failed, Uploading, Deleting
    """
