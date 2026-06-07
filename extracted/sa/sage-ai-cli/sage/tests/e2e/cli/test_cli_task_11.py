import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_11():
    """Verify exhaustive task creation via CLI: Create a fast API server with one route...."""
    prompt = "Create a fast API server with one route."
    verify_cli_with_rubric(prompt)
