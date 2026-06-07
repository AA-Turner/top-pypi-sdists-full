import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_26():
    """Verify exhaustive task creation via Website: Write a simple unit test using pytest...."""
    prompt = "Write a simple unit test using pytest."
    verify_website_with_rubric(prompt)
