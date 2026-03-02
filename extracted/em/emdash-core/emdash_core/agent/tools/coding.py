"""Coding tools for file operations."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class CodingTool(BaseTool):
    """Base class for coding tools that operate on files."""

    category = ToolCategory.PLANNING  # File ops are part of planning/coding workflow

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root for path validation.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used for file ops)
        """
        self.repo_root = repo_root.resolve()
        self.connection = connection

    def _validate_path(self, path: str) -> tuple[bool, str, Optional[Path]]:
        """Validate that a path is within the repo root.

        Args:
            path: Path to validate

        Returns:
            Tuple of (is_valid, error_message, resolved_path)
        """
        try:
            # Handle relative and absolute paths
            if os.path.isabs(path):
                full_path = Path(path).resolve()
            else:
                full_path = (self.repo_root / path).resolve()

            # Check if within repo
            try:
                full_path.relative_to(self.repo_root)
            except ValueError:
                return False, f"Path {path} is outside repository", None

            return True, "", full_path

        except Exception as e:
            return False, f"Invalid path: {e}", None


class ReadFileTool(CodingTool):
    """Read the contents of a file."""

    name = "read_file"
    description = """Read the contents of a file.
Returns the file content as text."""

    def execute(
        self,
        path: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> ToolResult:
        """Read a file.

        Args:
            path: Path to the file
            start_line: Optional starting line (1-indexed)
            end_line: Optional ending line (1-indexed)
            offset: Alternative to start_line - line number to start from (1-indexed)
            limit: Alternative to end_line - number of lines to read

        Returns:
            ToolResult with file content
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {path}")

        if not full_path.is_file():
            return ToolResult.error_result(f"Not a file: {path}")

        try:
            content = full_path.read_text()
            lines = content.split("\n")

            # Handle line ranges - support both start_line/end_line and offset/limit
            # offset/limit take precedence if provided
            if offset is not None or limit is not None:
                start_idx = (offset - 1) if offset else 0
                end_idx = start_idx + limit if limit else len(lines)
                lines = lines[start_idx:end_idx]
                content = "\n".join(lines)
            elif start_line or end_line:
                start_idx = (start_line - 1) if start_line else 0
                end_idx = end_line if end_line else len(lines)
                lines = lines[start_idx:end_idx]
                content = "\n".join(lines)

            return ToolResult.success_result(
                data={
                    "path": path,
                    "content": content,
                    "line_count": len(lines),
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to read file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to read",
                },
                "start_line": {
                    "type": "integer",
                    "description": "Starting line number (1-indexed)",
                },
                "end_line": {
                    "type": "integer",
                    "description": "Ending line number (1-indexed)",
                },
                "offset": {
                    "type": "integer",
                    "description": "Line number to start reading from (1-indexed). Alternative to start_line.",
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of lines to read. Alternative to end_line.",
                },
            },
            required=["path"],
        )


class WriteToFileTool(CodingTool):
    """Write content to a file."""

    name = "write_to_file"
    description = """Write content to a file.
Creates the file if it doesn't exist, or overwrites if it does."""

    def __init__(self, repo_root: Path, connection=None, allowed_paths: list[str] | None = None):
        """Initialize with optional path restrictions.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used for file ops)
            allowed_paths: If provided, only these paths can be written to.
                          Used in plan mode to restrict writes to the plan file.
        """
        super().__init__(repo_root, connection)
        self.allowed_paths = allowed_paths

    def execute(
        self,
        path: str,
        content: str,
    ) -> ToolResult:
        """Write to a file.

        Args:
            path: Path to the file
            content: Content to write

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        # Check allowed paths restriction (used in plan mode)
        if self.allowed_paths is not None:
            path_str = str(full_path)
            is_allowed = any(
                path_str == allowed or path_str.endswith(allowed.lstrip("/"))
                for allowed in self.allowed_paths
            )
            if not is_allowed:
                return ToolResult.error_result(
                    f"In plan mode, you can only write to: {', '.join(self.allowed_paths)}",
                    suggestions=["Write your plan to the designated plan file"],
                )

        try:
            # Capture old content if file exists (for diff rendering)
            old_content = ""
            if full_path.exists():
                old_content = full_path.read_text()

            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            full_path.write_text(content)

            return ToolResult.success_result(
                data={
                    "path": path,
                    "bytes_written": len(content),
                    "lines_written": content.count("\n") + 1,
                    "old_content": old_content,
                    "new_content": content,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to write file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to write",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            required=["path", "content"],
        )


class EditFileTool(CodingTool):
    """Performs exact string replacements in files."""

    name = "edit_file"
    description = """Performs exact string replacements in files.

Usage:
- You must use read_file at least once before editing. This tool will error if you attempt an edit without reading the file first.
- When editing text from read_file output, preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix.
- ALWAYS prefer editing existing files. NEVER write new files unless explicitly required.
- The edit will FAIL if old_string is not unique in the file. Either provide more surrounding context to make it unique or use replace_all.
- Use replace_all for replacing/renaming strings across the file (e.g., renaming a variable)."""

    def execute(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> ToolResult:
        """Edit a file using search and replace.

        Args:
            file_path: Absolute path to the file to modify
            old_string: The text to replace
            new_string: The text to replace it with (must be different from old_string)
            replace_all: Replace all occurrences of old_string (default: false)

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(file_path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {file_path}")

        # Validate old_string != new_string
        if old_string == new_string:
            return ToolResult.error_result("old_string and new_string must be different")

        try:
            content = full_path.read_text()
            old_content = content  # Store original for diff rendering

            # Check if old_string exists in file
            if old_string not in content:
                # Try to find similar content for better error message
                lines = content.split('\n')
                search_lines = old_string.split('\n')
                first_search = search_lines[0].strip() if search_lines else ""

                # Find lines that might be close matches
                close_matches = []
                for i, line in enumerate(lines):
                    if first_search and first_search in line:
                        close_matches.append(f"  Line {i+1}: {line.strip()[:80]}")

                error_msg = f"old_string not found in file"
                if close_matches:
                    error_msg += f"\n\nSimilar lines found:\n" + "\n".join(close_matches[:5])
                    error_msg += "\n\nMake sure whitespace/indentation matches exactly."

                return ToolResult.error_result(error_msg)

            # Check for uniqueness if not replace_all
            if not replace_all:
                count = content.count(old_string)
                if count > 1:
                    return ToolResult.error_result(
                        f"old_string found {count} times. Use replace_all=true or provide more context to make it unique."
                    )

            # Perform replacement
            if replace_all:
                new_content = content.replace(old_string, new_string)
                replacements = content.count(old_string)
            else:
                new_content = content.replace(old_string, new_string, 1)
                replacements = 1

            # Write back
            full_path.write_text(new_content)

            return ToolResult.success_result(
                data={
                    "file_path": file_path,
                    "replacements": replacements,
                    "old_content": old_content,
                    "new_content": new_content,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to edit file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to modify",
                },
                "old_string": {
                    "type": "string",
                    "description": "The text to replace",
                },
                "new_string": {
                    "type": "string",
                    "description": "The text to replace it with (must be different from old_string)",
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences of old_string (default: false)",
                    "default": False,
                },
            },
            required=["file_path", "old_string", "new_string"],
        )


class ApplyDiffTool(CodingTool):
    """Apply a search/replace diff to a file with fuzzy matching."""

    name = "apply_diff"
    description = """Apply changes to a file using search/replace blocks with fuzzy matching.

Format:
<<<<<<< SEARCH
[exact content to find - include enough context for uniqueness]
=======
[replacement content]
>>>>>>> REPLACE

You can include multiple SEARCH/REPLACE blocks in one diff.
The SEARCH content should match the file exactly (or very closely for fuzzy matching).
Include enough surrounding lines to make the match unique.

Example:
<<<<<<< SEARCH
def hello():
    print("Hello")
=======
def hello():
    print("Hello, World!")
>>>>>>> REPLACE"""

    # Confidence threshold for fuzzy matching (0.0-1.0)
    CONFIDENCE_THRESHOLD = 0.85
    # Buffer lines to extend search area around line hints
    BUFFER_LINES = 40

    def execute(
        self,
        file_path: str,
        diff: str,
    ) -> ToolResult:
        """Apply a search/replace diff to a file.

        Args:
            file_path: Path to the file to modify
            diff: Search/replace diff content

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(file_path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {file_path}")

        try:
            content = full_path.read_text()
            original_content = content

            # Parse the diff into search/replace blocks
            blocks = self._parse_diff_blocks(diff)
            if not blocks:
                return ToolResult.error_result(
                    "No valid SEARCH/REPLACE blocks found in diff.\n"
                    "Expected format:\n"
                    "<<<<<<< SEARCH\n"
                    "[content to find]\n"
                    "=======\n"
                    "[replacement]\n"
                    ">>>>>>> REPLACE"
                )

            # Apply each block
            applied = 0
            failed = []
            for i, block in enumerate(blocks):
                search_text = block["search"]
                replace_text = block["replace"]

                # Try exact match first
                if search_text in content:
                    # Check uniqueness
                    count = content.count(search_text)
                    if count > 1:
                        failed.append(f"Block {i+1}: SEARCH text found {count} times, add more context")
                        continue
                    content = content.replace(search_text, replace_text, 1)
                    applied += 1
                else:
                    # Try fuzzy matching
                    match_result = self._fuzzy_find(content, search_text)
                    if match_result:
                        start, end, confidence = match_result
                        if confidence >= self.CONFIDENCE_THRESHOLD:
                            content = content[:start] + replace_text + content[end:]
                            applied += 1
                        else:
                            failed.append(
                                f"Block {i+1}: Best match confidence {confidence:.2f} "
                                f"below threshold {self.CONFIDENCE_THRESHOLD}"
                            )
                    else:
                        # Provide helpful error with similar lines
                        similar = self._find_similar_lines(content, search_text)
                        error_msg = f"Block {i+1}: SEARCH text not found"
                        if similar:
                            error_msg += f"\nSimilar lines:\n{similar}"
                        failed.append(error_msg)

            if applied == 0:
                return ToolResult.error_result(
                    f"Failed to apply any blocks:\n" + "\n".join(failed)
                )

            # Write back
            full_path.write_text(content)

            result_data = {
                "file_path": file_path,
                "blocks_applied": applied,
                "blocks_total": len(blocks),
                "old_content": original_content,
                "new_content": content,
            }
            if failed:
                result_data["warnings"] = failed

            return ToolResult.success_result(data=result_data)

        except Exception as e:
            return ToolResult.error_result(f"Failed to apply diff: {e}")

    def _parse_diff_blocks(self, diff: str) -> list[dict]:
        """Parse diff into search/replace blocks."""
        import re

        blocks = []
        # Pattern to match search/replace blocks
        pattern = r'<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE'
        matches = re.findall(pattern, diff, re.DOTALL)

        for search, replace in matches:
            blocks.append({
                "search": search,
                "replace": replace,
            })

        return blocks

    def _fuzzy_find(self, content: str, search_text: str) -> tuple[int, int, float] | None:
        """Find best fuzzy match for search_text in content.

        Returns (start_index, end_index, confidence) or None if no good match.
        """
        from difflib import SequenceMatcher

        search_lines = search_text.split('\n')
        content_lines = content.split('\n')
        search_len = len(search_lines)

        if search_len == 0:
            return None

        best_match = None
        best_confidence = 0.0

        # Sliding window approach
        for i in range(len(content_lines) - search_len + 1):
            window = '\n'.join(content_lines[i:i + search_len])
            matcher = SequenceMatcher(None, search_text, window)
            confidence = matcher.ratio()

            if confidence > best_confidence:
                best_confidence = confidence
                # Calculate character positions
                start = sum(len(line) + 1 for line in content_lines[:i])
                end = start + len(window)
                best_match = (start, end, confidence)

        return best_match if best_confidence >= 0.5 else None

    def _find_similar_lines(self, content: str, search_text: str) -> str:
        """Find lines in content similar to the first line of search_text."""
        lines = content.split('\n')
        search_first = search_text.split('\n')[0].strip() if search_text else ""

        if not search_first:
            return ""

        similar = []
        for i, line in enumerate(lines):
            if search_first[:20] in line or line.strip()[:20] in search_first:
                similar.append(f"  Line {i+1}: {line.strip()[:60]}")
                if len(similar) >= 3:
                    break

        return "\n".join(similar)

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to modify",
                },
                "diff": {
                    "type": "string",
                    "description": "Search/replace diff with <<<<<<< SEARCH ... ======= ... >>>>>>> REPLACE blocks",
                },
            },
            required=["file_path", "diff"],
        )


class DeleteFileTool(CodingTool):
    """Delete a file."""

    name = "delete_file"
    description = """Delete a file from the repository.
Use with caution - this cannot be undone."""

    def execute(self, path: str) -> ToolResult:
        """Delete a file.

        Args:
            path: Path to the file

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {path}")

        if not full_path.is_file():
            return ToolResult.error_result(f"Not a file: {path}")

        try:
            full_path.unlink()

            return ToolResult.success_result(
                data={
                    "path": path,
                    "deleted": True,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to delete file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to delete",
                },
            },
            required=["path"],
        )


