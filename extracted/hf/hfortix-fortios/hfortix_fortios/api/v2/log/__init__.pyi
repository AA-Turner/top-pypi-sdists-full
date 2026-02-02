"""Type stubs for LOG category."""

from typing import TYPE_CHECKING

from .disk import Disk as Disk
from .fortianalyzer import Fortianalyzer as Fortianalyzer
from .forticloud import Forticloud as Forticloud
from .memory import Memory as Memory
from .search import Search as Search

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient


class Log:
    """Container for LOG endpoints.
    
    Provides access to log query endpoints for different storage locations:
    - disk: Logs stored on local disk
    - memory: Logs stored in memory
    - fortianalyzer: Logs from FortiAnalyzer
    - forticloud: Logs from FortiCloud
    - search: Log search operations
    """
    disk: Disk
    fortianalyzer: Fortianalyzer
    forticloud: Forticloud
    memory: Memory
    search: Search

    def __init__(self, client: IHTTPClient) -> None: ...