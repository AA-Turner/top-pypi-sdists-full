import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_05():
    """Verify exhaustive task creation via Website: Generate a simple react component...."""
    prompt = "Generate a simple react component."
    verify_website_with_rubric(prompt)
