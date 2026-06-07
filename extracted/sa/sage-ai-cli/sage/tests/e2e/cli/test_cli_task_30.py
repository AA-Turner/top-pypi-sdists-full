import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_30():
    """Verify exhaustive task creation via CLI: Write a python script to send an email...."""
    prompt = "Write a python script to send an email."
    verify_cli_with_rubric(prompt)
