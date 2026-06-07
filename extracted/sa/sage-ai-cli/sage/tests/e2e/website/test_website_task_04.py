import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_04():
    """Verify exhaustive task creation via Website: Build a basic HTML landing page...."""
    prompt = "Build a basic HTML landing page."
    verify_website_with_rubric(prompt)
