"""Unit tests for canonical capability provisioning (FR-016)."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.scopes import (
    BASELINE_CAPABILITIES,
    AgentScopeLevel,
    CapabilityProvisioningError,
    SpecializationCategory,
    provision_capabilities,
    required_capabilities,
)


def test_provision_capabilities_success() -> None:
    available = frozenset(required_capabilities(AgentScopeLevel.SUBTASK, SpecializationCategory.PYTHON))
    provisioned = provision_capabilities(AgentScopeLevel.SUBTASK, SpecializationCategory.PYTHON, available)
    assert set(provisioned) == available


def test_provision_capabilities_raises_on_missing_capability() -> None:
    available = frozenset(BASELINE_CAPABILITIES)  # missing write_files, version_control, python_*
    with pytest.raises(CapabilityProvisioningError):
        provision_capabilities(AgentScopeLevel.SUBTASK, SpecializationCategory.PYTHON, available)
