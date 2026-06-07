import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_25():
    """Verify exhaustive task creation via CLI: Create a python script to scrape a webpage...."""
    prompt = "Create a python script to scrape a webpage."
    verify_cli_with_rubric(prompt)
