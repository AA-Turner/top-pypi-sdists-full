"""LOG API - Auto-generated __init__ file."""

from typing import TYPE_CHECKING

from .disk import Disk
from .fortianalyzer import Fortianalyzer
from .forticloud import Forticloud
from .memory import Memory
from .search import Search

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

    def __init__(self, client: "IHTTPClient"):
        """Initialize LOG category."""
        self.disk = Disk(client)
        self.fortianalyzer = Fortianalyzer(client)
        self.forticloud = Forticloud(client)
        self.memory = Memory(client)
        self.search = Search(client)
