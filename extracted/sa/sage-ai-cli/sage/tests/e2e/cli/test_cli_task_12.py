import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_12():
    """Verify exhaustive task creation via CLI: Generate a JSON schema for a user profile...."""
    prompt = "Generate a JSON schema for a user profile."
    verify_cli_with_rubric(prompt)
