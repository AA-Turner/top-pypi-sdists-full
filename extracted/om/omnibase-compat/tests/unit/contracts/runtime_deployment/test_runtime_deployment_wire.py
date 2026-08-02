# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Regression tests for the runtime deployment wire DTOs (OMN-12576).

These DTOs transiently mirror the OCC-owned wire schema
(``onex_change_control/src/onex_change_control/wire_schemas/runtime_deployment_request_v1.yaml``
and ``runtime_deployment_proof_v1.yaml``). OCC owns the source of truth; compat
is temporary. The tests pin: required-field rejection (missing source_sha,
image_digest, runtime_lane, promotion_batch where required), the runtime-lane
enum values, and round-trip stability.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from omnibase_compat.contracts.runtime_deployment.wire.model_runtime_deployment_proof import (
    ModelRuntimeDeploymentProof,
)
from omnibase_compat.contracts.runtime_deployment.wire.model_runtime_deployment_request import (
    ModelRuntimeDeploymentRequest,
)
from omnibase_compat.contracts.runtime_deployment.wire.types import EnumRuntimeLane


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_runtime_lane_enum_values() -> None:
    assert EnumRuntimeLane.DEV.value == "dev"
    assert EnumRuntimeLane.STABILITY_TEST.value == "stability-test"
    assert EnumRuntimeLane.PROD.value == "prod"


def _valid_request_kwargs() -> dict[str, object]:
    return {
        "correlation_id": uuid4(),
        "deployment_id": uuid4(),
        "runtime_lane": EnumRuntimeLane.DEV,
        "source_branch": "dev",
        "source_sha": "abc123def456",
        "requested_by": "runtime-rebuild-trigger",
        "requested_at": datetime.now(tz=UTC),
    }


def _valid_proof_kwargs() -> dict[str, object]:
    return {
        "correlation_id": uuid4(),
        "deployment_id": uuid4(),
        "runtime_lane": EnumRuntimeLane.STABILITY_TEST,
        "source_sha": "abc123def456",
        "image_digest": "sha256:deadbeef",
        "compose_project": "omnibase-infra-stability-test",
        "health_status": "pass",
        "ready_status": "pass",
        "probed_at": datetime.now(tz=UTC),
        "status": "success",
    }


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_request_accepts_valid_payload() -> None:
    request = ModelRuntimeDeploymentRequest(**_valid_request_kwargs())  # type: ignore[arg-type]

    assert request.runtime_lane is EnumRuntimeLane.DEV
    assert request.image_digest is None
    assert request.promotion_batch_id is None


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_request_rejects_missing_source_sha() -> None:
    kwargs = _valid_request_kwargs()
    del kwargs["source_sha"]

    with pytest.raises(ValidationError):
        ModelRuntimeDeploymentRequest(**kwargs)  # type: ignore[arg-type]


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_request_rejects_missing_runtime_lane() -> None:
    kwargs = _valid_request_kwargs()
    del kwargs["runtime_lane"]

    with pytest.raises(ValidationError):
        ModelRuntimeDeploymentRequest(**kwargs)  # type: ignore[arg-type]


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_request_rejects_unknown_lane() -> None:
    kwargs = _valid_request_kwargs()
    kwargs["runtime_lane"] = "canary"

    with pytest.raises(ValidationError):
        ModelRuntimeDeploymentRequest(**kwargs)  # type: ignore[arg-type]


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_proof_requires_image_digest() -> None:
    """image_digest is the prod-gate authority and is required on the proof."""
    kwargs = _valid_proof_kwargs()
    del kwargs["image_digest"]

    with pytest.raises(ValidationError):
        ModelRuntimeDeploymentProof(**kwargs)  # type: ignore[arg-type]


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_proof_rejects_missing_runtime_lane() -> None:
    kwargs = _valid_proof_kwargs()
    del kwargs["runtime_lane"]

    with pytest.raises(ValidationError):
        ModelRuntimeDeploymentProof(**kwargs)  # type: ignore[arg-type]


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_request_round_trips_new_fields() -> None:
    kwargs = _valid_request_kwargs()
    kwargs["image_digest"] = "sha256:deadbeef"
    kwargs["promotion_batch_id"] = "promo-2026-06-01-001"
    request = ModelRuntimeDeploymentRequest(**kwargs)  # type: ignore[arg-type]

    dumped = request.model_dump(mode="json")
    restored = ModelRuntimeDeploymentRequest.model_validate(dumped)

    assert restored == request
    assert restored.image_digest == "sha256:deadbeef"
    assert restored.promotion_batch_id == "promo-2026-06-01-001"


@pytest.mark.unit
@pytest.mark.timeout(30)
def test_proof_round_trips() -> None:
    proof = ModelRuntimeDeploymentProof(**_valid_proof_kwargs())  # type: ignore[arg-type]

    dumped = proof.model_dump(mode="json")
    restored = ModelRuntimeDeploymentProof.model_validate(dumped)

    assert restored == proof
    assert restored.image_digest == "sha256:deadbeef"
