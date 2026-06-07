import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_29():
    """Verify exhaustive task creation via CLI: Generate a basic package.json file...."""
    prompt = "Generate a basic package.json file."
    verify_cli_with_rubric(prompt)
