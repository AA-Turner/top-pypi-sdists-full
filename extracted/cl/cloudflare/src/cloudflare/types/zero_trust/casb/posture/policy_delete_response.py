# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ....._models import BaseModel

__all__ = ["PolicyDeleteResponse"]


class PolicyDeleteResponse(BaseModel):
    """Response from DeletePolicy operation."""

    id: str
    """ID of the policy deleted."""
