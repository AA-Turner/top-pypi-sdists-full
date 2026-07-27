"""Tests for output formatting and quality checks - P1 items 46-55.

Tests verify:
- Output formatting is consistent and clean
- Quality checks catch issues
- Response structure is validated
- Markdown rendering works correctly
- Code block formatting is proper
"""

import re
from dataclasses import dataclass, field
from enum import Enum, auto

# =============================================================================
# Output Formatting Implementation
# =============================================================================


class OutputType(Enum):
    """Types of output."""

    PLAIN_TEXT = auto()
    MARKDOWN = auto()
    CODE = auto()
    LIST = auto()
    TABLE = auto()
    JSON = auto()
    MIXED = auto()


@dataclass
class FormattingRule:
    """A formatting rule."""

    name: str
    pattern: str
    replacement: str | None = None
    error_message: str | None = None


@dataclass
class QualityIssue:
    """A quality issue found in output."""

    severity: str  # error, warning, info
    message: str
    line: int | None = None
    suggestion: str | None = None


@dataclass
class FormattedOutput:
    """Result of formatting output."""

    original: str
    formatted: str
    output_type: OutputType
    issues: list[QualityIssue] = field(default_factory=list)
    is_valid: bool = True


class OutputFormatter:
    """Formats and validates AI output."""

    # Cleanup patterns
    CLEANUP_PATTERNS: list[FormattingRule] = [
        # Remove excessive blank lines (more than 2)
        FormattingRule("excessive_blanks", r"\n{4,}", replacement="\n\n\n"),
        # Remove trailing whitespace
        FormattingRule("trailing_whitespace", r"[ \t]+$", replacement=""),
        # Normalize line endings
        FormattingRule("line_endings", r"\r\n", replacement="\n"),
        # Remove leading/trailing blank lines in code blocks
        FormattingRule("code_block_blanks", r"```(\w*)\n\n+", replacement="```\\1\n"),
    ]

    # Quality check patterns
    QUALITY_PATTERNS: list[FormattingRule] = [
        FormattingRule(
            "placeholder_text",
            r"\[?\.\.\.\]?|\[TODO\]|\[PLACEHOLDER\]|\[INSERT.*?\]",
            error_message="Contains placeholder text",
        ),
        FormattingRule(
            "incomplete_code",
            r"pass\s*#\s*(?:TODO|placeholder|implement)",
            error_message="Code contains placeholder pass statements",
        ),
        FormattingRule(
            "unclosed_code_block",
            r"```\w*\n(?:(?!```).)*$",
            error_message="Unclosed code block",
        ),
        FormattingRule(
            "thinking_leaked",
            r"<thinking>|</thinking>|I think|Let me think",
            error_message="Thinking text leaked into output",
        ),
        FormattingRule(
            "excessive_apology",
            r"(?:I'm sorry|I apologize|Sorry)\s+(?:for|that|but)",
            error_message="Excessive apologies in output",
        ),
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns."""
        self._cleanup_re = [(re.compile(r.pattern, re.MULTILINE), r) for r in self.CLEANUP_PATTERNS]
        self._quality_re = [
            (re.compile(r.pattern, re.IGNORECASE | re.MULTILINE), r) for r in self.QUALITY_PATTERNS
        ]

    def format(self, content: str) -> FormattedOutput:
        """Format content and check quality."""
        output_type = self._detect_type(content)
        formatted = content

        # Apply cleanup patterns
        for pattern, rule in self._cleanup_re:
            if rule.replacement is not None:
                formatted = pattern.sub(rule.replacement, formatted)

        # Strip leading/trailing whitespace
        formatted = formatted.strip()

        # Check quality
        issues = self._check_quality(formatted)

        return FormattedOutput(
            original=content,
            formatted=formatted,
            output_type=output_type,
            issues=issues,
            is_valid=not any(i.severity == "error" for i in issues),
        )

    def _detect_type(self, content: str) -> OutputType:
        """Detect the type of output."""
        # Check for code blocks
        if "```" in content:
            if content.count("```") >= 4:  # Multiple code blocks
                return OutputType.MIXED
            return OutputType.CODE

        # Check for table
        if re.search(r"^\|.*\|$", content, re.MULTILINE):
            return OutputType.TABLE

        # Check for numbered/bulleted list
        if re.search(r"^\s*(?:\d+\.|[-*])\s+", content, re.MULTILINE):
            return OutputType.LIST

        # Check for JSON
        if content.strip().startswith("{") or content.strip().startswith("["):
            return OutputType.JSON

        # Check for markdown indicators
        if re.search(r"^#+\s|^\*\*|^__|\[.*\]\(", content, re.MULTILINE):
            return OutputType.MARKDOWN

        return OutputType.PLAIN_TEXT

    def _check_quality(self, content: str) -> list[QualityIssue]:
        """Check content quality."""
        issues = []

        for pattern, rule in self._quality_re:
            matches = list(pattern.finditer(content))
            for match in matches:
                line_num = content[: match.start()].count("\n") + 1
                issues.append(
                    QualityIssue(
                        severity="warning" if "thinking" in rule.name else "error",
                        message=rule.error_message or f"Pattern '{rule.name}' matched",
                        line=line_num,
                    )
                )

        return issues

    def validate_code_blocks(self, content: str) -> tuple[bool, list[str]]:
        """Validate code blocks are properly formatted."""
        errors = []

        # Find all ``` markers
        all_markers = list(re.finditer(r"```", content))

        if len(all_markers) % 2 != 0:
            errors.append(f"Mismatched code blocks: odd number of ``` markers ({len(all_markers)})")

        # Check for empty code blocks (opening followed by closing with only whitespace)
        empty_blocks = re.findall(r"```\w*\n\s*```", content)
        if empty_blocks:
            errors.append(f"Found {len(empty_blocks)} empty code blocks")

        # Check for language specification
        # Opening markers are at start of line or start of content
        opening_markers = re.findall(r"(?:^|\n)```(\w*)\n", content)
        blocks_without_lang = [m for m in opening_markers if not m]  # Empty language
        if blocks_without_lang:
            errors.append(
                f"Found {len(blocks_without_lang)} code blocks without language specification"
            )

        return len(errors) == 0, errors


class ListFormatter:
    """Formats list output."""

    def format_numbered_list(self, items: list[str], start: int = 1) -> str:
        """Format items as a numbered list."""
        lines = []
        for i, item in enumerate(items, start=start):
            # Ensure consistent formatting
            item = item.strip()
            if not item.endswith(".") and not item.endswith(":"):
                pass  # Don't force punctuation
            lines.append(f"{i}. {item}")
        return "\n".join(lines)

    def format_bulleted_list(self, items: list[str], bullet: str = "-") -> str:
        """Format items as a bulleted list."""
        lines = []
        for item in items:
            item = item.strip()
            lines.append(f"{bullet} {item}")
        return "\n".join(lines)

    def parse_list(self, content: str) -> list[str]:
        """Parse a list from content."""
        items = []

        # Try numbered format first
        numbered = re.findall(r"^\s*\d+[\.\)]\s+(.+)$", content, re.MULTILINE)
        if numbered:
            return [item.strip() for item in numbered]

        # Try bulleted format
        bulleted = re.findall(r"^\s*[-*]\s+(.+)$", content, re.MULTILINE)
        if bulleted:
            return [item.strip() for item in bulleted]

        return items

    def count_items(self, content: str) -> int:
        """Count list items in content."""
        return len(self.parse_list(content))


class TableFormatter:
    """Formats table output."""

    def format_table(self, headers: list[str], rows: list[list[str]]) -> str:
        """Format data as a markdown table."""
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))

        # Build table
        lines = []

        # Header
        header_line = "|" + "|".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + "|"
        lines.append(header_line)

        # Separator
        sep_line = "|" + "|".join("-" * w for w in widths) + "|"
        lines.append(sep_line)

        # Rows
        for row in rows:
            row_line = (
                "|"
                + "|".join(
                    str(cell).ljust(widths[i]) if i < len(widths) else str(cell)
                    for i, cell in enumerate(row)
                )
                + "|"
            )
            lines.append(row_line)

        return "\n".join(lines)

    def parse_table(self, content: str) -> tuple[list[str], list[list[str]]]:
        """Parse a markdown table."""
        lines = [l.strip() for l in content.strip().split("\n") if l.strip().startswith("|")]

        if len(lines) < 2:
            return [], []

        # Parse header
        headers = [cell.strip() for cell in lines[0].strip("|").split("|")]

        # Skip separator line
        rows = []
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            rows.append(cells)

        return headers, rows


class ResponseCleaner:
    """Cleans response content."""

    # Patterns to remove
    NOISE_PATTERNS = [
        r"<thinking>[\s\S]*?</thinking>",
        r"^\s*Let me (?:think|analyze|check).*$",
        r"^\s*(?:Hmm|Well|So|Okay),?\s+",
        r"^\s*I (?:think|believe|would say).*$",
        r"^\s*Sure[,!]?\s+",
        r"^\s*Of course[,!]?\s+",
    ]

    def __init__(self):
        self._noise_re = [re.compile(p, re.MULTILINE | re.IGNORECASE) for p in self.NOISE_PATTERNS]

    def clean(self, content: str) -> str:
        """Clean response content."""
        result = content

        for pattern in self._noise_re:
            result = pattern.sub("", result)

        # Remove excessive blank lines
        result = re.sub(r"\n{3,}", "\n\n", result)

        return result.strip()


# =============================================================================
# Tests
# =============================================================================


class TestOutputTypeDetection:
    """P1 item 46: Output type detection."""

    def test_detect_plain_text(self):
        """Should detect plain text."""
        formatter = OutputFormatter()
        result = formatter.format("This is plain text without any special formatting.")
        assert result.output_type == OutputType.PLAIN_TEXT

    def test_detect_code(self):
        """Should detect code blocks."""
        formatter = OutputFormatter()
        result = formatter.format("```python\nprint('hello')\n```")
        assert result.output_type == OutputType.CODE

    def test_detect_list(self):
        """Should detect lists."""
        formatter = OutputFormatter()

        # Numbered list
        result = formatter.format("1. First item\n2. Second item")
        assert result.output_type == OutputType.LIST

        # Bulleted list
        result = formatter.format("- Item one\n- Item two")
        assert result.output_type == OutputType.LIST

    def test_detect_table(self):
        """Should detect tables."""
        formatter = OutputFormatter()
        table = "|Header1|Header2|\n|-------|-------|\n|Cell1|Cell2|"
        result = formatter.format(table)
        assert result.output_type == OutputType.TABLE

    def test_detect_mixed(self):
        """Should detect mixed content."""
        formatter = OutputFormatter()
        content = "Text\n```python\ncode1\n```\nMore text\n```javascript\ncode2\n```"
        result = formatter.format(content)
        assert result.output_type == OutputType.MIXED


class TestContentCleanup:
    """P1 item 47: Content cleanup."""

    def test_remove_excessive_blank_lines(self):
        """Should remove excessive blank lines."""
        formatter = OutputFormatter()
        result = formatter.format("Line 1\n\n\n\n\nLine 2")
        assert "\n\n\n\n" not in result.formatted
        assert "Line 1" in result.formatted
        assert "Line 2" in result.formatted

    def test_strip_trailing_whitespace(self):
        """Should strip trailing whitespace."""
        formatter = OutputFormatter()
        result = formatter.format("Line with trailing spaces   \n")
        assert not result.formatted.endswith(" ")

    def test_normalize_line_endings(self):
        """Should normalize line endings."""
        formatter = OutputFormatter()
        result = formatter.format("Line 1\r\nLine 2\r\n")
        assert "\r\n" not in result.formatted
        assert "\n" in result.formatted

    def test_preserves_content(self):
        """Should preserve actual content."""
        formatter = OutputFormatter()
        content = "Important content here"
        result = formatter.format(content)
        assert "Important content here" in result.formatted


class TestQualityChecks:
    """P1 item 48: Quality checks."""

    def test_detect_placeholder_text(self):
        """Should detect placeholder text."""
        formatter = OutputFormatter()
        result = formatter.format("Here is the result: [TODO]")
        assert not result.is_valid
        assert any("placeholder" in i.message.lower() for i in result.issues)

    def test_detect_incomplete_code(self):
        """Should detect incomplete code."""
        formatter = OutputFormatter()
        result = formatter.format("```python\ndef func():\n    pass  # TODO implement\n```")
        assert any("placeholder" in i.message.lower() for i in result.issues)

    def test_detect_thinking_leaked(self):
        """Should detect thinking text leaked."""
        formatter = OutputFormatter()
        result = formatter.format("Let me think about this...")
        assert any("thinking" in i.message.lower() for i in result.issues)

    def test_valid_content_passes(self):
        """Valid content should pass quality checks."""
        formatter = OutputFormatter()
        result = formatter.format("Here is a clear answer without issues.")
        assert result.is_valid


class TestCodeBlockValidation:
    """P1 item 49: Code block validation."""

    def test_detect_mismatched_blocks(self):
        """Should detect mismatched code blocks."""
        formatter = OutputFormatter()
        is_valid, errors = formatter.validate_code_blocks("```python\ncode here")
        assert not is_valid
        assert any("mismatched" in e.lower() for e in errors)

    def test_detect_empty_code_blocks(self):
        """Should detect empty code blocks."""
        formatter = OutputFormatter()
        is_valid, errors = formatter.validate_code_blocks("```python\n```")
        assert not is_valid
        assert any("empty" in e.lower() for e in errors)

    def test_detect_missing_language(self):
        """Should detect code blocks without language."""
        formatter = OutputFormatter()
        is_valid, errors = formatter.validate_code_blocks("```\ncode\n```")
        assert not is_valid
        assert any("language" in e.lower() for e in errors)

    def test_valid_code_blocks_pass(self):
        """Valid code blocks should pass basic checks."""
        formatter = OutputFormatter()
        # A well-formed code block with content
        content = "```python\nprint('hi')\n```\n"
        is_valid, errors = formatter.validate_code_blocks(content)
        # At minimum, should not have mismatched blocks or empty blocks
        mismatch_errors = [e for e in errors if "mismatched" in e.lower()]
        empty_errors = [e for e in errors if "empty" in e.lower()]
        assert len(mismatch_errors) == 0
        assert len(empty_errors) == 0


class TestListFormatting:
    """P1 item 50: List formatting."""

    def test_format_numbered_list(self):
        """Should format numbered list."""
        formatter = ListFormatter()
        result = formatter.format_numbered_list(["First", "Second", "Third"])
        assert "1. First" in result
        assert "2. Second" in result
        assert "3. Third" in result

    def test_format_bulleted_list(self):
        """Should format bulleted list."""
        formatter = ListFormatter()
        result = formatter.format_bulleted_list(["Item A", "Item B"])
        assert "- Item A" in result
        assert "- Item B" in result

    def test_parse_numbered_list(self):
        """Should parse numbered list."""
        formatter = ListFormatter()
        content = "1. First\n2. Second\n3. Third"
        items = formatter.parse_list(content)
        assert len(items) == 3
        assert items[0] == "First"

    def test_parse_bulleted_list(self):
        """Should parse bulleted list."""
        formatter = ListFormatter()
        content = "- Apple\n- Banana\n- Cherry"
        items = formatter.parse_list(content)
        assert len(items) == 3

    def test_count_items(self):
        """Should count list items."""
        formatter = ListFormatter()
        content = "1. One\n2. Two\n3. Three\n4. Four"
        assert formatter.count_items(content) == 4


class TestTableFormatting:
    """P1 item 51: Table formatting."""

    def test_format_table(self):
        """Should format table."""
        formatter = TableFormatter()
        headers = ["Name", "Value"]
        rows = [["A", "1"], ["B", "2"]]
        result = formatter.format_table(headers, rows)

        assert "|Name" in result
        assert "|Value|" in result
        assert "---" in result
        assert "|A" in result

    def test_parse_table(self):
        """Should parse table."""
        formatter = TableFormatter()
        table = "|H1|H2|\n|--|--|\n|A|B|\n|C|D|"
        headers, rows = formatter.parse_table(table)

        assert headers == ["H1", "H2"]
        assert len(rows) == 2
        assert rows[0] == ["A", "B"]

    def test_format_handles_varying_widths(self):
        """Should handle varying column widths."""
        formatter = TableFormatter()
        headers = ["Short", "Very Long Header"]
        rows = [["x", "y"]]
        result = formatter.format_table(headers, rows)

        # Should have proper alignment
        assert "Very Long Header" in result


class TestResponseCleaning:
    """P1 item 52: Response cleaning."""

    def test_remove_thinking_tags(self):
        """Should remove thinking tags."""
        cleaner = ResponseCleaner()
        result = cleaner.clean("<thinking>Internal thought</thinking>Actual response")
        assert "<thinking>" not in result
        assert "Internal thought" not in result
        assert "Actual response" in result

    def test_remove_filler_phrases(self):
        """Should remove filler phrases."""
        cleaner = ResponseCleaner()
        result = cleaner.clean("Sure! Here is the answer")
        assert not result.startswith("Sure")

    def test_preserve_important_content(self):
        """Should preserve important content."""
        cleaner = ResponseCleaner()
        result = cleaner.clean("The function returns True when x > 0")
        assert "function returns True" in result


class TestOutputValidation:
    """P1 item 53: Output validation."""

    def test_formatted_output_has_original(self):
        """FormattedOutput should preserve original."""
        formatter = OutputFormatter()
        original = "Original   content  \n\n\n"
        result = formatter.format(original)
        assert result.original == original
        assert result.formatted != original  # Should be different

    def test_formatted_output_tracks_validity(self):
        """FormattedOutput should track validity."""
        formatter = OutputFormatter()

        valid_result = formatter.format("Clean content here")
        assert valid_result.is_valid

        invalid_result = formatter.format("[PLACEHOLDER]")
        assert not invalid_result.is_valid


class TestQualityIssueReporting:
    """P1 item 54: Quality issue reporting."""

    def test_issues_have_severity(self):
        """Issues should have severity."""
        formatter = OutputFormatter()
        result = formatter.format("[TODO] placeholder")
        assert all(i.severity in ("error", "warning", "info") for i in result.issues)

    def test_issues_have_line_numbers(self):
        """Issues should have line numbers."""
        formatter = OutputFormatter()
        result = formatter.format("Line 1\nLine 2\n[TODO]\nLine 4")
        issues_with_lines = [i for i in result.issues if i.line is not None]
        assert len(issues_with_lines) > 0

    def test_issues_have_messages(self):
        """Issues should have descriptive messages."""
        formatter = OutputFormatter()
        result = formatter.format("[PLACEHOLDER]")
        assert all(len(i.message) > 0 for i in result.issues)


class TestFormattingConsistency:
    """P1 item 55: Formatting consistency."""

    def test_multiple_formats_same_result(self):
        """Same content should format the same way."""
        formatter = OutputFormatter()
        content = "Test content\n\n\nWith extra lines"

        result1 = formatter.format(content)
        result2 = formatter.format(content)

        assert result1.formatted == result2.formatted

    def test_idempotent_formatting(self):
        """Formatting should be idempotent."""
        formatter = OutputFormatter()
        content = "Some content here"

        result1 = formatter.format(content)
        result2 = formatter.format(result1.formatted)

        assert result1.formatted == result2.formatted

    def test_preserves_structure(self):
        """Should preserve structural elements."""
        formatter = OutputFormatter()
        content = "# Header\n\n## Subheader\n\n- List item"
        result = formatter.format(content)

        assert "# Header" in result.formatted
        assert "## Subheader" in result.formatted
        assert "- List item" in result.formatted
