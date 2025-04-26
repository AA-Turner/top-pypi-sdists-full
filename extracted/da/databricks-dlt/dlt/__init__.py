from .api import *
from .helpers import deprecation_warn

# Deprecated but kept here for backward compatibility.
create_target_table = deprecation_warn(
    replacement_func=create_streaming_table, deprecated_func_name="create_target_table"
)
create_streaming_live_table = deprecation_warn(
    replacement_func=create_streaming_table, deprecated_func_name="create_streaming_live_table"
)
create_view = deprecation_warn(replacement_func=view, deprecated_func_name="create_view")
create_table = deprecation_warn(replacement_func=table, deprecated_func_name="create_table")
readStream = read_stream
__all__ = [
    "create_view",
    "create_table",
    "create_streaming_live_table",
    "create_streaming_table",
    "create_target_table",
    "view",
    "table",
    "append_flow",
    "read",
    "read_stream",
    "readStream",
    "expect",
    "expect_or_fail",
    "expect_or_drop",
    "expect_all_or_fail",
    "expect_all_or_drop",
    "expect_all",
    "apply_changes",
    "apply_changes_from_snapshot",
]
