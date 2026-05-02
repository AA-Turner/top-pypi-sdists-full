"""
Context persistence for SAGE - Fixes P0 issue 4, P3 issues 61-80.

P0-4: Context loss between turns
P0-17: Lost track of original request
P3-61: Context lost between turns
P3-64: Forgets original request

This module ensures context is preserved across conversation turns.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sage.core.request_classifier import ClassifiedRequest


@dataclass
class OriginalRequest:
    """Immutable record of the user's original request."""

    id: str
    timestamp: float
    raw_text: str
    classification: dict[str, Any]  # Serialized ClassifiedRequest

    # Extracted requirements (never modified)
    quantity_required: int | None = None
    priority_ranking: bool = False
    read_only: bool = False

    @classmethod
    def from_classification(cls, text: str, classification: ClassifiedRequest) -> OriginalRequest:
        """Create from a classified request."""
        return cls(
            id=str(uuid.uuid4())[:8],
            timestamp=time.time(),
            raw_text=text,
            classification={
                "request_type": classification.request_type.name,
                "expected_format": classification.expected_format.name,
                "quantity_required": classification.quantity_required,
                "priority_ranking": classification.priority_ranking,
                "read_only": classification.read_only,
                "min_items": classification.min_items,
            },
            quantity_required=classification.quantity_required,
            priority_ranking=classification.priority_ranking,
            read_only=classification.read_only,
        )


@dataclass
class TaskProgress:
    """Progress tracking for multi-item tasks."""

    total_items: int
    completed_items: int = 0
    failed_items: int = 0
    skipped_items: int = 0
    current_item: int | None = None
    item_statuses: dict[int, str] = field(default_factory=dict)  # item_num -> status

    @property
    def remaining(self) -> int:
        return self.total_items - self.completed_items - self.failed_items - self.skipped_items

    @property
    def progress_percent(self) -> float:
        if self.total_items == 0:
            return 0.0
        return (self.completed_items / self.total_items) * 100

    def mark_completed(self, item_num: int) -> None:
        self.item_statuses[item_num] = "COMPLETED"
        self.completed_items += 1

    def mark_failed(self, item_num: int, reason: str = "") -> None:
        self.item_statuses[item_num] = f"FAILED: {reason}" if reason else "FAILED"
        self.failed_items += 1

    def mark_skipped(self, item_num: int, reason: str = "") -> None:
        self.item_statuses[item_num] = f"SKIPPED: {reason}" if reason else "SKIPPED"
        self.skipped_items += 1


@dataclass
class FileReference:
    """A verified file reference."""

    path: str
    verified_at: float
    exists: bool
    size: int | None = None
    modified_at: float | None = None

    @classmethod
    def verify(cls, path: str, base_dir: Path) -> FileReference:
        """Verify a file exists and create reference."""
        full_path = base_dir / path if not Path(path).is_absolute() else Path(path)
        exists = full_path.exists()

        return cls(
            path=path,
            verified_at=time.time(),
            exists=exists,
            size=full_path.stat().st_size if exists else None,
            modified_at=full_path.stat().st_mtime if exists else None,
        )


