"""FortiOS CMDB - ConfigScript category (stub)"""

from typing import Any
from ..config_script_base import ConfigScript as ConfigScriptBase
from .delete import Delete
from .run import Run
from .upload import Upload

class ConfigScript(ConfigScriptBase):
    """ConfigScript endpoints wrapper for CMDB API."""

    delete: Delete
    run: Run
    upload: Upload

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
