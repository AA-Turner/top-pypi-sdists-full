"""Shared fixtures for matrx-ai persistence tests.

The Coordinator pushes its wrapped Session onto matrx-orm's
``_session_stack`` at __init__ and never pops it (request-task
lifecycle bounds it). In a test environment, we need to clear the
stack between tests so one test's Coordinator doesn't leak into the
next.
"""

from __future__ import annotations

from collections.abc import Iterable

import pytest


@pytest.fixture(autouse=True)
def capture_sink(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    failures: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []

    async def fake_record_failures(
        ops: Iterable[object], exc: BaseException, **kwargs: object
    ) -> list[str]:
        ops = list(ops)
        failures.append({"ops": ops, "exc": exc, "kwargs": kwargs})
        # The real contract: one receipt (op_id) per preserved op.
        return [str(getattr(op, "op_id", "")) for op in ops]

    async def fake_record_error(exc: BaseException, **kwargs: object) -> None:
        errors.append({"exc": exc, "kwargs": kwargs})

    monkeypatch.setattr("matrx_orm.session.fallback.record_failures", fake_record_failures)
    monkeypatch.setattr("matrx_orm.session.fallback.record_error", fake_record_error)
    return failures, errors


@pytest.fixture(autouse=True)
def _reset_session_stack():
    from matrx_orm.session.session import _session_stack

    token = _session_stack.set(())
    yield
    _session_stack.reset(token)


@pytest.fixture(autouse=True)
def _write_retry_policy_never_reads_the_live_knob_table(monkeypatch: pytest.MonkeyPatch):
    """The individual-write fallback reads its retry budget from ``platform.feature_knob``.

    When the run also loaded the host conftest (a multi-package invocation), ``import db``
    has registered the real platform database, so that read dials a live host and can outlast
    a test's wait window, and the captured failure arrives late. A persistence test pins the
    recorded starting policy instead; nothing here may depend on a live knob read.
    """
    from matrx_orm.core.write_retry import STARTING_POLICY

    async def _starting_policy(config_name: str):
        return STARTING_POLICY

    monkeypatch.setattr("matrx_orm.core.write_retry.resolve_policy", _starting_policy)
