import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_20():
    """Verify exhaustive task creation via Website: Implement a stack data structure in Python...."""
    prompt = "Implement a stack data structure in Python."
    verify_website_with_rubric(prompt)
