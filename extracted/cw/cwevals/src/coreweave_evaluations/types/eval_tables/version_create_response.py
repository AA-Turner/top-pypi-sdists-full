# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["VersionCreateResponse"]


class VersionCreateResponse(BaseModel):
    dataset_version_id: str

    evaluation_version_id: str
