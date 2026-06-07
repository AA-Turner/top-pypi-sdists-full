import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_13():
    """Verify exhaustive task creation via Website: Write a regex to match email addresses...."""
    prompt = "Write a regex to match email addresses."
    verify_website_with_rubric(prompt)
