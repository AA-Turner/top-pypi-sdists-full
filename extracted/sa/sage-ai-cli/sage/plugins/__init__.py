"""SAGE plugin catalogs and migration helpers.

This package vendors external plugin metadata into SAGE-native runtime
structures so orchestration does not depend on external plugin directories.
"""

from sage.plugins.catalog import (
    CLAUDE_PLUGIN_SNAPSHOT_PATH,
    iter_claude_capabilities,
    iter_claude_plugin_groups,
    iter_claude_skills,
    load_claude_plugin_snapshot,
)

__all__ = [
    "CLAUDE_PLUGIN_SNAPSHOT_PATH",
    "iter_claude_capabilities",
    "iter_claude_plugin_groups",
    "iter_claude_skills",
    "load_claude_plugin_snapshot",
]
