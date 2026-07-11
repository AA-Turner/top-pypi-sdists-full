# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["AnnotationTaskBatchUpdateParams", "AuditAssignment"]


class AnnotationTaskBatchUpdateParams(TypedDict, total=False):
    assigned_to: str

    audit_assignment: AuditAssignment

    ids: SequenceNotStr[str]

    status: Literal["PENDING_REDO", "COMPLETED"]


class AuditAssignment(TypedDict, total=False):
    evaluation_id: Required[str]

    evaluation_item_ids: Required[SequenceNotStr[str]]

    queue_id: Required[str]

    level_1_assigned_to: str

    level_2_assigned_to: str
