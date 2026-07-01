# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ApplicationDeployment"]


class ApplicationDeployment(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    endpoint: str

    is_active: bool

    name: str

    status: Literal["PENDING", "READY", "FAILED", "STOPPED"]
    """
    An enum representing the status of an application deployment. Attributes:
    PENDING: The deployment is pending. READY: The deployment is ready. FAILED: The
    deployment has failed. STOPPED: The deployment has stopped.
    """
