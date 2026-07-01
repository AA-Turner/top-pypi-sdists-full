# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["EvaluationDatasetVersionPublishParams"]


class EvaluationDatasetVersionPublishParams(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    force: bool
    """Force approve an evaluation dataset"""
