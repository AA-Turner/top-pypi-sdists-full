from dlt.common.exceptions import TerminalException

from dlthub.common.exceptions import DltPlusException


class ChangeTrackingVersionExpired(DltPlusException, TerminalException):
    def __init__(self, table_name: str, start_version: int, min_valid_version: int) -> None:
        self.table_name = table_name
        self.start_version = start_version
        self.min_valid_version = min_valid_version
        super().__init__(
            f"Change tracking version `{start_version}` of table `{table_name}` is below its"
            f" minimum valid version `{min_valid_version}`, so SQL Server has already cleaned up"
            " changes that were never loaded. Reset the resource state and load again with"
            " `initial_tracking_version` set to the current change tracking version, after"
            " taking a full snapshot of the table."
        )
