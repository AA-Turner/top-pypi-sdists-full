import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_07():
    """Verify exhaustive task creation via CLI: Write a bash script to backup a directory...."""
    prompt = "Write a bash script to backup a directory."
    verify_cli_with_rubric(prompt)
