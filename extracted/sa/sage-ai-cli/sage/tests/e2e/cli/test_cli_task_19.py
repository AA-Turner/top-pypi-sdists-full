import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_19():
    """Verify exhaustive task creation via CLI: Create a simple CSS grid layout...."""
    prompt = "Create a simple CSS grid layout."
    verify_cli_with_rubric(prompt)
