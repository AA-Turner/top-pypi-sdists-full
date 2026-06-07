import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_10():
    """Verify exhaustive task creation via CLI: Write a SQL query to join two tables...."""
    prompt = "Write a SQL query to join two tables."
    verify_cli_with_rubric(prompt)
