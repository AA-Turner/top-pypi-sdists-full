# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

from .sort_order import SortOrder

__all__ = ["CompletionModelsParams"]


class CompletionModelsParams(TypedDict, total=False):
    ending_before: str

    limit: int

    model_vendor: Literal[
        "openai",
        "cohere",
        "vertex_ai",
        "anthropic",
        "azure",
        "gemini",
        "launch",
        "llmengine",
        "model_zoo",
        "bedrock",
        "xai",
        "fireworks_ai",
    ]

    sort_by: str

    sort_order: SortOrder

    starting_after: str
