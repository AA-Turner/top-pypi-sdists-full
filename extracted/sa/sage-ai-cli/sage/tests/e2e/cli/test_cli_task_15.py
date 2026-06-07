import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_15():
    """Verify exhaustive task creation via CLI: Implement binary search in Python...."""
    prompt = "Implement binary search in Python."
    verify_cli_with_rubric(prompt)
