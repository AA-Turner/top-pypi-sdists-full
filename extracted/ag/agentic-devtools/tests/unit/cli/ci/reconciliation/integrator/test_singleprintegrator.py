from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.reconciliation.integrator import (
    SinglePRIntegrator,
    SpecialistOutput,
    StaleWriterError,
)
from agentic_devtools.cli.ci.reconciliation.models import PermitStatus, WorkerPermit


def _state():
    permit = WorkerPermit(
        "permit:a",
        "request:a",
        "owner/repo",
        1,
        "obligation",
        "batch",
        "worker",
        "github",
        "gpt-5.6-luna",
        1,
        datetime.now(UTC),
        datetime.now(UTC) + timedelta(minutes=5),
        PermitStatus.ACCEPTED,
    )
    return Mock(active_permits={"permit:a": permit})


def test_integrator_serializes_overlaps_and_publishes_once() -> None:
    integrator = SinglePRIntegrator(lambda: datetime.now(UTC))
    first = SpecialistOutput("worker", "permit:a", "head", ("a.py",))
    second = SpecialistOutput("worker", "permit:a", "head", ("a.py",))
    applied: list[tuple[SpecialistOutput, ...]] = []
    result = integrator.integrate(
        _state(), (first, second), current_head_sha="head", apply_batch=applied.append, publish=lambda: "new"
    )
    assert result.accepted and len(result.batches) == 2 and len(applied) == 2


def test_integrator_rejects_stale_output_and_missing_permit() -> None:
    integrator = SinglePRIntegrator(lambda: datetime.now(UTC))
    output = SpecialistOutput("worker", "permit:a", "other")
    with pytest.raises(StaleWriterError, match="stale"):
        integrator.integrate(_state(), (output,), current_head_sha="head", apply_batch=Mock(), publish=Mock())
    with pytest.raises(StaleWriterError, match="active"):
        integrator.integrate(
            Mock(active_permits={}),
            (SpecialistOutput("w", "missing", "head"),),
            current_head_sha="head",
            apply_batch=Mock(),
            publish=Mock(),
        )
    with pytest.raises(ValueError, match="clock"):
        SinglePRIntegrator(None)  # type: ignore[arg-type]


def test_integrator_batches_non_overlapping_outputs() -> None:
    state = _state()
    second_permit = state.active_permits["permit:a"]
    state.active_permits["permit:b"] = second_permit
    outputs = (
        SpecialistOutput("a", "permit:a", "head", ("a.py",)),
        SpecialistOutput("b", "permit:b", "head", ("b.py",)),
    )
    applied: list[tuple[SpecialistOutput, ...]] = []
    result = SinglePRIntegrator(lambda: datetime.now(UTC)).integrate(
        state, outputs, current_head_sha="head", apply_batch=applied.append, publish=lambda: "new"
    )
    assert len(result.batches) == 1 and len(applied[0]) == 2
