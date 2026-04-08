"""Unit tests for execution surface routing advisory (#1317)."""

from anteroom.config import build_runtime_context


class TestRoutingAdvisory:
    def test_advisory_appears_with_thresholds(self) -> None:
        ctx = build_runtime_context(
            model="test",
            background_suggest_seconds=30,
            detach_suggest_seconds=120,
        )
        assert "Execution surface routing:" in ctx
        assert "30s" in ctx
        assert "120s" in ctx
        assert "briefly tell the user why" in ctx

    def test_advisory_omitted_when_disabled(self) -> None:
        ctx = build_runtime_context(
            model="test",
            background_suggest_seconds=0,
            detach_suggest_seconds=0,
        )
        assert "Execution surface routing:" not in ctx

    def test_advisory_partial_background_only(self) -> None:
        ctx = build_runtime_context(
            model="test",
            background_suggest_seconds=60,
            detach_suggest_seconds=0,
        )
        assert "60s" in ctx
        assert "detach" not in ctx.lower().split("execution surface routing:")[1].split("workflow")[0]
