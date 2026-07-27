"""
Response generation and validation for SAGE - Fixes P2 issues 41-60.

P2-41: Vague step descriptions
P2-42: Missing line number references
P2-43: No code examples from actual codebase
P2-44: Hypothetical over actual
P2-46: Nested thinking without action
P2-47: Repetitive disclaimers
P2-48: No progress tracking
P2-53: Excessive token usage
P2-54: No concrete deliverables
P2-55: Overuse of placeholders
P2-56: No validation of own output

This module ensures responses are concrete, actionable, and grounded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar

from sage.core.list_generator import extract_list_item_count
from sage.core.request_classifier import ClassifiedRequest, OutputFormat, RequestType


@dataclass
class ResponseQualityIssue:
    """A quality issue found in a response."""

    severity: str  # ERROR, WARNING, INFO
    category: str  # vagueness, ungrounded, format, etc.
    message: str
    location: str | None = None  # Where in response
    suggestion: str | None = None  # How to fix


@dataclass
class ResponseValidationResult:
    """Result of validating a response."""

    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: list[ResponseQualityIssue] = field(default_factory=list)

    # Metrics
    item_count: int = 0
    file_references: int = 0
    verified_references: int = 0
    code_blocks: int = 0
    line_references: int = 0

    # Content analysis
    has_priority_ranking: bool = False
    has_concrete_actions: bool = False
    has_file_paths: bool = False
    has_code_examples: bool = False

    def get_error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "ERROR")

    def get_warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "WARNING")


class ResponseQualityValidator:
    """
    Validates response quality against requirements.

    Fixes:
    - P2-41 to P2-60: Various response quality issues
    """

    # Patterns indicating vague/placeholder content
    VAGUE_PATTERNS: ClassVar[list[tuple[str, str]]] = [
        (r"\b(conceptual|hypothetical)\b", "Uses hypothetical language"),
        (r"\b(would|could|might|should)\s+(?:be|have|need)", "Uses conditional language"),
        (r"\bin\s+a\s+real\s+scenario\b", "References 'real scenario'"),
        (r"\bfor\s+demonstration\s+purposes\b", "Uses demonstration disclaimer"),
        (r"\bassum(?:e|ing|ption)\b", "Makes assumptions instead of verifying"),
        (r"#\s*(?:TODO|FIXME|PLACEHOLDER)", "Contains placeholder comments"),
        (r"pass\s*#", "Contains pass with comment placeholder"),
        (r"\.\.\.\s*$", "Truncated with ellipsis"),
        (r"\[\s*\.\.\.\s*\]", "Contains [...] placeholder"),
    ]

    # Patterns indicating concrete content
    CONCRETE_PATTERNS: ClassVar[list[tuple[str, str]]] = [
        (r"`[a-zA-Z0-9_/\-]+\.(?:py|js|ts|json|yaml|yml|md|toml)`", "file_reference"),
        (r"[a-zA-Z0-9_/\-]+\.(?:py|js|ts|json|yaml|yml|md|toml):\d+", "line_reference"),
        (r"^\d+[\.\)]\s+", "numbered_item"),
        (r"^\|[^|]+\|", "table_row"),
        (r"```\w*\n", "code_block"),
        (r"\bP[0-4]\b|\b(?:CRITICAL|HIGH|MEDIUM|LOW)\b", "priority"),
    ]

    # Excessive patterns to flag
    EXCESSIVE_PATTERNS: ClassVar[list[tuple[str, str]]] = [
        (r"<thinking>[\s\S]*?</thinking>", "thinking_block"),
        (r"(?:Let me|I will|I am going to)\s+", "announcement"),
        (r"(?:As mentioned|As I said|As noted)\s+", "redundant_reference"),
    ]

    def validate(
        self,
        response: str,
        classification: ClassifiedRequest,
        verified_files: set[str] | None = None,
    ) -> ResponseValidationResult:
        """
        Validate a response against quality criteria.

        Args:
            response: The generated response
            classification: The request classification
            verified_files: Set of verified file paths

        Returns:
            ResponseValidationResult with issues and metrics
        """
        issues = []
        verified_files = verified_files or set()

        # Check for vague patterns
        vague_issues = self._check_vague_patterns(response)
        issues.extend(vague_issues)

        # Count concrete elements
        metrics = self._count_concrete_elements(response)

        # Check format matches expected
        format_issues = self._check_format(response, classification)
        issues.extend(format_issues)

        # Check quantity requirements
        if classification.quantity_required:
            if metrics["item_count"] < classification.quantity_required:
                issues.append(
                    ResponseQualityIssue(
                        severity="ERROR",
                        category="quantity",
                        message=f"Response has {metrics['item_count']} items but {classification.quantity_required} required",
                        suggestion=f"Add {classification.quantity_required - metrics['item_count']} more items",
                    )
                )

        # Check priority ranking
        if classification.priority_ranking and not metrics["has_priority"]:
            issues.append(
                ResponseQualityIssue(
                    severity="WARNING",
                    category="format",
                    message="Response lacks priority ranking",
                    suggestion="Add P0/P1/P2/P3 or CRITICAL/HIGH/MEDIUM/LOW labels",
                )
            )

        # Check file references are verified
        if classification.must_include_file_paths:
            unverified = self._check_file_references(response, verified_files)
            for path in unverified:
                issues.append(
                    ResponseQualityIssue(
                        severity="ERROR",
                        category="ungrounded",
                        message=f"Unverified file reference: {path}",
                        suggestion="Verify file exists with READ: or SEARCH: before referencing",
                    )
                )

        # Check read-only constraint
        if classification.read_only and self._contains_file_blocks(response):
            issues.append(
                ResponseQualityIssue(
                    severity="ERROR",
                    category="constraint",
                    message="Response contains FILE: blocks but request is read-only",
                    suggestion="Remove FILE: blocks and provide analysis only",
                )
            )

        # Check for excessive announcements
        excessive_issues = self._check_excessive_patterns(response)
        issues.extend(excessive_issues)

        # Calculate score
        error_count = sum(1 for i in issues if i.severity == "ERROR")
        warning_count = sum(1 for i in issues if i.severity == "WARNING")
        score = max(0.0, 1.0 - (error_count * 0.2) - (warning_count * 0.05))

        return ResponseValidationResult(
            is_valid=error_count == 0,
            score=score,
            issues=issues,
            item_count=metrics["item_count"],
            file_references=metrics["file_references"],
            verified_references=len(verified_files),
            code_blocks=metrics["code_blocks"],
            line_references=metrics["line_references"],
            has_priority_ranking=metrics["has_priority"],
            has_concrete_actions=metrics["item_count"] > 0 or metrics["code_blocks"] > 0,
            has_file_paths=metrics["file_references"] > 0,
            has_code_examples=metrics["code_blocks"] > 0,
        )

    def _check_vague_patterns(self, response: str) -> list[ResponseQualityIssue]:
        """Check for vague/placeholder patterns."""
        issues = []

        for pattern, description in self.VAGUE_PATTERNS:
            matches = list(re.finditer(pattern, response, re.IGNORECASE | re.MULTILINE))
            if matches:
                # Only report first few occurrences
                for match in matches[:3]:
                    context = response[max(0, match.start() - 20) : match.end() + 20]
                    issues.append(
                        ResponseQualityIssue(
                            severity="WARNING",
                            category="vagueness",
                            message=description,
                            location=f"...{context}...",
                        )
                    )

        return issues

    def _count_concrete_elements(self, response: str) -> dict[str, Any]:
        """Count concrete elements in response."""
        metrics = {
            "item_count": 0,
            "file_references": 0,
            "line_references": 0,
            "code_blocks": 0,
            "has_priority": False,
        }

        # Use unified extraction for consistent counting across SAGE
        # This is the CANONICAL function - all item counting should use this
        metrics["item_count"] = extract_list_item_count(response)

        # Count file references
        file_refs = re.findall(
            r"`([^`]+\.(?:py|js|ts|json|yaml|yml|md|toml|go|rs|java))`", response
        )
        metrics["file_references"] = len(set(file_refs))

        # Count line references
        line_refs = re.findall(r"\.(?:py|js|ts):\d+", response)
        metrics["line_references"] = len(line_refs)

        # Count code blocks
        metrics["code_blocks"] = len(re.findall(r"```\w*\n", response))

        # Check for priority indicators
        metrics["has_priority"] = bool(
            re.search(r"\bP[0-4]\b|\b(?:CRITICAL|HIGH|MEDIUM|LOW)\b", response, re.IGNORECASE)
        )

        return metrics

    def _check_format(
        self, response: str, classification: ClassifiedRequest
    ) -> list[ResponseQualityIssue]:
        """Check if response format matches expected."""
        issues = []

        if classification.expected_format == OutputFormat.MARKDOWN_TABLE:
            if "|" not in response or response.count("|") < 6:
                issues.append(
                    ResponseQualityIssue(
                        severity="WARNING",
                        category="format",
                        message="Expected markdown table format",
                        suggestion="Format results as | Column1 | Column2 | table",
                    )
                )

        elif classification.expected_format == OutputFormat.MARKDOWN_LIST:
            if not re.search(r"^\s*[\d\-\*]\s+", response, re.MULTILINE):
                issues.append(
                    ResponseQualityIssue(
                        severity="WARNING",
                        category="format",
                        message="Expected markdown list format",
                        suggestion="Format results as numbered (1. 2. 3.) or bulleted (- or *) list",
                    )
                )

        elif classification.expected_format == OutputFormat.CODE_FILES:
            if "FILE:" not in response and "```" not in response:
                issues.append(
                    ResponseQualityIssue(
                        severity="ERROR",
                        category="format",
                        message="Expected code files but none found",
                        suggestion="Include FILE: blocks or code fences",
                    )
                )

        return issues

    def _check_file_references(self, response: str, verified_files: set[str]) -> list[str]:
        """Check file references against verified files."""
        # Extract all file references
        refs = set()

        # Backtick paths
        refs.update(
            re.findall(r"`([^`]+\.(?:py|js|ts|json|yaml|yml|md|toml|go|rs|java))`", response)
        )

        # Extract from FILE block markers
        refs.update(re.findall(r"FILE:\s*`([^`]+)`", response))

        # path:line references
        for match in re.finditer(
            r"([a-zA-Z0-9_/\-]+\.(?:py|js|ts|json|yaml|yml|md|toml|go|rs|java)):\d+", response
        ):
            refs.add(match.group(1))

        return [r for r in refs if r not in verified_files]

    def _contains_file_blocks(self, response: str) -> bool:
        """Check if response contains FILE: blocks."""
        return bool(re.search(r"^FILE:\s*`", response, re.MULTILINE))

    def _check_excessive_patterns(self, response: str) -> list[ResponseQualityIssue]:
        """Check for excessive/redundant patterns."""
        issues = []

        for pattern, name in self.EXCESSIVE_PATTERNS:
            matches = list(re.finditer(pattern, response, re.IGNORECASE))
            if len(matches) > 3:
                issues.append(
                    ResponseQualityIssue(
                        severity="INFO",
                        category="verbosity",
                        message=f"Excessive {name} ({len(matches)} occurrences)",
                        suggestion="Reduce verbosity and get to the point",
                    )
                )

        return issues


class ConcreteResponseBuilder:
    """
    Builds responses with concrete, verified content.

    Fixes:
    - P2-41: Vague step descriptions -> Concrete actions
    - P2-42: Missing line references -> Includes file:line
    - P2-43: No code examples -> Includes real code snippets
    - P2-54: No deliverables -> Explicit deliverables section
    """

    def __init__(self, verified_files: set[str], file_contents: dict[str, str]):
        self.verified_files = verified_files
        self.file_contents = file_contents

    def build_item(
        self,
        item_num: int,
        title: str,
        description: str,
        file_path: str | None = None,
        line_number: int | None = None,
        _code_snippet: str | None = None,
        priority: str | None = None,
        impact: str | None = None,
    ) -> str:
        """Build a single concrete item."""
        parts = []

        # Header with number and title
        priority_str = f" ({priority})" if priority else ""
        parts.append(f"| {item_num} | **{title}**{priority_str} |")

        # File reference
        if file_path:
            if file_path in self.verified_files:
                if line_number:
                    parts.append(f" `{file_path}:{line_number}` |")
                else:
                    parts.append(f" `{file_path}` |")
            else:
                parts.append(f" {file_path} (unverified) |")
        else:
            parts.append(" - |")

        # Description
        parts.append(f" {description} |")

        # Impact
        if impact:
            parts.append(f" {impact} |")

        return " ".join(parts)

    def build_table_header(self, columns: list[str]) -> str:
        """Build markdown table header."""
        header = "| " + " | ".join(columns) + " |"
        separator = "| " + " | ".join(["---"] * len(columns)) + " |"
        return f"{header}\n{separator}"

    def build_code_reference(
        self, file_path: str, start_line: int, end_line: int, description: str = ""
    ) -> str:
        """Build a code reference with actual content."""
        if file_path not in self.file_contents:
            return f"<!-- File {file_path} not loaded -->"

        content = self.file_contents[file_path]
        lines = content.splitlines()

        if start_line > len(lines):
            return f"<!-- Line {start_line} out of range for {file_path} -->"

        snippet = "\n".join(lines[start_line - 1 : end_line])
        extension = Path(file_path).suffix[1:]  # Remove leading dot

        desc_line = f"# {description}\n" if description else ""

        return f"""
