# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import FileTypes

__all__ = ["TrainingDatasetCreateParams"]


class TrainingDatasetCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    file: Required[FileTypes]
    """The file to upload as the training dataset"""

    name: Required[str]
    """The name of the dataset"""

    schema_type: Required[Literal["GENERATION", "RERANKING_QUESTIONS"]]
    """The schema type of the dataset, currently only GENERATION is supported"""
