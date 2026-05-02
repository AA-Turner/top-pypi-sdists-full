"""
Instruction Compliance Validation for SAGE - Items 106-120 from Roadmap P0.

This module provides validation to ensure model responses comply with instructions.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING

from sage.core.p0_request_classification import OutputFormatV2

if TYPE_CHECKING:
    from sage.core.p0_request_classification import ClassifiedRequestV2
    from sage.core.instruction_extraction import ExtractedInstruction

from sage.core.code_generation_blocking import CodeBlockerV2


@dataclass
class ComplianceResult:
    """Result of compliance validation."""
    is_compliant: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class ComplianceValidator:
    """
    Items 106-120: Validates that responses comply with instructions and classification.
    """

    def validate(
        self,
        response: str,
        classification_or_instructions: ClassifiedRequestV2
        | list[ExtractedInstruction]
        | None = None,
        instructions: list[ExtractedInstruction] | None = None,
    ) -> tuple[bool, list[str], list[str]]:
        """
        Items 106-120: Validate response compliance.

        Returns (is_compliant, errors, warnings)
        """
        # Handle flexible argument passing
        if isinstance(classification_or_instructions, list):
            # Called as validate(response, instructions)
            instructions = classification_or_instructions
            classification = None
        else:
            # Called as validate(response, classification, instructions)
            classification = classification_or_instructions
            if instructions is None:
                instructions = []

        errors = []
        warnings = []

        # Item 106: Quantity compliance (only if classification provided)
        quantity_required = getattr(classification, 'quantity_required', 0)
        if classification and quantity_required:
            item_count = len(re.findall(r"^\s*\d+[\.\)]\s+", response, re.MULTILINE))
            if item_count < quantity_required:
                errors.append(
                    f"Quantity violation: {item_count} items but {quantity_required} required"
                )

        # Item 107: Format compliance (only if classification provided)
        if classification and hasattr(classification, 'output_format'):
            if classification.output_format == OutputFormatV2.MARKDOWN_TABLE:
                if not re.search(r"^\|.*\|$", response, re.MULTILINE):
                    warnings.append("Expected table format but no table found")

        # Item 108-109: Inclusion/exclusion compliance
        for inst in instructions:
            if hasattr(inst, 'type') and inst.type == "include":
                if inst.content.lower() not in response.lower():
                    warnings.append(f"Missing required element: {inst.content}")
            elif hasattr(inst, 'type') and inst.type == "exclude":
                if inst.content.lower() in response.lower():
                    errors.append(f"Contains forbidden element: {inst.content}")

        # Item 110: Code compliance for read-only (only if classification provided)
        if classification and getattr(classification, 'strict_read_only', False):
            blocker = CodeBlockerV2()
            has_code, code_violations = blocker.check(response)
            if has_code:
                errors.extend(code_violations)

        is_compliant = len(errors) == 0
        return is_compliant, errors, warnings

    def get_retry_prompt(
        self, errors: list[str], warnings: list[str], classification: ClassifiedRequestV2
    ) -> str:
        """Item 113-114: Generate retry prompt for non-compliant responses."""
        parts = ["## COMPLIANCE ISSUES DETECTED", ""]

        if errors:
            parts.append("### Errors (MUST FIX):")
            for error in errors:
                parts.append(f"- {error}")
            parts.append("")

        if warnings:
            parts.append("### Warnings:")
            for warning in warnings:
                parts.append(f"- {warning}")
            parts.append("")

        parts.append("Please regenerate your response fixing these issues.")

        if getattr(classification, 'strict_read_only', False):
            parts.append("\nREMINDER: This is READ-ONLY analysis. NO code generation.")

        quantity_required = getattr(classification, 'quantity_required', 0)
        if quantity_required:
            parts.append(
                f"\nREMINDER: You must provide at least {quantity_required} items."
            )

        return "\n".join(parts)
