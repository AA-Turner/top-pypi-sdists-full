"""Checkpoint manager for orchestrating git-based checkpoints."""

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from ..utils.logger import log
from .models import CheckpointMetadata, ConversationState
from .git_operations import GitCheckpointOperations
from .storage import CheckpointStorage


class CheckpointManager:
    """Manages git-based checkpoints for agent sessions.

    Creates checkpoint commits after each agentic loop completes,
    storing file changes in git and conversation state in files.

    Example:
        manager = CheckpointManager(repo_root=Path("."))

        # After agent completes a run
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

    def __init__(
        self,
        repo_root: Path,
        session_id: Optional[str] = None,
        enabled: bool = True,
    ):
        """Initialize checkpoint manager.

        Args:
            repo_root: Root of the git repository
            session_id: Optional session ID (auto-generated if None)
            enabled: Whether checkpointing is enabled
        """
        self.repo_root = repo_root.resolve()
        self.session_id = session_id or str(uuid4())[:8]
        self.enabled = enabled
        self.iteration = 0

        self.git_ops = GitCheckpointOperations(repo_root)
        self.storage = CheckpointStorage(repo_root)

    def create_checkpoint(
        self,
        messages: list[dict],
        model: str,
        system_prompt: str,
        tools_used: list[str],
        token_usage: dict[str, int],
        summary: Optional[str] = None,
    ) -> Optional[CheckpointMetadata]:
        """Create a checkpoint after successful agent run.

        Creates a git commit with all file changes and saves
        conversation state for later restoration.

        Args:
            messages: Full conversation message history
            model: Model used for the run
            system_prompt: System prompt used
            tools_used: List of tool names used during the run
            token_usage: Token usage stats (input, output, thinking)
            summary: Optional human-readable summary

        Returns:
            CheckpointMetadata if checkpoint was created, None if no changes
        """
        if not self.enabled:
            log.debug("Checkpointing disabled, skipping")
            return None

        # Check for changes
        if not self.git_ops.has_changes():
            log.debug("No changes to checkpoint")
            return None

        self.iteration += 1
        checkpoint_id = f"cp_{self.session_id}_{self.iteration:03d}"
        timestamp = datetime.now().isoformat()

        # Generate summary if not provided
        if not summary:
            summary = self._generate_summary(messages)

        # Get list of modified files
        files_modified = self.git_ops.get_modified_files()

        # Build metadata
        metadata = CheckpointMetadata(
            id=checkpoint_id,
            session_id=self.session_id,
            iteration=self.iteration,
            timestamp=timestamp,
            summary=summary,
            tools_used=tools_used,
            files_modified=files_modified,
            token_usage=token_usage,
        )

        # Save conversation state first (so it's included in the commit)
        conv_state = ConversationState(
            messages=messages,
            model=model,
            system_prompt_hash=hashlib.sha256(
                system_prompt.encode()
            ).hexdigest()[:16],
            token_usage=token_usage,
        )
        self.storage.save_conversation(checkpoint_id, self.session_id, conv_state)

        # Create git commit (includes the conversation file)
        commit_sha = self.git_ops.create_checkpoint_commit(metadata, summary)
        metadata.commit_sha = commit_sha

        # Update index
        self.storage.update_index(metadata)

        log.info(f"Created checkpoint {checkpoint_id} at {commit_sha[:8]}")
        return metadata

    def _generate_summary(self, messages: list[dict]) -> str:
        """Generate a brief summary from messages.

        Extracts the last user query and summarizes the response.

        Args:
            messages: Conversation messages

        Returns:
            Brief summary string
        """
        # Find last user message
        user_query = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str) and not content.startswith("[SYSTEM"):
                    user_query = content[:100]
                    if len(content) > 100:
                        user_query += "..."
                    break

        if user_query:
            return f"Response to: {user_query}"
        return "Agent checkpoint"

    def restore_checkpoint(
        self,
        checkpoint_id: str,
        restore_conversation: bool = True,
        create_branch: bool = True,
    ) -> Optional[ConversationState]:
        """Restore to a checkpoint.

        Checks out the git commit and optionally loads conversation state.

        Args:
            checkpoint_id: ID of checkpoint to restore
            restore_conversation: Whether to load conversation state
            create_branch: Whether to create a branch at the restored state

        Returns:
            ConversationState if restore_conversation=True, None otherwise

        Raises:
            ValueError: If checkpoint not found
        """
        # Find checkpoint in index
        metadata = self.storage.find_checkpoint(checkpoint_id)
        if not metadata:
            raise ValueError(f"Checkpoint not found: {checkpoint_id}")

        if not metadata.commit_sha:
            raise ValueError(f"Checkpoint {checkpoint_id} has no commit SHA")

        # Git checkout
        self.git_ops.restore_to_commit(metadata.commit_sha, create_branch)

        # Load conversation if requested
        if restore_conversation:
            return self.storage.load_conversation(
                checkpoint_id,
                metadata.session_id,
            )
        return None

    def list_checkpoints(
        self,
        session_id: Optional[str] = None,
        limit: int = 50,
    ) -> list[CheckpointMetadata]:
        """List checkpoints.

        Args:
            session_id: Filter by session ID (optional)
            limit: Maximum number of checkpoints

        Returns:
            List of CheckpointMetadata, most recent first
        """
        return self.storage.get_checkpoints(session_id, limit)

    def get_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointMetadata]:
        """Get a specific checkpoint by ID.

        Args:
            checkpoint_id: Checkpoint ID

        Returns:
            CheckpointMetadata if found, None otherwise
        """
        return self.storage.find_checkpoint(checkpoint_id)
