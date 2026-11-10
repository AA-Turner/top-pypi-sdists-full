# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Dict

from .._models import BaseModel

__all__ = ["SessionUpdateMetadataResponse"]


class SessionUpdateMetadataResponse(BaseModel):
    metadata: Dict[str, str]
    """Customer-defined flat metadata.

    Values are always strings: numbers and booleans sent on write come back in their
    string form.
    """