```{extension}
{desc_line}# {file_path}:{start_line}-{end_line}
{snippet}
```
"""


class ProgressTracker:
    """
    Tracks progress during multi-item response generation.

    Fixes:
    - P2-48: No progress tracking
    """

    def __init__(self, total_items: int):
        self.total_items = total_items
        self.current_item = 0
        self.completed_items: list[int] = []
        self.failed_items: list[int] = []

    def start_item(self, item_num: int) -> str:
        """Mark an item as started."""
        self.current_item = item_num
        return f"--- Item {item_num}/{self.total_items} [IN PROGRESS] ---"

    def complete_item(self, item_num: int) -> str:
        """Mark an item as completed."""
        self.completed_items.append(item_num)
        return f"--- Item {item_num}/{self.total_items} [DONE] ---"

    def fail_item(self, item_num: int, reason: str = "") -> str:
        """Mark an item as failed."""
        self.failed_items.append(item_num)
        reason_str = f": {reason}" if reason else ""
        return f"--- Item {item_num}/{self.total_items} [FAILED{reason_str}] ---"

    def get_progress(self) -> float:
        """Get progress percentage."""
        return (len(self.completed_items) / self.total_items) * 100 if self.total_items else 0

    def get_summary(self) -> str:
        """Get progress summary."""
        return (
            f"Progress: {len(self.completed_items)}/{self.total_items} completed "
            f"({self.get_progress():.1f}%), {len(self.failed_items)} failed"
        )


# Convenience functions


def validate_response(
    response: str, classification: ClassifiedRequest, verified_files: set[str] | None = None
) -> ResponseValidationResult:
    """Validate a response against quality criteria."""
    validator = ResponseQualityValidator()
    return validator.validate(response, classification, verified_files)


def check_response_quality(response: str) -> dict[str, Any]:
    """Quick quality check on a response."""
    validator = ResponseQualityValidator()

    # Use a minimal classification for basic checks
    minimal = ClassifiedRequest(
        original_request="",
        request_type=RequestType.ANALYSIS,
        expected_format=OutputFormat.MARKDOWN_LIST,
    )

    result = validator.validate(response, minimal)

    return {
        "score": result.score,
        "is_valid": result.is_valid,
        "error_count": result.get_error_count(),
        "warning_count": result.get_warning_count(),
        "item_count": result.item_count,
        "file_references": result.file_references,
        "has_priority_ranking": result.has_priority_ranking,
        "issues": [{"severity": i.severity, "message": i.message} for i in result.issues],
    }
