import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_11():
    """Verify exhaustive task creation via Website: Create a fast API server with one route...."""
    prompt = "Create a fast API server with one route."
    verify_website_with_rubric(prompt)
