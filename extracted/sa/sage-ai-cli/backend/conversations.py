import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings

logger = logging.getLogger("ai-platform.conversations")


class ConversationStore:
    """Persists conversations as individual JSON files in data_dir/conversations/."""

    def __init__(self) -> None:
        self.base = settings.data_dir / "conversations"
        self.base.mkdir(parents=True, exist_ok=True)

    def _path(self, conversation_id: str) -> Path:
        return self.base / f"{conversation_id}.json"

    def create(self, title: str) -> dict:
        conv_id = str(uuid.uuid4())
        conv = {
            "id": conv_id,
            "title": title,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "messages": [],
        }
        self._path(conv_id).write_text(json.dumps(conv, indent=2), encoding="utf-8")
        return conv

    def get(self, conversation_id: str) -> dict:
        path = self._path(conversation_id)
        if not path.exists():
            raise KeyError(f"Conversation not found: {conversation_id}")
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Corrupt conversation file %s: %s", path, e)
            raise KeyError(f"Conversation corrupted: {conversation_id}") from e

    def list_all(self) -> list[dict]:
        convos = []
        for path in sorted(self.base.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                convos.append({
                    "id": data["id"],
                    "title": data["title"],
                    "created_at": data["created_at"],
                    "message_count": len(data.get("messages", [])),
                })
            except (json.JSONDecodeError, KeyError):
                logger.warning("Skipping corrupt conversation file: %s", path)
        return convos

    def append_message(self, conversation_id: str, role: str, content: str) -> None:
        path = self._path(conversation_id)
        if not path.exists():
            # Auto-create if needed
            conv = {
                "id": conversation_id,
                "title": "Untitled",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "messages": [],
            }
        else:
            try:
                conv = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                logger.error("Corrupt conversation file %s, resetting: %s", path, e)
                conv = {
                    "id": conversation_id,
                    "title": "Recovered",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "messages": [],
                }

        conv["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        path.write_text(json.dumps(conv, indent=2), encoding="utf-8")

    def delete(self, conversation_id: str) -> None:
        path = self._path(conversation_id)
        if path.exists():
            path.unlink()
