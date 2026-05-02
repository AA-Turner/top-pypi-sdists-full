# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ModelUpdateParams", "BaseModelMetadata", "BaseModelMetadataModelDetails"]


class ModelUpdateParams(TypedDict, total=False):
    base_model_id: str

    base_model_metadata: BaseModelMetadata

    description: str

    display_name: str

    model_card: str

    model_creation_parameters: Dict[str, object]

    model_group_id: str

    model_template_id: str

    model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC", "BUNDLE"]
    """An enum representing the different types of models supported.

    Attributes: COMPLETION: Denotes that the model type is completion.
    CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
    that the model type is agent. EMBEDDING: Denotes that the model type is
    embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
    that the model type is generic. BUNDLE: "Not to be used directly - type to
    surface a model bundle in the UI - TODO: Explicitly type a bundle
    """

    model_vendor: Literal[
        "OPENAI",
        "COHERE",
        "GOOGLE",
        "VERTEX_AI",
        "ANTHROPIC",
        "LAUNCH",
        "LLMENGINE",
        "BEDROCK",
        "FIREWORKS_AI",
        "OTHER",
    ]
    """An enum representing the different types of model vendors supported.

    Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
    that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
    Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
    Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
    vendor is Other.
    """

    name: str

    training_data_card: str


class BaseModelMetadataModelDetails(TypedDict, total=False):
    alignments: int

    languages: int

    number_of_parameters: int

    token_context_window: int


class BaseModelMetadata(TypedDict, total=False):
    delivery_date: str

    model_developer: str

    model_license_url: str

    model_details: Annotated[BaseModelMetadataModelDetails, PropertyInfo(alias="modelDetails")]

    ui_model_section_type: Literal["PARTNER", "OPENSOURCE", "CUSTOM"]
