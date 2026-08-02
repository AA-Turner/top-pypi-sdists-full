"""Result type for pre-retry session compaction.

Carried back to the SDK retry loop (``events_module``) and the cloud retry
loop (xpander-mono ``agent_executor``) so both sites can fold the
compaction's token usage into the task's billing metrics.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class CompactRetryResult:
    """Result of a pre-retry session compaction."""

    compacted: bool = False
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    backup_path: Optional[str] = None
