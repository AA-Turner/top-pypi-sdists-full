"""Data operation constants (matching real SDK with API best practices)."""

# Pagination limits
DEFAULT_PAGE_SIZE = 10000  # Standard page size for reads
CELL_PAGINATION_LIMIT = 9000  # Max cells per write request
DELETION_PAGINATION_LIMIT = 10000  # Max records per delete batch (default, can go up to 10000)

# Parallel worker counts
DATA_READ_WORKER_COUNT = 8  # Workers for parallel data reads
VIEW_READ_WORKER_COUNT = 2  # Workers for view reads (more conservative)
DELETE_WORKER_COUNT = 8  # Workers for parallel deletes

# Pagination strategy
MAX_SPECULATIVE_PAGES = 10  # Initial pages to fetch in parallel
# Per API docs: Continue until empty rows array returned
# Do NOT rely on totalRecords for pagination


