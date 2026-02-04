"""FortiOS CMDB - Csf category (stub)"""

from typing import Any
from ..csf_base import Csf as CsfBase
from .pending_authorizations import PendingAuthorizations
from .register_appliance import RegisterAppliance

class Csf(CsfBase):
    """Csf endpoints wrapper for CMDB API."""

    pending_authorizations: PendingAuthorizations
    register_appliance: RegisterAppliance

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
