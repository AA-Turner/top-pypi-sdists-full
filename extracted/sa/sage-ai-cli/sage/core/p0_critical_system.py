"""
P0 Critical System for SAGE - Integrated Items 1-130 from Roadmap P0.

This module provides the integrated system combining classification, quantity parsing,
instruction extraction, and compliance validation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sage.core.quantity_detection import QuantityParser, QuantityResult
from sage.core.p0_request_classification import (
    ClassifiedRequestV2,
    RequestClassifierV2,
    RequestTypeV2,
    PipelineTypeV2,
)
from sage.core.code_generation_blocking import CodeBlockerV2
from sage.core.list_format_enforcement import ListEnforcerV2
from sage.core.instruction_extraction import InstructionExtractor, ExtractedInstruction
from sage.core.instruction_compliance import ComplianceValidator, OutputFormatV2
from sage.core.follow_through_validation import FollowThroughValidator

@dataclass
class ProcessResult:
    """Complete result of request processing."""
    request: str
    classification: ClassifiedRequestV2
    quantity_result: QuantityResult
    instructions: list[ExtractedInstruction]
    expanded_prompt: str

class P0CriticalSystem:
    """
    Complete P0 Critical system integrating all Items 1-130.
    """

    def __init__(self):
        self.quantity_parser = QuantityParser()
        self.classifier = RequestClassifierV2()
        self.code_blocker = CodeBlockerV2()
        self.list_enforcer = ListEnforcerV2()
        self.instruction_extractor = InstructionExtractor()
        self.compliance_validator = ComplianceValidator()
        self.follow_through_validator = FollowThroughValidator()

    def process_request(self, request: str) -> tuple[ClassifiedRequestV2, str]:
        """
        Process a request and return classification + expanded prompt.
        """
        classification = self.classifier.classify(request)
        instructions = self.instruction_extractor.extract(request)
        classification.explicit_instructions = [i.content for i in instructions]
        expanded = self._build_expanded_prompt(request, classification)
        return classification, expanded

    def process(self, request: str) -> ProcessResult:
        """
        Process a request and return a comprehensive result.
        """
        quantity_result = self.quantity_parser.parse(request)
        classification = self.classifier.classify(request)
        instructions = self.instruction_extractor.extract(request)
        expanded_prompt = self._build_expanded_prompt(request, classification)
        return ProcessResult(
            request=request,
            classification=classification,
            quantity_result=quantity_result,
            instructions=instructions,
            expanded_prompt=expanded_prompt,
        )

    def validate_response(
        self, response: str, classification: ClassifiedRequestV2
    ) -> tuple[bool, list[str], str | None]:
        """
        Validate a response against all requirements.
        """
        all_errors = []

        if getattr(classification, 'strict_read_only', False):
            has_code, code_violations = self.code_blocker.check(response)
            if has_code:
                all_errors.extend(code_violations)

        if classification.request_type == RequestTypeV2.LIST_GENERATION:
            list_result = self.list_enforcer.validate(response, classification)
            all_errors.extend(list_result.errors)

        instructions = [
            ExtractedInstruction(type="must", content=i, priority=1)
            for i in getattr(classification, 'explicit_instructions', [])
        ]
        is_compliant, compliance_errors, _ = self.compliance_validator.validate(
            response, classification, instructions
        )
        all_errors.extend(compliance_errors)

        followed_through, follow_issues = self.follow_through_validator.validate(
            response, classification
        )
        all_errors.extend(follow_issues)

        continuation = None
        if classification.request_type == RequestTypeV2.LIST_GENERATION:
            item_count = len(re.findall(r"^\s*\d+[\.\)]\s+", response, re.MULTILINE))
            min_items = getattr(classification, 'min_items', 0)
            if item_count < min_items:
                continuation = self.list_enforcer.get_continuation_prompt(
                    classification, item_count
                )

        return len(all_errors) == 0, all_errors, continuation

    def _build_expanded_prompt(self, request: str, classification: ClassifiedRequestV2) -> str:
        """Build expanded prompt with all constraints."""
        parts = [request]

        if getattr(classification, 'strict_read_only', False):
            parts.append(self.code_blocker.get_blocking_prompt(classification))

        if getattr(classification, 'requires_exploration', False):
            parts.append("""
## MANDATORY EXPLORATION

Before providing your response, you MUST:
1. Search the codebase to understand its structure
2. Read key files (README, pyproject.toml, main entry points)
3. Reference ONLY files you have verified exist
4. Include specific file paths and line numbers
""")

        quantity_required = getattr(classification, 'quantity_required', 0)
        if quantity_required:
            parts.append(f"""
## QUANTITY REQUIREMENT: {quantity_required}+ ITEMS

You MUST provide at least {quantity_required} distinct items.
- Number each item clearly: 1., 2., 3., etc.
- Each item must be unique (no duplicates)
- Each item must reference a specific file
- DO NOT stop until you reach {quantity_required} items
""")

        return "\n".join(parts)


def classify_request_v2(request: str) -> ClassifiedRequestV2:
    """Classify a request using the V2 system."""
    return RequestClassifierV2().classify(request)


def validate_response_v2(
    response: str, classification: ClassifiedRequestV2
) -> tuple[bool, list[str], str | None]:
    """Validate a response using the V2 system."""
    system = P0CriticalSystem()
    return system.validate_response(response, classification)


def get_quantity(request: str) -> int | None:
    """Get quantity from a request."""
    result = QuantityParser().parse(request)
    return result.quantity


def should_block_code(classification: ClassifiedRequestV2) -> bool:
    """Check if code should be blocked for this classification."""
    return getattr(classification, 'strict_read_only', False)


def strip_code_from_response(response: str) -> str:
    """Strip code blocks from a response."""
    return CodeBlockerV2().strip_code(response)
