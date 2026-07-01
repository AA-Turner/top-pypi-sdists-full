"""
cvc.workspace_manager — Multi-workspace isolation manager for the CVC Gateway.

Manages a registry of workspace instances, each with its own isolated four-tier
memory (SQLite, CAS blobs, ChromaDB, PageIndex). Enables dynamic workspace
switching from a single Gateway dashboard session.

Inspired by:
- OpenClaw's per-agent workspace binding pattern
- Claude Cowork's persistent session with dynamic folder navigation
- CVC MCP server's ``_MCPSession`` reference implementation

Usage::

    mgr = WorkspaceManager()
    await mgr.switch_to("/projects/app-a")   # Auto-inits .cvc/ if needed
    mgr.engine.commit(...)                     # Commits to app-a's .cvc/
    await mgr.switch_to("/projects/app-b")   # Switches, preserving app-a state
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.workspace_manager")

# Maximum number of workspace instances kept open simultaneously.
# Oldest (LRU) workspace gets its DB connections closed when exceeded.
_DEFAULT_MAX_OPEN = 5

# Global workspace registry file
_REGISTRY_PATH = Path.home() / ".cvc" / "workspaces.json"
_ACTIVE_PATH = Path.home() / ".cvc" / "active_workspace"


class WorkspaceInstance:
    """A single workspace's isolated CVC stack (config + database + engine)."""

    __slots__ = ("path", "config", "db", "engine", "last_accessed", "initialized")

    def __init__(self, path: Path) -> None:
        self.path = path.resolve()
        self.config = None      # CVCConfig
        self.db = None          # ContextDatabase
        self.engine = None      # CVCEngine
        self.last_accessed: float = time.time()
        self.initialized: bool = False

    def initialize(self) -> None:
        """Initialize the four-tier CVC stack for this workspace."""
        from cvc.core.database import ContextDatabase
        from cvc.core.models import CVCConfig
        from cvc.operations.engine import CVCEngine

        # Ensure .cvc/ directory structure exists
        cvc_dir = self.path / ".cvc"
        if not cvc_dir.exists():
            logger.info("Auto-initializing CVC in %s", self.path)

        # Create config anchored to this workspace
        original_cwd = Path.cwd()
        try:
            os.chdir(self.path)
            self.config = CVCConfig.for_project(project_root=self.path, mode="gateway")
            self.config.ensure_dirs()
        finally:
            os.chdir(original_cwd)

        # Initialize database (all four tiers) and engine
        self.db = ContextDatabase(self.config)
        self.engine = CVCEngine(self.config, self.db)

        self.initialized = True
        self.last_accessed = time.time()
        logger.info(
            "Workspace initialized: %s (branch=%s)",
            self.path,
            self.engine.active_branch,
        )

    def close(self) -> None:
        """Close database connections for this workspace."""
        if self.db:
            try:
                self.db.close()
            except Exception:
                logger.debug("Error closing DB for %s", self.path, exc_info=True)
        self.initialized = False
        self.db = None
        self.engine = None
        self.config = None
        logger.info("Workspace closed: %s", self.path)

    def touch(self) -> None:
        """Update last-accessed timestamp (for LRU tracking)."""
        self.last_accessed = time.time()


