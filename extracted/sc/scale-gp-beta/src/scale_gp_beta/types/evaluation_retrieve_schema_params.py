# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EvaluationRetrieveSchemaParams"]


class EvaluationRetrieveSchemaParams(TypedDict, total=False):
    include_archived: bool
    """Include archived items in schema analysis"""
