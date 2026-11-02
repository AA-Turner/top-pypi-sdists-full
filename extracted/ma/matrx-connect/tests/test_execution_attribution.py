from __future__ import annotations

import pytest
from matrx_connect import AppContext, ConsoleEmitter


def _context() -> AppContext:
    return AppContext(emitter=ConsoleEmitter("test", accumulate=False))


def test_execution_attribution_is_paired_canonical_and_fork_safe() -> None:
    run_id = "AAAAAAAA-AAAA-4AAA-8AAA-AAAAAAAAAAAA"
    attributed = _context().with_execution_attribution("workflow_run", run_id)

    assert attributed.execution_kind == "workflow_run"
    assert attributed.execution_id == run_id.lower()
    child = attributed.fork_for_workflow_step(
        "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
    )
    assert child.execution_kind == "workflow_run"
    assert child.execution_id == run_id.lower()


@pytest.mark.parametrize(
    ("kind", "execution_id", "message"),
    [
        ("workflow_run", None, "must be set together"),
        (None, "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "must be set together"),
        ("Workflow Run", "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "lowercase"),
        ("workflow_run", "not-a-uuid", "valid UUID"),
    ],
)
def test_invalid_execution_attribution_fails_at_context_boundary(
    kind: str | None,
    execution_id: str | None,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        AppContext(
            emitter=ConsoleEmitter("test", accumulate=False),
            execution_kind=kind,
            execution_id=execution_id,
        )
