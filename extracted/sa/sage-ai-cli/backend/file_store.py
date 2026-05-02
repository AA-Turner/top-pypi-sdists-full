"""
File Store for managing uploaded files.

Provides:
- File upload with metadata storage
- File retrieval and download
- File deletion
- Content preview for text files
"""

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings

logger = logging.getLogger("ai-platform.files")

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Text MIME types that support preview
TEXT_MIME_TYPES = {
    "text/plain",
    "text/html",
    "text/css",
    "text/javascript",
    "text/x-python",
    "text/x-java",
    "text/x-c",
    "text/x-c++",
    "text/x-go",
    "text/x-rust",
    "text/markdown",
    "application/json",
    "application/xml",
    "application/javascript",
    "application/x-yaml",
    "application/x-sh",
}

# Preview length for text files
PREVIEW_LENGTH = 500


class FileStore:
    """Manages file storage with metadata."""

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or (settings.data_dir / "files")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir = self.base_dir / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir = self.base_dir / "content"
        self.content_dir.mkdir(parents=True, exist_ok=True)

    def _content_path(self, file_id: str) -> Path:
        """Get path to file content."""
        return self.content_dir / file_id

    def _metadata_path(self, file_id: str) -> Path:
        """Get path to file metadata."""
        return self.metadata_dir / f"{file_id}.json"

    def _generate_id(self) -> str:
        """Generate unique file ID."""
        return str(uuid.uuid4())

    def _is_text_type(self, mime_type: str) -> bool:
        """Check if MIME type is a text type."""
        if mime_type in TEXT_MIME_TYPES:
            return True
        if mime_type.startswith("text/"):
            return True
        return False

    def _generate_preview(self, content: bytes, mime_type: str) -> str | None:
        """Generate content preview for text files."""
        if not self._is_text_type(mime_type):
            return None

        try:
            text = content.decode("utf-8")
            if len(text) <= PREVIEW_LENGTH:
                return text
            return text[:PREVIEW_LENGTH] + "..."
        except UnicodeDecodeError:
            return None

    def save(
        self,
        content: bytes,
        filename: str,
        mime_type: str,
        file_id: str | None = None,
    ) -> str:
        """
        Save a file to the store.

        Args:
            content: File content as bytes
            filename: Original filename
            mime_type: MIME type of the file
            file_id: Optional custom file ID

        Returns:
            file_id: Unique identifier for the file

        Raises:
            ValueError: If file is empty or exceeds size limit
        """
        if not content:
            raise ValueError("File content cannot be empty")

        if len(content) > MAX_FILE_SIZE:
            raise ValueError(f"File exceeds maximum size of {MAX_FILE_SIZE} bytes")

        file_id = file_id or self._generate_id()

        # Sanitize filename
        safe_filename = self._sanitize_filename(filename)

        # Generate preview for text files
        preview = self._generate_preview(content, mime_type)

        # Save content
        content_path = self._content_path(file_id)
        content_path.write_bytes(content)

        # Save metadata
        metadata = {
            "file_id": file_id,
            "filename": safe_filename,
            "mime_type": mime_type,
            "size_bytes": len(content),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "content_preview": preview,
        }
        metadata_path = self._metadata_path(file_id)
        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        logger.info(
            "File saved: %s (%s, %d bytes)",
            file_id,
            safe_filename,
            len(content),
        )

        return file_id

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        # Remove path components
        filename = os.path.basename(filename)
        # Remove dangerous characters
        filename = filename.replace("..", "").replace("/", "").replace("\\", "")
        # Ensure not empty
        if not filename:
            filename = "unnamed"
        return filename

    def get(self, file_id: str) -> dict:
        """
        Retrieve a file from the store.

        Args:
            file_id: File identifier

        Returns:
            dict with content, filename, mime_type

        Raises:
            KeyError: If file not found
        """
        content_path = self._content_path(file_id)
        metadata_path = self._metadata_path(file_id)

        if not content_path.exists() or not metadata_path.exists():
            raise KeyError(f"File not found: {file_id}")

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Corrupt metadata for %s: %s", file_id, e)
            raise KeyError(f"File metadata corrupted: {file_id}") from e

        content = content_path.read_bytes()

        return {
            "content": content,
            "filename": metadata["filename"],
            "mime_type": metadata["mime_type"],
            "size_bytes": metadata["size_bytes"],
        }

    def get_metadata(self, file_id: str) -> dict:
        """
        Get file metadata without content.

        Args:
            file_id: File identifier

        Returns:
            dict with filename, mime_type, size_bytes, etc.

        Raises:
            KeyError: If file not found
        """
        metadata_path = self._metadata_path(file_id)

        if not metadata_path.exists():
            raise KeyError(f"File not found: {file_id}")

        try:
            return json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error("Corrupt metadata for %s: %s", file_id, e)
            raise KeyError(f"File metadata corrupted: {file_id}") from e

    def delete(self, file_id: str) -> None:
        """
        Delete a file from the store.

        Args:
            file_id: File identifier
        """
        content_path = self._content_path(file_id)
        metadata_path = self._metadata_path(file_id)

        if content_path.exists():
            content_path.unlink()
        if metadata_path.exists():
            metadata_path.unlink()

        logger.info("File deleted: %s", file_id)

    def list_all(self) -> list[dict]:
        """
        List all files in the store.

        Returns:
            List of file metadata dicts
        """
        files = []
        for metadata_path in sorted(
            self.metadata_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        ):
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                files.append({
                    "file_id": metadata["file_id"],
                    "filename": metadata["filename"],
                    "mime_type": metadata["mime_type"],
                    "size_bytes": metadata["size_bytes"],
                    "created_at": metadata.get("created_at"),
                })
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning("Skipping corrupt file metadata: %s (%s)", metadata_path, e)

        return files

    def get_content_for_chat(self, file_id: str) -> str:
        """
        Get file content formatted for AI chat context.

        Args:
            file_id: File identifier

        Returns:
            Formatted string with file content

        Raises:
            KeyError: If file not found
        """
        file_data = self.get(file_id)
        filename = file_data["filename"]
        mime_type = file_data["mime_type"]
        content = file_data["content"]

        # Try to decode as text
        if self._is_text_type(mime_type):
            try:
                text_content = content.decode("utf-8")
                return f"[File: {filename}]\n```\n{text_content}\n```"
            except UnicodeDecodeError:
                pass

        # Binary file - just indicate it exists
        return f"[Binary file: {filename} ({file_data['size_bytes']} bytes)]"


# Global file store instance
file_store = FileStore()
