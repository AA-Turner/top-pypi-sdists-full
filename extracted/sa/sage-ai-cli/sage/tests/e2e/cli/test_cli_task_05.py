import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_05():
    """Verify exhaustive task creation via CLI: Generate a simple react component...."""
    prompt = "Generate a simple react component."
    verify_cli_with_rubric(prompt)
