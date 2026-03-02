"""Checkpoint module for git-based agent checkpoints.

This module provides automatic checkpoint creation after each agentic
loop completes, storing file changes as git commits with metadata.

Example:
    from emdash_core.checkpoint import CheckpointManager

    manager = CheckpointManager(repo_root=Path("."))

    # Create checkpoint after agent run
    checkpoint = manager.create_checkpoint(
        messages=runner._messages,
        model=runner.model,
        system_prompt=runner.system_prompt,
        tools_used=["read_file", "write_to_file"],
        token_usage={"input": 1000, "output": 500},
    )

    # List checkpoints
    for cp in manager.list_checkpoints():
        print(f"{cp.id}: {cp.summary}")

    # Restore to checkpoint
    conv = manager.restore_checkpoint("cp_abc123_001")
"""

from .manager import CheckpointManager
from .models import CheckpointMetadata, ConversationState, CheckpointIndex
from .storage import CheckpointStorage
from .git_operations import GitCheckpointOperations

__all__ = [
    "CheckpointManager",
    "CheckpointMetadata",
    "ConversationState",
    "CheckpointIndex",
    "CheckpointStorage",
    "GitCheckpointOperations",
]
