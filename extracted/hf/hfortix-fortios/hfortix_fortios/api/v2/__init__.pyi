"""Type stubs for FortiOS API v2."""

from .cmdb import CMDB as CMDB
from .monitor import Monitor as Monitor
from .service import Service as Service
from .log import Log as Log

__all__ = [
    "CMDB",
    "Monitor",
    "Service",
    "Log",
]
