# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ApplicationNodeParam", "Configuration"]


class Configuration(TypedDict, total=False):
    value: Required[object]


class ApplicationNodeParam(TypedDict, total=False):
    id: Required[str]

    application_node_schema_id: Required[
        Literal[
            "text_input_schema",
            "text_output_schema",
            "knowledge_base_input_schema",
            "knowledge_base_schema",
            "multi_knowledge_base_input_schema",
            "multi_knowledge_base_schema",
            "reranker_schema",
            "prompt_engineering_schema",
            "completion_model_input_schema",
            "completion_model_schema",
            "external_endpoint_schema",
            "document_input_schema",
            "map_reduce_schema",
            "document_search_schema",
            "document_prompt_schema",
        ]
    ]

    configuration: Dict[str, Configuration]
