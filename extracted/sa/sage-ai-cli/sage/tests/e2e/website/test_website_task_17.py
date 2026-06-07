import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_17():
    """Verify exhaustive task creation via Website: Write a script to parse a CSV file...."""
    prompt = "Write a script to parse a CSV file."
    verify_website_with_rubric(prompt)
