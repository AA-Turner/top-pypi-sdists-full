# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ApplicationMetricScore", "LlmMetadata", "LlmMetadataUsage"]


class LlmMetadataUsage(BaseModel):
    completion_tokens: Optional[int] = None

    cost: Optional[float] = None

    model: Optional[
        Literal[
            "gpt-4-turbo-2024-04-09",
            "gpt-3.5-turbo-0125",
            "gpt-4o-2024-05-13",
            "gpt-4-32k-0613",
            "gpt-4-turbo-preview",
            "gpt-4o",
            "gpt-4o-mini-2024-07-18",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-5-nano",
            "gpt-5-mini",
            "gpt-5",
            "gpt-5.1",
            "gpt-5.2",
            "o1",
            "o1-mini",
            "o3",
            "o3-mini",
            "o3-mini-2025-01-31",
            "o4-mini",
            "gpt-oss-120b",
            "gpt-oss-20b",
            "llama-3-70b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-70b-instruct-bedrock",
        ]
    ] = None

    prompt_tokens: Optional[int] = None


class LlmMetadata(BaseModel):
    logging: Optional[Dict[str, object]] = None

    reasoning: Optional[str] = None

    time_elapsed_s: Optional[int] = None

    usage: Optional[List[LlmMetadataUsage]] = None


class ApplicationMetricScore(BaseModel):
    category: Literal["accuracy", "quality", "retrieval", "trust-and-safety"]

    metric_type: Literal[
        "answer-correctness",
        "answer-relevance",
        "faithfulness",
        "context-recall",
        "coherence",
        "grammar",
        "moderation",
        "safety",
        "safety-bias-and-stereotyping",
        "safety-opinions-disputed-topics",
        "safety-unethical-harmful-activities",
        "safety-copyright-violations",
        "safety-harmful-content",
        "safety-privacy-violations",
    ]

    llm_metadata: Optional[LlmMetadata] = None

    score: Optional[float] = None