class ListFilesTool(CodingTool):
    """List files in a directory."""

    name = "list_files"
    description = """List files in a directory.
Can filter by pattern and recurse into subdirectories."""

    def execute(
        self,
        path: str = ".",
        pattern: Optional[str] = None,
        recursive: bool = False,
    ) -> ToolResult:
        """List files in a directory.

        Args:
            path: Directory path
            pattern: Optional glob pattern
            recursive: Whether to recurse

        Returns:
            ToolResult with file list
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"Directory not found: {path}")

        if not full_path.is_dir():
            return ToolResult.error_result(f"Not a directory: {path}")

        try:
            files = []
            glob_pattern = pattern or "*"

            if recursive:
                matches = full_path.rglob(glob_pattern)
            else:
                matches = full_path.glob(glob_pattern)

            for match in matches:
                if match.is_file():
                    # Get relative path from repo root
                    rel_path = match.relative_to(self.repo_root)
                    files.append({
                        "path": str(rel_path),
                        "size": match.stat().st_size,
                    })

            # Sort by path
            files.sort(key=lambda x: x["path"])

            return ToolResult.success_result(
                data={
                    "directory": path,
                    "files": files[:1000],  # Limit results
                    "count": len(files),
                    "truncated": len(files) > 1000,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to list files: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Directory path (default: current directory)",
                    "default": ".",
                },
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to filter files",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Recurse into subdirectories",
                    "default": False,
                },
            },
            required=[],
        )


class ExecuteCommandTool(CodingTool):
    """Execute a shell command."""

    name = "execute_command"
    description = """Execute a shell command in the repository.
