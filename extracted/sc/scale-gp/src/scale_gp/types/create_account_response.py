# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["CreateAccountResponse"]


class CreateAccountResponse(BaseModel):
    account_id: str
    """The ID of the created account."""
