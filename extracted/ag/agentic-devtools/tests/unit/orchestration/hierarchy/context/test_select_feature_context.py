"""Unit tests for ContextProvenance and verified/unavailable/inferred field construction."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import (
    ArtifactAvailability,
    ContextProvenance,
    select_feature_context,
)


def test_select_feature_context_includes_verified_artifact() -> None:
    fields = select_feature_context(
        {"spec.md": ArtifactAvailability(path="specs/x/spec.md", exists=True, content="hello")}, revision="rev1"
    )
    by_name = {f.name: f for f in fields}
    assert by_name["spec_md"].provenance == ContextProvenance.VERIFIED


def test_select_feature_context_covers_every_profile_artifact() -> None:
    from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
    from agentic_devtools.hierarchy.models import HierarchyLevel

    profile = get_artifact_profile(HierarchyLevel.FEATURE)
    fields = select_feature_context({}, revision="rev1")
    assert len(fields) == len(profile.included_artifacts)
    assert all(f.provenance == ContextProvenance.UNAVAILABLE for f in fields)
