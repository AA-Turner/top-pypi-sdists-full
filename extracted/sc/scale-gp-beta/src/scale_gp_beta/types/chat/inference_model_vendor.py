# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["InferenceModelVendor"]

InferenceModelVendor: TypeAlias = Literal[
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
