import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_28():
    """Verify exhaustive task creation via CLI: Implement a queue data structure in Python...."""
    prompt = "Implement a queue data structure in Python."
    verify_cli_with_rubric(prompt)
