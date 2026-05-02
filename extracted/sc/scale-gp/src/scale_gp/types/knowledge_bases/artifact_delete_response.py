# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["ArtifactDeleteResponse"]


class ArtifactDeleteResponse(BaseModel):
    artifact_id: str
    """The ID of the artifact that was deleted"""

    deleted: bool
    """Whether or not the artifact was successfully deleted"""