@dataclass
class ConversationContext:
    """
    Persistent conversation context that survives across turns.

    Fixes:
    - P0-4: Context loss between turns
    - P0-17: Lost track of original request
    - P3-61 to P3-80: State management issues
    """

    session_id: str
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    # Original request - NEVER modified after creation
    original_request: OriginalRequest | None = None

    # Task progress for multi-item requests
    task_progress: TaskProgress | None = None

    # Verified file references (path -> FileReference)
    verified_files: dict[str, FileReference] = field(default_factory=dict)

    # Files modified during this session
    files_modified: list[str] = field(default_factory=list)

    # Search results cache
    search_results: dict[str, list[str]] = field(default_factory=dict)

    # Accumulated findings/items (for list generation)
    accumulated_items: list[dict[str, Any]] = field(default_factory=list)

    # Accumulated findings from analysis phases (for cross-phase context)
    accumulated_findings: list[str] = field(default_factory=list)

    # Turn counter
    turn_count: int = 0

    # Execution history
    execution_history: list[dict[str, Any]] = field(default_factory=list)

    def set_original_request(self, text: str, classification: ClassifiedRequest) -> None:
        """Set the original request (can only be set once)."""
        if self.original_request is not None:
            raise ValueError("Original request already set - cannot be modified")
        self.original_request = OriginalRequest.from_classification(text, classification)
        self.updated_at = time.time()

    def verify_file(self, path: str, base_dir: Path) -> bool:
        """Verify a file exists and cache the result."""
        ref = FileReference.verify(path, base_dir)
        self.verified_files[path] = ref
        self.updated_at = time.time()
        return ref.exists

    def is_file_verified(self, path: str) -> bool:
        """Check if a file path has been verified to exist."""
        ref = self.verified_files.get(path)
        if ref is None:
            return False
        # Check if verification is still fresh (within 5 minutes)
        if time.time() - ref.verified_at > 300:
            return False
        return ref.exists

    def get_verified_paths(self) -> set[str]:
        """Get set of all verified file paths."""
        return {
            path
            for path, ref in self.verified_files.items()
            if ref.exists and (time.time() - ref.verified_at < 300)
        }

    def record_file_modification(self, path: str) -> None:
        """Record that a file was modified."""
        if path not in self.files_modified:
            self.files_modified.append(path)
        self.updated_at = time.time()

    def cache_search_results(self, query: str, results: list[str]) -> None:
        """Cache search results for a query."""
        self.search_results[query] = results
        self.updated_at = time.time()

    def get_cached_search(self, query: str) -> list[str] | None:
        """Get cached search results."""
        return self.search_results.get(query)

    def add_item(self, item: dict[str, Any]) -> int:
        """Add an accumulated item (for list generation). Returns item number."""
        item_num = len(self.accumulated_items) + 1
        item["_item_num"] = item_num
        item["_added_at"] = time.time()
        self.accumulated_items.append(item)
        self.updated_at = time.time()
        return item_num

    def get_item_count(self) -> int:
        """Get count of accumulated items."""
        return len(self.accumulated_items)

    def record_execution(
        self, action: str, result: str, details: dict[str, Any] | None = None
    ) -> None:
        """Record an execution in history."""
        self.execution_history.append(
            {
                "turn": self.turn_count,
                "timestamp": time.time(),
                "action": action,
                "result": result,
                "details": details or {},
            }
        )
        self.updated_at = time.time()

    def increment_turn(self) -> None:
        """Increment turn counter."""
        self.turn_count += 1
        self.updated_at = time.time()

    def get_context_summary(self) -> str:
        """Get a summary of current context for injection into prompts."""
        parts = []

        if self.original_request:
            parts.append(f"ORIGINAL REQUEST: {self.original_request.raw_text}")
            parts.append(
                f"REQUEST TYPE: {self.original_request.classification.get('request_type', 'UNKNOWN')}"
            )
            if self.original_request.quantity_required:
                parts.append(f"REQUIRED QUANTITY: {self.original_request.quantity_required} items")
            if self.original_request.priority_ranking:
                parts.append("REQUIRES: Priority ranking")
            if self.original_request.read_only:
                parts.append("CONSTRAINT: Read-only (no file modifications)")

        if self.task_progress:
            parts.append(
                f"PROGRESS: {self.task_progress.completed_items}/{self.task_progress.total_items} "
                f"completed ({self.task_progress.progress_percent:.1f}%)"
            )

        if self.accumulated_items:
            parts.append(f"ACCUMULATED ITEMS: {len(self.accumulated_items)}")

        if self.accumulated_findings:
            parts.append(f"ACCUMULATED FINDINGS: {len(self.accumulated_findings)} items recorded")

        if self.files_modified:
            parts.append(f"FILES MODIFIED: {len(self.files_modified)}")

        return "\n".join(parts)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "original_request": asdict(self.original_request) if self.original_request else None,
            "task_progress": asdict(self.task_progress) if self.task_progress else None,
            "verified_files": {k: asdict(v) for k, v in self.verified_files.items()},
            "files_modified": self.files_modified,
            "search_results": self.search_results,
            "accumulated_items": self.accumulated_items,
            "accumulated_findings": self.accumulated_findings,
            "turn_count": self.turn_count,
            "execution_history": self.execution_history,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationContext:
        """Deserialize from dictionary."""
        ctx = cls(
            session_id=data["session_id"],
            created_at=data.get("created_at", time.time()),
            updated_at=data.get("updated_at", time.time()),
            files_modified=data.get("files_modified", []),
            search_results=data.get("search_results", {}),
            accumulated_items=data.get("accumulated_items", []),
            accumulated_findings=data.get("accumulated_findings", []),
            turn_count=data.get("turn_count", 0),
            execution_history=data.get("execution_history", []),
        )

        # Restore original request
        if data.get("original_request"):
            req_data = data["original_request"]
            ctx.original_request = OriginalRequest(
                id=req_data["id"],
                timestamp=req_data["timestamp"],
                raw_text=req_data["raw_text"],
                classification=req_data["classification"],
                quantity_required=req_data.get("quantity_required"),
                priority_ranking=req_data.get("priority_ranking", False),
                read_only=req_data.get("read_only", False),
            )

        # Restore task progress
        if data.get("task_progress"):
            prog_data = data["task_progress"]
            ctx.task_progress = TaskProgress(
                total_items=prog_data["total_items"],
                completed_items=prog_data.get("completed_items", 0),
                failed_items=prog_data.get("failed_items", 0),
                skipped_items=prog_data.get("skipped_items", 0),
                current_item=prog_data.get("current_item"),
                item_statuses=prog_data.get("item_statuses", {}),
            )

        # Restore verified files
        for path, ref_data in data.get("verified_files", {}).items():
            ctx.verified_files[path] = FileReference(
                path=ref_data["path"],
                verified_at=ref_data["verified_at"],
                exists=ref_data["exists"],
                size=ref_data.get("size"),
                modified_at=ref_data.get("modified_at"),
            )

        return ctx


