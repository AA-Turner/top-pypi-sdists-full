"""Deprecated client.tools.* aliases for methods that moved to entity groups.

Scripts written against SDK versions before the jobs and files groups call
client.tools.start_job_execution(), upload_file(), and the other names below.
These aliases keep those calls working, forwarding to the new group's method
with a deprecation warning.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any

# Entity group -> {former client.tools method name: method name in that group}.
LEGACY_TOOLS_METHODS = {
    "jobs": {
        "start_job_execution": "start",
        "update_job_execution_status": "close",
        "revert_job_execution": "revert",
    },
    "files": {
        "upload_file": "upload",
        "list_files": "list",
        "get_file_content": "get_content",
    },
}


class LegacyToolsAliases:
    """Mixin that attaches the deprecated aliases to the tools client."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for group_name, methods in LEGACY_TOOLS_METHODS.items():
            group_client = getattr(self, group_name)
            for old_name, new_name in methods.items():
                setattr(
                    self.tools,
                    old_name,
                    _deprecated_alias(group_client, group_name, old_name, new_name),
                )


def _deprecated_alias(
    group_client: Any, group_name: str, old_name: str, new_name: str
) -> Callable[..., Any]:
    def alias(*args: Any, **kwargs: Any) -> Any:
        warnings.warn(
            f"client.tools.{old_name}() is deprecated and will be removed; "
            f"use client.{group_name}.{new_name}() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(group_client, new_name)(*args, **kwargs)

    return alias
