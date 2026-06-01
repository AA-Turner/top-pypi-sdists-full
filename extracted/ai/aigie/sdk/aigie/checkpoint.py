"""
Checkpoint API - State Management for Agent Rollback.

This module provides checkpoint creation and restoration capabilities
for AI agent state management. Checkpoints enable rollback to previous
known-good states during remediation.

Key Features:
- create_checkpoint(): Snapshot agent state
- restore_checkpoint(): Rollback to previous state
- Automatic checkpoint on remediation attempts
- Checkpoint status reporting to backend

Integration with Backend:
The backend has a full checkpoint manager with state snapshots
and rollback. This SDK module provides the client-side API.

Usage:
    from aigie import CheckpointManager, Checkpoint

    # Initialize checkpoint manager
    manager = CheckpointManager(api_url=api_url, api_key=api_key)

    # Create a checkpoint before risky operations
    checkpoint = await manager.create(
        trace_id="trace_123",
        state={"messages": [...], "context": {...}},
        metadata={"reason": "before_tool_call"}
    )

    # If something goes wrong, restore
    state = await manager.restore(checkpoint.checkpoint_id)
"""

import asyncio
import contextlib
import hashlib
import json
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger("aigie.checkpoint")


class CheckpointStatus(str, Enum):
    """Status of a checkpoint."""

    PENDING = "pending"  # Being created
    ACTIVE = "active"  # Available for restore
    RESTORED = "restored"  # Has been restored
    EXPIRED = "expired"  # Past retention period
    DELETED = "deleted"  # Manually deleted


class CheckpointType(str, Enum):
    """Type of checkpoint."""

    MANUAL = "manual"  # Created manually by user
    AUTO_REMEDIATION = "auto_remediation"  # Created before remediation
    AUTO_PERIODIC = "auto_periodic"  # Created periodically
    PRE_TOOL_CALL = "pre_tool_call"  # Created before tool call
    POST_CYCLE = "post_cycle"  # Created after execution cycle


