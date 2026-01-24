"""File prioritization utilities for PR review analysis."""

from typing import Any, ClassVar, Dict, List, Tuple


class FilePrioritizer:
    """Intelligent file prioritization for PR analysis."""

    # File patterns to deprioritize or skip
    LOW_PRIORITY_PATTERNS: ClassVar[List[str]] = [
        ".lock",
        "package-lock.json",
        "yarn.lock",
        "Pipfile.lock",
        ".generated",
        ".gen.",
        "_generated.",
        "generated_",
        "node_modules/",
        "__pycache__/",
        ".pytest_cache/",
        ".git/",
        ".DS_Store",
        "Thumbs.db",
        ".min.js",
        ".min.css",
        ".bundle.js",
        ".map",
        ".sourcemap",
    ]

    # File patterns that are typically high-priority for analysis
    HIGH_PRIORITY_PATTERNS: ClassVar[List[str]] = [
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".go",
        ".rs",
        ".rb",
        ".php",
        "Dockerfile",
        "docker-compose",
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        ".yml",
        ".yaml",
        ".json",
        ".toml",
    ]

    @classmethod
    def basic_priority(cls, files: List[Dict[str, Any]], max_files: int = 10) -> Tuple[List[Dict[str, Any]], int]:
        """
        Basic file prioritization - simple filtering and sorting by change volume.

        Args:
            files: List of file dictionaries from GitHub API
            max_files: Maximum number of files to analyze

        Returns:
            Tuple of (prioritized_files, skipped_count)
        """
        # Filter out obvious low-value files
        filtered_files = [f for f in files if cls._is_analyzable_file(f["filename"])]

        # Sort by total changes (additions + deletions)
        sorted_files = sorted(filtered_files, key=lambda x: x.get("additions", 0) + x.get("deletions", 0), reverse=True)

        selected = sorted_files[:max_files]
        skipped = len(files) - len(selected)

        return selected, skipped

    @classmethod
    def smart_priority(cls, files: List[Dict[str, Any]], max_files: int = 10) -> Tuple[List[Dict[str, Any]], int]:
        """
        Advanced file prioritization - considers file types, status, and change patterns.

        Args:
            files: List of file dictionaries from GitHub API
            max_files: Maximum number of files to analyze

        Returns:
            Tuple of (prioritized_files, skipped_count)
        """
        # Separate files by status and filter
        analyzable_files = [f for f in files if cls._is_analyzable_file(f["filename"])]

        new_files = [f for f in analyzable_files if f.get("status") == "added"]
        modified_files = [f for f in analyzable_files if f.get("status") == "modified"]
        renamed_files = [f for f in analyzable_files if f.get("status") == "renamed"]

        priority_files = []

        # 1. New files first (most likely to have issues)
        new_by_priority = sorted(new_files, key=cls._file_importance_score, reverse=True)
        priority_files.extend(new_by_priority)

        # 2. Modified files by importance score (combines change volume + file type)
        modified_by_priority = sorted(modified_files, key=cls._file_importance_score, reverse=True)
        priority_files.extend(modified_by_priority)

        # 3. Renamed files (usually lower priority)
        renamed_by_priority = sorted(renamed_files, key=cls._file_importance_score, reverse=True)
        priority_files.extend(renamed_by_priority)

        # Select top files
        selected = priority_files[:max_files]
        skipped = len(files) - len(selected)

        return selected, skipped

    @classmethod
    def get_analysis_summary(cls, all_files: List[Dict[str, Any]], analyzed_files: List[Dict[str, Any]]) -> str:
        """
        Generate a summary of file analysis coverage.

        Args:
            all_files: All files in the PR
            analyzed_files: Files that were analyzed in detail

        Returns:
            Formatted summary string
        """
        total_count = len(all_files)
        analyzed_count = len(analyzed_files)
        skipped_count = total_count - analyzed_count

        summary = f"""**File Analysis Coverage:**
- Analyzed in detail: {analyzed_count} files
- Total files in PR: {total_count} files"""

        if skipped_count > 0:
            skipped_files = [f for f in all_files if f not in analyzed_files]
            skipped_names = [f["filename"] for f in skipped_files[:5]]  # Show first 5

            summary += f"""
- Skipped: {skipped_count} files (low-priority, generated, or minimal changes)"""

            if skipped_count <= 5:
                summary += f"""
- Skipped files: {", ".join(skipped_names)}"""
            else:
                summary += f"""
- Example skipped files: {", ".join(skipped_names)}, and {skipped_count - 5} others"""

        summary += f"""

**Analyzed files:**
{chr(10).join([f"- {f['filename']} (+{f.get('additions', 0)} -{f.get('deletions', 0)})" for f in analyzed_files])}"""

        return summary

    @classmethod
    def _is_analyzable_file(cls, filename: str) -> bool:
        """Check if a file should be analyzed (not generated, not binary artifacts, etc.)."""
        filename_lower = filename.lower()

        # Skip files matching low-priority patterns
        for pattern in cls.LOW_PRIORITY_PATTERNS:
            if pattern in filename_lower:
                return False

        return True

    @classmethod
    def _file_importance_score(cls, file_info: Dict[str, Any]) -> float:
        """Calculate importance score for a file (higher = more important)."""
        filename = file_info["filename"]
        additions = file_info.get("additions", 0)
        deletions = file_info.get("deletions", 0)

        # Base score from change volume
        change_score = additions + deletions

        # Bonus for high-priority file types
        filename_lower = filename.lower()
        type_bonus = 0

        for pattern in cls.HIGH_PRIORITY_PATTERNS:
            if filename_lower.endswith(pattern) or pattern in filename_lower:
                type_bonus += 50
                break

        # Bonus for files that look like configuration or core logic
        if any(keyword in filename_lower for keyword in ["config", "main", "index", "init", "setup"]):
            type_bonus += 25

        # Bonus for test files (important but not as much as source)
        if any(keyword in filename_lower for keyword in ["test", "spec"]):
            type_bonus += 15

        # Penalty for very large files (might be auto-generated)
        size_penalty = 0
        if change_score > 1000:
            size_penalty = change_score * 0.1  # Reduce importance of massive changes

        return change_score + type_bonus - size_penalty
