import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_15():
    """Verify exhaustive task creation via Website: Implement binary search in Python...."""
    prompt = "Implement binary search in Python."
    verify_website_with_rubric(prompt)
