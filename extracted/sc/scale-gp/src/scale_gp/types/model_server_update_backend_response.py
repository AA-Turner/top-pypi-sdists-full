# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._compat import PYDANTIC_V1, ConfigDict
from .._models import BaseModel

__all__ = ["ModelServerUpdateBackendResponse"]


class ModelServerUpdateBackendResponse(BaseModel):
    """Point the model server to a new model deployment.

    Args:
        old_model_deployment_id(str): The ID of the model deployment to use as the new backend.
    """

    account_id: str

    model_server_id: str

    name: str

    new_model_deployment_id: str

    alias: Optional[str] = None

    model_deployment_id: Optional[str] = None

    old_model_deployment_id: Optional[str] = None

    if not PYDANTIC_V1:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())
