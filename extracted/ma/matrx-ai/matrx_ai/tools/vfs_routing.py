from __future__ import annotations

from typing import Any

# Map: original (real-disk) function_path → VFS-backed function_path.
# When VFS routing fires, lookups in this table determine the swap target.
VFS_REMAP_TABLE: dict[str, str] = {
    "matrx_ai.tools.implementations.filesystem.fs_read": "matrx_ai.tools.implementations.vfs_filesystem.fs_read",
    "matrx_ai.tools.implementations.filesystem.fs_write": "matrx_ai.tools.implementations.vfs_filesystem.fs_write",
    "matrx_ai.tools.implementations.filesystem.fs_list": "matrx_ai.tools.implementations.vfs_filesystem.fs_list",
    "matrx_ai.tools.implementations.filesystem.fs_search": "matrx_ai.tools.implementations.vfs_filesystem.fs_search",
    "matrx_ai.tools.implementations.filesystem.fs_mkdir": "matrx_ai.tools.implementations.vfs_filesystem.fs_mkdir",
    "matrx_ai.tools.implementations.filesystem.fs_edit": "matrx_ai.tools.implementations.vfs_filesystem.fs_edit",
    "matrx_ai.tools.implementations.shell.shell_execute": "matrx_ai.tools.implementations.vfs_shell.shell_execute",
}

# Sentinel source_kind values for VFS routing.
#
# The schema canonical ``source_kind`` enum is 'native' | 'mcp_discovered' |
# 'admin_authored' | 'agent_authored'. VFS routing is a code-only concern
# (no DB row uses ``matrx_vfs`` as a source_kind), so we keep the in-memory
# marker as a magic string and only ever set it via FS_EDIT_TOOL_DEFINITION
# below. A row whose source_kind is ``native`` and whose function_path lands
# in the VFS remap table is the only other condition that triggers routing.
NATIVE_SOURCE_KIND = "native"
VFS_SOURCE_KIND = "matrx_vfs"

# ── FEATURE TOGGLE (code-reviewed, NOT an env var) ───────────────────────
# Route native filesystem/shell tools through the VFS-backed implementations
# in VFS_REMAP_TABLE. Off by default; flip here and ship via git. (Was
# MATRX_VFS_ENABLED.) Tracked for keep/on-off review in /docs/ENV_FLAG_ERADICATION.md.
VFS_GLOBALLY_ENABLED: bool = False


def is_vfs_globally_enabled() -> bool:
    return VFS_GLOBALLY_ENABLED


def should_route_to_vfs(function_path: str, source_kind: str | None) -> bool:
    if source_kind == VFS_SOURCE_KIND:
        return True
    if source_kind == NATIVE_SOURCE_KIND and is_vfs_globally_enabled():
        return function_path in VFS_REMAP_TABLE
    return False


def remap(function_path: str) -> str:
    return VFS_REMAP_TABLE.get(function_path, function_path)


# Synthetic tool definition for fs_edit. DEPRECATED fallback: fs_edit is now a
# first-class native tool (real-disk impl in implementations/filesystem.py,
# registered in tool_def / bound to matrx-ai-core, migration 0101), so the DB
# row supersedes this injection (registry._maybe_inject_fs_edit skips when the
# row is present). Kept only for the standalone/no-DB case where VFS is on but
# no fs_edit row was loaded.
FS_EDIT_TOOL_DEFINITION: dict[str, Any] = {
    "name": "fs_edit",
    "description": (
        "Edit a file by exact string replacement. Requires an exact match of "
        "old_str that is unique within the file unless replace_all is true."
    ),
    "parameters": {
        "path": {
            "type": "string",
            "description": "File path within the workspace.",
            "required": True,
        },
        "old_str": {
            "type": "string",
            "description": "Exact string to find. Must be unique unless replace_all=true.",
            "required": True,
        },
        "new_str": {
            "type": "string",
            "description": "Replacement string.",
            "required": True,
        },
        "replace_all": {
            "type": "boolean",
            "description": "If true, replace every occurrence of old_str.",
            "default": False,
        },
    },
    "function_path": "matrx_ai.tools.implementations.vfs_filesystem.fs_edit",
    "source_kind": VFS_SOURCE_KIND,
    "is_active": True,
    "version": 1,
    "category": "filesystem",
    "tags": ["edit", "patch", "vfs"],
}
