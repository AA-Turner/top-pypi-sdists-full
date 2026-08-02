# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest
from pydantic import ValidationError

from omnibase_compat.metadata.artifact_status import ArtifactStatus
from omnibase_compat.metadata.transitional import TransitionalMeta


@pytest.mark.unit
def test_artifact_status_values() -> None:
    assert {status.value for status in ArtifactStatus} == {
        "experimental",
        "candidate",
        "stable",
        "deprecated",
        "retired",
    }


@pytest.mark.unit
def test_transitional_meta_full_fields() -> None:
    meta = TransitionalMeta(
        canonical_owner="omnibase_spi.contracts.ticket",
        removal_ticket="OMN-9999",
        removal_milestone="v2.0",
        introduced_by_ticket="OMN-9998",
        review_owner="jonah",
    )
    assert meta.removal_ticket == "OMN-9999"


@pytest.mark.unit
def test_transitional_meta_missing_fields() -> None:
    with pytest.raises(ValidationError):
        TransitionalMeta(canonical_owner="foo")  # type: ignore[call-arg]
