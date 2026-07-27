"""Tests for the `sage ask --no-agent` flag.

`sage ask` normally routes complex-looking prompts ("Implement a class
LRUCache...") through the full agentic SAGEAgent — which writes files,
runs tests, and consumes 4+ minutes for what should be a quick code
snippet. The `--no-agent` flag forces the simple-QA path: one model
call, return the response, no tool execution.
"""

from __future__ import annotations

import pytest
from pathlib import Path

@pytest.fixture(autouse=True)
def mock_home(monkeypatch, tmp_path):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    import sage.config
    monkeypatch.setattr(sage.config, "CONFIG_PATH", tmp_path / "config.json")
    monkeypatch.setattr(sage.config, "SAGE_DIR", tmp_path)
    return tmp_path

class TestNoAgentFlag:

    def test_no_agent_forces_simple_qa_for_implement_prompts(self, monkeypatch, tmp_path):
        """Even a prompt like `Implement a class` should hit the simple-QA
        message builder when --no-agent is set."""
        from typer.testing import CliRunner

        # Patch the model-prep step so we don't depend on real model registry
        def fake_prepare(cfg, model_id):
            return cfg, model_id or "ollama:fake"
        monkeypatch.setattr("sage.cli_core._prepare_model_for_use", fake_prepare)

        # Patch the router-build to return an inert dummy router
        class _DummyRouter:
            def generate(self, *a, **kw): return "def hello(): return 1"
            def stream(self, *a, **kw): yield "def hello(): return 1"
        monkeypatch.setattr("sage.cli_core._build_router", lambda cfg: _DummyRouter())
        monkeypatch.setattr("sage.cli_core._auto_upgrade_model_if_possible", lambda r, c, m, **kw: m)

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