Commands are run from the repository root.

IMPORTANT: Use run_in_background=true for:
- Dev servers: npm run dev, npm start, python -m http.server, flask run, etc.
- Watch mode: npm run watch, tsc --watch, etc.
- Any command that runs indefinitely or takes more than 30 seconds

Background commands return immediately with a task_id. You'll be notified
when they complete, or use task_output(task_id) to check status.

If a command times out, DO NOT retry it the same way - use run_in_background=true instead."""

    def execute(
        self,
        command: str,
        timeout: int = 60,
        run_in_background: bool = False,
        description: str = "",
    ) -> ToolResult:
        """Execute a command.

        Args:
            command: Command to execute
            timeout: Timeout in seconds (ignored for background commands)
            run_in_background: Run command in background, return immediately
            description: Short description of what this command does

        Returns:
            ToolResult with command output or task info for background
        """
        if run_in_background:
            return self._run_background(command, description)
        else:
            return self._run_sync(command, timeout)

    def _run_sync(self, command: str, timeout: int) -> ToolResult:
        """Run command synchronously."""
        import re

        # Inject GitHub token into git clone URLs for authentication
        # This is the most reliable method for containers without credential helpers
        github_token = os.environ.get("GITHUB_TOKEN")
        actual_command = command

        if github_token and "git clone" in command:
            # Pattern to match GitHub HTTPS URLs
            # Matches: https://github.com/owner/repo or https://github.com/owner/repo.git
            pattern = r'https://github\.com/([^/\s]+/[^/\s]+?)(?:\.git)?(?=\s|$)'

            def inject_token(match):
                repo_path = match.group(1)
                # Remove .git suffix if present for clean URL
                if repo_path.endswith('.git'):
                    repo_path = repo_path[:-4]
                return f'https://x-access-token:{github_token}@github.com/{repo_path}.git'

            actual_command = re.sub(pattern, inject_token, command)
            log.debug(f"Injected GitHub token into clone command")

        try:
            result = subprocess.run(
                actual_command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=timeout,
                env=os.environ.copy(),  # Explicitly pass environment
            )

            # Remove token from output for security
            stdout = result.stdout[-10000:] if result.stdout else ""
            stderr = result.stderr[-5000:] if result.stderr else ""
            if github_token:
                stdout = stdout.replace(github_token, "[REDACTED]")
                stderr = stderr.replace(github_token, "[REDACTED]")

            return ToolResult.success_result(
                data={
                    "command": command,  # Show original command (without token)
                    "exit_code": result.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                },
            )

        except subprocess.TimeoutExpired:
            return ToolResult.error_result(
                f"Command timed out after {timeout}s",
                suggestions=["Use run_in_background=true for long-running commands"],
            )
        except Exception as e:
            return ToolResult.error_result(f"Command failed: {e}")

    def _run_background(self, command: str, description: str) -> ToolResult:
        """Run command in background."""
        from ..background import BackgroundTaskManager

        try:
            manager = BackgroundTaskManager.get_instance()
            task_id = manager.start_shell(
                command=command,
                description=description or command[:50],
                cwd=self.repo_root,
            )

            return ToolResult.success_result(
                data={
                    "task_id": task_id,
                    "status": "running",
                    "command": command,
                    "message": "Command started in background. You'll be notified when it completes.",
                },
                suggestions=[
                    f"Use task_output(task_id='{task_id}') to check status",
                    f"Use kill_task(task_id='{task_id}') to stop it",
                ],
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to start background command: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "command": {
                    "type": "string",
                    "description": "Shell command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (for synchronous execution)",
                    "default": 60,
                },
                "run_in_background": {
                    "type": "boolean",
                    "description": "Run in background and return immediately. Use for long-running commands.",
                    "default": False,
                },
                "description": {
                    "type": "string",
                    "description": "Short description of what this command does",
                },
            },
            required=["command"],
        )
