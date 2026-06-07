import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_06():
    """Verify exhaustive task creation via CLI: Create a Dockerfile for a node app...."""
    prompt = "Create a Dockerfile for a node app."
    verify_cli_with_rubric(prompt)
