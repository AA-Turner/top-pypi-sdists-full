# Temporal has a 2MB payload limit. We use 1.9MB to leave headroom for metadata and headers.
MAX_INPUT_SIZE_BYTES = int(1.9 * 1024 * 1024)

INTERNAL_METADATA_PREFIX = "__internal_"
# Temporal header carrying the API caller's call context (see get_call_context). The prefix keeps it
# out of the history API.
CALL_CONTEXT_HEADER = f"{INTERNAL_METADATA_PREFIX}call_context"

PARALLEL_EXECUTION_WORKFLOW_NAME = "__parallel_execution__"
OBO_PARALLEL_EXECUTION_WORKFLOW_NAME = "__parallel_execution_obo__"
