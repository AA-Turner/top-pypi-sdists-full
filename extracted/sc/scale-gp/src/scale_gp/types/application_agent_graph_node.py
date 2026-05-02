# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .application_agent_graph_edge import ApplicationAgentGraphEdge

__all__ = ["ApplicationAgentGraphNode"]


class ApplicationAgentGraphNode(BaseModel):
    id: str

    name: str

    type: str

    config: Optional[Dict[str, object]] = None

    edges: Optional[List[ApplicationAgentGraphEdge]] = None

    nodes: Optional[List["ApplicationAgentGraphNode"]] = None

    operation_type: Optional[
        Literal[
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
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
    ] = None
