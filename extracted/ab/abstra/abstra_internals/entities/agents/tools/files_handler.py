"""Tool handlers for file and source code operations.

Files handlers operate on a configurable base directory.
Source code handlers operate on the project root (read-only).
"""

import fnmatch
import mimetypes
from pathlib import Path
from typing import Any, Dict

from abstra_internals.interface.sdk.files import create_public_link
from abstra_internals.settings import Settings


def _is_glob_allowed(path: str, glob_pattern: str) -> bool:
    """Check if a path matches a glob pattern. Empty pattern means all allowed."""
    if not glob_pattern:
        return True
    return fnmatch.fnmatch(path, glob_pattern)


def _safe_path(base: Path, relative: str) -> Path:
    """Resolve a relative path within a base directory, preventing traversal."""
    resolved = (base / relative).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise ValueError(f"Path traversal not allowed: {relative}")
    return resolved


class FilesReadHandler:
    """Read files from a base directory."""

    def __init__(self, base_dir: Path, glob_pattern: str = "") -> None:
        self._base_dir = base_dir
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "files_read"

    @property
    def description(self) -> str:
        return (
            "Read a file from the agent's temporary working directory. "
            "This directory is for files YOU created (via files_write) or downloaded (via move_download). "
            "To read project files (e.g. logo.png, config.json), use source_code_read instead."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path within the working directory.",
                },
            },
            "required": ["path"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", "")
        if not rel_path:
            return "Error: 'path' is required."

        if not _is_glob_allowed(rel_path, self._glob):
            return f"Error: path '{rel_path}' not allowed by pattern '{self._glob}'."

        try:
            full_path = _safe_path(self._base_dir, rel_path)
            if not full_path.exists():
                return f"Error: file not found: {rel_path}. This directory only contains files you created or downloaded. To read project files, use source_code_read instead."
            content = full_path.read_text(encoding="utf-8")
            if len(content) > 50000:
                content = content[:50000] + "\n... (truncated)"
            return content
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error reading file: {e}"


class FilesWriteHandler:
    """Write/create files in a base directory."""

    def __init__(self, base_dir: Path, glob_pattern: str = "") -> None:
        self._base_dir = base_dir
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "files_write"

    @property
    def description(self) -> str:
        return (
            "Create or overwrite a file in the agent's temporary working directory. "
            "Use this to save outputs, reports, or downloaded content. "
            "The observation will include the absolute file path."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path within the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file.",
                },
            },
            "required": ["path", "content"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", "")
        content = action_input.get("content", "")
        if not rel_path:
            return "Error: 'path' is required."

        if not _is_glob_allowed(rel_path, self._glob):
            return f"Error: path '{rel_path}' not allowed by pattern '{self._glob}'."

        try:
            full_path = _safe_path(self._base_dir, rel_path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            return f"File written: {full_path} ({len(content)} bytes)"
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error writing file: {e}"


class FilesDeleteHandler:
    """Delete files from a base directory."""

    def __init__(self, base_dir: Path, glob_pattern: str = "") -> None:
        self._base_dir = base_dir
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "files_delete"

    @property
    def description(self) -> str:
        return "Delete a file from the agent's temporary working directory."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path within the working directory.",
                },
            },
            "required": ["path"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", "")
        if not rel_path:
            return "Error: 'path' is required."

        if not _is_glob_allowed(rel_path, self._glob):
            return f"Error: path '{rel_path}' not allowed by pattern '{self._glob}'."

        try:
            full_path = _safe_path(self._base_dir, rel_path)
            if not full_path.exists():
                return f"Error: file not found: {rel_path}"
            full_path.unlink()
            return f"File deleted: {full_path}"
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error deleting file: {e}"


class FilesListHandler:
    """List files in a base directory."""

    def __init__(self, base_dir: Path, glob_pattern: str = "") -> None:
        self._base_dir = base_dir
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "files_list"

    @property
    def description(self) -> str:
        return (
            "List files in the agent's temporary working directory. "
            "This directory only contains files you created or downloaded. "
            "To list project files, use source_code_list instead."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative directory path (default: root of working dir).",
                    "default": ".",
                },
            },
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", ".")
        try:
            base = self._base_dir
            full_path = _safe_path(base, rel_path)
            if not full_path.exists():
                return f"Error: directory not found: {rel_path}"
            if not full_path.is_dir():
                return f"Error: not a directory: {rel_path}"

            entries = []
            for entry in sorted(full_path.iterdir()):
                rel = str(entry.relative_to(base))
                if self._glob and not _is_glob_allowed(rel, self._glob):
                    continue
                kind = "dir" if entry.is_dir() else "file"
                size = entry.stat().st_size if entry.is_file() else 0
                entries.append(
                    f"  {kind}: {entry} ({size} bytes)"
                    if kind == "file"
                    else f"  {kind}: {entry}/"
                )

            if not entries:
                return "Directory is empty."
            return "\n".join(entries)
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error listing files: {e}"