@dataclass
class Checkpoint:
    """Represents a state checkpoint."""

    checkpoint_id: str
    trace_id: str
    span_id: str | None = None
    checkpoint_type: CheckpointType = CheckpointType.MANUAL
    status: CheckpointStatus = CheckpointStatus.PENDING

    # State data
    state: dict[str, Any] = field(default_factory=dict)
    state_hash: str = ""

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    expires_at: datetime | None = None
    restored_at: datetime | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    reason: str | None = None

    # Lineage
    parent_checkpoint_id: str | None = None
    child_checkpoint_ids: list[str] = field(default_factory=list)

    # Metrics
    state_size_bytes: int = 0
    restore_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert checkpoint to dictionary."""
        return {
            "checkpoint_id": self.checkpoint_id,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "checkpoint_type": self.checkpoint_type.value,
            "status": self.status.value,
            "state": self.state,
            "state_hash": self.state_hash,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "restored_at": self.restored_at.isoformat() if self.restored_at else None,
            "metadata": self.metadata,
            "tags": self.tags,
            "reason": self.reason,
            "parent_checkpoint_id": self.parent_checkpoint_id,
            "child_checkpoint_ids": self.child_checkpoint_ids,
            "state_size_bytes": self.state_size_bytes,
            "restore_count": self.restore_count,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Checkpoint":
        """Create checkpoint from dictionary."""

        def parse_datetime(val):
            if not val:
                return None
            if isinstance(val, datetime):
                return val
            try:
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                return None

        return cls(
            checkpoint_id=data.get("checkpoint_id", ""),
            trace_id=data.get("trace_id", ""),
            span_id=data.get("span_id"),
            checkpoint_type=CheckpointType(data.get("checkpoint_type", "manual")),
            status=CheckpointStatus(data.get("status", "pending")),
            state=data.get("state", {}),
            state_hash=data.get("state_hash", ""),
            created_at=parse_datetime(data.get("created_at")) or datetime.utcnow(),
            updated_at=parse_datetime(data.get("updated_at")),
            expires_at=parse_datetime(data.get("expires_at")),
            restored_at=parse_datetime(data.get("restored_at")),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            reason=data.get("reason"),
            parent_checkpoint_id=data.get("parent_checkpoint_id"),
            child_checkpoint_ids=data.get("child_checkpoint_ids", []),
            state_size_bytes=data.get("state_size_bytes", 0),
            restore_count=data.get("restore_count", 0),
        )


@dataclass
class CheckpointConfig:
    """Configuration for checkpoint manager."""

    # Retention
    default_retention_hours: int = 24
    max_checkpoints_per_trace: int = 50

    # Auto-checkpoint settings
    auto_checkpoint_on_remediation: bool = True
    auto_checkpoint_on_tool_call: bool = False
    auto_checkpoint_interval_seconds: int | None = None

    # Size limits
    max_state_size_bytes: int = 10 * 1024 * 1024  # 10MB

    # Backend sync
    sync_to_backend: bool = True
    backend_sync_interval_seconds: float = 5.0

    # Callbacks
    on_checkpoint_created: Callable[["Checkpoint"], Awaitable[None]] | None = None
    on_checkpoint_restored: Callable[["Checkpoint", dict[str, Any]], Awaitable[None]] | None = None


@dataclass
class CheckpointMetrics:
    """Metrics for checkpoint operations."""

    checkpoints_created: int = 0
    checkpoints_restored: int = 0
    checkpoints_expired: int = 0
    checkpoints_deleted: int = 0
    restore_failures: int = 0
    total_state_bytes: int = 0
    avg_state_size_bytes: float = 0.0
    backend_syncs: int = 0
    backend_sync_failures: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "checkpoints_created": self.checkpoints_created,
            "checkpoints_restored": self.checkpoints_restored,
            "checkpoints_expired": self.checkpoints_expired,
            "checkpoints_deleted": self.checkpoints_deleted,
            "restore_failures": self.restore_failures,
            "total_state_bytes": self.total_state_bytes,
            "avg_state_size_bytes": self.avg_state_size_bytes,
            "backend_syncs": self.backend_syncs,
            "backend_sync_failures": self.backend_sync_failures,
        }


class CheckpointManager:
    """
    Manage agent state checkpoints for rollback.

    Provides checkpoint creation, storage, and restoration capabilities.
    Integrates with the backend for persistent storage and cross-session
    checkpoint management.

    Features:
    - Create snapshots of agent state
    - Restore to previous checkpoints
    - Automatic checkpoint on remediation
    - Backend synchronization
    - Checkpoint expiration and cleanup
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
        config: CheckpointConfig | None = None,
        http_client: Any | None = None,
    ):
        """
        Initialize the checkpoint manager.

        Args:
            api_url: Backend API URL for checkpoint storage
            api_key: API key for authentication
            config: Checkpoint configuration
            http_client: Optional HTTP client for backend communication
        """
        self._api_url = api_url
        self._api_key = api_key
        self._config = config or CheckpointConfig()
        self._http_client = http_client

        # Local checkpoint storage
        self._checkpoints: dict[str, Checkpoint] = {}
        self._checkpoints_by_trace: dict[str, list[str]] = {}

        # Metrics
        self._metrics = CheckpointMetrics()

        # Background tasks
        self._cleanup_task: asyncio.Task | None = None
        self._sync_task: asyncio.Task | None = None

        # Counters
        self._checkpoint_counter = 0

    async def create(
        self,
        trace_id: str,
        state: dict[str, Any],
        *,
        span_id: str | None = None,
        checkpoint_type: CheckpointType = CheckpointType.MANUAL,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        reason: str | None = None,
        parent_checkpoint_id: str | None = None,
        retention_hours: int | None = None,
    ) -> Checkpoint:
        """
        Create a checkpoint to snapshot agent state.

        Args:
            trace_id: ID of the trace this checkpoint belongs to
            state: Agent state to snapshot (messages, context, etc.)
            span_id: Optional span ID for finer-grained tracking
            checkpoint_type: Type of checkpoint being created
            metadata: Additional metadata to store
            tags: Tags for categorization
            reason: Reason for creating the checkpoint
            parent_checkpoint_id: ID of parent checkpoint (for lineage)
            retention_hours: Hours to retain checkpoint

        Returns:
            Created Checkpoint object
        """
        # Generate checkpoint ID
        self._checkpoint_counter += 1
        checkpoint_id = f"chk_{trace_id[:8]}_{self._checkpoint_counter}_{int(time.time() * 1000)}"

        # Serialize and hash state
        state_json = json.dumps(state, sort_keys=True, default=str)
        state_hash = hashlib.sha256(state_json.encode()).hexdigest()
        state_size = len(state_json.encode())

        # Check size limit
        if state_size > self._config.max_state_size_bytes:
            raise ValueError(
                f"State size ({state_size} bytes) exceeds limit "
                f"({self._config.max_state_size_bytes} bytes)"
            )

        # Calculate expiration
        retention = retention_hours or self._config.default_retention_hours
        expires_at = datetime.utcnow() + timedelta(hours=retention)

        # Create checkpoint
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            trace_id=trace_id,
            span_id=span_id,
            checkpoint_type=checkpoint_type,
            status=CheckpointStatus.ACTIVE,
            state=state,
            state_hash=state_hash,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            metadata=metadata or {},
            tags=tags or [],
            reason=reason,
            parent_checkpoint_id=parent_checkpoint_id,
            state_size_bytes=state_size,
        )

        # Store locally
        self._checkpoints[checkpoint_id] = checkpoint

        # Track by trace
        if trace_id not in self._checkpoints_by_trace:
            self._checkpoints_by_trace[trace_id] = []
        self._checkpoints_by_trace[trace_id].append(checkpoint_id)

        # Enforce max checkpoints per trace
        await self._enforce_max_checkpoints(trace_id)

        # Update parent's children
        if parent_checkpoint_id and parent_checkpoint_id in self._checkpoints:
            self._checkpoints[parent_checkpoint_id].child_checkpoint_ids.append(checkpoint_id)

        # Update metrics
        self._metrics.checkpoints_created += 1
        self._metrics.total_state_bytes += state_size
        if self._metrics.checkpoints_created > 0:
            self._metrics.avg_state_size_bytes = (
                self._metrics.total_state_bytes / self._metrics.checkpoints_created
            )

        # Sync to backend
        if self._config.sync_to_backend and self._api_url:
            await self._sync_checkpoint_to_backend(checkpoint)

        # Callback
        if self._config.on_checkpoint_created:
            try:
                await self._config.on_checkpoint_created(checkpoint)
            except Exception as e:
                logger.warning(f"Checkpoint created callback error: {e}")

        logger.debug(f"Created checkpoint {checkpoint_id} for trace {trace_id}")
        return checkpoint

    async def restore(
        self,
        checkpoint_id: str,
    ) -> dict[str, Any]:
        """
        Restore agent state from a checkpoint.

        Args:
            checkpoint_id: ID of the checkpoint to restore

        Returns:
            The state dictionary from the checkpoint

        Raises:
            KeyError: If checkpoint not found
            ValueError: If checkpoint is not active
        """
        # Try local first
        checkpoint = self._checkpoints.get(checkpoint_id)

        # Try backend if not found locally
        if not checkpoint and self._api_url:
            checkpoint = await self._fetch_checkpoint_from_backend(checkpoint_id)

        if not checkpoint:
            raise KeyError(f"Checkpoint {checkpoint_id} not found")

        if checkpoint.status != CheckpointStatus.ACTIVE:
            raise ValueError(
                f"Checkpoint {checkpoint_id} is not active (status: {checkpoint.status.value})"
            )

        # Update checkpoint status
        checkpoint.status = CheckpointStatus.RESTORED
        checkpoint.restored_at = datetime.utcnow()
        checkpoint.restore_count += 1
        checkpoint.updated_at = datetime.utcnow()

        # Update metrics
        self._metrics.checkpoints_restored += 1

        # Sync to backend
        if self._config.sync_to_backend and self._api_url:
            await self._sync_checkpoint_to_backend(checkpoint)

        # Callback
        if self._config.on_checkpoint_restored:
            try:
                await self._config.on_checkpoint_restored(checkpoint, checkpoint.state)
            except Exception as e:
                logger.warning(f"Checkpoint restored callback error: {e}")

        logger.info(f"Restored checkpoint {checkpoint_id}")
        return checkpoint.state

    async def list_checkpoints(
        self,
        trace_id: str,
        *,
        status: CheckpointStatus | None = None,
        checkpoint_type: CheckpointType | None = None,
        include_expired: bool = False,
    ) -> list[Checkpoint]:
        """
        List checkpoints for a trace.

        Args:
            trace_id: ID of the trace
            status: Filter by status
            checkpoint_type: Filter by type
            include_expired: Whether to include expired checkpoints

        Returns:
            List of Checkpoint objects
        """
        checkpoint_ids = self._checkpoints_by_trace.get(trace_id, [])
        checkpoints = []

        for checkpoint_id in checkpoint_ids:
            checkpoint = self._checkpoints.get(checkpoint_id)
            if not checkpoint:
                continue

            # Filter by status
            if status and checkpoint.status != status:
                continue

            # Filter by type
            if checkpoint_type and checkpoint.checkpoint_type != checkpoint_type:
                continue

            # Filter expired
            if not include_expired:
                if checkpoint.status == CheckpointStatus.EXPIRED:
                    continue
                if checkpoint.expires_at and checkpoint.expires_at < datetime.utcnow():
                    continue

            checkpoints.append(checkpoint)

        # Sort by creation time (newest first)
        checkpoints.sort(key=lambda c: c.created_at, reverse=True)
        return checkpoints

    async def get_checkpoint(self, checkpoint_id: str) -> Checkpoint | None:
        """Get a checkpoint by ID."""
        checkpoint = self._checkpoints.get(checkpoint_id)
        if not checkpoint and self._api_url:
            checkpoint = await self._fetch_checkpoint_from_backend(checkpoint_id)
        return checkpoint

    async def get_latest_checkpoint(
        self,
        trace_id: str,
        *,
        checkpoint_type: CheckpointType | None = None,
    ) -> Checkpoint | None:
        """Get the most recent active checkpoint for a trace."""
        checkpoints = await self.list_checkpoints(
            trace_id,
            status=CheckpointStatus.ACTIVE,
            checkpoint_type=checkpoint_type,
        )
        return checkpoints[0] if checkpoints else None

    async def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint."""
        checkpoint = self._checkpoints.get(checkpoint_id)
        if not checkpoint:
            return False

        checkpoint.status = CheckpointStatus.DELETED
        checkpoint.updated_at = datetime.utcnow()

        # Remove from local storage
        del self._checkpoints[checkpoint_id]

        # Remove from trace index
        trace_ids = self._checkpoints_by_trace.get(checkpoint.trace_id, [])
        if checkpoint_id in trace_ids:
            trace_ids.remove(checkpoint_id)

        # Update metrics
        self._metrics.checkpoints_deleted += 1

        # Sync deletion to backend
        if self._config.sync_to_backend and self._api_url:
            await self._delete_checkpoint_from_backend(checkpoint_id)

        logger.debug(f"Deleted checkpoint {checkpoint_id}")
        return True

    async def create_remediation_checkpoint(
        self,
        trace_id: str,
        state: dict[str, Any],
        span_id: str | None = None,
        issues: list[str] | None = None,
    ) -> Checkpoint:
        """
        Create an automatic checkpoint before remediation.

        This is called automatically when auto_checkpoint_on_remediation is enabled.

        Args:
            trace_id: Trace ID
            state: Current agent state
            span_id: Span ID where remediation is happening
            issues: List of issues being remediated

        Returns:
            Created Checkpoint
        """
        return await self.create(
            trace_id=trace_id,
            state=state,
            span_id=span_id,
            checkpoint_type=CheckpointType.AUTO_REMEDIATION,
            metadata={"issues": issues or []},
            reason=f"Auto-checkpoint before remediation ({len(issues or [])} issues)",
            tags=["auto", "remediation"],
        )

    async def create_tool_call_checkpoint(
        self,
        trace_id: str,
        state: dict[str, Any],
        tool_name: str,
        tool_args: dict[str, Any],
        span_id: str | None = None,
    ) -> Checkpoint:
        """
        Create an automatic checkpoint before a tool call.

        This is called automatically when auto_checkpoint_on_tool_call is enabled.

        Args:
            trace_id: Trace ID
            state: Current agent state
            tool_name: Name of the tool being called
            tool_args: Arguments to the tool
            span_id: Span ID

        Returns:
            Created Checkpoint
        """
        return await self.create(
            trace_id=trace_id,
            state=state,
            span_id=span_id,
            checkpoint_type=CheckpointType.PRE_TOOL_CALL,
            metadata={"tool_name": tool_name, "tool_args": tool_args},
            reason=f"Auto-checkpoint before tool call: {tool_name}",
            tags=["auto", "tool_call", tool_name],
        )

    async def _enforce_max_checkpoints(self, trace_id: str) -> None:
        """Enforce maximum checkpoints per trace by expiring old ones."""
        checkpoint_ids = self._checkpoints_by_trace.get(trace_id, [])

        while len(checkpoint_ids) > self._config.max_checkpoints_per_trace:
            # Find oldest checkpoint
            oldest_id = checkpoint_ids[0]
            oldest = self._checkpoints.get(oldest_id)

            if oldest:
                oldest.status = CheckpointStatus.EXPIRED
                oldest.updated_at = datetime.utcnow()
                self._metrics.checkpoints_expired += 1

            checkpoint_ids.pop(0)

    async def _sync_checkpoint_to_backend(self, checkpoint: Checkpoint) -> None:
        """Sync a checkpoint to the backend."""
        if not self._api_url or not self._api_key:
            return

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-API-Key": self._api_key,
                    "Content-Type": "application/json",
                }

                async with session.post(
                    f"{self._api_url}/v1/checkpoints",
                    json=checkpoint.to_dict(),
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status in (200, 201):
                        self._metrics.backend_syncs += 1
                    else:
                        logger.warning(f"Failed to sync checkpoint to backend: {response.status}")
                        self._metrics.backend_sync_failures += 1

        except ImportError:
            logger.debug("aiohttp not installed, skipping backend sync")
        except Exception as e:
            logger.warning(f"Error syncing checkpoint to backend: {e}")
            self._metrics.backend_sync_failures += 1

    async def _fetch_checkpoint_from_backend(
        self,
        checkpoint_id: str,
    ) -> Checkpoint | None:
        """Fetch a checkpoint from the backend."""
        if not self._api_url or not self._api_key:
            return None

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-API-Key": self._api_key,
                }

                async with session.get(
                    f"{self._api_url}/v1/checkpoints/{checkpoint_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        checkpoint = Checkpoint.from_dict(data)
                        # Cache locally
                        self._checkpoints[checkpoint_id] = checkpoint
                        return checkpoint

        except ImportError:
            logger.debug("aiohttp not installed, cannot fetch from backend")
        except Exception as e:
            logger.warning(f"Error fetching checkpoint from backend: {e}")

        return None

    async def _delete_checkpoint_from_backend(self, checkpoint_id: str) -> None:
        """Delete a checkpoint from the backend."""
        if not self._api_url or not self._api_key:
            return

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-API-Key": self._api_key,
                }

                async with session.delete(
                    f"{self._api_url}/v1/checkpoints/{checkpoint_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status not in (200, 204):
                        logger.warning(
                            f"Failed to delete checkpoint from backend: {response.status}"
                        )

        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Error deleting checkpoint from backend: {e}")

    def get_metrics(self) -> CheckpointMetrics:
        """Get checkpoint metrics."""
        return self._metrics

    def get_stats(self) -> dict[str, Any]:
        """Get checkpoint manager statistics."""
        return {
            **self._metrics.to_dict(),
            "total_checkpoints": len(self._checkpoints),
            "traces_with_checkpoints": len(self._checkpoints_by_trace),
            "config": {
                "default_retention_hours": self._config.default_retention_hours,
                "max_checkpoints_per_trace": self._config.max_checkpoints_per_trace,
                "auto_checkpoint_on_remediation": self._config.auto_checkpoint_on_remediation,
                "sync_to_backend": self._config.sync_to_backend,
            },
        }

    async def cleanup_expired(self) -> int:
        """Clean up expired checkpoints. Returns number cleaned."""
        now = datetime.utcnow()
        expired_count = 0

        for checkpoint_id, checkpoint in list(self._checkpoints.items()):
            if checkpoint.expires_at and checkpoint.expires_at < now:
                checkpoint.status = CheckpointStatus.EXPIRED
                del self._checkpoints[checkpoint_id]
                expired_count += 1

        self._metrics.checkpoints_expired += expired_count
        return expired_count

    async def start_background_tasks(self) -> None:
        """Start background cleanup and sync tasks."""
        if not self._cleanup_task or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def stop_background_tasks(self) -> None:
        """Stop background tasks."""
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._cleanup_task

    async def _cleanup_loop(self) -> None:
        """Background loop for cleaning up expired checkpoints."""
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                await self.cleanup_expired()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.warning(f"Checkpoint cleanup error: {e}")
