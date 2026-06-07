import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_17():
    """Verify exhaustive task creation via CLI: Write a script to parse a CSV file...."""
    prompt = "Write a script to parse a CSV file."
    verify_cli_with_rubric(prompt)
