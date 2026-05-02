"""
List Format Enforcement for SAGE - Items 71-90 from Roadmap P0.

This module provides validation and enforcement for list formats in model responses.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sage.core.p0_request_classification import ClassifiedRequestV2

from sage.core.list_generator import extract_list_item_count

@dataclass
class ListValidationResult:
    """Result of list format validation."""

    is_valid: bool = True
    item_count: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    # Quality metrics
    with_file_refs: int = 0
    with_line_numbers: int = 0
    with_priority: int = 0
    duplicate_count: int = 0
    format_consistent: bool = True  # Whether all items use same format


class ListEnforcerV2:
    """
    Items 71-90: Enforces list format requirements.
    """

    def __init__(self):
        # Item 71: Numbered list pattern
        self._numbered_pattern = re.compile(r"^\s*(\d+)[\.\)]\s+", re.MULTILINE)

        # Item 72: Bullet list pattern
        self._bullet_pattern = re.compile(r"^\s*[-*]\s+", re.MULTILINE)

        # Item 79: File reference pattern
        self._file_ref_pattern = re.compile(r"`([^`]+\.\w+)(?::(\d+))?`")

        # Item 81: Priority pattern
        self._priority_pattern = re.compile(r"\b(P[0-4]|CRITICAL|HIGH|MEDIUM|LOW)\b", re.IGNORECASE)

    def validate(
        self,
        response_or_items: str | list[str],
        classification: ClassifiedRequestV2 = None,
        min_count: int = 0,
    ) -> ListValidationResult:
        """
        Items 71-90: Validate list format against requirements.
        """
        result = ListValidationResult()

        # Handle list input
        if isinstance(response_or_items, list):
            items = response_or_items
            result.item_count = len(items)

            # Check for proper numbered format
            formats_found = set()
            for item in items:
                fmt = self.detect_format(item)
                formats_found.add(fmt)

            # Check if all items have consistent format
            result.format_consistent = len(formats_found) <= 1

            # Check for numbered list validity
            numbered_count = sum(1 for item in items if re.match(r"^\s*\d+[\.\)]\s+", item))
            if numbered_count > 0 and numbered_count == len(items):
                # Check sequential numbering
                numbers = []
                for item in items:
                    m = re.match(r"^\s*(\d+)[\.\)]\s+", item)
                    if m:
                        numbers.append(int(m.group(1)))
                if numbers:
                    # Check if sequential (1, 2, 3...)
                    expected = list(range(1, len(numbers) + 1))
                    if numbers != expected:
                        result.is_valid = False
                result.is_valid = result.is_valid and numbered_count == len(items)
            elif len(items) > 0:
                result.is_valid = False

            # Detect duplicates in list
            seen = set()
            for item in items:
                # Extract text after format prefix
                cleaned = re.sub(r"^\s*(?:\d+[\.\)]|[-*•]|[a-z][\.\)])\s*", "", item, flags=re.I)
                normalized = cleaned.lower().strip()[:50]
                if normalized in seen:
                    result.duplicate_count += 1
                seen.add(normalized)

            # Check minimum count
            if min_count > 0:
                if result.item_count < min_count:
                    result.is_valid = False

            return result

        # Original string response handling
        response = response_or_items

        # Item 73: Count items using unified extraction for consistency
        result.item_count = extract_list_item_count(response)

        # Item 74: Validate minimum count
        if classification and hasattr(classification, 'min_items') and classification.min_items > 0:
            if result.item_count < classification.min_items:
                result.is_valid = False
                result.errors.append(
                    f"Only {result.item_count} items found, need {classification.min_items}"
                )

        # Item 76: Check for duplicates
        items = self._extract_item_titles(response)
        seen = set()
        for item in items:
            normalized = item.lower().strip()[:50]
            if normalized in seen:
                result.duplicate_count += 1
            seen.add(normalized)

        if result.duplicate_count > 0:
            result.warnings.append(f"Found {result.duplicate_count} duplicate items")

        # Item 79: Check file references
        file_refs = self._file_ref_pattern.findall(response)
        result.with_file_refs = len(file_refs)

        if classification and hasattr(classification, 'requires_file_refs') and classification.requires_file_refs:
            expected_refs = max(3, (classification.min_items if hasattr(classification, 'min_items') else 0) // 10)
            if result.with_file_refs < expected_refs:
                result.warnings.append(
                    f"Only {result.with_file_refs} file references, expected {expected_refs}+"
                )

        # Item 80: Check line numbers
        result.with_line_numbers = sum(1 for _, line in file_refs if line)

        if classification and hasattr(classification, 'requires_line_numbers') and classification.requires_line_numbers:
            if result.with_line_numbers < result.item_count // 2:
                result.warnings.append("Many items lack specific line number references")

        # Item 81: Check priority indicators
        priority_matches = self._priority_pattern.findall(response)
        result.with_priority = len(set(priority_matches))

        if classification and hasattr(classification, 'requires_priority_ranking') and classification.requires_priority_ranking:
            if result.with_priority < 2:
                result.warnings.append("Items lack priority ranking")

        return result

    def _extract_item_titles(self, response: str) -> list[str]:
        """Extract item titles for duplicate checking."""
        titles = []
        for line in response.split("\n"):
            match = self._numbered_pattern.match(line)
            if match:
                # Get text after the number
                title = line[match.end() :].strip()
                titles.append(title)
        return titles

    def get_continuation_prompt(
        self, classification: ClassifiedRequestV2, current_count: int
    ) -> str:
        """Item 75: Generate continuation prompt for incomplete lists."""
        min_items = getattr(classification, 'min_items', 0)
        if not min_items or current_count >= min_items:
            return ""

        remaining = min_items - current_count

        return f"""
## CONTINUATION REQUIRED

Current items: {current_count}
Target: {min_items}
Remaining needed: {remaining}

Continue the list from item {current_count + 1}.
Each item MUST:
- Be numbered ({current_count + 1}., {current_count + 2}., etc.)
- Reference a specific file path in backticks
- Include priority (P0/P1/P2/P3)
- Be unique (no duplicates of previous items)

DO NOT repeat previous items. Continue from where you left off.
""".strip()

    def detect_format(self, text: str) -> str:
        """Detect the format used in the text."""
        if self._numbered_pattern.match(text):
            return "numbered"
        if self._bullet_pattern.match(text):
            return "bullet"
        return "plain"
