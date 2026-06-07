import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_23():
    """Verify exhaustive task creation via CLI: Generate a basic README template...."""
    prompt = "Generate a basic README template."
    verify_cli_with_rubric(prompt)
