"""Deprecated client.tools.* aliases for the job execution methods that moved to client.jobs.*.

Scripts written against SDK versions before the jobs group call
client.tools.start_job_execution(), update_job_execution_status(), and
revert_job_execution(). These aliases keep those calls working, forwarding to the
client.jobs methods with a deprecation warning.

TODO(ENG-695): remove this module, and its mixin in client.py, after 2026-09-30.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import Any

# Former client.tools method name -> client.jobs method name.
JOB_EXECUTION_METHODS = {
    "start_job_execution": "start",
    "update_job_execution_status": "close",
    "revert_job_execution": "revert",
}


class LegacyToolsAliases:
    """Mixin that attaches the deprecated job execution aliases to the tools client."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for old_name, new_name in JOB_EXECUTION_METHODS.items():
            setattr(
                self.tools, old_name, _deprecated_alias(self.jobs, old_name, new_name)
            )


def _deprecated_alias(
    jobs_client: Any, old_name: str, new_name: str
) -> Callable[..., Any]:
    def alias(*args: Any, **kwargs: Any) -> Any:
        warnings.warn(
            f"client.tools.{old_name}() is deprecated and will be removed; "
            f"use client.jobs.{new_name}() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(jobs_client, new_name)(*args, **kwargs)

    return alias
