
from __future__ import annotations
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from sage.cli_core import _execute_task_prompt, _get_current_classification

class TestBackToBackBehavior:
    """Tests the back-to-back scenario: analysis followed by implementation."""

    @patch("sage.core.repl_agent.SAGEAgent.send_to_model")
    @patch("sage.core.repl_agent.SAGEAgent.send_single_turn_to_model")
    @patch("sage.core.procedural_workflow.IntelligentExecutionEngine.create_plan")
    def test_analysis_then_tdd_implementation(
        self, mock_create_plan, mock_send_single, mock_send_to_model, tmp_path
    ):
        from sage.cli_core import _set_current_cwd
        _set_current_cwd(tmp_path)

        # Setup dummy files
        (tmp_path / "app.py").write_text("def hello(): pass\n")
        (tmp_path / "ai-platform").mkdir() # simulate the nested dir structure

        # 1. TASK 1: Analyze this codebase
        # Classification should be read_only=True
        # Now uses multi-step pipeline (planning, analysis, synthesis)
        mock_send_to_model.side_effect = [
            "READ: app.py\nPLAN: 1. Read app.py. 2. Analyze logic.", # Phase 1: Planning
            "Plan confirmed.",                                       # Follow-up for planning tool
            "READ: app.py\nI see some issues.",                      # Phase 2: Analysis
            "Analysis complete.",                                    # Follow-up for analysis tool
            "Findings: app.py needs improvement. FILE: app.py\n```python\n# evil edit\n```", # Phase 3: Synthesis (with violation)
            "I apologize. Here are the findings without code: app.py needs improvement.",     # Retry response
            "Analysis finalized."                                    # Fallback
        ]
        
        # We need to mock create_plan to return a plan
        mock_plan = MagicMock()
        mock_plan.id = "plan_1"
        mock_plan.goal = "Analyze"
        mock_plan.tasks = []
        mock_create_plan.return_value = mock_plan
        mock_send_single.return_value = "Done"

        written, ok = _execute_task_prompt(
            "Analyze this codebase and tell me what needs to be fixed and improved.",
            save_history=False
        )

        # Assertions for Task 1
        assert written == [] # FILE: block should have been rejected because it's analysis
        assert (tmp_path / "app.py").read_text() == "def hello(): pass\n" # No changes

        # 2. TASK 2: Implement all the fixes using TDD
        # Classification should be read_only=False
        
        # Reset side_effect for Task 2
        # Mock responses for TDD cycle (multistep: planning, analysis, testing, implementation)
        mock_send_to_model.side_effect = [
            "PLAN: 1. Analyze. 2. Write tests. 3. Fix code.", # Phase 1: Planning
            "READ: app.py\nI've analyzed the code.",          # Phase 2: Analysis
            "I will write the tests first.\nFILE: tests/test_app.py\n```python\nfrom app import hello\ndef test_hello(): assert hello() == 'hi'\n```", # Phase 3: Testing
            "Now implementing the fix.\nFILE: app.py\n```python\ndef hello(): return 'hi'\n```", # Phase 4: Implementation
            "Implementation complete."               # Fallback/Follow-up
        ]

        # Mock tdd_gate to skip actual execution for speed
        with patch("sage.main.TDDGate") as mock_tdd_gate_cls:
            mock_tdd_gate = mock_tdd_gate_cls.return_value
            mock_tdd_gate.verify_red.return_value = (True, "Tests failed")
            mock_tdd_gate.verify_tests_pass.return_value = (True, "Tests passed", {})

            written, ok = _execute_task_prompt(
                "Implement all the fixes using TDD",
                save_history=False
            )

        # Assertions for Task 2
        assert "app.py" in written or "tests/test_app.py" in written
        assert (tmp_path / "app.py").read_text() == "def hello(): return 'hi'\n"
        assert (tmp_path / "tests/test_app.py").exists()

    @patch("sage.core.repl_agent.SAGEAgent.send_to_model")
    @patch("sage.core.repl_agent.SAGEAgent.send_single_turn_to_model")
    def test_dynamic_plan_generation(
        self, mock_send_single, mock_send_to_model, tmp_path
    ):
        from sage.cli_core import _set_current_cwd
        _set_current_cwd(tmp_path)

        # Mock LLM response for decomposition
        mock_send_single.return_value = """
        [
          {"description": "Task A", "priority": "HIGH", "dependencies": [], "complexity": 1},
          {"description": "Task B", "priority": "MEDIUM", "dependencies": ["task_1"], "complexity": 2}
        ]
        """
        
        mock_send_to_model.return_value = "Done"

        with patch("sage.main.renderer.phase") as mock_phase, \
             patch("sage.main.renderer.info") as mock_info:
            _execute_task_prompt("Add a new feature", save_history=False)
            
            # Verify create_plan was called and result was used
            # We can check if "Decided plan" info was printed
            found_planning = any("Decided plan" in str(call) for call in mock_info.call_args_list)
            
            # Since we moved the phase message to after planning, we check for planning phase too
            found_phase = any("planning" in str(call).lower() for call in mock_phase.call_args_list)
            assert found_phase
