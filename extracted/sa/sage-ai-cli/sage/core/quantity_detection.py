"""Quantity detection and parsing logic for SAGE."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class QuantityResult:
    """Result of quantity parsing with confidence and validation data."""

    quantity: int | None = None
    modifier: str | None = None  # "minimum", "maximum", "approximate"
    range_max: int | None = None
    detection_method: str = ""
    confidence: float = 0.0
    unit: str | None = None  # Unit extracted from request (e.g., "items", "things", "bugs")
    is_exact: bool = True  # Whether the quantity is exact or approximate

    @property
    def effective_quantity(self) -> int | None:
        """Get the effective quantity to use for validation."""
        return self.quantity

    def validate_against(self, actual_count: int) -> tuple[bool, str]:
        """Validate actual count against detected quantity."""
        if not self.quantity:
            return True, ""

        if self.modifier == "minimum":
            if actual_count < self.quantity:
                return False, f"Expected at least {self.quantity} items, got {actual_count}"
        elif self.modifier == "maximum":
            if actual_count > self.quantity:
                return False, f"Expected at most {self.quantity} items, got {actual_count}"
        else:
            # For approximate quantities, allow 10% variance
            variance = self.quantity * 0.1
            if actual_count < self.quantity - variance:
                return False, f"Expected ~{self.quantity} items, got only {actual_count}"

        return True, ""


class QuantityParser:
    """
    Complete quantity detection and parsing.

    Handles:
    - Numeric quantities: "100 items"
    - Spelled numbers: "hundred things" -> 100
    - Compound numbers: "one hundred fifty" -> 150
    - Hyphenated: "twenty-five" -> 25
    - Relative: "over 100", "at least 50", "more than 200"
    - Approximate: "about 100", "around fifty", "roughly 25"
    - Implicit: "dozen" -> 12, "score" -> 20, "couple" -> 2
    - Multipliers: "5x the items"
    - Ordinals: "first 10 results" -> 10
    """

    # Spelled number dictionary with all variants
    SPELLED_NUMBERS: ClassVar[dict[str, int]] = {
        # Basic numbers
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        # Special large numbers
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        # Relative quantities
        "dozen": 12,
        "score": 20,
        "gross": 144,
        # Implicit quantities
        "couple": 2,
        "pair": 2,
        "few": 3,
        "several": 5,
        "many": 10,
        "some": 5,
        "numerous": 20,
        "lots": 20,
        "plenty": 20,
    }

    # Modifier keywords
    QUANTITY_MODIFIERS: ClassVar[dict[str, str]] = {
        "over": "over",
        "at least": "at_least",
        "more than": "more_than",
        "minimum of": "minimum",
        "minimum": "minimum",
        "about": "approximate",
        "around": "approximate",
        "roughly": "approximate",
        "approximately": "approximate",
        "nearly": "approximate",
        "almost": "approximate",
        "up to": "up_to",
        "under": "under",
        "less than": "less_than",
        "fewer than": "less_than",
        "no more than": "maximum",
        "maximum of": "maximum",
    }

    # List item indicators
    LIST_INDICATORS: ClassVar[list[str]] = [
        "things",
        "items",
        "improvements",
        "issues",
        "problems",
        "suggestions",
        "recommendations",
        "changes",
        "fixes",
        "points",
        "results",
        "examples",
        "features",
        "bugs",
        "tasks",
        "steps",
        "ideas",
        "concepts",
        "errors",
        "warnings",
        "tips",
        "notes",
        "questions",
        "answers",
        "options",
        "ways",
        "methods",
        "approaches",
        "techniques",
        "patterns",
        "practices",
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for quantity detection."""
        # Modifier pattern
        modifier_parts = "|".join(re.escape(m) for m in self.QUANTITY_MODIFIERS.keys())
        self._modifiers = re.compile(rf"\b({modifier_parts})\s+", re.IGNORECASE)

        # Range patterns
        self._range_pattern = re.compile(r"\b(\d+)\s*(?:[-–]|to)\s*(\d+)\b", re.IGNORECASE)

        # Between pattern
        self._between_pattern = re.compile(r"\bbetween\s+(\d+)\s+and\s+(\d+)\b", re.IGNORECASE)

        # Multiplier patterns
        self._multiplier = re.compile(r"\b(\d+)x\s+(?:the\s+)?(?:number\s+of\s+)?", re.IGNORECASE)

        # List indicator pattern
        indicators = "|".join(self.LIST_INDICATORS)
        self._list_indicator_pattern = re.compile(rf"\b(?:{indicators})\b", re.IGNORECASE)

        # Compound spelled number patterns
        tens = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
        ones = "one|two|three|four|five|six|seven|eight|nine"
        self._compound_tens_ones = re.compile(rf"\b({tens})[- ]?({ones})\b", re.IGNORECASE)

        # "X hundred Y" pattern
        self._hundreds_pattern = re.compile(
            rf"\b({ones}|two|three|four|five|six|seven|eight|nine|ten)\s+hundred\s*(?:and\s+)?({ones}|{tens})?\b",
            re.IGNORECASE,
        )

    def parse(self, text: str) -> QuantityResult:
        """
        Parse quantity from text with full analysis.

        Returns QuantityResult with detected quantity and metadata.
        """
        text_lower = text.lower()
        result = QuantityResult()

        # Priority 1: Check for explicit numeric with modifier
        if modified := self._parse_modified_numeric(text_lower):
            return modified

        # Priority 2: Check for ranges
        if range_result := self._parse_range(text_lower):
            return range_result

        # Priority 3: Check compound spelled numbers
        if compound := self._parse_compound_spelled(text_lower):
            return compound

        # Priority 4: Check numeric with context
        if numeric := self._parse_numeric_with_context(text_lower):
            return numeric

        # Priority 5: Check single spelled numbers
        if spelled := self._parse_single_spelled(text_lower):
            return spelled

        # Priority 6: Check implicit quantities
        if implicit := self._parse_implicit(text_lower):
            return implicit

        # No quantity detected
        result.confidence = 0.0
        result.is_exact = False
        return result

    def _parse_modified_numeric(self, text: str) -> QuantityResult | None:
        """Parse modified numeric quantities like 'over 100', 'at least 50'."""
        for modifier_text, modifier_type in self.QUANTITY_MODIFIERS.items():
            pattern = rf"\b{re.escape(modifier_text)}\s+(\d+)\b"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return QuantityResult(
                    quantity=int(match.group(1)),
                    modifier=modifier_type,
                    detection_method="modified_numeric",
                    confidence=0.95,
                    is_exact=modifier_type not in ("approximate", "minimum", "maximum"),
                )
        return None

    def _parse_range(self, text: str) -> QuantityResult | None:
        """Parse range expressions like '50-100' or 'between 50 and 100'."""
        # Check "X-Y" or "X to Y"
        match = self._range_pattern.search(text)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                range_max=int(match.group(2)),
                detection_method="range",
                confidence=0.9,
                is_exact=False,
            )

        # Check "between X and Y"
        match = self._between_pattern.search(text)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                range_max=int(match.group(2)),
                detection_method="range",
                confidence=0.9,
                is_exact=False,
            )

        return None

    def _parse_compound_spelled(self, text: str) -> QuantityResult | None:
        """Parse compound spelled numbers like 'twenty-five' or 'one hundred fifty'."""
        # Check "X hundred Y"
        match = self._hundreds_pattern.search(text)
        if match:
            hundreds = self.SPELLED_NUMBERS.get(match.group(1).lower(), 0) * 100
            remainder = self.SPELLED_NUMBERS.get(match.group(2).lower(), 0) if match.group(2) else 0
            return QuantityResult(
                quantity=hundreds + remainder,
                detection_method="compound_hundreds",
                confidence=0.95,
                is_exact=True,
            )

        # Check "twenty-five" style
        match = self._compound_tens_ones.search(text)
        if match:
            tens = self.SPELLED_NUMBERS.get(match.group(1).lower(), 0)
            ones = self.SPELLED_NUMBERS.get(match.group(2).lower(), 0)
            return QuantityResult(
                quantity=tens + ones,
                detection_method="compound_tens",
                confidence=0.95,
                is_exact=True,
            )

        return None

    def _parse_numeric_with_context(self, text: str) -> QuantityResult | None:
        """Parse numeric quantities with context validation."""
        # Pattern: "100 items", "50 different things"
        pattern = r"\b(\d+)\s+(?:different\s+)?(?:" + "|".join(self.LIST_INDICATORS) + r")\b"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                detection_method="numeric_with_context",
                confidence=0.95,
                is_exact=True,
            )

        # Pattern: "list/give/provide X"
        verbs = r"list|give|provide|show|find|identify|create|generate|write"
        pattern = rf"\b(?:{verbs})\s+(\d+)\b"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                detection_method="verb_numeric",
                confidence=0.9,
                is_exact=True,
            )

        # Pattern: "first/top X"
        pattern = r"\b(?:first|top)\s+(\d+)\b"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                detection_method="ordinal_numeric",
                confidence=0.9,
                is_exact=True,
            )

        return None

    def _parse_single_spelled(self, text: str) -> QuantityResult | None:
        """Parse single spelled numbers like 'hundred' or 'fifty'."""
        # Check if text has list indicator context
        has_list_context = bool(self._list_indicator_pattern.search(text))

        for word, value in sorted(
            self.SPELLED_NUMBERS.items(), key=lambda x: -len(x[0])
        ):  # Longer words first
            if value >= 10:  # Skip small implicit quantities
                pattern = rf"\b{re.escape(word)}\b"
                if re.search(pattern, text, re.IGNORECASE):
                    return QuantityResult(
                        quantity=value,
                        detection_method="spelled_single",
                        confidence=0.9 if has_list_context else 0.7,
                        is_exact=True,
                    )

        return None

    def _parse_implicit(self, text: str) -> QuantityResult | None:
        """Parse implicit quantities like 'couple', 'few', 'several'."""
        implicit_words = [
            "couple",
            "pair",
            "few",
            "several",
            "many",
            "some",
            "numerous",
            "lots",
            "plenty",
        ]

        for word in implicit_words:
            pattern = rf"\b{word}\b"
            if re.search(pattern, text, re.IGNORECASE):
                return QuantityResult(
                    quantity=self.SPELLED_NUMBERS.get(word, 5),
                    detection_method="implicit",
                    confidence=0.6,
                    is_exact=False,
                )

        return None