class SourceCodeReadHandler:
    """Read source code files from the project root (read-only)."""

    def __init__(self, glob_pattern: str = "") -> None:
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "source_code_read"

    @property
    def description(self) -> str:
        return (
            "Read a file from the project directory (read-only). "
            "Use this to access project files like images, configs, scripts, or any file referenced in the task. "
            "For files you created yourself, use files_read instead."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path within the project root (e.g. 'logo.png', 'data/input.csv').",
                },
            },
            "required": ["path"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", "")
        if not rel_path:
            return "Error: 'path' is required."

        if not _is_glob_allowed(rel_path, self._glob):
            return f"Error: path '{rel_path}' not allowed by pattern '{self._glob}'."

        try:
            full_path = _safe_path(Settings.root_path, rel_path)
            if not full_path.exists():
                return f"Error: file not found: {rel_path}"
            try:
                content = full_path.read_text(encoding="utf-8")
                if len(content) > 50000:
                    content = content[:50000] + "\n... (truncated)"
                return content
            except UnicodeDecodeError:
                mime_type = (
                    mimetypes.guess_type(str(full_path))[0]
                    or "application/octet-stream"
                )
                size = full_path.stat().st_size
                return (
                    f"Binary file: {rel_path}\n"
                    f"Type: {mime_type}\n"
                    f"Size: {size} bytes\n"
                    f"Absolute path: {full_path}\n"
                    f"This file cannot be read as text. "
                    f"To share this file, use create_public_link to get a public URL."
                )
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error reading file: {e}"


class CreatePublicLinkHandler:
    """Create a public link for a project file."""

    def __init__(self, glob_pattern: str = "") -> None:
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "create_public_link"

    @property
    def description(self) -> str:
        return (
            "Create a publicly accessible URL for a project file. "
            "Use this when you need to share a file (image, PDF, etc.) via a message or link. "
            "The returned URL can be sent in Slack messages, emails, etc."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative file path within the project (e.g. 'logo.png', 'reports/output.pdf').",
                },
            },
            "required": ["path"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", "")
        if not rel_path:
            return "Error: 'path' is required."

        if not _is_glob_allowed(rel_path, self._glob):
            return f"Error: path '{rel_path}' not allowed by pattern '{self._glob}'."

        try:
            full_path = _safe_path(Settings.root_path, rel_path)
            if not full_path.exists():
                return f"Error: file not found: {rel_path}"
            url = create_public_link(full_path)
            return f"Public link created: {url}"
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error creating public link: {e}"


class SourceCodeListHandler:
    """List source code files in the project root (read-only)."""

    def __init__(self, glob_pattern: str = "") -> None:
        self._glob = glob_pattern

    @property
    def name(self) -> str:
        return "source_code_list"

    @property
    def description(self) -> str:
        return (
            "List files in the project directory (read-only). "
            "Use this to find project files like images, configs, scripts, or any file referenced in the task. "
            "For files you created yourself, use files_list instead."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative directory path within the project (default: project root).",
                    "default": ".",
                },
            },
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        rel_path = action_input.get("path", ".")
        try:
            base = Settings.root_path
            full_path = _safe_path(base, rel_path)
            if not full_path.exists():
                return f"Error: directory not found: {rel_path}"
            if not full_path.is_dir():
                return f"Error: not a directory: {rel_path}"

            entries = []
            for entry in sorted(full_path.iterdir()):
                name = entry.name
                if (
                    name.startswith(".")
                    or name == "__pycache__"
                    or name == "node_modules"
                ):
                    continue
                rel = str(entry.relative_to(base))
                if self._glob and not _is_glob_allowed(rel, self._glob):
                    continue
                kind = "dir" if entry.is_dir() else "file"
                size = entry.stat().st_size if entry.is_file() else 0
                entries.append(
                    f"  {kind}: {rel} ({size} bytes)"
                    if kind == "file"
                    else f"  {kind}: {rel}/"
                )

            if not entries:
                return "Directory is empty."
            return "\n".join(entries)
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error listing files: {e}"
