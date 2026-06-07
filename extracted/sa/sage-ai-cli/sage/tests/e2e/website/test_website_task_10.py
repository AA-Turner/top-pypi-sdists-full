import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_10():
    """Verify exhaustive task creation via Website: Write a SQL query to join two tables...."""
    prompt = "Write a SQL query to join two tables."
    verify_website_with_rubric(prompt)
