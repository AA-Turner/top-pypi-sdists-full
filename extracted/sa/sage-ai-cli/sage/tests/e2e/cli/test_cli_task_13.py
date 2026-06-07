import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_13():
    """Verify exhaustive task creation via CLI: Write a regex to match email addresses...."""
    prompt = "Write a regex to match email addresses."
    verify_cli_with_rubric(prompt)
