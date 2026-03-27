"""Tests for workflow gate conditions (#1021)."""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.workflows.gates import (
    always_pass,
    issue_is_current,
    plan_is_approved,
    register_builtin_gates,
)


def _make_run(target_ref: str | None = None) -> dict[str, Any]:
    run: dict[str, Any] = {"id": "run-1"}
    if target_ref is not None:
        run["target_ref"] = target_ref
    return run


def _mock_proc(stdout: bytes, returncode: int = 0) -> AsyncMock:
    proc = AsyncMock()
    proc.communicate = AsyncMock(return_value=(stdout, b""))
    proc.returncode = returncode
    return proc


# ---------------------------------------------------------------------------
# issue_is_current
# ---------------------------------------------------------------------------


class TestIssueIsCurrent:
    @pytest.mark.asyncio
    async def test_open_returns_true(self) -> None:
        proc = _mock_proc(b"OPEN\n")
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await issue_is_current(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is True

    @pytest.mark.asyncio
    async def test_closed_returns_false(self) -> None:
        proc = _mock_proc(b"CLOSED\n")
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await issue_is_current(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is False

    @pytest.mark.asyncio
    async def test_subprocess_failure_returns_false(self) -> None:
        with patch("asyncio.create_subprocess_exec", side_effect=OSError("gh not found")):
            result = await issue_is_current(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is False

    @pytest.mark.asyncio
    async def test_timeout_returns_false(self) -> None:
        proc = _mock_proc(b"")
        proc.communicate = AsyncMock(side_effect=asyncio.TimeoutError)
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await issue_is_current(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is False

    @pytest.mark.asyncio
    async def test_no_issue_number_returns_false(self) -> None:
        result = await issue_is_current(_make_run(), MagicMock(), {})
        assert result is False

    @pytest.mark.asyncio
    async def test_issue_number_from_target_ref(self) -> None:
        proc = _mock_proc(b"open\n")
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await issue_is_current(_make_run(target_ref="99"), MagicMock(), {})
        assert result is True


# ---------------------------------------------------------------------------
# plan_is_approved
# ---------------------------------------------------------------------------


class TestPlanIsApproved:
    @pytest.mark.asyncio
    async def test_has_label_returns_true(self) -> None:
        proc = _mock_proc(b"true\n")
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await plan_is_approved(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is True

    @pytest.mark.asyncio
    async def test_no_label_returns_false(self) -> None:
        proc = _mock_proc(b"false\n")
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await plan_is_approved(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is False

    @pytest.mark.asyncio
    async def test_malformed_output_returns_false(self) -> None:
        proc = _mock_proc(b"not-json\n")
        with patch("asyncio.create_subprocess_exec", return_value=proc):
            result = await plan_is_approved(_make_run(), MagicMock(), {"issue_number": "42"})
        assert result is False

    @pytest.mark.asyncio
    async def test_no_issue_number_returns_false(self) -> None:
        result = await plan_is_approved(_make_run(), MagicMock(), {})
        assert result is False


# ---------------------------------------------------------------------------
# always_pass
# ---------------------------------------------------------------------------


class TestAlwaysPass:
    @pytest.mark.asyncio
    async def test_returns_true(self) -> None:
        result = await always_pass({}, MagicMock(), {})
        assert result is True


# ---------------------------------------------------------------------------
# register_builtin_gates
# ---------------------------------------------------------------------------


class TestRegisterBuiltinGates:
    def test_registers_all_gates(self) -> None:
        with patch("anteroom.services.workflow_engine.register_gate_condition") as mock_reg:
            register_builtin_gates()
        names = {call.args[0] for call in mock_reg.call_args_list}
        assert names == {"issue_is_current", "plan_is_approved", "always_pass"}