class ContextPersistenceManager:
    """
    Manages persistence of conversation context to disk.

    Fixes:
    - P3-66: State not serialized
    - P3-67: No rollback capability
    - P3-74: State corruption possible
    """

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.context_dir = base_dir / ".sage" / "context"
        self.context_dir.mkdir(parents=True, exist_ok=True)
        self._current_context: ConversationContext | None = None

    def create_context(self) -> ConversationContext:
        """Create a new conversation context."""
        ctx = ConversationContext(session_id=str(uuid.uuid4())[:12])
        self._current_context = ctx
        self._save_context(ctx)
        return ctx

    def load_context(self, session_id: str) -> ConversationContext | None:
        """Load an existing context by session ID."""
        ctx_file = self.context_dir / f"{session_id}.json"
        if not ctx_file.exists():
            return None

        try:
            data = json.loads(ctx_file.read_text(encoding="utf-8", errors="replace"))
            ctx = ConversationContext.from_dict(data)
            self._current_context = ctx
            return ctx
        except Exception as e:
            # Log error but don't crash
            print(f"Warning: Failed to load context {session_id}: {e}")
            return None

    def load_latest_context(self) -> ConversationContext | None:
        """Load the most recently updated context."""
        ctx_files = list(self.context_dir.glob("*.json"))
        if not ctx_files:
            return None

        # Find most recently modified
        latest = max(ctx_files, key=lambda f: f.stat().st_mtime)
        session_id = latest.stem
        return self.load_context(session_id)

    def get_current_context(self) -> ConversationContext | None:
        """Get the current context (create if none exists)."""
        if self._current_context is None:
            self._current_context = self.load_latest_context()
        return self._current_context

    def save_context(self, ctx: ConversationContext | None = None) -> None:
        """Save context to disk."""
        ctx = ctx or self._current_context
        if ctx:
            self._save_context(ctx)

    def _save_context(self, ctx: ConversationContext) -> None:
        """Internal save implementation."""
        ctx_file = self.context_dir / f"{ctx.session_id}.json"

        # Create backup before writing
        if ctx_file.exists():
            backup = self.context_dir / f"{ctx.session_id}.backup.json"
            backup.write_text(ctx_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

        # Write new context
        ctx_file.write_text(json.dumps(ctx.to_dict(), indent=2))

    def create_checkpoint(self, ctx: ConversationContext, description: str = "") -> str:
        """Create a checkpoint of current context state."""
        checkpoint_id = f"cp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_file = (
            self.context_dir / "checkpoints" / f"{ctx.session_id}_{checkpoint_id}.json"
        )
        checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

        data = ctx.to_dict()
        data["_checkpoint_id"] = checkpoint_id
        data["_checkpoint_description"] = description
        checkpoint_file.write_text(json.dumps(data, indent=2))

        return checkpoint_id

    def restore_checkpoint(self, ctx: ConversationContext, checkpoint_id: str) -> bool:
        """Restore context to a checkpoint."""
        checkpoint_file = (
            self.context_dir / "checkpoints" / f"{ctx.session_id}_{checkpoint_id}.json"
        )
        if not checkpoint_file.exists():
            return False

        try:
            data = json.loads(checkpoint_file.read_text(encoding="utf-8", errors="replace"))
            restored = ConversationContext.from_dict(data)
            # Copy restored state to current context
            ctx.verified_files = restored.verified_files
            ctx.files_modified = restored.files_modified
            ctx.search_results = restored.search_results
            ctx.accumulated_items = restored.accumulated_items
            ctx.task_progress = restored.task_progress
            ctx.execution_history = restored.execution_history
            ctx.updated_at = time.time()
            self._save_context(ctx)
            return True
        except Exception:
            return False

    def list_sessions(self, limit: int = 10) -> list[dict[str, Any]]:
        """List recent sessions."""
        ctx_files = sorted(
            self.context_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True
        )[:limit]

        sessions = []
        for f in ctx_files:
            try:
                data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
                sessions.append(
                    {
                        "session_id": data.get("session_id"),
                        "created_at": data.get("created_at"),
                        "updated_at": data.get("updated_at"),
                        "turn_count": data.get("turn_count", 0),
                        "original_request": data.get("original_request", {}).get("raw_text", "")[
                            :100
                        ],
                    }
                )
            except Exception:  # noqa: S112
                continue  # Skip corrupted session files

        return sessions


# Convenience functions


def create_context(base_dir: Path) -> ConversationContext:
    """Create a new conversation context."""
    manager = ContextPersistenceManager(base_dir)
    return manager.create_context()


def load_or_create_context(base_dir: Path) -> ConversationContext:
    """Load existing context or create new one."""
    manager = ContextPersistenceManager(base_dir)
    ctx = manager.load_latest_context()
    if ctx is None:
        ctx = manager.create_context()
    return ctx
