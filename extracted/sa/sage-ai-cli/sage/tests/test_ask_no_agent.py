"""Tests for the `sage ask --no-agent` flag.

`sage ask` normally routes complex-looking prompts ("Implement a class
LRUCache...") through the full agentic SAGEAgent — which writes files,
runs tests, and consumes 4+ minutes for what should be a quick code
snippet. The `--no-agent` flag forces the simple-QA path: one model
call, return the response, no tool execution.
"""

from __future__ import annotations

import pytest


class TestNoAgentFlag:

    def test_no_agent_forces_simple_qa_for_implement_prompts(self, monkeypatch):
        """Even a prompt like `Implement a class` should hit the simple-QA
        message builder when --no-agent is set."""
        from typer.testing import CliRunner

        # Patch the model-prep step so we don't depend on real model registry
        from sage.config import SageConfig
        def fake_prepare(cfg, model_id):
            return cfg, model_id or "ollama:fake"
        monkeypatch.setattr("sage.cli_core._prepare_model_for_use", fake_prepare)

        # Patch the router-build to return an inert dummy router
        class _DummyRouter:
            def generate(self, *a, **kw): return "def hello(): return 1"
            def stream(self, *a, **kw): yield "def hello(): return 1"
        monkeypatch.setattr("sage.cli_core._build_router", lambda cfg: _DummyRouter())

        # Import app AFTER patches so any closure-captured refs are fresh
        from sage.cli_core import app
        runner = CliRunner()
        result = runner.invoke(
            app,
            ["ask", "--no-agent", "--model", "ollama:fake",
             "--raw", "--max-tokens", "100",
             "Implement a class LRUCache with O(1) operations"],
        )
        assert result.exit_code == 0, f"rc={result.exit_code} exc={result.exception!r}"
        assert "def hello(): return 1" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
