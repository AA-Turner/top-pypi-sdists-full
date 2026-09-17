"""Tests for RepairPromptInput."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.dispatch_state import MAX_DISPATCHES_PER_SHA
from agentic_devtools.cli.ci.repair_prompt import RepairPromptInput


def _input(**overrides: object) -> RepairPromptInput:
    values: dict[str, object] = {
        "repo": "swai-factory",
        "pull_request_id": 42,
        "sha": "a" * 40,
        "ordinal": 1,
        "review_context": "review\ncontext",
        "ci_diagnostics": "ci diagnostics",
    }
    values.update(overrides)
    return RepairPromptInput(**values)  # type: ignore[arg-type]


def test_accepts_the_maximum_dispatch_ordinal() -> None:
    assert _input(ordinal=MAX_DISPATCHES_PER_SHA).ordinal == MAX_DISPATCHES_PER_SHA


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("repo", ""),
        ("repo", "Owner/repo"),
        ("repo", "SWAI-FACTORY"),
        ("repo", 1),
        ("pull_request_id", 0),
        ("pull_request_id", True),
        ("pull_request_id", "42"),
        ("sha", "A" * 40),
        ("sha", "a" * 39),
        ("sha", "g" * 40),
        ("sha", None),
        ("ordinal", 0),
        ("ordinal", False),
        ("ordinal", "1"),
        ("ordinal", MAX_DISPATCHES_PER_SHA + 1),
    ],
)
def test_rejects_malformed_identity(field: str, value: object) -> None:
    with pytest.raises(ValueError):
        _input(**{field: value})


@pytest.mark.parametrize("field", ["review_context", "ci_diagnostics"])
def test_rejects_non_string_required_artifacts(field: str) -> None:
    with pytest.raises(ValueError):
        _input(**{field: object()})


@pytest.mark.parametrize("value", [1, False, object()])
def test_rejects_non_string_prior_state(value: object) -> None:
    with pytest.raises(ValueError):
        _input(prior_round_state=value)
