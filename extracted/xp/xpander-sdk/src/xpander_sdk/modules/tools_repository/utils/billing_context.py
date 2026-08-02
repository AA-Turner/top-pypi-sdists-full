"""Per-call billing id propagated from the tool hook down to the HTTP layer.

The agno tool hook retries transient failures (timeouts, 5xx) and agno's fixed
function signature cannot carry extra arguments, so the id is minted once per
logical tool call and read via ContextVar inside `Tool.acall_remote_tool`. Every
retry of the same call then reuses the same backend billing idempotency key and
is billed exactly once.
"""

from contextvars import ContextVar
from typing import Optional

current_tool_call_id: ContextVar[Optional[str]] = ContextVar(
    "xpander_current_tool_call_id", default=None
)
