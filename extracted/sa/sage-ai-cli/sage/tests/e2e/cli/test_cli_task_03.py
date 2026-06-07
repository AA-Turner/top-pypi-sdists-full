import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_03():
    """Verify exhaustive task creation via CLI: Write a quick sort algorithm in python...."""
    prompt = "Write a quick sort algorithm in python."
    verify_cli_with_rubric(prompt)
