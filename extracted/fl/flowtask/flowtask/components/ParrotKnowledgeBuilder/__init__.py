"""ParrotKnowledgeBuilder — builds GraphIndex/PageIndex knowledge structures from documents."""
from .loader import ParrotKnowledgeBuilder
from .payload import KnowledgeArtifact

__all__ = ["KnowledgeArtifact", "ParrotKnowledgeBuilder"]
