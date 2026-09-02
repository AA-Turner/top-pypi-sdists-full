"""Abstract, parrot-agnostic payload emitted by ParrotKnowledgeBuilder."""
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class KnowledgeArtifact(BaseModel):
    """Abstract structure emitted by ParrotKnowledgeBuilder for a downstream CopyTo*.

    Carries plain dicts only — no parrot UniversalNode/Edge objects and no live
    rustworkx graph — so the downstream persister never needs to import parrot.

    kind=="graph"  (graphindex): nodes/edges hold UniversalNode/Edge.model_dump() dicts.
    kind=="tree"   (pageindex):  tree holds the build_page_index() dict; node_markdown
                                 holds the popped _node_markdown mapping.
    """

    kind: Literal["graph", "tree"]
    index_type: Literal["graphindex", "pageindex"]
    source: str
    tenant_id: str = "default"
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[dict[str, Any]] = Field(default_factory=list)
    tree: Optional[dict[str, Any]] = None
    node_markdown: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
