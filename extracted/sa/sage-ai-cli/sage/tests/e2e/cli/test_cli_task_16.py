import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_16():
    """Verify exhaustive task creation via CLI: Create a gitignore file for python projects...."""
    prompt = "Create a gitignore file for python projects."
    verify_cli_with_rubric(prompt)
