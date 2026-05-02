# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["EvaluationClaimTaskParams"]


class EvaluationClaimTaskParams(TypedDict, total=False):
    task_type: Literal["EVALUATION_ANNOTATION", "EVALUATION_AUDIT", "CONTRIBUTOR_ANNOTATION", "CONTRIBUTOR_AUDIT"]

    skip_current: bool
