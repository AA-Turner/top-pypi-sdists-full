import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_09():
    """Verify exhaustive task creation via Website: Implement a simple calculator class in python...."""
    prompt = "Implement a simple calculator class in python."
    verify_website_with_rubric(prompt)
