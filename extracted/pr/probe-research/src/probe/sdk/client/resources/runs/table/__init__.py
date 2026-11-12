"""`client.runs.table(...)`: every listed run as one table row (`RunTable`, `.to_pandas()`)."""

from probe.sdk.client.resources.runs.table.table import RUN_COLUMNS, RunTable

__all__ = ["RUN_COLUMNS", "RunTable"]
