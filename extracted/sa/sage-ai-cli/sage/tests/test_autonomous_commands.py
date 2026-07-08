"""Tests for SAGE autonomous commands (/autopolit, /autofleet, /autoorg)."""

import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sage.cli_core import app
from sage.core.autonomous import (
    LoopState,
    run_autofleet_loop,
    run_autoorg_loop,
    run_autopolit_loop,
)

# ---------------------------------------------------------------------------
# Phase 1: Loop Primitive Tests
# ---------------------------------------------------------------------------


class TestLoopPrimitives:
    """Test the autonomous loop machinery directly (no real LLM)."""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.state = LoopState(project_root=self.temp_dir)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_autopolit_loop_max_iterations(self):
        """Test autopolit runs exactly max_iterations times."""
        called_iters = []

        def _mock_iteration(prompt: str, state: LoopState) -> dict:
            called_iters.append(state.iteration)
            return {"iteration": state.iteration, "ok": True}

        state = run_autopolit_loop(
            task="Optimize memory usage",
            project_root=self.temp_dir,
            run_one_iteration=_mock_iteration,
            max_iterations=2,
            iteration_delay_seconds=0.01,
        )

        assert called_iters == [1, 2]
        assert state.iteration == 2
        assert len(state.history) == 2

    def test_autopolit_loop_auto_stop(self):
        """Test that .sage/AUTO-STOP cleanly interrupts the loop."""
        def _mock_iteration(prompt: str, state: LoopState) -> dict:
            # Create stop file during iteration 1
            if state.iteration == 1:
                state.stop_file.parent.mkdir(parents=True, exist_ok=True)
                state.stop_file.touch()
            return {"iteration": state.iteration, "ok": True}

        state = run_autopolit_loop(
            task="Will be stopped early",
            project_root=self.temp_dir,
            run_one_iteration=_mock_iteration,
            max_iterations=5,
            iteration_delay_seconds=0.01,
        )

        assert state.iteration == 1  # Exited before starting iteration 2

    def test_autofleet_loop_parallel_decomposition(self):
        """Test autofleet decomposes and runs subtasks."""
        def _mock_decompose(task, state):
            return [f"Subtask A (iter {state.iteration})", f"Subtask B (iter {state.iteration})"]

        def _mock_subtask(sub, state):
            return {"subtask": sub, "ok": True}

        state = run_autofleet_loop(
            task="Refactor core module",
            project_root=self.temp_dir,
            decompose=_mock_decompose,
            run_one_subtask=_mock_subtask,
            max_iterations=1,
            iteration_delay_seconds=0.01,
        )

        assert state.iteration == 1
        assert len(state.history) == 1
        results = state.history[0]["results"]
        assert len(results) == 2
        assert "Subtask A" in results[0]["subtask"] or "Subtask B" in results[0]["subtask"]

    def test_autoorg_loop_roles(self):
        """Test autoorg assigns roles correctly."""
        def _mock_role(role, prompt, state):
            return {"role": role, "ok": True}

        roles = [("CEO", "Lead"), ("CTO", "Tech")]

        state = run_autoorg_loop(
            task="Scale the company",
            project_root=self.temp_dir,
            run_one_role=_mock_role,
            roles=roles,
            max_iterations=1,
            iteration_delay_seconds=0.01,
        )

        assert state.iteration == 1
        results = state.history[0]["roles"]
        assert len(results) == 2
        role_names = [r["role"] for r in results]
        assert "CEO" in role_names
        assert "CTO" in role_names


# ---------------------------------------------------------------------------
# Phase 2 & 3: CLI Integration Tests (with mocks)
# ---------------------------------------------------------------------------
# Note: For real end-to-end testing, we use the `CliRunner` with the mock LLM
# by relying on the SAGE_TESTING=1 environment variable already set in conftest.


class TestAutonomousCLIIntegration:
    """Test CLI autonomous commands using mocked LLM."""

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.runner = CliRunner()

        # Write a dummy mock response file for testing if necessary
        # The underlying tests use the default mock response if no specific file is found.
        # Ensure we are in a clean env
        os.environ.pop("SAGE_AUTOPOLIT_RUN", None)
        os.environ.pop("SAGE_AUTOPOLIT_TASK", None)

    def teardown_method(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        os.environ.pop("SAGE_AUTOPOLIT_RUN", None)
        os.environ.pop("SAGE_AUTOPOLIT_TASK", None)

    @patch("sage.cli_core.run")
    def test_cli_autopolit_new_project(self, mock_run):
        """Test running `sage autopolit 'task'` sets the right env and calls the loop."""
        # Using CliRunner
        result = self.runner.invoke(app, ["autopolit", "Create a web server"])
        
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert os.environ.get("SAGE_AUTOPOLIT_RUN") == "1"
        assert os.environ.get("SAGE_AUTOPOLIT_TASK") == "Create a web server"

    @patch("sage.cli_core.run")
    def test_cli_autopolit_existing_project(self, mock_run):
        """Test running `sage autopolit` without a task."""
        result = self.runner.invoke(app, ["autopolit"])
        
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert os.environ.get("SAGE_AUTOPOLIT_RUN") == "1"
        assert "SAGE_AUTOPOLIT_TASK" not in os.environ

    @patch("sage.cli_core.run")
    def test_cli_autofleet(self, mock_run):
        """Test running `sage autofleet 'task'` sets the right env and calls the loop."""
        os.environ.pop("SAGE_AUTOFLEET_RUN", None)
        os.environ.pop("SAGE_AUTOFLEET_TASK", None)
        
        result = self.runner.invoke(app, ["autofleet", "Build a dashboard"])
        
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert os.environ.get("SAGE_AUTOFLEET_RUN") == "1"
        assert os.environ.get("SAGE_AUTOFLEET_TASK") == "Build a dashboard"

    @patch("sage.cli_core.run")
    def test_cli_autoorg(self, mock_run):
        """Test running `sage autoorg 'task'` sets the right env and calls the loop."""
        os.environ.pop("SAGE_AUTOORG_RUN", None)
        os.environ.pop("SAGE_AUTOORG_TASK", None)
        
        result = self.runner.invoke(app, ["autoorg", "Refactor the backend"])
        
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert os.environ.get("SAGE_AUTOORG_RUN") == "1"
        assert os.environ.get("SAGE_AUTOORG_TASK") == "Refactor the backend"
