"""FortiOS CMDB - ConfigRevision category (stub)"""

from typing import Any
from ..config_revision_base import ConfigRevision as ConfigRevisionBase
from .delete import Delete
from .file import File
from .info import Info
from .save import Save
from .update_comments import UpdateComments

class ConfigRevision(ConfigRevisionBase):
    """ConfigRevision endpoints wrapper for CMDB API."""

    delete: Delete
    file: File
    info: Info
    save: Save
    update_comments: UpdateComments

    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
