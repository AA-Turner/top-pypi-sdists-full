# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Phase-1 local artifact registry.

This is scaffolding, not final governance policy.
If experimental artifacts need cross-environment discoverability,
move to file-backed or CI-enforced metadata in a future phase.
"""

from omnibase_compat.metadata.artifact_status import ArtifactStatus

_registry: dict[str, dict[str, str]] = {}


def register_experimental(
    *,
    name: str,
    status: ArtifactStatus,
    ticket: str,
    review_milestone: str,
) -> None:
    if not ticket:
        raise ValueError(f"Experimental artifact '{name}' requires a non-empty ticket.")
    if not review_milestone:
        raise ValueError(f"Experimental artifact '{name}' requires a non-empty review_milestone.")
    _registry[name] = {
        "status": status.value,
        "ticket": ticket,
        "review_milestone": review_milestone,
    }


def get_experimental_artifacts() -> dict[str, dict[str, str]]:
    return dict(_registry)
