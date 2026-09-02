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
    ) -> None:
        failures.append({"ops": list(ops), "exc": exc, "kwargs": kwargs})

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
