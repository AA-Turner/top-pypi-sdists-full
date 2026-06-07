import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_08():
    """Verify exhaustive task creation via CLI: Create a python function to fetch data from an API..."""
    prompt = "Create a python function to fetch data from an API."
    verify_cli_with_rubric(prompt)
