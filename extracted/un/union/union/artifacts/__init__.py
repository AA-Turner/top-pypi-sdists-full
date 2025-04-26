import flytekit.core.artifact  # noqa: F401 place this line first

from union.artifacts._artifact import Artifact
from union.artifacts._card import DataCard, ModelCard
from union.artifacts._triggers import OnArtifact

__all__ = ["Artifact", "DataCard", "ModelCard", "OnArtifact"]
