import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_27():
    """Verify exhaustive task creation via CLI: Create a basic nginx configuration file...."""
    prompt = "Create a basic nginx configuration file."
    verify_cli_with_rubric(prompt)
