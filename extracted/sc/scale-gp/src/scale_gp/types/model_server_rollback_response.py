# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ModelServerRollbackResponse"]


class ModelServerRollbackResponse(BaseModel):
    from_deployment: str

    rolled_back_to_deployment: str
