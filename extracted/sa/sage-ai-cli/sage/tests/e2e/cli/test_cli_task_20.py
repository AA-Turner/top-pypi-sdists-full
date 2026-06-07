import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_20():
    """Verify exhaustive task creation via CLI: Implement a stack data structure in Python...."""
    prompt = "Implement a stack data structure in Python."
    verify_cli_with_rubric(prompt)
