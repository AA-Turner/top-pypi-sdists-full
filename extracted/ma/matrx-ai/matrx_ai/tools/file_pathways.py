"""The file placement pathways matrx-ai's own writers name (placement registry).

A package that writes files declares the pathway it names HERE, beside the writer, so the name is
known in every process the writer runs in (aidream, a sandbox, a standalone install) — a pathway
declared only by one host is ``Unknown pathway`` everywhere else. aidream's
``services/files/pathways.py`` imports this module so the host's declared set (and the live
``files.file_pathway`` rows synced from it) still lists it. Plan: common-docs
systems/files/file-service/projects/placement-registry/PLAN.md.
"""

from __future__ import annotations

from matrx_files.placement import register_pathway

#: Image-shaped tool output masters (screenshots, rendered captures) — ``tools/image_outputs.py``.
TOOL_IMAGE_PATHWAY = "agent.tool_image"

register_pathway(
    TOOL_IMAGE_PATHWAY,
    owner_feature="agents/agent-tools",
    audience="automated",
    root="system",
    subfolder="tool-images/{conversation}",
    naming="id_only",
    description="Screenshots agent tools take while working.",
    legacy_prefixes=("tool-images", "system-files/tool-images"),
)

__all__ = ["TOOL_IMAGE_PATHWAY"]
