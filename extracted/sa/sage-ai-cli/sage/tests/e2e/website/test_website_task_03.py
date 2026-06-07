import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_03():
    """Verify exhaustive task creation via Website: Write a quick sort algorithm in python...."""
    prompt = "Write a quick sort algorithm in python."
    verify_website_with_rubric(prompt)
