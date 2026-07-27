"""
Follow-Through Validation for SAGE - Items 121-130 from Roadmap P0.

This module provides validation to ensure the model follows through on its commitments.
"""

from __future__ import annotations

import re
from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from sage.core.p0_request_classification import ClassifiedRequestV2


class FollowThroughValidator:
    """
    Items 121-130: Validates that the model follows through on commitments.
    """

    # Item 121: Self-promise patterns
    PROMISE_PATTERNS: ClassVar[list[str]] = [
        r"I\s+will\s+(?:list|provide|identify|create)\s+(\d+)",
        r"Here\s+(?:are|is)\s+(\d+)\s+(?:things?|items?|improvements?)",
        r"(?:listing|providing)\s+(\d+)\s+(?:things?|items?)",
    ]

    def __init__(self):
        self._promise_re = [re.compile(p, re.IGNORECASE) for p in self.PROMISE_PATTERNS]

    def validate(
        self, response: str, classification: ClassifiedRequestV2 | None = None
    ) -> tuple[bool, list[str]]:
        """
        Validate follow-through on promises.
        """
        issues = []

        # Item 121-122: Check self-promises
        promised_count = None
        for pattern in self._promise_re:
            match = pattern.search(response)
            if match:
                promised_count = int(match.group(1))
                break

        # Item 122: Count actual items
        actual_count = len(re.findall(r"^\s*\d+[\.\)]\s+", response, re.MULTILINE))

        if promised_count and actual_count < promised_count:
            issues.append(f"Promised {promised_count} items but only provided {actual_count}")

        # Item 123-125: Check for premature conclusion
        premature_endings = [
            r"(?:that's|those\s+are)\s+(?:all|the\s+main)\s+(?:items?|things?)",
            r"I\s+(?:hope|believe)\s+this\s+(?:helps|covers)",
            r"let\s+me\s+know\s+if\s+you\s+(?:need|want)\s+more",
        ]

        # Use either quantity_required or min_items for the target
        quantity_required = getattr(classification, 'quantity_required', 0) if classification else 0
        min_items = getattr(classification, 'min_items', 0) if classification else 0
        target_items = quantity_required or min_items

        for pattern in premature_endings:
            if re.search(pattern, response, re.IGNORECASE):
                if target_items and actual_count < target_items:
                    issues.append(
                        f"Premature conclusion at {actual_count} items (need {target_items})"
                    )
                    break

        # Item 126-127: Check completion status
        if min_items > 0:
            completion_pct = (actual_count / min_items) * 100
            if completion_pct < 90:
                issues.append(
                    f"Task only {completion_pct:.0f}% complete "
                    f"({actual_count}/{min_items} items)"
                )

        return len(issues) == 0, issues
