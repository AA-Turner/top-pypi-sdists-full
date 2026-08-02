# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

import pytest

from omnibase_compat.experimental._registry import (
    get_experimental_artifacts,
    register_experimental,
)
from omnibase_compat.metadata.artifact_status import ArtifactStatus


@pytest.mark.unit
def test_register_experimental_artifact() -> None:
    register_experimental(
        name="NewEventFormatV2",
        status=ArtifactStatus.experimental,
        ticket="OMN-9001",
        review_milestone="v0.3",
    )
    artifacts = get_experimental_artifacts()
    assert "NewEventFormatV2" in artifacts
    assert artifacts["NewEventFormatV2"]["ticket"] == "OMN-9001"


@pytest.mark.unit
def test_experimental_artifact_requires_ticket() -> None:
    with pytest.raises(ValueError, match="ticket"):
        register_experimental(
            name="BadArtifact",
            status=ArtifactStatus.experimental,
            ticket="",
            review_milestone="v0.3",
        )


@pytest.mark.unit
def test_experimental_artifact_requires_milestone() -> None:
    with pytest.raises(ValueError, match="review_milestone"):
        register_experimental(
            name="BadArtifact2",
            status=ArtifactStatus.experimental,
            ticket="OMN-9001",
            review_milestone="",
        )