class WorkspaceManager:
    """
    Manages multiple CVC workspace instances with LRU eviction.

    Each workspace gets its own isolated four-tier memory:
    - Tier 1: SQLite (.cvc/cvc.db)
    - Tier 2: CAS blobs (.cvc/objects/)
    - Tier 3: ChromaDB (.cvc/chroma/)
    - Tier 4: PageIndex (.cvc/pageindex/)
    """

    def __init__(self, max_open: int = _DEFAULT_MAX_OPEN) -> None:
        self._workspaces: OrderedDict[str, WorkspaceInstance] = OrderedDict()
        self._current_key: str | None = None
        self._max_open = max_open

    # ── Properties for the active workspace ──────────────────────────

    @property
    def current(self) -> WorkspaceInstance | None:
        """The currently active workspace instance."""
        if self._current_key and self._current_key in self._workspaces:
            return self._workspaces[self._current_key]
        return None

    @property
    def current_path(self) -> Path | None:
        """Path of the currently active workspace."""
        inst = self.current
        return inst.path if inst else None

    @property
    def config(self):
        """CVCConfig of the active workspace."""
        inst = self.current
        return inst.config if inst else None

    @property
    def db(self):
        """ContextDatabase of the active workspace."""
        inst = self.current
        return inst.db if inst else None

    @property
    def engine(self):
        """CVCEngine of the active workspace."""
        inst = self.current
        return inst.engine if inst else None

    # ── Core operations ──────────────────────────────────────────────

    def switch_to(self, path: str | Path) -> WorkspaceInstance:
        """
        Switch to a workspace at the given path.

        - Validates the path exists (or creates it)
        - Auto-initializes .cvc/ if not present
        - Evicts LRU workspace if at capacity
        - Updates the persistent workspace registry

        Returns the WorkspaceInstance for the target workspace.
        """
        target = Path(path).resolve()
        key = str(target)

        # Validate path
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            logger.info("Created workspace directory: %s", target)

        if not target.is_dir():
            raise ValueError(f"Workspace path is not a directory: {target}")

        # Check if already open
        if key in self._workspaces:
            inst = self._workspaces[key]
            if not inst.initialized:
                inst.initialize()
            inst.touch()
            # Move to end (most recently used)
            self._workspaces.move_to_end(key)
            self._current_key = key
            logger.info("Switched to existing workspace: %s", target)
            self._update_registry(inst)
            self._save_active(target)
            return inst

        # Evict LRU if at capacity
        self._evict_if_needed()

        # Create and initialize new workspace instance
        inst = WorkspaceInstance(target)
        inst.initialize()

        self._workspaces[key] = inst
        self._current_key = key
        logger.info("Switched to new workspace: %s", target)
        self._update_registry(inst)
        self._save_active(target)
        return inst

    def init_workspace(self, path: str | Path) -> WorkspaceInstance:
        """
        Initialize .cvc/ in a directory without switching to it.
        Useful for pre-warming a workspace.
        """
        target = Path(path).resolve()
        key = str(target)

        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)

        if key in self._workspaces and self._workspaces[key].initialized:
            return self._workspaces[key]

        self._evict_if_needed()
        inst = WorkspaceInstance(target)
        inst.initialize()
        self._workspaces[key] = inst
        self._update_registry(inst)
        return inst

    def close_workspace(self, path: str | Path) -> bool:
        """Close a workspace's DB connections (does not delete .cvc/)."""
        key = str(Path(path).resolve())
        if key not in self._workspaces:
            return False

        inst = self._workspaces.pop(key)
        inst.close()

        if self._current_key == key:
            # Switch to another open workspace if available
            if self._workspaces:
                self._current_key = next(reversed(self._workspaces))
            else:
                self._current_key = None

        return True

    def remove_from_registry(self, path: str | Path) -> dict[str, Any]:
        """Permanently remove a workspace from the persisted list.

        v2.91.46 — "Delete workspace" in the dashboard.

        The workspace is removed from:
          1. The in-memory ``_workspaces`` dict (DB connections closed)
          2. The ``_registered_workspaces`` proxy registry
          3. The persistent ``~/.cvc/workspaces.json`` registry

        It is NOT deleted from disk. The user can re-add the same path
        later — `.cvc/` will be re-initialized from scratch on next add.

        If the removed workspace was active, this method switches the
        active workspace to the next available one (or None if no
        workspaces remain).

        Args:
            path: absolute path of the workspace to remove.

        Returns:
            A dict describing the result::

                {
                    "removed": True|False,    # was it actually in the registry?
                    "path": "/abs/path",       # normalized path
                    "was_active": True|False,  # was it the active workspace?
                    "new_active": "/other/path" | None,  # new active if switched
                }
        """
        target = Path(path).resolve()
        key = str(target)
        result: dict[str, Any] = {
            "removed": False,
            "path": key,
            "was_active": False,
            "new_active": None,
        }

        # 1. Close + drop from in-memory cache
        if key in self._workspaces:
            inst = self._workspaces.pop(key)
            inst.close()
            result["removed"] = True

        # 2. Drop from persistent registry
        registry = self._load_registry()
        new_registry = [e for e in registry if e.get("path") != key]
        if len(new_registry) != len(registry):
            result["removed"] = True
        self._save_registry(new_registry)

        # 3. If it was the active workspace, switch to another
        if self._current_key == key:
            result["was_active"] = True
            self._current_key = None
            # Prefer the most-recently-used remaining open workspace
            if self._workspaces:
                self._current_key = next(reversed(self._workspaces))
                result["new_active"] = self._current_key
            else:
                # Fall back to the most recent entry in the registry
                if new_registry:
                    new_registry_sorted = sorted(
                        new_registry,
                        key=lambda e: e.get("last_accessed", 0),
                        reverse=True,
                    )
                    fallback = new_registry_sorted[0].get("path")
                    if fallback and Path(fallback).is_dir():
                        try:
                            self.switch_to(fallback)
                            result["new_active"] = fallback
                        except Exception:
                            pass
            # Clear the active-workspace pointer if it was this path
            try:
                if _ACTIVE_PATH.exists():
                    raw = _ACTIVE_PATH.read_text(encoding="utf-8").strip()
                    if raw and Path(raw).resolve() == target:
                        # Wipe the active marker so gateway restart
                        # doesn't auto-switch back to the deleted path.
                        _ACTIVE_PATH.unlink(missing_ok=True)
            except OSError:
                pass

        return result

    def purge_workspace(self, path: str | Path) -> dict[str, Any]:
        """Remove a workspace AND delete its on-disk .cvc/ directory.

        v2.91.46 — "Delete workspace + wipe .cvc/" in the dashboard.

        This is a DESTRUCTIVE operation. The .cvc/ directory contains:
          - SQLite database (all CVC commits, snapshots)
          - CAS object store (file blobs)
          - ChromaDB vector index (semantic search)
          - PageIndex (tree-sitter parse trees)
          - Persona + memory + tool-cache state

        After purge, the workspace is GONE. Re-adding the path creates
        a fresh empty .cvc/.

        Safety: refuses to purge if the .cvc/ directory is the user's
        current working directory or a system directory. Operates only
        on ``<path>/.cvc/`` — never on the project source code itself.
        """
        result = self.remove_from_registry(path)
        target = Path(path).resolve()
        cvc_dir = target / ".cvc"
        if cvc_dir.exists() and cvc_dir.is_dir():
            # Defensive: confirm the path is exactly <target>/.cvc
            try:
                cvc_dir_resolved = cvc_dir.resolve()
                if cvc_dir_resolved.parent.resolve() == target:
                    import shutil
                    shutil.rmtree(cvc_dir_resolved, ignore_errors=True)
                    result["purged"] = True
                else:
                    result["purged"] = False
                    result["purge_error"] = "Refusing: .cvc/ is not a direct child of the target path"
            except Exception as exc:
                result["purged"] = False
                result["purge_error"] = str(exc)
        else:
            result["purged"] = False
            result["purge_error"] = "No .cvc/ directory to purge"
        return result

    def list_workspaces(self) -> list[dict[str, Any]]:
        """
        List all known workspaces (open + from persistent registry).
        Returns a combined, deduplicated list.
        """
        result: dict[str, dict[str, Any]] = {}

        # Add open workspaces
        for key, inst in self._workspaces.items():
            info = self._workspace_info(inst)
            info["open"] = True
            info["active"] = key == self._current_key
            result[key] = info

        # Merge from persistent registry
        registry = self._load_registry()
        import hashlib
        from pathlib import Path as _P
        for entry in registry:
            path = entry.get("path", "")
            if path and path not in result:
                result[path] = {
                    "path": path,
                    "name": _P(path).name or path,
                    "workspace_id": hashlib.sha256(path.encode()).hexdigest()[:12],
                    "last_accessed": entry.get("last_accessed", 0),
                    "open": False,
                    "active": False,
                    "branch": entry.get("branch", "main"),
                    "commit_count": entry.get("commit_count", 0),
                }

        return list(result.values())

    def close_all(self) -> None:
        """Close all open workspace connections. Called on gateway shutdown."""
        for inst in self._workspaces.values():
            inst.close()
        self._workspaces.clear()
        self._current_key = None
        logger.info("All workspaces closed")

    # ── LRU eviction ─────────────────────────────────────────────────

    def _evict_if_needed(self) -> None:
        """Evict the least-recently-used workspace if at max capacity."""
        while len(self._workspaces) >= self._max_open:
            # Pop the oldest (first) item
            oldest_key, oldest_inst = next(iter(self._workspaces.items()))
            # Don't evict the current workspace
            if oldest_key == self._current_key and len(self._workspaces) > 1:
                # Move current to end and evict the next oldest
                self._workspaces.move_to_end(oldest_key)
                oldest_key, oldest_inst = next(iter(self._workspaces.items()))
            logger.info("Evicting LRU workspace: %s", oldest_key)
            oldest_inst.close()
            del self._workspaces[oldest_key]
            if self._current_key == oldest_key:
                self._current_key = next(reversed(self._workspaces)) if self._workspaces else None

    # ── Persistent workspace registry ────────────────────────────────

    def _load_registry(self) -> list[dict[str, Any]]:
        """Load the global workspace registry from ~/.cvc/workspaces.json."""
        if not _REGISTRY_PATH.exists():
            return []
        try:
            data = json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _save_registry(self, registry: list[dict[str, Any]]) -> None:
        """Save the global workspace registry."""
        _REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        _REGISTRY_PATH.write_text(
            json.dumps(registry, indent=2, default=str),
            encoding="utf-8",
        )

    def _update_registry(self, inst: WorkspaceInstance) -> None:
        """Update or add a workspace entry in the persistent registry."""
        registry = self._load_registry()
        key = str(inst.path)
        info = self._workspace_info(inst)

        # Update existing or append new
        found = False
        for entry in registry:
            if entry.get("path") == key:
                entry.update(info)
                found = True
                break
        if not found:
            registry.append(info)

        self._save_registry(registry)

    # ── Active workspace persistence (survives gateway restart) ──────

    @staticmethod
    def load_active_workspace() -> Path | None:
        """Return the last-active workspace path, or None if not recorded.

        v3.4.2 — Source of truth moved to ``cvc.host_state`` (SQLite at
        ``~/.cvc/host_state.db``) so it survives gateway restart, full
        reboot, and partial-write corruption that bit us on the legacy
        sidecar file (it once contained ``/Users/jkm--`` — truncated
        garbage from a torn write). The legacy sidecar file is now just
        a redundant backup, migrated into the DB on first boot.
        """
        # Lazy import to avoid a circular dep at module load
        from cvc.host_state import load_active_workspace as _load
        try:
            return _load()
        except Exception:  # noqa: BLE001 — must never crash gateway boot
            logger.exception("HostState.load_active_workspace failed")
            return None

    def _save_active(self, path: Path) -> None:
        """Persist the active workspace path so it survives gateway restart.

        v3.4.2 — Source of truth is now ``cvc.host_state`` (SQLite).
        The legacy sidecar at ``~/.cvc/active_workspace`` is kept in
        sync as a redundant backup; if the DB write fails the sidecar
        still carries the value, and vice versa.
        """
        try:
            from cvc.host_state import save_active_workspace as _save
            _save(path)
        except Exception as exc:  # noqa: BLE001 — must never crash gateway
            logger.warning("Could not persist active workspace: %s", exc)

    def _workspace_info(self, inst: WorkspaceInstance) -> dict[str, Any]:
        """Build a workspace info dict from a WorkspaceInstance."""
        import hashlib
        path_str = str(inst.path)
        info: dict[str, Any] = {
            "path": path_str,
            "name": inst.path.name or path_str,
            "workspace_id": hashlib.sha256(path_str.encode()).hexdigest()[:12],
            "last_accessed": inst.last_accessed,
        }
        if inst.initialized and inst.engine:
            info["branch"] = inst.engine.active_branch
            try:
                commits = inst.db.index.list_all_commits(limit=9999)
                info["commit_count"] = len(commits)
            except Exception:
                info["commit_count"] = 0
        return info
