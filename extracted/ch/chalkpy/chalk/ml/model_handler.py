from __future__ import annotations

CHALK_HANDLER_ARTIFACT_PATH = "/app/artifacts"
"""Mount path inside the deployed container where chalkpy attaches the
handler-artifact volume. Single source of truth shared by the image-only
deploy path (which probes for a deterministic-named volume) and any future
abstraction that uploads files to that volume."""
