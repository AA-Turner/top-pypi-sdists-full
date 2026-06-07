import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_24():
    """Verify exhaustive task creation via CLI: Implement a linked list in python...."""
    prompt = "Implement a linked list in python."
    verify_cli_with_rubric(prompt)
