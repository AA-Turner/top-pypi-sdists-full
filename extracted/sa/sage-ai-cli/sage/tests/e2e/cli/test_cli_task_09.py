import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_09():
    """Verify exhaustive task creation via CLI: Implement a simple calculator class in python...."""
    prompt = "Implement a simple calculator class in python."
    verify_cli_with_rubric(prompt)
