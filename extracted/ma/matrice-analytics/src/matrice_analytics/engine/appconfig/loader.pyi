"""Auto-generated stub for module: loader."""
from typing import Any

# Constants
logger: Any

# Functions
def load_app_config(root: str | Any) -> Any:
    """
    Parse ``metrics.json``, ``widgets.json`` and ``post_processing_config.json`` from a folder.
    """
    ...

# Classes
class AppConfigBundle:
    # The three sibling files as parsed, plus everything wrong with them.
    #
    #     A ``None`` collection means the file was absent or could not be parsed at all — distinct from
    #     an empty tuple, which means the file was a well-formed empty array.

    def all_present(self: Any) -> bool: ...

    def errors(self: Any) -> tuple[Any, ...]: ...

    def metric_keys(self: Any) -> Any[str]: ...

    def none_present(self: Any) -> bool: ...

    def warnings(self: Any) -> tuple[Any, ...]: ...

