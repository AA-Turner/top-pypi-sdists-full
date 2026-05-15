# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

from .application_agent_graph_edge_param import ApplicationAgentGraphEdgeParam

__all__ = ["ApplicationAgentGraphNodeParam"]


class ApplicationAgentGraphNodeParam(TypedDict, total=False):
    id: Required[str]

    name: Required[str]

    type: Required[str]

    config: Dict[str, object]

    edges: Iterable[ApplicationAgentGraphEdgeParam]

    nodes: Iterable["ApplicationAgentGraphNodeParam"]

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION_INPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "KB_INPUT",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "CODE_EXECUTION",
        "DATA_MANIPULATION",
        "EVALUATION",
        "FILE_RETRIEVAL",
        "KB_ADD_CHUNK",
        "KB_MANAGEMENT",
        "GUARDRAIL",
        "OUTPUT_GUARDRAIL",
        "TRACER",
        "AGENT_TRACER",
        "AGENT_WORKFLOW",
        "STANDALONE",
    ]
