"""Tests for _helpers.build_idempotency_registry."""

from __future__ import annotations

from unittest.mock import patch


class TestBuildIdempotencyRegistry:
    def test_returns_none_when_run_id_is_none(self):
        from agentic_devtools.orchestration.nodes._helpers import build_idempotency_registry

        assert build_idempotency_registry(None) is None

    def test_returns_none_when_run_id_is_empty_string(self):
        from agentic_devtools.orchestration.nodes._helpers import build_idempotency_registry

        assert build_idempotency_registry("") is None

    def test_returns_registry_when_state_dir_resolves(self, tmp_path):
        from agentic_devtools.orchestration.nodes._helpers import build_idempotency_registry

        with patch("agentic_devtools.state.get_state_dir", return_value=str(tmp_path)):
            registry = build_idempotency_registry("run-abc")
        assert registry is not None

    def test_returns_none_when_state_dir_raises(self):
        from agentic_devtools.orchestration.nodes._helpers import build_idempotency_registry

        with patch("agentic_devtools.state.get_state_dir", side_effect=RuntimeError("no state dir")):
            result = build_idempotency_registry("run-abc")
        assert result is None
