# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["ArtifactBatchDeleteResponse"]


class ArtifactBatchDeleteResponse(BaseModel):
    artifact_ids: List[str]
    """List of artifact ids that were deleted"""
