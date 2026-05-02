"""
Conversation Logger for tracking user inputs and AI outputs.

Maintains separate logs for:
- User inputs (prompts, questions)
- AI outputs (responses, generations)

This provides context and memory for the AI chat system.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from .config import settings

logger = logging.getLogger("ai-platform.conversation_logger")

# Simple token estimation: ~4 chars per token
CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    """Estimate token count for text."""
    return max(1, len(text) // CHARS_PER_TOKEN)


class ConversationLogger:
    """Logs conversation inputs and outputs separately."""

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or (settings.data_dir / "conversation_logs")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _inputs_path(self, conversation_id: str) -> Path:
        """Get path to inputs log file."""
        return self.base_dir / f"{conversation_id}_inputs.json"

    def _outputs_path(self, conversation_id: str) -> Path:
        """Get path to outputs log file."""
        return self.base_dir / f"{conversation_id}_outputs.json"

    def _load_log(self, path: Path) -> list[dict]:
        """Load a log file."""
        if not path.exists():
            return []
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Corrupt log file %s: %s", path, e)
            return []

    def _save_log(self, path: Path, entries: list[dict]) -> None:
        """Save a log file."""
        path.write_text(json.dumps(entries, indent=2), encoding="utf-8")

    def log_input(
        self,
        conversation_id: str,
        content: str,
        timestamp: str | None = None,
        attachments: list[dict] | None = None,
    ) -> None:
        """
        Log a user input.

        Args:
            conversation_id: Conversation identifier
            content: User's input text
            timestamp: Optional timestamp (ISO format)
            attachments: Optional list of file attachments
        """
        path = self._inputs_path(conversation_id)
        entries = self._load_log(path)

        entry = {
            "content": content,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "token_count": estimate_tokens(content),
        }

        if attachments:
            entry["attachments"] = attachments

        entries.append(entry)
        self._save_log(path, entries)

        logger.debug(
            "Logged input for %s: %d chars, %d tokens",
            conversation_id,
            len(content),
            entry["token_count"],
        )

    def log_output(
        self,
        conversation_id: str,
        content: str,
        model_id: str,
        timestamp: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        """
        Log an AI output.

        Args:
            conversation_id: Conversation identifier
            content: AI's output text
            model_id: Model that generated the output
            timestamp: Optional timestamp (ISO format)
            metadata: Optional additional metadata
        """
        path = self._outputs_path(conversation_id)
        entries = self._load_log(path)

        entry = {
            "content": content,
            "model_id": model_id,
            "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
            "token_count": estimate_tokens(content),
        }

        if metadata:
            entry["metadata"] = metadata

        entries.append(entry)
        self._save_log(path, entries)

        logger.debug(
            "Logged output for %s: %d chars, %d tokens, model=%s",
            conversation_id,
            len(content),
            entry["token_count"],
            model_id,
        )

    def get_inputs(self, conversation_id: str) -> list[dict]:
        """
        Get all inputs for a conversation.

        Args:
            conversation_id: Conversation identifier

        Returns:
            List of input entries
        """
        return self._load_log(self._inputs_path(conversation_id))

    def get_outputs(self, conversation_id: str) -> list[dict]:
        """
        Get all outputs for a conversation.

        Args:
            conversation_id: Conversation identifier

        Returns:
            List of output entries
        """
        return self._load_log(self._outputs_path(conversation_id))

    def export(self, conversation_id: str) -> dict:
        """
        Export full conversation log.

        Args:
            conversation_id: Conversation identifier

        Returns:
            Dict with inputs and outputs lists
        """
        return {
            "conversation_id": conversation_id,
            "inputs": self.get_inputs(conversation_id),
            "outputs": self.get_outputs(conversation_id),
            "exported_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_context(self, conversation_id: str, max_entries: int = 10) -> list[dict]:
        """
        Get recent context for AI (interleaved inputs/outputs).

        Args:
            conversation_id: Conversation identifier
            max_entries: Maximum entries to return

        Returns:
            List of context entries with role markers
        """
        inputs = self.get_inputs(conversation_id)
        outputs = self.get_outputs(conversation_id)

        # Interleave by timestamp
        context = []
        for inp in inputs:
            context.append({
                "role": "user",
                "content": inp["content"],
                "timestamp": inp["timestamp"],
            })
        for out in outputs:
            context.append({
                "role": "assistant",
                "content": out["content"],
                "timestamp": out["timestamp"],
            })

        # Sort by timestamp
        context.sort(key=lambda x: x["timestamp"])

        # Return most recent
        return context[-max_entries:]

    def delete(self, conversation_id: str) -> None:
        """
        Delete logs for a conversation.

        Args:
            conversation_id: Conversation identifier
        """
        inputs_path = self._inputs_path(conversation_id)
        outputs_path = self._outputs_path(conversation_id)

        if inputs_path.exists():
            inputs_path.unlink()
        if outputs_path.exists():
            outputs_path.unlink()

        logger.info("Deleted logs for conversation: %s", conversation_id)

    def get_stats(self, conversation_id: str) -> dict:
        """
        Get statistics for a conversation.

        Args:
            conversation_id: Conversation identifier

        Returns:
            Dict with stats
        """
        inputs = self.get_inputs(conversation_id)
        outputs = self.get_outputs(conversation_id)

        total_input_tokens = sum(i.get("token_count", 0) for i in inputs)
        total_output_tokens = sum(o.get("token_count", 0) for o in outputs)

        return {
            "conversation_id": conversation_id,
            "input_count": len(inputs),
            "output_count": len(outputs),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
        }


# Global conversation logger instance
conversation_logger = ConversationLogger()
