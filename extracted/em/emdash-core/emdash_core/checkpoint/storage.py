"""File storage for checkpoint data."""

import json
from pathlib import Path
from typing import Optional

from ..utils.logger import log
from .models import CheckpointIndex, CheckpointMetadata, ConversationState


class CheckpointStorage:
    """Handles checkpoint file storage.

    Stores conversation state and checkpoint index in:
        .emdash/checkpoints/
            index.json                           # Checkpoint index
            {session_id}/{checkpoint_id}/
                conversation.json                # Full conversation state
    """

    CHECKPOINT_DIR = ".emdash/checkpoints"
    INDEX_FILE = "index.json"

    def __init__(self, repo_root: Path):
        """Initialize checkpoint storage.

        Args:
            repo_root: Root of the repository
        """
        self.repo_root = repo_root.resolve()
        self.checkpoint_dir = self.repo_root / self.CHECKPOINT_DIR

    def _ensure_dir(self, path: Path) -> None:
        """Ensure directory exists."""
        path.mkdir(parents=True, exist_ok=True)

    def _get_checkpoint_path(self, session_id: str, checkpoint_id: str) -> Path:
        """Get path for a checkpoint's data directory."""
        return self.checkpoint_dir / session_id / checkpoint_id

    def save_conversation(
        self,
        checkpoint_id: str,
        session_id: str,
        state: ConversationState,
    ) -> Path:
        """Save conversation state to checkpoint directory.

        Args:
            checkpoint_id: Unique checkpoint ID
            session_id: Session ID
            state: Conversation state to save

        Returns:
            Path to saved file
        """
        checkpoint_path = self._get_checkpoint_path(session_id, checkpoint_id)
        self._ensure_dir(checkpoint_path)

        file_path = checkpoint_path / "conversation.json"
        with open(file_path, "w") as f:
            json.dump(state.to_dict(), f, indent=2)

        log.debug(f"Saved conversation to {file_path}")
        return file_path

    def load_conversation(
        self,
        checkpoint_id: str,
        session_id: str,
    ) -> Optional[ConversationState]:
        """Load conversation state from checkpoint.

        Args:
            checkpoint_id: Unique checkpoint ID
            session_id: Session ID

        Returns:
            ConversationState if found, None otherwise
        """
        checkpoint_path = self._get_checkpoint_path(session_id, checkpoint_id)
        file_path = checkpoint_path / "conversation.json"

        if not file_path.exists():
            log.warning(f"Conversation file not found: {file_path}")
            return None

        with open(file_path) as f:
            data = json.load(f)
            return ConversationState.from_dict(data)

    def get_index_path(self) -> Path:
        """Get path to index file."""
        return self.checkpoint_dir / self.INDEX_FILE

    def load_index(self) -> CheckpointIndex:
        """Load checkpoint index.

        Returns:
            CheckpointIndex, empty if file doesn't exist
        """
        index_path = self.get_index_path()
        if not index_path.exists():
            return CheckpointIndex()

        try:
            with open(index_path) as f:
                data = json.load(f)
                return CheckpointIndex.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            log.warning(f"Failed to load checkpoint index: {e}")
            return CheckpointIndex()

    def save_index(self, index: CheckpointIndex) -> None:
        """Save checkpoint index.

        Args:
            index: CheckpointIndex to save
        """
        self._ensure_dir(self.checkpoint_dir)
        index_path = self.get_index_path()

        with open(index_path, "w") as f:
            json.dump(index.to_dict(), f, indent=2)

        log.debug(f"Saved checkpoint index to {index_path}")

    def update_index(self, metadata: CheckpointMetadata) -> None:
        """Add a checkpoint to the index.

        Args:
            metadata: Checkpoint metadata to add
        """
        index = self.load_index()
        index.add(metadata)
        self.save_index(index)

    def get_checkpoints(
        self,
        session_id: Optional[str] = None,
        limit: int = 50,
    ) -> list[CheckpointMetadata]:
        """Get checkpoints from index.

        Args:
            session_id: Filter by session ID (optional)
            limit: Maximum number of checkpoints to return

        Returns:
            List of CheckpointMetadata, most recent first
        """
        index = self.load_index()

        if session_id:
            checkpoints = index.find_by_session(session_id)
        else:
            checkpoints = index.checkpoints

        return checkpoints[:limit]

    def find_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointMetadata]:
        """Find a checkpoint by ID.

        Args:
            checkpoint_id: Checkpoint ID to find

        Returns:
            CheckpointMetadata if found, None otherwise
        """
        index = self.load_index()
        return index.find(checkpoint_id)

    def delete_checkpoint(self, checkpoint_id: str, session_id: str) -> bool:
        """Delete a checkpoint's data.

        Note: This only deletes the conversation data, not the git commit.

        Args:
            checkpoint_id: Checkpoint ID to delete
            session_id: Session ID

        Returns:
            True if deleted, False if not found
        """
        checkpoint_path = self._get_checkpoint_path(session_id, checkpoint_id)

        if not checkpoint_path.exists():
            return False

        import shutil
        shutil.rmtree(checkpoint_path)

        # Update index
        index = self.load_index()
        index.checkpoints = [
            cp for cp in index.checkpoints if cp.id != checkpoint_id
        ]
        self.save_index(index)

        log.info(f"Deleted checkpoint {checkpoint_id}")
        return True
