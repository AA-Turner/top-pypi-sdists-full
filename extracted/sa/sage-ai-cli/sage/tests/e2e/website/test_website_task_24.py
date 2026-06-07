import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_24():
    """Verify exhaustive task creation via Website: Implement a linked list in python...."""
    prompt = "Implement a linked list in python."
    verify_website_with_rubric(prompt)
