import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_22():
    """Verify exhaustive task creation via CLI: Create a simple Flask application...."""
    prompt = "Create a simple Flask application."
    verify_cli_with_rubric(prompt)
