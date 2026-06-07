import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_02():
    """Verify exhaustive task creation via CLI: Create a python script that prints 'hello world'...."""
    prompt = "Create a python script that prints 'hello world'."
    verify_cli_with_rubric(prompt)
