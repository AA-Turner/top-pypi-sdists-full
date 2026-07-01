# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._compat import PYDANTIC_V1, ConfigDict
from ..._models import BaseModel

__all__ = ["ModelServerInfo"]


class ModelServerInfo(BaseModel):
    """Model server information.
    name: The name of the model server.

    Only used for display purposes.
    model_server_id: The ID of the model server.
    model_deployment_id: The ID of the model deployment being used as the backend.
    account_id: The ID of the account that owns the model server.
    alias: An alias for the model server. If configured the model server can be accessed via the alias instead of the model server ID. i.e /models/server/alias/{alias}/execute
    """

    account_id: str

    model_server_id: str

    name: str

    alias: Optional[str] = None

    model_deployment_id: Optional[str] = None

    if not PYDANTIC_V1:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())
