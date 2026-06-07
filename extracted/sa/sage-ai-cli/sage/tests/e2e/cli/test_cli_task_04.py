import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_04():
    """Verify exhaustive task creation via CLI: Build a basic HTML landing page...."""
    prompt = "Build a basic HTML landing page."
    verify_cli_with_rubric(prompt)
