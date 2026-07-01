# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AutoEvaluationParameters"]


class AutoEvaluationParameters(TypedDict, total=False):
    batch_size: int

    temperature: float
