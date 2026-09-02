"""Artifact block parser.

Parses the inner content and metadata of an <artifact> block into structured data.

Expected LLM XML shape:
    <artifact id="artifact_1" type="iframe" title="Revenue Dashboard">
        ...content...
    </artifact>

The full opening tag is parsed separately by the detector; this parser
receives the inner content plus pre-parsed metadata dict containing
artifactId, artifactIndex, artifactType, and artifactTitle.
"""

from __future__ import annotations

from matrx_ai.processing.blocks.models.artifact import ArtifactBlockData


def parse_artifact(
    inner_content: str,
    metadata: dict | None = None,
) -> ArtifactBlockData | None:
    """
    Parse an artifact block's inner content into structured data.

    Args:
        inner_content: Raw text between <artifact ...> and </artifact> tags.
        metadata: Pre-parsed metadata from the detector, containing
                  artifactId, artifactIndex, artifactType, artifactTitle.

    Returns:
        ArtifactBlockData if valid content exists, else None.
    """
    if not inner_content.strip():
        return None

    meta = metadata or {}

    artifact_id = meta.get("artifactId", "artifact-0")
    artifact_index = meta.get("artifactIndex", 0)
    artifact_type = meta.get("artifactType", "text")
    title = meta.get("artifactTitle", "")

    return ArtifactBlockData(
        artifact_id=artifact_id,
        artifact_index=artifact_index,
        artifact_type=artifact_type,
        title=title,
        content=inner_content.strip(),
    )
