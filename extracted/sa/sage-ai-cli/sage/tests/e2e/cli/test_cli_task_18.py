import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_18():
    """Verify exhaustive task creation via CLI: Generate a basic GitHub Actions workflow...."""
    prompt = "Generate a basic GitHub Actions workflow."
    verify_cli_with_rubric(prompt)
