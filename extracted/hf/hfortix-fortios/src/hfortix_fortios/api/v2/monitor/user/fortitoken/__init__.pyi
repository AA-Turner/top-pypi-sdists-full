"""FortiOS CMDB - Fortitoken category (stub)"""

from typing import Any
from ..fortitoken_base import Fortitoken as FortitokenBase
from .activate import Activate
from .import_mobile import ImportMobile
from .import_seed import ImportSeed
from .import_trial import ImportTrial
from .provision import Provision
from .refresh import Refresh
from .send_activation import SendActivation

class Fortitoken(FortitokenBase):
    """Fortitoken endpoints wrapper for CMDB API."""

    activate: Activate
    import_mobile: ImportMobile
    import_seed: ImportSeed
    import_trial: ImportTrial
    provision: Provision
    refresh: Refresh
    send_activation: SendActivation

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
