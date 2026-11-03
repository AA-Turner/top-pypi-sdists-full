"""process_groups: end the tools a daemon host started, each its own process group (TERM, then KILL)."""

from probe.foundation.process_groups.process_groups import END_TOOLS_GRACE_S, end_tool_groups, is_group_alive

__all__ = ["END_TOOLS_GRACE_S", "end_tool_groups", "is_group_alive"]
