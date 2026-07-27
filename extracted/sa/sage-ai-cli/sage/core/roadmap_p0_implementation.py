"""
SAGE Roadmap P0 Critical Implementation - Items 1-130.

This module provides the comprehensive fixes for all P0 Critical items:
- Items 1-20: Quantity Detection
- Items 21-35: Request Type Classification
- Items 36-50: Pipeline Selection
- Items 51-70: Code Generation Blocking
- Items 71-90: List Format Enforcement
- Items 91-105: Explicit Instruction Detection
- Items 106-120: Instruction Compliance Validation
- Items 121-130: Follow-Through Validation

All 130 P0 items are addressed in this module.
"""

from __future__ import annotations

# Re-export from specialized modules for backwards compatibility
from sage.core.quantity_detection import QuantityParser, QuantityResult
from sage.core.p0_request_classification import (
    RequestTypeV2,
    ClassifiedRequestV2,
    RequestClassifierV2,
    OutputFormatV2,
    PipelineTypeV2,
)
from sage.core.code_generation_blocking import CodeBlockerV2
from sage.core.list_format_enforcement import ListEnforcerV2, ListValidationResult
ListFormatEnforcer = ListEnforcerV2  # Legacy alias
from sage.core.instruction_extraction import ExtractedInstruction, InstructionExtractor
from sage.core.instruction_compliance import ComplianceValidator, ComplianceResult
from sage.core.follow_through_validation import FollowThroughValidator
from sage.core.p0_critical_system import (
    P0CriticalSystem,
    ProcessResult,
    classify_request_v2,
    validate_response_v2,
    get_quantity,
    should_block_code,
    strip_code_from_response,
)
